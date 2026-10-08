# -*- coding: utf-8 -*-
"""Tercera pasada de auditoría (8 de octubre de 2026, noche), aplicada por build_docs.py a cada
documento ya ensamblado. Cada reemplazo lleva su anclaje exacto y falla si el texto cambió.

Qué corrige: índice único del paquete (LEAME y 00), marcadores de gráficos sin gráfico, párrafos
duplicados entre documentos, tabla de operadores logísticos con licencias y estado, correos de
cotización enviados, estructura real de la carpeta de Drive, celdas vacías, encabezados, y las
secciones nuevas sobre la DNFD (quién decide y cuánto tarda) y la verificación de la noche en 07.
"""
import json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
FECHA = '8 de octubre de 2026'

# ---------------------------------------------------------------- índice único del paquete
DOC_INDEX = [
    ('LEAME.md', 'Esta guía: qué es cada archivo, en qué orden leerlo según su papel, dónde vive cada cosa y qué cambió en cada versión', 'Empezar'),
    ('00_Resumen_y_plan.md', 'Veredicto, números que valen, línea de tiempo, plan por fases y compuertas, posición de trabajo, pendientes, glosario', 'Entender el negocio en 15 minutos'),
    ('01_Investigacion_Rutul_y_fabricante.md', 'Debida diligencia sobre Rutul Patel, Zywie y el fabricante identificado; qué pedirle y qué ha dicho frente a lo encontrado', 'Saber con quién estamos tratando'),
    ('02_Mercado_requisitos_y_competencia.md', 'Cómo compra el Estado, canales de venta, precios adjudicados frente a costo, competencia, ruta regulatoria y legal, quién decide y cuánto tarda la DNFD', 'Saber dónde está el dinero y qué exige la ley'),
    ('03_Costos_capital_y_proyeccion.md', 'Costos de arranque (mercado y SignatureLex), costos fijos, inversión por hito y por socio, proyección, sensibilidad, riesgo simulado, supuestos', 'Saber cuánto hay que poner y cuánto puede volver'),
    ('04_Logistica_y_operacion.md', 'Operación, vida útil y bodega, operadores logísticos con licencia y estado de las cotizaciones, estimación logística, correos enviados', 'Cerrar las cotizaciones'),
    ('05_Trato_socios_y_hoja_de_ruta.md', 'Estructura del trato con Patel, capital por socio, roles, pasos de constitución, contratos, honorarios legales, herramientas', 'Decidir cómo nos organizamos'),
    ('06_Guion_conversacion_Rutul.md', 'Mensajes en inglés por etapas, respuestas a objeciones, qué no decir, señales, tabla de seguimiento', 'Hablar con Rutul'),
    ('07_Auditoria_y_confianza.md', 'Cifra por cifra: fuente, verificación, confianza y cómo argumentarla; cómo leer el 77%; brechas y verificaciones posteriores', 'Defender los números ante socios e inversionistas'),
    ('Cotizaciones_3PL_seguimiento.md', 'Operadores logísticos: canal de contacto, evidencia de licencia, qué se pidió, cuándo, y qué respondieron', 'Seguir las cotizaciones'),
    ('Resumen_ejecutivo_socios_inversionistas.md', 'Cuatro páginas para un socio o inversionista: qué es el negocio, veredicto, números, el 77% y cómo baja, tramos de capital, riesgos', 'Presentar el negocio'),
    ('Modelo_financiero_socios.xlsx', 'El modelo de 60 meses con fórmulas vivas: supuestos, escenarios, simulación, sensibilidad, trato, capital por socio, operación', 'Cambiar un supuesto y ver el efecto'),
    ('Factory_data_for_3PL_quote.xlsx y 3PL_questionnaire_blank_EN.xlsx', 'Lo único que va a Rutul: la hoja de datos que debe llenar la fábrica y el cuestionario del 3PL en blanco', 'Reenviar'),
    ('Anexo_Plan_de_negocio_completo.md', 'El plan de negocio en una sola pieza, del que salen los documentos 00 a 05; repite su contenido, por eso vive solo en el repositorio y en el proyecto de Claude, no en Drive', 'Consultar todo junto'),
    ('Anexo_DD_hallazgos_en.md', 'Hallazgos de la primera ronda de debida diligencia, en inglés, con cada enlace', 'Verificar fuente por fuente'),
]


def mapa_table(current=None):
    rows = ['| Archivo | Qué contiene | Léalo para |', '| --- | --- | --- |']
    for name, what, why in DOC_INDEX:
        label = name + (' (este)' if name == current else '')
        rows.append(f'| {label} | {what} | {why} |')
    return '\n'.join(rows)


REGLA_USO = ('Regla de uso: los documentos 00 a 07, el seguimiento de cotizaciones y el modelo son para los tres socios panameños. '
             'A Rutul solo van la hoja de datos, el cuestionario del 3PL y, más adelante, el acuerdo de confidencialidad y la propuesta de términos. '
             'Nada de la investigación se le reenvía ni se le cita: se le piden los documentos y se contrastan en privado.')

