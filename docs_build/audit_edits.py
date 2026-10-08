# -*- coding: utf-8 -*-
"""Edits that follow the 8 October 2026 audit (independent research pass + own re-verification)."""

# ---------- replacements applied to the plan export (before sectioning) ----------
PLAN_REPL = [
    # CSS budget figure as published by La Prensa, plus the units nuance
    ("baja 28.7% frente al de 2026, aunque queda 11% sobre el gasto que la CSS proyecta para 2026; la presión va hacia precios más bajos.",
     "baja 28.6% frente al de 2026 (B/.92.5 millones menos), aunque queda 11% sobre el gasto que la CSS proyecta para 2026 y prevé dispensar 7.2% más unidades (23.6 millones frente a 22.0 millones, [Decisiones Panamá](https://decisionespanama.com/css-proyecta-invertir-b-230-3-millones-en-medicamentos-en-2027-y-aumentar-7-2-las-unidades-dispensadas/)); la presión va hacia precios más bajos."),
    # LPU 01-2026 chronology
    ("La LPU 01-2026 quedó adjudicada el 15 de mayo de 2026 por 15 meses, y la LPU 11-2026 (antirretrovirales, controlados e intercambiables) el 31 de agosto.",
     "La LPU 01-2026 (proceso 2025-1-10-01-99-SPU-000009; precio de referencia B/.95.3 millones por 349 renglones, B/.91.98 millones según la CSS) recibió ofertas el 1 y 2 de diciembre de 2025; la CSS anunció 282 renglones adjudicados por unos B/.77.9 millones el 26 de marzo de 2026 y PanamaCompra la registra como adjudicada desde el 15 de mayo de 2026. Su vigencia es de 15 meses desde que quede ejecutoriada la adjudicación (cláusula 20 del pliego), así que vence hacia la segunda mitad de 2027. La LPU 11-2026 (antirretrovirales, controlados e intercambiables) aparece adjudicada el 31 de agosto de 2026."),
    # legal basis of the small-purchase thresholds
    ("| Contratación menor y compra menor ágil (hospitales, regiones, unidades CSS) | Hasta B/.70 mil y B/.50 mil por acto;",
     "| Contratación menor y compra menor ágil (hospitales, regiones, unidades CSS) | Hasta B/.70 mil y B/.50 mil por acto (topes de la Ley 419 para medicamentos; la Ley 22 general fija B/.50 mil);"),
    # Contraloría nuance
    ("la gestión de cobro en la Contraloría bajó de 188.5 a 5.4 días en promedio en 2025, y la Contraloría reporta",
     "la gestión de cobro en la Contraloría bajó de 188.5 a 5.4 días en promedio en 2025 (de 220.8 a 32.9 días para cobros mayores de B/.200 mil, la cifra que aplica a una LPU), y la Contraloría reporta"),
    # reference laboratories
    ("cada registro pasa por el análisis del Instituto Especializado de Análisis (IEA) salvo que",
     "cada registro pasa por el análisis de un laboratorio de referencia, el Instituto Especializado de Análisis (IEA) de la Universidad de Panamá o el INDICASAT (Ley 419, art. 72), salvo que"),
    ("| Registro sanitario por producto, ruta ordinaria | IEA hasta 60 días hábiles + DNFD hasta 20 días hábiles | B/.500 DNFD + análisis del IEA (B/.200–1,000 en la guía de 2012; cotizar) + MEF y Colegio | Ley 419, arts. 41 y 74; DE 27, art. 15 |",
     "| Registro sanitario por producto, ruta ordinaria | Laboratorio de referencia (IEA o INDICASAT) hasta 60 días hábiles + DNFD hasta 20 días hábiles | B/.500 DNFD + análisis del laboratorio (B/.200–1,000 en la guía de 2012; cotizar a los dos) + MEF y Colegio | Ley 419, arts. 41, 72 y 74; DE 27, arts. 15 y 248–251 |"),
    # Res. 985: products that are on the list and may matter for a second wave
    ("amitriptilina, quetiapina, topiramato ni prednisolona.",
     "amitriptilina, quetiapina, topiramato ni prednisolona. Sí están en la lista cefalexina (27), azitromicina (15), ciprofloxacina (30) y fluconazol (67), además de claritromicina y metronidazol: cualquier segunda ola debe cruzarse con la resolución antes de pedir precios."),
    # Bueno board: mirrors disagree
    ("Bueno Salud Care (Sanand): directores Deepti Rutul Patel (desde julio de 2024) y Abhinav Bhargava (desde marzo de 2024), junto con Shivkumar Dudhwewala, de la familia fundadora;",
     "Bueno Salud Care (Sanand): directores Shivkumar Dudhwewala (familia fundadora, director a tiempo completo desde 2019), Abhinav Bhargava (desde marzo o abril de 2024, según el espejo) y Deepti Rutul Patel (nombrada en julio o septiembre de 2024 según Falconebiz y AllIndiaITR; Zauba y Tracxn, cuyos datos parecen anteriores a esa fecha, no la muestran: estado por confirmar con el formulario DIR-12);"),
    ("y una directora de Bueno desde julio de 2024 es Deepti Rutul Patel | Amarilla: intermediario con posible vínculo familiar con el fabricante |",
     "y dos espejos del registro listan a Deepti Rutul Patel como directora de Bueno desde 2024 (estado actual por confirmar) | Amarilla: intermediario con posible vínculo familiar con el fabricante |"),
    ("Año fiscal 2025: ventas de ₹101.8 crore (+30%), pérdida neta de ₹4.8 crore, 252 empleados en planilla y deuda garantizada por ₹104 crore; la junta cambió en 2024 y el enlace «Annual Return» del sitio es una página en blanco |",
     "Año fiscal 2025: ventas de ₹101.8 crore (+30%), pérdida neta de ₹4.8 crore, 252 empleados en planilla (249 según Tracxn) y deuda garantizada por ₹104 crore, según los espejos comerciales del registro (The Company Check, Zauba), que venden el informe completo; sin contrastar con estados auditados. La junta cambió en 2024 y el enlace «Annual Return» del sitio es una página en blanco |"),
    # sources: add the CSS communiqués and the PanamaCompra public search
    ("- [ANTAI: reportes mensuales de contrataciones de la CSS, el MINSA y los patronatos](https://monitoreo.antai.gob.pa/)",
     "- [ANTAI: reportes mensuales de contrataciones de la CSS, el MINSA y los patronatos](https://monitoreo.antai.gob.pa/)\n- Comunicados de la CSS: [3 de diciembre de 2025, LPU por B/.91.98 millones y 348 renglones](https://prensa.css.gob.pa/2025/12/03/css-invertira-91-millones-de-dolares-en-compra-masiva-de-medicamentos/) · [6 de enero de 2026, ahorro de B/.37.4 millones](https://prensa.css.gob.pa/2026/01/06/compras-estrategicas-de-medicamentos-logran-ahorro-record-de-b-37-4-millones/) · [26 de marzo de 2026, 282 renglones adjudicados por B/.77.9 millones](https://prensa.css.gob.pa/2026/03/26/llegan-miles-de-medicamentos-css-refuerza-a-nivel-nacional/) · PanamaCompra, búsqueda pública de procesos (estado «Adjudicado» de la LPU 01-2026 el 15 de mayo de 2026 y de la LPU 11-2026 el 31 de agosto de 2026; 33 subastas en reversa del MINSA en 2026)"),
    ("- [La Prensa: presupuesto 2027 de la CSS](https://www.prensa.com/sociedad/presupuesto-2027-de-la-css-contempla-925-millones-menos-para-medicamentos/)",
     "- [La Prensa: presupuesto 2027 de la CSS](https://www.prensa.com/sociedad/presupuesto-2027-de-la-css-contempla-925-millones-menos-para-medicamentos/) · [Decisiones Panamá: B/.230.3 millones y 7.2% más unidades en 2027](https://decisionespanama.com/css-proyecta-invertir-b-230-3-millones-en-medicamentos-en-2027-y-aumentar-7-2-las-unidades-dispensadas/)"),
]

