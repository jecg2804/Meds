# Consolidated Monte Carlo statistics for the plan (model v3: on-costs, ITBMS, bonds on max quantity, bid bond, aviso)
import numpy as np, json, sys
from multiprocessing import Pool
import mc
from mc import simulate
from mc_more import restructured_override, bueno_override, run_C
from engine import T
from inputs import SKUS
inc_cns = [1 if s['group'] in ('Bueno', 'CNS') else 0 for s in SKUS]
W = 100000.0
D = {r: (1 + r) ** (-np.arange(T + 1) / 12) for r in (0.15, 0.25, 0.30)}

def run_case(args):
    name, kind, inc, mod, sim_kw = args
    acc = {k: [] for k in ('cf', 'cfx', 'no_go', 'fail_gate', 'forfeit', 'gate_m')}
    for i in range(5):
        seed = 1000 + i; n = 4000
        if kind == 'committed': po, strat = {}, 'committed'
        elif kind == 'staged': po, strat = {}, 'staged'
        elif kind == 'restr': po, strat = restructured_override(n, seed), 'staged'
        elif kind == 'bueno': po, strat = bueno_override(n, seed), 'staged'
        for k, v in (mod or {}).items():
            po[k] = np.full(n, v)
        r = simulate(n=n, seed=seed, strategy=strat, p_override=po or None, inc_override=inc, **(sim_kw or {}))
        cf = r['cf']; ng = r['no_go']
        cfx = cf.copy(); cfx[:, T] -= np.where(ng, 0.0, r['o']['tvnet_liq'])
        acc['cf'].append(cf); acc['cfx'].append(cfx); acc['no_go'].append(ng)
        acc['fail_gate'].append(r['gate']['fail_gate'] & ~ng); acc['forfeit'].append(r['forfeit'] * (~ng))
        acc['gate_m'].append(np.asarray(r['gate']['gate_m']).astype(int))
    return name, {k: np.concatenate(v) for k, v in acc.items()}

def kelly(j_in, j_out, rf):
    lam_max = W / np.max(j_in) * 0.999
    lams = np.linspace(0, lam_max, 1500)
    el = np.array([np.mean(np.log(W * rf + l * (j_out - j_in * rf))) for l in lams])
    k = int(np.argmax(el))
    return dict(amount=float(lams[k] * j_in.mean()), at_bound=bool(k == len(lams) - 1), frac_of_bound=float(lams[k] / lam_max))

def stats(R, jfr=(1/6, 1/6, 1/3), c_mode=False):
    cf = R['cf']; cfx = R['cfx']; ng = R['no_go']; go = ~ng
    neg = -np.where(cf < 0, cf, 0).sum(1); pos = np.where(cf > 0, cf, 0).sum(1); ph0 = -cf[:, 0]
    moic = np.where(neg > 0, pos / neg, np.nan)
    npv = {k: (cf * D[k]).sum(1) for k in D}
    cum = np.cumsum(cfx, 1); peak = -cum.min(1)
    if c_mode:      # option C: no cash pooling, capital at risk = peak cumulative need
        j_in = peak * jfr[0]; j_net = cf.sum(1) * jfr[1]; j_out = j_net + j_in
    else:
        j_in = ph0 * jfr[2] + (neg - ph0) * jfr[0]; j_out = pos * jfr[1]; j_net = j_out - j_in
    ph0j = ph0 * jfr[2]
    res = dict(npv15=npv[0.15].mean(), npv25=npv[0.25].mean(), npv30=npv[0.30].mean(), p_npv_neg=(npv[0.15] < 0).mean(),
               p_loss=(pos < neg).mean(), p_loss_b=((pos - neg) < -ph0 - 1).mean(),
               moic_pcts=np.nanpercentile(moic, [10, 25, 50, 75, 90]).tolist(), npv_pcts=np.percentile(npv[0.15], [5, 10, 25, 50, 75, 90, 95]).tolist(), moic_med_go=float(np.nanmedian(moic[go])),
               peak_med_go=float(np.median(peak[go])), peak_p90_go=float(np.percentile(peak[go], 90)), peak_mean_go=float(peak[go].mean()),
               p_nogo=ng.mean(), p_gate=R['fail_gate'].mean(), p_fail=(R['forfeit'] > 0).mean(),
               j_in_mean=j_in.mean(), j_in_mean_go=j_in[go].mean(), j_in_p90=float(np.percentile(j_in, 90)), j_in_p90_go=float(np.percentile(j_in[go], 90)),
               j_net_mean=j_net.mean(), j_ploss=(j_net < 0).mean(), j_ploss_b=(j_net < -ph0j - 1).mean())
    gm = R['gate_m']
    if gm.max() > 0:
        idx = np.clip(gm, 0, T)
        capg = -cum[np.arange(len(gm)), idx]
        sel = go & (gm > 0)
        res['cap_at_gate_med'] = float(np.median(capg[sel]))
    res['k4'] = kelly(j_in, j_out, 1.04 ** 5); res['k15'] = kelly(j_in, j_out, 1.15 ** 5)
    return {k: (float(v) if isinstance(v, (np.floating, float, np.bool_)) else v) for k, v in res.items()}