# ---------------------------------------------------------------- 00: plan por fases en tabla
FASES = """| Fase | Qué se hace | Capital acumulado (caso base / con SignatureLex) | Termina en |
| --- | --- | --- | --- |
| 0. Verificar (ahora) | Hoja de datos y paquete del fabricante, lista de precios, cotizaciones (3PL, fianzas, regente, contador, IEA), segunda opinión legal, acuerdo de confidencialidad | Unos B/.2,700 entre los tres socios panameños | Compuerta 0: precio hasta 1.1 veces la referencia FOB, 150 días de crédito, registros pagados por Bueno, planta y fabricante del sistema nervioso verificados |
| 1. Constituir y registrar (meses 0–6) | Pacto de accionistas, S.A., cuenta bancaria, licencia de la DNFD, contrato con el 3PL, 11 registros sanitarios | B/.70 mil / B/.100 mil | Compuerta 1: 8 o más registros aprobados, contrato con el 3PL, regente y Registro de Oferentes |
| 2. Operar (meses 6–15) | Primer inventario, ofertas en compras menores, primer cobro, primer contrato centralizado | Hasta la primera venta, B/.90 mil / B/.121 mil; hasta el pico del mes 27, B/.258 mil / B/.297 mil | Compuerta 2: ventas anualizadas de B/.90 mil o más nueve meses después de la primera venta y menos de 30% de ofertas descalificadas |
| 3. Escalar (año 2 en adelante) | Segunda ola (seis productos del sistema nervioso) y segunda licitación de precio único | Se define con la compuerta 2 | — |"""

PEND_3PL_OLD = '- [ ] Comparación detallada de los siete operadores logísticos (servicios, zonas, requisitos de alta) y validación del flete con un transitario.'
PEND_3PL_NEW = ('- [ ] Cotizaciones de 3PL: solicitudes indicativas enviadas el 8 de octubre a J. Cain, Osala, DSV e Interworld; BP Logistics, DHL y Farmazona por formulario o WhatsApp; '
                'cotización firme con la hoja de datos de fábrica; validación del flete con un transitario (seguimiento en Cotizaciones_3PL_seguimiento.md).')
PASOS_3PL_OLD = '- [ ] Cotizar regente, contador y coordinador, y pedir una cotización indicativa del 3PL: los costos fijos son el supuesto que más mueve el resultado.'
PASOS_3PL_NEW = '- [ ] Cotizar regente, contador y coordinador (las cotizaciones indicativas de 3PL se pidieron el 8 de octubre): los costos fijos son el supuesto que más mueve el resultado.'

# ---------------------------------------------------------------- 02: cadena de valor, calendario, DNFD
CADENA = """| Eslabón | Qué hace | Qué gana (caso base) |
| --- | --- | --- |
| Bueno (fábrica, Sanand) | Fabrica, emite el CPP y los certificados, firma la carta del fabricante | Su margen de fábrica (si Patel participa en ella, no está verificado) |
| Zywie (Rutul Patel) | Exporta y factura; hoy con margen propio | 15% sobre el precio de fábrica en la propuesta; el plan pide 5% o menos a libro abierto |
| La S.A. panameña | Registra, licencia, almacena en un 3PL, oferta, entrega y cobra | Precio adjudicado menos costo puesto: 49–96% de margen bruto en compras menores; −24% a 92% en precio único |
| CSS, MINSA y patronatos | Compran por PanamaCompra y pagan a 90 días desde la cuenta (unos 150 reales) | — |"""

CAL_OLD_START = 'La LPU 01-2026 (proceso 2025-1-10-01-99-SPU-000009; precio de referencia B/.95.3 millones por 349 renglones'
CAL_OLD_END = '(MINSA 2,323 y 160; CSS 1,010 y 111).'
CALENDARIO = """Qué hay en el calendario de compras, al 7 de octubre de 2026:

| Acto | Fechas verificadas | Qué implica para el plan |
| --- | --- | --- |
| LPU 01-2026 de la CSS (síntesis química; proceso 2025-1-10-01-99-SPU-000009; referencia B/.95.3 millones por 349 renglones, B/.91.98 millones según la CSS) | Ofertas el 1 y 2 de diciembre de 2025; 282 renglones adjudicados por unos B/.77.9 millones anunciados el 26 de marzo de 2026; estado «Adjudicado» en PanamaCompra desde el 15 de mayo de 2026; vigencia de 15 meses desde que quede ejecutoriada (cláusula 20) | Vence hacia la segunda mitad de 2027; la próxima LPU de síntesis química llegaría entonces. No hay LPU nueva ni plan anual de compras de la CSS publicado |
| LPU 11-2026 de la CSS (antirretrovirales, controlados e intercambiables) | Adjudicada el 31 de agosto de 2026 | Fuera de nuestro catálogo |
| Subastas en reversa del MINSA (un producto por acto) | 33 entre junio y el 6 de octubre de 2026, 28 adjudicadas | El canal centralizado disponible hoy: sin fianza de propuesta, 20% de cumplimiento, cantidades fijas |
| Contrataciones menores y compras menores ágiles de medicamentos, 2026 | Unas 3,300 y 270 (MINSA 2,323 y 160; CSS 1,010 y 111) | El canal de la primera venta |"""

PRIV_OLD_START = 'Canal privado: el mercado de farmacias existe (importaciones de medicamentos por unos US$670 millones en 2024'
PRIV_OLD_END = 'no cambia el veredicto; el modelo no lo incluye.'
PRIV_NEW = 'El canal privado de farmacias y los demás canales fuera de PanamaCompra se comparan en la sección siguiente; ninguno cambia el veredicto de la fase 0.'

