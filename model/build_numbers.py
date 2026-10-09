# -*- coding: utf-8 -*-
"""Corre el análisis determinístico y la simulación y escribe outputs/numbers.json:
la única fuente de cifras de los documentos (docs_src/render.py la lee)."""
import json
import os
import time
import analysis
import structures
from inputs import P, FIXED, SETUP, ANNUAL_CHARGES, SKUS, MONTH1, LIC_M, RS_PAY_M

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', 'outputs', 'numbers.json')


def main():
    t0 = time.time()
    A = analysis.main()
    json.dump(A, open(os.path.join(HERE, 'analysis.json'), 'w'), ensure_ascii=False, indent=1, default=float)
    S = structures.run_all()
    json.dump(S, open(os.path.join(HERE, 'structures.json'), 'w'), ensure_ascii=False, indent=1, default=float)
    cal = analysis.cal
    base = A['det']['base']
    N = dict(
        version='2026-10-09',
        month1=A['month1'],
        calendar=dict(lic=dict(m=LIC_M, cal=cal(LIC_M)), filing=dict(m=RS_PAY_M, cal=cal(RS_PAY_M)),
                      reg=dict(m=int(P['reg_m'][3]), cal=cal(P['reg_m'][3])),
                      first_sale=dict(m=base['first_sale_m'], cal=base['first_sale_cal']),
                      cen=dict(m=base['cen_m'], cal=base['cen_cal'])),
        inputs={k: dict(label=v[0], unit=v[1], pes=v[2], base=v[3], opt=v[4], src=v[5]) for k, v in P.items()},
        fixed=[dict(label=f[0], pes=f[1], base=f[2], opt=f[3], start=f[4], src=f[5]) for f in FIXED],
        setup=[dict(label=s[0], pes=s[1], base=s[2], opt=s[3], month=s[4], sl=s[5], src=s[6]) for s in SETUP],
        annual=[dict(label=a[0], amount=a[1], src=a[2]) for a in ANNUAL_CHARGES],
        skus=[dict(id=s['id'], short=s['short'], name=s['name'], group=s['group'], inc=s['inc'], fob=s['fob'], adder=s['adder'], c2=s.get('c2'),
                   src_cost=s['src_cost'], q=[s['q1'], s['q2'], s['q3'], s['q4']], p=[s['p1'], s['p2'], s['p3'], s['p4']], b1=s['b1'])
              for s in SKUS],
        det=A['det'], cap_decomp=A['cap_decomp_base'], unit_econ=A['unit_econ'], market=A['market_first_wave'],
        breakeven=A['breakeven'], tornado=A['tornado'], whatif={w['key']: w for w in A['whatif']}, whatif_list=A['whatif'],
        pes_gate=A['pes_gate'], value_split=A['value_split'], ie=A['ie'], product_contrib=A['product_contrib'], keep_ids=A['keep_ids'], price_grid=A['price_grid'], sim=S, sim_n=S['A']['n'],
        runtime_s=round(time.time() - t0),
    )
    from engine import run, scenario_params
    ob = run(scenario_params('base'))
    N['unit_costs'] = dict(rs_unit=float(ob['rs_unit'][0]), n_first=int(sum(s['inc'] for s in SKUS)),
                           rs_first=float(ob['rs_unit'][0]) * int(sum(s['inc'] for s in SKUS)),
                           setup_after_ph0=float(ob['setup'][0].sum()), phase0=float(ob['phase0'][0]))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(N, open(OUT, 'w'), ensure_ascii=False, indent=1, default=float)
    print('numbers.json escrito en', os.path.normpath(OUT), 'en', N['runtime_s'], 's')


if __name__ == '__main__':
    main()
