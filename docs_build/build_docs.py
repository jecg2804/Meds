"""Build the partner-facing markdown package from the exported Docs + the engine.
Run from anywhere: python3 build_docs.py
"""
import json, re, os, sys, shutil
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..', 'model'))
import numpy as np
from engine import run, scenario_params

UD = os.environ.get('USER_DATA_OUT', '/mnt/user-data/outputs')          # session outputs (when running inside Claude)
REPO_DOCS = os.path.join(HERE, '..', 'docs', 'socios')                    # repo copy of the partner package
OUT = os.environ.get('SOCIOS_OUT', os.path.join(UD, 'socios') if os.path.isdir(UD) else REPO_DOCS)
os.makedirs(OUT, exist_ok=True)
XIN = os.path.join(HERE, '..', 'model', 'xlsx_inputs')                    # questionnaire + factory sheet (repo)
PERSONAL_XLSX = os.environ.get('PERSONAL_MODEL_XLSX', os.path.join(UD, 'Modelo_financiero_distribuidora_medicamentos_Panama.xlsx'))
EX = os.path.join(HERE, 'exports')
XLSX_OUT = os.environ.get('XLSX_OUT', os.path.join(HERE, '..', 'outputs'))   # Excel deliverables live in outputs/, not with the md
os.makedirs(XLSX_OUT, exist_ok=True)
rd = lambda n: open(os.path.join(EX, n), encoding='utf-8').read()
plan = rd('Plan_de_negocio_distribuidora_de_medicamentos_para_compras_públicas_en_Panamá.md')
guion = rd('Conversación_con_Rutul_guion_por_etapas.md')
hoja = rd('Hoja_de_ruta_del_lado_panameño.md')
centro = rd('Centro_de_control_del_negocio.md')


def clean(md):
    md = re.sub(r'^Oct \d+, 2026 · @\w+\n', '', md, flags=re.M)
    md = re.sub(r'^&#91;embedded content: (.*?)\\\][ \t]*$', r'*(Gráfico: \1. Ver el modelo en Excel.)*', md, flags=re.M)
    md = re.sub(r'^\[embedded content: (.*?)\][ \t]*$', r'*(Gráfico: \1. Ver el modelo en Excel.)*', md, flags=re.M)
    md = md.replace('\\_', '_')
    # cross-references that pointed inside the single plan document
    md = md.replace('(ver Mercado)', '(ver 02_Mercado_requisitos_y_competencia)')
    md = md.replace('(las tres se definen en el Plan de ejecución)', '(las tres se definen en 00_Resumen_y_plan)')
    md = md.replace('ver Capital por socio)', 'ver la sección Capital por socio)')
    # personal references → generic partner wording
    md = md.replace('excede el tope prudente de un socio', 'puede exceder el tope prudente de un socio')
    md = md.replace('aun así excede el tope', 'aun así puede exceder ese tope')
    return md


def sections(md):
    parts = re.split(r'^## ', md, flags=re.M)
    head = parts[0]
    out, order = {}, []
    for p in parts[1:]:
        title, _, body = p.partition('\n')
        out[title.strip()] = body.strip('\n')
        order.append(title.strip())
    return head, out, order


plan, guion, hoja, centro = map(clean, (plan, guion, hoja, centro))
from audit_edits import *
for _a, _b in PLAN_REPL:
    assert _a in plan, 'plan repl missing: ' + _a[:70]
    plan = plan.replace(_a, _b)
for _a, _b in HOJA_REPL:
    assert _a in hoja, 'hoja repl missing: ' + _a[:70]
    hoja = hoja.replace(_a, _b)
Phead, P, Porder = sections(plan)
Ghead, G, Gorder = sections(guion)
Hhead, H, Horder = sections(hoja)
Chead, C, Corder = sections(centro)

# ---------- sources, split by group ----------
groups, cur = {}, None
for block in re.split(r'\n\s*\n', P['Fuentes'].strip()):
    b = block.strip()
    if not b.startswith('-') and not b.startswith('Debida') and '\n' not in b and len(b) < 40:
        cur = b; groups[cur] = []
    elif cur:
        groups[cur].append(b)
    else:
        groups.setdefault('Otras', []).append(b)
print('source groups:', {k: len(v) for k, v in groups.items()})


def fuentes(*keys, extra=''):
    s = '## Fuentes\n\n'
    for k in keys:
        s += k + '\n\n' + '\n\n'.join(groups[k]) + '\n\n'
    if extra:
        s += extra.rstrip('\n') + '\n\n'
    return s.rstrip('\n') + '\n'


HEADER = ('*Preparado el 7 de octubre de 2026 para los socios panameños del proyecto. Uso interno: no se comparte con Rutul Patel ni con terceros. '
          'Las cifras salen del modelo financiero adjunto (Modelo_financiero_socios.xlsx) y de las fuentes citadas al final de cada documento; '
          'toda cifra sin cotización firme está marcada como estimación o supuesto.*\n\n')

# ---------- capital by milestone, from the engine ----------
def milestones(sc, sl=False):
    p = scenario_params(sc); o = run(p, signaturelex=sl)
    cum = np.cumsum(o['inj'][0]); ph0 = float(o['phase0'][0]); fd = int(o['first_dec'][0])
    at = lambda m: ph0 + cum[m - 1]
    return dict(ph0=ph0, fd=fd, m3=at(3), m6=at(6), m9=at(9), m12=at(12), m18=at(18), m27=at(27), fs=at(fd),
                peak=ph0 + cum.max(), peak_m=int(np.argmax(cum)) + 1, o=o, eq=float(o['eq_in'][0]))


def decomp(o, m):
    i = m - 1
    S = lambda k: float(o[k][0, :i + 1].sum())
    d = {}
    d['setup'] = S('setup'); d['rs'] = S('rs')
    d['fij'] = S('fixed') + S('annual') + S('postreg') + S('aviso') + S('taxpay')
    d['pay'] = S('pay'); d['var'] = S('var') + S('prem')
    d['col'] = float(o['collat'][0, i]); d['cash'] = float(o['cash'][0, i]); d['div'] = S('div')
    d['coll'] = -S('coll')
    d['total'] = sum(d.values()) + float(o['phase0'][0])
    return d


B = milestones('base'); S = milestones('base', True); PE = milestones('pes'); OP = milestones('opt')
for name, X in (('base', B), ('SL', S), ('pes', PE), ('opt', OP)):
    chk = decomp(X['o'], 9)['total']; assert abs(chk - X['m9']) < 50, (name, chk, X['m9'])
    print(name, 'ph0', round(X['ph0']), 'fd', X['fd'], 'm3', round(X['m3']), 'm6', round(X['m6']), 'm9', round(X['m9']),
          'm12', round(X['m12']), 'm18', round(X['m18']), 'm27', round(X['m27']), 'fs', round(X['fs']), 'peak', round(X['peak']), '@', X['peak_m'], 'eq', round(X['eq']))
