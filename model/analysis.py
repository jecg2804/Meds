import numpy as np, json, copy
from engine import run, scenario_params, irr, T
from inputs import SKUS, P, FIXED, SETUP, FIXED_KIND, ANNUAL_CHARGES, ANNUAL_KIND
out={}
def summ(o):
    cf=o['cf_liq'][0]
    cum=np.cumsum(cf)
    pay=next((i for i in range(1,len(cum)) if cum[i]>=0), None)
    return dict(revY=o['revY'][0].round().tolist(), NI=o['NI'][0].round().tolist(), eq_in=round(float(o['eq_in'][0])),
                phase0=round(float(o['phase0'][0])), npv15=round(float(o['npv15_liq'][0])), npv30=round(float(o['npv_liq'][0])),
                npv15_gc=round(float(o['npv15_best'][0])), irr=float(irr(cf)), irr_gc=float(irr(o['cf_best'][0])),
                moic=float(o['moic_liq'][0]), moic_gc=float(o['moic_best'][0]), payback_m=pay, tv_liq=round(float(o['tv_liq'][0])),
                tv_gc=round(float(o['tv_gc'][0])), divs=round(float(o['div'][0].sum())), cash60=round(float(o['cash'][0,-1])),
                peak_cum_neg=round(float(-cum.min())), zywie=round(float(o['zywie_profit'][0])))
for sc in ('pes','base','opt'):
    out['det_'+sc]=summ(run(scenario_params(sc)))
b=scenario_params('base'); o=run(b)
out['monthly_base']={k: o[k][0].round(1).tolist() for k in ('rev','rev_dec','rev_cen','cogs','pay','coll','fixed','inj','cash','inv','collat','div','income')}
out['monthly_base']['cum_inj']=np.cumsum(o['inj'][0]).round(1).tolist()
# capital need decomposition at the month where cumulative injections reach 95% of total
cuminj=np.cumsum(o['inj'][0]); m95=int(np.argmax(cuminj>=0.95*cuminj[-1]))
idx=m95
dec=dict(
 setup=float(o['setup'][0,:idx+1].sum()), registros=float(o['rs'][0,:idx+1].sum()),
 fijos_y_anuales=float((o['fixed'][0,:idx+1]+o['annual'][0,:idx+1]+o['postreg'][0,:idx+1]+o['aviso'][0,:idx+1]+o['taxpay'][0,:idx+1]).sum()),
 compras_pagadas=float(o['pay'][0,:idx+1].sum()), cobros=-float(o['coll'][0,:idx+1].sum()),
 colateral=float(o['collat'][0,idx]), var=float(o['var'][0,:idx+1].sum()+o['prem'][0,:idx+1].sum()),
 caja_minima=float(o['cash'][0,idx]), mes=idx+1, total_inj=float(cuminj[idx]))
dec['check']=dec['setup']+dec['registros']+dec['fijos_y_anuales']+dec['compras_pagadas']-dec['cobros']*-1*-1+dec['colateral']+dec['var']+dec['caja_minima']
dec['check']=dec['setup']+dec['registros']+dec['fijos_y_anuales']+dec['compras_pagadas']+dec['cobros']+dec['colateral']+dec['var']+dec['caja_minima']+float(o['fact_exp'][0,:idx+1].sum())
out['cap_decomp_base']=dec
# unit economics table
ue=[]
for j,s in enumerate(SKUS):
    row=dict(id=s['id'], name=s['name'], group=s['group'], inc=s['inc'], unit_cost=float(o['unit_cost'][0,j]), src=s['src_cost'])
    for c in range(4):
        row[f'p{c+1}']=s[f'p{c+1}']; row[f'q{c+1}']=s[f'q{c+1}']
        row[f'our{c+1}']=float(o['ourp'][c,0,j]); row[f'gm{c+1}']=float(o['gm'][c,0,j]); row[f'go{c+1}']=bool(o['go'][c,0,j])
    row['Rd']=float(o['Rd'][:,0,j].sum()); row['Rc_exp']=float(o['Rc'][0,0,j]*b['pwin_cen']+o['Rc'][1,0,j]*b['pwin_cen']*b['minsa_occ'])
    row['GP_mature']=float((o['Rd'][:,0,j]*(1-o['ratio'][2:,0,j])).sum()+ (o['Rc'][0,0,j]*(1-o['ratio'][0,0,j]))*b['pwin_cen']+(o['Rc'][1,0,j]*(1-o['ratio'][1,0,j]))*b['pwin_cen']*b['minsa_occ'])
    ue.append(row)
