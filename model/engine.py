# -*- coding: utf-8 -*-
"""Monthly cash-flow engine (vectorized over simulations) for the Panama tender distributor.
Deterministic mode = expected values, replicable cell by cell in the Excel model.
Monte Carlo mode = discrete draws (registrations, tender wins), supply failure and stage gates.

Audit corrections (9 Oct 2026), each one can be switched off through `fixes` to reproduce the previous version:
 - 'bond_tail'      performance bonds stay in force after each contract (LPU: contract + 3 months; MINSA: + 6 months),
                    so consecutive bonds overlap and their collateral is tied up twice for those months
 - 'reg_before_bid' the sanitary registration must exist when the offer is submitted (bid_m months before the contract);
                    if the first window is missed, the first centralized contract moves to the next 15-month cycle
 - 'wave2_cycle'    second-wave products enter centralized contracts only at the next LPU (15-month) or MINSA (12-month)
                    cycle for which they are registered before the offer and in stock at the start
 - 'est_tax'        income tax paid through the Panamanian estimated-tax installments (June, September, December of the
                    current year, on the prior year's tax) plus the balance in March
 - 'aviso_cap'      aviso de operación capped at B/.60,000 a year
 - 'forfeit_full'   on involuntary failure the insurer pays the full performance bond and recovers it from the company
                    (collateral plus the uncollateralized part), not only the collateral
 - 'close_distrib'  after a closure the company is wound down and its remaining cash is returned to the shareholders
                    instead of waiting until month 60
 - 'pipeline_loss'  on involuntary failure the advances and balances already paid for goods not yet received are lost
"""
import numpy as np
from inputs import SKUS, P, FIXED, SETUP, ANNUAL_CHARGES, LIC_M, RS_PAY_M, FIXED_KIND, SETUP_KIND, ANNUAL_KIND

T = 60
SC = {'pes': 2, 'base': 3, 'opt': 4}
SCF = {'pes': 1, 'base': 2, 'opt': 3}
ALL_FIXES = frozenset({'bond_tail', 'reg_before_bid', 'wave2_cycle', 'est_tax', 'aviso_cap', 'forfeit_full',
                       'close_distrib', 'pipeline_loss'})
AVISO_CAP = 60000.0


def scenario_params(sc='base'):
    i = SC[sc]
    p = {k: v[i] for k, v in P.items()}
    p['fixed'] = [f[SCF[sc]] for f in FIXED]
    p['setup'] = [s[SCF[sc]] for s in SETUP]
    return p


def rhu(x):
    """round half up (matches Excel ROUND for positive numbers)"""
    return np.floor(np.asarray(x, dtype=float) + 0.5)


def _arr(x, n):
    a = np.asarray(x, dtype=float)
    return np.broadcast_to(a, (n,)).copy() if a.ndim == 0 else a.astype(float)


def sku_arrays():
    fob = np.array([s['fob'] for s in SKUS])
    adder = np.array([s['adder'] for s in SKUS])
    q = np.array([[s['q%d' % c] for s in SKUS] for c in (1, 2, 3, 4)], dtype=float)
    pr = np.array([[s['p%d' % c] for s in SKUS] for c in (1, 2, 3, 4)], dtype=float)
    inc = np.array([s['inc'] for s in SKUS], dtype=float)
    return fob, adder, q, pr, inc


def _next_cycle(start, need, length):
    """first contract start >= need on a calendar of cycles of `length` months that begins at `start`"""
    return start + length * np.ceil(np.maximum(0, need - start) / length).astype(int)


