# -*- coding: utf-8 -*-
"""Cuarta pasada de auditoría (9 de octubre de 2026).

Correcciones de contenido y de coherencia detectadas por la revisión cruzada de los trece documentos:
cifras redondeadas mal, referencias cruzadas equivocadas, afirmaciones sin fuente, inferencias presentadas
como hechos, duplicados, el cuestionario de BP Logistics fuera del paquete para Rutul, la lista de cifras
no obtenidas (07), la respuesta de J. Cain y la regla de que ninguna comunicación externa sale sin la
aprobación de Jaime. Se aplica después de audit_edits2.apply_post sobre el texto final de cada documento.
"""
import re


def _rep(md, old, new, name, count=1):
    assert old in md, f'{name}: no se encontró el anclaje «{old[:90]}»'
    return md.replace(old, new, count)


def _opt(md, old, new):
    return md.replace(old, new)


REV = ('revisado el 8 de octubre de 2026', 'revisado el 9 de octubre de 2026')

# ---------------------------------------------------------------- reemplazos comunes (old, new, documento donde debe existir)
GLOBAL = [
    REV + ('00_Resumen_y_plan.md',),
    ('Las cifras salen del modelo financiero adjunto (Modelo_financiero_socios.xlsx)',
     'Las cifras financieras salen del modelo (Modelo_financiero_socios.xlsx, en la misma carpeta de Drive)', '00_Resumen_y_plan.md'),
    ('B/.70 mil / B/.100 mil', 'B/.71 mil / B/.102 mil', '00_Resumen_y_plan.md'),
    ('150 días de crédito, registros pagados por Bueno', '150 días de crédito o más (objetivo 180), registros pagados por Bueno', '00_Resumen_y_plan.md'),
    ('B/.3,425 por registro (unos B/.3,570 con muestras)', 'B/.3,420 por registro (unos B/.3,570 con muestras)', '03_Costos_capital_y_proyeccion.md'),
    ('| 3,425 sin muestras |', '| 3,420 sin muestras |', '03_Costos_capital_y_proyeccion.md'),
    ('| Base de 800–1,200: +B/.2–7 mil de capital |', '| Base de 800–1,200: +B/.2–7 mil de capital en la primera ola (+3–10 mil con la segunda) |', '03_Costos_capital_y_proyeccion.md'),
    ('unos B/.222 mil hasta el mes 18', 'unos B/.225 mil (222 sin la fase 0) hasta el mes 18', '03_Costos_capital_y_proyeccion.md'),
    ('Juntos suben el capital del caso base de B/.209 mil a B/.255 mil y bajan el VPN de −B/.13 mil a −B/.56 mil.',
     'Juntos suben el capital del caso base de B/.209 mil a B/.255 mil y bajan el VPN de −B/.13 mil a −B/.56 mil (cifras de la versión del 6 de octubre frente a la actual).', '03_Costos_capital_y_proyeccion.md'),
    ('que bajan el VPN del caso base de −B/.13 mil a −B/.56 mil.', 'que bajan el VPN del caso base de −B/.13 mil (versión del 6 de octubre) a −B/.56 mil.', '00_Resumen_y_plan.md'),
    ('Con las cremas al precio de aduana, el VPN del caso base baja de −B/.56 mil a −B/.77 mil y la TIR de 6.8% a 3.3%; por eso la lista de precios de la fábrica decide qué entra en la primera ola.',
     'Con las cremas al precio de aduana, el VPN del caso base baja de −B/.56 mil a −B/.77 mil y la TIR de 6.8% a 3.3% (sin las dos cremas, −B/.66 mil y 4.6%; ambos casos están en la tabla de qué pasaría si del análisis del modelo); por eso la lista de precios de la fábrica decide qué entra en la primera ola.', '03_Costos_capital_y_proyeccion.md'),
    ('Se adjudicaron 283 (81%), con una mediana', 'Se adjudicaron 283 según la tabulación propia del cuadro de propuestas (282 según el comunicado de la CSS), 81%, con una mediana', '02_Mercado_requisitos_y_competencia.md'),
    ('referencia B/.95.3 millones por 349 renglones, B/.91.98 millones según la CSS)', 'referencia B/.95.3 millones por 349 renglones, 348 en el cuadro de propuestas; B/.91.98 millones según la CSS)', '02_Mercado_requisitos_y_competencia.md'),
    ('| Certificado de buenas prácticas de almacenamiento | — | B/.100 | Res. 181 de 2025 |',
     '| Certificado de buenas prácticas de almacenamiento | — | B/.100 | DE 27, art. 15 (tasa); Res. 181 de 2025 (procedimiento y vigencia de 2 años) |', '02_Mercado_requisitos_y_competencia.md'),
    ('Bueno cerró el año fiscal 2025 con pérdida neta y deuda garantizada del orden de sus ventas, así que',
     'Según los espejos del registro mercantil indio (sin estados auditados), Bueno cerró el año fiscal 2025 con pérdida neta y gravámenes registrados del orden de sus ventas, así que', '05_Trato_socios_y_hoja_de_ruta.md'),
    ('| 1. Constituir y registrar (meses 0–6) | Pacto de accionistas, S.A., cuenta bancaria, licencia de la DNFD, contrato con el 3PL, 11 registros sanitarios | B/.71 mil / B/.102 mil |',
     '| 1. Constituir y registrar (meses 0–6) | Pacto de accionistas, S.A., cuenta bancaria, licencia de la DNFD, contrato con el 3PL, 11 registros sanitarios | B/.71 mil / B/.102 mil (incluida la fase 0) |', '00_Resumen_y_plan.md'),
    ('| 3. Escalar (año 2 en adelante) | Segunda ola (seis productos del sistema nervioso) y segunda licitación de precio único | Se define con la compuerta 2 | — |',
     '| 3. Escalar (año 2 en adelante) | Ampliación con los seis productos del sistema nervioso (si su fabricante se verifica; la segunda ola genérica del mes 18 ya está en el caso base) y segunda licitación de precio único | Se define con la compuerta 2 | Sin compuerta posterior: revisión anual con los indicadores de la tabla siguiente |', '00_Resumen_y_plan.md'),
    ('Compuerta 0: precio de Bueno de 1.1 veces la referencia FOB del modelo (hoja SKUs) o menos, 150 días de crédito o más (objetivo 180), registros pagados por Bueno, y planta y fabricante del sistema nervioso verificados. Compuerta 1: 8 o más registros aprobados, contrato con el 3PL, regente y Registro de Oferentes. Compuerta 2: ventas anualizadas de B/.90 mil o más nueve meses después de la primera venta, contando contratos ganados, y menos de 30% de ofertas descalificadas.\n\n',
     '', '00_Resumen_y_plan.md'),
    ('- [ ] Cotizaciones de 3PL: solicitudes indicativas enviadas el 8 de octubre a J. Cain, Osala, DSV e Interworld; BP Logistics, DHL y Farmazona por formulario o WhatsApp; cotización firme con la hoja de datos de fábrica; validación del flete con un transitario (seguimiento en Cotizaciones_3PL_seguimiento.md).\n',
     '', '00_Resumen_y_plan.md'),
    ('- [ ] Cotizaciones firmes: tres 3PL (con la hoja de datos llena), dos aseguradoras de fianzas (colateral y prima), regente, contador y análisis del IEA por producto. Los costos fijos son el supuesto que más mueve el resultado.',
     '- [ ] Cotizaciones firmes: tres 3PL (solicitudes indicativas enviadas el 8 de octubre a J. Cain, Osala, DSV e Interworld; J. Cain propuso una videollamada para el 14 de octubre; BP Logistics, DHL y Farmazona pendientes por formulario o WhatsApp; la firme con la hoja de datos de fábrica; seguimiento en Cotizaciones_3PL_seguimiento.md), dos aseguradoras de fianzas (colateral y prima), regente, contador y análisis del IEA por producto. Los costos fijos son el supuesto que más mueve el resultado.', '00_Resumen_y_plan.md'),
    ('- [ ] Estado actual de la junta de Bueno (formulario DIR-12 o lista de directores) y estados auditados del año fiscal 2025: los espejos del registro no coinciden.\n', '', '00_Resumen_y_plan.md'),
    ('- [ ] Quiénes son los accionistas de Bueno Salud Care y de Zywie; estados financieros auditados del año fiscal 2025.',
     '- [ ] Quiénes son los accionistas de Bueno Salud Care y de Zywie; estado actual de la junta de Bueno (formulario DIR-12 o lista de directores: los espejos del registro no coinciden) y estados financieros auditados del año fiscal 2025.', '00_Resumen_y_plan.md'),
    ('- [ ] Licencias de fabricación de la FDCA de Gujarat por bloque y planta de fabricación de cada producto (Sanand o Roorkee).',
     '- [ ] Licencias de fabricación estatales por bloque y planta de fabricación de cada producto (FDCA de Gujarat para Sanand; Uttarakhand si algo se fabrica en Roorkee).', '00_Resumen_y_plan.md'),
    ('- [ ] Fabricante, licencias y certificados de los productos del sistema nervioso de la segunda ola.',
     '- [ ] Fabricante, licencias y certificados de los seis productos del sistema nervioso (ampliación de la primera ola).', '00_Resumen_y_plan.md'),
    ('- [ ] Negociar la hoja de términos con las siete condiciones de la sección del trato.',
     '- [ ] Negociar la hoja de términos con las siete condiciones de 05, sección «Estructura del trato con Patel».', '00_Resumen_y_plan.md'),
    ('(las cotizaciones indicativas de 3PL se pidieron el 8 de octubre): los costos fijos son el supuesto que más mueve el resultado.',
     '(las cotizaciones indicativas de 3PL se pidieron el 8 de octubre).', '00_Resumen_y_plan.md'),
    ('| Victorias sobre cotizaciones presentadas | 20% o más | PanamaCompra |',
     '| Victorias sobre cotizaciones presentadas | 20% o más (meta; el modelo usa 22% en compras menores y 30% en licitaciones) | PanamaCompra |', '00_Resumen_y_plan.md'),
    ('| Margen bruto realizado en compras menores | 50% o más | Contabilidad |',
     '| Margen bruto realizado en compras menores | 50% o más (meta; el modelo estima 62% en promedio) | Contabilidad |', '00_Resumen_y_plan.md'),
    ('pago a 90 días desde la cuenta, unos 150 reales | Pliegos |', 'pago a 90 días desde la cuenta, unos 150 reales | Pliegos (90 días); estimación propia (150) |', '00_Resumen_y_plan.md'),
    ('| Canal privado de farmacias | B/.5–35 mil al año de contribución para una marca desconocida | Investigación del 7 de octubre |',
     '| Canal privado de farmacias | B/.5–35 mil al año de contribución para una marca desconocida (estimación propia) | 02, sección Canales de venta |', '00_Resumen_y_plan.md'),
    ('su lista de productos coincide en 97% con la de Zywie;', 'su lista de productos coincide en 97% con la de Zywie (comparación propia, ver 01);', '00_Resumen_y_plan.md'),
    ('| 3–6 (5–9) | Expedientes de los 11 productos: análisis del IEA (hasta 60 días hábiles) y evaluación de la DNFD (hasta 20 días hábiles); registros aprobados | Ley 419, arts. 41 y 74; calidad de los expedientes que mande la fábrica | Abril–junio de 2027',
     '| 3–6 (5–9) | Expedientes de los 11 productos: análisis del IEA (hasta 60 días hábiles) y evaluación de la DNFD (hasta 20 días hábiles); registros aprobados | Ley 419, arts. 41 y 74; calidad de los expedientes que mande la fábrica | Marzo–junio de 2027', '00_Resumen_y_plan.md'),
    ('| Anexo_DD_hallazgos_en.md | Hallazgos de la primera ronda de debida diligencia, en inglés, con cada enlace | Verificar fuente por fuente |',
     '| Anexo_DD_hallazgos_en.md | Hallazgos de la debida diligencia, en inglés, con cada enlace: primera ronda (6 de octubre) y addendum (7 y 8 de octubre) | Verificar fuente por fuente |', 'LEAME.md'),
    ('`Farma/02 Socios Panamá/00 Plan y análisis (socios)`', '`Farma/02 Socios Panamá/00 Plan y análisis`', 'LEAME.md'),
    ('un mercado de más de B/.230 millones al año solo en la CSS', 'un presupuesto de medicamentos de unos B/.230 millones en la CSS para 2027', 'LEAME.md'),
    ('las siete condiciones del plan de negocio', 'las siete condiciones de la sección «Estructura del trato con Patel» de este documento', '05_Trato_socios_y_hoja_de_ruta.md'),
    ('| Juan Luis | Capital dentro de su tope | Por definir: quién vigila', '| Juan Luis | Capital dentro de su tope | Abierto (lo deciden los tres): quién vigila', '05_Trato_socios_y_hoja_de_ruta.md'),
    ('sin comprometer más de 40% de los ahorros en negocios propios.', 'sin comprometer más de 40% de los ahorros en negocios propios (regla de prudencia personal, no un resultado del modelo).', '05_Trato_socios_y_hoja_de_ruta.md'),
    ('- Riesgo fuera del capital: las aseguradoras piden codeudores solidarios para las fianzas;', '- Riesgo fuera del capital: las aseguradoras piden codeudores solidarios para las fianzas (requisitos publicados por Internacional de Seguros y ASSA; ver 03);', '05_Trato_socios_y_hoja_de_ruta.md'),
    ('con accionista extranjero e importación de medicamentos la revisión es más larga, así que se empieza apenas exista la S.A.',
     'con accionista extranjero e importación de medicamentos la revisión suele ser más larga (práctica bancaria, sin plazo publicado), así que se empieza apenas exista la S.A.', '05_Trato_socios_y_hoja_de_ruta.md'),
    ('El capital por socio en esta tabla es el del caso base, con un tercio del lado panameño cada uno.',
     'El capital por socio en esta tabla es el del caso base: un sexto del capital de la S.A. (la mitad panameña entre tres; con Patel al 70%, el 30% entre tres) más un tercio de la fase 0, que pagan solo los socios panameños (B/.43,435, B/.29,304 y B/.17,939). La parte del valor para Patel usa el método de la hoja Valoración del modelo: margen de Zywie más su parte de lo distribuido menos su parte del capital (casos «reparto por estructura» del análisis).', '05_Trato_socios_y_hoja_de_ruta.md'),
    ('| Tasa única 300 al año |', '| La tasa única (B/.300 al año) va en los costos fijos |', '03_Costos_capital_y_proyeccion.md'),
    ('| B/.26,476 | B/.11,602 | B/.26,476 | B/.11,602 |', '| B/.26,476 | B/.11,603 | B/.26,476 | B/.11,603 |', '03_Costos_capital_y_proyeccion.md'),
    ('82% del dinero son arranque, registros y costos fijos', '82% del dinero (76% con tarifas de mercado) son arranque, registros y costos fijos', '03_Costos_capital_y_proyeccion.md'),
    ('la fianza en efectivo o cheque certificado es una alternativa legal sin prima', 'la fianza en efectivo o cheque certificado es una alternativa sin prima (formas de garantía de la Ley 22; artículo por confirmar en el Texto Único)', '03_Costos_capital_y_proyeccion.md'),
    ('| La Ley 22 permite ceder el crédito; baja la TIR', '| La Ley 22 permite ceder el crédito (art. 97 del Texto Único, por confirmar); baja la TIR', '03_Costos_capital_y_proyeccion.md'),
    ('desconsolidación US$86.5 por m³; THC en Manzanillo US$275 por contenedor | Contenedor a US$180–220 por m³; la carga consolidada puede subir a 250–300 |',
     'desconsolidación US$0.20 por pie cúbico (unos US$7 por m³, mínimo US$55) en el tarifario de Crowley y US$86.5 por m³ en una cotización privada de 2025; THC en Manzanillo US$275 por contenedor | Contenedor: US$180–220 por m³ solo de flete (US$251 con destino); carga consolidada: US$302 por m³ puesta en bodega en el caso base y hasta 470 en el alto |', '03_Costos_capital_y_proyeccion.md'),
    ('más B/.2 por línea | B/.200–400 por embarque |', 'más B/.2 por línea | B/.200–350 por embarque |', '03_Costos_capital_y_proyeccion.md'),
    ('unos B/.200–400 por embarque de 11 productos', 'unos B/.200–350 por embarque de 11 productos', '04_Logistica_y_operacion.md'),
    ('[CDSCO, lista OMS-BPM al 31 de diciembre de 2025](', '[CDSCO, lista OMS-BPM al 31 de diciembre de 2025; el nombre del archivo en su servidor habla de laboratorios, pero el contenido es la lista OMS-BPM](', '01_Investigacion_Rutul_y_fabricante.md'),
    ('compuerta operativa', 'compuerta 2 (operativa)', '03_Costos_capital_y_proyeccion.md'),
    ('Compuerta operativa', 'Compuerta 2 (operativa)', 'Resumen_ejecutivo_socios_inversionistas.md'),
]