dB9, dS9, dB27, dS27 = decomp(B['o'], 9), decomp(S['o'], 9), decomp(B['o'], 27), decomp(S['o'], 27)
f = lambda x: f"{x:,.0f}"
k = lambda x: f"{x/1000:,.0f}"
r100 = lambda x: f"{round(x/100)*100:,.0f}"
neg = lambda x: ("−B/." + f(x)) if x > 0.5 else "B/.0"
share9 = (dS9['setup'] + dS9['rs'] + dS9['fij']) / dS9['total']
fixed_m = float(B['o']['fixed'][0, 8])

CAPITAL = f"""## Inversión hasta la primera venta y hasta el pico

Capital = aportes acumulados de los socios, incluida la fase 0 (unos B/.{r100(B['ph0'])} de debida diligencia antes de constituir). El caso de planificación usa las tarifas de SignatureLex para lo legal y los registros y, en todo lo demás, los supuestos del caso base; al lado van el caso base con tarifas de mercado y los extremos pesimista y optimista. La primera venta llega un ciclo de reposición después de los registros: mes {B['fd']} en la base, {PE['fd']} en el pesimista, {OP['fd']} en el optimista. Primera venta no es primer cobro: el Estado paga unos 150 días después de entregar.

| Hito | Mes | Planificación: SignatureLex | Caso base: tarifas de mercado | Pesimista | Optimista |
| --- | --- | --- | --- | --- | --- |
| Fase 0 pagada | 0 | B/.{f(S['ph0'])} | B/.{f(B['ph0'])} | B/.{f(PE['ph0'])} | B/.{f(OP['ph0'])} |
| Empresa, licencia y 3PL contratados | 3 | B/.{f(S['m3'])} | B/.{f(B['m3'])} | B/.{f(PE['m3'])} | B/.{f(OP['m3'])} |
| Registros presentados | 6 | B/.{f(S['m6'])} | B/.{f(B['m6'])} | B/.{f(PE['m6'])} | B/.{f(OP['m6'])} |
| Primera venta | {B['fd']} (pes. {PE['fd']}, opt. {OP['fd']}) | B/.{f(S['fs'])} | B/.{f(B['fs'])} | B/.{f(PE['fs'])} | B/.{f(OP['fs'])} |
| Un año de operación | 12 | B/.{f(S['m12'])} | B/.{f(B['m12'])} | B/.{f(PE['m12'])} | B/.{f(OP['m12'])} |
| Dieciocho meses | 18 | B/.{f(S['m18'])} | B/.{f(B['m18'])} | B/.{f(PE['m18'])} | B/.{f(OP['m18'])} |
| Pico de capital (mes {B['peak_m']} en la base) | {B['peak_m']} | B/.{f(S['m27'])} | B/.{f(B['m27'])} | B/.{f(PE['m27'])} y sigue subiendo si nadie cierra: B/.{f(PE['peak'])} en el mes {PE['peak_m']} | B/.{f(OP['m27'])} |
| Por socio panameño, un sexto (capital 50/50 con Patel), hasta la primera venta / hasta el pico | — | B/.{f(S['fs']/6)} / B/.{f(S['m27']/6)} | B/.{f(B['fs']/6)} / B/.{f(B['m27']/6)} | B/.{f(PE['fs']/6)} / B/.{f(PE['m27']/6)} | B/.{f(OP['fs']/6)} / B/.{f(OP['m27']/6)} |
| Por socio panameño, un tercio (si Patel no aporta efectivo), hasta la primera venta / hasta el pico | — | B/.{f(S['fs']/3)} / B/.{f(S['m27']/3)} | B/.{f(B['fs']/3)} / B/.{f(B['m27']/3)} | B/.{f(PE['fs']/3)} / B/.{f(PE['m27']/3)} | B/.{f(OP['fs']/3)} / B/.{f(OP['m27']/3)} |

El plan de negocio cita B/.{k(B['eq'])} mil de capital en el caso base y B/.{k(S['eq'])} mil con SignatureLex: son los aportes de los 60 meses sin la fase 0; esta tabla la incluye, por eso difiere en unos B/.{r100(B['ph0'])}. Rango para hablar con inversionistas: hasta la primera venta, entre B/.{k(OP['fs'])} mil y B/.{k(PE['fs'])} mil, con B/.{k(S['fs'])} mil como cifra de planificación; hasta el pico del mes 27, entre B/.{k(OP['m27'])} mil y B/.{k(PE['m27'])} mil, con B/.{k(S['m27'])} mil de planificación. En el pesimista el capital no hace pico: si nadie cierra, sigue subiendo hasta B/.{k(PE['peak'])} mil en el mes {PE['peak_m']}; para eso existe la compuerta operativa, que en ese escenario cierra el negocio con una pérdida de unos B/.265 mil.

En qué se va el dinero, acumulado hasta la primera venta (mes 9) y hasta el pico (mes 27):

| Partida | Mes 9, SignatureLex | Mes 9, mercado | Mes 27, SignatureLex | Mes 27, mercado |
| --- | --- | --- | --- | --- |
| Arranque de la empresa: legal, licencia, cumplimiento, registros de proveedor del Estado | B/.{f(dS9['setup'])} | B/.{f(dB9['setup'])} | B/.{f(dS27['setup'])} | B/.{f(dB27['setup'])} |
| Registros sanitarios de los 11 productos | B/.{f(dS9['rs'])} | B/.{f(dB9['rs'])} | B/.{f(dS27['rs'])} | B/.{f(dB27['rs'])} |
| Costos fijos, cargos anuales, posregistro e impuestos | B/.{f(dS9['fij'])} | B/.{f(dB9['fij'])} | B/.{f(dS27['fij'])} | B/.{f(dB27['fij'])} |
| Compras pagadas al proveedor | B/.{f(dS9['pay'])} | B/.{f(dB9['pay'])} | B/.{f(dS27['pay'])} | B/.{f(dB27['pay'])} |
| Costos variables y primas de fianzas | B/.{f(dS9['var'])} | B/.{f(dB9['var'])} | B/.{f(dS27['var'])} | B/.{f(dB27['var'])} |
| Colateral de fianzas inmovilizado en ese mes | B/.{f(dS9['col'])} | B/.{f(dB9['col'])} | B/.{f(dS27['col'])} | B/.{f(dB27['col'])} |
| Caja mínima en ese mes | B/.{f(dS9['cash'])} | B/.{f(dB9['cash'])} | B/.{f(dS27['cash'])} | B/.{f(dB27['cash'])} |
| Dividendos ya repartidos | B/.{f(dS9['div'])} | B/.{f(dB9['div'])} | B/.{f(dS27['div'])} | B/.{f(dB27['div'])} |
| Menos cobros recibidos del Estado | {neg(-dS9['coll'])} | {neg(-dB9['coll'])} | {neg(-dS27['coll'])} | {neg(-dB27['coll'])} |
| Fase 0 | B/.{f(S['ph0'])} | B/.{f(B['ph0'])} | B/.{f(S['ph0'])} | B/.{f(B['ph0'])} |
| Capital acumulado | B/.{f(dS9['total'])} | B/.{f(dB9['total'])} | B/.{f(dS27['total'])} | B/.{f(dB27['total'])} |

Lectura: hasta la primera venta, {share9:.0%} del dinero son arranque, registros y costos fijos, no inventario; por eso el supuesto de costos fijos es el que más mueve el resultado y por eso cada mes de demora en los registros cuesta unos B/.{f(fixed_m)} más. El salto hasta el mes 27 es capital de trabajo: inventario pagado antes de embarcar, cuentas por cobrar a 150 días y el colateral de la fianza de cumplimiento de la segunda licitación de precio único mientras todavía se cobra la primera.
"""