# ---------- replacements applied to the hoja de ruta export ----------
HOJA_REPL = [
    ("| BP Logistics | Panamá Pacífico | Aloja 8 agencias; amplió su área de temperatura controlada en 2025; es a quien ya se le mandó el cuestionario |",
     "| BP Logistics (Grupo Hilasal, El Salvador) | Panamá Pacífico | Aloja 8 agencias; se presenta como operador logístico autorizado por el MINSA, con bodegas de 15–25 °C y de 2–8 °C; duplicó su área de temperatura controlada en 2025; es a quien ya se le mandó el cuestionario |\n| Interworld Freight | Panamá (con opción de depósito aduanero y Zona Libre de Colón) | Bodega farmacéutica con zonas de 2–8 °C y 15–25 °C; menos conocido, vale una cotización |"),
]

# ---------- new logistics-cost section (replaces LOGCOST) ----------
LOGCOST_V2 = """## Estimación de costos logísticos mientras no haya cotización firme

Ningún operador logístico de Panamá publica tarifas. La tabla separa lo que es tarifa publicada (defendible con un enlace), lo que es referencia pública indirecta y lo que es un supuesto presupuestario nuestro. Las cifras se reemplazan por las cotizaciones en cuanto lleguen.

| Concepto | Estimación | Naturaleza de la cifra | Base |
| --- | --- | --- | --- |
| Almacenamiento y manejo en un 3PL licenciado: 5–10 tarimas, 15–25 °C, control por lote y vencimiento, 2–4 despachos al mes | B/.300–1,200 al mes; el modelo usa B/.600 (cuota mínima) | **Supuesto presupuestario** | Construido con el alquiler de bodega en Panamá (CBRE, 2H2022: clase A US$7.05 y clase B US$5.05 por m² al mes), la densidad de un rack de tarimas y la estructura tarifaria que usan los 3PL (recepción + posición de tarima al mes + picking por caja, con mínimo mensual); ningún 3PL de Panamá publica tarifas |
| Flete marítimo en contenedor de 20 pies India–Manzanillo | US$3,750 de flete (tarifa FAK de CMA CGM vigente desde el 10 de junio de 2026; US$2,600 en febrero, +44%), sin THC ni recargos | **Tarifa publicada** (prensa especializada que reproduce el aviso de la naviera) | [Container News, junio de 2026](https://container-news.com/cma-cgm-raises-fak-rates-from-indian-subcontinent-to-latin-america-europe-and-north-africa/) · [febrero de 2026](https://container-news.com/cma-cgm-updates-fak-rates-from-indian-subcontinent-to-latin-america/); la tarifa de octubre de 2026 puede ser distinta |
| Cargo de manejo en terminal (THC/DHC) en Manzanillo | US$275 por contenedor seco (US$295 refrigerado) desde el 15 de octubre de 2026 | **Tarifa publicada** | [Maersk, aviso del 16 de septiembre de 2026](https://www.maersk.com/news/articles/2026/09/16/terminal-handling-service-revision-panama) |
| Carga consolidada (LCL), unos 9 m³ por embarque al inicio | US$200 por m³ de flete más unos US$100 de desconsolidación y destino (el modelo usa US$300 por m³ puesto en bodega) | **Referencia indirecta** | Desconsolidación US$86.5 por m³ en el tarifario de destino de Crowley Panamá; el flete por m³ es un supuesto derivado de la tarifa FAK por contenedor |
| Corredor de aduana | B/.50 + 0.15% del valor CIF + B/.2 por línea; unos B/.200–400 por embarque de 11 productos | **Honorario mínimo legal** (Ley 20 de 1994); el honorario real se cotiza | Texto de la ley; ningún corredor publica tarifas |
| Autorización de importación de la DNFD por embarque | Sin tasa para no controlados; hasta 3 días hábiles | **Norma** | DE 27 de 2024, art. 364 |
| Seguro de carga | 0.3–0.5% del valor CIF; el modelo usa B/.100 al mes | **Supuesto** | Práctica de mercado; cotizar |
| Entregas a los almacenes de la CSS y del MINSA | 4% de las ventas en el modelo | **Supuesto** | Varios 3PL lo incluyen con flota propia |
| Primer embarque de 5 tarimas puesto en bodega, sin contar la mercancía | Unos US$2,700–3,500: flete y destino 1,800–2,700, corredor y acarreo 300–500, seguro según valor | **Estimación compuesta** | Suma de las líneas anteriores |

Comparación con una bodega propia, sin contar el regente que ambas necesitan: con 5 tarimas, un 3PL cuesta unos B/.680 al mes contra B/.4,030 más B/.37 mil de inversión en bodega propia; con 15 tarimas, B/.960 contra B/.5,920 más B/.54 mil. Es una estimación propia (alquiler CBRE, aire acondicionado, personal, equipo); a este volumen la bodega propia no tiene sentido con ningún supuesto razonable.

Qué se le puede decir a Rutul y cómo defenderlo: las cifras de flete y de THC son avisos públicos de las navieras, con fecha; el almacenamiento es nuestro presupuesto de trabajo mientras los 3PL no coticen, y así hay que presentarlo. Si pregunta de dónde salen los números, la respuesta es exactamente esa: «freight and terminal charges are published carrier notices (CMA CGM June 2026, Maersk October 2026); the storage range is our budget assumption, built from Panama warehouse rent benchmarks and the way 3PLs price (receiving, pallet position, picking); it is not a quote, which is why we need the factory data».
"""

