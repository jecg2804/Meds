# -*- coding: utf-8 -*-
"""Genera los documentos en Markdown desde plantillas Jinja2 y outputs/numbers.json (la única fuente de cifras).
Uso: python3 docs_src/render.py   (desde la raíz del repositorio)"""
import json
import math
import os
import sys
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, os.path.join(ROOT, 'model'))
N = json.load(open(os.path.join(ROOT, 'outputs', 'numbers.json'), encoding='utf-8'))
MINUS = '−'

DOCS = [  # (plantilla, destino relativo a la raíz)
    ('resumen.md.j2', 'docs/socios_panama/1_Resumen_para_socios_e_inversionistas.md'),
    ('plan.md.j2', 'docs/socios_panama/2_Plan_de_negocio.md'),
    ('dd.md.j2', 'docs/socios_panama/3_Debida_diligencia_del_proveedor.md'),
    ('negociacion.md.j2', 'docs/socios_panama/4_Negociacion_con_Rutul_Patel.md'),
    ('seguimiento.md.j2', 'docs/socios_panama/5_Seguimiento_operativo.md'),
    ('overview_en.md.j2', 'docs/compartido_todos/Panama_project_overview_and_requirements.md'),
    ('bitacora.md.j2', 'private/Bitacora_negocio.md'),
]


def _num(x):
    return x is not None and not (isinstance(x, float) and math.isnan(x))


def n0(x):
    if not _num(x):
        return '—'
    s = f"{abs(x):,.0f}"
    return (MINUS + s) if round(x) < 0 else s


def n1(x):
    if not _num(x):
        return '—'
    s = f"{abs(x):,.1f}"
    return (MINUS + s) if x < -0.05 else s


def b0(x):
    if not _num(x):
        return '—'
    s = f"B/.{abs(x):,.0f}"
    return (MINUS + s) if round(x) < 0 else s


def bk(x):
    """B/.385 mil; millones con un decimal"""
    if not _num(x):
        return '—'
    a = abs(x)
    if a >= 999_500:
        s = f"B/.{a / 1e6:,.2f} millones"
    else:
        s = f"B/.{a / 1000:,.0f} mil"
    return (MINUS + s) if x < 0 and round(a / 1000) > 0 else s


def pct(x, d=0):
    if not _num(x):
        return '—'
    v = x * 100
    s = f"{abs(v):.{d}f}%"
    return (MINUS + s) if v < 0 and round(abs(v), d) > 0 else s


def p3(x):
    return '—' if not _num(x) or x == 0 else f"{x:,.3f}"


def p4(x):
    return '—' if not _num(x) or x == 0 else f"{x:,.4f}"


def mx(x):
    return '—' if not _num(x) else f"{x:.2f}x"


def irrf(x):
    return 'no hay (nunca recupera)' if not _num(x) or x <= -0.99 else pct(x, 1)


def mes(m):
    from analysis import cal
    return cal(m)


def val(v, unit):
    """valor de un supuesto con su unidad"""
    if unit == '%':
        return pct(v, 1 if (v * 100) % 1 else 0)
    if unit == 'x':
        return f"{v:.2f}"
    if unit in ('B/.',):
        return b0(v)
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    return f"{v:,}" if isinstance(v, int) else f"{v}"


env = Environment(loader=FileSystemLoader(os.path.join(ROOT, 'docs_src', 'templates')), undefined=StrictUndefined,
                  trim_blocks=True, lstrip_blocks=True, keep_trailing_newline=True)
env.filters.update(n0=n0, n1=n1, b0=b0, bk=bk, pct=pct, p3=p3, p4=p4, mx=mx, irrf=irrf, mes=mes, val=val)


def main():
    for tpl, dst in DOCS:
        dpath = os.path.join(ROOT, 'private', 'drive_ids.json')
        drive = json.load(open(dpath, encoding='utf-8')) if os.path.exists(dpath) else {}
        out = env.get_template(tpl).render(N=N, I=N['inputs'], S=N['sim'], D=N['det'], W=N['whatif'], DRIVE=drive)
        path = os.path.join(ROOT, dst)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        open(path, 'w', encoding='utf-8').write(out.rstrip() + '\n')
        print(f"{dst}: {len(out.encode('utf-8')):,} bytes")


if __name__ == '__main__':
    only = sys.argv[1:]
    if only:
        DOCS[:] = [d for d in DOCS if any(o in d[0] for o in only)]
    main()
