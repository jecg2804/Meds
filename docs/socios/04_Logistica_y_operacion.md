# Logística y operación

*Preparado el 7 de octubre de 2026 y revisado el 9 de octubre de 2026 tras una auditoría independiente (ver 07_Auditoria_y_confianza.md) para los socios panameños del proyecto. Uso interno: no se comparte con Rutul Patel ni con terceros. Las cifras financieras salen del modelo (Modelo_financiero_socios.xlsx; dónde está, en LEAME.md) y de las fuentes citadas al final de cada documento; toda cifra sin cotización firme está marcada como estimación o supuesto.*

## Operación

La operación cabe en un 3PL licenciado; el cuello de botella es la vida útil: los pliegos exigen 18 meses al entregar, así que un producto de 24 meses solo puede pasar 2.75 meses en bodega.

Flujo: orden a Bueno → producción y liberación → embarque → tránsito y aduana → cuarentena y liberación por el regente en el 3PL → oferta → orden de compra → entrega en el almacén de la CSS o del MINSA → recibido conforme → cuenta → cobro. Fuera de las compras por desabastecimiento crítico declarado (DE 27, arts. 824–829), que este plan no usaría, no se puede importar sin registro sanitario; por eso la primera venta llega un ciclo de reposición después del registro.

| Vida útil aprobada | Máximo en bodega para cumplir 18 meses | Política de reposición |
| --- | --- | --- |
| 24 meses | 2.75 meses | Mensual, por carga consolidada; inventario de 1.5 meses o menos |
| 30 meses | 8.75 meses | Bimestral |
| 36 meses | 14.75 meses | Trimestral, en contenedor de 20 pies |

Cálculo: vida útil − 18 meses exigidos − 1 mes de liberación en fábrica − 2 meses de tránsito y aduana − 0.25 meses de pedido a entrega. Regla de la columna «Política de reposición»: la permanencia máxima en bodega debe cubrir el intervalo entre embarques más la cobertura de inventario; con 24 meses solo cabe un embarque mensual con 1.5 meses de cobertura; con 30, uno cada dos meses con los 3 meses de cobertura del caso base; con 36, uno trimestral en contenedor. La vida útil aprobada de cada producto todavía no se conoce: hay que pedírsela a Bueno junto con el lote mínimo de fabricación.

Volumen físico de los 11 productos en madurez (caso base): unos 74 m³ y 38 tarimas al año, es decir, unas 3 tarimas al mes (un contenedor de 20 pies lleva 10). El jarabe de paracetamol es 48% del volumen y 18% de las ventas, así que el flete pesa más en líquidos que en tabletas. El lote económico (calculado con un costo fijo de US$1,000 por embarque, 15% anual de costo de tenencia más almacenamiento y 3% de merma) es de unos 19 m³ por embarque (4 al año), justo un contenedor de 20 pies, que sale a unos US$251 por m³ contra US$302 en carga consolidada.

Inventario del caso base: tres meses de cobertura para compras menores (las entregas se piden en días) y dos meses en contratos de precio único (la LPU exige al menos uno), con reposición mensual en carga consolidada. Eso supone 30 meses o más de vida útil: con 24 meses la cobertura tendría que bajar a 1.5 meses, y el embarque trimestral en contenedor solo cabe con 36 meses. Despacho por fecha de vencimiento. El pliego de la LPU exige que el empaque secundario lleve impreso el número de la licitación y no acepta reetiquetado ni sobreetiquetado; el del MINSA exige el rotulado de propiedad del MINSA. Cada canal necesita su corrida de empaque en fábrica y el lote mínimo puede dejar inventario varado.

A este volumen la bodega propia no tiene sentido (la comparación está en la sección «Estimación de costos logísticos»). Los operadores que ya alojan más agencias con licencia de la DNFD son J. Cain (24), Panalog/Farmazona (22), DHL (16), Osala (15), Grupo TLA (11) y BP Logistics (8). En la fase 0 basta una cotización indicativa del 3PL; la firme hace falta en la fase 1.

Roles mínimos: regente (al menos 4 horas diarias), coordinador de licitaciones que vigile PanamaCompra a diario y arme cotizaciones, logística, cobros (cuentas y gestión de cobro) y farmacovigilancia.