TIMELINE = f"""## Línea de tiempo

Los meses cuentan desde la constitución de la S.A. (mes 0). Los plazos legales salen de la Ley 419 y del Decreto Ejecutivo 27 de 2024; los demás, del caso base del modelo, con el rango pesimista–optimista entre paréntesis. La última columna es el calendario que resulta si la fase 0 termina en noviembre de 2026 y la S.A. se constituye en diciembre; cada mes que se alargue la fase 0 corre todo lo demás un mes.

| Mes | Hito | Qué lo determina | Calendario ilustrativo |
| --- | --- | --- | --- |
| Antes del 0 | Fase 0: hoja de datos y paquete del fabricante, lista de precios, cotizaciones de 3PL, aseguradora de fianzas, regente, contador e IEA, segunda opinión legal; compuerta 0 | Rutul y las cotizaciones; unos B/.{r100(B['ph0'])} entre los tres | Octubre–noviembre de 2026 |
| 0–1 | Pacto de accionistas, S.A., RUC, aviso de operación, cuenta bancaria; contrato de distribución y acuerdo de calidad con el fabricante; contrato con el 3PL | Notaría, DGI y banco (la revisión del banco es más larga con accionista extranjero) | Diciembre de 2026 – enero de 2027 |
| 2–3 | Licencia de operación de la DNFD (hasta 20 días hábiles para subsanar), certificado de buenas prácticas de almacenamiento, regente contratado | DE 27, arts. 382 y 396–398; Resolución 181 de 2025 | Febrero–marzo de 2027 |
| 3–6 (5–9) | Expedientes de los 11 productos: análisis del IEA (hasta 60 días hábiles) y evaluación de la DNFD (hasta 20 días hábiles); registros aprobados | Ley 419, arts. 41 y 74; calidad de los expedientes que mande la fábrica | Abril–junio de 2027 (hasta septiembre de 2027 en el pesimista) |
| 6–8 | Primer pedido, producción, embarque, tránsito y aduana (unos 90 días en total); liberación por el regente | Lote mínimo y vida útil aprobada; flete India–Panamá | Junio–agosto de 2027 |
| {B['fd']} ({OP['fd']}–{PE['fd']}) | Primera venta en compras menores; Registro de Oferentes y PanamaCompra listos | Rampa de participación en compras descentralizadas | Septiembre de 2027 (agosto de 2027 – enero de 2028) |
| 14 | Primer cobro del Estado (unos 150 días desde la entrega: cuenta, Contraloría, pago) | Ciclo de pago de la CSS y del MINSA | Febrero de 2028 |
| 15 (12–27) | Primer contrato centralizado: subasta del MINSA o licitación de precio único de la CSS; fianza de cumplimiento de 30% | La LPU 01-2026 (ofertas en diciembre de 2025, adjudicada entre marzo y mayo de 2026, 15 meses de vigencia) vence en la segunda mitad de 2027; la siguiente debería publicarse por esas fechas | Marzo de 2028 |
| 18 | Capital acumulado de unos B/.{k(B['m18'])} mil en el caso base (B/.{k(S['m18'])} mil con SignatureLex) | Inventario, cuentas por cobrar y colateral de fianzas | Junio de 2028 |
| {B['peak_m']} | Pico de capital: B/.{k(B['m27'])} mil incluida la fase 0, B/.{k(B['eq'])} mil sin ella (B/.{k(S['m27'])} mil con SignatureLex); se afianza la segunda LPU | Fianzas de la segunda licitación mientras se cobra la primera | Marzo de 2029 |
| 36 | Ventas de unos B/.265 mil al año; primeros dividendos, pequeños, al cierre del año 3 | Caso base | Diciembre de 2029 |
| 48–60 | Dividendos del año 4; el capital se recupera solo con el valor terminal del año 5 (múltiplo 1.29x, TIR 6.8% en la base) | Caso base | 2030–2031 |

Si los registros se atrasan hasta septiembre de 2027 (pesimista), la primera venta cae en enero de 2028 y el capital hasta ese momento sube a unos B/.{k(PE['fs'])} mil; además se pierde la ventana de la próxima LPU de la CSS, y el primer contrato centralizado pasa a depender de las subastas del MINSA y de la compra conjunta. Por eso la calidad de los expedientes que mande la fábrica es el riesgo de calendario número uno.
"""

