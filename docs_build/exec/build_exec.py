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
.fig img{width:100%;height:auto;display:block}
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

HTML = f"""<!doctype html>
<html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Resumen ejecutivo — Distribuidora de medicamentos para compras públicas en Panamá</title>
<style>{CSS}</style></head>
<body><div class="page">

<h1>Distribuidora de medicamentos para compras públicas en Panamá</h1>
<p class="sub">Resumen para socios e inversionistas · 8 de octubre de 2026 · Las cifras salen del modelo financiero de 60 meses y de la auditoría del 8 de octubre (documento 07). Uso interno de los socios panameños.</p>

<div class="tiles">
  <div class="tile"><div class="v">B/.2,700</div><div class="l">Lo único que se arriesga hoy: la fase 0 (verificación), entre los tres socios panameños</div></div>
  <div class="tile"><div class="v">B/.121 mil</div><div class="l">Capital hasta la primera venta en el caso de planificación (de B/.48 mil a B/.184 mil según escenario)</div></div>
  <div class="tile"><div class="v">B/.297 mil</div><div class="l">Capital máximo acumulado, mes 27, caso de planificación (de B/.184 mil a B/.321 mil)</div></div>
  <div class="tile"><div class="v">77% → 29%</div><div class="l">Probabilidad de perder más de lo puesto en la fase 0: el trato como lo propone Rutul Patel, frente al trato con las condiciones de la compuerta 0</div></div>
</div>

<h2>Qué es el negocio</h2>
<p>Una sociedad anónima panameña que importa medicamentos genéricos de un fabricante indio con certificado de buenas prácticas de la OMS, los registra ante la autoridad sanitaria de Panamá y los vende a la Caja de Seguro Social (CSS) y al Ministerio de Salud (MINSA) por licitación pública. Rutul Patel (comercializadora Zywie Worldwide, Gujarat, India) aporta el suministro; el lado panameño aporta la empresa, los registros, la licencia y la operación. Se gana por <strong>precio y cumplimiento</strong>: en estas licitaciones gana la oferta más barata que cumple el pliego, y así se adjudica el 95% de los renglones (análisis propio de los actos públicos 2020–2024). Los contactos en el Gobierno no forman parte del plan.</p>
<p>La primera ola son 11 productos que no requieren estudios de bioequivalencia en Panamá (paracetamol en tableta y jarabe, amoxicilina con clavulánico, ceftriaxona, cefotaxima, albendazol, mebendazol, nistatina, hidrocortisona y mometasona). Solo la CSS presupuesta unos B/.230 millones de medicamentos para 2027; el negocio apunta a unos B/.265 mil de ventas anuales en el año 3 del caso base, con margen bruto de 62%.</p>

<h2>Cómo entra y sale el dinero</h2>
<ol>
<li><strong>Registro sanitario</strong> de cada producto (unos B/.2,100 por producto; plazo legal de 4 a 5 meses).</li>
<li><strong>Compra</strong> a la fábrica: hoy se pagaría antes de embarcar; el plan pide 150–180 días de crédito.</li>
<li><strong>Oferta</strong> en PanamaCompra: compras menores (días) y licitaciones grandes (una vez al año, con fianza de 30% del contrato).</li>
<li><strong>Entrega</strong> desde un operador logístico licenciado (3PL); no hace falta bodega propia.</li>
<li><strong>Cobro</strong>: el Estado paga a 90 días desde la cuenta; en la práctica unos 150 días desde la entrega. Ese plazo, más la fianza, es lo que consume capital.</li>
</ol>

<div class="verdict"><strong>Veredicto a hoy: no se pone capital todavía.</strong> Tal como lo propone Rutul Patel (capital 50/50, registros pagados por nosotros, pago a la fábrica al embarcar, margen del intermediario de 15%), el negocio pierde dinero en 77 de cada 100 escenarios y devuelve 6.8% anual en el caso base, por debajo del 15% mínimo. Con tres condiciones (precio de fábrica a libro abierto hasta 1.1 veces la referencia, la fábrica paga o acredita los registros, y 150–180 días de crédito) la probabilidad de pérdida baja a 29%; si además un socio opera sin sueldo, a 18%, y el valor esperado al 15% pasa a positivo. Esas condiciones se verifican en la fase 0, que cuesta B/.2,700 y no exige constituir nada.</div>

<h2>Los números</h2>
<table>
<thead><tr><th>Indicador (60 meses)</th><th class="n">Pesimista</th><th class="n">Base</th><th class="n">Optimista</th></tr></thead>
<tbody>
<tr><td>Ventas del año 3</td><td class="n">B/.14 mil</td><td class="n">B/.265 mil</td><td class="n">B/.1.37 millones</td></tr>
<tr><td>Utilidad neta del año 3</td><td class="n">−B/.99 mil</td><td class="n">B/.64 mil</td><td class="n">B/.590 mil</td></tr>
<tr><td>Capital aportado por los socios</td><td class="n">B/.593 mil (si nadie cierra)</td><td class="n">B/.255 mil</td><td class="n">B/.183 mil</td></tr>
<tr><td>Valor presente neto al 15%</td><td class="n">−B/.430 mil</td><td class="n">−B/.56 mil</td><td class="n">+B/.951 mil</td></tr>
<tr><td>Rentabilidad anual (TIR)</td><td class="n">−93%</td><td class="n">6.8%</td><td class="n">111%</td></tr>
<tr><td>Múltiplo del capital</td><td class="n">0.05x</td><td class="n">1.29x</td><td class="n">11.0x</td></tr>
</tbody></table>
<p class="small">El pesimista supone que nadie cierra el negocio; con la compuerta operativa del plan, la pérdida se detiene en unos B/.265 mil. El optimista junta todos los supuestos favorables a la vez y casi no ocurre en la simulación. El caso base con las tarifas legales propuestas por el bufete del socio (en vez de tarifas de mercado) sube el capital a B/.294 mil.</p>
<div class="fig"><img src="{C['c1']}" alt="Capital aportado acumulado por mes en los tres escenarios"></div>
<p class="cap">Capital acumulado que ponen los socios, mes a mes. En el caso base el dinero se recupera por dividendos desde el cierre del año 3 y el grueso en el año 4; en el pesimista no hay techo si nadie cierra, y para eso existen las compuertas.</p>

<h2>Por qué el 77% y cómo baja</h2>
<div class="fig"><img src="{C['c2']}" alt="Probabilidad de perder más que la fase 0 según la estructura del trato"></div>
<p class="cap">Probabilidad de terminar con menos dinero del que se puso (más allá de la fase 0), en 20,000 escenarios que sortean costos, plazos, registros aprobados, renglones ganados, fallas de planta y ruptura del suministro.</p>
<p>El 77% mide la estructura propuesta, no el negocio en abstracto. Lo que más pesa, en orden: los costos fijos antes de vender (unos B/.4,700 al mes durante 9 meses sin ingresos), la probabilidad de ganar renglones, el colateral de las fianzas y los 150 días de cobro, el margen del intermediario y el riesgo de un problema de planta. Las tres primeras causas se atacan con dinero del otro lado (crédito y registros pagados por la fábrica) y con trabajo propio (un socio operando); la cuarta con precio a libro abierto; la quinta con la auditoría de planta de la fase 0.</p>

<h2>Qué compra cada tramo de capital</h2>
<table class="tr">
<thead><tr><th>Tramo</th><th class="n">Monto (base / planificación)</th><th>Qué paga</th><th>Solo se desembolsa si…</th></tr></thead>
<tbody>
<tr><td>Fase 0 (ahora)</td><td class="n">B/.2,700</td><td>Acuerdo de confidencialidad, cotizaciones, segunda opinión legal, auditoría documental de la planta</td><td>Nada que condicionar: es la verificación</td></tr>
<tr><td>Tramo 1: empresa y registros</td><td class="n">B/.70 mil / B/.100 mil</td><td>S.A., licencia, 3PL, cumplimiento, 11 registros sanitarios</td><td>Compuerta 0: precio hasta 1.1 veces la referencia, fábrica paga o acredita registros, crédito de 150–180 días, documentos completos</td></tr>
<tr><td>Tramo 2: operación e inventario</td><td class="n">Hasta la primera venta: B/.20 mil / B/.20 mil. Hasta el pico del mes 27: B/.168 mil / B/.176 mil</td><td>Primer inventario, costos fijos hasta cobrar, fianzas y su colateral</td><td>Compuerta 1: registros aprobados y cotizaciones firmes dentro del presupuesto</td></tr>
<tr><td>Tramo 3: segunda ola</td><td class="n">Por definir</td><td>Seis productos más (sistema nervioso), si el fabricante se verifica</td><td>Compuerta 2: ventas anualizadas de al menos B/.90 mil nueve meses después de la primera venta</td></tr>
</tbody></table>
<p class="small">Por socio panameño, con capital 50/50 con Patel: entre B/.15 mil y B/.20 mil hasta la primera venta y entre B/.43 mil y B/.50 mil hasta el pico; si Patel no aporta efectivo, el doble. El plan fija como tope prudente 15% de los ahorros líquidos de cada socio, en tramos.</p>

<h2>Cinco riesgos y cómo se controlan</h2>
<table>
<thead><tr><th>Riesgo</th><th>Qué pasaría</th><th>Control</th></tr></thead>
<tbody>
<tr><td>El precio de fábrica no deja margen</td><td>No se puede ofertar por debajo de los precios ya adjudicados</td><td>No se registra nada sin la lista de precios FOB; compuerta 0 cierra a más de 1.1 veces la referencia</td></tr>
<tr><td>Calidad del fabricante</td><td>Registro rechazado, fianza ejecutada, inventario perdido</td><td>Certificado OMS-BPM vigente (confirmado en la lista oficial india), informe de causa y corrección de dos lotes observados en 2024, auditoría de planta antes de pagar registros</td></tr>
<tr><td>No ganar renglones</td><td>Costos fijos sin ventas</td><td>Compuerta operativa: si a los nueve meses de la primera venta no hay B/.90 mil anualizados, se cierra con pérdida acotada</td></tr>
<tr><td>El Estado paga tarde o compra menos del máximo</td><td>Más capital de trabajo</td><td>Crédito de la fábrica, factoring de cuentas del Estado, oferta solo donde la compra mínima del pliego cubre el costo</td></tr>
<tr><td>Conflictos entre socios (honorarios del bufete del socio, parentesco con un funcionario)</td><td>Decisiones sesgadas o reputación</td><td>Pacto de accionistas: gastos mayores con doble firma, honorarios de partes relacionadas aprobados por los otros socios, declaración de intereses ante la ANTAI (Ley 316), ningún contacto con funcionarios fuera de los canales públicos</td></tr>
</tbody></table>

<h2>Lo que todavía no sabemos</h2>
<ul>
<li><strong>El precio real de la fábrica, el lote mínimo y la vida útil:</strong> Rutul no ha mandado la lista; es la primera petición del guion de conversación.</li>
<li><strong>Los costos fijos reales</strong> (operador logístico, regente farmacéutico, contador, fianzas): nadie los publica; se cotizan en la fase 0 con la hoja de datos de la fábrica. Son el supuesto que más mueve el resultado.</li>
<li><strong>La tasa de victoria:</strong> el modelo usa 30% en licitaciones grandes y 22% en compras menores, por encima del 17% de los entrantes; solo se conoce compitiendo, y por eso existe la compuerta operativa.</li>
</ul>

<div class="two">
<div><h2>Liquidez y salida</h2>
<p>El capital queda atado unos cinco años. Los primeros dividendos llegan al cierre del año 3, pequeños, y el grueso al cierre del año 4. No hay mercado para vender la participación; el pacto de accionistas prevé la compra a valor en libros si se rompe el suministro y una licencia de uso de los registros mientras se reemplaza al fabricante.</p></div>
<div><h2>Qué se le pide hoy a un inversionista</h2>
<p>Nada de dinero. Leer este resumen, hacer preguntas y, si le interesa, acompañar la fase 0 para ver con qué llega la fábrica. La decisión de poner capital se toma en la compuerta 0, con la lista de precios y las cotizaciones sobre la mesa, no antes.</p></div>
</div>

<div class="note"><strong>Cómo se hicieron los números.</strong> Modelo mensual de 60 meses con las cláusulas reales de los pliegos de la CSS y del MINSA (fianzas, plazos de pago, compra mínima, vida útil), tasas oficiales y precios adjudicados públicos; 20,000 escenarios simulados; una auditoría independiente el 8 de octubre revisó 31 afirmaciones contra fuentes primarias y clasificó cada cifra como firme, de fuente secundaria o supuesto. Lo firme: normas, pliegos, precios adjudicados, fletes publicados. Lo supuesto: costos fijos, tarifas de 3PL y aseguradoras, precio de la fábrica. El detalle, cifra por cifra, está en el documento 07 del paquete; el modelo completo, en el Excel adjunto.</div>

<p class="small" style="margin-top:6px">Documentos del paquete: 00 Resumen y plan · 01 Investigación del socio y del fabricante · 02 Mercado, requisitos y competencia · 03 Costos, capital y proyección · 04 Logística y operación · 05 Trato, socios y hoja de ruta · 06 Guion de conversación · 07 Auditoría y confianza · Modelo_financiero_socios.xlsx.</p>
</div></body></html>
"""
os.makedirs(OUT, exist_ok=True)
open(os.path.join(OUT, 'Resumen_ejecutivo_socios_inversionistas.html'), 'w', encoding='utf-8').write(HTML)
print('html written', len(HTML) // 1024, 'KB')