DNFD = """## Quién decide y cuánto tarda la DNFD

El registro sanitario lo evalúa la Dirección Nacional de Farmacia y Drogas (DNFD) del MINSA, que dirige Uriel Pérez (director nacional desde al menos enero de 2025); el ministro de Salud es Fernando Boyd Galindo. La DNFD no publica tiempos reales por expediente; lo que sí publica da el orden de magnitud de su carga y de la nuestra:

| Dato verificado | Fuente | Qué implica para el plan |
| --- | --- | --- |
| Entre julio de 2022 y junio de 2023 la DNFD recibió 844 solicitudes de registro de medicamentos nuevos y 1,326 de renovación, y emitió 1,322 registros; el propio informe habla de «por arriba de 1,000 solicitudes» y «más de 1,000 certificados» al año | MINSA, 4.º informe de gestión 2022–2023 | Nuestros 11 expedientes son 1% de la cola anual: el plazo lo fija la cola, no nuestro volumen; por eso el modelo usa 5–9 meses y no los 80 días hábiles de la ley |
| Ruta abreviada del DE 2 de 2025 para productos ya registrados por una autoridad de referencia de la OMS: revisión en un máximo de 10 días hábiles más 5 para subsanar | TVN-2, 15 de enero de 2025 | No aplica a los productos de Bueno (la CDSCO no es autoridad de referencia); sí beneficia a competidores con registros de la FDA o la EMA |
| La salida de EE. UU. de la OMS podría sacar a la FDA de la lista de referencia; la DNFD dijo que en ese caso ajustaría el decreto | La Estrella, 31 de enero de 2025 | Riesgo para los competidores que dependen de la ruta rápida, no para nosotros |
| El IEA (Universidad de Panamá) hace el análisis de control previo y los estudios de estabilidad para la zona climática IVb; en 2015 recibía unas 900 solicitudes al año y tardaba entre 3 meses y 1 año por análisis | TVN-2, enero de 2025; La Prensa vía Salud y Fármacos, agosto de 2015 | La Ley 419 fija 60 días hábiles; el dato de 2015 es viejo, pero explica por qué el modelo deja margen |
| Los certificados OMS-BPM (COPP) de la India se tramitan solo en línea, por el portal ONDLS, desde el 15 de agosto de 2025 (circulares de la CDSCO del 25 de junio y del 15 de julio de 2025) | Medical Dialogues, 11 de agosto de 2025 | Pedir a Rutul el COPP emitido por ONDLS, verificable en línea; un certificado reciente solo en papel es una señal amarilla |

Documentos extranjeros: lo que entra al expediente va en español o con traducción de traductor público autorizado; el costo por página no está regulado y se cotiza junto con los expedientes."""

FUENTES_DNFD = """Autoridad sanitaria y capacidad

- [MINSA: 4.º informe de gestión 2022–2023 (Departamento de Registro Sanitario, gráfica 15)](https://www.minsa.gob.pa/sites/default/files/publicacion-general/4to_informe_de_gestion_2022-2023consolidado_22-09-23.pdf) · [TVN-2, 15 de enero de 2025: registro abreviado en 10 días hábiles; Uriel Pérez, director nacional de Farmacia y Drogas](https://www.tvn-2.com/contenido-exclusivo/panama-ley-de-medicamentos-seguridad-pacientes-minsa_1_2172763.html) · [La Estrella, 31 de enero de 2025: salida de EE. UU. de la OMS y registro de medicamentos](https://www.laestrella.com.pa/panama/nacional/salida-de-ee-uu-de-la-oms-complica-al-minsa-y-el-registro-de-medicamentos-NC10476319)
- [Salud y Fármacos (La Prensa, 26 de agosto de 2015): carga de trabajo del IEA](https://www.saludyfarmacos.org/?p=47058) · [Medical Dialogues, 11 de agosto de 2025: solicitudes de WHO-GMP y COPP solo por el portal ONDLS desde el 15 de agosto de 2025](https://medicaldialogues.in/news/industry/pharma/cdsco/no-more-physical-who-gmp-certificate-applications-after-august-15-dcgi-alerts-pharma-firms-153274)"""

# ---------------------------------------------------------------- 03: sensibilidad desde analysis.json
_FMT = {
    'fixed': lambda p, o: f'B/.{p:,.0f} → B/.{o:,.0f} al mes',
    'pwin_cen': lambda p, o: f'{p:.0%} → {o:.0%}',
    'share_dec': lambda p, o: f'{p:.0%} → {o:.0%}',
    'erosion': lambda p, o: f'{p:.0%} → {o:.0%} al año',
    'sup_idx': lambda p, o: f'{p:.2f} → {o:.2f} veces la referencia',
    'realiz': lambda p, o: f'{p:.0%} → {o:.0%}',
    'minsa_occ': lambda p, o: f'{p:.0%} → {o:.0%}',
    'rs_succ': lambda p, o: f'{p:.0%} → {o:.0%}',
    'mkt': lambda p, o: f'{p:.2f} → {o:.2f}',
    'cen_start': lambda p, o: f'mes {p:.0f} → mes {o:.0f}',
    'n2': lambda p, o: f'{p:.0f} → {o:.0f} productos',
    'signaturelex': lambda p, o: 'tarifas de SignatureLex → tarifas de mercado',
    'collat': lambda p, o: f'{p:.0%} → {o:.0%}',
    'pf_dec': lambda p, o: f'{p:.2f} → {o:.2f} de la mediana',
    'dso_days': lambda p, o: f'{p:.0f} → {o:.0f} días',
    'expiry': lambda p, o: f'{p:.1%} → {o:.1%}',
    'ramp_m': lambda p, o: f'{p:.0f} → {o:.0f} meses',
    'credit_days': lambda p, o: f'{p:.0f} → {o:.0f} días',
    'lead_days': lambda p, o: f'{p:.0f} → {o:.0f} días',
    'adv': lambda p, o: f'{p:.0%} → {o:.0%}',
    'reg_m': lambda p, o: f'mes {p:.0f} → mes {o:.0f}',
}


_LABEL = {
    'fixed': 'Costos fijos mensuales con cargas laborales e ITBMS',
    'sup_idx': 'Precio del proveedor frente a la referencia FOB de India',
    'mkt': 'Factor de mercado (demanda futura frente a los datos de 2025–2026)',
    'cen_start': 'Mes del primer contrato centralizado (LPU de la CSS o subasta del MINSA)',
    'realiz': 'Cantidad realmente comprada frente a la máxima del contrato',
    'minsa_occ': 'Probabilidad de que el MINSA haga su compra centralizada en el año',
    'rs_succ': 'Registros aprobados sobre registros presentados',
    'signaturelex': 'Tarifas legales: SignatureLex frente a mercado',
    'n2': 'Productos de la segunda ola (sin equivalencia terapéutica, con fabricante verificado)',
}