LOGCOST = """## Estimación de costos logísticos mientras no haya cotización firme

Ningún operador logístico de Panamá publica tarifas, así que estas cifras combinan los supuestos del modelo con los pocos precios públicos que sí existen: tarifas FAK de las navieras, cargos portuarios y los honorarios mínimos del corredor de aduana. Sirven para dimensionar y para contestarle a Rutul con un rango; se reemplazan por las cotizaciones en cuanto lleguen.

| Concepto | Estimación | Base |
| --- | --- | --- |
| Almacenamiento y manejo en un 3PL licenciado: 5–10 tarimas, 15–25 °C, control por lote y vencimiento, 2–4 despachos al mes | B/.300–1,200 al mes; el modelo usa B/.600 (cuota mínima) | Supuesto del modelo; ningún 3PL publica tarifas |
| Flete marítimo India–Panamá en carga consolidada (LCL), unos 9 m³ por embarque al inicio | US$200 por m³ de flete más unos US$100 de desconsolidación y destino; el flete puede estar en 250–300 por m³ en 2026 | Desconsolidación US$86.5 por m³ (tarifario de Crowley); las tarifas FAK de CMA CGM subieron 44% entre febrero y junio de 2026 |
| Flete en contenedor de 20 pies (madurez: unos 19 m³ por embarque, 4 al año) | US$3,750 de flete (FAK de junio de 2026) más unos US$700 de cargos locales (THC US$275 en Manzanillo, documentación, acarreo): US$180–220 por m³ | CMA CGM, Maersk, Crowley |
| Corredor de aduana | B/.50 + 0.15% del valor CIF + B/.2 por línea; unos B/.200–400 por embarque de 11 productos | Ley 20 de 1994, honorarios mínimos |
| Autorización de importación de la DNFD por embarque | Sin tasa para no controlados; hasta 3 días hábiles | DE 27, art. 364 |
| Seguro de carga | 0.3–0.5% del valor CIF; el modelo usa B/.100 al mes | Mercado |
| Entregas a los almacenes de la CSS y del MINSA | 4% de las ventas en el modelo; varios 3PL lo incluyen con flota propia | Supuesto del modelo |
| Primer embarque de 5 tarimas puesto en bodega, sin contar la mercancía | Unos US$2,700–3,500: flete y destino 1,800–2,700, corredor y acarreo 300–500, seguro según valor | Suma de las líneas anteriores |

Comparación con una bodega propia, sin contar el regente que ambas necesitan: con 5 tarimas, un 3PL cuesta unos B/.680 al mes contra B/.4,030 más B/.37 mil de inversión en bodega propia; con 15 tarimas, B/.960 contra B/.5,920 más B/.54 mil. A este volumen la bodega propia no tiene sentido.

Lo que sí se puede decir a Rutul con estas bases: que un depósito farmacéutico licenciado para 5–10 tarimas cuesta del orden de B/.300–1,200 al mes con manejo, que el flete consolidado India–Panamá sale en unos US$300 por m³ puesto en bodega (o un contenedor de 20 pies en unos US$4,500 con cargos locales) y que el corredor cobra unos cientos por embarque. Y que son estimaciones de escritorio, no cotizaciones.
"""

FACTORY = """## La hoja de datos de fábrica y el cuestionario del 3PL

Los operadores logísticos cotizan por posición de tarima, por manejo y por servicios; la naviera y el consolidador por metro cúbico y peso; la aseguradora por valor CIF. Ninguno cotiza sobre estimaciones. El cuestionario que mandó el 3PL (3PL_questionnaire_blank_EN.xlsx, versión en inglés y en blanco) pide pesos, dimensiones, volumen, valor por embarque, sensibilidad, control por lote, fichas técnicas y fotos: casi todo depende de la fábrica. Por eso la hoja Factory_data_for_3PL_quote.xlsx pide, por producto: unidades por empaque, empaques por caja máster, dimensiones y peso de la caja, cajas por tarima, condiciones de almacenamiento, vida útil aprobada y mínima garantizada al embarcar, código arancelario, planta, tamaño de lote, lote mínimo, tiempo de entrega, precio FOB, y si hay CPP, hoja de seguridad y fotos; y, por embarque: incoterm, puerto, tipo de tarima, valor, documentos que viajan con la carga y si pueden imprimir el número de licitación en el empaque. Con esa hoja llena se cotiza a tres operadores a la vez (correos listos más abajo)."""

MAPA = """## Cómo leer este paquete

| Archivo | Qué contiene | Léalo para |
| --- | --- | --- |
| 00_Resumen_y_plan.md (este) | Veredicto, números que valen, línea de tiempo, plan por fases, posición de trabajo, pendientes, glosario | Entender el negocio en 15 minutos |
| 01_Investigacion_Rutul_y_fabricante.md | Debida diligencia sobre Rutul Patel, Zywie, el fabricante identificado y sus empresas; qué pedirle | Saber con quién estamos tratando |
| 02_Mercado_requisitos_y_competencia.md | Cómo compra el Estado, precios adjudicados frente a costo, competencia, ruta regulatoria y legal, canal privado | Saber dónde está el dinero y qué exige la ley |
| 03_Costos_capital_y_proyeccion.md | Costos de arranque (mercado y SignatureLex), costos fijos, inversión hasta la primera venta y hasta el pico, proyección, riesgo simulado, supuestos | Saber cuánto hay que poner y cuánto puede volver |
| 04_Logistica_y_operacion.md | Cómo funciona la operación, vida útil y bodega, cómo trabaja un 3PL y con quién cotizar, estimación logística, correos de cotización listos | Cerrar las cotizaciones |
| 05_Trato_socios_y_hoja_de_ruta.md | Estructura del trato con Patel, capital por socio, roles, pasos de constitución, contratos, honorarios legales, herramientas | Decidir cómo nos organizamos |
| 06_Guion_conversacion_Rutul.md | Mensajes en inglés por etapas, respuestas a objeciones, qué no decir, señales, tabla de seguimiento | Hablar con Rutul |
| Modelo_financiero_socios.xlsx | El modelo de 60 meses con fórmulas vivas: supuestos, escenarios, simulación, sensibilidad, trato, capital por socio, operación | Cambiar un supuesto y ver el efecto |
| Factory_data_for_3PL_quote.xlsx y 3PL_questionnaire_blank_EN.xlsx | Lo único que va a Rutul: la hoja de datos que debe llenar la fábrica y el cuestionario del 3PL en blanco | Reenviar |
| Anexo_Plan_de_negocio_completo.md | El plan de negocio en una sola pieza, del que salen los documentos 00 a 05 | Consultar todo junto |
| Anexo_DD_hallazgos_en.md | Hallazgos de la primera ronda de debida diligencia, en inglés, con cada enlace | Verificar fuente por fuente |

Regla de uso: los documentos 00 a 06 y el modelo son para los tres socios panameños. A Rutul solo van la hoja de datos, el cuestionario del 3PL y, más adelante, el acuerdo de confidencialidad y la propuesta de términos. Nada de la investigación se le reenvía ni se le cita: se le piden los documentos y se contrastan en privado."""