out['unit_econ']=ue
# break-even
kfac={'staff':1+b['oncost'],'service':1+b['itbms_srv'],'other':1.0}
f_total=sum(f[2]*kfac[k] for f,k in zip(FIXED,FIXED_KIND))
c_annual=sum(a[1]*kfac[k] for a,k in zip(ANNUAL_CHARGES,ANNUAL_KIND))
fixed_annual=f_total*12 + c_annual + sum(1 for s in SKUS if s['inc'])*b['rs_succ']*b['postreg']
rev_m=sum(r['Rd']+r['Rc_exp'] for r in ue if r['inc']); gp_m=sum(r['GP_mature'] for r in ue if r['inc'])
gm_avg=gp_m/rev_m; varpct=b['dist']+b['penal']+b['baddebt']+b['expiry']*(1-gm_avg)
out['breakeven']=dict(fixed_annual=fixed_annual, f_total=f_total, c_annual=c_annual, gm_avg=gm_avg, var_pct=varpct, be_revenue=fixed_annual/(gm_avg-varpct), mature_rev_wave1=rev_m)
# tornado on NPV15 (liq) and equity
base_o=run(b); base_npv=float(base_o['npv15_liq'][0]); base_eq=float(base_o['eq_in'][0])
tor=[]
keys=['sup_idx','share_dec','pwin_cen','dso_days','cen_start','reg_m','mkt','erosion','pf_dec','n2','realiz','minsa_occ','collat','expiry','lead_days','ramp_m','rs_succ','adv','credit_days']
for k in keys:
    lab=P[k][0]
    r=[]
    for sc,i in (('pes',2),('opt',4)):
        p=copy.deepcopy(b); p[k]=P[k][i]; oo=run(p); r.append((float(oo['npv15_liq'][0]), float(oo['eq_in'][0]), P[k][i]))
    tor.append(dict(key=k,label=lab,pes_val=r[0][2],opt_val=r[1][2],base_val=b[k],npv_pes=r[0][0],npv_opt=r[1][0],eq_pes=r[0][1],eq_opt=r[1][1]))
# fixed costs as a block
for sc,i in (('pes',1),('opt',3)):
    pass
# every line of the monthly fixed-cost table moves together: amounts, plus the ITBMS on the monthly services
# at its own pessimistic/optimistic rate (0% optimistic = recovered). The ITBMS on setup and registrations stays at base,
# so the block isolates the monthly fixed costs. The engine multiplies service lines by (1 + base ITBMS), so the
# amounts are pre-scaled to land on amount x (1 + scenario ITBMS).
def fixed_block(col, itb):
    adj=[f[col]*(1+itb)/(1+b['itbms_srv']) if k=='service' else f[col] for f,k in zip(FIXED,FIXED_KIND)]
    allin=sum(f[col]*(1+b['oncost'] if k=='staff' else (1+itb if k=='service' else 1.0)) for f,k in zip(FIXED,FIXED_KIND))
    return adj, allin
fx_p, allin_p=fixed_block(1, P['itbms_srv'][2]); fx_o, allin_o=fixed_block(3, P['itbms_srv'][4])
p=copy.deepcopy(b); p['fixed']=fx_p; o1=run(p)
p=copy.deepcopy(b); p['fixed']=fx_o; o2=run(p)
tor.append(dict(key='fixed',label='Costos fijos mensuales con cargas laborales e ITBMS (bloque, B/. al mes)',pes_val=round(allin_p),opt_val=round(allin_o),base_val=round(f_total),
                npv_pes=float(o1['npv15_liq'][0]),npv_opt=float(o2['npv15_liq'][0]),eq_pes=float(o1['eq_in'][0]),eq_opt=float(o2['eq_in'][0])))
p=copy.deepcopy(b); o1=run(p, signaturelex=True)
tor.append(dict(key='signaturelex',label='Tarifas legales SignatureLex vs mercado',pes_val='SignatureLex',opt_val='mercado',base_val='mercado',
                npv_pes=float(o1['npv15_liq'][0]),npv_opt=base_npv,eq_pes=float(o1['eq_in'][0]),eq_opt=base_eq))
