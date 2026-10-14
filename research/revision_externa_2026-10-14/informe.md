# Revisión externa del plan «Med Tenders Panama»

*Revisor externo independiente, 14 de octubre de 2026. Fuentes públicas consultadas el 14-oct-2026 salvo otra fecha indicada. No modifiqué el repositorio. «Corrida del revisor» = copia del modelo del paquete con el cambio indicado.*

## 1. Veredicto

**La conclusión económica se sostiene; el análisis legal no.**

- **Economía.** El paquete es riguroso: trazable (487 afirmaciones con fuente), con simulación por estructura, compuertas y techos por producto, y sin apoyarse en contactos. Tiene supuestos pesimistas (colateral de 75% en efectivo, sin factoring, portafolio recortado sin razón, costos fijos nueve meses antes de vender) y optimistas (22% de las compras menores, lotes mínimos no modelados, tiempo de los socios gratis). Corregí todo lo que favorece al negocio en la estructura D: el valor presente sigue negativo (−B/.31 mil a −B/.89 mil) y la probabilidad de perder más que la fase 0 queda en 61%. No constituir es correcto.
- **Lo que decide.** El paquete trata el parentesco como una duda de la Ley 316. Omite la **Ley 419 de 2024, art. 249.2**: son *incompatibles para contratar con las instituciones públicas de salud* los parientes **hasta el cuarto grado de consanguinidad** de los miembros de junta directiva, dirección o cargos administrativos de esas instituciones. Un sobrino es tercer grado; el ministro dirige el MINSA e integra la Junta Directiva de la CSS. El **DE 27 de 2024, art. 791**, ordena desestimar la propuesta del incompatible. La única duda real es si la norma alcanza a una S.A. a través de sus accionistas; la lectura prudente, y la de un competidor que impugne, es que sí.
- **Recomendación.** Detener todo gasto salvo la opinión legal, y que empiece por el art. 249. Si confirma la lectura prudente, quedan tres caminos: (a) una S.A. sin Jaime ni Juan Luis, sin acciones, cargos ni beneficio económico; (b) solo el canal privado, que otro agente estudia; (c) esperar a que el ministro deje el cargo y avanzar mientras tanto con registros. Con el capital disponible, la mejor estructura no es la D: es la E (la S.A. tiene los registros y un distribuidor establecido vende) con registros pagados por la fábrica, que pide B/.36–50 mil (sección 8).

## 2. Errores encontrados en el paquete

| # | Dónde | Qué dice | Qué debería decir | Fuente |
| --- | --- | --- | --- | --- |
| 1 | Doc. 2 §2, doc. 1 «Compuerta legal», doc. 5 §3.5 | La compuerta descansa en la Ley 316, con «argumentos en los dos sentidos» | Abrir con la Ley 419, art. 249.2 (cuarto grado) y el DE 27, art. 791. La Ley 462 de 2025 (art. 243) modificó los arts. 1, 46, 47, 237 y 261–264 de la Ley 419, no el 249 | Ley 419, G.O. 29962-A, pp. 75–76: <https://dnfd.minsa.gob.pa/sites/default/files/2025-08/Ley%20419%20de%201%20de%20febrero%20de%202024.pdf>; DE 27: <https://www.minsa.gob.pa/sites/default/files/general/decreto_ejecutivo_27_de_10_de_mayo_de_2024.pdf>; Ley 462: <https://www.css.gob.pa/wp-content/uploads/2025/03/Ley-462-de-2025.pdf> |
| 2 | Doc. 2 §2 (fila «art. 13») y registro R1-37 | El impedimento «llega a familiares hasta el segundo grado»; el parentesco no está en el art. 24 de la Ley 22 | El art. 13 solo cubre empresas que el funcionario o sus parientes de segundo grado dirigieron o asesoraron **en los dos años previos a asumir el cargo**: no es un umbral general. Que la Ley 22 calle es irrelevante: el DE 27, art. 790, suma el art. 24 de la Ley 22 a la ley especial | Ley 316: <https://s3-legispan.asamblea.gob.pa/legispan/NORMAS/2020/2022/LEY/Administrador%20Legispan_29602-A_2022_8_18_ASAMBLEA%20NACIONAL_316.pdf> |
| 3 | Doc. 2 §3.3 y §5 | Primera ola limitada a productos del DE 16 | El DE 16 no importa para la LPU. El filtro excluyó la mayor oportunidad del catálogo: **amoxicilina 250 mg/5 ml en polvo** (renglón 27, 2 oferentes, B/.1.73, unos B/.262 mil al año, catálogo P-295, fuera de la Res. 985) y **clobetasol 0.05% en tubo de 25 g** (renglón 89, 2 oferentes, unos B/.45 mil) | Cuadro oficial (API): <https://apisv3.panamacompra.gob.pa/documentos-actos-publico/cuadroPropuesta/12/procesoVistaCuadroPropuesta/712894> |
| 4 | Doc. 2 §7.2 y anexo | «Ninguna aseguradora publica el porcentaje» de colateral | Internacional de Seguros publica que el colateral primario es pagaré con **codeudor solidario**; el efectivo, la garantía bancaria o la hipoteca dependen del tamaño de la fianza. El 75% en efectivo es conservador, pero el paquete omite que los socios responden con su patrimonio | <https://www.iseguros.com/Formularios/Asegurados/Fianzas/Requisitos-de-Persona-Juridica.pdf> (jun-2019) |
| 5 | Doc. 1 (tercera columna) y doc. 2 §1 | «D más sistema nervioso y coordinador sin sueldo» como caso casi viable | Depende de fabricantes desconocidos y de trabajo no pagado (unos B/.20 mil al año). No es comparable con las otras columnas | Doc. 3 §4 |
| 6 | Doc. 2 §9 y `mc.py` | Probabilidades de pérdida | Todas suponen que la compuerta legal ya se pasó: son condicionales a una opinión favorable | `mc.py` |
| 7 | Anexo, `penal` | La mora de 10% sale del art. 231 | Es el art. 232 de la Ley 419 | Ley 419 |