# ---------- opening message: bubble 4 rewritten with only defensible figures ----------
BUBBLE4_OLD_START = "Burbuja 4 (opcional; úsela si pregunta cuánto cuesta o si quiere adelantarle el orden de magnitud):"
BUBBLE4_V2 = """Burbuja 4 (opcional; úsela si pregunta cuánto cuesta o si quiere adelantarle el orden de magnitud; cada cifra tiene fuente o está marcada como presupuesto nuestro):

```text
We don't have a real quote yet. What we do have: published freight benchmarks (CMA CGM's FAK rate India-Manzanillo was US$3,750 per 20' in June 2026, before local charges, and Maersk's terminal handling in Manzanillo is US$275 per box from mid-October), and our own working budget for licensed pharma storage of 5-10 pallets, roughly B/.300-1,200 a month with handling, until the 3PLs quote. Freight is public data, storage is our budget; both get replaced by real quotes once the factory data is in.
```

Si ya mandó la versión anterior de esta burbuja y él pregunta de dónde salen los números:

```text
Fair question. The freight and terminal figures are the carriers' published notices (CMA CGM FAK June 2026, Maersk THC October 2026). The storage range is our budget assumption, built from Panama warehouse rent benchmarks and the way 3PLs price here (receiving, pallet position per month, picking). It's not a quote, and that's exactly why we need the factory data: with it the 3PLs give us real numbers in days.
```
"""

# ---------- 01: method note and claims table ----------
METODO_OLD = "Las fechas de nombramiento de los directores de Bueno difieren entre los espejos del registro mercantil (marzo, julio o septiembre de 2024); todas caen en 2024, cuando cambió la junta."
METODO_NEW = ("Sobre la junta de Bueno los espejos del registro mercantil no coinciden: Falconebiz y AllIndiaITR listan a Deepti Rutul Patel como directora desde julio o septiembre de 2024 y a Abhinav Bhargava desde marzo o abril de 2024; Zauba y Tracxn, cuyos datos parecen anteriores a esa fecha (última junta anual registrada: septiembre de 2023), muestran solo a Shivkumar Dudhwewala y a Bhargava. "
              "Por eso el vínculo familiar con el fabricante se trata como probable, no como hecho, hasta ver el formulario DIR-12 o la lista de directores que entregue la contraparte (lo pide el paso 6 del guion).")
DICHO_OLD = "Patel no es director de Bueno, pero sí lo son Deepti Rutul Patel desde 2024 y su socio Abhinav Bhargava | Hay fábrica y es seria en papel; falta que la nombre y que firme como fabricante |"
DICHO_NEW = "Patel no es director de Bueno; su socio Abhinav Bhargava sí lo es desde 2024, y dos espejos del registro listan a Deepti Rutul Patel como directora desde 2024 (otros dos no la muestran; por confirmar) | Hay fábrica y es seria en papel; falta que la nombre y que firme como fabricante |"

# ---------- 00: pending items and reading map ----------
PENDIENTES_OLD = "- [ ] Canal privado de farmacias: solo si se decide explorarlo; hoy el modelo no lo incluye."
PENDIENTES_NEW = ("- [ ] Consulta escrita a la DNFD: si el depósito de un 3PL puede declararse como depósito de la agencia y si el regente del 3PL puede cubrirla o cada agencia necesita el suyo (DE 27, arts. 382 y 396–398); define el costo fijo más grande después del coordinador.\n"
                  "- [ ] Estado actual de la junta de Bueno (formulario DIR-12 o lista de directores) y estados auditados del año fiscal 2025: los espejos del registro no coinciden.\n"
                  "- [ ] Resolución de adjudicación de la LPU 01-2026 (PanamaCompra) para fijar la fecha exacta de vencimiento del contrato vigente y, con ella, la ventana de la próxima LPU.\n"
                  "- [ ] Canal privado de farmacias: solo si se decide explorarlo; hoy el modelo no lo incluye.")
MAPA_OLD = "| Anexo_Plan_de_negocio_completo.md | El plan de negocio en una sola pieza, del que salen los documentos 00 a 05 | Consultar todo junto |"
MAPA_NEW = ("| 07_Auditoria_y_confianza.md | Qué cifra está firme, cuál es supuesto, de dónde sale cada una, cómo argumentarla y qué falta; cómo leer el 77% | Defender los números ante socios e inversionistas |\n"
            "| Anexo_Plan_de_negocio_completo.md | El plan de negocio en una sola pieza, del que salen los documentos 00 a 05 | Consultar todo junto |")
HOJA_RFQ_NOTE = ("\n\nNota de la auditoría del 8 de octubre: los 3PL no publican tarifas y la ley no dice en una sola línea si el regente del operador cubre al cliente; por eso el correo pregunta por regente o licencia compartida, y conviene una consulta escrita a la DNFD en paralelo. "
                 "BP Logistics pertenece al Grupo Hilasal (El Salvador) y se presenta como operador autorizado por el MINSA; Interworld Freight también ofrece bodega farmacéutica con cadena de frío.")