## Cotizar el 3PL: con quién y cómo

Qué contrata la S.A. cuando contrata un 3PL farmacéutico:

- Lo que hace: su bodega tiene licencia de la DNFD y se declara como el depósito de nuestra agencia; recibe el contenedor (con su corredor de aduana o el nuestro), lo pone en cuarentena hasta que el regente libera, almacena por lote y vencimiento, prepara los despachos por cajas y entrega en los almacenes de la CSS o del MINSA con nuestros documentos.
- Lo que cobra: al mes por posición de tarima, por recepción y por despacho; aparte el etiquetado u otros servicios; casi siempre con un mínimo mensual.
- Lo que no hace: la licencia, el regente, los registros, las ofertas y la factura al Estado siguen siendo de la S.A.
- El flujo de una venta: orden de compra de la entidad a la S.A. → instrucción de la S.A. al 3PL → entrega del 3PL con acta de recibido → factura de la S.A. → cuenta en la entidad → cobro.

Estado de las cotizaciones: antes del 8 de octubre solo se había intercambiado el cuestionario operativo de BP Logistics, lleno con estimaciones y sin fichas de producto, sin llegar a una cotización. El 8 de octubre de 2026 se enviaron solicitudes de cotización indicativa, o de tarifario estándar, a los cuatro operadores con correo público (J. Cain, Osala, DSV e Interworld); J. Cain respondió el 9 de octubre proponiendo una videollamada para el 14. BP Logistics recibe por formulario web o WhatsApp, DHL solo por formulario web y Farmazona por WhatsApp. La ficha logística por producto se les manda cuando la fábrica llene la hoja de datos, y con ella se pide la cotización firme. El detalle de cada operador, las respuestas al formulario de BP Logistics y la tabla de seguimiento están en Cotizaciones_3PL_seguimiento.md.

| Operador | Dónde | Evidencia pública (licencia, certificados) | Agencias con licencia que aloja (lista DNFD, 28-sep-2026) | Estado al 9 de octubre |
| --- | --- | --- | --- | --- |
| J. Cain & Cía | Zona Libre de Colón y Panamá Pacífico | Licencias de agencia 13-005 A (Panamá Pacífico) y 3-001 (Colón); licencias MINSA 3-009 L y 13-001 LA; certificado BPM de acondicionamiento vigente a julio de 2027; INVIMA a diciembre de 2028; áreas de 2–8 y 15–25 °C | 24 | Correo enviado; respondió el 9 de octubre: videollamada propuesta para el 14 |
| Osala Logistics (Bomi Group / UPS Healthcare) | Terminal de carga de Tocumen, depósito aduanero logístico | Publica certificación DNFD de importación, almacenamiento y distribución de medicamentos con cadena de frío; ISO 9001 y 13485 | 15 | Correo enviado |
| DSV Panamá | Zona Libre de Colón | 8,000 m² y 3,500 posiciones; sistema de calidad para salud; sin licencia DNFD publicada | — | Correo enviado |
| Interworld Freight Panamá | Panamá, en bodega de un socio | Almacén farmacéutico de 2–8 y 15–25 °C; sin licencia DNFD visible | — | Correo enviado; pedir el número de licencia |
| BP Logistics (Grupo Hilasal) | Panamá Pacífico | Licencia de agencia 13-031 A (vence el 16 de diciembre de 2026); licencia MINSA 13-006 LA; certificado BPM 012-23 con vencimiento el 25 de octubre de 2025 en la lista (confirmar renovación); 15–25 y 2–8 °C | 8 | Formulario web de 13 preguntas con las respuestas listas (Cotizaciones_3PL_seguimiento.md); ya recibió nuestro cuestionario operativo con estimaciones |
| DHL (Global Forwarding Panamá; Supply Chain) | Parque Industrial Sur, Tocumen | Licencia MINSA 8-236 L; certificado BPM de acondicionamiento 015-24 a agosto de 2026 (vencido en la lista; confirmar renovación) | 16 | Formulario web pendiente |
| Farmazona / FZ Logistics (Panalog) | Fuerte Davis, Colón | Licencia MINSA 3-011 L; certificado BPM 021-24 a noviembre de 2026; INVIMA a mayo de 2029 | 22 | WhatsApp pendiente (mensaje listo) |
| Grupo TLA | Panamá Pacífico | Licencias propias 13-000 y 13-132 (lista de la DNFD, 28 de septiembre de 2026); aloja a Vanguard Medical Logistics (Promed), licencia 13-012 LA | 11 | Baja prioridad |
| Alliance Transport Logistics (Grupo ALG) · Master Logistic Solutions · Kuehne+Nagel · FedEx Logistics Center | Panamá Pacífico y Tocumen | Licencias 13-002 LA y 13-003 LA (los dos primeros); áreas de 2–8 y 15–25 °C y CEIV Pharma (los dos últimos) | 7 y 4 (los dos primeros) | Segunda ronda, si los cuatro primeros no responden |