def _k(x):
    x = round(x / 1000)
    return ('−' if x < 0 else '+' if x > 0 else '') + f'B/.{abs(x):,.0f} mil'


def sens_table(n=12):
    a = json.load(open(os.path.join(HERE, '..', 'model', 'analysis.json'), encoding='utf-8'))
    t = a['tornado']
    rows = sorted(t['rows'], key=lambda r: -(abs(r['npv_opt'] - r['npv_pes'])))[:n]
    out = [f"Sensibilidad del caso base (VPN al 15%: {_k(t['base_npv15'])}; capital B/.{t['base_eq']/1000:,.0f} mil), moviendo un supuesto a la vez de su valor pesimista a su valor optimista, ordenada por el tamaño del efecto:", '',
           '| Supuesto | Pesimista → optimista | VPN al 15% (pesimista / optimista) | Capital (pesimista / optimista) |', '| --- | --- | --- | --- |']
    for r in rows:
        f = _FMT.get(r['key'], lambda p, o: f'{p} → {o}')
        try:
            rng = f(r['pes_val'], r['opt_val'])
        except Exception:
            rng = f"{r['pes_val']} → {r['opt_val']}"
        out.append(f"| {_LABEL.get(r['key'], r['label'])} | {rng} | {_k(r['npv_pes'])} / {_k(r['npv_opt'])} | B/.{r['eq_pes']/1000:,.0f} mil / B/.{r['eq_opt']/1000:,.0f} mil |")
    return '\n'.join(out)

# ---------------------------------------------------------------- 04: operadores, correo enviado
OPERADORES = """| Operador | Dónde | Evidencia pública (licencia, certificados) | Agencias con licencia que aloja (lista DNFD, 28-sep-2026) | Estado al 8 de octubre |
| --- | --- | --- | --- | --- |
| J. Cain & Cía | Zona Libre de Colón y Panamá Pacífico | Licencias MINSA 3-009 L y 13-001 LA; certificado BPM de acondicionamiento vigente a julio de 2027; INVIMA a diciembre de 2028; áreas de 2–8 y 15–25 °C | 24 | Correo enviado |
| Osala Logistics (Bomi Group / UPS Healthcare) | Terminal de carga de Tocumen, depósito aduanero logístico | Publica certificación DNFD de importación, almacenamiento y distribución de medicamentos con cadena de frío; ISO 9001 y 13485 | 15 | Correo enviado |
| DSV Panamá | Zona Libre de Colón | 8,000 m² y 3,500 posiciones; sistema de calidad para salud; sin licencia DNFD publicada | — | Correo enviado |
| Interworld Freight Panamá | Panamá, en bodega de un socio | Almacén farmacéutico de 2–8 y 15–25 °C; sin licencia DNFD visible | — | Correo enviado; pedir el número de licencia |
| BP Logistics (Grupo Hilasal) | Panamá Pacífico | Licencia MINSA 13-006 LA; certificado BPM 012-23 con vencimiento el 25 de octubre de 2025 en la lista (confirmar renovación); 15–25 y 2–8 °C | 8 | Formulario web de 13 preguntas con las respuestas listas (Cotizaciones_3PL_seguimiento.md); ya recibió el cuestionario anterior |
| DHL (Global Forwarding Panamá; Supply Chain) | Parque Industrial Sur, Tocumen | Licencia MINSA 8-236 L; certificado BPM de acondicionamiento 015-24 a agosto de 2026 | 16 | Formulario web pendiente |
| Farmazona / FZ Logistics (Panalog) | Fuerte Davis, Colón | Licencia MINSA 3-011 L; certificado BPM 021-24 a noviembre de 2026; INVIMA a mayo de 2029 | 22 | WhatsApp pendiente (mensaje listo) |
| Grupo TLA | Panamá Pacífico | Aloja a Vanguard Medical Logistics (Promed), licencia 13-012 LA; sin licencia propia visible | 11 | Baja prioridad |
| Alliance Transport Logistics (Grupo ALG) · Master Logistic Solutions · Kuehne+Nagel · FedEx Logistics Center | Panamá Pacífico y Tocumen | Licencias 13-002 LA y 13-003 LA (los dos primeros); áreas de 2–8 y 15–25 °C y CEIV Pharma (los dos últimos) | — | Segunda ronda, si los cuatro primeros no responden |

Nota: las listas públicas de la DNFD que se pudieron abrir son las de laboratorios acondicionadores con certificado de BPM y la de establecimientos con licencia; la licencia de almacén o de agencia es otra categoría sin lista pública consolidada. Que un operador no aparezca no significa que no tenga licencia de almacenamiento: por eso el correo pide el número de licencia."""