# ---------------------------------------------------------------- 07: cifras no obtenidas e información faltante
MISSING = """## Cifras no obtenidas e información faltante (9 de octubre de 2026)

Lo que el modelo usa como supuesto porque nadie lo publica o porque solo lo tiene la contraparte. La columna «Fuente pública» dice si vale la pena seguir buscando: cuando dice «No», el dato se obtiene cotizando o pidiéndolo, no investigando. Los supuestos van en el orden pesimista / base / optimista del modelo (hoja Supuestos).

| Dato | Dónde se usa | Qué se intentó | Fuente pública | Cómo se obtiene | Supuesto en el modelo (pes / base / opt) |
| --- | --- | --- | --- | --- | --- |
| Tarifa del 3PL licenciado: posición de tarima, mínimo mensual, recepción y despacho | 03, 04; costo fijo «3PL» | Correos a J. Cain, Osala, DSV e Interworld (8 de octubre); formularios de BP Logistics y DHL; WhatsApp de Farmazona; búsqueda de tarifarios | No: ningún 3PL de Panamá publica tarifas | Cotización (J. Cain propuso videollamada el 14 de octubre); la firme exige la hoja de datos de fábrica | B/.1,200 / 600 / 300 al mes |
| Flete consolidado (LCL) India–Manzanillo por m³ y costos de destino | 04; multiplicador logístico | Tarifa FAK por contenedor (CMA CGM, publicada), THC de Maersk (publicada), tarifario de Crowley, referencias LCL India–EE. UU. y Europa | Parcial: contenedor sí; LCL a Panamá no | Transitario o consolidador, con la ficha logística por producto | US$450 / 300 / 240 por m³ puesto en bodega (multiplicador 1.5 / 1.0 / 0.8 sobre 300) |
| Seguro de carga | 04 | Sin tarifa pública | No | Aseguradora de carga o transitario | 0.5% / 0.3% / 0.15% del CIF (dentro del costo por m³) |
| Colateral y prima de las fianzas | 03; capital | Banco General publica 1.07–1.605% anual (marzo de 2026); las aseguradoras publican requisitos, no el colateral | Parcial: prima sí (un emisor); colateral no | Dos aseguradoras: correo listo, sale cuando Jaime apruebe el texto | Colateral 100% / 50% / 25%; prima 3.0% / 1.6% / 1.07% |
| Análisis de control previo del IEA por producto | 03; costo de registro | Guía oficial de 2012 (B/.200–1,000); Ley 419, art. 72; sin tarifario actual | No: cotiza caso a caso | IEA e INDICASAT: correo listo, sale cuando Jaime apruebe el texto | B/.1,500 / 600 / 300 |
| Regente farmacéutico a medio tiempo | 03; costo fijo | DE 27, art. 382 (4 horas diarias); SignatureLex 400–500; Paylab 1,339–3,228 a tiempo completo | Parcial: referencias salariales, sin cotización | Dos o tres regentes (Colegio de Farmacéuticos, anuncios) | B/.1,200 / 700 / 450 al mes |
| Contabilidad y auditoría anual | 03; costo fijo | Sin tarifario público | No | Dos firmas contables | B/.450 + 400 / 300 + 250 / 200 + 150 al mes |
| Coordinador de licitaciones a medio tiempo | 03; costo fijo (la palanca que más mueve el VPN) | Referencias salariales | Parcial | Decisión de los socios: quién opera y con qué sueldo | B/.2,500 / 1,500 / 800 al mes |
| Precio FOB de fábrica, lote mínimo, vida útil aprobada, anticipo y crédito | Todo el modelo (índice del proveedor, anticipo, crédito) | Referencias indias (TNMSC, Jan Aushadhi, contrato de Delhi) y muestra de aduana india de 2016 | No: solo la fábrica | Rutul Patel (pasos 2, 3 y 7 del guion) | Índice 1.80 / 1.25 / 1.00; anticipo 100% / 30% / 0; crédito 0 / 0 / 120 días |
| Nombre legal del fabricante y planta de cada producto | 01, 02, 06 | Registros públicos de India y de nueve países; comparación de listas (97%) | Inferido (Bueno Salud Care, Sanand); no confirmable sin su CPP | Rutul (paso 2); el CPP y la licencia lo cierran | Se asume Bueno Salud Care |
| Accionistas de Bueno y de Zywie; estados auditados del año fiscal 2025 | 01, 05 | Espejos gratuitos del MCA (directores, cargas, cifras resumidas); el informe completo es de pago | Parcial: directores sí; accionistas y estados solo con el informe del MCA (US$10–30) o pidiéndolos | Rutul (paso 6) o compra del informe del MCA | Pérdida neta y gravámenes por ₹104 crore según espejos; capacidad de financiar por probar |
| Causa y corrección de las dos alertas de calidad de marzo de 2024 | 01, 06 | Lista pública de la CDSCO (solo el hecho) | No: documento interno de la fábrica | Rutul (paso 5, cuestionario de calificación) | Riesgo de planta de 15% en la simulación |
| Licencias de fabricación por bloque (FDCA de Gujarat) | 01 | fdca.gujarat.gov.in inaccesible desde aquí (DNS / 502); lista OMS-BPM de la CDSCO sí abierta | No desde aquí | Rutul (paso 5) | COPP vigente hasta el 26 de enero de 2029 (CDSCO) |
| Experiencia en El Salvador y Colombia (registros, distribuidor) | 01, 06 | DNM de El Salvador (2,149 registros), COMPRASAL (5,819 líneas), INVIMA en datos abiertos: cero | No aparece en ninguna | Rutul (paso 6) | Se trata como no verificada |
| Fecha exacta de adjudicación ejecutoriada y vencimiento de la LPU 01-2026 | 00, 02 | Comunicado de la CSS (26 de marzo de 2026); estado «Adjudicado» en PanamaCompra (15 de mayo de 2026); resolución no localizada | Parcial: la resolución debe estar en los documentos del acto en PanamaCompra | Descargar la resolución del acto | Vence en la segunda mitad de 2027; primer contrato centralizado en el mes 27 / 15 / 12 |
| Pliego y fecha de la compra conjunta MINSA-CSS (DE 16 de 2026) | 02 | Búsqueda en PanamaCompra al 7 de octubre: sin acto publicado | Todavía no existe | PanamaCompra cuando se publique | Probabilidad de que el MINSA compre centralizado en el año: 30% / 50% / 70% |
| Si el depósito del 3PL puede declararse como depósito de la agencia y si su regente puede cubrirla | 04 | DE 27, arts. 382 y 396–398 leídos; la práctica no está publicada | No sin consulta | Consulta escrita a la DNFD (texto por preparar y aprobar) | Se asume que sí (3PL como costo fijo) |
| Tasa propia de victoria y de descalificación | 02; probabilidad de ganar y participación | OCDS del MINSA 2020–2024: entrantes 17% de victorias y 56% de descalificación | Parcial: histórico sí; propia no | Solo compitiendo (compuerta 2) | Probabilidad de ganar renglón centralizado 15% / 30% / 45%; participación madura 10% / 22% / 32% |
| Traducción pública y apostillas por expediente | 02, 03 | Sin tarifa regulada | No | Traductor público autorizado | Dentro del honorario y gastos por registro |
| Costo del CPP y de la legalización en India | 06 | No publicado para la fábrica | No | Rutul | Dentro del paquete del proveedor |
| Honorario real del corredor de aduana | 04 | Ley 20 de 1994: mínimo legal B/.50 + 0.15% del CIF | Parcial: el mínimo legal sí | Corredor, con el primer embarque | B/.350 / 200 / 100 por embarque |
| Acarreo de Manzanillo a la bodega | 04 | Sin tarifa pública | No | 3PL o transportista | US$550 / 350 / 200 por embarque |
| Volumen real de compra del Estado en 2027 | 02; factor de mercado | Presupuesto de la CSS 2027 (−28.6%, La Prensa; 7.2% más unidades, Decisiones Panamá) | Parcial: presupuesto sí; ejecución no existe aún | Ejecución presupuestaria de 2027 | Factor de mercado 0.75 / 0.90 / 1.00 |

### Verificaciones del 9 de octubre

| Afirmación | Resultado | Fuente |
| --- | --- | --- |
| Lisinopril y clopidogrel exigen equivalencia terapéutica; mometasona e hidrocortisona no (06, paso 2) | Confirmado: lisinopril es el número 103 y clopidogrel el 34 de la lista; mometasona, hidrocortisona, paracetamol, amoxicilina, ceftriaxona, cefotaxima, albendazol, mebendazol y nistatina no figuran | Resolución 985 de 2025, PDF del MINSA (texto extraíble) |
| Capital por socio y parte del valor para Patel por estructura (05): B/.43.4 / 29.3 / 17.9 mil y 69% / 54% / 43% | Reproducidos con el motor del modelo (un sexto del capital más un tercio de la fase 0; reparto con el método de la hoja Valoración) y añadidos al análisis | model/analysis.py, casos «value_split_struct» |
| Sensibilidad de las cremas (03, 07): −B/.77 mil y 3.3%; sin cremas −B/.66 mil y 4.6% | Reproducidos y añadidos a la tabla de qué pasaría si del análisis | model/analysis.py, casos «Cremas a precio de aduana» y «Primera ola sin las dos cremas» |
| Desconsolidación US$86.5 por m³ «en el tarifario de Crowley» (04) | Corregido: el tarifario de Crowley cobra US$0.20 por pie cúbico (mínimo US$55); los US$86.5 son una cotización privada de 2025 | Tarifario DHC de Crowley (PDF); registro de la investigación logística |
| Licencias de agencia de los propios operadores (04) | Añadidas: J. Cain 13-005 A y 3-001; BP Logistics 13-031 A (vence el 16 de diciembre de 2026); Grupo TLA 13-000 y 13-132 | Lista de la DNFD de establecimientos con licencia al 28 de septiembre de 2026 |
| Junta de Bueno (01) | Los espejos con fecha de consulta (Falconebiz, The Company Check) listan tres directores; se retiran las citas a AllIndiaITR y Tracxn, sin registro de lo visto | Registro de la investigación del 7 de octubre |

"""