if __name__ == '__main__':
    cases = [('A_comprometido', 'committed', None, None, None),
             ('A_por_etapas', 'staged', None, None, None),
             ('A_por_etapas_reestructurado', 'restr', None, None, None),
             ('A_por_etapas_reestructurado_SNC', 'restr', inc_cns, None, None),
             ('A_bueno_financia_SNC', 'bueno', inc_cns, None, None),
             ('bueno_cap11', 'bueno', inc_cns, None, dict(dd_price_cap=1.10)),
             ('bueno_pwin17', 'bueno', inc_cns, dict(pwin_cen=0.17), None),
             ('bueno_collat100', 'bueno', inc_cns, dict(collat=1.0), None),
             ('bueno_sup125', 'bueno', inc_cns, dict(sup_idx=1.25), None),
             ('bueno_pwin17_sup125', 'bueno', inc_cns, dict(pwin_cen=0.17, sup_idx=1.25), None),
             ('bueno_nocoord', 'bueno', inc_cns, None, None)]
    # 'bueno_nocoord' is handled below by zeroing the coordinator line through p_override of fixed is not supported; skip in pool
    cases = cases[:-1]
    with Pool(2) as pool:
        raw = dict(pool.map(run_case, cases))
    out = {}
    for name, R in raw.items():
        out[name] = stats(R)
        if name == 'A_bueno_financia_SNC':
            out[name + '_70_30'] = stats(R, jfr=(0.3 / 3, 0.5 / 3, 1 / 3))
            out[name + '_80_20'] = stats(R, jfr=(0.2 / 3, 0.5 / 3, 1 / 3))
        np.save(f'v3_cf_{name}.npy', R['cf'])
    # option C
    cfC = run_C()
    RC_ = dict(cf=cfC, cfx=np.concatenate([cfC[:, :T], np.zeros((len(cfC), 1))], axis=1), no_go=(cfC[:, 1:] == 0).all(axis=1),
               fail_gate=np.zeros(len(cfC), bool), forfeit=np.zeros(len(cfC)), gate_m=np.zeros(len(cfC), int))
    out['C'] = stats(RC_, jfr=(1 / 3, 1 / 3, 1 / 3), c_mode=True)
    np.save('v3_cf_C.npy', cfC)
    json.dump(out, open('stats_v3.json', 'w'), indent=1, default=float)
    for k, v in out.items():
        print(k, {kk: (round(vv, 3) if isinstance(vv, float) and abs(vv) < 10 else (round(vv) if isinstance(vv, float) else vv)) for kk, vv in v.items() if kk not in ('k4', 'k15')}, 'K4', v['k4'], 'K15', v['k15'])
