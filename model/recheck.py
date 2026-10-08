import numpy as np, json, copy
from mc_more import run_A, run_C
from engine import run, scenario_params, T
from inputs import SKUS
inc_cns=[1 if s['group'] in ('Bueno','CNS') else 0 for s in SKUS]
cases=[('A_comprometido', dict(strategy='committed')),
       ('A_por_etapas', dict(strategy='staged')),
       ('A_por_etapas_reestructurado', dict(strategy='staged', restructured=True)),
       ('A_por_etapas_reestructurado_SNC', dict(strategy='staged', restructured=True, inc=inc_cns)),
       ('A_bueno_financia_SNC', dict(strategy='staged', bueno=True, inc=inc_cns))]
out={}
disc15=(1.15**(1/12))**(-np.arange(T+1)); disc25=(1.25**(1/12))**(-np.arange(T+1)); disc30=(1.30**(1/12))**(-np.arange(T+1))
def stats(name, cf, jcash=1/6, jout=1/6, phase0_share=1/3):
    neg=-np.where(cf<0,cf,0).sum(1); pos=np.where(cf>0,cf,0).sum(1)
    ph0=-cf[:,0]
    went=neg>ph0+1          # went beyond phase 0
    moic=np.where(neg>0,pos/neg,np.nan)
    cum=np.cumsum(cf,1); peak=-cum.min(1)
    net=pos-neg
    # Jaime: phase 0 paid by Panama side (1/3 each), injections (1-patel_cash)/3, outflows (1-patel_eq)/3
    inj=neg-ph0
    j_in=ph0*phase0_share+inj*jcash
    j_out=pos*jout
    j_net=j_out-j_in
    r=dict(p_loss=float(np.mean(net<0)), p_loss_beyond_ph0=float(np.mean(net< -ph0-1)), p_nogo=float(np.mean(~went)),
           npv15=float((cf*disc15).sum(1).mean()), npv25=float((cf*disc25).sum(1).mean()), npv30=float((cf*disc30).sum(1).mean()),
           peak_med_go=float(np.median(peak[went])), peak_p90_go=float(np.percentile(peak[went],90)), peak_mean_go=float(peak[went].mean()),
           moic_med=float(np.nanmedian(moic)), moic_med_go=float(np.nanmedian(moic[went])),
           j_in_mean=float(j_in.mean()), j_in_mean_go=float(j_in[went].mean()), j_in_p90=float(np.percentile(j_in,90)), j_net_mean=float(j_net.mean()),
           j_ploss=float(np.mean(j_net<0)), j_ploss_beyond=float(np.mean(j_net< -ph0*phase0_share-1)))
    out[name]=r
    print(name, {k:(round(v,3) if abs(v)<10 else round(v)) for k,v in r.items()})
for name,kw in cases:
    cf=run_A(**kw)
    stats(name, cf)
    if name=='A_bueno_financia_SNC':
        stats(name+'_70_30', cf, jcash=0.3/3, jout=0.5/3)
        stats(name+'_80_20', cf, jcash=0.2/3, jout=0.5/3)
cf=run_C(); stats('C', cf, jcash=1/3, jout=1/3)
json.dump(out, open('recheck.json','w'), indent=1)
# deterministic pessimistic with gate at 9 months after first sale (month 13+9=22)
p=scenario_params('pes'); p['stop_det']=22; o=run(p); cfp=o['cf_liq'][0]
print('pes stop 22: eq', round(o['eq_in'][0]), 'net', round(cfp.sum()), 'phase0', o['phase0'][0])
p=scenario_params('pes'); p['stop_det']=15; o=run(p); print('pes stop 15: net', round(o['cf_liq'][0].sum()))
