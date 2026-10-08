# -*- coding: utf-8 -*-
"""Build the navigable HTML package (one self-contained file) from the partner markdown docs,
plus an audit report (empty cells, unresolved cross-references, leftover markers).
Run: python3 build_html.py [SOCIOS_DIR]
"""
import os, re, subprocess, sys, html, json

SRC = sys.argv[1] if len(sys.argv) > 1 else '/mnt/user-data/outputs/socios'
OUT_HTML = os.path.join(SRC, 'Farma_paquete_socios.html')
DOCS = [
    ('00', '00_Resumen_y_plan.md', 'Resumen y plan'),
    ('01', '01_Investigacion_Rutul_y_fabricante.md', 'Investigación de Rutul y el fabricante'),
    ('02', '02_Mercado_requisitos_y_competencia.md', 'Mercado, requisitos y competencia'),
    ('03', '03_Costos_capital_y_proyeccion.md', 'Costos, capital y proyección'),
    ('04', '04_Logistica_y_operacion.md', 'Logística y operación'),
    ('05', '05_Trato_socios_y_hoja_de_ruta.md', 'Trato, socios y hoja de ruta'),
    ('06', '06_Guion_conversacion_Rutul.md', 'Guion de conversación con Rutul'),
    ('07', '07_Auditoria_y_confianza.md', 'Auditoría y confianza'),
]
TITLE = {k: t for k, _, t in DOCS}


def pandoc(md):
    r = subprocess.run(['pandoc', '-f', 'gfm-tex_math_dollars', '-t', 'html', '--wrap=none'], input=md.encode('utf-8'), capture_output=True, check=True)
    h = r.stdout.decode('utf-8')
    h = re.sub(r' id="[^"]*"', '', h)
    h = re.sub(r' class="[^"]*"', '', h)
    h = h.replace('<label><input type="checkbox" />', '☐ ').replace('</label>', '').replace('<ol type="1">', '<ol>')
    return h


def link_refs(h):
    # 0X_Nombre_de_archivo(.md) → link to section
    def rep(m):
        k = m.group(1)
        return f'<a href="#doc-{k}">{k} {TITLE.get(k, "")}</a>'
    h = re.sub(r'\b(0[0-7])_[A-Za-zÁÉÍÓÚáéíóúñÑ_]+(?:\.md)?', rep, h)
    # "(ver 03)" / "ver 07" / "documento 04" / "documentos 03 y 04"
    h = re.sub(r'\b(ver|documento|documentos|en|el|del) (0[0-7])\b(?![\d_])', lambda m: f'{m.group(1)} <a href="#doc-{m.group(2)}">{m.group(2)}</a>', h)
    return h


def heading_ids(h, key):
    # give h2/h3 anchors for the sidebar
    toc = []
    def rep(m):
        lvl, text = m.group(1), m.group(2)
        slug = key + '-' + re.sub(r'[^a-z0-9]+', '-', re.sub(r'<[^>]+>', '', text).lower()).strip('-')[:60]
        toc.append((lvl, re.sub(r'<[^>]+>', '', text), slug))
        return f'<h{lvl} id="{slug}">{text}</h{lvl}>'
    h = re.sub(r'<h([23])>(.*?)</h\1>', rep, h, flags=re.S)
    return h, toc


def audit(md, name):
    issues = []
    lines = md.split('\n')
    for i, l in enumerate(lines, 1):
        if l.startswith('|') and not re.match(r'^\|[\s:|-]+\|$', l):
            cells = [c.strip() for c in l.strip().strip('|').split('|')]
            empties = sum(1 for c in cells if c == '')
            if empties and not name.startswith('06'):   # 06 tracking table is meant to be blank
                issues.append(f'{name}:{i} fila con {empties} celda(s) vacía(s)')
    for pat, label in [(r'socio indio', 'socio indio'), (r'\bTBD\b', 'TBD'), (r'\[\[', 'marcador [['), (r'embedded content', 'embedded content'), (r'  +\S', 'doble espacio')]:
        for i, l in enumerate(lines, 1):
            if re.search(pat, l):
                issues.append(f'{name}:{i} {label}')
    return issues


