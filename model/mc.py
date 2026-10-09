# -*- coding: utf-8 -*-
"""Monte Carlo for the Panama tender distributor. Two strategies:
 - 'committed': constitute, register and operate regardless of what is learned (no gates).
 - 'staged'   : Phase 0 due diligence gate before constituting (price list + GMP/documents),
                and a month-15 gate (annualized sales must cover break-even) before wave 2 / continuing.

Audit corrections (9 Oct 2026), switchable through `mc_fixes`:
 - 'fixed_corr'       the fixed-cost lines (and the setup lines) share a common cost factor (Gaussian copula, rho_fixed)
                      instead of being drawn independently, which understated the spread of the total
 - 'wave2_after_gate' in the staged strategies the second wave is filed only after the operating gate (m2 >= gate month)
"""
import numpy as np
from scipy.stats import norm
from engine import run, scenario_params, irr_rows, T
from inputs import P, FIXED, SETUP, SKUS

FIXED_KEYS = {'gm_dec', 'gm_cen', 'bond_css', 'bond_minsa', 'mincash_m', 'rs_off', 'isr', 'divtax', 'payout', 'disc',
              'patel_eq', 'patel_cash', 'jaime_frac', 'ship_m', 'stop_det', 'inv_liq', 'fact_share', 'fact_cost',
              'bond_tail_css', 'bond_tail_minsa', 'forfeit_frac'}
INT_KEYS = {'reg_m', 'cen_start', 'm2', 'n2', 'bid_m'}
ALL_MC_FIXES = frozenset({'fixed_corr', 'wave2_after_gate'})
RHO_FIXED = 0.5


def tri_ppf(u, a, c, b):
    """Inverse CDF of triangular(min=a, mode=c, max=b)."""
    a, c, b = float(a), float(c), float(b)
    if b <= a:
        return np.full_like(u, c)
    fc = (c - a) / (b - a)
    return np.where(u < fc, a + np.sqrt(u * (b - a) * (c - a)), b - np.sqrt((1 - u) * (b - a) * (b - c)))


def _corr_u(u, z0, rho):
    """keeps each line's own uniform draw and mixes it with a common factor z0 (Gaussian copula)"""
    if rho <= 0:
        return u
    z = norm.ppf(np.clip(u, 1e-12, 1 - 1e-12))
    return norm.cdf(np.sqrt(rho) * z0 + np.sqrt(1 - rho) * z)


def draw(n, rng, rho_comp=0.6, rho_mkt=0.4, rho_fixed=0.0, rng_common=None):
    p = scenario_params('base')
    z = rng.standard_normal((n, 4))
    # correlated latent factors: competitiveness (share_dec, pwin_cen) and market (mkt, erosion)
    zc1 = z[:, 0]; zc2 = rho_comp * z[:, 0] + np.sqrt(1 - rho_comp ** 2) * z[:, 1]
    zm1 = z[:, 2]; zm2 = -(rho_mkt * z[:, 2] + np.sqrt(1 - rho_mkt ** 2) * z[:, 3])   # weak market <-> higher erosion
    special = {'share_dec': norm.cdf(zc1), 'pwin_cen': norm.cdf(zc2), 'mkt': norm.cdf(zm1), 'erosion': norm.cdf(zm2)}
    for k, v in P.items():
        if k in FIXED_KEYS:
            continue
        pes, base, opt = v[2], v[3], v[4]
        lo, hi = min(pes, opt), max(pes, opt)
        if lo == hi:
            continue
        u = special[k] if k in special else rng.random(n)
        x = tri_ppf(u, lo, base, hi)
        if k in INT_KEYS:
            x = np.rint(x)
        p[k] = x
    zf = rng_common.standard_normal(n) if (rng_common is not None and rho_fixed > 0) else np.zeros(n)
    zs = rng_common.standard_normal(n) if (rng_common is not None and rho_fixed > 0) else np.zeros(n)
    p['fixed'] = [tri_ppf(_corr_u(rng.random(n), zf, rho_fixed), min(f[1], f[3]), f[2], max(f[1], f[3])) for f in FIXED]
    p['setup'] = [tri_ppf(_corr_u(rng.random(n), zs, rho_fixed), min(s[1], s[3]), s[2], max(s[1], s[3])) for s in SETUP]
    return p