def doc07(header):
    return f"""# Auditoría de los entregables y nivel de confianza

{header.rstrip()}

Qué es este documento: el resultado de revisar el paquete del 7 de octubre como lo haría un auditor externo. Dice, cifra por cifra, de dónde sale cada número, si se pudo comprobar en una fuente primaria, qué grado de confianza merece y cómo explicarlo en una frase si alguien lo pregunta. También dice qué cambió en los demás documentos a raíz de la revisión y qué sigue abierto.

## Cómo se hizo

Dos capas, con fechas:

1. **Rastro propio de verificación (5 al 7 de octubre).** Documentos primarios descargados y leídos: el pliego de la LPU 01-2026 de la CSS (60 páginas, PanamaCompra), los cuadros de propuestas de las LPU 01-2026 y 11-2026, la búsqueda pública de procesos de PanamaCompra (estados y fechas de los actos, conteo de subastas y de compras menores), el Decreto Ejecutivo 27 de 2024 y la Resolución 985 de 2025 (PDF del MINSA), la circular ANTAI-DS-001-2026, las listas de la CDSCO (plantas con certificado OMS-BPM al 31 de diciembre de 2025 y alertas de calidad de marzo de 2024), los espejos del registro mercantil indio, el verificador de la FDA de Filipinas, los registros de El Salvador (DNM y COMPRASAL), la lista de establecimientos de la DNFD (28 de septiembre de 2026) y los avisos tarifarios de las navieras. Las bitácoras con cada URL y fecha están en el respaldo del código.
2. **Revisión independiente (8 de octubre).** Un pase de investigación separado volvió a buscar desde cero 31 afirmaciones del plan, sin acceso a los archivos descargados. Confirmó las cifras de mercado, la Resolución 985 y los fletes; matizó tres puntos (la cronología de la LPU 01-2026, la base legal de los topes de compra menor y la junta de Bueno); y no pudo abrir varias fuentes que sí están en la capa 1 (los PDF de PanamaCompra, la lista de la DNFD, los PDF de la CDSCO, los registros pagados del MCA). Donde dice «no verificable» pero el documento primario está en la capa 1, aquí se dice cuál es y la confianza se fija con ese documento, no con la ausencia del segundo pase.

Escala: **Alta** = documento primario leído (ley, pliego, acto, tarifa oficial, registro); **Media** = fuente pública secundaria o primaria parcial, o dato que depende de la fecha; **Baja** = supuesto de trabajo nuestro, con una base razonada pero sin cotización ni dato publicado. Los supuestos no son errores: son lo que las cotizaciones de la fase 0 van a reemplazar.

## Veredicto por entregable

| Documento | Confianza | Qué está firme | Qué es supuesto o análisis propio | Qué cambió el 8 de octubre |
| --- | --- | --- | --- | --- |
| 00 Resumen y plan | Media-Alta | Plan por fases, compuertas, línea de tiempo regulatoria (plazos de la Ley 419 y del DE 27) | El calendario ilustrativo depende de cuándo llegue el paquete de la fábrica | Cronología de la LPU 01-2026 corregida; tres pendientes nuevos |
| 01 Investigación de Rutul y el fabricante | Media | Datos societarios básicos de Bueno (CIN, capital, directores Dudhwewala y Bhargava, seis cargas), certificado OMS-BPM vigente a 2029 en la lista de la CDSCO, alertas de marzo de 2024, registros en Filipinas, ausencia en El Salvador y en PanamaCompra, perfil comercial de Zywie | Que Bueno sea el fabricante (inferencia por coincidencia de listas, 97%); la directora Deepti Rutul Patel (dos espejos sí, dos no); las finanzas del año fiscal 2025 (espejos comerciales, sin estados auditados) | La junta de Bueno pasa de hecho a probable; se pide el DIR-12 |
| 02 Mercado, requisitos y competencia | Media-Alta en mercado y regulación; Media en competencia | Presupuestos de la CSS, ahorro de B/.37.4 millones, tamaño y cláusulas de la LPU 01-2026 (pliego), subastas del MINSA (búsqueda pública de PanamaCompra), Resolución 985, plazos de la Ley 419, tasas del DE 27 | Las tasas de victoria y descalificación, la concentración de proveedores y el 1.8× son análisis propios sobre extracciones de PanamaCompra; no existe un estudio público que los respalde | −28.6% en vez de −28.7%; INDICASAT como segundo laboratorio; topes de compra menor atribuidos a la Ley 419; cobro de la Contraloría para montos grandes (32.9 días) |
| 03 Costos, capital y proyección | Media en estructura; Baja en costos fijos y logísticos | Tasas oficiales, impuestos y cargas (textos legales y resúmenes de PwC), fletes publicados, el mecanismo del modelo (verificado contra el Excel) | Sueldos, contabilidad, auditoría, 3PL, seguro, prima y colateral de las fianzas, el precio de Zywie (×1.25 sobre una referencia india) y el análisis del laboratorio (B/.600): todos supuestos hasta cotizar | Ninguna cifra cambia; se marca con más claridad qué es supuesto |
| 04 Logística y operación | Media | Cómo opera un 3PL licenciado, vida útil y bodega (pliego), fletes y THC publicados, lista de 3PL con agencias alojadas (lista de la DNFD) | Tarifa de almacenamiento (B/.300–1,200), LCL por m³, seguro, distribución 4%; si el regente del 3PL puede cubrir a la agencia (no está resuelto en una línea de la norma) | Tabla de costos con la naturaleza de cada cifra; BP Logistics (Grupo Hilasal) e Interworld Freight; consulta a la DNFD como pendiente |
| 05 Trato, socios y hoja de ruta | Media-Alta | Condiciones del trato, estructura de capital, reglas de gobierno, contratos | El reparto de valor depende del margen de Zywie (15% supuesto) | Sin cambios |
| 06 Guion | Alta en método; Media en la burbuja de costos | Lo que exige cada tercero (pliego, DNFD, aseguradora) es cierto y se puede citar | El rango de almacenamiento es presupuesto nuestro | Burbuja 4 reescrita con fuentes; respuesta de respaldo si ya se envió la anterior |

## Qué cambió en los documentos

- 00 y Anexo del plan: la LPU 01-2026 recibió ofertas el 1 y 2 de diciembre de 2025, la CSS anunció 282 renglones adjudicados (B/.77.9 millones) el 26 de marzo de 2026 y PanamaCompra la registra como adjudicada desde el 15 de mayo de 2026; vigencia de 15 meses desde que quede ejecutoriada la adjudicación. La conclusión de calendario no cambia: la próxima LPU de síntesis química llegaría en la segunda mitad de 2027.
- 02: presupuesto de la CSS −28.6% (cifra de La Prensa) y 7.2% más unidades en 2027; los topes de B/.70 mil y B/.50 mil se atribuyen a la Ley 419 (la Ley 22 general fija B/.50 mil); el análisis de control previo lo hace el IEA o el INDICASAT (Ley 419, art. 72), y conviene cotizar a los dos; la Contraloría tarda 32.9 días en cobros mayores de B/.200 mil (no 5.4), que es el dato que aplica a una LPU; en la Resolución 985 también figuran cefalexina, azitromicina, ciprofloxacina y fluconazol.
- 01: la junta de Bueno se describe con la discrepancia entre espejos; las finanzas del año fiscal 2025 quedan marcadas como cifras de espejos comerciales sin contrastar.
- 04: la estimación logística distingue tarifa publicada, referencia indirecta y supuesto; BP Logistics (Grupo Hilasal, El Salvador) e Interworld Freight entran a la lista.
- 06: la burbuja 4 solo usa cifras con fuente o marcadas como presupuesto nuestro, y trae la respuesta si ya se envió la versión anterior.
- Lo que no cambió: ningún número del modelo (capital, VPN, probabilidad de pérdida), las cláusulas del pliego, la lista de productos, las tasas oficiales ni la estructura del trato.

## Tabla de afirmaciones: fuente, verificación y cómo argumentarla

| Cifra o afirmación | Dónde se usa | Fuente primaria (capa 1) | Pase independiente (8-oct) | Confianza | Cómo argumentarla |
| --- | --- | --- | --- | --- | --- |
| CSS: B/.322.8 millones (2026) → B/.230.3 millones (2027); gasto real 2026 ≈ B/.207 millones | 00, 02 | La Prensa, Decisiones Panamá, Panamá América (proyecto de presupuesto presentado por la CSS) | Confirmado; −28.6%; +7.2% unidades | Alta (es un proyecto de presupuesto, sujeto a cambios) | «Es el proyecto de presupuesto que la CSS presentó en septiembre de 2026; frente al gasto real de 2026 sube, frente al presupuesto baja» |
| CSS adjudicó B/.192.4 millones sobre B/.229.8 millones estimados | 02 | Comunicado de la CSS del 6 de enero de 2026 | Confirmado | Alta | «Comunicado oficial de la CSS; el ahorro es 16.3%» |
| LPU 01-2026: B/.92 millones, 348 renglones, 15 meses; ofertas en diciembre de 2025; 282 renglones adjudicados en marzo; estado adjudicado el 15 de mayo de 2026 | 00, 02 | Pliego y cuadro de propuestas (PanamaCompra, proceso 2025-1-10-01-99-SPU-000009); comunicados de la CSS; búsqueda pública de PanamaCompra | Confirmado el tamaño; la fecha de mayo no la encontró; la de marzo sí | Alta en tamaño y cláusulas; Media en la fecha exacta de adjudicación | «El pliego dice 15 meses desde la adjudicación ejecutoriada; la CSS anunció los renglones adjudicados en marzo y PanamaCompra cerró el estado en mayo; la próxima LPU cae en la segunda mitad de 2027» |
| Cláusulas de la LPU: fianza de propuesta 10% por 180 días hábiles (subsanable); cumplimiento 30%; pago a 90 días desde la cuenta; compra mínima 60% (capítulo II) o 50% (contrato); vida útil 18 meses; carta solidaria del fabricante apostillada a 45 días; empaque secundario con «L.P.U. No.01-2026»; sin reetiquetado; registro sanitario y licencia DNFD no subsanables | 02, 04, 06 | Pliego de la LPU 01-2026, cláusulas 8.1, 8.12, 8.14, 11, 13, 18, 20, 24 y contrato modelo (cláusula Cuarta) | No pudo abrir el pliego | Alta | «Está en el pliego, cláusula por cláusula; tenemos el PDF» |
| MINSA: 33 subastas en reversa de un producto entre junio y octubre de 2026, 28 adjudicadas; 20% de cumplimiento, sin fianza de propuesta, cantidades fijas, «Propiedad del MINSA» | 02 | Búsqueda pública de PanamaCompra (tipo 17, SSR-000001 a 000034) y pliego de subasta del MINSA 2026 | Solo confirmó el anuncio de marzo | Alta (conteo del 7 de octubre; cambia cada semana) | «Lo contamos en PanamaCompra el 7 de octubre; el pliego de las subastas trae las condiciones» |
| Compra conjunta DE 16 de 2026 (376 renglones) sin acto publicado | 00, 02 | Decreto en el sitio del MINSA; búsqueda de PanamaCompra sin actos | Confirmó los 376 medicamentos | Alta al 7 de octubre | «El decreto existe; el acto no ha salido en PanamaCompra» |
| Topes: contratación menor B/.70 mil; compra menor ágil B/.50 mil | 02 | Ley 419 de 2024 (procedimientos de selección para medicamentos) | Confirmado, atribuido a la Ley 419 | Media-Alta (falta citar el artículo exacto) | «Topes de la Ley 419 para medicamentos; la Ley 22 general fija B/.50 mil» |
| Conteos de compras menores 2025 y 2026 | 02 | Extracción propia de la búsqueda pública de PanamaCompra (heurística por título) | No verificable | Media | «Extracción propia de PanamaCompra con criterio de título; es un orden de magnitud» |
| Compras descentralizadas a 1.8× el precio centralizado | 02 | Análisis propio sobre 105 pares de precios de PanamaCompra | No verificable | Media-Baja | «Análisis interno sobre precios públicos; la metodología está en el respaldo; no es un estudio publicado» |
| Tasas de victoria (77% con un oferente…), 95% gana el más barato, 17% vs 26%, 56% vs 34% | 02, 03 | Análisis propio sobre cuadros de propuestas 2020–2024 | No verificable | Media-Baja | «Estadística propia sobre actos públicos; el modelo usa 30% de probabilidad de ganar, por encima del 17% de los nuevos, y lo dice» |
| Concentración de proveedores y canales de los fabricantes indios | 02 | Análisis propio sobre cuadros de propuestas 2023–2026 | No verificable | Media-Baja | «Conteo propio sobre PanamaCompra» |
| Contraloría: cobros de 188.5 a 5.4 días; 32.9 días para cobros mayores de B/.200 mil | 02, 03 | Panamá América, 4 de octubre de 2025 (informe de la Contraloría) | Confirmado | Media (fuente interesada) | «Dato de la propia Contraloría vía prensa; mide el refrendo, no el ciclo completo; por eso el modelo usa 150 días» |
| Ley 419: IEA o INDICASAT hasta 60 días hábiles (art. 74); DNFD 20 días hábiles (art. 41); dos análisis posregistro (art. 67); vigencia 5 años (art. 48); laboratorios de referencia (art. 72) | 00, 02 | Texto de la Ley 419 (vLex) | Confirmado, con los artículos | Alta | «Artículos 41, 48, 67, 72 y 74 de la Ley 419» |
| DE 27 de 2024: registro B/.500; licencia B/.200 por 2 años + B/.50 de inspección; intercambiabilidad B/.400; controlados B/.100 y B/.50; regente al menos 4 horas; Registro de Oferentes 30 días hábiles; importación 3 días hábiles | 02, 03 | PDF del DE 27 (art. 15; p. 102 regencia; arts. 248–251, 364, 725–726) | Confirmó B/.500, B/.200 y B/.100; el resto no lo encontró | Alta en B/.500/200/100; Media en B/.50, B/.400 y plazos | «Está en el PDF del decreto; las tasas menores conviene confirmarlas en ventanilla» |
| Resolución 985: 173 principios activos; los 11 de la primera ola no están | 02 | PDF de la resolución (GO 30317) | Confirmado al detalle | Alta | «Lista oficial; levofloxacina es el 99 y metformina el 111; ninguno de los 11 aparece» |
| Autoridades de referencia (DE 2 y DE 12 de 2025); CDSCO fuera de la lista de la OMS | 02 | PDF del DE 12; lista WLA de la OMS (diciembre de 2025) | Parcial | Alta | «La lista de la OMS pasa de Islandia a Indonesia; India no está» |
| Ley 462 de 2025 (excepción de importación, paralelas, topes) | 02 | PDF de la Ley 462 | Parcial | Media-Alta | «Texto de la ley; un abogado debe confirmar el alcance» |
| Ley 316 y circular ANTAI-DS-001-2026 | 02, 05 | PDF de la circular y requisitos de la ANTAI | No verificable | Alta | «La circular de la ANTAI está descargada; aplica a toda adjudicataria» |
| Informe 930; impuestos; cargas laborales (13.25% → 14.25%) | 03 | Páginas de la DGI; resúmenes fiscales de PwC; Ley 462 | No verificable | Media-Alta | «Cifras de la DGI y de PwC; el contador las confirma» |
| Flete FAK 20 pies US$3,750 (junio de 2026, +44%) | 03, 04, 06 | Container News (aviso de CMA CGM) | Confirmado | Alta, con fecha | «Aviso de la naviera reproducido por prensa especializada; la tarifa de octubre puede ser otra» |
| THC Manzanillo US$275 desde el 15 de octubre de 2026 | 04, 06 | Aviso de Maersk del 16 de septiembre de 2026 | Confirmado | Alta | «Aviso oficial de Maersk» |
| Desconsolidación US$86.5 por m³ | 04 | Tarifario de destino de Crowley Panamá (PDF) | No verificable | Media | «Tarifario publicado por Crowley; otros consolidadores cobran distinto» |
| Corredor: B/.50 + 0.15% del CIF + B/.2 por línea | 04 | Ley 20 de 1994 (texto en Justia) | No verificable | Media | «Honorario mínimo legal; el real se cotiza» |
| Seguro de carga 0.3–0.5% | 03, 04 | Práctica de mercado | No verificable | Baja | «Supuesto; se cotiza con la carga» |
| Sueldos (coordinador B/.1,500; regente B/.700 medio tiempo), contabilidad B/.300, auditoría B/.3,000 | 03 | Bolsas de empleo (Konzerta, unmejorempleo, octubre de 2026); una referencia pública de contabilidad | No verificable | Baja-Media | «Rangos de bolsas de empleo; son los costos que más mueven el resultado y por eso se cotizan en la fase 0» |
| Fianzas: cuatro aseguradoras emiten 76%; colateral 50% (25–100%); prima 1.6% | 03 | Superintendencia de Seguros (primas por ramo, diciembre de 2025); requisitos publicados de Internacional de Seguros y ASSA | No verificable | Media en requisitos; Baja en prima y colateral | «La estadística de la Superintendencia es pública; la prima y el colateral se cotizan» |
| 3PL B/.600 al mes (300–1,200); bodega propia B/.4,030 + B/.37 mil | 03, 04, 06 | Supuesto construido con alquileres CBRE 2H2022 y la estructura tarifaria de los 3PL | No verificable | Baja | «Presupuesto nuestro; se reemplaza con las cotizaciones» |
| 3PL con agencias alojadas: J. Cain 24, Panalog 22, DHL 16, Osala 15, TLA 11, BP 8 | 04 | Lista de establecimientos de la DNFD (28 de septiembre de 2026) | No verificable | Media-Alta (conteo propio sobre la lista oficial) | «Lo contamos en la lista de la DNFD» |
| Precios unitarios de la LPU 01-2026 por producto | 02 | Cuadro de propuestas de la LPU (PanamaCompra, JSON) | No verificable | Alta | «Están en el cuadro de propuestas; tenemos el archivo» |
| Referencias FOB indias (TNMSC, Delhi, Jan Aushadhi) ×1.35–1.4 y ×1.25 | 02, 03 | PDF de TNMSC y Delhi; espejo de Jan Aushadhi | No verificable | Baja como costo real: son precios internos de la India, no FOB de exportación | «Son referencias públicas indias ajustadas; el costo real lo da la lista de precios de la fábrica, y el modelo se recalcula con ella» |
| Bueno: CIN, capital ₹22.27 crore, Dudhwewala y Bhargava directores, seis cargas | 01 | Zauba, Tofler, Falconebiz | Confirmado | Alta | «Registro mercantil indio, varios espejos coinciden» |
| Deepti Rutul Patel directora de Bueno desde 2024 | 01 | Falconebiz, AllIndiaITR | Dos espejos no la muestran | Media-Baja | «Dos espejos la listan desde 2024, dos no; por eso pedimos la lista de directores» |
| Bueno FY2025: ₹101.8 crore, pérdida ₹4.8 crore, deuda ₹104 crore | 01, 05 | The Company Check, Zauba (espejos comerciales) | No verificable | Media-Baja | «Cifras de espejos del registro; se piden los estados auditados» |
| OMS-BPM (COPP) de Sanand vigente al 26 de enero de 2029; sin alertas nuevas | 01 | Lista de la CDSCO al 31 de diciembre de 2025; portal de alertas | No verificable | Alta | «Lista oficial de la CDSCO» |
| Alertas de marzo de 2024 (ceftriaxona, amoxicilina dispersable) | 01 | PDF de alertas de la CDSCO, marzo de 2024, p. 5 | No verificable | Alta | «Alerta oficial de la CDSCO; por eso se pide el informe de causa y corrección» |
| Filipinas: 39 registros | 01 | Verificador de la FDA de Filipinas | No verificable | Media-Alta | «Verificador público de la FDA de Filipinas» |
| El Salvador: cero registros y cero adjudicaciones | 01 | DNM (2,149 registros revisados) y COMPRASAL (5,819 líneas) | No verificable | Media-Alta (búsqueda por nombre; un registro a nombre de un distribuidor local no aparecería) | «Buscamos por nombre en los dos registros públicos; por eso se le pide a Rutul el número de registro o el distribuidor» |
| Zywie: sociedad de 2018, arroz y vegetales, tabletas desde 2026 | 01 | GST público, IndiaMART | No verificable | Media | «Perfil comercial público y registro GST» |

## Cómo leer el 77% y cómo presentarlo

El 77% es la proporción de 20,000 escenarios simulados en los que la S.A., **tal como la propone Patel** (50/50 en capital, sin compuertas, Zywie con margen propio, registros pagados por nosotros, anticipo al proveedor), termina con menos dinero del que puso. No es una predicción sobre el negocio en general: es una medida de esa estructura. Lo que mueve ese número, en orden: los costos fijos antes de vender (unos B/.4,700 al mes durante 9 meses sin ingresos), la probabilidad de ganar renglones, el colateral de las fianzas y los 150 días de cobro, el margen del intermediario, y la probabilidad de un problema de planta (15%) o de ruptura del suministro (4% anual).

Tres cosas que hay que decir al presentarlo:

1. Con las condiciones de la compuerta 0 (precio a libro abierto, fabricante paga registros, 150–180 días de crédito) la probabilidad baja a 41%, y a 29% si se mide la pérdida más allá de la fase 0; con un socio operando sin sueldo, a 31% y 18%. El resto solo se conoce compitiendo, y para eso está la compuerta operativa.
2. La fase 0 acota la pérdida: unos B/.2,700 entre los tres mientras no se cumplan las condiciones. Un inversionista no arriesga el capital grande hasta que las cotizaciones y la lista de precios estén sobre la mesa.
3. El modelo es deliberadamente conservador en costos y plazos (todo tarda y cuesta más en la simulación) y algo generoso en una sola cosa, la tasa de victoria (30% frente al 17% de los nuevos); el documento 03 lo dice y muestra cuánto cambia el resultado si se usa 20% o 17%.

Lo que debilita el 77% como argumento: los costos fijos son supuestos (Baja) y pesan más que cualquier otro factor. Lo que lo fortalece: las cláusulas que generan el capital de trabajo (30% de fianza, 90 días de pago, 18 meses de vida útil) están en el pliego (Alta). Por eso la fase 0 va primero a las cotizaciones.

## Lo que no se pudo cerrar y cómo se cierra

| Brecha | Por qué sigue abierta | Cómo se cierra |
| --- | --- | --- |
| Tarifas de 3PL, corredor, seguro, regente, contador, auditoría, fianzas | Nadie las publica; la auditoría no contacta a terceros | Los correos de cotización del documento 04, con la hoja de datos llena; tres 3PL y dos aseguradoras a la vez |
| Precio real de la fábrica, lote mínimo, vida útil, crédito | Depende de Rutul | Pasos 2, 3 y 7 del guion |
| Junta y finanzas de Bueno | Los espejos no coinciden y el informe del MCA es de pago | Pedir el DIR-12 y los estados auditados (paso 6 del guion); comprar el informe del MCA (unos US$10–30) si la contraparte demora |
| Si el regente del 3PL cubre a la agencia y si el depósito de un tercero vale como depósito propio | La norma no lo resuelve en una línea | Consulta escrita a la DNFD; preguntar a los 3PL en la cotización |
| Fecha exacta de vencimiento de la LPU 01-2026 y de la próxima LPU | La resolución de adjudicación no está en nuestro archivo | Descargar la resolución en PanamaCompra; vigilar el plan anual de compras de la CSS |
| Tarifa del laboratorio de referencia por producto | El IEA y el INDICASAT cotizan caso a caso | Correo del documento 04 a los dos laboratorios |
| Tasas de victoria y 1.8× como estudio independiente | No existe un estudio público | Presentarlas como análisis interno con metodología; actualizarlas con nuestras primeras 20 cotizaciones |
| Experiencia de la fábrica en Latinoamérica | No aparece en registros públicos a su nombre | Pedir números de registro o el distribuidor (paso 6) |

## Fuentes de esta auditoría

- Comunicados de la CSS: [3 de diciembre de 2025](https://prensa.css.gob.pa/2025/12/03/css-invertira-91-millones-de-dolares-en-compra-masiva-de-medicamentos/) · [6 de enero de 2026](https://prensa.css.gob.pa/2026/01/06/compras-estrategicas-de-medicamentos-logran-ahorro-record-de-b-37-4-millones/) · [26 de marzo de 2026](https://prensa.css.gob.pa/2026/03/26/llegan-miles-de-medicamentos-css-refuerza-a-nivel-nacional/)
- [PanamaCompra: cuadro de propuestas de la LPU 01-2026](https://apisv3.panamacompra.gob.pa/documentos-actos-publico/cuadroPropuesta/12/procesoVistaCuadroPropuesta/712894) · [pliego de la LPU 01-2026](https://apisv3.panamacompra.gob.pa/procesos-contratacion-archivos/v2/download-file-2325E044-04B2-F011-80EA-0017A477FC74-ZA-101-1AZ-8120731-ZA-101-1AZ-8120731)
- [La Prensa: presupuesto 2027 de la CSS](https://www.prensa.com/sociedad/presupuesto-2027-de-la-css-contempla-925-millones-menos-para-medicamentos/) · [Decisiones Panamá: unidades 2027](https://decisionespanama.com/css-proyecta-invertir-b-230-3-millones-en-medicamentos-en-2027-y-aumentar-7-2-las-unidades-dispensadas/) · [Panamá América: Contraloría, 4 de octubre de 2025](https://www.panamaamerica.com.pa/sociedad/gestiones-de-cobro-en-la-contraloria-pasan-de-1885-dias-en-la-administracion-cortizo-54)
- [Ley 419 de 2024, texto (vLex)](https://vlex.com.pa/vid/ley-n-419-regula-1089176602) · [Decreto Ejecutivo 27 de 2024](https://www.minsa.gob.pa/sites/default/files/general/decreto_ejecutivo_27_de_10_de_mayo_de_2024.pdf) · [Resolución 985 de 2025](https://www.minsa.gob.pa/sites/default/files/general/resolucion_985_go30317_08072025.pdf) · [Ley 22 de 2006, texto único](https://www.dgcp.gob.pa/images/legislacion/leyes/2024/TEXTO%20UNICO%20Ley%2022%20DGCP%202023.pdf)
- [CMA CGM FAK junio de 2026](https://container-news.com/cma-cgm-raises-fak-rates-from-indian-subcontinent-to-latin-america-europe-and-north-africa/) · [febrero de 2026](https://container-news.com/cma-cgm-updates-fak-rates-from-indian-subcontinent-to-latin-america/) · [Maersk THC Panamá](https://www.maersk.com/news/articles/2026/09/16/terminal-handling-service-revision-panama)
- [Zauba Corp: Bueno Salud Care](https://www.zaubacorp.com/company/BUENO-SALUD-CARE-INDIA-PRIVATE-LIMITED/U24304GJ2016PTC094652) · [Tofler](https://www.tofler.in/bueno-salud-care-india-private-limited/company/U24304GJ2016PTC094652) · [AllIndiaITR](https://www.allindiaitr.com/company/bueno-salud-care-india-private-limited/U24304GJ2016PTC094652) · [Tracxn](https://tracxn.com/d/legal-entities/india/bueno-salud-care-india-private-limited/__QkyE0fWHXfeIPptyCGSAs34b_zI2Ih3d3EQ5h30DeaY) · [Falconebiz](https://www.falconebiz.com/company/BUENO-SALUD-CARE-INDIA-PRIVATE-LIMITED-U24304GJ2016PTC094652)
- [BP Logistics: instalaciones](https://www.bplogistics.com.pa/instalaciones/) · [Revista E&N: ampliación de BP Logistics](https://www.revistaeyn.com/empresasymanagement/bp-logistics-amplia-su-centro-de-distribucion-en-panama-pacifico-BJ23915163) · [Interworld Freight: almacén farmacéutico](https://interwf.com/es/servicios/almacenamiento/farmaceutico/panama) · [CBRE vía The Logistics World: alquiler de bodegas en Panamá](https://thelogisticsworld.com/actualidad-logistica/alza-de-precios-en-el-alquiler-de-bodegas-y-almacenes-industriales-en-panama)
- Las demás fuentes de la capa 1 están al final de cada documento del paquete y en las bitácoras del respaldo del código.
"""