Nota: la lista de establecimientos con licencia de la DNFD (28 de septiembre de 2026) incluye las licencias de agencia de los propios operadores (J. Cain Panamá Pacífico 13-005 A y J. Cain & Co. 3-001; BP Logistics 13-031 A, que vence el 16 de diciembre de 2026; Grupo TLA 13-000 y 13-132); las licencias «L» y «LA» de la tabla vienen de la lista de laboratorios acondicionadores con certificado de BPM. Que un operador no aparezca en una lista no significa que no tenga licencia de almacenamiento: por eso el correo pide el número de licencia.

Dos preguntas que ningún operador contesta solo y que van en paralelo a la DNFD por consulta escrita: si el depósito del 3PL puede declararse como depósito de la agencia y si el regente del operador puede cubrir a una agencia nueva o cada agencia necesita el suyo (DE 27, arts. 382 y 396–398). La respuesta define el costo fijo más grande después del coordinador.

## La hoja de datos de fábrica y el cuestionario del 3PL

Los operadores logísticos cotizan por posición de tarima, por manejo y por servicios; la naviera y el consolidador por metro cúbico y peso; la aseguradora por valor CIF. Ninguno cotiza sobre estimaciones. El cuestionario operativo de BP Logistics pide pesos, dimensiones, volumen, valor por embarque, sensibilidad, control por lote, fichas técnicas y fotos: casi todo depende de la fábrica (por ser un formulario con la marca de ese operador, no se le manda a Rutul).

Por eso la hoja Factory_data_for_3PL_quote.xlsx pide, por producto: unidades por empaque, empaques por caja máster, dimensiones y peso de la caja, cajas por tarima, condiciones de almacenamiento, vida útil aprobada y mínima garantizada al embarcar, código arancelario, planta, tamaño de lote, lote mínimo, tiempo de entrega, precio FOB, y si hay CPP, hoja de seguridad y fotos; y, por embarque: incoterm, puerto, tipo de tarima, valor, documentos que viajan con la carga y si pueden imprimir el número de licitación en el empaque. Con esa hoja llena se afinan las cotizaciones indicativas ya pedidas y se pide la firme (el correo enviado está en la sección «Correos de cotización»).

## Estimación de costos logísticos mientras no haya cotización firme

Ningún operador logístico de Panamá publica tarifas. La tabla separa lo que es tarifa publicada (defendible con un enlace), lo que es referencia pública indirecta y lo que es un supuesto presupuestario nuestro. Las cifras se reemplazan por las cotizaciones en cuanto lleguen.

