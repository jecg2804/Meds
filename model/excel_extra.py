import numpy as np, json
W=100000.0
R=json.load(open('recheck.json')); R2=json.load(open('recheck2.json')); R3=json.load(open('recheck3.json'))
def jflows(cf, cash_frac=1/6, eq_frac=1/6, ph0_frac=1/3):
    ph0=-cf[:,0]; neg=-np.where(cf<0,cf,0).sum(1); pos=np.where(cf>0,cf,0).sum(1)
    return ph0*ph0_frac+(neg-ph0)*cash_frac, pos*eq_frac
def kelly_amt(j_in, j_out, rf):
    lam_max=W/np.max(j_in)*0.999
    lams=np.linspace(0,lam_max,2000)
    el=np.array([np.mean(np.log(W*rf+l*(j_out-j_in*rf))) for l in lams])
    return float(lams[int(np.argmax(el))]*j_in.mean())
out={'kelly':{}}
for key,fn,fr in (('A_comprometido','cf_A_comprometido.npy',(1/6,1/6,1/3)),('A_por_etapas_reestructurado_SNC','cf_A_por_etapas_reestructurado_SNC.npy',(1/6,1/6,1/3)),
                  ('A_bueno_financia_SNC','cf_A_bueno_financia_SNC.npy',(1/6,1/6,1/3)),('C','cf_C.npy',(1/3,1/3,1/3))):
    cf=np.load(fn); j_in,j_out=jflows(cf,*fr)
    print(key, 'j_in_mean', round(j_in.mean()), 'recheck', round(R[key]['j_in_mean']))
    out['kelly'][key]=dict(j_in_mean=float(j_in.mean()), j_net_mean=float((j_out-j_in).mean()), k4=kelly_amt(j_in,j_out,1.04**5), k15=kelly_amt(j_in,j_out,1.15**5))
    print(out['kelly'][key])
out['kelly']['bueno_stress']=dict(k4=R3['bueno_pwin17_sup125']['rf4_amt'], npv15=R3['bueno_pwin17_sup125']['npv15'])
out['recheck']=R; out['gates']=R2
json.dump(out, open('excel_extra.json','w'), indent=1)
