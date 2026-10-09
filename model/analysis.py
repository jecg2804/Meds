# -*- coding: utf-8 -*-
"""Análisis determinístico: escenarios, descomposición del capital, economía por producto y canal, precio techo de la fábrica,
sensibilidad (tornado), casos «qué pasaría si» y punto de equilibrio. Escribe analysis.json."""
import copy
import json
import numpy as np
from engine import run, scenario_params, irr, T
from inputs import SKUS, P, FIXED, FIXED_KIND, ANNUAL_CHARGES, ANNUAL_KIND, MONTH1

MESES = ['enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio', 'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre']
CHANNELS = ['LPU de la CSS', 'MINSA centralizado', 'CSS compras menores', 'MINSA y otros, compras menores']


def cal(m):
    """mes del modelo -> 'mes de año' calendario"""
    y0, m0 = MONTH1
    k = (m0 - 1) + (int(m) - 1)
    return f"{MESES[k % 12]} de {y0 + k // 12}"


def summ(o, i=0):
    cf = o['cf_liq'][i]
    inj = o['inj'][i]; ph0 = float(o['phase0'][i])
    cum = np.cumsum(inj) + ph0
    peak_m = int(np.argmax(cum >= cum.max() - 0.5)) + 1
    first_dec = int(o['first_dec'][i]); cen = int(o['cen_start'][i])
    return dict(
        eq_in=float(o['eq_in'][i]), phase0=ph0, capital=float(o['eq_in'][i] + ph0), peak_m=peak_m, peak_cal=cal(peak_m),
        cum_at={m: float(cum[m - 1]) for m in (3, 6, 9, 12, 18, 24, 36, 48, 60)},
        npv15=float(o['npv15_liq'][i]), npv30=float(o['npv_liq'][i]), irr=float(irr(cf)), moic=float(o['moic_liq'][i]),
        first_sale_m=first_dec, first_sale_cal=cal(first_dec), cen_m=cen, cen_cal=cal(cen),
        revY=[float(x) for x in o['revY'][i]], NIY=[float(x) for x in o['NI'][i]],
        divs=float(o['div'][i].sum()), cash60=float(o['cash'][i, -1]), net=float(cf.sum()),
        fixed_month_steady=float(o['fixed'][i, -1]), zywie=float(o['zywie_profit'][i]))


def cap_decomp(o, i=0):
    """capital en el mes pico = pérdidas acumuladas hasta ese mes + capital de trabajo + caja mínima"""
    inj = o['inj'][i]; ph0 = float(o['phase0'][i])
    cum = np.cumsum(inj) + ph0
    m = int(np.argmax(cum >= cum.max() - 0.5)); mm = m + 1
    rev = o['rev'][i]; coll = o['coll'][i]; pay = o['pay'][i]; arr = o['arrivals'][i]
    recv = float(rev[:mm].sum() - coll[:mm].sum())
    prepaid = float(pay[:mm].sum() - arr[:mm].sum())
    d = dict(mes=mm, mes_cal=cal(mm), capital=float(cum[m]),
             arranque=float(o['setup'][i, :mm].sum() + ph0), registros=float(o['rs'][i, :mm].sum()),
             fijos=float((o['fixed'][i, :mm] + o['annual'][i, :mm] + o['postreg'][i, :mm]).sum()),
             impuestos=float((o['aviso'][i, :mm] + o['taxpay'][i, :mm]).sum()),
             cobrar=recv, inventario=float(o['inv'][i, m]), colateral=float(o['collat'][i, m]), anticipos=prepaid,
             caja=float(o['cash'][i, m]))
    gp = float((rev[:mm] - o['cogs'][i, :mm] * (1 + P['expiry'][3]) - o['var'][i, :mm] - o['prem'][i, :mm]).sum())
    d['margen_acumulado'] = gp
    d['check'] = d['arranque'] + d['registros'] + d['fijos'] + d['impuestos'] - gp + d['cobrar'] + d['inventario'] + d['colateral'] + d['anticipos'] + d['caja'] - d['capital']
    return d