## 3. Supuestos del modelo que cuestiono

| Supuesto | Dirección | Evidencia y efecto (corrida del revisor) |
| --- | --- | --- |
| Costos fijos de B/.4,600 al mes | Monto algo optimista; fecha pesimista | Falta la gestión de cobros ante la CSS, el MINSA y la Contraloría, y un coordinador con experiencia en licitaciones y regulación cuesta más de B/.1,300. Pero los costos arrancan con la licencia (mes 3) y la primera venta es en el mes 12. Con la licencia en el mes 8: capital de B/.379 mil y valor presente de −B/.186 mil. Hay que confirmar con la DNFD si la licencia es requisito para presentar registros |
| Probabilidad de ganar un renglón: 30% | Neutral, regla rígida | Encaja con ofertar a 0.95 veces el precio vigente y con la descalificación de los nuevos: en la LPU 01-2026, la oferta más baja no ganó en nistatina (3.08) ni en jarabe (0.57). En renglones finos con ofertas pegadas a la referencia (mebendazol, mometasona, albendazol) se podría ofertar 40–60% más bajo con margen de más de 70% y ganar más. Con 45%: −B/.187 mil |
| 22% de las compras menores | Optimista | El 36.6% que lo respalda viene de actos centralizados del MINSA. Las compras menores de la CSS cayeron 50% y piden inventario y rapidez. Con 10%: −B/.227 mil |
| Índice de fábrica 1.25 sobre referencia × 1.4 | Neutral en precio, optimista en lotes | 1.75 veces la licitación india es plausible entre partes relacionadas. El modelo ignora el lote mínimo: se esperan unos 3,300 frascos de nistatina, 8,400 de albendazol y 1,300 de suspensión de amoxicilina con clavulánico al año, con empaque impreso con el número del acto. Las mermas pueden superar el 4% |
| Colateral de 75% | Pesimista en efectivo; omite el riesgo personal | Ver error 4. Con 25%: capital de B/.312 mil y valor presente de −B/.173 mil. Pero los codeudores panameños responden por el 100% de la fianza |
| 150 días de cobro | Razonable | El contrato paga a 90 días de aceptada la cuenta, más el refrendo. No hallé datos públicos de 2026; las deudas de B/.40–48 millones reportadas son de 2023-2024 |
| Ventas maduras de B/.171 mil | Pesimista por el portafolio | Con amoxicilina y clobetasol, las ventas del año 3 suben de B/.176 mil a B/.229 mil y el valor presente pasa de −B/.199 mil a −B/.167 mil |
| Demanda de la LPU 01-2026 y las subastas de 2026 | Neutral | Base prudente. Al 14-oct-2026 la API de PanamaCompra no muestra la LPU que reemplaza a la 01-2026: hay posibilidad de prórroga |
| Sin factoring | Pesimista en capital | La Ley 22, art. 97, permite ceder el crédito. Factorizar 80% de las ventas baja el capital de B/.393 mil a B/.352 mil con el mismo valor presente |