COTIZAR_NEW = """## Cotizar el 3PL: con quién y cómo

Qué contrata la S.A. cuando contrata un 3PL farmacéutico:

- Lo que hace: su bodega tiene licencia de la DNFD y se declara como el depósito de nuestra agencia; recibe el contenedor (con su corredor de aduana o el nuestro), lo pone en cuarentena hasta que el regente libera, almacena por lote y vencimiento, prepara los despachos por cajas y entrega en los almacenes de la CSS o del MINSA con nuestros documentos.
- Lo que cobra: al mes por posición de tarima, por recepción y por despacho; aparte el etiquetado u otros servicios; casi siempre con un mínimo mensual.
- Lo que no hace: la licencia, el regente, los registros, las ofertas y la factura al Estado siguen siendo de la S.A.
- El flujo de una venta: orden de compra de la entidad a la S.A. → instrucción de la S.A. al 3PL → entrega del 3PL con acta de recibido → factura de la S.A. → cuenta en la entidad → cobro.

Estado de las cotizaciones: las dos solicitudes anteriores no prosperaron porque fueron con estimaciones y sin fichas. El 8 de octubre de 2026 se enviaron solicitudes de cotización indicativa, o de tarifario estándar, a los cuatro operadores con correo público (J. Cain, Osala, DSV e Interworld); BP Logistics y DHL solo reciben por formulario web y Farmazona por WhatsApp. La ficha logística por producto se les manda cuando la fábrica llene la hoja de datos, y con ella se pide la cotización firme. El detalle de cada operador, las respuestas al formulario de BP Logistics y la tabla de seguimiento están en Cotizaciones_3PL_seguimiento.md.

""" + OPERADORES + """

Dos preguntas que ningún operador contesta solo y que van en paralelo a la DNFD por consulta escrita: si el depósito del 3PL puede declararse como depósito de la agencia y si el regente del operador puede cubrir a una agencia nueva o cada agencia necesita el suyo (DE 27, arts. 382 y 396–398). La respuesta define el costo fijo más grande después del coordinador."""

OPER_OLD_START = '3PL o bodega propia, sin contar el regente que ambas necesitan: con 5 tarimas, un 3PL cuesta unos B/.680 al mes contra B/.4,030 más B/.37 mil de inversión en bodega propia; con 15 tarimas, B/.960 contra B/.5,920 más B/.54 mil. Los operadores que ya alojan'
OPER_NEW_START = 'A este volumen la bodega propia no tiene sentido (la comparación está en la estimación logística, más abajo). Los operadores que ya alojan'

FACTORY_OLD = 'Con esa hoja llena se cotiza a tres operadores a la vez (correos listos más abajo).'
FACTORY_NEW = 'Con esa hoja llena se afinan las cotizaciones indicativas ya pedidas y se pide la firme (el correo enviado está más abajo).'

CORREOS_OLD_START = '## Correos de cotización listos para enviar'
CORREOS_OLD_END = '### A la aseguradora de fianzas'
CORREO_3PL = """## Correos de cotización

El correo a los operadores logísticos se envió el 8 de octubre de 2026 desde el correo de Jaime a J. Cain, Osala, DSV e Interworld; el mismo texto sirve para la segunda ronda. Los correos a las aseguradoras de fianzas y al IEA siguen pendientes de envío. Pedir a varios a la vez y decirlo.

### A los operadores logísticos (enviado el 8 de octubre de 2026)

```text
Asunto: Solicitud de cotización indicativa – almacenamiento y distribución de medicamentos (agencia en constitución)

Estimados señores de [operador]:

Somos una agencia distribuidora de medicamentos en proceso de constitución en Panamá. Importaremos 11 medicamentos genéricos de síntesis química (tabletas, suspensiones orales, cremas e inyectables en polvo, todos a temperatura ambiente controlada de 15 a 25 °C) para suministrarlos a la Caja de Seguro Social y al Ministerio de Salud mediante licitación pública. Necesitamos un depósito con licencia de la Dirección Nacional de Farmacia y Drogas que pueda declararse como depósito de nuestra agencia, y estamos solicitando cotización indicativa a tres o cuatro operadores para decidir con quién trabajar.

Volúmenes estimados:
- Primer ingreso: 5 tarimas (unos 9 m3), carga consolidada marítima desde la India vía Manzanillo.
- Régimen: 3 a 5 tarimas al mes, con picos de hasta 10; 11 productos (SKU); control por lote y fecha de vencimiento (FEFO); 2 a 4 despachos al mes, por cajas completas, a los almacenes de la CSS y del MINSA en la ciudad de Panamá.
- Sin cadena de frío por ahora; sin reetiquetado (los pliegos lo prohíben).

Agradeceríamos una cotización indicativa, o su tarifario estándar, con:
1. Tarifa mensual por posición de tarima (15 a 25 °C) y mínimo mensual facturable.
2. Recepción y despacho, por tarima y por caja; costo de alta o apertura de cuenta.
3. Corredor de aduana y acarreo desde el puerto, si lo ofrecen.
4. Entrega a los almacenes de la CSS y del MINSA, si la ofrecen, y su costo.
5. Número de licencia de operación de Farmacia y Drogas del depósito y si pueden cubrir, con su licencia y regente farmacéutico, a una agencia nueva, o qué requieren de nuestra parte.
6. Tiempo de implementación una vez firmado el contrato.

La ficha logística por producto (dimensiones y pesos de caja máster, unidades por caja, cajas por tarima, código arancelario) la estamos recibiendo de la fábrica y se la enviaremos en cuanto la tengamos, para que puedan afinar la cotización. Fecha estimada de inicio de operaciones: al obtener los registros sanitarios.

Quedamos atentos y con gusto coordinamos una visita a sus instalaciones.

Saludos cordiales,

Jaime Cucalon
Socio, agencia distribuidora de medicamentos (en constitución)
```

"""