| Concepto | Estimación | Naturaleza de la cifra | Base |
| --- | --- | --- | --- |
| Almacenamiento y manejo en un 3PL licenciado: 5–15 tarimas, 15–25 °C, control por lote y vencimiento, 2–4 despachos al mes | B/.300–1,200 al mes; el modelo usa B/.600 (cuota mínima) | **Supuesto presupuestario** | Construido con el alquiler de bodega en Panamá (CBRE, 2H2022: clase A US$7.05 y clase B US$5.05 por m² al mes), la densidad de un rack de tarimas y la estructura tarifaria que usan los 3PL (recepción + posición de tarima al mes + picking por caja, con mínimo mensual); ningún 3PL de Panamá publica tarifas |
| Flete marítimo en contenedor de 20 pies India–Manzanillo | US$3,750 de flete (tarifa FAK de CMA CGM vigente desde el 10 de junio de 2026; US$2,600 en febrero, +44%), sin THC ni recargos | **Tarifa publicada** (prensa especializada que reproduce el aviso de la naviera) | [Container News, junio de 2026](https://container-news.com/cma-cgm-raises-fak-rates-from-indian-subcontinent-to-latin-america-europe-and-north-africa/) · [febrero de 2026](https://container-news.com/cma-cgm-updates-fak-rates-from-indian-subcontinent-to-latin-america/); la tarifa de octubre de 2026 puede ser distinta |
| Cargo de manejo en terminal (THC/DHC) en Manzanillo | US$275 por contenedor seco desde el 15 de octubre de 2026 | **Tarifa publicada** | [Maersk, aviso del 16 de septiembre de 2026](https://www.maersk.com/news/articles/2026/09/16/terminal-handling-service-revision-panama) |
| Carga consolidada (LCL), unos 10 m³ por embarque al inicio | US$200 por m³ de flete más unos US$100 de desconsolidación, destino y entrega local (el modelo usa US$300 por m³ puesto en bodega) | **Referencia indirecta** | Desconsolidación US$0.20 por pie cúbico (mínimo US$55 por embarque) en el tarifario de destino de Crowley Panamá; una cotización privada de 2025 cobra US$86.5 por m³; el flete por m³ es un supuesto derivado de la tarifa FAK por contenedor y de referencias LCL India–EE. UU. y Europa (US$65–160 por m³) |
| Corredor de aduana | B/.50 + 0.15% del valor CIF + B/.2 por línea; unos B/.200–350 por embarque de 11 productos | **Honorario mínimo legal** (Ley 20 de 1994); el honorario real se cotiza | Texto de la ley; ningún corredor publica tarifas |
| Autorización de importación de la DNFD por embarque | Sin tasa para no controlados; hasta 3 días hábiles | **Norma** | DE 27 de 2024, art. 364 |
| Seguro de carga | 0.3–0.5% del valor CIF, dentro de los US$300 por m³ del modelo (los B/.100 al mes de los costos fijos son el seguro de responsabilidad civil y de producto) | **Supuesto** | Práctica de mercado; cotizar |
| Entregas a los almacenes de la CSS y del MINSA | 4% de las ventas en el modelo | **Supuesto** | Los operadores que ofrecen distribución local lo cotizan por entrega; el correo lo pide |
| Primer embarque de 5 tarimas (unos 10 m³) puesto en bodega, sin contar la mercancía | Unos US$2,900–3,100 en el caso base: flete 1,900–2,000 (US$200 por m³), desconsolidación, destino y entrega local unos 750, corredor unos 200 y seguro unos 70; en el escenario alto, unos US$4,500 (US$470 por m³) | **Estimación compuesta** | Suma de las líneas anteriores |

Comparación con una bodega propia, sin contar el regente que ambas necesitan: con 5 tarimas, un 3PL cuesta unos B/.680 al mes contra B/.4,030 más B/.37 mil de inversión en bodega propia; con 15 tarimas, B/.960 contra B/.5,920 más B/.54 mil. Es una estimación propia (alquiler CBRE, aire acondicionado, personal, equipo); a este volumen la bodega propia no tiene sentido con ningún supuesto razonable.

Qué se le puede decir a Rutul y cómo defenderlo: las cifras de flete y de THC son avisos públicos de las navieras, con fecha; el almacenamiento es nuestro presupuesto de trabajo mientras los 3PL no coticen, y así hay que presentarlo. Si pregunta de dónde salen los números, la respuesta es exactamente esa: «freight and terminal charges are published carrier notices (CMA CGM June 2026, Maersk October 2026); the storage range is our budget assumption, built from Panama warehouse rent benchmarks and the way 3PLs price (receiving, pallet position, picking); it is not a quote, which is why we need the factory data».

## Correos de cotización

El correo a los operadores logísticos se envió el 8 de octubre de 2026 desde el correo de Jaime a J. Cain, Osala, DSV e Interworld; el mismo texto sirve para la segunda ronda. Los correos a las aseguradoras de fianzas y al IEA salen desde el correo de Jaime cuando él apruebe el texto (regla desde el 9 de octubre: ninguna comunicación externa sale sin su revisión). Pedir a varios a la vez y decirlo. Nota sobre el correo enviado: dice «unos 9 m³»; 5 tarimas de 1.2 × 1.0 × 1.6 m son 9.6 m³ y el cuestionario anterior decía 10; la cotización firme lleva la cifra exacta con la hoja de datos.

### A los operadores logísticos (enviado el 8 de octubre de 2026)

```text
Asunto: Solicitud de cotización indicativa – almacenamiento y distribución de medicamentos (agencia en constitución)

Estimados señores de (nombre del operador):

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

### A la aseguradora de fianzas (Mapfre, Internacional, ASSA, Interamericana de Fianzas)

```text
Asunto: Consulta de requisitos y tarifas – fianzas de propuesta y cumplimiento para licitaciones de medicamentos

Estimados:

Somos una sociedad en constitución que participará en licitaciones de medicamentos de la CSS (fianza de propuesta de 10% por 180 días hábiles y de cumplimiento de 30% por 18 meses) y en subastas del MINSA (cumplimiento de 20%). Montos iniciales estimados entre B/.20,000 y B/.150,000 por fianza (por ejemplo, un renglón de paracetamol de la LPU de unos B/.226 mil al precio de oferta del modelo exige una fianza de cumplimiento de 30%, unos B/.68 mil).

Agradecemos indicarnos: requisitos para una empresa nueva (estados financieros, codeudores, contragarantías), porcentaje de colateral líquido o bancario que exigirían, tasa anual de prima por tipo de fianza, costo mínimo por fianza y tiempo de emisión una vez aprobada la línea.
```

### Al Instituto Especializado de Análisis (Universidad de Panamá)

```text
Asunto: Cotización de análisis de control previo para registro sanitario – 11 productos

Estimados:

Para el registro sanitario por ruta ordinaria de 11 medicamentos de síntesis química fabricados en India, agradecemos cotizar el análisis de control previo por producto y forma farmacéutica: paracetamol 500 mg tableta y jarabe 120–160 mg/5 ml; amoxicilina con ácido clavulánico 500/125 mg tableta y 400/57 mg/5 ml polvo para suspensión; ceftriaxona 1 g y cefotaxima 1 g polvo para inyección; albendazol suspensión; mebendazol 100 mg tableta; nistatina suspensión; hidrocortisona crema (concentración por confirmar con la fábrica); mometasona 0.1% crema.

Agradecemos indicar también qué patrones de referencia y cantidad de muestra debe aportar el solicitante, y el tiempo estimado de análisis.
```

## Fuentes

Costos y logística

- [TNMSC, licitación e-018 de 2024 (precios de referencia en India)](https://tnmsc.tn.gov.in/linkfiles/news_events/N2502472.pdf) · [Contrato de precios de hospitales de Delhi, 2022](https://dgehs.delhi.gov.in/sites/default/files/inline-files/rc2.pdf) · [Lista de precios de Jan Aushadhi (espejo)](https://sarkariyojana.com/jan-aushadhi-products-medicines-list-with-price-drug-code/)
- [Fletes CMA CGM del subcontinente indio a Manzanillo, marzo de 2026](https://www.ajot.com/news/cma-cgm-fak-rates-from-the-indian-subcontinent-to-latin-america-as-of-march-15th-2026) · [junio de 2026](https://container-news.com/cma-cgm-raises-fak-rates-from-indian-subcontinent-to-latin-america-europe-and-north-africa/) · [Maersk: THC en Panamá desde octubre de 2026](https://www.maersk.com/news/articles/2026/09/16/terminal-handling-service-revision-panama) · [Tarifas de destino de Crowley en Panamá](https://www.crowley.com/wp-content/uploads/sites/7/2023/10/Destination-Handling-Charge-DHC-23rd-Revised.pdf) · [Ley 20 de 1994: honorarios mínimos de corredores de aduana](https://docs.panama.justia.com/federales/leyes/20-de-1994-aug-16-1994.pdf)
- Fianzas: [Superintendencia de Seguros, primas por ramo a diciembre de 2025](https://www.superseguros.gob.pa/wp-content/uploads/DES-PP-12-2025.pdf) · [Internacional de Seguros: requisitos para fianzas de persona jurídica](https://iseguros.com/Formularios/Asegurados/Fianzas/Requisitos-de-Persona-Juridica.pdf) · [ASSA: evaluación de fianzas de cumplimiento](https://www.assanet.com/formularios/C-Evaluacion-y-Tramite-de-Fianzas-de-Cumplimiento1.pdf)
- [DNFD: establecimientos con licencia al 28 de septiembre de 2026](https://dnfd.minsa.gob.pa/)
- Documentos del proyecto: propuesta y tabla de honorarios de SignatureLex, lista de productos de Zywie, catálogo de Modi, Decreto Ejecutivo 16 de 2026 y cuestionario de BP Logistics.

Compras públicas

- [LPU 01-2026 de la CSS: cuadro de propuestas](https://apisv3.panamacompra.gob.pa/documentos-actos-publico/cuadroPropuesta/12/procesoVistaCuadroPropuesta/712894) · [pliego](https://apisv3.panamacompra.gob.pa/procesos-contratacion-archivos/v2/download-file-2325E044-04B2-F011-80EA-0017A477FC74-ZA-101-1AZ-8120731-ZA-101-1AZ-8120731) (fianzas, pago, compra mínima, carta del fabricante y empaque: cláusulas 8, 11, 13, 18 y 24 y contrato modelo)
- [LPU 11-2026 de la CSS: cuadro de propuestas](https://apisv3.panamacompra.gob.pa/documentos-actos-publico/cuadroPropuesta/12/procesoVistaCuadroPropuesta/712187)
- [Pliego de subasta en reversa del MINSA 2026](https://apisv3.panamacompra.gob.pa/procesos-contratacion-archivos/v2/download-file-41E2472E-8233-F111-80EA-0017A477FC74-ZA-101-1AZ-9715601-ZA-101-1AZ-9715601) · [resultado del jarabe de paracetamol](https://apisv3.panamacompra.gob.pa/procesos-contratacion-archivos/v2/download-file-21F2213F-5354-F111-80EB-0017A477FC64-ZA-101-1AZ-10368555-ZA-101-1AZ-10368555) · [PanamaCompra: búsqueda de actos](https://www.panamacompra.gob.pa/) (33 subastas del MINSA de junio al 6 de octubre de 2026; sin acto de compra conjunta)
- [Decreto Ejecutivo 16 de 2026, listado conjunto de desabastecimiento crítico](https://www.minsa.gob.pa/normatividad/decreto-ejecutivo-ndeg-16-lunes-09-de-marzo-2026-que-declara-el-listado-conjunto-de) · Pliego de la compra conjunta 2024: enlace de PanamaCompra caído al 7 de octubre de 2026
- [ANTAI: reportes mensuales de contrataciones de la CSS, el MINSA y los patronatos](https://monitoreo.antai.gob.pa/)
- Comunicados de la CSS: [3 de diciembre de 2025, LPU por B/.91.98 millones y 348 renglones](https://prensa.css.gob.pa/2025/12/03/css-invertira-91-millones-de-dolares-en-compra-masiva-de-medicamentos/) · [6 de enero de 2026, ahorro de B/.37.4 millones](https://prensa.css.gob.pa/2026/01/06/compras-estrategicas-de-medicamentos-logran-ahorro-record-de-b-37-4-millones/) · [26 de marzo de 2026, 282 renglones adjudicados por B/.77.9 millones](https://prensa.css.gob.pa/2026/03/26/llegan-miles-de-medicamentos-css-refuerza-a-nivel-nacional/) · PanamaCompra, búsqueda pública de procesos (estado «Adjudicado» de la LPU 01-2026 el 15 de mayo de 2026 y de la LPU 11-2026 el 31 de agosto de 2026; 33 subastas en reversa del MINSA en 2026)

- Seguimiento de las cotizaciones de 3PL: Cotizaciones_3PL_seguimiento.md (canales, licencias, fechas y respuestas).