**Todo a favor a la vez** (la fábrica financia, amoxicilina y clobetasol, licencia en el mes 8, colateral de 50%, factoring): capital de B/.156 mil y valor presente de −B/.31 mil sin fallas. En la simulación de D (8,000 escenarios, sin factoring): 61% de perder más que la fase 0 (antes 81%), −B/.89 mil y capital de B/.254 mil (mediana) y B/.377 mil (p90). Cambia el tamaño, no el signo.

## 4. Conflicto de intereses

### 4.1 Lo que dicen las normas

- **Ley 316.**
  - Art. 2.1: el conflicto incluye los intereses «de sus familiares», sin grado. Art. 4: ministros y miembros de juntas de instituciones públicas son sujetos obligados.
  - **Art. 5:** deben declarar los «**accionistas, beneficiarios finales y apoderados**», directores y dignatarios de personas jurídicas adjudicatarias de licitaciones públicas. **Sí los alcanza.**
  - Art. 8: no se adjudican actos con conflicto entre un sujeto obligado de la entidad y el contratista; el funcionario debe apartarse.
  - Art. 16: nulidad absoluta y responsabilidad solidaria de la contratista por los daños. Art. 18.6: se declaran acciones en sociedades, fundaciones y fideicomisos.
  - Art. 25: multas de 2–4 meses de salario y vía penal si hay falsedad; pensado para funcionarios.