# ---------- 01: identity chain (8 Oct, question from Jaime) ----------
IDENTIDAD = """## Cómo sabemos que es el mismo Rutul Patel

Hay muchas personas con ese nombre. La cadena que une al Rutul que negocia con nosotros con los registros revisados es esta, eslabón por eslabón, con su confianza:

| Eslabón | Evidencia | Confianza |
| --- | --- | --- |
| El Rutul que nos escribe es el de Zywie Worldwide | Él mismo lo dice; la propuesta de SignatureLex está hecha para «Zywie Worldwide Panamá»; la lista de productos que mandó es la «Product List PICS 2026» de Zywie | Alta |
| Zywie Worldwide (Vapi, Gujarat; GST 24AACFZ1221A1ZY, sociedad de personas registrada en 2018) es de Rutul Divyakant Patel | El perfil de Zywie en IndiaMART nombra como contacto a «Rutul Divyakant Patel (Director)»; el nombre completo con el segundo nombre es mucho menos común que «Rutul Patel» | Alta |
| El Rutul Divyakant Patel con DIN 05194106 (socio designado de Nosher Pharmaceutical LLP desde 2018 y director de Shape Wellness Pvt Ltd desde 2025) es la misma persona | Mismo nombre completo, mismo estado (Gujarat), mismo sector (farmacéutico), empresas en Ahmedabad; Nosher tiene registrado en el MCA un correo de Gmail formado con su nombre y su inicial | Media-Alta: coincidencia fuerte, sin un documento que la cierre |
| Deepti Rutul Patel (directora de Bueno según dos espejos del registro) está relacionada con él | En Gujarat el segundo nombre de una mujer casada suele ser el nombre del esposo; es una convención, no una prueba, y dos espejos no la muestran como directora | Media-Baja: inferencia |

Cómo cerrar la cadena sin preguntar nada incómodo: comparar el correo que Rutul usa con nosotros con el correo registrado de Nosher en el MCA (visible en Tofler); pedir, dentro del KYC del paso 6 del guion, el certificado de constitución de Zywie con la lista de socios (y, si lo ofrece, su DIN); y revisar si su perfil profesional público menciona Nosher o Shape Wellness. Si el correo coincide, los tres primeros eslabones quedan en confianza alta; el cuarto solo lo cierra la lista de directores de Bueno."""