CSS = """
:root{--ink:#0b0b0b;--ink2:#52514e;--muted:#8a8984;--line:#e6e5e1;--surface:#fff;--tile:#f6f5f2;--accent:#2a78d6;--bubble:#e8f1fb}
*{box-sizing:border-box}html{scroll-behavior:smooth}
body{margin:0;background:var(--surface);color:var(--ink);font-family:"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;font-size:15px;line-height:1.5}
a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
.wrap{display:grid;grid-template-columns:280px 1fr;min-height:100vh}
nav{position:sticky;top:0;height:100vh;overflow:auto;border-right:1px solid var(--line);padding:18px 14px;background:var(--tile);font-size:13px}
nav h1{font-size:15px;margin:0 0 10px}
nav .doc{margin:8px 0 2px;font-weight:600}
nav ul{list-style:none;margin:0 0 4px 10px;padding:0}nav li{margin:2px 0;color:var(--ink2)}nav li a{color:var(--ink2)}
main{padding:28px 40px 60px;max-width:960px}
section.doc{padding-top:8px;margin-bottom:48px;border-top:3px solid var(--line)}
section.doc>h1{font-size:24px;margin:18px 0 6px;letter-spacing:-.01em}
.meta{color:var(--ink2);font-size:13px;margin:0 0 14px}
h2{font-size:18px;margin:26px 0 8px;padding-top:8px;border-top:1px solid var(--line)}
h3{font-size:15.5px;margin:18px 0 6px}
p{margin:7px 0}ul,ol{margin:6px 0 10px 22px;padding:0}li{margin:3px 0}
table{border-collapse:collapse;width:100%;margin:10px 0 14px;font-size:13.5px}
th,td{text-align:left;vertical-align:top;padding:6px 8px;border-bottom:1px solid var(--line)}
th{font-weight:600;color:var(--ink2);font-size:12.5px;background:var(--tile);border-bottom:1.5px solid #cfcdc7}
tbody tr:nth-child(even){background:#fbfaf8}
td:first-child{font-weight:500}
pre{background:var(--bubble);border-radius:12px;padding:10px 14px;white-space:pre-wrap;font-family:inherit;font-size:14px;margin:8px 0}
code{font-family:ui-monospace,Menlo,Consolas,monospace;font-size:13px}
pre code{font-family:inherit;font-size:inherit}
.index{background:var(--tile);border-radius:10px;padding:14px 18px;margin:10px 0 20px}
.index table{font-size:13.5px}
.exec{border:1px solid var(--line);border-radius:10px;padding:6px 22px 18px;margin:10px 0 30px}
.exec .tiles{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:14px 0 6px}
.exec .tile{background:var(--tile);border-radius:8px;padding:12px}
.exec .tile .v{font-size:22px;font-weight:600;white-space:nowrap}
.exec .tile .l{font-size:12px;color:var(--ink2);margin-top:4px}
.exec .verdict{background:#fff7ed;border-left:3px solid #b45309;padding:9px 12px;border-radius:0 6px 6px 0;margin:10px 0}
.exec .note{background:var(--tile);border-left:3px solid var(--accent);padding:9px 12px;border-radius:0 6px 6px 0;margin:10px 0}
.exec .fig img{width:100%;height:auto;display:block}.exec .cap{font-size:12.5px;color:var(--ink2)}
.exec .two{display:grid;grid-template-columns:1fr 1fr;gap:18px}.exec .small{font-size:13px;color:var(--ink2)}
.exec .sub{color:var(--ink2);font-size:13.5px}
.topbar{display:none}
@media (max-width:980px){.wrap{grid-template-columns:1fr}nav{position:static;height:auto;border-right:0;border-bottom:1px solid var(--line)}main{padding:18px 16px 40px}.exec .tiles{grid-template-columns:repeat(2,1fr)}.exec .two{grid-template-columns:1fr}table{display:block;overflow-x:auto}}
@media print{nav{display:none}.wrap{display:block}main{max-width:none;padding:0}section.doc{break-before:page;border-top:0}h2{break-after:avoid}tr,.exec .tile,.exec .note,.exec .verdict{break-inside:avoid}thead{display:table-header-group}@page{size:A4;margin:14mm 13mm}body{font-size:11pt}table{font-size:9.5pt}}
"""

parts, nav, issues = [], [], []
# executive summary body
exec_path = os.path.join(SRC, 'Resumen_ejecutivo_socios_inversionistas.html')
if os.path.exists(exec_path):
    e = open(exec_path, encoding='utf-8').read()
    body = e[e.index('<div class="page">') + len('<div class="page">'):e.rindex('</div></body>')]
    body = body.replace('<h1>', '<h1 id="doc-RE">', 1)
    parts.append(f'<section class="doc exec" id="doc-RE">{body}</section>')
    nav.append(('RE', 'Resumen ejecutivo', []))

for key, fn, title in DOCS:
    md = open(os.path.join(SRC, fn), encoding='utf-8').read()
    issues += audit(md, fn)
    h = pandoc(md)
    h = link_refs(h)
    h, toc = heading_ids(h, 'd' + key)
    # first h1 → section title with anchor
    h = re.sub(r'<h1>(.*?)</h1>', lambda m: f'<h1>{key} · {m.group(1)}</h1>', h, count=1)
    h = h.replace('<p><em>Preparado el', '<p class="meta"><em>Preparado el', 1)
    parts.append(f'<section class="doc" id="doc-{key}">{h}</section>')
    nav.append((key, title, [(t, s) for lvl, t, s in toc if lvl == '2']))