COMPARTIR = """## Qué se comparte y con quién

- Socios panameños: todo este paquete, incluida la debida diligencia sobre el fabricante.
- Rutul y la fábrica: la hoja de datos, el cuestionario del 3PL, el acuerdo de confidencialidad, las solicitudes de cotización que él deba reenviar y, después de los precios, la propuesta de términos de una página. Nunca el plan, el modelo, los números internos ni lo investigado.
- Proveedores (3PL, aseguradoras, IEA, regente, contador): solo la solicitud de cotización correspondiente, con la hoja de datos llena.
- Antes de compartir un documento con una audiencia nueva se prepara la versión para esa audiencia; lo que un socio dijo en privado no se traslada a los documentos compartidos."""

POSICION = """## Posición de trabajo propuesta, para discutir entre los tres

| Fecha | Posición |
| --- | --- |
| 6 de octubre de 2026 | No entrar en la S.A. tal como la propone Patel; pagar solo la fase 0; el negocio gana por precio y cumplimiento, sin contactos |
| 7 de octubre de 2026 | Primera ola: los 11 productos sin equivalencia terapéutica; a Rutul se le pide como socios, sin revelar lo investigado; la propuesta de términos la escribimos nosotros; los documentos van a los socios panameños, no a Rutul |
| Abierto | Quién opera a diario (el coordinador sin sueldo es la palanca que más mejora el resultado); cómo se pagan los honorarios legales (ver 05); tope de capital de cada socio |"""

PENDIENTES = """## Pendientes de investigación y de cotización

Lo que todavía no está verificado o cotizado, en orden de impacto en el resultado:

- [ ] Precio de fábrica de los 11 productos, lote mínimo, vida útil aprobada y crédito (lo pide el guion; sin esto no hay compuerta 0).
- [ ] Cotizaciones firmes: tres 3PL (con la hoja de datos llena), dos aseguradoras de fianzas (colateral y prima), regente, contador y análisis del IEA por producto. Los costos fijos son el supuesto que más mueve el resultado.
- [ ] Segunda cotización legal de un bufete independiente con el mismo alcance que la propuesta de SignatureLex, y opinión escrita sobre el parentesco con el ministro de Salud.
- [ ] Quiénes son los accionistas de Bueno Salud Care y de Zywie; estados financieros auditados del año fiscal 2025.
- [ ] Prueba de la experiencia declarada en El Salvador y Colombia (números de registro, distribuidor); hoy no aparece en ningún registro público revisado.
- [ ] Explicación escrita de las dos alertas de calidad de 2024 (ceftriaxona y amoxicilina), con causa y acción correctiva.
- [ ] Licencias de fabricación de la FDCA de Gujarat por bloque y planta de fabricación de cada producto (Sanand o Roorkee).
- [ ] Si la fábrica tiene registros vigentes en Panamá o aprobaciones en países de referencia de la OMS (abrirían la ruta rápida).
- [ ] Pliego de la compra conjunta MINSA-CSS del Decreto 16 de 2026 y fecha de la próxima LPU de la CSS.
- [ ] Comparación detallada de los siete operadores logísticos (servicios, zonas, requisitos de alta) y validación del flete con un transitario.
- [ ] Tarifa real del IEA y patrones de referencia que debe aportar el solicitante.
- [ ] Fabricante, licencias y certificados de los productos del sistema nervioso de la segunda ola.
- [ ] Canal privado de farmacias: solo si se decide explorarlo; hoy el modelo no lo incluye."""

METODO = """## Método y fuentes

Todo lo que sigue sale de registros públicos consultados entre el 5 y el 7 de octubre de 2026: el registro mercantil de la India a través de espejos públicos (Falconebiz, Zauba Corp, Tofler, The Company Check), las listas de alertas de calidad y de plantas con certificado OMS-BPM de la autoridad india (CDSCO), los registros sanitarios públicos de El Salvador, Ecuador, Colombia, Paraguay, Filipinas, Tanzania, Sri Lanka, Ghana y Nigeria, los portales de compras públicas de Panamá y El Salvador, y los sitios y folletos de las propias empresas. No se contactó a nadie ni se usó información privada. Lo que no se pudo verificar se dice así.

Rutul Patel no ha nombrado al fabricante. El nombre Bueno Salud Care (India) Pvt Ltd surge de que la lista de productos que él compartió coincide en 97% con la lista pública de Bueno, con los mismos errores de escritura, y de que una directora de Bueno desde 2024 se llama Deepti Rutul Patel. Es una inferencia sólida, pero inferencia: por eso el guion le pide a Rutul que nombre al fabricante legal (el que firma el CPP y la licencia) y no se le menciona Bueno hasta que él lo haga. Las fechas de nombramiento de los directores de Bueno difieren entre los espejos del registro mercantil (marzo, julio o septiembre de 2024); todas caen en 2024, cuando cambió la junta."""

DICHO = """## Lo que Rutul ha dicho frente a lo que se encontró

| Lo que ha dicho o dado a entender | Lo que muestran los registros públicos | Lectura |
| --- | --- | --- |
| Tiene una fábrica aliada que produce la lista de 230 productos (nunca la ha nombrado) | La lista coincide en 97% con la de Bueno Salud Care (Sanand, Gujarat), planta real con certificado OMS-BPM vigente hasta enero de 2029; Patel no es director de Bueno, pero sí lo son Deepti Rutul Patel desde 2024 y su socio Abhinav Bhargava | Hay fábrica y es seria en papel; falta que la nombre y que firme como fabricante |
| Zywie es un exportador farmacéutico con experiencia | Zywie es una sociedad de personas de 2018 registrada en Vapi; en su perfil comercial se anuncia como vendedora de arroz basmati y vegetales congelados y, desde 2026, de tabletas farmacéuticas; sin licencia mayorista de medicamentos localizada | Intermediario comercial, no fabricante ni distribuidor farmacéutico establecido |
| La fábrica vende y participa en licitaciones en El Salvador y Colombia | Cero registros sanitarios y cero adjudicaciones a nombre de Bueno, Zywie, Nosher, Modi, Patel o Bhargava en El Salvador (2,149 registros y 5,819 líneas revisadas); tampoco aparece como fabricante en INVIMA ni en los registros de Ecuador, Paraguay, Tanzania, Sri Lanka, Ghana o Nigeria; sí tiene unos 39 registros en Filipinas | La experiencia latinoamericana declarada no se pudo verificar; la asiática sí |
| Zywie pondría el capital de arranque (primera versión); después preguntó cuánto pondría el lado panameño; la última versión es 50/50 | No es verificable por registros; Bueno cerró el año fiscal 2025 con pérdida neta y deuda garantizada del orden de sus ventas | La posición de capital hay que fijarla por escrito (paso 9 del guion) antes de constituir nada |
| Calidad de exportación | Dos lotes de Bueno fallaron pruebas oficiales en marzo de 2024 (ceftriaxona 1 g, uno de nuestros 11 productos, y amoxicilina dispersable); ninguna alerta nueva desde entonces | Se pide el informe de causa y corrección sin citar la fuente; si lo entrega por iniciativa propia es buena señal |

Nada de esta tabla se le dice a Rutul. Se le piden los documentos que cualquier distribuidor pide (ver la sección siguiente) y se contrasta en privado."""

