# -*- coding: utf-8 -*-
"""Simulación de Monte Carlo por estructura del trato (20,000 escenarios por estructura, mismas semillas).

Estructuras:
  A  Propuesta de Rutul Patel tal cual: se constituye y se opera sin compuertas; 30% de anticipo, sin crédito.
  B  Por etapas: fase 0 (precio y documentos de la fábrica, opinión legal) y compuerta operativa; mismos términos que A.
  C  Por etapas con términos negociados: crédito de 60-180 días, anticipo de 0-30%, precio de fábrica 0.95-1.30 veces la referencia.
  D  Por etapas, la fábrica paga los registros y da crédito de 120-180 días sin anticipo, precio 0.95-1.30.
  E  Registros más distribuidor establecido: la S.A. solo tiene los registros y cobra una regalía de 20-40% del margen bruto.
Variantes de D: con productos de sistema nervioso (si se verifica su fabricante), con un socio como coordinador sin sueldo,
con colateral de 100%, y con prueba de precio estricta en la fase 0 (1.1 veces la referencia).
"""
import numpy as np
from multiprocessing import Pool
import mc
from mc import simulate, tri_ppf
from engine import T
from inputs import SKUS, FIXED, ANNUAL_CHARGES

N_CHUNK, N_REP = 4000, 5           # 5 x 4,000 = 20,000 escenarios
INC_FIRST = [s['inc'] for s in SKUS]
INC_SNC = [1 if s['group'] in ('Primera ola', 'SNC') else 0 for s in SKUS]
COORD_IDX = [i for i, f in enumerate(FIXED) if f[0].startswith('Coordinador')]
D15 = (1.15 ** (1 / 12)) ** (-np.arange(T + 1))


def negotiated_override(n, seed):
    rng = np.random.default_rng(seed + 777)
    return {'credit_days': tri_ppf(rng.random(n), 60, 120, 180), 'adv': tri_ppf(rng.random(n), 0, 0, 0.3),
            'sup_idx': tri_ppf(rng.random(n), 0.95, 1.05, 1.30)}


def factory_funds_override(n, seed):
    rng = np.random.default_rng(seed + 11)
    z = np.zeros(n)
    return {'credit_days': tri_ppf(rng.random(n), 120, 180, 180), 'adv': z.copy(), 'sup_idx': tri_ppf(rng.random(n), 0.95, 1.05, 1.3),
            'rs_off': z.copy(), 'rs_iea': z.copy(), 'rs_law': z.copy(), 'rs_smp': z.copy(), 'rs_trad': z.copy()}


def _coord_zero_draw(orig):
    def d(n, rng, **kw):
        p = orig(n, rng, **kw)
        for i in COORD_IDX:
            p['fixed'][i] = np.zeros(n)
        return p
    return d


def run_structure(args):
    """devuelve los flujos de los accionistas (n, T+1) y marcas por escenario"""
    key, kind, inc, mod, sim_kw, coord0 = args
    orig_draw = mc.draw
    if coord0:
        mc.draw = _coord_zero_draw(orig_draw)
    try:
        return key, _run_structure(kind, inc, mod, sim_kw)
    finally:
        mc.draw = orig_draw