- **Ley 419.** El art. 249.2 trae la incompatibilidad hasta el cuarto grado. El art. 251 prohíbe a los servidores contratar «por interpuestas personas». El art. 182 adscribe la Comisión Nacional de Registro de Oferentes, donde la S.A. debe inscribirse, al Despacho Superior del MINSA. **DE 27, art. 791:** se desestima la propuesta del incompatible.
- **Texto Único de la Ley 22.** El art. 24.5 incapacita para contratar a quien incurra en falsedad. El art. 28 prohíbe a servidores y miembros de juntas contratar por interpuestas personas. **El art. 41**, en actos de más de B/.500 mil, exige declarar a todo beneficiario final **directo o indirecto de 10% o más**; la declaración falsa tiene responsabilidad penal y civil (<https://ministeriopublico.gob.pa/wp-content/uploads/LIBRO_TEXTO_UNICO_LEY22_2006.pdf>).
- **Ley 129 de 2020 y DE 35 de 2022.** Beneficiario final es quien tiene 25% o más, o controla por una cadena de sociedades, por partes relacionadas o por otros medios (guía del MEF, dic-2025: <https://cnbc.mef.gob.pa/wp-content/uploads/2026/02/Guia-de-Beneficiarios-Finales-para-Panama.pdf>).
- **Circular ANTAI-DS-001-2026.** La declaración es condición para formalizar el contrato una vez adjudicada la licitación (<https://antai.gob.pa/wp-content/uploads/2026/03/Circular-ANTAI-DS-001-2026.pdf>).
- **Hechos.** El ministro dijo el 25-jun-2026 que su firma es «el último paso» en los contratos del MINSA (TVN: <https://www.tvn-2.com/nacionales/ministro-salud-fernando-boyd-niega-conflicto-bio-materiales-s-a_1_2247875.html>). Además preside la comisión de desabastecimiento (Ley 419, art. 262, texto de la Ley 462).

### 4.2 Mi opinión (no es opinión legal)

1. **El art. 249.2 alcanza a Jaime y a Juan Luis.** La duda es si se extiende a la S.A. Hay un argumento literal en contra («personas que tengan vínculos de parentesco»), pero la Ley 316 y la Ley 22 miran a través de accionistas, beneficiarios finales, cadenas de sociedades e interpuestas personas. Nadie adjudicará con esa duda abierta, y un competidor impugnaría.
2. **Que el ministro se aparte no lo cura:** el art. 8 regula su conducta; el art. 249 regula la condición del oferente.
3. **La incompatibilidad dura lo que dure el cargo.** No encontré un período de enfriamiento.

### 4.3 ¿Sirve una holding?

**No: solo oculta, y mal.**

- Cada sobrino tendría cerca de 16.7% indirecto, por encima del 10% «directo o indirecto» del art. 41; el DE 35 cuenta la cadena de sociedades como control.
- La Ley 316, art. 5, nombra a los beneficiarios finales.
- Omitir el vínculo convierte la nulidad en falsedad: incapacidad para contratar (Ley 22, art. 24.5), responsabilidad penal y civil (art. 41) y nulidad con responsabilidad solidaria (Ley 316, art. 16).
- Con el antecedente de Bio Materiales, la estructura se leería como encubrimiento.

**Preguntas para el abogado:**

1. ¿Alcanza el art. 249.2 a una persona jurídica por sus accionistas, beneficiarios finales, directores o apoderados?
2. ¿Hay jurisprudencia o dictámenes de la DGCP sobre el art. 249 o su antecedente de 2001?
3. ¿Alcanza a los patronatos? La Ley 462 permite al ministro integrar otras juntas.
4. ¿Hay una configuración limpia con Jaime y Juan Luis fuera de la S.A.?

## 5. Rutul Patel, Zywie y Bueno

| Fuente (14-oct-2026) | Consulta | Resultado |
| --- | --- | --- |
| SECOP II, contratos (Colombia): <https://www.datos.gov.co/resource/jbjy-vk9h.json> | Proveedor «ZYWIE», «BUENO SALUD» o «NOSHER» | 0 contratos |
| SECOP II, proveedores registrados: <https://www.datos.gov.co/resource/qmzu-gj57.json> | Mismos nombres | 0 |
| INVIMA, CUM vigentes: <https://www.datos.gov.co/resource/i7cb-raxc.json> | Titular o rol «BUENO SALUD», «SALUD CARE», «ZYWIE» o «SANAND» | 0 |
| DNM de El Salvador: <https://expedientes.medicamentos.gob.sv/productos/buscarProducto> | 1,773 registros de 9 moléculas de la primera ola o afines, en todos los estados | 0 coincidencias. El listado muestra al titular, no al fabricante |
| PanamaCompra | LPU 01-2026, LPU 11-2026 y compras conjuntas 2023-2025 | Ninguna oferta con Bueno o Zywie como fabricante; sí un licenciatario de la planta (doc. 3) |
| GLEIF: <https://api.gleif.org/api/v1/lei-records/335800V2EE9V8NY8JH42> | LEI de Bueno | Activo; renovación el 28-dic-2026 |
| El Mundo (25-jun-2026): <https://diario.elmundo.sv/economia/proveedores-extranjeros-dominan-compras-estatales-de-medicamentos-segun-informe-de-inquifar> | Compras del ISSS en 2025 | 90% de US$46.9 millones fue a proveedores internacionales: que un exportador indio participe es plausible |

**No hay adjudicaciones ni registros públicos de Zywie o Bueno en América Latina.** Las únicas huellas son de licenciatarios de la planta (Ecuador y Panamá). No pude consultar COMPRASAL (requiere JavaScript), Guatecompras, Honducompras, SICOP (por NIT o con cuenta), DIGEMID ni COFEPRIS; IndiaMART respondió 429.

**Prueba simple:** pedirle a Rutul Patel los números de proceso en COMPRASAL o SECOP y los números de registro. Si no los da, la afirmación se trata como no cierta.

## 6. Productos

**Competencia en la LPU 01-2026** (cuadro oficial; B/. por unidad):

| Producto | Oferentes | Adjudicado | Rango | Referencia | Origen del ganador |
| --- | --- | --- | --- | --- | --- |
| Paracetamol 500 mg | 3 | 0.010 | 0.01–0.02 | 0.01 | India |
| Paracetamol jarabe | 4 | 0.59 | 0.57–1.20 | 0.60 | Panamá (la más baja no ganó) |
| Amoxicilina + clavulánico, tableta | 1 | 0.179 | — | 0.19 | Portugal |
| Amoxicilina + clavulánico, suspensión | 2 | 1.98 | 1.98–4.40 | 2.01 | Portugal |
| Ceftriaxona 1 g | 6 | 0.239 | 0.239–0.65 | 0.28 | China |
| Cefotaxima 1 g | 3 | 0.259 | 0.259–0.90 | 0.28 | China |
| Albendazol, suspensión | 3 | 1.81 | 1.81–1.85 | 1.86 | Guatemala (se acepta frasco de 10 ml) |
| Mebendazol 100 mg | 1 | 0.13 | — | 0.13 | Panamá |
| Nistatina, suspensión | 3 | 3.18 | 3.08–3.30 | 3.39 | El Salvador (la más baja no ganó) |
| Hidrocortisona, crema | 5 | 0.555 | 0.555–1.90 | 0.58 | India |
| Mometasona (alta potencia) | 1 | 1.02 | — | 1.03 | Chile |

**Hay dos mercados:**

- **Disputados**, con precios en el costo indio o chino: cefalosporinas, paracetamol 500 mg y, en parte, hidrocortisona.
- **Finos**, con 1–3 oferentes pegados a la referencia y sin competencia real de precio: mebendazol, mometasona, albendazol, nistatina y la tableta de amoxicilina con clavulánico. Solo aquí tiene ventaja una fábrica india.

**Lo omitido.** La LPU 01-2026 tiene **87 renglones** sin equivalencia terapéutica exigida, no estériles, no controlados, con dos oferentes o menos, a B/.10 o menos por unidad y más de B/.20 mil al año. Suman **B/.11.3 millones al año**; 20 quedaron desiertos (B/.2.2 millones) y solo 18 (B/.1.4 millones) están en los catálogos de Zywie o Modi (cálculo sobre `central_renglones_all.csv`).

- En el catálogo de Zywie: amoxicilina 250 mg/5 ml (unos B/.262 mil, 2 oferentes), clobetasol (B/.45 mil, 2), peróxido de benzoilo al 5% (B/.30 mil, 2) e ibuprofeno en suspensión (B/.44 mil, 1, en 2023).
- Fuera: dicloxacilina de 500 mg (B/.173 mil, 1 oferente) y en suspensión (desierta).

**Recomendación:**

1. Primera ola: los cuatro que pagan su registro, más la amoxicilina y el clobetasol, con el precio real de fábrica.
2. Sacar las cefalosporinas y el jarabe (B/.0.40 en el MINSA y mucho volumen físico).
3. Revisar en cada renglón la presentación aceptada.
4. Evaluar un portafolio de varios fabricantes certificados, porque el problema central del plan es la escala.

## 7. Acuerdos y reparto con la fábrica

**Práctica de mercado y evidencia pública:**

- **Registros.** El esquema MAI de la India reembolsa **50% de los cargos de registro en el exterior**, con tope de Rs 2 crore por exportador al año (pautas de 2021; vigencia actual no confirmada). Exige que el certificado nombre al solicitante como titular o fabricante. Los comercializadores como Zywie solo cobran por registros a su nombre (<https://pharmexcil.com/uploads/RevisedMAIGuildelines19thJuly2021.pdf>; <http://pharmexcil.com/docs/MAI/PR/0.PRRequirements.pdf>). **Pedir que la fábrica pague los registros es razonable:** recupera la mitad. Pero querrá figurar y protegerse.
- **Crédito.** La póliza SCR de ECGC cubre 90% del riesgo comercial y político para exportadores con más de Rs 5 crore de facturación; Bueno califica por tamaño (<https://main.ecgc.in/english/wp-content/themes/pcwebecgc/images/pcECGPagePDF/SalesLiterature/SCR.pdf>). El RBI amplió de 9 a 15 meses el plazo para repatriar cobros de exportación (FEMA 23(R)/(7)/2025-RB, 13-nov-2025; EY: <https://www.ey.com/en_in/technical/alerts-hub/2025/12/rbi-introduces-comprehensive-relaxations-for-exporters-and-importers>). **120–180 días es legal y asegurable.** El límite es la caja de Bueno (deuda sobre patrimonio de 1.26) y el cupo que ECGC dé a una S.A. nueva. A mi juicio, la consignación es rara con distribuidores nuevos.
- **Titularidad.** Quien tiene el registro controla el mercado (bioaccess, 13-oct-2026: <https://cms.bioaccessla.com/blog/latam-authorized-representative-is-the-real-market-access-asset/>). «La fábrica paga y el registro es de la S.A.» solo es estable con traspaso a costo si la relación termina por causa de la S.A.

**¿Es justo el 50/50?** No con aportes iguales. El lado de Rutul Patel gana el margen de fábrica (su entorno está en la directiva de Bueno) y el de Zywie (B/.34 mil en 60 meses, doc. 2), más la mitad de las utilidades; el lado panameño opera, firma como codeudor y carga el riesgo legal. Es justo solo si:

1. el lado indio pone 70–80% del efectivo;
2. un retorno preferente de 8–10% anual al capital panameño;
3. la fábrica financia registros, crédito de 180 días e inventario inicial.

En cualquier caso, con precio a libro abierto y el margen de Zywie fijo, de 5% o menos.

**Contratos, en orden:**

1. Acuerdo de confidencialidad mutuo.
2. Opinión legal, antes de cualquier compromiso.
3. KYC y paquete de calidad: CPP por ONDLS, certificado OMS, licencias e informe de los lotes de 2024.
4. Memorando de entendimiento no vinculante: precio, registros, crédito, exclusividad, capital y compuertas.
5. Pacto de accionistas (compuertas, salida, bloqueos, partes relacionadas) junto con el contrato de distribución exclusiva **firmado por la fábrica**: metas mínimas, carta solidaria por acto, prohibición de ofertar directo (Ley 419, art. 204), titularidad y traspaso de registros, fórmula de precio, crédito y costos de retiros del mercado.
6. Acuerdo de calidad (glicoles por lote, estabilidad en zona IVb, reclamos, farmacovigilancia) antes del primer expediente.

## 8. Capital con B/.60 mil

| Estructura | Lado panameño (mediana / p90) | ¿Cabe? |
| --- | --- | --- |
| A–D con aportes 50/50 (paquete) | B/.126–202 mil | No |
| D con Rutul Patel poniendo 70% / 80% (paquete) | Unos B/.76 mil / B/.50–85 mil | Solo D con 80%, en la mediana |
| E, solo panameños (paquete) | B/.117 / 139 mil | No |
| **E con registros pagados por la fábrica** (revisor) | **B/.37 / 50 mil**; perder más que la fase 0: 46%; valor presente de −B/.12 mil | Sí |
| **Lo anterior más amoxicilina y clobetasol** (revisor) | **B/.36 / 45 mil**; 27%; valor presente de +B/.2 mil | Sí, y pasa la compuerta de 35% |

Dos advertencias:

1. La estructura E depende de supuestos del paquete no probados: un distribuidor licenciado que pague una regalía de 20–40% del margen bruto y venda 1.25 veces lo que vendería la S.A.
2. Si el art. 249.2 deja fuera a Jaime y a Juan Luis, el capital panameño es el de Francisco más inversionistas.

**Lo que pediría un inversionista** (criterio profesional, sin fuente pública): opinión legal limpia que incluya el art. 249; precio y crédito firmados por la fábrica; retorno preferente y preferencia en la liquidación; tramos según las compuertas; veto sobre operaciones con Zywie y la fábrica; puesto en la junta; arrastre, acompañamiento y salida a 5 años; ninguna garantía personal. Buscaría 25% o más, y ningún caso realista del modelo llega.

## 9. Puntos ciegos y riesgos

1. **Legal:** Ley 419, art. 249.2, y la comisión de oferentes en el despacho del ministro; riesgo de impugnación y de prensa.
2. **Garantías personales:** los codeudores de fianzas de 30% pueden perder más que su capital; el modelo carga la ejecución solo a la S.A.
3. **Lotes mínimos y empaque exclusivo** frente a miles de unidades al año por producto.
4. **Un solo catálogo:** deja fuera 87% de los renglones finos.
5. **Venta directa** de la fábrica o Zywie en emergencias (Ley 419, art. 204).
6. **Tiempo de los socios** contado como mejora, no como costo.
7. **Oportunidades:** estructura E con registros de la fábrica, reembolso MAI, factoring, y el fin del parentesco relevante cuando el ministro salga. El canal privado lo estudia otro agente.

## 10. Lo que no pude verificar

- Jurisprudencia o dictámenes del art. 249.2 aplicado a personas jurídicas.
- El formulario de la ANTAI (no respondió): no sé si pregunta por el parentesco.
- Precios públicos indios de la amoxicilina en polvo y del clobetasol. PMBI, TNMSC y Assam cortaron la conexión. Usé FOB estimados de US$0.23 por frasco de 60 ml y US$0.40 por tubo; a costo doble, la amoxicilina sigue dejando más de 50% de margen.
- Si la licencia de agencia se necesita para presentar los registros.
- Pagos reales de la CSS y el MINSA en 2026, y el colateral para una S.A. nueva.
- COMPRASAL, Guatecompras, Honducompras, SICOP, DIGEMID y COFEPRIS.
- Si el ministro integra juntas de patronatos.