# ---------------------------------------------------------------- Anexo DD: addendum de la segunda ronda (en inglés, como el anexo)
DD_ADDENDUM = """
## D. ADDENDUM — second round (public sources; 2026-10-07, checked again 2026-10-08)

Raw log with every URL: research/research2_a_bueno_dd/notes.md in the code repository (Meds).

### D1. Verified
1. Bueno's board per MCA mirrors: Falconebiz (last updated 02-Sep-2026) lists three directors — Shivkumar Dudhwewala (WTD since 26-Sep-2019), Deepti Rutul Patel and Abhinav Bhargava (both "since 30-Sep-2024", the regularisation date); The Company Check (updated 21-Sep-2026) gives Bhargava from 18-Mar-2024 and Deepti Rutul Patel from 08-Jul-2024 (additional directors regularised 29-Sep-2024). Tofler (AGM 30-Sep-2023) and Zauba (to 2024) predate her appointment. — https://www.falconebiz.com/company/BUENO-SALUD-CARE-INDIA-PRIVATE-LIMITED-U24304GJ2016PTC094652 ; https://www.thecompanycheck.com/company/bueno-salud-care-india-private-limited/U24304GJ2016PTC094652 ; https://www.tofler.in/bueno-salud-care-india-private-limited/company/U24304GJ2016PTC094652 ; https://www.zaubacorp.com/company/BUENO-SALUD-CARE-INDIA-PRIVATE-LIMITED/U24304GJ2016PTC094652 . Section A.7 above (two directors) is superseded by this entry.
2. Bueno FY2025 (The Company Check, free summary; not audited accounts): revenue ₹101.8 crore (+30%), net loss ₹4.8 crore, 252 EPFO employees; open charges ₹103.96 crore (secured facilities registered, not necessarily drawn debt), satisfied ₹60.24 crore; registered office moved to the plant (K-20/21, Sanand); financials filed for 31-Mar-2025, AGM 30-Sep-2025. Full MCA documents are paywalled.
3. Salud Care (India) Limited (group parent, Ahmedabad): CIN U24239GJ2003PLC130558, paid-up ₹17.41 crore, FY2025 revenue ₹80.41 crore, net profit ₹1.06 crore, 338 EPFO employees; directors from the Dudhwewala family plus Sanket Singhania, Dewang Madhukar Modi and Vishrut Chandramauli Pathak (2024). — https://www.thecompanycheck.com/company/salud-care-india-limited/U24239WB2003PTC097481 (page resolves to the Gujarat CIN).
4. WHO-GMP / COPP: CDSCO list up to 31-Dec-2025 (released 17-Jun-2026; server filename "Testing Laboratories approved by States & UT in Form 37.pdf" is misleading, the content is the WHO-GMP list, 372 pp.): Gujarat #1666 Bueno Salud Care (India) Pvt Ltd, K-20/21 — General (tablets, capsules, oral liquids, externals) and Beta-lactam & Cephalosporin (tablets, capsules, dry syrup, SVP dry-powder injections); WHO GMP COPP validity 26-Jan-2029. Loan-licensees at the same plot with the same validity: Seraga Lifesciences, Ahaan Healthcare, Niya Health Care, Swiss Parenterals. Earlier list (Jan-2023–Mar-2024): Bueno #534 with Deutsche Labs, Swiss Parenterals, Saga Lifesciences and Ocean Pharmaceutical as loan-licensees. Dec-2022 list: Bueno not listed; Salud Care (I) Pvt Ltd, Roorkee, listed (Uttarakhand #87). — https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadIndustryCommon/Testing%20Laboratories%20approved%20by%20Statas%20%26%20UT%20in%20Form%2037.pdf ; https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadIndustryCommon/Final%20WHO%20GMP%20data%20for%20website%2011.09.2025.pdf ; https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadIndustryCommon/22WHO%20GMP%20CoPP%20units.pdf
5. CDSCO NSQ alerts after June 2025 moved to a portal (notice of 28-Aug-2025). Portal data Jul-2025 to Aug-2026 downloaded (Sep-2026 not yet published on 2026-10-07): zero rows for Bueno, Lorisol, Edmax, Zywie or Vapi. Two rows for the Roorkee plant (Salud Care (India) Ltd / Salud Care (I) Pvt Ltd, Plot 435 Kishanpur): Aug-2025 amlodipine + atenolol (assay) and May-2026 calcium/D3/methylcobalamin/L-methylfolate/P5P (assay). Caveat: several states show "pending submission" in most months (Gujarat pending Jul–Oct 2025), so state-lab coverage is incomplete. — https://cdscoonline.gov.in/CDSCO/viewPublicNSQDrug
6. Bueno website (about-us, 2026-10-07) lists as management Sandip Bhargav, Shiv Kumar Dudhewala, Deepti Patel (RA/QA), Abhinav Bhargav (BD) and Kailesh Desai (operations); brochure milestones: 2016 incorporation, 2018 Ahmedabad plant, 2019 "WHO certificate", registrations claimed in Cambodia, Kenya, Philippines, Yemen, Afghanistan; "expected" NAFDAC, NMRA Sri Lanka, NDA Uganda. The "Annual Return" link is still a one-page blank PDF (21-Aug-2026). — https://buenosalud.in/about-us/ ; https://buenosalud.in/wp-content/uploads/2025/01/BUENO-BROCHURE.pdf
7. Registries searched for Bueno / Salud Care / Zywie, with zero hits: Ecuador ARCSA (four public exports, manufacturer column), Colombia INVIMA (datos.gov.co datasets updated 2026-09-16; titular and nombrerol), Paraguay DINAVISA (48,662 records; holder only, manufacturer not searchable), Tanzania TMDA (5,723 human-medicine rows), Sri Lanka NMRA (xls of 01-Oct-2026, manufacturer column), Nigeria NAFDAC Greenbook (applicant/product, not manufacturer), Ghana FDA foreign-facility list as at 28-Feb-2025 (not listed), Panama DNFD substandard lists 2025–2026 and sanitary alerts (no mention). — https://aplicaciones.arcsa.gob.ec/publico/consultas/index ; https://www.datos.gov.co/ ; https://dnvspy.mspbs.gov.py/dnvspy/reportes_publicos/consulta_publica_rs/consulta-publica-rs.html ; https://imis2.tmda.go.tz/portal/#/public/registered-medicines ; https://nmra.gov.lk/ ; https://greenbook.nafdac.gov.ng/ ; https://fdaghana.gov.gh/list-of-foreign-pharmaceutical-manufacturing-facilities-with-valid-licenses-as-at-28-feb-25 ; https://dnfd.minsa.gob.pa/medicamentos-subestandar
8. Zywie on IndiaMART (mobile page, 2026-10-07): GST 24AACFZ1221A1ZY; "Exporter & Retailer of Basmati Rice, Frozen Vegetables & Pharmaceutical Tablets"; service "Merchant Exports"; contact Rutul Divyakant Patel (Director); Vapi. No date for when the pharmaceutical line was added. — https://m.indiamart.com/zywie-worldwide/
9. No CDSCO public notice (818 notices to 06-Oct-2026), Philippine FDA advisory or Kenya PPB notice names Bueno, Salud Care or Zywie.

### D2. Still not verified or not accessible
- Gujarat FDCA manufacturing licences by block (site unreachable); shipment databases (Volza, Seair, Trademo, Eximpedia: blocked or paywalled); DGFT IEC status (captcha); litigation (Indian Kanoon excluded, NCLT not searched); Bueno's shareholders and audited accounts (paywalled MCA documents); registries of Costa Rica, Guatemala (no manufacturer field), Honduras, Dominican Republic (captcha), Peru, Bolivia, Nicaragua, Uganda, Nepal, Cambodia, Yemen, Myanmar (no public register or not accessible); Kenya PPB (register shows holders, not manufacturers).
- Family link between Deepti Rutul Patel and Rutul Divyakant Patel: naming convention only; director pages for her returned 403/404.
"""