def run(p, n=1, mc=None, inc_override=None, signaturelex=False, fixes=None):
    F = ALL_FIXES if fixes is None else frozenset(fixes)
    S = len(SKUS)
    g = {k: _arr(v, n) for k, v in p.items() if k not in ('fixed', 'setup')}
    for k, dflt in (('bond_tail_css', 3.0), ('bond_tail_minsa', 6.0), ('forfeit_frac', 1.0)):
        if k not in g:
            g[k] = np.full(n, dflt)
    fixed = np.stack([_arr(v, n) for v in p['fixed']], axis=1)
    setup = np.stack([_arr(v, n) for v in p['setup']], axis=1)
    if signaturelex:
        sl = np.array([s[5] for s in SETUP], dtype=float)
        setup[:, sl > 0] = sl[sl > 0]
        g['rs_law'] = np.full(n, 1350.0)
        g['rs_iea'] = np.full(n, 1500.0)   # SignatureLex lists B/.1,500 "formula revision" per product
    # employer on-costs on staff lines, non-recoverable ITBMS on purchased services
    kmult = {'staff': 1 + g['oncost'], 'service': 1 + g['itbms_srv'], 'other': np.ones(n)}
    fixed = fixed * np.stack([kmult[k] for k in FIXED_KIND], axis=1)
    setup = setup * np.stack([kmult[k] for k in SETUP_KIND], axis=1)
    annual_amt = sum(a[1] * kmult[k] for a, k in zip(ANNUAL_CHARGES, ANNUAL_KIND))

    fob, adder, q0, pr, inc = sku_arrays()
    # demanda del MINSA centralizado: la compra conjunta de 2023 solo cuenta en la fracción cc_w
    cc_mask = np.array([s.get('c2', 'cc') == 'cc' for s in SKUS])
    q = np.broadcast_to(q0[:, None, :], (4, n, S)).copy()
    q[1] = q[1] * np.where(cc_mask[None, :], g['cc_w'][:, None], 1.0)
    if inc_override is not None:
        inc = np.asarray(inc_override, dtype=float)
    inc = np.broadcast_to(inc, (n, S))

    fob_part = fob[None, :] * g['sup_idx'][:, None] * (1 + g['pack'][:, None])
    unit_cost = fob_part + adder[None, :] * g['log_mult'][:, None]
    pf = np.stack([g['pf_cen'], g['pf_cen'], g['pf_dec'], g['pf_dec']])
    ourp = pr[:, None, :] * pf[:, :, None]
    with np.errstate(divide='ignore', invalid='ignore'):
        ratio = np.where(ourp > 0, unit_cost[None] / ourp, 0.0)
        gm = np.where(ourp > 0, 1 - unit_cost[None] / ourp, -9.0)
    gmmin = np.stack([g['gm_cen'], g['gm_cen'], g['gm_dec'], g['gm_dec']])[:, :, None]
    go = (q > 0) & (gm >= gmmin) & (inc[None] > 0)

    rs_ok = (mc['rs_ok'] if mc is not None else np.broadcast_to(g['rs_succ'][:, None], (n, S))) * inc
    base_rev = go * q * g['mkt'][None, :, None] * ourp * rs_ok[None]
    Rd = base_rev[2:] * g['share_dec'][None, :, None]
    # MINSA reverse auctions are for fixed quantities: optional separate realization ('realiz_minsa'); default = realiz
    real = np.stack([g['realiz'], g.get('realiz_minsa', g['realiz'])])
    Rc = base_rev[:2] * real[:, :, None]

    lead_m = rhu(g['lead_days'] / 30).astype(int)
    dso_m = rhu(g['dso_days'] / 30).astype(int)
    credit_m = rhu(g['credit_days'] / 30).astype(int)
    ship_m = rhu(g['ship_m']).astype(int)
    reg_m = rhu(g['reg_m']).astype(int)
    bid_m = rhu(g['bid_m']).astype(int)
    first_dec = reg_m + lead_m
    cen0 = rhu(g['cen_start']).astype(int)
    if 'reg_before_bid' in F:
        # the offer needs the sanitary registration (pliego LPU: registro sanitario no subsanable)
        cen0 = _next_cycle(cen0, reg_m + bid_m, 15)
    cen_start = np.maximum(cen0, first_dec)
    rt = np.maximum(reg_m - RS_PAY_M, 1)                      # months from filing to approval
    n2 = g['n2'] * (mc['wave2'] if mc is not None else 1.0)
    m2 = rhu(g['m2']).astype(int)
    first_dec2 = m2 + rt + lead_m
    n1 = np.maximum(inc.sum(axis=1), 1)
    k2 = n2 * g['rel2'] / n1

    t = np.arange(1, T + 2)
    year = (np.minimum(t, T) - 1) // 12 + 1
    eros = (1 - g['erosion'][:, None]) ** (year[None, :] - 1)
    ramp = np.clip((t[None, :] - first_dec[:, None] + 1) / g['ramp_m'][:, None], 0, 1)
    ramp2 = np.clip((t[None, :] - first_dec2[:, None] + 1) / g['ramp_m'][:, None], 0, 1)
    cen_on = (t[None, :] >= cen_start[:, None]).astype(float)
    if 'wave2_cycle' in F:
        c2_lpu = _next_cycle(cen_start, np.maximum(first_dec2, m2 + rt + bid_m), 15)
        c2_minsa = _next_cycle(cen_start, np.maximum(first_dec2, m2 + rt + 1), 12)
    else:
        c2_lpu = c2_minsa = np.maximum(cen_start, first_dec2)
    cen2_on1 = (t[None, :] >= c2_lpu[:, None]).astype(float)
    cen2_on2 = (t[None, :] >= c2_minsa[:, None]).astype(float)
    mult_dec = 1 + k2[:, None] * ramp2
    mult_cen1 = 1 + k2[:, None] * cen2_on1                      # LPU (CSS)
    mult_cen2 = 1 + k2[:, None] * cen2_on2                      # MINSA

    if mc is None:
        w1 = np.broadcast_to(g['pwin_cen'][:, None, None], (n, S, T + 1))
        w2 = np.broadcast_to((g['pwin_cen'] * g['minsa_occ'])[:, None, None], (n, S, T + 1))
        w1p, w2p = w1, w2
    else:
        k1i = np.clip((t[None, :] - cen_start[:, None]) // 15, 0, 5)
        k2i = np.clip((t[None, :] - cen_start[:, None]) // 12, 0, 5)
        w1 = np.take_along_axis(mc['win1'], np.broadcast_to(k1i[:, None, :], (n, S, T + 1)), axis=2)
        w2 = np.take_along_axis(mc['win2'], np.broadcast_to(k2i[:, None, :], (n, S, T + 1)), axis=2)
        k1p = np.clip(k1i - 1, 0, 5); k2p = np.clip(k2i - 1, 0, 5)
        w1p = np.take_along_axis(mc['win1'], np.broadcast_to(k1p[:, None, :], (n, S, T + 1)), axis=2)
        w2p = np.take_along_axis(mc['win2'], np.broadcast_to(k2p[:, None, :], (n, S, T + 1)), axis=2)
    stop_m = (mc['stop_m'] if (mc is not None and 'stop_m' in mc) else rhu(g['stop_det']).astype(int))
    active = (t[None, :] <= stop_m[:, None]).astype(float)
    forfeit = mc['forfeit'] if (mc is not None and 'forfeit' in mc) else np.zeros(n)
    inv_rec = mc['inv_rec'] if (mc is not None and 'inv_rec' in mc) else g['inv_liq']

    dec_rev = (Rd.sum(axis=(0, 2)))[:, None] / 12 * ramp * mult_dec
    dec_cogs = ((Rd * ratio[2:]).sum(axis=(0, 2)))[:, None] / 12 * ramp * mult_dec
    c_rev_raw = ((Rc[0][:, :, None] * w1).sum(axis=1) * mult_cen1 + (Rc[1][:, :, None] * w2).sum(axis=1) * mult_cen2) / 12 * cen_on
    c_cogs = (((Rc[0] * ratio[0])[:, :, None] * w1).sum(axis=1) * mult_cen1
              + ((Rc[1] * ratio[1])[:, :, None] * w2).sum(axis=1) * mult_cen2) / 12 * cen_on
    Rmax = base_rev[:2]                                         # contract value at maximum quantity
    bond_base = ((Rmax[0][:, :, None] * w1).sum(axis=1) * g['bond_css'][:, None] * 15 / 12 * mult_cen1
                 + (Rmax[1][:, :, None] * w2).sum(axis=1) * g['bond_minsa'][:, None] * mult_cen2) * cen_on
    if 'bond_tail' in F:
        # the bond of the previous contract is still in force during the first months of the next one
        dt = t[None, :] - cen_start[:, None]
        tail1 = rhu(g['bond_tail_css']).astype(int); tail2 = rhu(g['bond_tail_minsa']).astype(int)
        ov1 = ((dt >= 15) & ((dt % 15) < tail1[:, None])).astype(float)
        ov2 = ((dt >= 12) & ((dt % 12) < tail2[:, None])).astype(float)
        bond_base = bond_base + ((Rmax[0][:, :, None] * w1p).sum(axis=1) * g['bond_css'][:, None] * 15 / 12 * mult_cen1 * ov1
                                 + (Rmax[1][:, :, None] * w2p).sum(axis=1) * g['bond_minsa'][:, None] * mult_cen2 * ov2) * cen_on
    # bid bond of 10% on every LPU offer, held bid_m months before each contract: Ley 419 art. 245 and the tender
    # (cl. 8.14) apply the B/.70,000 threshold to the reference price of the whole act (B/.95.3 million in LPU 01-2026),
    # so every renglon offered carries it (audit fix of 9-oct-2026: the old rule applied it per renglon)
    thr = (q0[0] > 0).astype(float)
    bid_val = (base_rev[0] * thr[None, :]).sum(axis=1) * 15 / 12
    start_b = cen_start - bid_m
    cyc = (t[None, :] >= start_b[:, None]) & (((t[None, :] - start_b[:, None]) % 15) < bid_m[:, None])
    bid_bonded = g['bid_bond'][:, None] * bid_val[:, None] * cyc * mult_cen1
    rev_dec = dec_rev * eros * active
    rev_cen = c_rev_raw * eros * active
    cogs_dec = dec_cogs * active
    cogs_cen = c_cogs * active
    rev = rev_dec + rev_cen
    cogs = cogs_dec + cogs_cen

    inv = np.zeros((n, T + 1))
    # inventory target uses next month's planned activity (not masked by closure) so that stock on hand
    # at closure is liquidated, never 'returned' through negative purchases
    inv[:, :T] = dec_cogs[:, 1:T + 1] * g['cover_m'][:, None] + c_cogs[:, 1:T + 1] * g['cen_stock_m'][:, None]
    inv[:, T] = inv[:, T - 1]
    inv_plan = inv * (t[None, :] >= first_dec[:, None])
    inv *= (t[None, :] >= first_dec[:, None]) * (t[None, :] <= stop_m[:, None])
    inv_prev = np.concatenate([np.zeros((n, 1)), inv[:, :-1]], axis=1)
    arrivals = cogs * (1 + g['expiry'][:, None]) + inv - inv_prev
    after_stop = t[None, :] > stop_m[:, None]
    # at closure the remaining stock is liquidated (cash in next month), never 'returned' through negative purchases
    inv_at_stop = np.where(stop_m <= T, inv[np.arange(n), np.clip(stop_m - 1, 0, T)], 0.0)
    arrivals = np.where(after_stop, 0.0, arrivals)
    inv = np.where(after_stop, 0.0, inv)
    arrivals[:, T] = 0.0

    def shift(a, k):
        out = np.zeros((n, T))
        idx = np.arange(T)[None, :] + k[:, None]
        valid = (idx >= 0) & (idx < T)
        out[valid] = a[np.nonzero(valid)[0], idx[valid]]
        return out

    arr60 = arrivals[:, :T]; rev60 = rev[:, :T]; cogs60 = cogs[:, :T]
    pay = g['adv'][:, None] * shift(arr60, lead_m) + (1 - g['adv'][:, None]) * shift(arr60, ship_m - credit_m)
    tt = np.arange(1, T + 1)
    lost_pipe = np.zeros(n)
    if 'pipeline_loss' in F:
        # goods ordered before an involuntary stop and due to arrive after it: what was already paid is lost
        inv_plan_prev = np.concatenate([np.zeros((n, 1)), inv_plan[:, :-1]], axis=1)
        arr_plan = (dec_cogs + c_cogs) * (1 + g['expiry'][:, None]) + inv_plan - inv_plan_prev
        arr_post = np.where(after_stop, np.maximum(arr_plan, 0.0), 0.0)[:, :T]
        pay_post = g['adv'][:, None] * shift(arr_post, lead_m) + (1 - g['adv'][:, None]) * shift(arr_post, ship_m - credit_m)
        pre = (tt[None, :] <= stop_m[:, None]) & (forfeit[:, None] > 0)
        pay_lost = np.where(pre, pay_post, 0.0)
        pay = pay + pay_lost
        lost_pipe = pay_lost.sum(axis=1)
    f = g['fact_share'][:, None]
    bd = g['baddebt'][:, None]
    one = np.ones(n, dtype=int)
    coll = (1 - f) * shift(rev60, -dso_m) * (1 - bd) + f * shift(rev60, -one) * (1 - bd) * (1 - g['fact_cost'][:, None] * dso_m[:, None])
    liq = np.zeros((n, T))
    sm = np.clip(stop_m, 0, T - 1)          # index of month stop+1
    has = stop_m < T
    liq[np.arange(n)[has], sm[has]] = (inv_at_stop * inv_rec)[has]
    coll = coll + liq
    fact_exp = f * rev60 * (1 - bd) * g['fact_cost'][:, None] * dso_m[:, None]

    var = (g['dist'] + g['penal'])[:, None] * rev60
    fixed_m = np.zeros((n, T))
    for j, fx in enumerate(FIXED):
        if fx[4] == 'm1':
            st = np.full(n, 1)
        elif fx[4] == 'lic':
            st = np.full(n, LIC_M)
        elif fx[4] == 'cen':
            st = cen_start
        else:
            st = np.maximum(reg_m - 1, 1)
        fixed_m += fixed[:, j][:, None] * (tt[None, :] >= st[:, None])
    dormant = tt[None, :] > (stop_m[:, None] + 3)          # company wound down 3 months after closure
    fixed_m = np.where(dormant, 0.0, fixed_m)
    rs_unit = g['rs_off'] + g['rs_iea'] + (g['rs_law'] + g['rs_trad']) * (1 + g['itbms_srv']) + g['rs_smp']
    n_reg1 = rs_ok.sum(axis=1)
    n_reg2 = n2 * (g['rs_succ'] if mc is None else mc['rs2_frac'])
    postreg = (n_reg1 * g['postreg'] / 12)[:, None] * (tt[None, :] >= reg_m[:, None]) \
            + (n_reg2 * g['postreg'] / 12)[:, None] * (tt[None, :] >= (m2 + rt)[:, None])
    setup_m = np.zeros((n, T))
    for j, s in enumerate(SETUP):
        if s[4] >= 1:
            setup_m[:, s[4] - 1] += setup[:, j]
    phase0 = sum(setup[:, j] for j, s in enumerate(SETUP) if s[4] == 0)
    n_filed = inc.sum(axis=1)
    rs_m = np.zeros((n, T)); rs_m[:, RS_PAY_M - 1] = n_filed * rs_unit
    m2c = np.clip(m2, 1, T)
    rs_m[np.arange(n), m2c - 1] += n2 * rs_unit
    annual = np.zeros((n, T))
    for m in (1, 13, 25, 37, 49):
        annual[:, m - 1] = annual_amt
    annual = np.where(dormant, 0.0, annual)
    postreg = np.where(dormant, 0.0, postreg)

    bonded = (bond_base + bid_bonded)[:, :T] * active[:, :T]
    collat = bonded * g['collat'][:, None]
    dcoll = np.diff(np.concatenate([np.zeros((n, 1)), collat], axis=1), axis=1)
    # involuntary failure: the State executes the performance bond, collateral is not returned
    dcoll = np.where((dcoll < 0) & (forfeit[:, None] > 0), 0.0, dcoll)
    stop_idx = np.clip(stop_m - 1, 0, T - 1)
    lost_coll = np.where(forfeit > 0, np.where(has, collat[np.arange(n), stop_idx], 0.0), 0.0)
    bond_call = np.zeros((n, T))
    if 'forfeit_full' in F:
        # the insurer pays the State the performance bond and recovers from the company what the collateral does not cover
        perf_at_stop = (bond_base[:, :T] * active[:, :T])[np.arange(n), stop_idx]
        extra = np.where((forfeit > 0) & has, np.maximum(0.0, g['forfeit_frac'] - g['collat']) * perf_at_stop, 0.0)
        bond_call[np.arange(n)[has], sm[has]] = extra[has]
    prem = bonded * g['bond_prem'][:, None] / 12

    inv_loss = np.zeros((n, T))
    inv_loss[np.arange(n)[has], sm[has]] = (inv_at_stop * (1 - inv_rec))[has] + lost_coll[has] + lost_pipe[has]
    inv_loss += bond_call
    income = (rev60 - cogs60 * (1 + g['expiry'][:, None]) - var - rev60 * bd - fact_exp
              - fixed_m - postreg - setup_m - rs_m - annual - prem - inv_loss)
    Y = income.reshape(n, 5, 12).sum(axis=2)
    revY = rev60.reshape(n, 5, 12).sum(axis=2)
    tax = np.zeros((n, 5))
    for y in range(5):
        pool = np.zeros(n)
        for k in range(max(0, y - 5), y):
            pool += 0.2 * np.maximum(0, -Y[:, k])
        ded = np.minimum(0.5 * np.maximum(0, Y[:, y]), pool)
        isr = g['isr'] * (np.maximum(0, Y[:, y]) - ded)
        cair = np.where(revY[:, y] > 1_500_000, 0.011675 * revY[:, y], 0)
        tax[:, y] = np.maximum(isr, cair)
    taxpay = np.zeros((n, T))
    if 'est_tax' in F:
        # Código Fiscal art. 710: estimated tax for the current year (at least the prior year's) in June, September and
        # December; the balance with the annual return in March of the following year
        for y in range(1, 5):
            for mm_ in (6, 9, 12):
                taxpay[:, 12 * y + mm_ - 1] += tax[:, y - 1] / 3
        for y in range(4):
            taxpay[:, 12 * (y + 1) + 2] += tax[:, y] - (tax[:, y - 1] if y >= 1 else 0.0)
        tax_due_T = tax[:, 4] - tax[:, 3]
    else:
        for y in range(4):
            taxpay[:, 12 * (y + 1) + 2] = tax[:, y]
        tax_due_T = tax[:, 4]
    NI = Y - tax
    cap = AVISO_CAP if 'aviso_cap' in F else np.inf

    cash = np.zeros((n, T)); inj = np.zeros((n, T)); div = np.zeros((n, T)); aviso = np.zeros((n, T))
    ret = np.zeros((n, T)); ret_tax = np.zeros((n, T))
    mincash = g['mincash_m'][:, None] * fixed_m
    c_prev = np.zeros(n); cum_div = np.zeros(n); cum_ret = np.zeros(n); cum_inj = np.zeros(n)
    for i in range(T):
        m = i + 1
        if m in (15, 27, 39, 51):     # aviso de operación on equity at the previous year end, paid in March
            y = (m - 3) // 12
            pat = inj[:, :12 * y].sum(axis=1) + NI[:, :y].sum(axis=1) - div[:, :12 * y].sum(axis=1) - ret[:, :12 * y].sum(axis=1)
            aviso[:, i] = np.where(m <= stop_m + 3, np.minimum(cap, np.maximum(100.0, g['aviso'] * np.maximum(pat, 0))), 0.0)
        pre = (c_prev + coll[:, i] - pay[:, i] - var[:, i] - fixed_m[:, i] - postreg[:, i] - setup_m[:, i]
               - rs_m[:, i] - annual[:, i] - dcoll[:, i] - prem[:, i] - taxpay[:, i] - aviso[:, i] - bond_call[:, i])
        inj[:, i] = np.maximum(0, mincash[:, i] - pre)
        cum_inj += inj[:, i]
        c = pre + inj[:, i]
        if m in (24, 36, 48):
            y = m // 12
            distributable = np.maximum(0, NI[:, :y].sum(axis=1) - cum_div)
            avail = c - 2 * mincash[:, i] - tax[:, y - 1]
            d = g['payout'] * np.maximum(0, np.minimum(avail, distributable))
            div[:, i] = d; cum_div += d; c = c - d
        if 'close_distrib' in F and m < T:
            # wound-down company: cash goes back to the shareholders (return of capital first, then taxed as dividend)
            r_ = np.where(dormant[:, i], np.maximum(0.0, c), 0.0)
            taxable = np.maximum(0, cum_ret + r_ - cum_inj) - np.maximum(0, cum_ret - cum_inj)
            ret[:, i] = r_; ret_tax[:, i] = g['divtax'] * taxable; cum_ret += r_; c = c - r_
        cash[:, i] = c; c_prev = c

    recv = np.zeros(n)
    for k in range(int(dso_m.max()) + 1):
        recv += np.where(k < dso_m, rev60[:, T - 1 - k] * (1 - g['baddebt']) * (1 - g['fact_share']), 0)
    recv += g['fact_share'] * rev60[:, T - 1] * (1 - g['baddebt']) * (1 - g['fact_cost'] * dso_m)
    payables = np.zeros(n)
    lagb = credit_m - ship_m
    for k in range(int(max(lagb.max(), 0)) + 1):
        payables += np.where(k < lagb, (1 - g['adv']) * arr60[:, T - 1 - k], 0)
    nwc = recv + inv[:, T - 1] + collat[:, T - 1] - payables
    pat5 = inj.sum(axis=1) + NI.sum(axis=1) - div.sum(axis=1) - ret.sum(axis=1)
    aviso5 = np.where(T <= stop_m + 3, np.minimum(cap, np.maximum(100.0, g['aviso'] * np.maximum(pat5, 0))), 0.0)
    taxY5 = tax_due_T + aviso5
    tv_liq = cash[:, T - 1] + g['recov'] * nwc - taxY5
    tv_gc = cash[:, T - 1] - taxY5 + g['gc_mult'] * np.maximum(0, NI[:, 4])
    tv_best = np.maximum(tv_liq, tv_gc)
    eq_in = inj.sum(axis=1)

    out = dict(rev=rev60, rev_dec=rev_dec[:, :T], rev_cen=rev_cen[:, :T], cogs=cogs60, arrivals=arr60, inv=inv[:, :T],
               pay=pay, coll=coll, var=var, fixed=fixed_m, postreg=postreg, setup=setup_m, rs=rs_m, annual=annual,
               collat=collat, prem=prem, fact_exp=fact_exp, aviso=aviso, aviso5=aviso5, bid_val=bid_val, bid_bonded=bid_bonded[:, :T], income=income, Y=Y, tax=tax, NI=NI, taxpay=taxpay, cash=cash,
               inj=inj, div=div, ret=ret, bond_call=bond_call, phase0=phase0, eq_in=eq_in, recv=recv, nwc=nwc, payables=payables, tv_liq=tv_liq,
               tv_gc=tv_gc, tv_best=tv_best, unit_cost=unit_cost, ourp=ourp, gm=gm, go=go, Rd=Rd, Rc=Rc,
               fob_part=fob_part, ratio=ratio, lead_m=lead_m, dso_m=dso_m, first_dec=first_dec, cen_start=cen_start,
               first_dec2=first_dec2, c2_lpu=c2_lpu, c2_minsa=c2_minsa, revY=revY, mincash=mincash, rs_unit=rs_unit, n_filed=n_filed, k2=k2,
               mult_dec=mult_dec[:, :T], mult_cen=mult_cen1[:, :T], mult_cen2=mult_cen2[:, :T], ramp=ramp[:, :T], eros=eros[:, :T])
    r_m = (1 + g['disc']) ** (1 / 12) - 1
    ret_net = ret - ret_tax
    for tag, tv in (('liq', tv_liq), ('best', tv_best)):
        tvnet = tv - g['divtax'] * np.maximum(0, tv - np.maximum(0, eq_in - cum_ret))
        cf = np.zeros((n, T + 1))
        cf[:, 0] = -phase0
        cf[:, 1:] = -inj + div * (1 - g['divtax'][:, None]) + ret_net
        cf[:, T] += tvnet
        out['cf_' + tag] = cf
        disc = (1 + r_m[:, None]) ** (-np.arange(T + 1)[None, :])
        out['npv_' + tag] = (cf * disc).sum(axis=1)
        disc15 = (1.15 ** (1 / 12)) ** (-np.arange(T + 1)[None, :])
        out['npv15_' + tag] = (cf * disc15).sum(axis=1)
        pos = np.where(cf > 0, cf, 0).sum(axis=1); neg = -np.where(cf < 0, cf, 0).sum(axis=1)
        out['moic_' + tag] = np.where(neg > 0, pos / neg, np.nan)
        out['tvnet_' + tag] = tvnet
    w = (Rd * ratio[2:]).sum(axis=0) + (Rc * ratio[:2]).sum(axis=0)
    fob_share = np.where(unit_cost > 0, fob_part / unit_cost, 0)
    wsum = w.sum(axis=1)
    out['fob_share'] = np.where(wsum > 0, (w * fob_share).sum(axis=1) / np.where(wsum > 0, wsum, 1), 0)
    out['zywie_profit'] = arr60.sum(axis=1) * out['fob_share'] * g['zy_markup'] / (1 + g['zy_markup'])
    return out


def irr(cf_row):
    c = np.asarray(cf_row, dtype=float)
    if not (c.min() < 0 < c.max()):
        return np.nan
    tt = np.arange(len(c))
    f = lambda r: (c / (1 + r) ** tt).sum()
    lo, hi = -0.95, 1.5
    flo, fhi = f(lo), f(hi)
    if flo * fhi > 0:
        return np.nan
    for _ in range(100):
        mid = (lo + hi) / 2; fm = f(mid)
        if flo * fm <= 0: hi = mid
        else: lo, flo = mid, fm
    return (1 + (lo + hi) / 2) ** 12 - 1


def irr_rows(cf):
    return np.array([irr(r) for r in cf])