tor.sort(key=lambda d: -abs(d['npv_opt']-d['npv_pes']))
out['tornado']=dict(base_npv15=base_npv, base_eq=base_eq, rows=tor)
# what-ifs
wi=[]
def wif(tag, p, **kw):
    oo=run(p,**kw); wi.append(dict(tag=tag, eq=float(oo['eq_in'][0]), npv15=float(oo['npv15_liq'][0]), irr=float(irr(oo['cf_liq'][0])), moic=float(oo['moic_liq'][0]), rev3=float(oo['revY'][0,2]), ni3=float(oo['NI'][0,2])))
wif('Base', b)
p=copy.deepcopy(b); p['credit_days']=120; p['adv']=0; wif('Crédito del proveedor 120 días, sin anticipo', p)
p=copy.deepcopy(b); p['sup_idx']=1.05; wif('Precio del proveedor a libro abierto (índice 1.05)', p)
p=copy.deepcopy(b); p['fixed'][5]=0; wif('Sin coordinador pagado (los socios operan)', p)
p=copy.deepcopy(b); p['dso_days']=105; wif('Cobro en 105 días', p)
inc2=[1 if s['group'] in ('Bueno','CNS') else 0 for s in SKUS]
wif('+ 6 productos SNC con fabricante verificado', b, inc_override=inc2)
p=copy.deepcopy(b); p['n2']=20; p['rel2']=0.6; wif('Escala: 20 productos en la segunda ola', p)
p=copy.deepcopy(b); p['credit_days']=120; p['adv']=0; p['sup_idx']=1.05; p['fixed'][5]=1000; wif('Reestructurado: crédito 120 d + índice 1.05 + coordinador 1,000', p)
wif('Reestructurado + SNC', p, inc_override=inc2)
p2=copy.deepcopy(p); p2['n2']=20; p2['rel2']=0.6; wif('Reestructurado + SNC + escala 20', p2, inc_override=inc2)
wif('Base con tarifas SignatureLex', b, signaturelex=True)
pb=copy.deepcopy(b); pb['credit_days']=180; pb['adv']=0; pb['sup_idx']=1.05; pb['fixed'][5]=1000
for k in ('rs_off','rs_iea','rs_law','rs_smp'): pb[k]=0
wif('Reestructurado + SNC + Bueno paga registros y 180 días', pb, inc_override=inc2)
ob=run(pb, inc_override=inc2)
out['bueno_det']=dict(cum=np.cumsum(ob['cf_liq'][0][:T]).round(0).tolist(), eq=float(ob['eq_in'][0]))
out['base_cum']=np.cumsum(o['cf_liq'][0][:T]).round(0).tolist()
# working-capital levers on the base case
lev=[]
def lv(tag,p,**kw):
    oo=run(p,**kw); lev.append(dict(tag=tag, eq=float(oo['eq_in'][0]), d_eq=float(oo['eq_in'][0])-base_eq, npv15=float(oo['npv15_liq'][0]), irr=float(irr(oo['cf_liq'][0]))))
p=copy.deepcopy(b); p['credit_days']=120; p['adv']=0; lv('credito120',p)
p=copy.deepcopy(b); p['fact_share']=0.7; lv('factoring70',p)
p=copy.deepcopy(b); p['fixed'][5]=0; lv('sin_coordinador',p)
p=copy.deepcopy(b); p['dso_days']=105; lv('cobro105',p)
p=copy.deepcopy(b); p['collat']=0.25; lv('colateral25',p)
p=copy.deepcopy(b); p['collat']=1.0; lv('colateral100',p)
lv('signaturelex',b,signaturelex=True)
out['levers']=lev
# modelling choices that favour the base case
ch=[]
for tag,k,v in (('pwin20','pwin_cen',0.20),('share17','share_dec',0.17),('realiz50','realiz',0.50),('sin_ola2','n2',0)):
    p=copy.deepcopy(b); p[k]=v; oo=run(p); ch.append(dict(tag=tag, npv15=float(oo['npv15_liq'][0]), irr=float(irr(oo['cf_liq'][0])), eq=float(oo['eq_in'][0])))
