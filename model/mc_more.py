import numpy as np
from mc import simulate, jaime_view, tri_ppf
from engine import irr_rows, T
from inputs import SKUS

def restructured_override(n, seed, lean=True):
    rng=np.random.default_rng(seed+777)
    o={'credit_days': tri_ppf(rng.random(n),60,120,180), 'adv': tri_ppf(rng.random(n),0,0,0.3),
       'sup_idx': tri_ppf(rng.random(n),0.95,1.05,1.30)}
    return o

def stats(cf, label, jfrac_in=1/6, jfrac_out=1/6):
    pos=np.where(cf>0,cf,0).sum(axis=1); neg=-np.where(cf<0,cf,0).sum(axis=1)
    moic=np.where(neg>0,pos/neg,np.nan)
    disc=(1.15**(1/12))**(-np.arange(T+1))
    npv=(cf*disc).sum(axis=1)
    cum=np.cumsum(cf,axis=1); peak=-cum.min(axis=1)
    jn=pos*jfrac_out-neg*jfrac_in
    r=dict(label=label, mean_npv15=float(npv.mean()), p_npv_neg=float((npv<0).mean()), p_moic_lt1=float(np.nanmean(moic<1)),
           p_moic_lt05=float(np.nanmean(moic<0.5)), p_moic_gt2=float(np.nanmean(moic>2)),
           moic_pcts=[float(x) for x in np.nanpercentile(moic,[10,25,50,75,90])],
           npv_pcts=[float(x) for x in np.percentile(npv,[5,10,25,50,75,90,95])],
           peak_pcts=[float(x) for x in np.percentile(peak,[10,50,90])], mean_peak=float(peak.mean()),
           j_in_mean=float((neg*jfrac_in).mean()), j_net_mean=float(jn.mean()), j_ploss=float((jn<0).mean()),
           j_in_pcts=[float(x) for x in np.percentile(neg*jfrac_in,[10,50,90])])
    return r, npv, moic

def bueno_override(n, seed):
    rng=np.random.default_rng(seed+11)
    z=np.zeros(n)
    return {'credit_days':tri_ppf(rng.random(n),120,180,180),'adv':z.copy(),'sup_idx':tri_ppf(rng.random(n),0.95,1.05,1.3),
            'rs_off':z.copy(),'rs_iea':z.copy(),'rs_law':z.copy(),'rs_smp':z.copy()}