# ---------- 06 guion: casual opening with the estimate bubble ----------
OPEN_BODY = """Cinco burbujas, en inglés, seguidas, en el grupo. Adjuntos: en la segunda, el cuestionario en blanco del 3PL (3PL_questionnaire_blank_EN.xlsx) para que vea qué piden; en la tercera, la hoja de datos de fábrica (Factory_data_for_3PL_quote.xlsx). Tono casual pero profesional; sin nombres de operadores ni cifras internas; nada que suene a redacción automática. Solo dos pedidos esta noche: la hoja de datos y el paquete del proveedor.

Burbuja 1:

```text
Hi Rutul, sorry for going quiet on our side. We wanted to come back with the cost side mapped like we said, and it took longer than planned.
```

Burbuja 2 (con el cuestionario del 3PL en blanco):

```text
Quick update: legal, registration and tax costs are mapped. The warehouse quote is the piece we couldn't close. The logistics companies here won't price anything without factory data: carton sizes and weights, units per carton, pallet configuration, storage conditions, HS codes, product sheets, shipment value. We gave them estimates and that didn't fly. Attaching the form one of them sent us so you can see what they ask for.
```

Burbuja 3 (con la hoja de datos):

```text
To fix it, I put together a simple sheet with the fields only the factory can fill (attached). If their export team can complete it, or just send the standard export packing list and product data sheets, we go back to the logistics companies with a complete file and get real numbers.
```

Burbuja 4 (opcional; úsela si pregunta cuánto cuesta o si quiere adelantarle el orden de magnitud):

```text
We don't have a real quote yet, but from what we've mapped so far: licensed pharma storage for a 5-10 pallet operation runs roughly B/.300-1,200 a month with handling, sea freight India-Panama is about US$300 per cubic metre door to warehouse for consolidated cargo (a 20' box is around US$3,750 ocean plus local charges), and the customs broker is a few hundred per shipment. Desk estimates, not quotes; real numbers once the factory data is in.
```

Burbuja 5:

```text
And since we're partners in this: could you share the usual regulatory and commercial package you give your distributors (El Salvador, Colombia)? CPP per product, WHO-GMP certificate and manufacturing licence, factory price list with MOQ and shelf life, and a sample of what ships with the goods (CoA, packing list, invoice). With that we can lock the first products and put a proper next-steps list on the table for both sides.
```

Lo que hace: explica el retraso sin excusas, convierte la falla del 3PL en el primer pedido con una razón que no es nuestra, y la última burbuja lo mide: un exportador con la experiencia que dice tener manda ese paquete en un día, y cada documento lleva el nombre del fabricante, así que él mismo nos lo dice. Si pregunta por capital o porcentajes, la respuesta de las reglas: la propuesta de términos viene después de la lista de precios. Si contesta con generalidades, un solo recordatorio: «even the packing list of your last export shipment works, the logistics people only need the format»."""
_i = OPEN_BODY.index(BUBBLE4_OLD_START); _j = OPEN_BODY.index('Burbuja 5:')
OPEN_BODY = OPEN_BODY[:_i] + BUBBLE4_V2 + '\n' + OPEN_BODY[_j:]
G['Mensaje de apertura'] = OPEN_BODY
guion_intro = Ghead.split('\n', 1)[1].strip()
guion_md = '# Conversación con Rutul: guion por etapas\n\n' + HEADER + guion_intro + '\n\n'
for t in Gorder:
    guion_md += f'## {t}\n\n{G[t]}\n\n'
guion_md = guion_md.rstrip('\n') + '\n'

# ---------- hoja de ruta tweaks ----------
hoja_roles = H['Roles de los socios'] \
    .replace('Trabajo legal valorado como aporte en especie; capital menor', 'Gestión legal a través de su firma (los documentos los firma un abogado idóneo de la firma), valorada como aporte en especie; capital menor') \
    .replace('| Constitución, licencias, contratos, KYC, precios de transferencia |', '| Coordina con la firma la constitución, las licencias, los contratos, el KYC y los precios de transferencia |')
hoja_tools = H['Herramientas y orden'] \
    .replace('- Este proyecto de Claude guarda la bitácora, el plan de negocio, el guion de la conversación y esta hoja; cada sesión actualiza la bitácora.',
             '- Los documentos de trabajo son archivos Markdown y Excel (este paquete) en la carpeta compartida; se actualizan y se vuelven a entregar cuando cambian, con fecha en el encabezado.') \
    .replace('- Repositorio privado en GitHub para el código del modelo: Jaime crea el repositorio vacío y Claude sube el código.', '- Repositorio privado en GitHub solo para el código del modelo; los socios no lo necesitan.')

HONORARIOS = """## Honorarios legales: cómo decidirlo entre los tres

La propuesta de SignatureLex cubre todo el arranque (constitución, cuenta bancaria, licencia, 3PL, cumplimiento, registros de proveedor del Estado) y los registros sanitarios; está completa y es el único presupuesto legal escrito que tenemos. La pregunta no es la calidad del trabajo sino cómo se paga, porque la firma del socio le cobraría a la empresa del socio y porque la diferencia frente a tarifas de mercado sube el capital del caso base en unos B/.39 mil (ver 03).

| Opción | Cómo funciona | A favor | En contra |
| --- | --- | --- | --- |
| A. SignatureLex con las tarifas propuestas, pagadas en efectivo | B/.24,750 de arranque más B/.3,425 por registro | Un solo responsable; Francisco coordina desde adentro | Es la opción más cara en capital; el conflicto de interés exige que los otros dos socios aprueben cada factura |
| B. SignatureLex a tarifas de mercado, y la diferencia como aporte en especie de Francisco | La S.A. paga unos B/.10,850 más B/.2,120 por registro; lo que la firma cobre por encima se reconoce como capital aportado por Francisco, con un tope pactado | Mantiene a Francisco dentro, alinea incentivos (cobra en acciones lo que la empresa no puede pagar en efectivo) y baja el capital que ponen los tres | Hay que valorar el aporte en especie con una segunda cotización y la firma tiene que aceptar cobrar menos ahora |
| C. Bufete independiente para la S.A. y el pacto; Francisco coordina y revisa | Se contrata al que gane la segunda cotización; Francisco aporta tiempo y seguimiento | Elimina el conflicto de interés en el pacto de accionistas, que es donde más importa | Pierde el conocimiento que ya tiene la firma del caso; Francisco aporta menos en especie |

Recomendación: pedir la segunda cotización con el mismo alcance (está en la fase 0), y con ella decidir entre B y C. En cualquier opción, el pacto de accionistas lo redacta o revisa un abogado que no sea socio, y los honorarios de partes relacionadas los aprueban los demás socios: son las reglas del plan, no una desconfianza hacia nadie."""