index = """
<section class="doc" id="top" style="border-top:0">
<h1>Farma · Paquete para socios</h1>
<p class="meta">Distribuidora de medicamentos para compras públicas en Panamá · versión del 8 de octubre de 2026 · uso interno de los socios panameños; no se comparte con Rutul Patel ni con terceros.</p>
<div class="index">
<p><strong>Cómo leerlo según lo que usted necesita decidir</strong></p>
<table><thead><tr><th>Si usted…</th><th>Lea, en este orden</th><th>Tiempo de lectura</th></tr></thead><tbody>
<tr><td>Solo va a poner dinero</td><td><a href="#doc-RE">Resumen ejecutivo</a> → <a href="#doc-03">03 Costos, capital y proyección</a> (secciones «Inversión» y «Riesgo cuantificado») → <a href="#doc-07">07 Auditoría</a> («Cómo leer el 77%»)</td><td>Corto</td></tr>
<tr><td>Va a operar o a hablar con Rutul</td><td><a href="#doc-00">00 Resumen y plan</a> → <a href="#doc-06">06 Guion</a> → <a href="#doc-04">04 Logística</a> → <a href="#doc-02">02 Mercado</a></td><td>Medio</td></tr>
<tr><td>Va a firmar el pacto o revisar lo legal</td><td><a href="#doc-05">05 Trato, socios y hoja de ruta</a> → <a href="#doc-01">01 Investigación</a> → <a href="#doc-02">02 Mercado</a> («Ruta regulatoria»)</td><td>Medio</td></tr>
<tr><td>Tiene que defender un número</td><td><a href="#doc-07">07 Auditoría y confianza</a> (tabla de afirmaciones) → el documento donde se usa</td><td>Según el número</td></tr>
</tbody></table>
<p><strong>Qué contiene cada documento</strong></p>
<table><thead><tr><th>Documento</th><th>Responde a</th></tr></thead><tbody>
<tr><td><a href="#doc-RE">Resumen ejecutivo</a></td><td>Qué es el negocio, el veredicto a hoy, los números, el 77% y cómo baja, tramos de capital, riesgos, lo que no sabemos</td></tr>
<tr><td><a href="#doc-00">00 Resumen y plan</a></td><td>Mapa, veredicto, línea de tiempo, plan por fases y compuertas, pendientes, glosario</td></tr>
<tr><td><a href="#doc-01">01 Investigación de Rutul y el fabricante</a></td><td>Quién es Rutul Patel, cadena de identidad, qué fabrica y qué dice el registro público</td></tr>
<tr><td><a href="#doc-02">02 Mercado, requisitos y competencia</a></td><td>Cuánto compra el Estado, canales de venta, cómo se adjudica, qué exige la DNFD y el pliego, quién compite</td></tr>
<tr><td><a href="#doc-03">03 Costos, capital y proyección</a></td><td>Costos, capital por hito y por socio, capital de trabajo, escenarios, riesgo cuantificado, supuestos</td></tr>
<tr><td><a href="#doc-04">04 Logística y operación</a></td><td>3PL, vida útil, costos logísticos y su naturaleza, correos de cotización</td></tr>
<tr><td><a href="#doc-05">05 Trato, socios y hoja de ruta</a></td><td>Estructura del trato, capital por socio, roles, hoja de términos, contratos, honorarios legales</td></tr>
<tr><td><a href="#doc-06">06 Guion de conversación con Rutul</a></td><td>Qué pedir, en qué orden, con qué palabras; señales; tabla de seguimiento</td></tr>
<tr><td><a href="#doc-07">07 Auditoría y confianza</a></td><td>Cifra por cifra: fuente, verificación, confianza y cómo argumentarla; brechas</td></tr>
</tbody></table>
<p class="meta">Reglas: ninguna cifra se cambia a mano en este archivo; se corrige la fuente (Markdown) y se regenera. Los archivos de Excel (modelo, hoja de datos de fábrica, cuestionario del 3PL) acompañan a este paquete.</p>
</div>
</section>
"""

navhtml = '<nav><h1>Farma · socios</h1><div class="doc"><a href="#top">Cómo leer este paquete</a></div>'
for key, title, subs in nav:
    label = ('Resumen ejecutivo' if key == 'RE' else f'{key} {title}')
    navhtml += f'<div class="doc"><a href="#doc-{key}">{label}</a></div>'
    if subs:
        navhtml += '<ul>' + ''.join(f'<li><a href="#{s}">{html.escape(t)}</a></li>' for t, s in subs[:12]) + '</ul>'
navhtml += '</nav>'

page = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Farma · Paquete para socios (8 oct 2026)</title><style>{CSS}</style></head>
<body><div class="wrap">{navhtml}<main>{index}{''.join(parts)}</main></div></body></html>"""
open(OUT_HTML, 'w', encoding='utf-8').write(page)
print('package:', OUT_HTML, len(page) // 1024, 'KB')
print('audit issues:', len(issues))
for i in issues[:60]:
    print(' -', i)
json.dump(issues, open(os.path.join(SRC, 'html', 'audit_issues.json'), 'w'), ensure_ascii=False, indent=1)
