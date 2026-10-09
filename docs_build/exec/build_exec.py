# -*- coding: utf-8 -*-
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.environ.get('BUILD_DIR', os.path.join(HERE, '..', '..', 'build'))
C = json.load(open(os.path.join(BUILD, 'charts.json')))
OUT = BUILD   # the HTML is only an intermediate for the PDF; Markdown is the reading format

CSS = """
:root{--ink:#0b0b0b;--ink2:#52514e;--muted:#8a8984;--line:#e6e5e1;--surface:#ffffff;--tile:#f6f5f2;--accent:#2a78d6;--warn:#b45309}
*{box-sizing:border-box}
html,body{margin:0;padding:0;background:var(--surface);color:var(--ink);font-family:"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;font-size:10.4pt;line-height:1.38}
.page{max-width:820px;margin:0 auto;padding:28px 36px 48px}
h1{font-size:22pt;line-height:1.15;margin:0 0 4px;letter-spacing:-.01em}
.sub{color:var(--ink2);font-size:10.5pt;margin:0 0 18px}
h2{font-size:13pt;margin:16px 0 6px;padding-top:5px;border-top:1px solid var(--line)}
h3{font-size:11pt;margin:14px 0 4px}
p{margin:6px 0}
.tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:14px 0 6px}
.tile{background:var(--tile);border-radius:8px;padding:12px 12px 10px}
.tile .v{font-size:19.5pt;white-space:nowrap;font-weight:600;letter-spacing:-.01em;line-height:1.05;font-variant-numeric:tabular-nums}
.tile .l{font-size:9pt;color:var(--ink2);margin-top:5px;line-height:1.3}
table{border-collapse:collapse;width:100%;margin:8px 0 10px;font-size:9.8pt}
th,td{text-align:left;vertical-align:top;padding:5px 7px;border-bottom:1px solid var(--line)}
th{font-weight:600;color:var(--ink2);font-size:9.2pt;border-bottom:1.5px solid #cfcdc7}
td.n,th.n{text-align:right;font-variant-numeric:tabular-nums;white-space:nowrap}
table.tr td.n,table.tr th.n{white-space:normal;text-align:left;width:24%}
table.tr td:first-child{width:16%}
.fig{margin:10px 0 4px}
.fig img{max-height:62mm;width:auto;max-width:100%;height:auto;display:block;margin:0 auto}
.cap{font-size:9pt;color:var(--ink2);margin:4px 0 10px}
ul,ol{margin:4px 0 8px 20px;padding:0}
li{margin:3px 0}
.note{background:var(--tile);border-left:3px solid var(--accent);padding:8px 12px;border-radius:0 6px 6px 0;margin:8px 0}
.verdict{background:#fff7ed;border-left:3px solid var(--warn);padding:9px 12px;border-radius:0 6px 6px 0;margin:10px 0}
.small{font-size:9.2pt;color:var(--ink2)}
.two{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media print{.page{max-width:none;padding:0}h2{break-after:avoid}.fig,.tile,.note,.verdict,tr{break-inside:avoid}thead{display:table-header-group}@page{size:A4;margin:13mm 13mm}}
@media (max-width:640px){.tiles{grid-template-columns:repeat(2,1fr)}.two{grid-template-columns:1fr}.page{padding:18px 16px 36px}}
"""

import re, subprocess, sys
SOCIOS = os.environ.get('SOCIOS_OUT', os.path.join(HERE, '..', '..', 'docs', 'socios'))
MD = open(os.path.join(SOCIOS, 'Resumen_ejecutivo_socios_inversionistas.md'), encoding='utf-8').read()


def pandoc(md):
    r = subprocess.run(['pandoc', '-f', 'gfm-tex_math_dollars', '-t', 'html', '--wrap=none'], input=md.encode('utf-8'), capture_output=True, check=True)
    h = r.stdout.decode('utf-8')
    h = re.sub(r' id="[^"]*"', '', h)
    h = re.sub(r' class="[^"]*"', '', h)
    return h.replace('<ol type="1">', '<ol>')


# 1. título y subtítulo
m = re.match(r'# (.*?)\n\n\*(.*?)\*\n\n', MD, flags=re.S)
title, sub = m.group(1), m.group(2)
body = MD[m.end():]
# 2. la primera tabla (4 columnas) son los mosaicos
tbl = re.match(r'\| (.*?) \|\n\| --- \| --- \| --- \| --- \|\n\| (.*?) \|\n\n', body)
labels = [c.strip() for c in tbl.group(1).split(' | ')]
cells = [c.strip() for c in tbl.group(2).split(' | ')]
tiles = []
for lab, cell in zip(labels, cells):
    v = re.match(r'\*\*(.*?)\*\*:?\s*(.*)', cell, flags=re.S)
    val, rest = (v.group(1), v.group(2)) if v else (cell, '')
    rest = pandoc(rest).strip()
    rest = re.sub(r'^<p>|</p>$', '', rest)
    tiles.append(f'<div class="tile"><div class="v">{val}</div><div class="l">{lab}: {rest}</div></div>')
body = body[tbl.end():]
h = pandoc(body)
# 3. clases: veredicto (blockquote), nota final, párrafos cortos bajo tablas
h = h.replace('<blockquote>\n<p>', '<div class="verdict">').replace('</p>\n</blockquote>', '</div>')
h = re.sub(r'<h2>Cómo se hicieron los números</h2>\n<p>(.*?)</p>', r'<div class="note"><strong>Cómo se hicieron los números.</strong> \1</div>', h, flags=re.S)
# 4. gráficos: capital acumulado tras la tabla de escenarios; probabilidad tras el título del 77%
cap1 = ''  # la leyenda ya está en el Markdown
cap2 = ''  # ídem
h = h.replace('<h2>Por qué el 77% y cómo baja</h2>', '<h2>Por qué el 77% y cómo baja</h2>\n<div class="fig"><img src="' + C['c2'] + '" alt="Probabilidad de perder más que la fase 0 según la estructura del trato"></div>\n' + cap2, 1)
k = h.index('<h2>Por qué el 77% y cómo baja</h2>')
j = h.rfind('</table>', 0, k)
h = h[:j + len('</table>')] + '\n<div class="fig"><img src="' + C['c1'] + '" alt="Capital aportado acumulado por mes en los tres escenarios"></div>\n' + cap1 + h[j + len('</table>'):]
# 5. celdas numéricas a la derecha en las tablas de escenarios y de probabilidades
h = re.sub(r'<td>([−+]?B/\.[\d.,]+ ?(mil|millones)?[^<]{0,40}|[−+]?\d[\d.,]*%?x?|nunca)</td>', r'<td class="n">\1</td>', h)

HTML = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Resumen ejecutivo — Distribuidora de medicamentos para compras públicas en Panamá</title>
<style>{CSS}</style></head>
<body><div class="page">
<h1>{title}</h1>
<p class="sub">{sub}</p>
<div class="tiles">{''.join(tiles)}</div>
{h}
</div></body></html>
"""
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'Resumen_ejecutivo_socios_inversionistas.html'), 'w', encoding='utf-8').write(HTML)
print('html written', len(HTML) // 1024, 'KB (desde el Markdown)')