def doc(title, intro, blocks, fuentes_md):
    md = f'# {title}\n\n' + HEADER + (intro.strip() + '\n\n' if intro else '')
    for b in blocks:
        md += b.rstrip('\n') + '\n\n'
    md += fuentes_md
    return md


def sec(d, name, new_title=None):
    return f'## {new_title or name}\n\n' + d[name]


# ---------- audit overrides (8 Oct) ----------
LOGCOST = LOGCOST_V2
assert METODO_OLD in METODO; METODO = METODO.replace(METODO_OLD, METODO_NEW)
assert DICHO_OLD in DICHO; DICHO = DICHO.replace(DICHO_OLD, DICHO_NEW)
assert PENDIENTES_OLD in PENDIENTES; PENDIENTES = PENDIENTES.replace(PENDIENTES_OLD, PENDIENTES_NEW)
assert MAPA_OLD in MAPA; MAPA = MAPA.replace(MAPA_OLD, MAPA_NEW)
H['Cotizar el 3PL: con quién y cómo'] = H['Cotizar el 3PL: con quién y cómo'].rstrip() + HOJA_RFQ_NOTE
HEADER0 = HEADER
HEADER = HEADER.replace('Preparado el 7 de octubre de 2026', 'Preparado el 7 de octubre de 2026 y revisado el 8 de octubre de 2026 tras una auditoría independiente (ver 07_Auditoria_y_confianza.md)')
guion_md = guion_md.replace(HEADER0, HEADER, 1)   # 06 lleva el mismo encabezado revisado

# ---------- 00 ----------
doc00 = doc('Distribuidora de medicamentos en Panamá: resumen, plan y guía de lectura', '', [
    MAPA,
    sec(P, 'Veredicto'),
    '## Los números que valen\n\n' + C['Los números que valen'].replace('B/.255 mil en el mes 27 (B/.297 mil con SignatureLex)', 'B/.258 mil en el mes 27 incluida la fase 0, B/.255 mil sin ella (B/.297 mil con SignatureLex)'),
    TIMELINE,
    sec(P, 'Plan de ejecución', 'Plan por fases y compuertas'),
    POSICION,
    PENDIENTES,
    COMPARTIR,
    sec(C, 'Glosario'),
], '## Fuentes\n\nCada documento del paquete trae sus fuentes al final; las de la debida diligencia están enlazadas en las tablas del documento 01 y en el anexo en inglés.\n')

# ---------- 01 ----------
dd_extra = ('Debida diligencia\n\n- Los enlaces de cada hallazgo están en la columna Fuente de la tabla; el anexo en inglés (Anexo_DD_hallazgos_en.md) trae la lista completa de páginas abiertas, con fecha.\n'
            '- Registros consultados: [CDSCO, alertas de calidad](https://cdsco.gov.in/opencms/opencms/en/Notifications/Alerts/) · [CDSCO, portal de lotes no conformes](https://cdscoonline.gov.in/CDSCO/viewPublicNSQDrug) · [FDA Filipinas](https://verification.fda.gov.ph/) · [DNM El Salvador](https://expedientes.medicamentos.gob.sv/productos/buscarProducto) · [COMPRASAL](https://www.comprasal.gob.sv/procesos-publicos) · [Falconebiz (MCA)](https://www.falconebiz.com/) · [Zauba Corp](https://www.zaubacorp.com/) · [Tofler](https://www.tofler.in/) · [The Company Check](https://www.thecompanycheck.com/) · [IndiaMART, Zywie Worldwide](https://www.indiamart.com/zywie-worldwide/) · [Bueno Salud Care](https://buenosalud.in/)')
doc01 = doc('Investigación sobre Rutul Patel, Zywie y el fabricante', '', [
    METODO,
    IDENTIDAD,
    sec(P, 'Debida diligencia del socio', 'Hallazgos'),
    DICHO,
    sec(G, 'Lo que un fabricante exportador manda sin que se lo pidan dos veces'),
], '## Fuentes\n\n' + dd_extra + '\n')

# ---------- 02 ----------
doc02 = doc('Mercado, requisitos y competencia', '', [
    sec(P, 'Modelo de negocio'),
    sec(P, 'Mercado'),
    CANALES,
    sec(P, 'Precios adjudicados frente al costo puesto en Panamá'),
    sec(P, 'Competencia y probabilidad de ganar'),
    sec(P, 'Ruta regulatoria y legal'),
], fuentes('Compras públicas', 'Normas', 'Mercado y pagos'))

# ---------- 03 ----------
doc03 = doc('Costos, capital y proyección de ganancias', '', [
    sec(P, 'Estructura de costos'),
    CAPITAL,
    sec(P, 'Capital de trabajo y financiamiento'),
    sec(P, 'Proyección financiera'),
    sec(P, 'Riesgo cuantificado'),
    sec(P, 'Supuestos del modelo y preguntas abiertas'),
], fuentes('Normas', 'Mercado y pagos', 'Costos y logística'))

# ---------- 04 ----------
doc04 = doc('Logística y operación', '', [
    sec(P, 'Operación'),
    sec(H, 'Cuánto tiempo puede estar el producto en bodega'),
    sec(H, 'Cotizar el 3PL: con quién y cómo'),
    FACTORY,
    LOGCOST,
    sec(H, 'Correos de cotización listos para enviar'),
], fuentes('Costos y logística', 'Compras públicas'))

# ---------- 05 ----------
doc05 = doc('Estructura del trato, socios y hoja de ruta', '', [
    sec(P, 'Estructura del trato con Patel'),
    sec(P, 'Capital por socio'),
    '## Roles de los socios\n\n' + hoja_roles,
    sec(H, 'Antes de constituir (fase 0, unos B/.2,700 entre los tres)'),
    sec(H, 'Constituir y licenciar (fase 1, solo tras la compuerta 0)'),
    sec(H, 'Contratos que hacen falta'),
    HONORARIOS,
    '## Herramientas y orden\n\n' + hoja_tools,
], fuentes('Normas'))