def main():
    out = {'month1': f"{MESES[MONTH1[1] - 1]} de {MONTH1[0]}"}
    b = scenario_params('base')
    det = {}
    for sc in ('pes', 'base', 'opt'):
        det[sc] = summ(run(scenario_params(sc)))
    det['base_sl'] = summ(run(b, signaturelex=True))
    out['det'] = det
    o = run(b)
    out['cap_decomp_base'] = cap_decomp(o)
    out['monthly_base_cum'] = [float(x) for x in (np.cumsum(o['inj'][0]) + o['phase0'][0])]

    # economía por producto y canal (caso base)
    ue = []
    pack, lm = b['pack'], b['log_mult']
    gmin = [b['gm_cen'], b['gm_cen'], b['gm_dec'], b['gm_dec']]
    for j, s in enumerate(SKUS):
        row = dict(id=s['id'], short=s['short'], name=s['name'], group=s['group'], inc=s['inc'], fob_ref=s['fob'], adder=s['adder'],
                   unit_cost=float(o['unit_cost'][0, j]), src=s['src_cost'], ch=[])
        for c in range(4):
            q_eff = s[f'q{c + 1}'] * (b['cc_w'] if (c == 1 and s.get('c2') == 'cc') else 1.0)
            ourp = float(o['ourp'][c, 0, j])
            ceil = (ourp * (1 - gmin[c]) - s['adder'] * lm) / (1 + pack) if ourp > 0 else None
            row['ch'].append(dict(q=float(q_eff), p=float(s[f'p{c + 1}']), our=ourp, gm=float(o['gm'][c, 0, j]) if ourp > 0 else None,
                                  go=bool(o['go'][c, 0, j]), value=float(q_eff * s[f'p{c + 1}']),
                                  ceiling_quoted_fob=(float(ceil) if ceil is not None else None)))
        row['Rd'] = float(o['Rd'][:, 0, j].sum())
        row['Rc_exp'] = float(o['Rc'][0, 0, j] * b['pwin_cen'] + o['Rc'][1, 0, j] * b['pwin_cen'] * b['minsa_occ'])
        ue.append(row)
    out['unit_econ'] = ue
    # volumen físico en el año maduro del caso base (primera ola): unidades esperadas y m3 (volumen = adder / US$300 por m3)
    ie = []
    for j, s in enumerate(SKUS):
        if not s['inc']:
            continue
        units = 0.0
        for c in range(4):
            ourp = float(o['ourp'][c, 0, j])
            if ourp <= 0:
                continue
            rev_c = float(o['Rd'][c - 2, 0, j]) if c >= 2 else float(o['Rc'][c, 0, j]) * b['pwin_cen'] * (b['minsa_occ'] if c == 1 else 1.0)
            units += rev_c / ourp
        vol_cm3 = s['adder'] / 300.0 * 1e6
        ie.append(dict(id=s['id'], units=units, vol_cm3=vol_cm3, m3=units * vol_cm3 / 1e6))
    m3 = sum(r['m3'] for r in ie)
    out['ie'] = dict(rows=ie, m3_year=m3, pallets_year=m3 / 1.92, pallets_month=m3 / 1.92 / 12, m3_per_pallet=1.92)
    first = [r for r in ue if r['inc']]
    out['market_first_wave'] = dict(
        by_channel=[sum(r['ch'][c]['value'] for r in first) for c in range(4)],
        go_by_channel=[sum(r['ch'][c]['value'] for r in first if r['ch'][c]['go']) for c in range(4)],
        total=sum(r['ch'][c]['value'] for r in first for c in range(4)),
        total_go=sum(r['ch'][c]['value'] for r in first for c in range(4) if r['ch'][c]['go']),
        expected_rev_mature=sum(r['Rd'] + r['Rc_exp'] for r in first))

    # punto de equilibrio en ventas anuales (régimen, primera ola)
    kfac = {'staff': 1 + b['oncost'], 'service': 1 + b['itbms_srv'], 'other': 1.0}
    f_total = sum(f[2] * kfac[k] for f, k in zip(FIXED, FIXED_KIND))
    c_annual = sum(a[1] * kfac[k] for a, k in zip(ANNUAL_CHARGES, ANNUAL_KIND))
    n1 = sum(s['inc'] for s in SKUS)
    fixed_annual = f_total * 12 + c_annual + n1 * b['rs_succ'] * b['postreg']
    rev_m = out['market_first_wave']['expected_rev_mature']
    gp_m = sum((o['Rd'][:, 0, j] * (1 - o['ratio'][2:, 0, j])).sum() + o['Rc'][0, 0, j] * (1 - o['ratio'][0, 0, j]) * b['pwin_cen']
               + o['Rc'][1, 0, j] * (1 - o['ratio'][1, 0, j]) * b['pwin_cen'] * b['minsa_occ'] for j, s in enumerate(SKUS) if s['inc'])
    gm_avg = float(gp_m / rev_m) if rev_m else 0.0
    var_pct = b['dist'] + b['penal'] + b['baddebt'] + b['expiry'] * (1 - gm_avg)
    out['breakeven'] = dict(fixed_month=float(f_total), fixed_annual=float(fixed_annual), gm_avg=gm_avg, var_pct=float(var_pct),
                            be_revenue=float(fixed_annual / (gm_avg - var_pct)) if gm_avg > var_pct else None,
                            expected_rev_mature=float(rev_m))

    # tornado
    base_npv = float(o['npv15_liq'][0]); base_cap = float(o['eq_in'][0] + o['phase0'][0])
    keys = ['sup_idx', 'share_dec', 'pwin_cen', 'cen_start', 'dso_days', 'reg_m', 'mkt', 'collat', 'log_mult', 'erosion', 'pf_dec',
            'n2', 'realiz', 'cc_w', 'minsa_occ', 'expiry', 'adv', 'credit_days', 'ramp_m', 'rs_succ', 'bond_prem', 'rs_iea']
    tor = []
    for k in keys:
        r = []
        for idx in (2, 4):
            v = P[k][idx]
            if k == 'cen_start' and idx == 4:
                v = max(v, b['reg_m'] + b['bid_m'])     # con registros del caso base no se puede ofertar antes del mes 14
            p = copy.deepcopy(b); p[k] = v; oo = run(p)
            r.append((float(oo['npv15_liq'][0]), float(oo['eq_in'][0] + oo['phase0'][0]), v))
        tor.append(dict(key=k, label=P[k][0], unit=P[k][1], base_val=b[k], pes_val=r[0][2], opt_val=r[1][2],
                        npv_pes=r[0][0], npv_opt=r[1][0], cap_pes=r[0][1], cap_opt=r[1][1]))

    def fixed_block(col, itb):
        return [f[col] * (1 + itb) / (1 + b['itbms_srv']) if k == 'service' else f[col] for f, k in zip(FIXED, FIXED_KIND)], \
               sum(f[col] * (1 + b['oncost'] if k == 'staff' else (1 + itb if k == 'service' else 1.0)) for f, k in zip(FIXED, FIXED_KIND))
    fx_p, allin_p = fixed_block(1, P['itbms_srv'][2]); fx_o, allin_o = fixed_block(3, P['itbms_srv'][4])
    p = copy.deepcopy(b); p['fixed'] = fx_p; o1 = run(p)
    p = copy.deepcopy(b); p['fixed'] = fx_o; o2 = run(p)
    tor.append(dict(key='fixed', label='Costos fijos mensuales con cargas e ITBMS (bloque)', unit='B/. al mes', base_val=float(f_total),
                    pes_val=float(allin_p), opt_val=float(allin_o), npv_pes=float(o1['npv15_liq'][0]), npv_opt=float(o2['npv15_liq'][0]),
                    cap_pes=float(o1['eq_in'][0] + o1['phase0'][0]), cap_opt=float(o2['eq_in'][0] + o2['phase0'][0])))
    tor.sort(key=lambda d: -abs(d['npv_opt'] - d['npv_pes']))
    out['tornado'] = dict(base_npv15=base_npv, base_cap=base_cap, rows=tor)

    # qué pasaría si (cada fila parte del caso base)
    inc_snc = [1 if s['group'] in ('Primera ola', 'SNC') else 0 for s in SKUS]
    coord = [i for i, f in enumerate(FIXED) if f[0].startswith('Coordinador')]
    wi = []

    def wif(key, tag, p, **kw):
        oo = run(p, **kw)
        wi.append(dict(key=key, tag=tag, cap=float(oo['eq_in'][0] + oo['phase0'][0]), npv15=float(oo['npv15_liq'][0]),
                       irr=float(irr(oo['cf_liq'][0])), moic=float(oo['moic_liq'][0]), rev3=float(oo['revY'][0, 2]),
                       ni3=float(oo['NI'][0, 2]), net=float(oo['cf_liq'][0].sum())))
    wif('base', 'Caso base', b)
    p = copy.deepcopy(b); p['credit_days'] = 120; p['adv'] = 0; wif('credit120', 'Crédito de la fábrica de 120 días, sin anticipo', p)
    p = copy.deepcopy(b); p['sup_idx'] = 1.05; wif('price105', 'Precio de fábrica a 1.05 veces la referencia', p)
    p = copy.deepcopy(b)
    for i in coord: p['fixed'][i] = 0
    wif('coord0', 'Un socio coordina sin sueldo', p)
    p = copy.deepcopy(b); p['collat'] = 0.5; wif('collat50', 'Colateral de 50% de la fianza', p)
    p = copy.deepcopy(b); p['collat'] = 1.0; wif('collat100', 'Colateral de 100% de la fianza', p)
    p = copy.deepcopy(b); p['cen_start'] = 14; wif('lpu14', 'La CSS prorroga la LPU vigente y la siguiente arranca en el mes 14', p)
    p = copy.deepcopy(b); p['cc_w'] = 0.5; wif('cc50', 'El MINSA compra 50% de lo que pidió en la compra conjunta de 2023', p)
    wif('snc', 'Más 6 productos de sistema nervioso (fabricante verificado)', b, inc_override=inc_snc)
    pf = copy.deepcopy(b); pf['credit_days'] = 180; pf['adv'] = 0; pf['sup_idx'] = 1.05
    for k in ('rs_off', 'rs_iea', 'rs_law', 'rs_smp', 'rs_trad'): pf[k] = 0
    wif('factory', 'La fábrica paga los registros, da 180 días de crédito y precio 1.05', pf)
    pf2 = copy.deepcopy(pf)
    for i in coord: pf2['fixed'][i] = 0
    wif('factory_coord0', 'Lo anterior y un socio coordina sin sueldo', pf2)
    wif('factory_coord0_snc', 'Lo anterior más sistema nervioso', pf2, inc_override=inc_snc)
    wif('sl', 'Caso base con las tarifas legales de SignatureLex', b, signaturelex=True)
    # aporte de cada producto: cambio en VPN y capital si se quita de la primera ola
    inc0 = np.array([s['inc'] for s in SKUS], dtype=float)
    base_o = run(b); bnpv = float(base_o['npv15_liq'][0]); bcap = float(base_o['eq_in'][0] + base_o['phase0'][0])
    contrib = []
    for j, s in enumerate(SKUS):
        if not s['inc']:
            continue
        inc = inc0.copy(); inc[j] = 0
        oo = run(b, inc_override=inc)
        contrib.append(dict(id=s['id'], short=s['short'], name=s['name'], d_npv_if_dropped=float(oo['npv15_liq'][0]) - bnpv,
                            d_cap_if_dropped=float(oo['eq_in'][0] + oo['phase0'][0]) - bcap))
    out['product_contrib'] = contrib
    keep = [c['id'] for c in contrib if c['d_npv_if_dropped'] < 0]
    inc_keep = [1 if s['id'] in keep else 0 for s in SKUS]
    wif('keep', f"Solo los {len(keep)} productos que pagan su registro", b, inc_override=inc_keep)
    out['keep_ids'] = keep
    out['whatif'] = wi

    # precio de fábrica que haría falta, según la estructura
    def struct_params(kind):
        p = copy.deepcopy(b)
        if kind in ('factory', 'factory_coord0'):
            p['credit_days'] = 180; p['adv'] = 0
            for k in ('rs_off', 'rs_iea', 'rs_law', 'rs_smp', 'rs_trad'): p[k] = 0
        if kind == 'factory_coord0':
            for i in coord: p['fixed'][i] = 0
        return p
    grid = []
    for kind, lab in (('base', 'Términos de la propuesta'), ('factory', 'La fábrica paga registros y da 180 días'),
                      ('factory_coord0', 'La fábrica financia y un socio coordina sin sueldo')):
        for snc in (False, True):
            row = dict(kind=kind, label=lab + (' + sistema nervioso' if snc else ''), cells=[])
            for si in (0.7, 0.8, 1.0, 1.25):
                p = struct_params(kind); p['sup_idx'] = si
                oo = run(p, inc_override=(inc_snc if snc else None))
                row['cells'].append(dict(sup_idx=si, npv15=float(oo['npv15_liq'][0]), cap=float(oo['eq_in'][0] + oo['phase0'][0])))
            grid.append(row)
    out['price_grid'] = grid

    # caso pesimista con la compuerta operativa (cierre a los 9 meses de la primera venta)
    pp = scenario_params('pes'); op = run(pp); gm_ = int(op['first_dec'][0]) + 9; pp['stop_det'] = gm_; op2 = run(pp)
    out['pes_gate'] = dict(gate_m=gm_, gate_cal=cal(gm_), net=float(op2['cf_liq'][0].sum()), cap=float(op2['eq_in'][0] + op2['phase0'][0]))

    # reparto del valor entre Zywie, Rutul Patel y los socios panameños (caso base y lo que se negocia)
    def split(tag, p, patel_cash, **kw):
        oo = run(p, **kw); cf = oo['cf_liq'][0]
        pos = float(np.where(cf[1:] > 0, cf[1:], 0).sum()); eq = float(oo['eq_in'][0]); zy = float(oo['zywie_profit'][0]); ph0 = float(oo['phase0'][0])
        pat = zy + 0.5 * pos - patel_cash * eq; pan = 0.5 * pos - (1 - patel_cash) * eq - ph0
        return dict(tag=tag, patel_cash=patel_cash, zywie=zy, patel=pat, panama=pan, cap_partner=eq * (1 - patel_cash) / 3 + ph0 / 3)
    pf5 = copy.deepcopy(pf); pf5['zy_markup'] = 0.05
    out['value_split'] = [split('Propuesta 50/50 (Zywie con 15% de margen)', b, 0.5),
                          split('Fábrica paga registros, 180 días, precio 1.05, Zywie 5%', pf5, 0.5),
                          split('Lo anterior con Rutul Patel aportando 70% del efectivo', pf5, 0.7)]
    return out