def simulate(n=20000, seed=20261006, strategy='staged', p_gmp_bad=0.15, hazard_annual=0.04,
             dd_price_cap=1.60, dd_detect=0.8, gate_runrate=90_000, gate_after=9, inc_override=None, p_override=None,
             fixes=None, mc_fixes=None):
    MF = ALL_MC_FIXES if mc_fixes is None else frozenset(mc_fixes)
    rng = np.random.default_rng(seed)
    rho_f = RHO_FIXED if 'fixed_corr' in MF else 0.0
    p = draw(n, rng, rho_fixed=rho_f, rng_common=np.random.default_rng(seed + 424242))
    if p_override:
        for k, v in p_override.items():
            p[k] = v
    S = len(SKUS)
    rs_ok = (rng.random((n, S)) < np.asarray(p['rs_succ'])[:, None]).astype(float)
    win1 = (rng.random((n, S, 6)) < np.asarray(p['pwin_cen'])[:, None, None]).astype(float)
    win2 = ((rng.random((n, S, 6)) < np.asarray(p['pwin_cen'])[:, None, None]) &
            (rng.random((n, 1, 6)) < np.asarray(p['minsa_occ'])[:, None, None])).astype(float)
    n2 = np.asarray(p['n2'])
    rs2 = np.where(n2 > 0, rng.binomial(n2.astype(int), np.asarray(p['rs_succ'])) / np.maximum(n2, 1), 0)
    gmp_bad = rng.random(n) < p_gmp_bad
    # random supply break (partner, quality alert, plant problem) after operations start
    fail_m = np.ceil(rng.exponential(12 / (-np.log(1 - hazard_annual)), n)).astype(int) + 6
    # a bad plant (GMP) shows up as a quality failure between months 12 and 36 if not caught in due diligence
    gmp_fail_m = rng.integers(12, 37, n)
    stop_m = np.full(n, 61)
    forfeit = np.zeros(n); inv_rec = np.full(n, 0.5)
    wave2 = np.ones(n)
    no_go = np.zeros(n, dtype=bool)

    if strategy in ('staged', 'staged_restructured'):
        detected = gmp_bad & (rng.random(n) < dd_detect)          # Phase 0 catches most plant/document problems
        no_go = detected | (np.asarray(p['sup_idx']) > dd_price_cap)
        leak = gmp_bad & ~detected
    else:
        leak = gmp_bad
    q = leak & (gmp_fail_m < stop_m)
    stop_m = np.where(q, gmp_fail_m, stop_m); forfeit = np.where(q, 1.0, forfeit); inv_rec = np.where(q, 0.0, inv_rec)
    rnd = fail_m < stop_m
    stop_m = np.where(rnd, fail_m, stop_m); forfeit = np.where(rnd, 1.0, forfeit)

    mc = dict(rs_ok=rs_ok, win1=win1, win2=win2, rs2_frac=rs2, wave2=wave2, stop_m=stop_m.copy(),
              forfeit=forfeit, inv_rec=inv_rec)
    if strategy in ('staged', 'staged_restructured'):
        # operating gate: after `gate_after` months of selling, annualized sales (decentralized + awarded
        # centralized contracts) must reach the break-even run-rate; otherwise wind down. Wave 2 only if passed.
        mc0 = dict(mc); mc0['wave2'] = np.zeros(n)
        o0 = run(p, n=n, mc=mc0, inc_override=inc_override, fixes=fixes)
        gm_ = np.clip(o0['first_dec'] + gate_after, 1, T)
        idx = gm_ - 1
        dec_rr = o0['rev_dec'][np.arange(n), idx] * 12
        # awarded centralized value known at the gate: contracts starting within the next 6 months count
        cen_rr = np.array([o0['rev_cen'][i, idx[i]:min(T, idx[i] + 7)].max() if idx[i] < T else 0 for i in range(n)]) * 12
        runrate = dec_rr + cen_rr
        fail_gate = (runrate < gate_runrate) & (stop_m > gm_)
        mc['stop_m'] = np.where(fail_gate, gm_, mc['stop_m'])
        mc['forfeit'] = np.where(fail_gate, 0.0, mc['forfeit'])
        mc['wave2'] = np.where(fail_gate, 0.0, 1.0)
        if 'wave2_after_gate' in MF:
            p = dict(p); p['m2'] = np.maximum(np.asarray(p['m2'], dtype=float), gm_)
        res_gate = dict(gate_m=gm_, runrate=runrate, fail_gate=fail_gate)
    else:
        res_gate = dict(gate_m=np.zeros(n), runrate=np.zeros(n), fail_gate=np.zeros(n, dtype=bool))
    o = run(p, n=n, mc=mc, inc_override=inc_override, fixes=fixes)

    # investor cash flows (all shareholders); no-go cases only lose Phase 0
    cf = o['cf_liq'].copy()
    cfb = o['cf_best'].copy()
    phase0 = o['phase0']
    for c in (cf, cfb):
        c[no_go] = 0.0
        c[no_go, 0] = -phase0[no_go]
    r15 = 1.15 ** (1 / 12) - 1
    disc15 = (1 + r15) ** (-np.arange(T + 1))
    r30 = 1.30 ** (1 / 12) - 1
    disc30 = (1 + r30) ** (-np.arange(T + 1))
    res = dict(p=p, o=o, cf=cf, cfb=cfb, no_go=no_go, gate=res_gate, stop_m=mc['stop_m'], forfeit=mc['forfeit'], gmp_bad=gmp_bad,
               npv15=(cf * disc15).sum(axis=1), npv30=(cf * disc30).sum(axis=1), npv15b=(cfb * disc15).sum(axis=1))
    pos = np.where(cf > 0, cf, 0).sum(axis=1); neg = -np.where(cf < 0, cf, 0).sum(axis=1)
    res['moic'] = np.where(neg > 0, pos / neg, np.nan)
    posb = np.where(cfb > 0, cfb, 0).sum(axis=1)
    res['moicb'] = np.where(neg > 0, posb / neg, np.nan)
    res['equity'] = neg
    res['net'] = cf.sum(axis=1)
    return res


def jaime_view(res, patel_eq=0.5, patel_cash=0.5, jaime_frac=1/3, phase0_paid_by_panama=True):
    cf = res['cf']; o = res['o']
    n = cf.shape[0]
    phase0 = -cf[:, 0]
    inj = -np.where(cf[:, 1:] < 0, cf[:, 1:], 0)
    outs = np.where(cf[:, 1:] > 0, cf[:, 1:], 0)
    j_in = np.zeros_like(cf)
    j_in[:, 0] = -phase0 * (jaime_frac if phase0_paid_by_panama else (1 - patel_cash) * jaime_frac)
    j_in[:, 1:] = -inj * (1 - patel_cash) * jaime_frac + outs * (1 - patel_eq) * jaime_frac
    return j_in
