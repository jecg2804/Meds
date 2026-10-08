import numpy as np, time
from mc import simulate, jaime_view, tri_ppf
from engine import irr_rows

def restructured_override(n, seed):
    rng=np.random.default_rng(seed+777)
    return {'credit_days': tri_ppf(rng.random(n),60,120,180), 'adv': tri_ppf(rng.random(n),0,0,0.3),
            'sup_idx': tri_ppf(rng.random(n),0.95,1.05,1.30)}

def chunked(strategy, n_total=20000, chunk=4000, **kw):
    parts=[]
    for i in range(n_total//chunk):
        seed=1000+i
        po = restructured_override(chunk, seed) if strategy=='staged_restructured' else None
        r=simulate(n=chunk, seed=seed, strategy=strategy, p_override=po, **kw)
        if strategy=='staged_restructured':
            pass
        j=jaime_view(r)
        parts.append(dict(npv15=r['npv15'], npv30=r['npv30'], npv15b=r['npv15b'], moic=r['moic'], moicb=r['moicb'],
                          equity=r['equity'], net=r['net'], no_go=r['no_go'], stop=r['stop_m'], forfeit=r['forfeit'],
                          gmp_bad=r['gmp_bad'], cf=r['cf'], cfb=r['cfb'], jcf=j, revY3=r['o']['revY'][:,2], ni5=r['o']['NI'][:,4],
                          fail_gate=r['gate']['fail_gate'], runrate=r['gate']['runrate'],
                          sup=np.asarray(r['p']['sup_idx']), share=np.asarray(r['p']['share_dec']), pwin=np.asarray(r['p']['pwin_cen']),
                          dso=np.asarray(r['p']['dso_days']), mkt=np.asarray(r['p']['mkt'])))
    return {k: np.concatenate([p[k] for p in parts]) for k in parts[0]}

if __name__=='__main__':
    t0=time.time(); res={}
    for st in ('committed','staged','staged_restructured'):
        res[st]=chunked(st); print(st,'done',round(time.time()-t0,1),'s')
    np.savez_compressed('mc_results.npz', **{f"{st}__{k}": v for st in res for k, v in res[st].items()})
    for st,r in res.items():
        irr=irr_rows(r['cf'][:4000])
        jn=r['jcf'].sum(axis=1); jin=-np.where(r['jcf']<0, r['jcf'],0).sum(axis=1)
        print(f"\n== {st} (n={len(r['npv15'])})")
        print(" P(no-go fase 0)=", r['no_go'].mean().round(3), " P(falla compuerta)=", r['fail_gate'].mean().round(3), " P(cierre/falla antes m60)=", ((r['stop']<=60)&~r['no_go']).mean().round(3), " P(forfeit)=", (r['forfeit']>0).mean().round(3))
        for q in (5,10,25,50,75,90,95):
            print(f"  p{q:2d}: NPV15={np.percentile(r['npv15'],q):10,.0f}  MOIC={np.nanpercentile(r['moic'],q):5.2f}  MOICgc={np.nanpercentile(r['moicb'],q):5.2f}  equity={np.percentile(r['equity'],q):9,.0f}  J net={np.percentile(jn,q):9,.0f}  J in={np.percentile(jin,q):8,.0f}")
        print("  mean NPV15", round(r['npv15'].mean()), " mean NPV15 gc", round(r['npv15b'].mean()), " P(NPV15<0)", (r['npv15']<0).mean().round(3), " P(MOIC<1)", np.nanmean(r['moic']<1).round(3), " P(MOIC<0.5)", np.nanmean(r['moic']<0.5).round(3), " P(MOIC>2)", np.nanmean(r['moic']>2).round(3))
        print("  IRR p10/p50/p90:", np.nanpercentile(irr,[10,50,90]).round(3))
        print("  Jaime: mean net", round(jn.mean()), " P(loss)", (jn<0).mean().round(3), " mean in", round(jin.mean()), " p50 in", round(np.percentile(jin,50)), " p95 in", round(np.percentile(jin,95)), " mean out", round((jn+jin).mean()))
        ok=~r['no_go']
        print("  conditional on going ahead: mean NPV15", round(r['npv15'][ok].mean()), " P(MOIC<1)", np.nanmean(r['moic'][ok]<1).round(3), " median equity", round(np.median(r['equity'][ok])))