# ---------------------------------------------------------------- 05: herramientas y orden
HERR_OLD_START = '- Carpeta compartida en Google Drive con esta estructura:'
HERR_OLD_END = '- Repositorio privado en GitHub solo para el código del modelo; los socios no lo necesitan.'
HERR_NEW = """- Carpeta compartida en Google Drive, raíz `Farma`, con tres carpetas por audiencia: `01 Privado (solo Jaime)`; `02 Socios Panamá`, para los tres socios (`00 Plan y análisis` con este paquete, `01 Empresa`, `02 Proveedor y fábrica`, `03 Registros DNFD`, `04 Licencia y 3PL`, `05 Licitaciones`, `06 Fianzas y seguros`, `07 Finanzas`); y `03 Zywie (compartido con Rutul)` (`01 Documentos enviados a Zywie`, `02 Lo que Zywie manda`). Rutul solo ve la tercera.
- Formato: los documentos de trabajo son archivos Markdown (fuente única) y Excel; para imprimir o enviar fuera se genera el PDF del paquete. Se actualizan y se vuelven a entregar cuando cambian, con fecha en el encabezado.
- Repositorio privado en GitHub (Meds) con el código del modelo y la fuente de estos documentos; los socios no lo necesitan."""
LISTA_ABAJO_OLD = '- [ ] Cotizar con la hoja de datos: tres 3PL (lista abajo), dos aseguradoras de fianzas, regente, contador, IEA.'
LISTA_ABAJO_NEW = '- [ ] Cotizar con la hoja de datos: 3PL (solicitudes indicativas enviadas el 8 de octubre; operadores en 04), dos aseguradoras de fianzas, regente, contador, IEA.'

# ---------------------------------------------------------------- 07: verificación de la noche
BRECHA_OLD = '| Tarifas de 3PL, corredor, seguro, regente, contador, auditoría, fianzas | Nadie las publica; la auditoría no contacta a terceros | Los correos de cotización del documento 04, con la hoja de datos llena; tres 3PL y dos aseguradoras a la vez |'
BRECHA_NEW = '| Tarifas de 3PL, corredor, seguro, regente, contador, auditoría, fianzas | Nadie las publica | Solicitudes indicativas enviadas el 8 de octubre a cuatro 3PL (seguimiento en Cotizaciones_3PL_seguimiento.md); firmes con la hoja de datos de fábrica; aseguradoras, IEA, regente y contador pendientes |'
VERED_02_OLD = '| −28.6% en vez de −28.7%; INDICASAT como segundo laboratorio; topes de compra menor atribuidos a la Ley 419; cobro de la Contraloría para montos grandes (32.9 días) |'
VERED_02_NEW = '| −28.6% en vez de −28.7%; INDICASAT como segundo laboratorio; topes de compra menor atribuidos a la Ley 419; cobro de la Contraloría para montos grandes (32.9 días); secciones nuevas de canales de venta y de quién decide y cuánto tarda la DNFD |'
VERED_04_OLD = '| Tabla de costos con la naturaleza de cada cifra; BP Logistics (Grupo Hilasal) e Interworld Freight; consulta a la DNFD como pendiente |'
VERED_04_NEW = '| Tabla de costos con la naturaleza de cada cifra; tabla de operadores con licencias verificadas y estado; solicitudes de cotización enviadas a cuatro operadores; consulta a la DNFD como pendiente |'
VERED_00_OLD = '| Cronología de la LPU 01-2026 corregida; tres pendientes nuevos |'
VERED_00_NEW = '| Cronología de la LPU 01-2026 corregida; tres pendientes nuevos; plan por fases en tabla; índice único del paquete (LEAME.md) |'

VERIF_NOCHE = """## Verificación adicional del 8 de octubre (noche): quién decide, cuánto tarda y qué se descartó

Se buscó de nuevo lo que la mañana había dejado como «no encontrado». Lo que se pudo verificar con documento primario o prensa fechada entró en 02 (sección «Quién decide y cuánto tarda la DNFD»); lo que no, se dice aquí para que nadie lo cite.

| Afirmación | Resultado | Confianza | Dónde se usa |
| --- | --- | --- | --- |
| Uriel Pérez es el director nacional de Farmacia y Drogas | Confirmado: así lo identifican TVN-2 (15 de enero de 2025) y La Estrella (31 de enero de 2025) | Alta (cargo público; confirmar que sigue en el cargo antes de una reunión) | 02 |
| Carga de trabajo de la DNFD: 844 solicitudes de registro nuevo y 1,326 renovaciones recibidas, 1,322 registros emitidos entre julio de 2022 y junio de 2023 | Confirmado en el 4.º informe de gestión del MINSA (gráfica 15); el informe no trae tiempos por expediente ni rezago | Alta como orden de magnitud; es el último informe con cifras abiertas | 02 |
| Cifras trimestrales de 2023 (701 solicitudes ingresadas, 457 evaluadas, 244 pendientes) y de personal (151 colaboradores, déficit de 30 farmacéuticos) citadas en la ronda de la tarde | No se pudo volver a abrir la fuente; se retiran del paquete hasta tener el documento | Sin confianza asignada; no se usan | — |
| Ruta abreviada del DE 2 de 2025: 10 días hábiles más 5 para subsanar | Confirmado en TVN-2 (15 de enero de 2025); aplica solo a productos ya registrados por autoridades de referencia | Alta | 02 |
| El IEA recibía unas 900 solicitudes al año y tardaba de 3 meses a 1 año (2015) | Confirmado en La Prensa vía Salud y Fármacos (26 de agosto de 2015); dato viejo | Media (antigüedad) | 02 |
| COPP y WHO-GMP de la India solo en línea por ONDLS | Confirmado: desde el 15 de agosto de 2025 (la fecha original del 15 de julio se extendió un mes); circulares de la CDSCO del 25 de junio y del 15 de julio de 2025 | Alta | 02, 06 |
| Los traductores públicos tienen tarifas reguladas | No: no se encontró norma que fije tarifas; el costo se cotiza | Media | 02 |

Lo que esta verificación cambia en el modelo: nada. Refuerza el supuesto de 5–9 meses para los registros (la cola de la DNFD y el IEA, no la ley, fijan el plazo) y añade una prueba barata al guion: pedir el COPP emitido por ONDLS.

Fuentes de esta verificación: [MINSA, 4.º informe de gestión 2022–2023](https://www.minsa.gob.pa/sites/default/files/publicacion-general/4to_informe_de_gestion_2022-2023consolidado_22-09-23.pdf) · [TVN-2, 15 de enero de 2025](https://www.tvn-2.com/contenido-exclusivo/panama-ley-de-medicamentos-seguridad-pacientes-minsa_1_2172763.html) · [La Estrella, 31 de enero de 2025](https://www.laestrella.com.pa/panama/nacional/salida-de-ee-uu-de-la-oms-complica-al-minsa-y-el-registro-de-medicamentos-NC10476319) · [Salud y Fármacos, 2015](https://www.saludyfarmacos.org/?p=47058) · [Medical Dialogues, 11 de agosto de 2025](https://medicaldialogues.in/news/industry/pharma/cdsco/no-more-physical-who-gmp-certificate-applications-after-august-15-dcgi-alerts-pharma-firms-153274)."""