def apply_post3(name, md):
    for old, new, must in GLOBAL:
        if name == must:
            assert old in md, f'{name}: no se encontró el anclaje común «{old[:90]}»'
        md = md.replace(old, new)
    md = md.replace('compuerta 2 (operativa) (operativa)', 'compuerta 2 (operativa)').replace('Compuerta 2 (operativa) (operativa)', 'Compuerta 2 (operativa)')

    if name == '00_Resumen_y_plan.md':
        # tabla de archivos: vive en LEAME; aquí solo el orden de lectura por papel
        i = md.index('## Cómo leer este paquete')
        j = md.index('## Veredicto')
        md = md[:i] + """## Cómo leer este paquete

La tabla completa de archivos, con qué contiene cada uno y dónde vive, está en LEAME.md. Orden de lectura según el papel:

| Si usted… | Lea |
| --- | --- |
| Decide si entra o no | Este documento, el Resumen_ejecutivo_socios_inversionistas.md y 03_Costos_capital_y_proyeccion.md (capital y riesgo) |
| Va a hablar con Rutul Patel | 06_Guion_conversacion_Rutul.md y 01_Investigacion_Rutul_y_fabricante.md |
| Va a cerrar cotizaciones | 04_Logistica_y_operacion.md y Cotizaciones_3PL_seguimiento.md |
| Va a defender los números | 07_Auditoria_y_confianza.md y el modelo (Modelo_financiero_socios.xlsx) |

Regla de uso: los documentos 00 a 07, el seguimiento de cotizaciones y el modelo son para los tres socios panameños. A Rutul solo van la hoja de datos y, más adelante, el acuerdo de confidencialidad y la propuesta de términos (detalle en «Qué se comparte y con quién», al final).

""" + md[j:]
        md = _rep(md, '| 7 de octubre de 2026 | Primera ola: los 11 productos sin equivalencia terapéutica; a Rutul se le pide como socios, sin revelar lo investigado; la propuesta de términos la escribimos nosotros; los documentos van a los socios panameños, no a Rutul |',
                  '| 7 de octubre de 2026 | Primera ola: los 11 productos sin equivalencia terapéutica; a Rutul se le pide como socios, sin revelar lo investigado; la propuesta de términos la escribimos nosotros; los documentos van a los socios panameños, no a Rutul |\n| 8 de octubre de 2026 | Markdown como formato único del paquete; auditoría de cifras y fuentes (07); solicitudes de cotización indicativa a cuatro operadores logísticos |\n| 9 de octubre de 2026 | Ninguna comunicación externa (correo, formulario, mensaje) sale sin que Jaime apruebe el texto y entienda los números; J. Cain propone videollamada el 14 de octubre; el cuestionario de BP Logistics sale del paquete para Rutul; lista de cifras no obtenidas en 07 |', name)

    elif name == '05_Trato_socios_y_hoja_de_ruta.md':
        pass

    elif name == 'LEAME.md':
        md = _rep(md, '*Versión del 8 de octubre de 2026.', '*Versión del 9 de octubre de 2026.', name)
        md = re.sub(r'^(\| 8 de octubre de 2026, noche \|.*)$', r'\1\n| 9 de octubre de 2026 | Cuarta pasada de auditoría: coherencia entre documentos, cifras redondeadas, referencias cruzadas y afirmaciones sin fuente; lista de cifras no obtenidas (07); reparto por estructura y sensibilidad de las cremas reproducibles en el análisis del modelo; el cuestionario de BP Logistics sale del paquete para Rutul; respuesta de J. Cain registrada; regla: ninguna comunicación externa sin aprobación de Jaime |', md, count=1, flags=re.M)
        assert '| 9 de octubre de 2026 | Cuarta pasada' in md, name

    elif name == 'Resumen_ejecutivo_socios_inversionistas.md':
        md = _rep(md, '*8 de octubre de 2026. Las cifras salen del modelo financiero de 60 meses y de la auditoría del 8 de octubre (07_Auditoria_y_confianza.md).', '*9 de octubre de 2026. Las cifras salen del modelo financiero de 60 meses y de las auditorías del 8 y del 9 de octubre (07_Auditoria_y_confianza.md).', name)
        md = _rep(md, '**B/.121 mil** en el caso de planificación (de B/.48 mil a B/.184 mil según el escenario)',
                  '**B/.121 mil** en el caso de planificación, que es el caso base con las tarifas legales de SignatureLex (de B/.48 mil a B/.184 mil según el escenario)', name)
        md = _rep(md, '**B/.297 mil** en el mes 27, caso de planificación (de B/.184 mil a B/.321 mil)',
                  '**B/.297 mil** en el mes 27, caso de planificación (B/.184 mil en el optimista; en el pesimista B/.321 mil al mes 27 y, si nadie cierra, B/.599 mil al mes 60; con la compuerta 2, B/.284 mil)', name)
        md = _rep(md, 'frente al trato con las condiciones de la compuerta 0 |',
                  'frente al trato reestructurado con la fábrica financiando (15% si además se aplica el tope de precio de la compuerta 0) |', name)
        md = _rep(md, 'La primera ola son 11 productos que no requieren estudios de bioequivalencia en Panamá (paracetamol en tableta y jarabe, amoxicilina con clavulánico, ceftriaxona,',
                  'La primera ola son 11 productos que no requieren estudios de bioequivalencia en Panamá (Resolución 985 de 2025): paracetamol en tableta y jarabe, amoxicilina con clavulánico en tableta y en suspensión, ceftriaxona,', name)
        md = _rep(md, 'nistatina, hidrocortisona y mometasona). Solo la CSS presupuesta unos B/.230 millones de medicamentos para 2027;',
                  'nistatina, hidrocortisona y mometasona. Solo la CSS presupuesta unos B/.230 millones de medicamentos para 2027 (fuentes en 02);', name)
        md = _rep(md, 'plazo legal de 4 a 5 meses, real de 5 a 9', 'plazo legal de 4 a 5 meses (Ley 419, arts. 41 y 74: 60 más 20 días hábiles), real de 5 a 9', name)
        md = _rep(md, 'con fianza de 30% del contrato)', 'con fianza de 30% del contrato, según el pliego de la LPU 01-2026)', name)
        md = _rep(md, 'el Estado paga a 90 días desde la cuenta;', 'el Estado paga a 90 días desde la cuenta (pliegos);', name)
        md = _rep(md, 'y devuelve 6.8% anual en el caso base, por debajo del 15% mínimo. Con tres condiciones (precio de fábrica a libro abierto hasta 1.1 veces la referencia, la fábrica paga o acredita los registros, y 150–180 días de crédito) la probabilidad de pérdida baja a 29%; si además un socio opera sin sueldo, a 18%, y el valor esperado al 15% pasa a positivo.',
                  'y devuelve 6.8% anual en el caso base, por debajo del 15% mínimo que usa este informe (el modelo descuenta al 30%, la tasa de una pyme nueva: VPN de −B/.107 mil). Con el trato reestructurado y la fábrica financiando (precio de fábrica a libro abierto, registros pagados o acreditados por la fábrica, 150–180 días de crédito y seis productos del sistema nervioso con fabricante verificado) la probabilidad de perder más que la fase 0 baja a 29% (18% si además un socio opera sin sueldo, y entonces el valor esperado al 15% pasa a positivo); aplicando también el tope de precio de 1.1 veces de la compuerta 0, la mitad de los escenarios se detiene en la fase 0 y la probabilidad baja a 15%.', name)
        md = _rep(md, '| Fábrica financia y Patel pone 70% del efectivo | 17% |', '| Fábrica financia y Patel pone 70% del efectivo (probabilidad para el socio panameño; la del negocio sigue en 29%) | 17% |', name)
        md = _rep(md, 'Lo que más pesa, en orden: los costos fijos antes de vender (unos B/.4,700 al mes durante 9 meses sin ingresos), la probabilidad de ganar renglones, el colateral de las fianzas y los 150 días de cobro, el margen del intermediario y el riesgo de un problema de planta. Las tres primeras causas se atacan con dinero del otro lado (crédito y registros pagados por la fábrica) y con trabajo propio (un socio operando); la cuarta con precio a libro abierto; la quinta con la auditoría de planta de la fase 0.',
                  'Lo que más pesa: sobre el valor esperado, los costos fijos antes de vender (unos B/.33 mil acumulados hasta la primera venta y B/.4,700 al mes en madurez), la probabilidad de ganar renglones y la participación en compras menores, la erosión de precios y el margen del intermediario; sobre el capital, el colateral de las fianzas y los 150 días de cobro; y, en la simulación, el riesgo de un problema de planta. Los costos fijos y el capital se atacan con dinero del otro lado (crédito y registros pagados por la fábrica) y con trabajo propio (un socio operando); el margen del intermediario, con precio a libro abierto; el riesgo de planta, con la auditoría de la fase 0; la tasa de victoria solo se conoce compitiendo.', name)
        md = _rep(md, '| Tramo 1: empresa y registros | B/.71 mil / B/.102 mil |', '| Tramo 1: empresa y registros | B/.68 mil / B/.99 mil |', name)
        md = _rep(md, 'Compuerta 0: precio hasta 1.1 veces la referencia, fábrica paga o acredita registros, crédito de 150–180 días, documentos completos |',
                  'Compuerta 0 (definida en 00): precio hasta 1.1 veces la referencia, fábrica paga o acredita registros, crédito de 150 días o más, planta y fabricante del sistema nervioso verificados, documentos completos |', name)
        md = _rep(md, 'Hasta la primera venta: B/.20 mil / B/.20 mil.', 'Hasta la primera venta: B/.19 mil / B/.19 mil.', name)
        md = _rep(md, '| Compuerta 1: registros aprobados y cotizaciones firmes dentro del presupuesto |', '| Compuerta 1 (definida en 00): 8 o más registros aprobados, contrato con el 3PL, regente y Registro de Oferentes |', name)
        md = _rep(md, '| Seis productos más (sistema nervioso), si el fabricante se verifica | Compuerta 2: ventas anualizadas de al menos B/.90 mil nueve meses después de la primera venta |',
                  '| Ampliación con seis productos del sistema nervioso si su fabricante se verifica (la segunda ola genérica del mes 18 ya está en el caso base) | Compuerta 2 (definida en 00): ventas anualizadas de al menos B/.90 mil nueve meses después de la primera venta y menos de 30% de ofertas descalificadas |', name)

    elif name == '01_Investigacion_Rutul_y_fabricante.md':
        md = _rep(md, 'consultados entre el 5 y el 7 de octubre de 2026:', 'consultados entre el 5 y el 8 de octubre de 2026:', name)
        md = _rep(md, 'Lo que no se pudo verificar se dice así.', 'Lo que no se pudo verificar se dice así. Modi Life Care Industries (Ahmedabad) se revisó porque su catálogo llegó con los materiales de Rutul como posible segunda fuente.', name)
        md = _rep(md, ' Sobre la junta de Bueno los espejos del registro mercantil no coinciden: Falconebiz y AllIndiaITR listan a Deepti Rutul Patel como directora desde julio o septiembre de 2024 y a Abhinav Bhargava desde marzo o abril de 2024; Zauba y Tracxn, cuyos datos parecen anteriores a esa fecha (última junta anual registrada: septiembre de 2023), muestran solo a Shivkumar Dudhwewala y a Bhargava. Por eso',
                  '\n\nSobre la junta de Bueno, los espejos del registro mercantil no coinciden entre sí: Falconebiz (actualizado el 2 de septiembre de 2026) y The Company Check (21 de septiembre de 2026) listan tres directores, Shivkumar Dudhwewala, Abhinav Bhargava (desde marzo o abril de 2024, regularizado a finales de septiembre de 2024) y Deepti Rutul Patel (desde julio o septiembre de 2024, según el espejo); Tofler (última junta anual registrada: septiembre de 2023) y Zauba (datos hasta 2024) no la muestran. Por eso', name)
        md = _rep(md, 'Su certificado OMS-BPM está vigente hasta enero de 2029 en la lista de la CDSCO y no tiene alertas nuevas desde entonces; vendió unos ₹102 crore (US$12 millones) en el año fiscal 2025 con pérdida neta y deuda del orden de sus ventas.',
                  'Su certificado OMS-BPM está vigente hasta enero de 2029 en la lista de la CDSCO y el portal de alertas no muestra ninguna nueva entre julio de 2025 y agosto de 2026 (con cobertura estatal incompleta); vendió unos ₹102 crore (unos US$12 millones a ₹85 por dólar) en el año fiscal 2025 con pérdida neta y gravámenes registrados del orden de sus ventas; la deuda viva no se conoce sin los estados auditados.', name)
        md = _rep(md, 'Deepti Rutul Patel (nombrada en julio o septiembre de 2024 según Falconebiz y AllIndiaITR; Zauba y Tracxn, cuyos datos parecen anteriores a esa fecha, no la muestran: estado por confirmar con el formulario DIR-12)',
                  'Deepti Rutul Patel (desde julio o septiembre de 2024 según Falconebiz y The Company Check; Tofler y Zauba, con datos anteriores, no la muestran: estado por confirmar con el formulario DIR-12)', name)
        md = _rep(md, '| Amarilla: fabricante real, no revelado |', '| Amarilla: fabricante probable, no revelado |', name)
        md = _rep(md, 'sin alertas nuevas de la CDSCO entre julio de 2025 y agosto de 2026 | Verde |', 'sin alertas nuevas de la CDSCO entre julio de 2025 y agosto de 2026 (portal con cobertura estatal incompleta: varios estados con envíos pendientes) | Verde |', name)
        md = _rep(md, '252 empleados en planilla (249 según Tracxn) y deuda garantizada por ₹104 crore, según los espejos comerciales del registro (The Company Check, Zauba), que venden el informe completo; sin contrastar con estados auditados.',
                  '252 empleados en planilla y gravámenes registrados por ₹104 crore (cupo garantizado, no deuda viva), según el espejo comercial The Company Check, que vende el informe completo; sin contrastar con estados auditados.', name)
        md = _rep(md, 'la planta del grupo en Roorkee (Salud Care India Ltd) tuvo alertas en agosto de 2025 y mayo de 2026 y su certificado venció en agosto de 2026',
                  'la planta del grupo en Roorkee (Salud Care (India) Pvt Ltd) tuvo alertas en febrero de 2017, junio de 2022, julio de 2024, agosto de 2025 y mayo de 2026, y su certificado OMS-BPM figura vigente hasta el 23 de agosto de 2026 en la lista al 31 de diciembre de 2025 (renovación por confirmar)', name)
        md = _rep(md, 'tampoco aparece como fabricante en los registros públicos de Ecuador, Colombia, Paraguay, Tanzania, Sri Lanka, Ghana ni Nigeria,',
                  'tampoco aparece como fabricante en los registros públicos de Ecuador, Colombia, Tanzania y Sri Lanka, ni como titular o solicitante en Paraguay y Nigeria, ni en la lista de plantas extranjeras de Ghana (28 de febrero de 2025),', name)
        md = _rep(md, 'vegetales congelados y, desde 2026, tabletas farmacéuticas;', 'vegetales congelados y tabletas farmacéuticas (sin fecha de alta visible);', name)
        md = _rep(md, 'vegetales congelados y, desde 2026, de tabletas farmacéuticas;', 'vegetales congelados y de tabletas farmacéuticas (sin fecha de alta visible);', name)
        md = _rep(md, 'tampoco aparece como fabricante en INVIMA ni en los registros de Ecuador, Paraguay, Tanzania, Sri Lanka, Ghana o Nigeria;',
                  'tampoco aparece como fabricante en INVIMA ni en los registros de Ecuador, Tanzania y Sri Lanka, ni como titular en Paraguay y Nigeria, ni en la lista de plantas extranjeras de Ghana;', name)
        md = _rep(md, '| Neutral: no han vendido al Estado panameño | PanamaCompra |', '| Neutral: no han vendido al Estado panameño | Cuadros de propuestas de PanamaCompra 2023–2026 revisados en 02 |', name)
        md = _rep(md, 'el anexo en inglés (Anexo_DD_hallazgos_en.md) trae la lista completa de páginas abiertas, con fecha.',
                  'el anexo en inglés (Anexo_DD_hallazgos_en.md) trae la primera ronda (6 de octubre) y un addendum con la segunda (7 y 8 de octubre), con cada enlace y su fecha.', name)

    elif name == '06_Guion_conversacion_Rutul.md':
        md = _rep(md, '## Mensaje de apertura\n', '## Mensaje de apertura (paso 1)\n', name)
        md = _rep(md, 'Seis burbujas, en inglés, seguidas, en el grupo. Adjuntos: en la segunda, el cuestionario en blanco del 3PL (3PL_questionnaire_blank_EN.xlsx) para que vea qué piden; en la tercera, la hoja de datos de fábrica (Factory_data_for_3PL_quote.xlsx). Tono casual pero profesional; sin nombres de operadores ni cifras internas; nada que suene a redacción automática. Solo tres pedidos esta noche: la hoja de datos, el paquete del proveedor y su correo electrónico (Jaime no lo tiene).',
                  'Cinco burbujas seguidas, en inglés, en el grupo (1, 2, 3, 5 y 6); la cuarta solo si pregunta por costos, y un bloque de respaldo si pregunta de dónde salen los números. Adjunto: en la tercera, la hoja de datos de fábrica (Factory_data_for_3PL_quote.xlsx). Tono casual pero profesional; sin nombres de operadores ni cifras internas; nada que suene a redacción automática. Solo tres pedidos en la apertura: la hoja de datos, el paquete del proveedor y su correo electrónico (Jaime no lo tiene).', name)
        md = _rep(md, 'Burbuja 2 (con el cuestionario del 3PL en blanco):', 'Burbuja 2:', name)
        md = _rep(md, 'We gave them estimates and that didn\'t fly. Attaching the form one of them sent us so you can see what they ask for.',
                  'We gave them estimates and that didn\'t fly; it\'s the standard list any 3PL asks for, and the sheet in the next message covers it.', name)
        md = _rep(md, 'Si ya mandó la versión anterior de esta burbuja y él pregunta de dónde salen los números:', 'Respaldo, si pregunta de dónde salen los números:', name)
        md = _rep(md, 'Rutul dice que Bueno vende en El Salvador y Colombia.', 'Rutul dice que la fábrica vende en El Salvador y Colombia.', name)
        md = _rep(md, '(el expediente en formato CTD de la OMS)', '(el expediente en formato CTD de la ICH, el que usan la OMS y la mayoría de las agencias)', name)
        md = _rep(md, '| Certificado OMS-BPM (COPP) de la planta y licencia de fabricación por bloque |', '| Certificado OMS-BPM de la planta (la CDSCO publica la lista «WHO GMP/COPP»; el CPP es por producto) y licencia de fabricación por bloque |', name)
        md = _rep(md, 'se pide el desglose (paso 7).', 'se pide el desglose (paso 8).', name)
        md = _rep(md, 'All-in it\'s about B/.2,000 per product, 11 products, and the legal deadlines alone add up to 4-5 months.',
                  'Our estimate is about B/.2,100 per product all-in (the official fee is B/.500; the lab analysis and the filing are quotes), 11 products, and the legal deadlines alone add up to 4-5 months.', name)
        md = _rep(md, 'any regulatory alerts, not-of-standard-quality findings or recalls on these products in the last three years, and if so the root cause and the corrective action. The DNFD cross-checks the Indian regulator\'s lists, so it\'s better to have it in the file than to be asked later.',
                  'any regulatory alerts, failed official quality tests or recalls on these products in the last three years, and if so the root cause and the corrective action. Regulators here can see the Indian regulator\'s public lists, so it\'s better to have it in the file than to be asked later.', name)
        md = _rep(md, '| La DNFD revisa las listas de la CDSCO; el expediente lo pide |', '| Las listas de la CDSCO son públicas y la DNFD puede verlas; el cuestionario va al expediente |', name)
        md = _rep(md, 'On El Salvador, can you share the registration numbers or the distributor there? Pointing at an existing Central American registration helps a lot with the Panamanian registry.',
                  'On El Salvador and Colombia, can you share the registration numbers or the distributor there? A Colombian (INVIMA) registration would matter most: Panama treats INVIMA as a reference authority, which opens a shorter registration route.', name)
        md = _rep(md, '| Nuestra debida diligencia; ayuda ante la DNFD |', '| Nuestra debida diligencia; un registro en Colombia (INVIMA es autoridad de referencia reconocida por Panamá) abriría la ruta abreviada; El Salvador solo vale como referencia comercial |', name)
        md = _rep(md, '(cerró 2025 con pérdida neta y deuda del tamaño de sus ventas, según los espejos del registro mercantil indio)', '(cerró el año fiscal 2025 con pérdida neta y gravámenes registrados del tamaño de sus ventas, según los espejos del registro mercantil indio)', name)
        md = _rep(md, 'cerró 2025 con pérdida y deuda del tamaño de sus ventas |', 'cerró el año fiscal 2025 con pérdida y gravámenes registrados del tamaño de sus ventas |', name)
        md = _rep(md, 'When you first spoke with my father and Juan Luis, the understanding was', 'When this started, the understanding was', name)
        md = _rep(md, 'get two surety quotes, regente and accountant quotes,', 'get two surety quotes, pharmacist-in-charge (regente) and accountant quotes,', name)
        md = _rep(md, 'the DNFD will see the same list we saw.', 'the DNFD can see the same public list.', name)
        md = _rep(md, '- Nada del parentesco con el ministro ni de contactos en el Gobierno. El plan se sostiene por precio y cumplimiento; la declaración ante la ANTAI (Ley 316) lo hará público a su debido tiempo y con abogado.',
                  '- Nada del parentesco con el ministro ni de contactos en el Gobierno como argumento comercial: el plan se sostiene por precio y cumplimiento. El dato se informa por escrito en la propuesta de términos (la S.A. estará sujeta a la declaración de la Ley 316 ante la ANTAI), no en el chat.', name)
        # columna «Paso del guion» en la tabla Qué queremos y numeración única en el seguimiento
        paso = {'1': '1 (apertura)', '2': '2', '3': '3', '4': '4', '5': '5', '6': '7', '7': '8', '8': '6', '9': '6', '10': 'Hoja de datos (Per shipment, fila 13)'}
        md = _rep(md, '| # | Pedido | Quién lo exige | Qué decide |\n| --- | --- | --- | --- |', '| # | Pedido | Paso del guion | Quién lo exige | Qué decide |\n| --- | --- | --- | --- | --- |', name)
        lines = md.split('\n'); out = []; in_q = False
        for ln in lines:
            if ln.startswith('## Qué queremos'): in_q = True
            elif ln.startswith('## ') and in_q: in_q = False
            if in_q:
                m = re.match(r'^\| (\d+) \| ', ln)
                if m and m.group(1) in paso:
                    cells = ln.split(' | ')
                    cells.insert(2, paso[m.group(1)])
                    ln = ' | '.join(cells)
            out.append(ln)
        md = '\n'.join(out)
        md = _rep(md, '| 6 | Accionistas, estados auditados, El Salvador y dos referencias | Francisco | — | — | — | Por pedir |\n| 7 | Crédito de 150–180 días sin anticipo | Jaime | — | — | — | Por pedir |\n| 8 | Quién factura y margen de Zywie a libro abierto | Francisco | — | — | — | Por pedir |\n| 9 | Empaque impreso con el número de licitación en corridas pequeñas | Jaime | — | — | — | Por pedir |\n| 10 | Propuesta de términos de una página (la mandamos nosotros) | Francisco y Jaime | — | — | — | Por pedir |',
                  '| 6 | Crédito de 150–180 días sin anticipo (paso 7) | Jaime | — | — | — | Por pedir |\n| 7 | Quién factura y margen de Zywie a libro abierto (paso 8) | Francisco | — | — | — | Por pedir |\n| 8 | Accionistas y estados auditados (paso 6) | Francisco | — | — | — | Por pedir |\n| 9 | Prueba de El Salvador y Colombia y dos referencias (paso 6) | Francisco | — | — | — | Por pedir |\n| 10 | Empaque impreso con el número de licitación en corridas pequeñas (hoja de datos) | Jaime | — | — | — | Por pedir |\n| 11 | Propuesta de términos de una página (la mandamos nosotros) | Francisco y Jaime | — | — | — | Por pedir |', name)
        md = _rep(md, '| 1 | Packing list y ficha técnica por producto | Jaime | — | — | — | Por pedir |', '| 1 | Packing list y ficha técnica por producto (paso 1, apertura) | Jaime | — | — | — | Por pedir |', name)

    elif name == '02_Mercado_requisitos_y_competencia.md':
        md = _rep(md, '| 15% sobre el precio de fábrica en la propuesta; el plan pide 5% o menos a libro abierto |', '| 15% sobre el precio de fábrica (estimación: Zywie no ha abierto su margen); el plan pide 5% o menos a libro abierto |', name)
        md = _rep(md, '33 subastas de un solo producto entre junio y el 6 de octubre de 2026, 28 adjudicadas; las primeras 19 sumaron B/.5.8 millones',
                  '33 procesos de subasta de un solo producto (19 de medicamentos, el resto insumos) publicados desde abril de 2026, con pujas entre mayo y junio; 26 adjudicados al 7 de octubre por unos B/.6.3 millones frente a B/.8.2 millones de referencia (conteo propio de los informes de cada subasta)', name)
        md = _rep(md, '| Adjudicada el 31 de agosto de 2026 | Fuera de nuestro catálogo |', '| Adjudicada el 31 de agosto de 2026 | Fuera de la primera ola: exige equivalencia terapéutica o licencia de controlados (26 coincidencias con el catálogo de Zywie y Modi) |', name)
        md = _rep(md, 'se comparan en la sección siguiente; ninguno cambia el veredicto de la fase 0.', 'se comparan en la sección siguiente.', name)
        md = _rep(md, '| Cientos de actos al año (conteo propio 2025–2026) |', '| Miles de actos al año (conteo propio 2025–2026: unas 3,300 contrataciones menores y 270 compras ágiles de medicamentos en 2026) |', name)
        md = _rep(md, 'No en la primera fase: una marca desconocida solo entra por una droguería', 'No en la primera fase. Estimación propia, sin fuente externa: una marca desconocida solo entra por una droguería', name)
        md = _rep(md, 'con más de 10 importaciones al año, el registro ordinario;', 'con más de 10 importaciones al año, el registro ordinario (regla por confirmar en el texto de la ley);', name)

    elif name == '03_Costos_capital_y_proyeccion.md':
        pass

    elif name == '04_Logistica_y_operacion.md':
        md = _rep(md, 'Estado de las cotizaciones: las dos solicitudes anteriores no prosperaron porque fueron con estimaciones y sin fichas. El 8 de octubre de 2026 se enviaron solicitudes de cotización indicativa, o de tarifario estándar, a los cuatro operadores con correo público (J. Cain, Osala, DSV e Interworld); BP Logistics y DHL solo reciben por formulario web y Farmazona por WhatsApp.',
                  'Estado de las cotizaciones: antes del 8 de octubre solo se había intercambiado el cuestionario operativo de BP Logistics, lleno con estimaciones y sin fichas de producto, sin llegar a una cotización. El 8 de octubre de 2026 se enviaron solicitudes de cotización indicativa, o de tarifario estándar, a los cuatro operadores con correo público (J. Cain, Osala, DSV e Interworld); J. Cain respondió el 9 de octubre proponiendo una videollamada para el 14. BP Logistics recibe por formulario web o WhatsApp, DHL solo por formulario web y Farmazona por WhatsApp.', name)
        md = _rep(md, '| J. Cain & Cía | Zona Libre de Colón y Panamá Pacífico | Licencias MINSA 3-009 L y 13-001 LA;', '| J. Cain & Cía | Zona Libre de Colón y Panamá Pacífico | Licencias de agencia 13-005 A (Panamá Pacífico) y 3-001 (Colón); licencias MINSA 3-009 L y 13-001 LA;', name)
        md = _rep(md, '| 24 | Correo enviado |', '| 24 | Correo enviado; respondió el 9 de octubre: videollamada propuesta para el 14 |', name)
        md = _rep(md, '| BP Logistics (Grupo Hilasal) | Panamá Pacífico | Licencia MINSA 13-006 LA;', '| BP Logistics (Grupo Hilasal) | Panamá Pacífico | Licencia de agencia 13-031 A (vence el 16 de diciembre de 2026); licencia MINSA 13-006 LA;', name)
        md = _rep(md, 'ya recibió el cuestionario anterior |', 'ya recibió nuestro cuestionario operativo con estimaciones |', name)
        md = _rep(md, 'certificado BPM de acondicionamiento 015-24 a agosto de 2026 | 16 |', 'certificado BPM de acondicionamiento 015-24 a agosto de 2026 (vencido en la lista; confirmar renovación) | 16 |', name)
        md = _rep(md, '| Grupo TLA | Panamá Pacífico | Aloja a Vanguard Medical Logistics (Promed), licencia 13-012 LA; sin licencia propia visible |', '| Grupo TLA | Panamá Pacífico | Licencias propias 13-000 y 13-132 (lista de la DNFD, 28 de septiembre de 2026); aloja a Vanguard Medical Logistics (Promed), licencia 13-012 LA |', name)
        md = _rep(md, 'CEIV Pharma (los dos últimos) | — | Segunda ronda', 'CEIV Pharma (los dos últimos) | 7 y 4 (los dos primeros) | Segunda ronda', name)
        md = _rep(md, 'Nota: las listas públicas de la DNFD que se pudieron abrir son las de laboratorios acondicionadores con certificado de BPM y la de establecimientos con licencia; la licencia de almacén o de agencia es otra categoría sin lista pública consolidada. Que un operador no aparezca no significa que no tenga licencia de almacenamiento: por eso el correo pide el número de licencia.',
                  'Nota: la lista de establecimientos con licencia de la DNFD (28 de septiembre de 2026) incluye las licencias de agencia de los propios operadores (J. Cain Panamá Pacífico 13-005 A y J. Cain & Co. 3-001; BP Logistics 13-031 A, que vence el 16 de diciembre de 2026; Grupo TLA 13-000 y 13-132); las licencias «L» y «LA» de la tabla vienen de la lista de laboratorios acondicionadores con certificado de BPM. Que un operador no aparezca en una lista no significa que no tenga licencia de almacenamiento: por eso el correo pide el número de licencia.', name)
        md = _rep(md, 'El cuestionario que mandó el 3PL (3PL_questionnaire_blank_EN.xlsx, versión en inglés y en blanco) pide pesos, dimensiones, volumen, valor por embarque, sensibilidad, control por lote, fichas técnicas y fotos: casi todo depende de la fábrica. Por eso la hoja',
                  'El cuestionario operativo de BP Logistics pide pesos, dimensiones, volumen, valor por embarque, sensibilidad, control por lote, fichas técnicas y fotos: casi todo depende de la fábrica (por ser un formulario con la marca de ese operador, no se le manda a Rutul).\n\nPor eso la hoja', name)
        md = _rep(md, 'Volumen físico de los 11 productos en madurez (caso base): unos 74 m³ y 38 tarimas al año.', 'Volumen físico de los 11 productos en madurez (caso base): unos 74 m³ y 38 tarimas al año, es decir, unas 3 tarimas al mes (un contenedor de 20 pies lleva 10).', name)
        md = _rep(md, 'El lote económico es de unos 19 m³ por embarque (4 al año), justo un contenedor de 20 pies,', 'El lote económico (calculado con un costo fijo de US$1,000 por embarque, 15% anual de costo de tenencia más almacenamiento y 3% de merma) es de unos 19 m³ por embarque (4 al año), justo un contenedor de 20 pies,', name)
        md = _rep(md, 'Cálculo: vida útil − 18 meses exigidos − 1 mes de liberación en fábrica − 2 meses de tránsito y aduana − 0.25 meses de pedido a entrega.',
                  'Cálculo: vida útil − 18 meses exigidos − 1 mes de liberación en fábrica − 2 meses de tránsito y aduana − 0.25 meses de pedido a entrega. Regla de la columna «Política de reposición»: la permanencia máxima en bodega debe cubrir el intervalo entre embarques más la cobertura de inventario; con 24 meses solo cabe un embarque mensual con 1.5 meses de cobertura; con 30, uno cada dos meses con los 3 meses de cobertura del caso base; con 36, uno trimestral en contenedor.', name)
        md = _rep(md, 'el del MINSA pide «Propiedad del MINSA/Panamá».', 'el del MINSA exige el rotulado de propiedad del MINSA.', name)
        md = _rep(md, '(la comparación está en la estimación logística, más abajo)', '(la comparación está en la sección «Estimación de costos logísticos»)', name)
        md = _rep(md, '| Almacenamiento y manejo en un 3PL licenciado: 5–10 tarimas,', '| Almacenamiento y manejo en un 3PL licenciado: 5–15 tarimas,', name)
        md = _rep(md, 'US$275 por contenedor seco (US$295 refrigerado) desde el 15 de octubre de 2026', 'US$275 por contenedor seco desde el 15 de octubre de 2026', name)
        md = _rep(md, '| Carga consolidada (LCL), unos 9 m³ por embarque al inicio | US$200 por m³ de flete más unos US$100 de desconsolidación y destino (el modelo usa US$300 por m³ puesto en bodega) | **Referencia indirecta** | Desconsolidación US$86.5 por m³ en el tarifario de destino de Crowley Panamá; el flete por m³ es un supuesto derivado de la tarifa FAK por contenedor |',
                  '| Carga consolidada (LCL), unos 10 m³ por embarque al inicio | US$200 por m³ de flete más unos US$100 de desconsolidación, destino y entrega local (el modelo usa US$300 por m³ puesto en bodega) | **Referencia indirecta** | Desconsolidación US$0.20 por pie cúbico (mínimo US$55 por embarque) en el tarifario de destino de Crowley Panamá; una cotización privada de 2025 cobra US$86.5 por m³; el flete por m³ es un supuesto derivado de la tarifa FAK por contenedor y de referencias LCL India–EE. UU. y Europa (US$65–160 por m³) |', name)
        md = _rep(md, '| Seguro de carga | 0.3–0.5% del valor CIF; el modelo usa B/.100 al mes | **Supuesto** | Práctica de mercado; cotizar |',
                  '| Seguro de carga | 0.3–0.5% del valor CIF, dentro de los US$300 por m³ del modelo (los B/.100 al mes de los costos fijos son el seguro de responsabilidad civil y de producto) | **Supuesto** | Práctica de mercado; cotizar |', name)
        md = _rep(md, '| 4% de las ventas en el modelo | **Supuesto** | Varios 3PL lo incluyen con flota propia |', '| 4% de las ventas en el modelo | **Supuesto** | Los operadores que ofrecen distribución local lo cotizan por entrega; el correo lo pide |', name)
        md = _rep(md, '| Primer embarque de 5 tarimas puesto en bodega, sin contar la mercancía | Unos US$2,700–3,500: flete y destino 1,800–2,700, corredor y acarreo 300–500, seguro según valor | **Estimación compuesta** | Suma de las líneas anteriores |',
                  '| Primer embarque de 5 tarimas (unos 10 m³) puesto en bodega, sin contar la mercancía | Unos US$2,900–3,100 en el caso base: flete 1,900–2,000 (US$200 por m³), desconsolidación, destino y entrega local unos 750, corredor unos 200 y seguro unos 70; en el escenario alto, unos US$4,500 (US$470 por m³) | **Estimación compuesta** | Suma de las líneas anteriores |', name)
        md = _rep(md, 'Los correos a las aseguradoras de fianzas y al IEA siguen pendientes de envío. Pedir a varios a la vez y decirlo.',
                  'Los correos a las aseguradoras de fianzas y al IEA salen desde el correo de Jaime cuando él apruebe el texto (regla desde el 9 de octubre: ninguna comunicación externa sale sin su revisión). Pedir a varios a la vez y decirlo. Nota sobre el correo enviado: dice «unos 9 m³»; 5 tarimas de 1.2 × 1.0 × 1.6 m son 9.6 m³ y el cuestionario anterior decía 10; la cotización firme lleva la cifra exacta con la hoja de datos.', name)
        md = _rep(md, 'Estimados señores de [operador]:', 'Estimados señores de (nombre del operador):', name)
        md = _rep(md, 'Montos iniciales estimados entre B/.20,000 y B/.150,000 por fianza.', 'Montos iniciales estimados entre B/.20,000 y B/.150,000 por fianza (por ejemplo, un renglón de paracetamol de la LPU de unos B/.226 mil al precio de oferta del modelo exige una fianza de cumplimiento de 30%, unos B/.68 mil).', name)
        md = _rep(md, 'paracetamol 500 mg tableta y jarabe 120 mg/5 ml;', 'paracetamol 500 mg tableta y jarabe 120–160 mg/5 ml;', name)
        md = _rep(md, 'hidrocortisona 1% crema; mometasona 0.1% crema.', 'hidrocortisona crema (concentración por confirmar con la fábrica); mometasona 0.1% crema.', name)

    elif name == '07_Auditoria_y_confianza.md':
        md = _rep(md, '| Ninguna cifra cambia; se marca con más claridad qué es supuesto |', '| Ninguna cifra del modelo cambia; se añade la verificación FOB contra aduana india (cremas: −B/.77 mil y 3.3%) y se marca con más claridad qué es supuesto |', name)
        md = _rep(md, '- Lo que no cambió: ningún número del modelo', '- 03 y Anexo: sección de verificación de las referencias FOB contra aduana india, con la sensibilidad de las cremas; el modelo no cambia.\n- Lo que no cambió: ningún número del modelo', name)
        md = _rep(md, '| THC Manzanillo US$275 desde el 15 de octubre de 2026 | 04, 06 |', '| THC Manzanillo US$275 desde el 15 de octubre de 2026 | 03, 04, 06 |', name)
        md = _rep(md, '| Desconsolidación US$86.5 por m³ | 04 | Tarifario de destino de Crowley Panamá (PDF) | No verificable | Media | «Tarifario publicado por Crowley; otros consolidadores cobran distinto» |',
                  '| Desconsolidación: US$0.20 por pie cúbico (mínimo US$55) en el tarifario de Crowley; US$86.5 por m³ en una cotización privada de 2025 | 03, 04 | Tarifario de destino de Crowley Panamá (PDF de 2023); cotización de una mudadora (abril de 2025) | Confirmado el tarifario de Crowley; la cotización privada es un dato único | Media | «Tarifario publicado por Crowley; los consolidadores cobran distinto» |', name)
        md = _rep(md, '| Corredor: B/.50 + 0.15% del CIF + B/.2 por línea | 04 |', '| Corredor: B/.50 + 0.15% del CIF + B/.2 por línea | 03, 04 |', name)
        md = _rep(md, 'Lo que mueve ese número, en orden: los costos fijos antes de vender (unos B/.4,700 al mes durante 9 meses sin ingresos), la probabilidad de ganar renglones, el colateral de las fianzas y los 150 días de cobro, el margen del intermediario, y la probabilidad de un problema de planta (15%) o de ruptura del suministro (4% anual).',
                  'Lo que mueve ese número: sobre el valor esperado, los costos fijos antes de vender (unos B/.33 mil acumulados hasta la primera venta; B/.4,700 al mes en madurez), la probabilidad de ganar renglones y la participación en compras menores, la erosión de precios y el margen del intermediario; sobre el capital, el colateral de las fianzas y los 150 días de cobro; y, en la simulación, la probabilidad de un problema de planta (15%) o de ruptura del suministro (4% anual).', name)
        md = _rep(md, '| Alta (cargo público; confirmar que sigue en el cargo antes de una reunión) |', '| Media (prensa; confirmar que sigue en el cargo antes de una reunión) |', name)
        md = _rep(md, 'aplica solo a productos ya registrados por autoridades de referencia | Alta |', 'aplica solo a productos ya registrados por autoridades de referencia | Media (prensa; falta leer el texto del DE 2 de 2025) |', name)
        md = _rep(md, 'circulares de la CDSCO del 25 de junio y del 15 de julio de 2025 | Alta |', 'circulares de la CDSCO del 25 de junio y del 15 de julio de 2025 | Media (prensa especializada; faltan las circulares) |', name)
        md = _rep(md, ' · [AllIndiaITR](https://www.allindiaitr.com/company/bueno-salud-care-india-private-limited/U24304GJ2016PTC094652) · [Tracxn](https://tracxn.com/d/legal-entities/india/bueno-salud-care-india-private-limited/__QkyE0fWHXfeIPptyCGSAs34b_zI2Ih3d3EQ5h30DeaY)', '', name)
        md = _rep(md, '## Fuentes de esta auditoría', MISSING + '## Fuentes de esta auditoría', name)

    elif name == 'Anexo_Plan_de_negocio_completo.md':
        md = _rep(md, 'exige B/.255 mil de capital en el caso base (B/.343 mil en la mediana simulada).', 'exige B/.255 mil de capital en el caso base, B/.258 mil con la fase 0 (B/.343 mil en la mediana simulada); el caso de planificación, con las tarifas legales de SignatureLex, pide B/.297 mil.', name)
        md = _rep(md, 'los costos fijos, el único que por sí solo vuelve positivo el VPN del caso base, y la tasa de victoria.', 'los costos fijos, el único que por sí solo vuelve positivo el VPN del caso base, y la tasa de victoria (tabla de sensibilidad en 03, sección «Riesgo cuantificado»).', name)
        md = _rep(md, '(−B/.13 mil si el coordinador cuesta B/.1,000 al mes)', '(−B/.12.6 mil si el coordinador cuesta B/.1,000 al mes)', name)
        md = _opt(md, '| Capital por socio, caso base |', '| Capital por socio, caso base (un sexto del capital más un tercio de la fase 0) |')

    elif name == 'Anexo_DD_hallazgos_en.md':
        md = _rep(md, '# B6 Partner DD — Findings summary (public sources; compiled 2026-10-06 UTC)', '# B6 Partner DD — Findings summary (public sources; compiled 2026-10-06 UTC; addendum of 2026-10-07/08 in section D)', name)
        md = _rep(md, '7. Directors per MCA: Deepti Rutul Patel (DIN 10699123) and Abhinav Bhargava, both since 30-Sep-2024;', '7. Directors per MCA mirror at the time (Falconebiz, 6-Oct): Deepti Rutul Patel (DIN 10699123) and Abhinav Bhargava, both since 30-Sep-2024 (the refreshed mirrors in section D also list Shivkumar Dudhwewala as whole-time director);', name)
        md = _rep(md, '- Gujarat FDCA WHO-GMP list & licence validity (sites unreachable: DNS/502). CDSCO SUGAM site list has no Gujarat data.', '- Gujarat FDCA licence list (site unreachable: DNS/502); the CDSCO WHO-GMP/COPP list was obtained later (section D).', name)
        md = _rep(md, '- CDSCO NSQ after Jun-2025 (dynamic search page).', '- CDSCO NSQ after Jun-2025: obtained later from the portal (section D).', name)
        md = _rep(md, '- Paywalled: shareholders, charges, financials of Bueno, Shape Wellness, Nosher.', '- Paywalled: shareholders and full accounts of Bueno, Shape Wellness, Nosher (free mirror summaries in section D).', name)
        md = _rep(md, 'WebFetch permission not granted; search budget exhausted', 'tool access not granted; search budget exhausted', name)
        md = md.rstrip('\n') + '\n' + DD_ADDENDUM

    return md
