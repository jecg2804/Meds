import numpy as np, copy, json
from engine import run, scenario_params, irr, T
from inputs import SKUS

def option_c(sc='base', rho=0.30, n_skus2=None, verbose=False, dist_params=None):
    p=scenario_params(sc)
    # an incumbent distributor sells our registered products: better win rates, faster ramp
    p.update(dict(share_dec=min(0.40,p['share_dec']*1.2), pwin_cen=min(0.6,p['pwin_cen']*1.2), ramp_m=max(6,p['ramp_m']-3)))
    if dist_params: p.update(dist_params)
    o=run(p)
    rev=o['rev'][0]; cogs=o['cogs'][0]*(1+p['expiry'])
    gp=rev*(1-p['baddebt'])-cogs-rev*(p['dist']+p['penal'])
    dso=int(round(p['dso_days']/30))+1
    roy=np.zeros(T); roy[dso:]=rho*gp[:T-dso]
    n1=sum(s['inc'] for s in SKUS); n2=p['n2']; m2=int(round(p['m2']))
    rs_unit=p['rs_off']+p['rs_iea']+p['rs_law']*(1+p['itbms_srv'])+p['rs_smp']+500   # + certificación de importación al amparo de RS
    out=np.zeros(T+1)
    setup=(2500+2500+650)*(1+p['itbms_srv'])
    out[0]=-p['setup'][0]                      # phase 0 DD
    out[1]-=setup; out[3]-=n1*rs_unit; out[m2]-= n2*rs_unit
    fixed=800*(1+0.5*p['oncost']+0.3*p['itbms_srv']); annual=300+250*(1+p['itbms_srv'])
    for t in range(1,T+1):
        out[t]-=fixed
        if t in (1,13,25,37,49): out[t]-=annual
        reg=n1*p['rs_succ']*(t>=p['reg_m']) + n2*p['rs_succ']*(t>=m2+3)
        out[t]-=reg*p['postreg']/12
        out[t]+=roy[t-1]
    for m in (15,27,39,51):
        y=(m-3)//12; out[m]-=max(100,0.02*max(0,-out[1:12*y+1].sum()))
    # taxes 25% on positive annual profit (simple), paid month 12y+3
    prof=np.array([out[1+12*y:13+12*y].sum() for y in range(5)])
    tax=np.maximum(0,prof)*0.25
    for y in range(4): out[12*(y+1)+3]-=tax[y]
    out[T]-=tax[4]
    # equity view: injections needed = running min of cumulative; distributions = remaining positive
    cum=np.cumsum(out)
    peak=-cum.min()
    # terminal: receivable royalties for last dso months (recovery 90%)
    tv=0.9*rho*gp[T-dso:T].sum()
    cf=out.copy(); cf[T]+=tv
    r=irr(cf)
    disc=(1.15**(1/12))**(-np.arange(T+1))
    return dict(peak=peak, npv15=float((cf*disc).sum()), irr=r, total_in=float(-cf[cf<0].sum()), total_out=float(cf[cf>0].sum()),
                royY=[float(roy[12*y:12*y+12].sum()) for y in range(5)], gpY=[float(gp[12*y:12*y+12].sum()) for y in range(5)],
                revY=[float(rev[12*y:12*y+12].sum()) for y in range(5)], moic=float(cf[cf>0].sum()/-cf[cf<0].sum()), cf=cf)
res={}
for sc in ('pes','base','opt'):
    for rho in (0.2,0.3,0.4):
        r=option_c(sc,rho); res[f'{sc}_{rho}']={k:v for k,v in r.items() if k!='cf'}
        print(f"{sc:4s} rho={rho:.1f}: peak={r['peak']:8,.0f} NPV15={r['npv15']:9,.0f} IRR={r['irr']:7.1%} MOIC={r['moic']:5.2f} roy={np.round(r['royY']).astype(int)} rev={np.round(r['revY']).astype(int)}")
json.dump(res, open('option_c.json','w'), indent=1, default=float)