# ---------- 8 Oct (tarde): FOB references vs Indian customs data ----------
VERIF_PRECIOS = """## Verificación adicional del 8 de octubre: las referencias FOB contra datos de aduana india

El eslabón más débil del modelo es el precio de fábrica, porque Rutul no ha mandado la lista y las referencias salen de licitaciones domésticas indias (TNMSC 2024, Delhi 2022) y del programa estatal Jan Aushadhi. Para medir qué tan lejos pueden estar de un precio de exportación real, se compararon con la muestra pública de declaraciones de exportación de India que publica Seair (datos de aduana; la muestra gratuita es de octubre–noviembre de 2016, así que sirve para el orden de magnitud, no para la cifra exacta) y con los precios adjudicados en Panamá que ya usa el modelo.

| Producto | Referencia FOB del modelo (US$) | Exportaciones indias en la muestra (US$ FOB por unidad) | Adjudicado en Panamá (CSS / MINSA) | Lectura |
| --- | --- | --- | --- | --- |
| Paracetamol 500 mg tableta | 0.0040 | 0.0032–0.0054 por tableta (Kenia, Sudáfrica, Reino Unido, Chile) | 0.010 / 0.020 | Consistente |
| Ceftriaxona 1 g vial | 0.20 (muestras 2023–2025 de 0.21–0.37 ya consideradas) | 0.75–0.92 por vial a México (producto de marca registrado allá, cuando el principio activo estaba caro) | 0.239–0.25 / 0.613 | La CSS adjudicó a 0.239, lo que implica un FOB de 0.18 o menos de algún competidor: la referencia es coherente con el mercado panameño; el margen está solo en el canal del MINSA |
| Albendazol 400 mg/10 ml | 0.08 | 0.089 (Senegal, misma presentación) | 1.81–1.86 / 1.62 | Consistente |
| Mebendazol 100 mg tableta | 0.008 | 0.0033–0.0119 por tableta | 0.13 / 0.164 | Consistente |
| Nistatina suspensión 30 ml | 0.40 (supuesto sin fuente) | 0.28–0.45 por frasco (cinco destinos) | 3.18–3.39 / 3.18 | El supuesto pasa de Baja a Media |
| Hidrocortisona 1% crema 15 g | 0.16 | 0.19–0.38 por tubo de 15 g | 0.555–0.58 / 1.875 | Posiblemente bajo |
| Mometasona 0.1% crema 15 g | 0.097 (derivado del precio Jan Aushadhi) | 0.46–2.39 por tubo; lo más frecuente 1.21–1.50 | 1.02 (y 0.65) / 3.66 | Probablemente bajo: Jan Aushadhi es un programa estatal de bajo costo, no un precio de exportación |
| Paracetamol jarabe, amoxicilina-clavulánico (tableta y suspensión), cefotaxima | — | Sin datos en la muestra gratuita | — | Pendiente: solo la lista de la fábrica los resuelve |

Efecto en el caso base si las dos cremas costaran lo que muestra la aduana (mometasona 0.60 e hidrocortisona 0.28 por tubo): el VPN al 15% pasa de −B/.56 mil a −B/.77 mil, la TIR de 6.8% a 3.3% y las ventas del año 3 de B/.265 mil a B/.248 mil; sin las dos cremas en la primera ola, −B/.66 mil y 4.6%. El veredicto no cambia (el caso base ya era negativo), pero la brecha crece, y confirma la regla del plan: ningún registro se paga antes de tener la lista de precios FOB (paso 3 del guion). Mientras no llegue, el margen de las dos cremas se trata como no verificado y las cuatro referencias consistentes suben a confianza Media.
"""