def run_A(strategy, n_total=20000, chunk=4000, restructured=False, inc=None, lean=False, p_extra=None, bueno=False):
    cfs=[]
    for i in range(n_total//chunk):
        seed=1000+i
        po=restructured_override(chunk, seed) if restructured else {}
        if bueno: po=bueno_override(chunk, seed)
        if lean:
            rng=np.random.default_rng(seed+99)
            po['_lean']=True
        if p_extra: po.update(p_extra)
        po2={k:v for k,v in po.items() if not k.startswith('_')}
        r=simulate(n=chunk, seed=seed, strategy=strategy, p_override=po2 or None, inc_override=inc)
        cfs.append(r['cf'])
    return np.concatenate(cfs)

def run_C(n_total=20000, chunk=4000, rho_lo=0.2, rho_mode=0.3, rho_hi=0.4, staged=True):
    cfs=[]
    for i in range(n_total//chunk):
        seed=2000+i
        rng=np.random.default_rng(seed+5)
        # incumbent distributor performance uplift
        from mc import draw
        r=simulate(n=chunk, seed=seed, strategy='staged' if staged else 'committed',
                   p_override=None, gate_runrate=0)       # gate disabled: low burn, keep running
        o=r['o']; p=r['p']; n=chunk
        rho=tri_ppf(rng.random(n),rho_lo,rho_mode,rho_hi)
        uplift=1.25
        rev=o['rev']*uplift; cogs=o['cogs']*uplift*(1+np.asarray(p['expiry']))[:,None]
        gp=rev*(1-np.asarray(p['baddebt']))[:,None]-cogs-rev*(np.asarray(p['dist'])+np.asarray(p['penal']))[:,None]
        dso=np.rint(np.asarray(p['dso_days'])/30).astype(int)+1
        roy=np.zeros((n,T))
        for k in range(n):
            d=dso[k]; roy[k,d:]=rho[k]*gp[k,:T-d]
        n1=sum(s['inc'] for s in SKUS)
        it=np.asarray(p['itbms_srv'])*np.ones(n); oc=np.asarray(p['oncost'])*np.ones(n)
        rs_unit=np.asarray(p['rs_off'])+np.asarray(p['rs_iea'])+np.asarray(p['rs_law'])*(1+it)+np.asarray(p['rs_smp'])+500
        cf=np.zeros((n,T+1))
        ph0=np.asarray(p['setup'][0])
        cf[:,0]=-ph0
        cf[:,1]-=5650*(1+it)
        cf[:,3]-=n1*rs_unit
        m2=np.clip(np.rint(np.asarray(p['m2'])).astype(int),1,T)
        n2=np.asarray(p['n2'])
        cf[np.arange(n),m2]-=n2*rs_unit
        fixed=tri_ppf(rng.random(n),600,800,1200)*(1+0.5*oc+0.3*it)    # about half regente salary (on-costs), 30% services (ITBMS)
        stop=r['stop_m']
        tt=np.arange(1,T+1)
        alive=(tt[None,:]<=np.minimum(stop+3,61)[:,None])
        cf[:,1:]-=fixed[:,None]*alive
        for m in (1,13,25,37,49): cf[:,m]-=(300+250*(1+it))*alive[:,m-1]
        cf[:,1:]+=roy
        prof=cf[:,1:].reshape(n,5,12).sum(axis=2)
        tax=np.maximum(0,prof)*0.25
        for y in range(4): cf[:,12*(y+1)+3]-=tax[:,y]
        cf[:,T]-=tax[:,4]
        for m in (15,27,39,51):        # aviso de operacion on net contributed capital, non-deductible
            y=(m-3)//12; netcap=-cf[:,1:12*y+1].sum(axis=1)
            cf[:,m]-=np.maximum(100,0.02*np.maximum(0,netcap))*alive[:,m-1]
        tv=np.array([0.9*rho[k]*gp[k,T-dso[k]:T].sum() for k in range(n)])
        cf[:,T]+=tv
        # no-go at phase 0 (staged): only phase 0 lost
        ng=r['no_go']
        cf[ng]=0; cf[ng,0]=-ph0[ng]
        cfs.append(cf)
    return np.concatenate(cfs)

if __name__=='__main__':
    import json
    results={}
    inc_cns=[1 if s['group'] in ('Bueno','CNS') else 0 for s in SKUS]
    cases=[('A_comprometido', dict(strategy='committed')),
           ('A_por_etapas', dict(strategy='staged')),
           ('A_por_etapas_reestructurado', dict(strategy='staged', restructured=True)),
           ('A_por_etapas_reestructurado_SNC', dict(strategy='staged', restructured=True, inc=inc_cns)),
           ('A_bueno_financia_SNC', dict(strategy='staged', bueno=True, inc=inc_cns))]
    for name,kw in cases:
        cf=run_A(**kw)
        jin = 1/6; jout = 1/6
        r,npv,moic=stats(cf,name,jin,jout)
        results[name]=r
        np.save(f'npv_{name}.npy', npv); np.save(f'moic_{name}.npy', moic); np.save(f'cf_{name}.npy', cf[:4000])
        print(name, {k:(round(v,3) if isinstance(v,float) else [round(x,2) for x in v] if isinstance(v,list) else v) for k,v in r.items() if k!='label'})
    cf=run_C()
    r,npv,moic=stats(cf,'C_registros_y_distribuidor',1/3,1/3)     # Panama side funds 100% of NewCo, Jaime 1/3
    results['C_registros_y_distribuidor']=r
    results['C']=r
    np.save('npv_C.npy', npv); np.save('moic_C.npy', moic); np.save('cf_C.npy', cf[:4000])
    print('C', {k:(round(v,3) if isinstance(v,float) else [round(x,2) for x in v] if isinstance(v,list) else v) for k,v in r.items() if k!='label'})
    json.dump(results, open('mc_summary.json','w'), indent=1)
