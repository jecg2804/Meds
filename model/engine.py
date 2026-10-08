# -*- coding: utf-8 -*-
"""Monthly cash-flow engine (vectorized over simulations) for the Panama tender distributor.
Deterministic mode = expected values, replicable cell by cell in the Excel model.
Monte Carlo mode = discrete draws (registrations, tender wins), supply failure and stage gates.
"""
import numpy as np
from inputs import SKUS, P, FIXED, SETUP, ANNUAL_CHARGES, LIC_M, RS_PAY_M, FIXED_KIND, SETUP_KIND, ANNUAL_KIND

T = 60
SC = {'pes': 2, 'base': 3, 'opt': 4}
SCF = {'pes': 1, 'base': 2, 'opt': 3}


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


def run(p, n=1, mc=None, inc_override=None, signaturelex=False):
    S = len(SKUS)
    g = {k: _arr(v, n) for k, v in p.items() if k not in ('fixed', 'setup')}
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

    fob, adder, q, pr, inc = sku_arrays()
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
    go = (q[:, None, :] > 0) & (gm >= gmmin) & (inc[None] > 0)

    rs_ok = (mc['rs_ok'] if mc is not None else np.broadcast_to(g['rs_succ'][:, None], (n, S))) * inc
    base_rev = go * q[:, None, :] * g['mkt'][None, :, None] * ourp * rs_ok[None]
    Rd = base_rev[2:] * g['share_dec'][None, :, None]
    Rc = base_rev[:2] * g['realiz'][None, :, None]

    lead_m = rhu(g['lead_days'] / 30).astype(int)
    dso_m = rhu(g['dso_days'] / 30).astype(int)
    credit_m = rhu(g['credit_days'] / 30).astype(int)
    ship_m = rhu(g['ship_m']).astype(int)
    reg_m = rhu(g['reg_m']).astype(int)
    first_dec = reg_m + lead_m
    cen_start = np.maximum(rhu(g['cen_start']).astype(int), first_dec)
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
    cen2_on = (t[None, :] >= np.maximum(cen_start, first_dec2)[:, None]).astype(float)
    mult_dec = 1 + k2[:, None] * ramp2
    mult_cen = 1 + k2[:, None] * cen2_on

    if mc is None:
        w1 = np.broadcast_to(g['pwin_cen'][:, None, None], (n, S, T + 1))
        w2 = np.broadcast_to((g['pwin_cen'] * g['minsa_occ'])[:, None, None], (n, S, T + 1))
    else:
        k1i = np.clip((t[None, :] - cen_start[:, None]) // 15, 0, 5)
        k2i = np.clip((t[None, :] - cen_start[:, None]) // 12, 0, 5)
        w1 = np.take_along_axis(mc['win1'], np.broadcast_to(k1i[:, None, :], (n, S, T + 1)), axis=2)
        w2 = np.take_along_axis(mc['win2'], np.broadcast_to(k2i[:, None, :], (n, S, T + 1)), axis=2)
    stop_m = (mc['stop_m'] if (mc is not None and 'stop_m' in mc) else rhu(g['stop_det']).astype(int))
    active = (t[None, :] <= stop_m[:, None]).astype(float)
    forfeit = mc['forfeit'] if (mc is not None and 'forfeit' in mc) else np.zeros(n)
    inv_rec = mc['inv_rec'] if (mc is not None and 'inv_rec' in mc) else g['inv_liq']

    dec_rev = (Rd.sum(axis=(0, 2)))[:, None] / 12 * ramp * mult_dec
    dec_cogs = ((Rd * ratio[2:]).sum(axis=(0, 2)))[:, None] / 12 * ramp * mult_dec
    c_rev_raw = ((Rc[0][:, :, None] * w1).sum(axis=1) + (Rc[1][:, :, None] * w2).sum(axis=1)) / 12 * cen_on * mult_cen
    c_cogs = (((Rc[0] * ratio[0])[:, :, None] * w1).sum(axis=1) + ((Rc[1] * ratio[1])[:, :, None] * w2).sum(axis=1)) / 12 * cen_on * mult_cen
    Rmax = base_rev[:2]                                         # contract value at maximum quantity
    bond_base = ((Rmax[0][:, :, None] * w1).sum(axis=1) * g['bond_css'][:, None] * 15 / 12
                 + (Rmax[1][:, :, None] * w2).sum(axis=1) * g['bond_minsa'][:, None]) * cen_on * mult_cen
    # bid bond on LPU offers for renglones whose reference value exceeds B/.70,000, held bid_m months before each contract
    thr = (q[0] * pr[0] * 15 / 12 > 70000).astype(float)
    bid_val = (base_rev[0] * thr[None, :]).sum(axis=1) * 15 / 12
    bid_m = rhu(g['bid_m']).astype(int)
    start_b = cen_start - bid_m
    cyc = (t[None, :] >= start_b[:, None]) & (((t[None, :] - start_b[:, None]) % 15) < bid_m[:, None])
    bid_bonded = g['bid_bond'][:, None] * bid_val[:, None] * cyc * mult_cen
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
    tt = np.arange(1, T + 1)
    fixed_m = np.zeros((n, T))
    for j, fx in enumerate(FIXED):
        st = np.full(n, 1) if fx[4] == 'm1' else (np.full(n, LIC_M) if fx[4] == 'lic' else np.maximum(reg_m - 1, 1))
        fixed_m += fixed[:, j][:, None] * (tt[None, :] >= st[:, None])
    dormant = tt[None, :] > (stop_m[:, None] + 3)          # company wound down 3 months after closure
    fixed_m = np.where(dormant, 0.0, fixed_m)
    rs_unit = g['rs_off'] + g['rs_iea'] + g['rs_law'] * (1 + g['itbms_srv']) + g['rs_smp']
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
    lost_coll = np.where(forfeit > 0, np.where(has, collat[np.arange(n), np.clip(stop_m - 1, 0, T - 1)], 0.0), 0.0)
    prem = bonded * g['bond_prem'][:, None] / 12

    inv_loss = np.zeros((n, T))
    inv_loss[np.arange(n)[has], sm[has]] = (inv_at_stop * (1 - inv_rec))[has] + lost_coll[has]
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
    for y in range(4):
        taxpay[:, 12 * (y + 1) + 2] = tax[:, y]
    NI = Y - tax

    cash = np.zeros((n, T)); inj = np.zeros((n, T)); div = np.zeros((n, T)); aviso = np.zeros((n, T))
    mincash = g['mincash_m'][:, None] * fixed_m
    c_prev = np.zeros(n); cum_div = np.zeros(n)
    for i in range(T):
        m = i + 1
        if m in (15, 27, 39, 51):     # aviso de operación on equity at the previous year end, paid in March
            y = (m - 3) // 12
            pat = inj[:, :12 * y].sum(axis=1) + NI[:, :y].sum(axis=1) - div[:, :12 * y].sum(axis=1)
            aviso[:, i] = np.where(m <= stop_m + 3, np.maximum(100.0, g['aviso'] * np.maximum(pat, 0)), 0.0)
        pre = (c_prev + coll[:, i] - pay[:, i] - var[:, i] - fixed_m[:, i] - postreg[:, i] - setup_m[:, i]
               - rs_m[:, i] - annual[:, i] - dcoll[:, i] - prem[:, i] - taxpay[:, i] - aviso[:, i])
        inj[:, i] = np.maximum(0, mincash[:, i] - pre)
        c = pre + inj[:, i]
        if m in (24, 36, 48):
            y = m // 12
            distributable = np.maximum(0, NI[:, :y].sum(axis=1) - cum_div)
            avail = c - 2 * mincash[:, i] - tax[:, y - 1]
            d = g['payout'] * np.maximum(0, np.minimum(avail, distributable))
            div[:, i] = d; cum_div += d; c = c - d
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
    pat5 = inj.sum(axis=1) + NI.sum(axis=1) - div.sum(axis=1)
    aviso5 = np.where(T <= stop_m + 3, np.maximum(100.0, g['aviso'] * np.maximum(pat5, 0)), 0.0)
    taxY5 = tax[:, 4] + aviso5
    tv_liq = cash[:, T - 1] + g['recov'] * nwc - taxY5
    tv_gc = cash[:, T - 1] - taxY5 + g['gc_mult'] * np.maximum(0, NI[:, 4])
    tv_best = np.maximum(tv_liq, tv_gc)
    eq_in = inj.sum(axis=1)

    out = dict(rev=rev60, rev_dec=rev_dec[:, :T], rev_cen=rev_cen[:, :T], cogs=cogs60, arrivals=arr60, inv=inv[:, :T],
               pay=pay, coll=coll, var=var, fixed=fixed_m, postreg=postreg, setup=setup_m, rs=rs_m, annual=annual,
               collat=collat, prem=prem, fact_exp=fact_exp, aviso=aviso, aviso5=aviso5, bid_val=bid_val, bid_bonded=bid_bonded[:, :T], income=income, Y=Y, tax=tax, NI=NI, taxpay=taxpay, cash=cash,
               inj=inj, div=div, phase0=phase0, eq_in=eq_in, recv=recv, nwc=nwc, payables=payables, tv_liq=tv_liq,
               tv_gc=tv_gc, tv_best=tv_best, unit_cost=unit_cost, ourp=ourp, gm=gm, go=go, Rd=Rd, Rc=Rc,
               fob_part=fob_part, ratio=ratio, lead_m=lead_m, dso_m=dso_m, first_dec=first_dec, cen_start=cen_start,
               first_dec2=first_dec2, revY=revY, mincash=mincash, rs_unit=rs_unit, n_filed=n_filed, k2=k2,
               mult_dec=mult_dec[:, :T], mult_cen=mult_cen[:, :T], ramp=ramp[:, :T], eros=eros[:, :T])
    r_m = (1 + g['disc']) ** (1 / 12) - 1
    for tag, tv in (('liq', tv_liq), ('best', tv_best)):
        tvnet = tv - g['divtax'] * np.maximum(0, tv - eq_in)
        cf = np.zeros((n, T + 1))
        cf[:, 0] = -phase0
        cf[:, 1:] = -inj + div * (1 - g['divtax'][:, None])
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