p=copy.deepcopy(b); p['pwin_cen']=0.17; p['share_dec']=0.17; oo=run(p); ch.append(dict(tag='ambas17', npv15=float(oo['npv15_liq'][0]), irr=float(irr(oo['cf_liq'][0])), eq=float(oo['eq_in'][0])))
ia=[s['id'] for s in SKUS].index('ALBSUS'); old=SKUS[ia]['q2']; SKUS[ia]['q2']=0
oo=run(b); ch.append(dict(tag='sin_albendazol_minsa', npv15=float(oo['npv15_liq'][0]), irr=float(irr(oo['cf_liq'][0])), eq=float(oo['eq_in'][0]))); SKUS[ia]['q2']=old
out['choices']=ch
# pessimistic case with the operating gate (first decentralized sale + 9 months)
pp=scenario_params('pes'); op=run(pp); gm_=int(op['first_dec'][0])+9; pp['stop_det']=gm_; op2=run(pp)
out['pes_gate']=dict(gate_m=gm_, net=float(op2['cf_liq'][0].sum()), eq=float(op2['eq_in'][0]))
# Zywie margin and value split (Valoracion method)
spl=[]
for mk in (0.0,0.05,0.10,0.15,0.25,0.40):
    p=copy.deepcopy(b); p['zy_markup']=mk; oo=run(p); cf=oo['cf_liq'][0]
    pos=float(np.where(cf[1:]>0,cf[1:],0).sum()); eq=float(oo['eq_in'][0]); zy=float(oo['zywie_profit'][0]); ph0=float(oo['phase0'][0])
    pat=zy+0.5*pos-0.5*eq; pan=0.5*pos-0.5*eq-ph0
    spl.append(dict(mk=mk, zywie=zy, patel=pat, panama=pan, share=pat/(pat+pan) if (pat+pan)!=0 else float('nan')))
out['value_split']=spl
# value split by deal structure (same method), reproducing the table in 05 / Anexo: capital per Panamanian partner = one sixth of eq_in (50/50) or 30%/3 (70/30) plus one third of phase 0
def split_struct(tag, p, pc, **kw):
    oo=run(p,**kw); cf=oo['cf_liq'][0]
    pos=float(np.where(cf[1:]>0,cf[1:],0).sum()); eq=float(oo['eq_in'][0]); zy=float(oo['zywie_profit'][0]); ph0=float(oo['phase0'][0])
    pat=zy+0.5*pos-pc*eq; pan=0.5*pos-(1-pc)*eq-ph0
    return dict(tag=tag, patel_cash=pc, eq=eq, zywie=zy, patel=pat, panama=pan, share=pat/(pat+pan) if (pat+pan)!=0 else float('nan'), cap_socio=eq*(1-pc)/3+ph0/3)
pb5=copy.deepcopy(pb); pb5['zy_markup']=0.05
out['value_split_struct']=[split_struct('Propuesta 50/50, Zywie 15%', b, 0.5),
                           split_struct('Libro abierto 5%, Bueno paga registros y 180 días, + SNC', pb5, 0.5, inc_override=inc2),
                           split_struct('Lo anterior con Patel aportando 70% del efectivo', pb5, 0.7, inc_override=inc2)]
# creams at Indian customs prices (verification of 8 Oct) and first wave without the two creams
im=[s['id'] for s in SKUS].index('MOMCRM'); ih=[s['id'] for s in SKUS].index('HCTCRM')
old_m, old_h = SKUS[im]['fob'], SKUS[ih]['fob']
SKUS[im]['fob']=0.60; SKUS[ih]['fob']=0.28
wif('Cremas a precio de aduana india (mometasona 0.60, hidrocortisona 0.28 por tubo)', b)
SKUS[im]['fob'], SKUS[ih]['fob'] = old_m, old_h
inc_nc=[ (0 if s['id'] in ('MOMCRM','HCTCRM') else s['inc']) for s in SKUS]
wif('Primera ola sin las dos cremas', b, inc_override=inc_nc)
out['whatif']=wi
json.dump(out, open('analysis.json','w'), ensure_ascii=False, indent=1, default=float)
print(json.dumps({k:out[k] for k in ('det_pes','det_base','det_opt','cap_decomp_base','breakeven')}, ensure_ascii=False, indent=1, default=float))
for w in wi: print(f"{w['tag'][:60]:60s} eq={w['eq']:9,.0f} NPV15={w['npv15']:9,.0f} IRR={w['irr']:6.1%} MOIC={w['moic']:4.2f} Rev3={w['rev3']:9,.0f} NI3={w['ni3']:8,.0f}")
print('\nTORNADO (NPV15 base', round(base_npv),')')
for t in tor: print(f"{t['label'][:70]:70s} pes={t['npv_pes']:10,.0f} opt={t['npv_opt']:10,.0f}  [{t['pes_val']} / {t['opt_val']}]")