# ---------- annex: full plan ----------
anexo_plan = plan.replace('# Plan de negocio: distribuidora de medicamentos para compras públicas en Panamá\n',
                          '# Plan de negocio: distribuidora de medicamentos para compras públicas en Panamá\n\n' + HEADER.rstrip('\n') + '\n', 1)

files = {
    '00_Resumen_y_plan.md': doc00,
    '01_Investigacion_Rutul_y_fabricante.md': doc01,
    '02_Mercado_requisitos_y_competencia.md': doc02,
    '03_Costos_capital_y_proyeccion.md': doc03,
    '04_Logistica_y_operacion.md': doc04,
    '05_Trato_socios_y_hoja_de_ruta.md': doc05,
    '06_Guion_conversacion_Rutul.md': guion_md,
    '07_Auditoria_y_confianza.md': doc07(HEADER).replace('## Fuentes de esta auditoría', VERIF_PRECIOS + '\n## Fuentes de esta auditoría').replace('- Las demás fuentes de la capa 1', VERIF_FUENTES + '- Las demás fuentes de la capa 1'),
    'Anexo_Plan_de_negocio_completo.md': anexo_plan,
}
from audit_edits2 import apply_post, LEAME
files['LEAME.md'] = LEAME
for name, md in files.items():
    md = apply_post(name, md)          # tercera pasada de auditoría (8 de octubre, noche)
    md = re.sub(r'\n{3,}', '\n\n', md)
    files[name] = md
    open(os.path.join(OUT, name), 'w', encoding='utf-8').write(md)
    print(f'{name}: {len(md.encode()):,} bytes, {md.count(chr(10))} lines')

# ---------- checks ----------
msgs = re.findall(r'```text(.*?)```', guion_md, flags=re.S)
bad = [m for m in msgs if 'Bueno' in m or 'Sanand' in m or 'Salud Care' in m]
assert not bad, 'a message names the manufacturer'
allmd = '\n'.join(files.values())
for word in ('100,000', 'ahorros de B/.', 'otra oportunidad'):
    assert word not in allmd, word
print('checks ok: messages clean, no private figures')

# ---------- annex: English DD findings ----------
_dd = open(os.path.join(HERE, '..', 'research', 'b6_partner', 'notes', '01_findings_summary.md'), encoding='utf-8').read()
_dd = _dd.replace('Raw log with every URL: notes/00_log.md. Downloads under downloads/ (untrusted).', 'Raw log with every URL: research/b6_partner/notes/00_log.md in the code repository (Meds); downloads are kept there as untrusted data.')
open(os.path.join(OUT, 'Anexo_DD_hallazgos_en.md'), 'w', encoding='utf-8').write(_dd)

# ---------- blank 3PL questionnaire (English tab only) ----------
from openpyxl import load_workbook
wb = load_workbook(os.path.join(XIN, 'Cuestionario_operativo_5_tarimas_revisado.xlsx') if os.path.exists(os.path.join(XIN, 'Cuestionario_operativo_5_tarimas_revisado.xlsx')) else os.path.join(UD, 'Cuestionario_operativo_5_tarimas_revisado.xlsx'))
for s in list(wb.sheetnames):
    if 'Ingl' not in s:
        del wb[s]
wb.active = 0
wb.save(os.path.join(XLSX_OUT, '3PL_questionnaire_blank_EN.xlsx'))
shutil.copy(os.path.join(XIN, 'Factory_data_for_3PL_quote.xlsx') if os.path.exists(os.path.join(XIN, 'Factory_data_for_3PL_quote.xlsx')) else os.path.join(UD, 'Factory_data_for_3PL_quote.xlsx'), os.path.join(XLSX_OUT, 'Factory_data_for_3PL_quote.xlsx'))

# ---------- partner version of the Excel model ----------
if os.path.exists(PERSONAL_XLSX):
    wb = load_workbook(PERSONAL_XLSX)
    rep = {
        ('Supuestos', 'B65'): 'Fracción de un socio dentro del 50% panameño',
        ('Valoración', 'B36'): 'Vista de un socio (participación y aportes según el trato)',
        ('Valoración', 'B37'): 'Participación del socio en las utilidades',
        ('Valoración', 'B38'): 'Porcentaje del capital que aporta el socio',
        ('Valoración', 'B39'): 'Capital total que pondría el socio (incluye su tercio de la fase 0)',
        ('Valoración', 'B40'): 'Lo que recibiría el socio (dividendos y valor terminal netos, conservador)',
        ('Valoración', 'B41'): 'Resultado neto del socio en 5 años (sin descontar)',
        ('Valoración', 'B42'): 'Capital del socio como % de sus ahorros líquidos (celda C17 de la hoja Capital por socio)',
        ('Monte Carlo', 'B23'): 'Lo que arriesga un socio (1/3 de la fase 0; 1/6 del capital posterior y de las utilidades en la S.A.; 1/3 en la opción de registros)',
        ('Capital personal', 'B1'): 'Cuánto capital tiene sentido que arriesgue cada socio',
        ('Capital personal', 'B2'): 'Criterio de Kelly sobre la distribución simulada (20,000 escenarios) con un patrimonio líquido de referencia de B/.100,000: monto esperado que maximiza el crecimiento del patrimonio. Si el trato se detiene en la fase 0, cada socio solo pierde su parte de esa fase.',
        ('Capital personal', 'C4'): 'Capital promedio por socio (un tercio del lado panameño) si el trato sigue',
        ('Capital personal', 'B12'): 'Registros propios + distribuidor (un tercio por socio)',
        ('Capital personal', 'B17'): 'Ahorros líquidos del socio (B/.): ejemplo, cambie este valor',
        ('Capital personal', 'C17'): 60000,
        ('Capital personal', 'B18'): 'Reserva para otros compromisos (B/.): ejemplo, cambie este valor',
        ('Capital personal', 'C18'): 10000,
    }
    for (sh, cell), val in rep.items():
        wb[sh][cell].value = val
    wb['Valoración']['C42'].value = "=C39/'Capital por socio'!C17"
    wb['Capital personal'].title = 'Capital por socio'
    for s in wb:
        for row in s.iter_rows():
            for c in row:
                if isinstance(c.value, str) and 'Capital personal' in c.value:
                    c.value = c.value.replace('Capital personal', 'Capital por socio')
    xl = os.path.join(XLSX_OUT, 'Modelo_financiero_socios.xlsx')
    wb.save(xl)
    print('partner excel saved')
else:
    print('personal model xlsx not found; partner excel left unchanged (set PERSONAL_MODEL_XLSX)')
print(sorted(os.listdir(OUT)))