def _run_structure(kind, inc, mod, sim_kw):
    acc = {k: [] for k in ('cf', 'cfx', 'no_go', 'fail_gate', 'forfeit', 'gate_m', 'cen_first', 'sales_y3')}
    for i in range(N_REP):
        seed = 1000 + i; n = N_CHUNK
        if kind == 'committed':
            po, strat = {}, 'committed'
        elif kind == 'staged':
            po, strat = {}, 'staged'
        elif kind == 'negotiated':
            po, strat = negotiated_override(n, seed), 'staged'
        elif kind == 'factory':
            po, strat = factory_funds_override(n, seed), 'staged'
        for k, v in (mod or {}).items():
            po[k] = np.full(n, v)
        r = simulate(n=n, seed=seed, strategy=strat, p_override=po or None, inc_override=inc, **(sim_kw or {}))
        cf = r['cf']; ng = r['no_go']
        cfx = cf.copy(); cfx[:, T] -= np.where(ng, 0.0, r['o']['tvnet_liq'])     # sin valor terminal, para el capital
        acc['cf'].append(cf); acc['cfx'].append(cfx); acc['no_go'].append(ng)
        acc['fail_gate'].append(r['gate']['fail_gate'] & ~ng); acc['forfeit'].append((r['forfeit'] > 0) & ~ng)
        acc['gate_m'].append(np.asarray(r['gate']['gate_m']).astype(int))
        acc['cen_first'].append(np.asarray(r['o']['cen_start']).astype(int))
        acc['sales_y3'].append(np.where(ng, 0.0, r['o']['revY'][:, 2]))
    return {k: np.concatenate(v) for k, v in acc.items()}