if __name__ == '__main__':
    res = main()
    json.dump(res, open('analysis.json', 'w'), ensure_ascii=False, indent=1, default=float)
    d = res['det']
    for k in ('pes', 'base', 'opt', 'base_sl'):
        x = d[k]
        print(f"{k:8s} cap {x['capital']:>9,.0f} pico {x['peak_m']:>2d} ({x['peak_cal']}) VPN15 {x['npv15']:>10,.0f} VPN30 {x['npv30']:>10,.0f} "
              f"TIR {x['irr'] * 100 if x['irr'] == x['irr'] else float('nan'):6.1f}% MOIC {x['moic']:.2f} 1a venta {x['first_sale_m']} cen {x['cen_m']} "
              f"ventas a3 {x['revY'][2]:,.0f} util a3 {x['NIY'][2]:,.0f}")
    print('descomp', {k: round(v) if isinstance(v, float) else v for k, v in res['cap_decomp_base'].items()})
    print('mercado', {k: (round(v) if isinstance(v, float) else [round(x) for x in v]) for k, v in res['market_first_wave'].items()})
    print('equilibrio', {k: (round(v, 3) if isinstance(v, float) else v) for k, v in res['breakeven'].items()})
    for w in res['whatif']:
        print(f"{w['tag'][:70]:70s} cap {w['cap']:>9,.0f} VPN15 {w['npv15']:>9,.0f} TIR {w['irr'] * 100:6.1f}% MOIC {w['moic']:.2f}")
    print('TORNADO')
    for t in res['tornado']['rows'][:14]:
        print(f"{t['label'][:60]:60s} {t['npv_pes']:>10,.0f} {t['npv_opt']:>10,.0f} cap {t['cap_pes']:>9,.0f} {t['cap_opt']:>9,.0f}")
    print('split', [(s['tag'][:30], round(s['zywie']), round(s['patel']), round(s['panama'])) for s in res['value_split']])
    print('pes_gate', res['pes_gate'])
    print('ie', round(res['ie']['m3_year'], 1), 'm3/año', round(res['ie']['pallets_month'], 2), 'tarimas/mes', [(r['id'], round(r['units']), round(r['m3'], 1)) for r in res['ie']['rows']])