# ---------------------------------------------------------------- LEAME
LEAME = f"""# LÉAME: cómo usar este paquete

*Versión del {FECHA}. Paquete de trabajo de los socios panameños del proyecto de distribuidora de medicamentos para compras públicas en Panamá. Uso interno: no se comparte con Rutul Patel ni con terceros.*

## En una frase

Un negocio real, con márgenes altos por producto y un mercado de más de B/.230 millones al año solo en la CSS, cuya estructura tal como la propone Rutul Patel pierde dinero en 77 de cada 100 escenarios; por eso hoy se arriesgan solo unos B/.2,700 de verificación (fase 0) y el capital grande espera a que la fábrica mande precios y documentos.

## Qué leer según lo que usted tiene que decidir

| Si usted… | Lea, en este orden | Extensión |
| --- | --- | --- |
| Solo va a poner dinero | Resumen_ejecutivo_socios_inversionistas.md → 03 (secciones «Inversión hasta la primera venta y hasta el pico» y «Riesgo cuantificado») → 07 («Cómo leer el 77% y cómo presentarlo») | Corta |
| Va a operar o a hablar con Rutul | 00 → 06 → 04 → 02 | Media |
| Va a firmar el pacto o revisar lo legal | 05 → 01 → 02 («Ruta regulatoria y legal») | Media |
| Tiene que defender un número | 07 (tabla de afirmaciones) → el documento donde se usa | Según el número |
| Va a cambiar un supuesto | Modelo_financiero_socios.xlsx (hoja de supuestos) → 03 («Supuestos del modelo y preguntas abiertas») | Según el supuesto |

## Qué contiene cada archivo

{mapa_table()}

## Reglas del paquete

- Formato: la fuente de todo es Markdown (archivos `.md`), que se lee en GitHub, en el proyecto de Claude y en cualquier editor; para imprimir o enviar fuera se genera el PDF del paquete (`Farma_paquete_socios.pdf`). No se editan cifras a mano: se corrige la fuente y se regenera.
- Toda cifra lleva su naturaleza (norma, pliego, tarifa publicada, referencia indirecta, supuesto). Lo que no tiene cotización firme está marcado como estimación o supuesto; 07 dice cuánta confianza merece cada número.
- Nombres: Rutul Patel o Patel; Zywie Worldwide; Bueno Salud Care (el fabricante inferido, que Rutul no ha nombrado).
- Con Rutul solo se comparten la hoja de datos de fábrica, el cuestionario del 3PL en blanco y, más adelante, el acuerdo de confidencialidad y la propuesta de términos.

## Dónde vive cada cosa

| Lugar | Qué hay | Quién lo ve |
| --- | --- | --- |
| Google Drive `Farma/02 Socios Panamá/00 Plan y análisis (socios)` | Este paquete en Markdown; las carpetas 01–07 de la misma raíz van recibiendo empresa, proveedor, registros, licencia y 3PL, licitaciones, fianzas y finanzas | Los tres socios panameños |
| Google Drive `Farma/03 Zywie (compartido con Rutul)` | Lo que se le envía a Zywie y lo que Zywie manda | Los socios y Rutul |
| Repositorio privado `Meds` (GitHub) | Código del modelo, generador de los documentos, notas de investigación con fuentes, este paquete y el PDF | Jaime y Claude |
| Proyecto de Claude «Med Tenders Panama» | Copia de trabajo del paquete y bitácora | Jaime y Claude |

## Qué cambió en cada versión

| Fecha | Cambios |
| --- | --- |
| 7 de octubre de 2026 | Primera versión del paquete (00–06, anexos y modelo) |
| 8 de octubre de 2026, mañana | Auditoría independiente de 31 afirmaciones (07); cronología de la LPU 01-2026; naturaleza de cada cifra logística; junta de Bueno con discrepancia entre espejos |
| 8 de octubre de 2026, tarde | Verificación de referencias FOB contra aduana india (03, 07); sección de canales de venta (02); resumen ejecutivo; investigación de operadores logísticos |
| 8 de octubre de 2026, noche | Solicitudes de cotización enviadas a cuatro 3PL; tabla de operadores con licencias (04); quién decide y cuánto tarda la DNFD (02); sensibilidad en tabla (03); plan por fases en tabla (00); este LÉAME; Markdown como formato de lectura; retirados los marcadores de gráficos y los párrafos duplicados |
"""

# ---------------------------------------------------------------- aplicación
_GRAFICO = re.compile(r'\*\(Gráfico:[^\n]*\)\*\n\n')


def _rep(md, old, new, name, count=1):
    assert old in md, f'{name}: no se encontró el anclaje «{old[:80]}»'
    return md.replace(old, new, count)