def run_registrations_distributor(n_total=20000, chunk=N_CHUNK):
    """Estructura E: la S.A. registra los productos y un distribuidor establecido los vende; regalía sobre el margen bruto."""
    cfs, ngs = [], []
    n1 = sum(s['inc'] for s in SKUS)
    annual_base = ANNUAL_CHARGES[0][1] + ANNUAL_CHARGES[1][1] + ANNUAL_CHARGES[2][1]
    for i in range(n_total // chunk):
        seed = 2000 + i
        rng = np.random.default_rng(seed + 5)
        r = simulate(n=chunk, seed=seed, strategy='staged', p_override=None, gate_runrate=0)
        o = r['o']; p = r['p']; n = chunk
        rho = tri_ppf(rng.random(n), 0.2, 0.3, 0.4)
        uplift = 1.25                    # un distribuidor establecido vende más que una S.A. nueva
        rev = o['rev'] * uplift
        cogs = o['cogs'] * uplift * (1 + np.asarray(p['expiry']))[:, None]
        gp = rev * (1 - np.asarray(p['baddebt']))[:, None] - cogs - rev * (np.asarray(p['dist']) + np.asarray(p['penal']))[:, None]
        dso = np.rint(np.asarray(p['dso_days']) / 30).astype(int) + 1
        roy = np.zeros((n, T))
        for k in range(n):
            d = dso[k]; roy[k, d:] = rho[k] * gp[k, :T - d]
        it = np.asarray(p['itbms_srv']) * np.ones(n); oc = np.asarray(p['oncost']) * np.ones(n)
        rs_unit = (np.asarray(p['rs_off']) + np.asarray(p['rs_iea']) + (np.asarray(p['rs_law']) + np.asarray(p['rs_trad'])) * (1 + it)
                   + np.asarray(p['rs_smp']) + 500)
        cf = np.zeros((n, T + 1))
        ph0 = np.asarray(p['setup'][0]) + np.asarray(p['setup'][1])
        cf[:, 0] = -ph0
        cf[:, 1] -= 5650 * (1 + it)                       # constitución, pacto y diagnóstico
        cf[:, 3] -= n1 * rs_unit
        m2 = np.clip(np.rint(np.asarray(p['m2'])).astype(int), 1, T)
        n2 = np.asarray(p['n2'])
        cf[np.arange(n), m2] -= n2 * rs_unit
        fixed = tri_ppf(rng.random(n), 600, 800, 1200) * (1 + 0.5 * oc + 0.3 * it)
        stop = r['stop_m']
        tt = np.arange(1, T + 1)
        alive = (tt[None, :] <= np.minimum(stop + 3, 61)[:, None])
        cf[:, 1:] -= fixed[:, None] * alive
        for m in (1, 13, 25, 37, 49):
            cf[:, m] -= annual_base * (1 + 0.5 * it) * alive[:, m - 1]
        cf[:, 1:] += roy
        prof = cf[:, 1:].reshape(n, 5, 12).sum(axis=2)
        tax = np.maximum(0, prof) * 0.25
        for y in range(4):
            cf[:, 12 * (y + 1) + 3] -= tax[:, y]
        cf[:, T] -= tax[:, 4]
        for m in (15, 27, 39, 51):
            y = (m - 3) // 12; netcap = -cf[:, 1:12 * y + 1].sum(axis=1)
            cf[:, m] -= np.maximum(100, 0.02 * np.maximum(0, netcap)) * alive[:, m - 1]
        tv = np.array([0.9 * rho[k] * gp[k, T - dso[k]:T].sum() for k in range(n)])
        cf[:, T] += tv
        ng = r['no_go']
        cf[ng] = 0; cf[ng, 0] = -ph0[ng]
        cfs.append(cf); ngs.append(ng)
    cf = np.concatenate(cfs); ng = np.concatenate(ngs)
    cfx = cf.copy()
    return dict(cf=cf, cfx=cfx, no_go=ng, fail_gate=np.zeros(len(cf), bool), forfeit=np.zeros(len(cf), bool),
                gate_m=np.zeros(len(cf), int), cen_first=np.zeros(len(cf), int), sales_y3=np.zeros(len(cf)))


def stats(R, cash_frac=1/6, eq_frac=1/6, ph0_frac=1/3, pooled=True):
    """Indicadores de una estructura. cf = flujos de todos los accionistas con valor terminal conservador."""
    cf = R['cf']; cfx = R['cfx']; ng = R['no_go']; go = ~ng
    ph0 = -cf[:, 0]
    neg = -np.where(cf < 0, cf, 0).sum(1); pos = np.where(cf > 0, cf, 0).sum(1)
    moic = np.where(neg > 0, pos / neg, np.nan)
    npv = (cf * D15).sum(1)
    cum = np.cumsum(cfx, 1); peak = -cum.min(1)
    if pooled:
        j_in = ph0 * ph0_frac + (neg - ph0) * cash_frac
        j_out = pos * eq_frac
    else:                              # E: la S.A. es solo de los panameños
        j_in = neg * cash_frac; j_out = pos * eq_frac
    j_net = j_out - j_in
    j_peak = peak * cash_frac + ph0 * (ph0_frac - cash_frac) if pooled else peak * cash_frac
    pct = lambda a, q: float(np.percentile(a, q))
    out = dict(
        n=int(len(cf)), p_nogo=float(ng.mean()), p_gate=float(R['fail_gate'].mean()), p_fail=float(R['forfeit'].mean()),
        p_loss=float((pos < neg).mean()), p_loss_beyond_ph0=float(((pos - neg) < -ph0 - 1).mean()),
        npv15_mean=float(npv.mean()), npv15_p10=pct(npv, 10), npv15_p50=pct(npv, 50), npv15_p90=pct(npv, 90),
        p_npv_neg=float((npv < 0).mean()),
        moic_p10=float(np.nanpercentile(moic, 10)), moic_p50=float(np.nanpercentile(moic, 50)), moic_p90=float(np.nanpercentile(moic, 90)),
        p_moic_ge2=float(np.nanmean(moic >= 2)),
        cap_go_p50=pct(peak[go], 50) if go.any() else 0.0, cap_go_p80=pct(peak[go], 80) if go.any() else 0.0,
        cap_go_p90=pct(peak[go], 90) if go.any() else 0.0, cap_go_mean=float(peak[go].mean()) if go.any() else 0.0,
        ph0_mean=float(ph0.mean()),
        j_cap_go_p50=pct(j_peak[go], 50) if go.any() else 0.0, j_cap_go_p90=pct(j_peak[go], 90) if go.any() else 0.0,
        j_in_mean=float(j_in.mean()), j_net_mean=float(j_net.mean()), j_p_loss=float((j_net < 0).mean()),
        j_net_p10=pct(j_net, 10), j_net_p50=pct(j_net, 50), j_net_p90=pct(j_net, 90),
        sales_y3_go_p50=pct(R['sales_y3'][go], 50) if go.any() else 0.0,
    )
    gm = R['gate_m']
    if gm.max() > 0:
        idx = np.clip(gm, 0, T)
        capg = -cum[np.arange(len(gm)), idx]
        sel = go & (gm > 0)
        out['cap_at_gate_p50'] = pct(capg[sel], 50)
        out['gate_month_p50'] = pct(gm[sel], 50)
    cen = R['cen_first']
    if cen.max() > 0:
        out['cen_first_p50'] = pct(cen[go], 50)
    return out


CASES = [
    ('A', 'committed', INC_FIRST, None, None, False),
    ('B', 'staged', INC_FIRST, None, None, False),
    ('C', 'negotiated', INC_FIRST, None, None, False),
    ('D', 'factory', INC_FIRST, None, None, False),
    ('D_snc', 'factory', INC_SNC, None, None, False),
    ('D_coord0', 'factory', INC_FIRST, None, None, True),
    ('D_collat100', 'factory', INC_FIRST, dict(collat=1.0), None, False),
    ('D_cap11', 'factory', INC_FIRST, None, dict(dd_price_cap=1.10), False),
    ('D_snc_coord0', 'factory', INC_SNC, None, None, True),
]

LABELS = {
    'A': 'A. Propuesta de Rutul Patel tal cual',
    'B': 'B. Por etapas, mismos términos',
    'C': 'C. Por etapas con términos negociados',
    'D': 'D. Por etapas; la fábrica paga registros y da crédito',
    'E': 'E. Registros más distribuidor establecido',
    'D_snc': 'D más productos de sistema nervioso (si se verifica su fabricante)',
    'D_coord0': 'D con un socio como coordinador sin sueldo',
    'D_collat100': 'D con colateral de 100% de la fianza',
    'D_cap11': 'D con prueba de precio estricta en la fase 0 (1.1 veces la referencia)',
    'D_snc_coord0': 'D más sistema nervioso y coordinador sin sueldo',
}


def run_all(processes=2):
    with Pool(processes) as pool:
        raw = dict(pool.map(run_structure, CASES))
    raw['E'] = run_registrations_distributor()
    out = {}
    for k, R in raw.items():
        out[k] = stats(R, pooled=(k != 'E'), cash_frac=(1 / 3 if k == 'E' else 1 / 6), eq_frac=(1 / 3 if k == 'E' else 1 / 6))
        out[k]['label'] = LABELS[k]
    # reparto alternativo del efectivo en D: Rutul Patel aporta 70% o 80% (los panameños 30% o 20%)
    out['D_cash70'] = stats(raw['D'], cash_frac=0.3 / 3, eq_frac=0.5 / 3); out['D_cash70']['label'] = 'D con Rutul Patel aportando 70% del efectivo'
    out['D_cash80'] = stats(raw['D'], cash_frac=0.2 / 3, eq_frac=0.5 / 3); out['D_cash80']['label'] = 'D con Rutul Patel aportando 80% del efectivo'
    return out


if __name__ == '__main__':
    import json, time
    t0 = time.time()
    res = run_all()
    json.dump(res, open('structures.json', 'w'), indent=1)
    for k, v in res.items():
        print(f"{k:14s} nogo {v['p_nogo']:.2f} gate {v['p_gate']:.2f} fail {v['p_fail']:.2f} | P(loss) {v['p_loss']:.3f} "
              f"P(>ph0) {v['p_loss_beyond_ph0']:.3f} | NPV15 {v['npv15_mean']:>9,.0f} | MOIC50 {v['moic_p50']:.2f} | "
              f"cap p50/p80/p90 {v['cap_go_p50']:>8,.0f} {v['cap_go_p80']:>8,.0f} {v['cap_go_p90']:>8,.0f} | J p50 {v['j_cap_go_p50']:>7,.0f} J net {v['j_net_mean']:>8,.0f}")
    print('segundos', round(time.time() - t0))