VERIF_03_PARA = ("Verificación del 8 de octubre contra datos de aduana india (ver 07_Auditoria_y_confianza): las referencias de paracetamol, albendazol, mebendazol y nistatina coinciden con precios reales de exportación; las de las dos cremas (mometasona e hidrocortisona) parecen bajas. Con las cremas al precio de aduana, el VPN del caso base baja de −B/.56 mil a −B/.77 mil y la TIR de 6.8% a 3.3%; por eso la lista de precios de la fábrica decide qué entra en la primera ola.")

VERIF_FUENTES = ("- Datos de aduana india (muestra pública, 2016): Seair, exportaciones de [paracetamol tabletas](https://www.seair.co.in/product-export-data/paracetamol-tablets-export-data.aspx) · [ceftriaxona a México](https://www.seair.co.in/ceftriaxone-export-data/hs-code-30042019/country-mexico.aspx) · [albendazol suspensión](https://www.seair.co.in/product-export-data/albendazole-suspension-export-data.aspx) · [mebendazol tabletas](https://www.seair.co.in/product-export-data/mebendazole-tablets-export-data.aspx) · [nistatina suspensión](https://www.seair.co.in/product-export-data/nystatin-oral-suspension-export-data.aspx) · [hidrocortisona crema](https://www.seair.co.in/product-export-data/hydrocortisone-cream-export-data.aspx) · [mometasona crema](https://www.seair.co.in/product-export-data/mometasone-furoate-cream-export-data.aspx)\n")

PLAN_REPL.append(("Preguntas abiertas:", VERIF_03_PARA + "\n\nPreguntas abiertas:"))