def _cut(md, start, end, new, name, keep_end=False):
    i = md.index(start) if start in md else None
    assert i is not None, f'{name}: no se encontró el inicio «{start[:70]}»'
    j = md.index(end, i)
    j_end = j if keep_end else j + len(end)
    return md[:i] + new + md[j_end:]


def apply_post(name, md):
    """Aplica las correcciones de la tercera pasada al documento `name` (texto Markdown final)."""
    # --- globales
    md = md.replace('Debida diligencia: enlaces en la tabla de esa sección.\n\n', '').replace('\nDebida diligencia: enlaces en la tabla de esa sección.\n', '\n')
    md = md.replace('\\~', 'unos ')
    if name.startswith('07'):
        md = md.replace('(ver 07_Auditoria_y_confianza.md)', '(este documento)')
    if name.startswith('00'):
        md = _cut(md, '| Archivo | Qué contiene | Léalo para |', 'se contrastan en privado.', mapa_table('00_Resumen_y_plan.md') + '\n\n' + REGLA_USO, name)
        md = _rep(md, '*(Gráfico: Plan por fases · 4 fases, 3 compuertas. Ver el modelo en Excel.)*', FASES, name)
        md = _rep(md, PEND_3PL_OLD, PEND_3PL_NEW, name)
        md = _rep(md, PASOS_3PL_OLD, PASOS_3PL_NEW, name)
    if name.startswith('01'):
        md = _cut(md, '## Lo que un fabricante exportador manda sin que se lo pidan dos veces', '## Fuentes', '', name, keep_end=True)
        md = _rep(md, 'Se le piden los documentos que cualquier distribuidor pide (ver la sección siguiente) y se contrasta en privado.',
                  'Se le piden los documentos que cualquier distribuidor pide (la lista del paquete estándar de un exportador está en 06_Guion_conversacion_Rutul.md) y se contrasta en privado.', name)
    if name.startswith('02'):
        md = _rep(md, '*(Gráfico: Cadena de valor y flujo de dinero · 4 eslabones, caso base. Ver el modelo en Excel.)*', CADENA, name)
        md = _cut(md, CAL_OLD_START, CAL_OLD_END, CALENDARIO, name)
        md = _cut(md, PRIV_OLD_START, PRIV_OLD_END, PRIV_NEW, name)
        md = _rep(md, '## Fuentes\n\n', DNFD + '\n\n## Fuentes\n\n', name)
        md = md.rstrip('\n') + '\n\n' + FUENTES_DNFD + '\n'
    if name.startswith('03'):
        md = _rep(md, '*(Gráfico: Modelo financiero, caso base · sensibilidad de un supuesto a la vez. Ver el modelo en Excel.)*', sens_table(), name)
    if name.startswith('04'):
        md = _cut(md, '## Cuánto tiempo puede estar el producto en bodega', '## Cotizar el 3PL: con quién y cómo', '', name, keep_end=True)
        md = _rep(md, OPER_OLD_START, OPER_NEW_START, name)
        md = _cut(md, '## Cotizar el 3PL: con quién y cómo', '## La hoja de datos de fábrica y el cuestionario del 3PL', COTIZAR_NEW + '\n\n', name, keep_end=True)
        md = _rep(md, FACTORY_OLD, FACTORY_NEW, name)
        md = _cut(md, CORREOS_OLD_START, CORREOS_OLD_END, CORREO_3PL, name, keep_end=True)
        md = md.rstrip('\n') + '\n\n- Seguimiento de las cotizaciones de 3PL: Cotizaciones_3PL_seguimiento.md (canales, licencias, fechas y respuestas).\n'
    if name.startswith('05'):
        md = _cut(md, HERR_OLD_START, HERR_OLD_END, HERR_NEW, name)
        md = _rep(md, LISTA_ABAJO_OLD, LISTA_ABAJO_NEW, name)
    if name.startswith('06'):
        md = _rep(md, 'Cinco burbujas, en inglés, seguidas, en el grupo.', 'Seis burbujas, en inglés, seguidas, en el grupo.', name)
        md = _rep(md, 'Solo dos pedidos esta noche: la hoja de datos y el paquete del proveedor.', 'Solo tres pedidos esta noche: la hoja de datos, el paquete del proveedor y su correo electrónico (Jaime no lo tiene).', name)
        md = _rep(md, "Lo que hace: explica el retraso sin excusas,", "Burbuja 6 (el correo de Rutul, que hoy no tenemos):\n\n```text\nAlso, what's the best email for you? Some of this is easier to send properly than over chat.\n```\n\nLo que hace: explica el retraso sin excusas,", name)
        # tabla de seguimiento: celdas por llenar llevan guion
        def fill(m):
            return m.group(0).replace('|  |', '| — |').replace('|  |', '| — |')
        md = re.sub(r'^\| \d+ \| .*\|$', fill, md, flags=re.M)
    if name.startswith('07'):
        md = _rep(md, BRECHA_OLD, BRECHA_NEW, name)
        md = _rep(md, VERED_02_OLD, VERED_02_NEW, name)
        md = _rep(md, VERED_04_OLD, VERED_04_NEW, name)
        md = _rep(md, VERED_00_OLD, VERED_00_NEW, name)
        md = _rep(md, '## Fuentes de esta auditoría', VERIF_NOCHE + '\n\n## Fuentes de esta auditoría', name)
    if name.startswith('Anexo_Plan'):
        md = md.replace('*(Gráfico: Plan por fases · 4 fases, 3 compuertas. Ver el modelo en Excel.)*', FASES)
        md = md.replace('*(Gráfico: Cadena de valor y flujo de dinero · 4 eslabones, caso base. Ver el modelo en Excel.)*', CADENA)
    # marcadores de gráficos que queden
    md = _GRAFICO.sub('', md)
    md = re.sub(r'\n{3,}', '\n\n', md)
    return md
