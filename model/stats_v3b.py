import numpy as np, json
from multiprocessing import Pool
import mc
import stats_v3 as S
_orig = mc.draw
def make_draw(coord):
    def d(n, rng, **kw):
        p = _orig(n, rng, **kw)
        p['fixed'][5] = np.full(n, float(coord))
        return p
    return d
def job(args):
    name, coord, sim_kw = args
    mc.draw = make_draw(coord)
    nm, R = S.run_case((name, 'bueno', S.inc_cns, None, sim_kw))
    return name, S.stats(R)
if __name__ == '__main__':
    cases = [('bueno_coord0', 0, None), ('bueno_coord1000', 1000, None), ('bueno_coord0_cap11', 0, dict(dd_price_cap=1.10)), ('bueno_coord1000_cap11', 1000, dict(dd_price_cap=1.10))]
    with Pool(2) as pool:
        res = dict(pool.map(job, cases))
    json.dump(res, open('stats_v3b.json', 'w'), indent=1, default=float)
    for k, v in res.items():
        print(k, {kk: round(v[kk], 3) if abs(v[kk]) < 10 else round(v[kk]) for kk in ('npv15', 'npv25', 'p_npv_neg', 'p_loss', 'p_loss_b', 'p_nogo', 'peak_med_go', 'peak_p90_go', 'j_in_mean_go', 'j_net_mean')}, 'K4', round(v['k4']['amount']), v['k4']['at_bound'], 'K15', round(v['k15']['amount']))
