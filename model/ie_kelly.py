import numpy as np, json, csv
from engine import run, scenario_params
from inputs import SKUS
b=scenario_params('base'); o=run(b)
# units per year at maturity (base) per SKU and channel
land=list(csv.DictReader(open('../research/b2_landed/landed.csv')))
upc={ 'PCT500':125000,'PCTSYR':1818,'AMCTAB':125000,'AMCSUS':1538,'CRO1G':16666,'CTX1G':16666,'ALBSUS':7692,'MBZ100':200000,'NYSSUS':5000,'HCTCRM':6060,'MOMCRM':6060}
rows=[]; tot_cbm=0; tot_cogs=0
for j,s in enumerate(SKUS):
    if not s['inc']: continue
    units=0; rev=0
    for c in range(4):
        rr = o['Rd'][c-2,0,j] if c>=2 else o['Rc'][c,0,j]*(b['pwin_cen'] if c==0 else b['pwin_cen']*b['minsa_occ'])
        price=o['ourp'][c,0,j]
        if price>0: units+=rr/price; rev+=rr
    k2=1+ b['n2']*b['rel2']/11
    cbm=units/upc[s['id']]
    cogs=units*o['unit_cost'][0,j]
    rows.append(dict(id=s['id'],units=units,rev=rev,cbm=cbm,cogs=cogs,val_density=cogs/cbm if cbm else 0))
    tot_cbm+=cbm; tot_cogs+=cogs
for r in rows: print(f"{r['id']:7s} units/yr={r['units']:11,.0f} rev={r['rev']:9,.0f} CBM/yr={r['cbm']:6.1f} COGS={r['cogs']:8,.0f} B/./CBM={r['val_density']:8,.0f}")
print('TOTAL wave-1 mature: CBM/yr',round(tot_cbm,1),' COGS',round(tot_cogs),' pallets/yr (1.92 m3 per pallet)',round(tot_cbm/1.92,1))
# EOQ
S_fixed=1000.0   # fixed cost per inbound shipment: broker+dest fixed+drayage+forwarder docs+admin (B2/B7 base)
for H_cap in (0.15,0.30):
    vd=tot_cogs/tot_cbm
    H=H_cap*vd + 12*16 + 0.03*vd     # capital + storage (~30 USD/pallet-month ~ 16/CBM-month) + expiry risk
    eoq=np.sqrt(2*tot_cbm*S_fixed/H)
    print(f"EOQ (cost of capital {H_cap:.0%}): {eoq:5.1f} CBM per shipment -> {tot_cbm/eoq:4.1f} shipments/yr; holding cost {H:6.0f} USD/CBM-yr; value density {vd:,.0f}")
# shelf-life budget
for SL in (24,30,36):
    dwell_max = SL - 18 - (1 + 2 + 0.25)
    print(f"Shelf life {SL} m -> máximo tiempo en bodega para cumplir 18 meses al entregar: {dwell_max:.2f} meses")
# Kelly for Jaime: distribution of 5-yr multiples from MC (his flows proportional when contributions == equity)
res={}
W=100000.0
for name,fn in (('A_comprometido','moic_A_comprometido.npy'),('A_por_etapas_reestructurado_SNC','moic_A_por_etapas_reestructurado_SNC.npy'),('A_bueno_financia_SNC','moic_A_bueno_financia_SNC.npy'),('C','moic_C.npy')):
    M=np.load(fn); M=M[~np.isnan(M)]
    for rf in (1.0, 1.22):     # cash at 0% or ~4%/yr for 5 yrs
        fs=np.linspace(0,0.6,121)
        el=[np.mean(np.log(np.maximum(1e-9,(1-f)*rf + f*M))) for f in fs]
        fstar=fs[int(np.argmax(el))]
        res[f'{name}_rf{rf}']=dict(fstar=float(fstar), EM=float(M.mean()), P_loss=float((M<1).mean()))
        print(f"{name:35s} rf={rf}: E[M]={M.mean():.2f} P(M<1)={np.mean(M<1):.2f}  Kelly f*={fstar:.3f} -> {fstar*W:,.0f} de 100,000; medio Kelly={fstar*W/2:,.0f}")
json.dump(dict(ie=rows, tot_cbm=tot_cbm, tot_cogs=tot_cogs, kelly=res), open('ie_kelly.json','w'), indent=1, default=float)
