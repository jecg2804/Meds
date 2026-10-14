# -*- coding: utf-8 -*-
"""Supuestos del modelo de la distribuidora de medicamentos para compras públicas en Panamá.

Versión auditada del 9 de octubre de 2026. Cada cifra lleva su fuente y su naturaleza:
  F = dato verificado en una fuente abierta (norma, pliego, adjudicación, tarifa publicada)
  R = referencia indirecta (precio de otro mercado, tarifa análoga)
  E = estimación o supuesto propio, pendiente de cotización
El detalle de cada verificación está en research/verificacion_2026-10-09/registro_verificaciones.csv.
Orden de los escenarios en todas las tuplas: (pesimista, base, optimista).
Mes 1 del modelo = enero de 2027 (constitución de la S.A. después de la fase 0 y de la opinión legal).
"""

MONTH1 = (2027, 1)          # año y mes calendario del mes 1 del modelo

# ---------------------------------------------------------------- productos
# Canales:
#   C1 = CSS centralizado: LPU 01-2026 (15 meses, del 11-feb-2026 al 11-may-2027), cantidad máxima anualizada x12/15;
#        precio = adjudicado (cuadro de propuestas oficial de PanamaCompra).
#   C2 = MINSA centralizado. c2='ssr': subasta en reversa del MINSA de 2026, cantidad fija verificada.
#        c2='cc': compra conjunta de 2023 (oferta más baja, sin adjudicación verificada; 50% de la cantidad al MINSA);
#        solo cuenta multiplicada por el parámetro cc_w.
#   C3 = CSS descentralizado (contratación menor y compra menor ágil): ritmo de enero a septiembre de 2026 anualizado,
#        precio ponderado por cantidad (tras la LPU la CSS casi dejó de comprar estos productos por compra menor).
#   C4 = MINSA, hospitales, patronatos y otros, descentralizado (enero de 2025 a septiembre de 2026, anualizado),
#        precio ponderado por cantidad; incluye las compras menores de la sede del MINSA.
# q = unidades por año; p = precio unitario en B/.; b1 = ofertas en el renglón de la LPU.
# fob = precio representativo de las compras públicas indias vigentes (PMBI 2022-2027, TNMSC 2024, Assam 2025) x 1.4,
#       a INR 96.6149 por dólar (RBI/FBIL 9-oct-2026); en PCT500, ALBSUS, MBZ100, NYSSUS y MOMCRM se ajustó con otras
#       referencias (ver src_cost). El índice del proveedor (sup_idx) se aplica encima.
# adder = flete y gastos hasta la bodega en Panamá a US$300 por m3 por el volumen de la unidad (catálogo IMRES);
#         el multiplicador log_mult lo lleva al costo cotizado (US$356 por m3 en la base).
SRC_C1 = 'F: PanamaCompra, cuadro de propuestas LPU 01-2026 (proceso 2025-1-10-01-99-SPU-000009)'
SKUS = [
 dict(id='PCT500', short='Paracetamol 500 mg', name='Paracetamol 500 mg tableta', group='Primera ola', inc=1,
      fob=0.0038, adder=0.00165, c2='cc',
      src_cost='R: PMBI 2024-27 INR 2.74 por 10, TNMSC 2024 INR 23.48 por 100 y Assam 2025 INR 2.50 por 10; x1.4 = US$0.0034-0.0040; se usa 0.0038; blíster 5.5 cm3',
      q1=23770516, p1=0.010, b1=3, q2=0, p2=0, q3=1141333, p3=0.020, q4=11112486, p4=0.0201),
 dict(id='PCTSYR', short='Paracetamol jarabe', name='Paracetamol 120-160 mg/5 ml jarabe, frasco 120 ml', group='Primera ola', inc=1,
      fob=0.1478, adder=0.135, c2='ssr',
      src_cost='R: TNMSC 2024 INR 5.72 y Assam 2025 INR 5.85 por 60 ml; a 120 ml se usa INR 10.2 (factor 1.75 por frasco más grande), x1.4; 450 cm3',
      q1=315718, p1=0.59, b1=4, q2=524358, p2=0.40, q3=0, p3=0, q4=63302, p4=0.6938),
 dict(id='AMCTAB', short='Amoxicilina + clavulánico tableta', name='Amoxicilina + clavulánico 500/125 mg tableta', group='Primera ola', inc=1,
      fob=0.0754, adder=0.0036, c2='cc',
      src_cost='R: PMBI 2024-26 INR 31.60 por 6 y TNMSC 2024 INR 30.81 por 6 (se usa INR 5.2 por tableta), x1.4; alu-alu 12 cm3',
      q1=46534, p1=0.179, b1=1, q2=191135, p2=0.19, q3=0, p3=0, q4=30555, p4=0.3211),
 dict(id='AMCSUS', short='Amoxicilina + clavulánico suspensión', name='Amoxicilina + clavulánico 400/57 mg/5 ml suspensión, frasco 100 ml', group='Primera ola', inc=1,
      fob=1.159, adder=0.15, c2='cc',
      src_cost='R: PMBI 2023-26 INR 28.06 por 30 ml, escalado a 100 ml (x2.85 = INR 80), x1.4; 500 cm3',
      q1=10217, p1=1.98, b1=2, q2=0, p2=0, q3=0, p3=0, q4=7463, p4=4.5197),
 dict(id='CRO1G', short='Ceftriaxona 1 g', name='Ceftriaxona 1 g vial (I.V.)', group='Primera ola', inc=1,
      fob=0.1956, adder=0.0162, c2='cc',
      src_cost='R: Assam 2025 INR 12.6 y Delhi 2022 INR 15.48 por vial; se usa INR 13.5, x1.4; 54 cm3',
      q1=194242, p1=0.239, b1=6, q2=201135, p2=0.25, q3=3899, p3=0.78, q4=43743, p4=0.452),
 dict(id='CTX1G', short='Cefotaxima 1 g', name='Cefotaxima 1 g vial', group='Primera ola', inc=1,
      fob=0.2029, adder=0.0162, c2='cc',
      src_cost='R: Assam 2025 INR 13.3 por vial (PMBI 500 mg con agua INR 12.32); se usa INR 14.0, x1.4; 54 cm3',
      q1=168687, p1=0.259, b1=3, q2=177344, p2=0.27, q3=0, p3=0, q4=79691, p4=0.3987),
 dict(id='ALBSUS', short='Albendazol suspensión', name='Albendazol 400 mg/10 ml suspensión', group='Primera ola', inc=1,
      fob=0.07, adder=0.024, c2='cc',
      src_cost='R: PMBI 2022-25 INR 4.22 y Delhi 2022 INR 4.59 por 10 ml; x1.4 = US$0.062; se usa 0.07; 80 cm3 (el ganador de la LPU entregó 20 ml)',
      q1=18762, p1=1.81, b1=3, q2=194990, p2=1.86, q3=0, p3=0, q4=10114, p4=1.5163),
 dict(id='MBZ100', short='Mebendazol 100 mg', name='Mebendazol 100 mg tableta', group='Primera ola', inc=1,
      fob=0.0085, adder=0.0009, c2='cc',
      src_cost='R: sin licitación india pública; precio al público de Jan Aushadhi INR 8.44 por 6 x0.42 = INR 0.59, x1.4; 3 cm3',
      q1=188514, p1=0.13, b1=1, q2=179270, p2=0.13, q3=8000, p3=0.2188, q4=1714, p4=0.1753),
 dict(id='NYSSUS', short='Nistatina suspensión', name='Nistatina 100,000 UI/ml suspensión, frasco 30 ml', group='Primera ola', inc=1,
      fob=0.42, adder=0.0555, c2='cc',
      src_cost='R: sin precio indio público; se usa US$0.42 con UNICEF US$0.60 por 30 ml como techo; 185 cm3',
      q1=14898, p1=3.18, b1=3, q2=18118, p2=3.39, q3=0, p3=0, q4=2142, p4=3.3201),
 dict(id='HCTCRM', short='Hidrocortisona crema', name='Hidrocortisona 1% crema, tubo 15 g', group='Primera ola', inc=1,
      fob=0.1988, adder=0.033, c2='cc',
      src_cost='R: PMBI 2024-26 INR 13.72 por tubo x1.4; 110 cm3',
      q1=89267, p1=0.555, b1=5, q2=44276, p2=0.58, q3=0, p3=0, q4=1564, p4=1.4679),
 dict(id='MOMCRM', short='Mometasona crema', name='Mometasona 0.1% crema, tubo 15 g (renglón de corticoide de alta potencia)', group='Primera ola', inc=1,
      fob=0.10, adder=0.033, c2='cc',
      src_cost='R: PMBI 2023-25 INR 6.00 por tubo; x1.4 = US$0.087; se usa 0.10; 110 cm3',
      q1=65534, p1=1.02, b1=1, q2=34482, p2=0.65, q3=0, p3=0, q4=343, p4=3.66),
 # Sistema nervioso central: fabricante no identificado (no están en el catálogo de la fábrica). Solo en la variante «+ SNC».
 dict(id='AMI10', short='Amitriptilina 10 mg', name='Amitriptilina 10 mg tableta', group='SNC', inc=0,
      fob=0.0028, adder=0.00054, c2='cc', src_cost='R: Assam 2025 INR 1.90 por 10 (PMBI INR 1.99; TNMSC INR 1.71), x1.4',
      q1=325776, p1=0.12, b1=0, q2=152808, p2=0.12, q3=0, p3=0, q4=0, p4=0),
 dict(id='AMI25', short='Amitriptilina 25 mg', name='Amitriptilina 25 mg tableta', group='SNC', inc=0,
      fob=0.0033, adder=0.00054, c2='cc', src_cost='R: Assam 2025 INR 2.30 por 10 (TNMSC INR 19.63 por 100; PMBI INR 3.49 por 15), x1.4',
      q1=1953204, p1=0.027, b1=1, q2=0, p2=0, q3=0, p3=0, q4=3086, p4=0.40),
 dict(id='QTP25', short='Quetiapina 25 mg', name='Quetiapina 25 mg tableta', group='SNC', inc=0,
      fob=0.0053, adder=0.00054, c2='cc', src_cost='R: PMBI 2023-26 INR 3.69 por 10 x1.4',
      q1=0, p1=0, b1=0, q2=0, p2=0, q3=0, p3=0, q4=558798, p4=0.18),
 dict(id='QTP100', short='Quetiapina 100 mg', name='Quetiapina 100 mg tableta', group='SNC', inc=0,
      fob=0.0138, adder=0.00066, c2='cc', src_cost='R: interpolado de PMBI 25 y 200 mg x1.4',
      q1=0, p1=0, b1=0, q2=0, p2=0, q3=0, p3=0, q4=509795, p4=0.13),
 dict(id='QTP200', short='Quetiapina 200 mg', name='Quetiapina 200 mg tableta', group='SNC', inc=0,
      fob=0.0216, adder=0.00075, c2='cc', src_cost='R: PMBI 2023-25 INR 14.90 por 10 x1.4',
      q1=1376100, p1=0.079, b1=3, q2=0, p2=0, q3=243829, p3=0.21, q4=28886, p4=0.20),
 dict(id='TPM100', short='Topiramato 100 mg', name='Topiramato 100 mg tableta', group='SNC', inc=0,
      fob=0.0116, adder=0.0006, c2='cc', src_cost='R: PMBI 2023-25 INR 7.98 por 10 x1.4',
      q1=443907, p1=0.065, b1=2, q2=0, p2=0, q3=26343, p3=1.02, q4=4640, p4=1.18),
]

# ---------------------------------------------------------------- parámetros escalares
# clave: (etiqueta, unidad, pesimista, base, optimista, fuente)
P = {
 # calendario
 'reg_m':      ('Mes en que salen los registros sanitarios (presentados en el mes 3)', 'mes', 12, 9, 7,
                'F: Ley 419 arts. 41 y 74 (20 días hábiles de la DNFD y 60 del laboratorio, unos 4 meses); E: base con 2 meses de observaciones, pesimista con subsanación y rezago'),
 'lead_days':  ('Tiempo de reposición: orden al proveedor hasta stock en Panamá', 'días', 120, 90, 75,
                'E: producción, flete marítimo con transbordo y aduana; se confirma con la fábrica y el agente de carga'),
 'ship_m':     ('Meses entre embarque y stock disponible', 'meses', 2, 2, 2, 'E: tránsito con transbordo y desaduanaje'),
 'ramp_m':     ('Meses para llegar a la participación madura en compras descentralizadas', 'meses', 18, 12, 9,
                'E: curva de aprendizaje; los nuevos son descalificados 57% de las veces frente a 36% de los establecidos (OCDS MINSA 2021-2024)'),
 'cen_start':  ('Mes en que podría arrancar el primer contrato centralizado (calendario de la LPU)', 'mes', 27, 20, 13,
                'F: la LPU 01-2026 vence el 11-may-2027; E: si se repite su ciclo, la siguiente se licita entre dic-2026 y feb-2027, antes de tener registros, y la que sigue arrancaría hacia ago-2028 (mes 20). Optimista: la CSS prorroga y licita a inicios de 2028; pesimista: el calendario se corre 7 meses'),
 # mercado
 'mkt':        ('Factor de mercado (demanda futura frente a 2025-2026)', 'x', 0.75, 0.90, 1.00,
                'F: presupuesto de medicamentos de la CSS 2027 de B/.230.3 millones (-28.6%), en trámite; la CSS gastó en 2026 el 64% de lo presupuestado'),
 'share_dec':  ('Participación madura en compras descentralizadas (valor)', '%', 0.10, 0.22, 0.32,
                'E: los nuevos ganan 36.6% de sus ofertas con precio (OCDS MINSA 2021-2024), ofertando en parte de los actos'),
 'pwin_cen':   ('Probabilidad de ganar un renglón centralizado en el que se oferta', '%', 0.15, 0.30, 0.45,
                'F: los nuevos ganan 36.6% por oferta en el MINSA y la LPU 01-2026 da 39.9% por oferta; E: descuento por descalificación'),
 'realiz':     ('Cantidad comprada frente a la máxima del contrato de la LPU', '%', 0.55, 0.75, 0.90,
                'F: compra mínima garantizada de 50% (Adenda 1 de la LPU 01-2026); E: el resto'),
 'realiz_minsa': ('Cantidad comprada frente a la del contrato del MINSA (subasta por cantidad fija)', '%', 1.0, 1.0, 1.0,
                'F: las subastas del MINSA de 2026 son por cantidad fija (informe de la SSR-000018)'),
 'minsa_occ':  ('Probabilidad de que el MINSA haga su compra centralizada en el año', '%', 0.30, 0.50, 0.70,
                'F: 33 subastas del MINSA entre el 24-mar y el 29-may-2026 y ninguna después; la compra conjunta del DE 16 no tiene acto a octubre de 2026'),
 'cc_w':       ('Parte de la cantidad de la compra conjunta de 2023 que se toma como demanda del MINSA', '%', 0.0, 0.15, 0.50,
                'F: de los renglones de la primera ola solo 3 de 9 aparecen como contratos y por 7-20% de lo pedido; las cifras de 2023 son ofertas, no adjudicaciones'),
 'pf_dec':     ('Precio de oferta descentralizado frente al precio ponderado actual', 'x', 0.80, 0.90, 0.95,
                'F: precio ganador / mediana de ofertas = 0.91; E: ajuste'),
 'pf_cen':     ('Precio de oferta centralizado frente al adjudicado actual', 'x', 0.90, 0.95, 1.00,
                'F: adjudicado / referencia 0.963 en la LPU 01-2026; E: descuento para desplazar al actual'),
 'erosion':    ('Caída anual de precios a partir del año 2', '%', 0.06, 0.03, 0.00, 'E: presión fiscal sobre la CSS'),
 'gm_dec':     ('Margen bruto mínimo para ofertar (descentralizado)', '%', 0.35, 0.35, 0.35, 'Regla de decisión'),
 'gm_cen':     ('Margen bruto mínimo para ofertar (centralizado)', '%', 0.20, 0.20, 0.20, 'Regla de decisión'),
 # suministro y costo
 'sup_idx':    ('Índice del precio de la fábrica frente a la referencia FOB', 'x', 1.80, 1.25, 1.00,
                'E: la fábrica no ha dado precios; 1.25 sobre la referencia = 1.75 veces el precio doméstico indio; UNICEF y OPS pagan 2 a 9 veces'),
 'pack':       ('Sobrecosto por empaque y rotulado exclusivo para Panamá', '%', 0.10, 0.05, 0.03,
                'F: el pliego exige rotulado del acto en el empaque; E: costo'),
 'log_mult':   ('Multiplicador del costo logístico (flete LCL, destino, corredor, seguro)', 'x', 2.20, 1.20, 0.80,
                'R: LCL puesto en bodega unos US$650 / 356 / 240 por m3 (FAK CMA CGM jun-2026 + recargo PSS; tarifario de destino Crowley; corredor)'),
 'dist':       ('Distribución local a almacenes y hospitales (% de ventas)', '%', 0.06, 0.04, 0.03, 'E: sin tarifa pública'),
 'penal':      ('Multas por atraso y reposiciones (% de ventas)', '%', 0.02, 0.005, 0.0,
                'F: multas de 5-15% y mora de al menos 10% (Ley 419 arts. 231 y 232); E: frecuencia'),
 'expiry':     ('Mermas y vencimientos (% del costo comprado)', '%', 0.08, 0.04, 0.015,
                'F: el pliego pide el vencimiento de la ficha técnica o, si no lo fija, 18 meses de vida útil al entregar; con 24 meses de vida útil quedan unos 3 meses de ventana en bodega; E: frecuencia'),
 'baddebt':    ('Incobrables y vigencias vencidas (% de ventas)', '%', 0.02, 0.005, 0.0,
                'F: la CSS debía US$48 millones a proveedores en 2023'),
 # capital de trabajo
 'dso_days':   ('Días de cobro: entrega hasta cobro', 'días', 240, 150, 105,
                'F: el contrato paga a 90 días después de presentada, verificada y aceptada la cuenta y del refrendo de la Contraloría; E: el resto'),
 'cover_m':    ('Cobertura de inventario para compras descentralizadas', 'meses', 3, 2.5, 2,
                'E: limitada por la vida útil exigida al entregar (18 meses si la ficha técnica no fija otra)'),
 'cen_stock_m':('Inventario para contratos centralizados', 'meses', 2, 2, 1, 'F: la LPU exige reserva de al menos 1 mes'),
 'adv':        ('Anticipo a la fábrica al colocar la orden', '%', 1.00, 0.30, 0.00, 'E: se negocia'),
 'credit_days':('Crédito de la fábrica desde el embarque', 'días', 0, 0, 120, 'E: objetivo de negociación; hoy no ofrecido'),
 'bond_css':   ('Fianza de cumplimiento de la LPU (% del contrato)', '%', 0.30, 0.30, 0.30, 'F: pliego de la LPU 01-2026, cláusula 11'),
 'bond_minsa': ('Fianza de cumplimiento del MINSA (% del contrato)', '%', 0.20, 0.20, 0.20, 'F: Ley 419 art. 246 (no menos de 20%)'),
 'collat':     ('Colateral en efectivo que pide la aseguradora o el banco (% de la fianza)', '%', 1.00, 0.75, 0.25,
                'E: ninguna aseguradora publica el porcentaje; una empresa nueva sin estados auditados; se cierra con dos cotizaciones'),
 'bond_prem':  ('Prima anual de la fianza', '%', 0.040, 0.025, 0.013,
                'F: Banco General, garantía de cumplimiento 1.07-1.605% anual con mínimo de US$1,337.50 (2026); los mínimos elevan la tasa efectiva'),
 'bid_bond':   ('Fianza de propuesta en la LPU (% de toda la oferta: el acto supera B/.70,000, Ley 419 art. 245)', '%', 0.10, 0.10, 0.10,
                'F: Ley 419 art. 245; pliego de la LPU 01-2026'),
 'bid_m':      ('Meses de colateral de la fianza de propuesta antes de cada contrato de la LPU', 'meses', 6, 5, 4,
                'F: vigencia exigida de 180 días hábiles; 3.5 meses de publicación a ejecutoria en la LPU 01-2026'),
 'mincash_m':  ('Caja mínima operativa (meses de costos fijos)', 'meses', 3, 3, 3, 'Política financiera'),
 # registros
 'rs_off':     ('Tasas oficiales por registro (DNFD 500 + MEF + refrendo)', 'B/.', 575, 570, 545, 'F: DE 27 art. 15; guía del MINSA de 2012 para MEF y refrendo'),
 'rs_iea':     ('Análisis de control previo (IEA o INDICASAT) por producto', 'B/.', 2000, 1500, 1000,
                'R: guía del MINSA de 2012 US$1,000; SignatureLex B/.1,500; la tasa vigente no está publicada pese a la Ley 419 art. 79'),
 'rs_law':     ('Honorario y gastos del abogado por registro', 'B/.', 1350, 800, 500, 'R: SignatureLex 600 + 750; arancel de 2001 B/.350'),
 'rs_smp':     ('Muestras y courier por registro', 'B/.', 300, 150, 100, 'E'),
 'rs_trad':    ('Traducciones oficiales por registro (CPP, BPM, poderes, etiquetas)', 'B/.', 1500, 600, 300,
                'F: DE 27 art. 220 exige traductor público autorizado; E: monto'),
 'rs_succ':    ('Registros aprobados / presentados', '%', 0.70, 0.85, 0.95, 'E'),
 'postreg':    ('Análisis posregistro por producto (2 en 5 años), por año', 'B/.', 800, 600, 400, 'F: Ley 419 art. 67; R: 2 x 1,500 / 5'),
 'n2':         ('Productos de la segunda ola (sin equivalencia terapéutica, fabricación verificada)', 'productos', 0, 6, 12,
                'E: candidatos del catálogo con compras públicas; exigen prueba de licencia de fabricación de cada uno'),
 'm2':         ('Mes en que se presentan los registros de la segunda ola', 'mes', 24, 18, 15, 'Decisión: solo si la primera ola pasa la compuerta operativa'),
 'rel2':       ('Ingreso por producto de la segunda ola frente al promedio de la primera', 'x', 0.5, 0.7, 1.0, 'E'),
 'fact_share': ('Porcentaje de las ventas que se factoriza', '%', 0.0, 0.0, 0.0, 'Opción; Ley 22 art. 97 permite ceder créditos'),
 'fact_cost':  ('Costo mensual del factoring sobre lo cedido', '%', 0.015, 0.0125, 0.010, 'R: Balboa Factoring 2025, 14.6-18.3% anual'),
 'stop_det':   ('Mes de cierre del negocio (61 = no se cierra)', 'mes', 61, 61, 61, 'Interruptor'),
 'inv_liq':    ('Recuperación del inventario si se cierra', '%', 0.5, 0.5, 0.5, 'E'),
 # impuestos y valoración
 'isr':        ('Impuesto sobre la renta', '%', 0.25, 0.25, 0.25, 'F: Código Fiscal art. 699'),
 'divtax':     ('Impuesto de dividendos', '%', 0.10, 0.10, 0.10, 'F: Código Fiscal art. 733'),
 'aviso':      ('Impuesto de aviso de operación (% del patrimonio; mínimo B/.100, máximo B/.60,000)', '%', 0.02, 0.02, 0.02, 'F: Código Fiscal art. 1004'),
 'oncost':     ('Cargas laborales sobre sueldos', '%', 0.29, 0.28, 0.27,
                'F: cuota patronal 13.25% hasta feb-2027, 14.25% hasta feb-2029 y 15.25% después (Ley 462 art. 84), seguro educativo 1.5%, riesgos profesionales, XIII mes y prima de antigüedad'),
 'itbms_srv':  ('ITBMS no recuperable sobre servicios contratados', '%', 0.07, 0.07, 0.0,
                'F: ITBMS 7%; los medicamentos están exentos; recuperable como «asimilado a exportador» solo en el optimista (Ley 8 de 2010 art. 80)'),
 'payout':     ('Porcentaje distribuible que se reparte cada año', '%', 0.80, 0.80, 0.80, 'Política'),
 'disc':       ('Tasa de descuento anual para el VPN del caso sin fallas', '%', 0.30, 0.30, 0.30, 'E: pyme nueva con un solo cliente estatal'),
 'recov':      ('Recuperación del capital de trabajo al cierre (cobro, inventario, colateral)', '%', 0.80, 0.90, 0.95, 'E'),
 'gc_mult':    ('Múltiplo de la utilidad del año 5 (negocio en marcha; no se usa en los documentos)', 'x', 0.0, 3.0, 4.0, 'E'),
 # propiedad
 'patel_eq':   ('Participación de Rutul Patel en la S.A.', '%', 0.50, 0.50, 0.50, 'F: propuesta de Rutul Patel (50/50)'),
 'patel_cash': ('Porcentaje del capital que aporta Rutul Patel', '%', 0.50, 0.50, 0.50, 'F: propuesta de Rutul Patel (costos 50/50)'),
 'jaime_frac': ('Fracción de cada socio panameño dentro del 50% panameño', '%', 1/3, 1/3, 1/3, 'F: tres socios panameños por partes iguales'),
 'zy_markup':  ('Margen de Zywie sobre el precio de fábrica (dentro del índice del proveedor)', '%', 0.25, 0.15, 0.05, 'E'),
 # fianzas y ejecución
 'bond_tail_css':   ('Meses que la fianza de cumplimiento de la LPU sigue vigente tras el contrato', 'meses', 3, 3, 3,
                     'F: contratos de la LPU 01-2026: ejecución más 3 meses de liquidación (cláusula Octava)'),
 'bond_tail_minsa': ('Meses que la fianza de cumplimiento del MINSA sigue vigente tras el contrato', 'meses', 6, 6, 6, 'E: ejecución, liquidación y 6 meses; se confirma en el pliego'),
 'forfeit_frac':    ('Parte de la fianza de cumplimiento que se pierde si el Estado la ejecuta', '%', 1.0, 1.0, 1.0,
                     'F: Ley 22 (ejecución de la fianza) y contragarantías de la aseguradora (pagaré, codeudores)'),
}

# Costos fijos mensuales: (etiqueta, pesimista, base, optimista, inicio, fuente)
# inicio: 'm1' mes 1; 'lic' mes de la licencia (3); 'prep' registros - 1; 'cen' primer contrato centralizado
FIXED = [
 ('Regente farmacéutico (medio tiempo, mínimo 4 h diarias)', 1200, 700, 450, 'lic',
  'F: DE 27 art. 382; R: SignatureLex 400-500 al mes; Paylab 1,339-3,228 a tiempo completo'),
 ('Operador logístico (3PL) licenciado: cuota mínima', 1200, 600, 300, 'lic', 'E: sin tarifa pública; cotizaciones pedidas'),
 ('Contabilidad e impuestos', 450, 300, 200, 'm1', 'R: Healy Consultants 2026, unos 192 al mes; E'),
 ('Auditoría anual de estados financieros, prorrateada', 400, 250, 150, 'm1',
  'F: el Registro Nacional de Oferentes pide solvencia certificada por CPA o banco (DE 27 arts. 724-725); E: costo'),
 ('Asesoría legal por hora (sin iguala)', 800, 300, 150, 'm1', 'R: SignatureLex B/.300 por hora; E: horas'),
 ('Coordinador de licitaciones y operaciones (medio tiempo, desde la licencia)', 1000, 700, 550, 'lic',
  'R: Konzerta mayo de 2026, semi-senior a jefatura US$1,033-1,291 a tiempo completo; a medio tiempo'),
 ('Coordinador: paso a tiempo completo desde el primer contrato centralizado', 800, 600, 450, 'cen',
  'R: diferencia entre tiempo completo (1,800 / 1,300 / 1,000) y medio tiempo'),
 ('Farmacovigilancia: responsable designado y diccionarios MedDRA y WHODrug', 300, 150, 75, 'lic',
  'F: DE 27 arts. 257, 318 y 319; E: costo (sin tarifa pública)'),
 ('Seguros (responsabilidad civil y de producto)', 200, 100, 75, 'lic', 'E: sin tarifa pública'),
 ('Software, banca, telecomunicaciones y administración', 200, 120, 80, 'm1', 'E'),
 ('Impuesto municipal', 200, 100, 100, 'm1', 'E: tramo por confirmar con el municipio'),
]
LIC_M = 3
# tipo de cada costo fijo: 'staff' lleva cargas laborales, 'service' lleva ITBMS no recuperable, 'other' ninguno
FIXED_KIND = ['staff', 'service', 'service', 'service', 'service', 'staff', 'staff', 'service', 'other', 'service', 'other']
ANNUAL_CHARGES = [('Tasa única de la S.A.', 300, 'F: DGI'),
                  ('Agente residente', 350, 'R: SignatureLex B/.350 al año; mercado US$150-800'),
                  ('Renovación de la licencia de operación (B/.200 cada 2 años)', 100, 'F: DE 27 arts. 15 y 398')]
ANNUAL_KIND = ['other', 'service', 'other']

# Gastos de arranque: (etiqueta, pesimista, base, optimista, mes, cotización de SignatureLex, fuente)
SETUP = [
 ('Fase 0: debida diligencia de la fábrica y de los documentos (antes de constituir)', 6000, 2500, 1000, 0, 0,
  'E: auditoría virtual de planta y verificación documental'),
 ('Fase 0: opinión legal escrita sobre la Ley 316 (parentesco), de un abogado independiente', 1500, 800, 500, 0, 0,
  'R: SignatureLex B/.300 por hora; E: 2 a 5 horas'),
 ('Constitución, libros, poderes, RUC, aviso de operación y municipal', 3500, 2500, 1500, 1, 5700,
  'R: SignatureLex unos 5,700; Expanship US$1,200-2,200 el primer año'),
 ('Pacto de accionistas, contrato de suministro exclusivo y acuerdo de calidad', 6200, 2500, 1500, 1, 1750,
  'R: escala de SignatureLex (B/.1,500 más 1% escalonado)'),
 ('Diagnóstico regulatorio y matriz de portafolio', 650, 650, 500, 1, 650, 'R: SignatureLex 500 + 150'),
 ('Apoyo para abrir la cuenta bancaria', 3150, 300, 0, 1, 3150, 'R: SignatureLex 3,000 + 150; E: base'),
 ('Licencia de operación: tasa oficial 250 + planos, procedimientos e inspección', 4000, 1750, 1000, 2, 4000,
  'F: DE 27 art. 15 (200 + 50); R: SignatureLex 3,500 + 500'),
 ('Revisión del 3PL y acuerdo de calidad', 2650, 750, 400, 2, 2650, 'R: SignatureLex 2,500 + 150; E: base'),
 ('Programa de cumplimiento y anticorrupción', 3150, 1500, 800, 2, 3150, 'R: SignatureLex 3,000 + 150'),
 ('Certificado de buenas prácticas de almacenamiento', 100, 100, 100, 3, 100, 'F: DE 27 art. 15'),
 ('Registro patronal en la CSS y contratos laborales', 900, 300, 100, 3, 900, 'R: SignatureLex 750 + 150'),
 ('PanamaCompra, Registro Nacional de Oferentes y proveedor de la CSS', 2700, 500, 0, 4, 2700,
  'F: trámites sin tasa oficial; R: SignatureLex 3 x (750 + 150)'),
]
SETUP_KIND = ['service', 'service', 'service', 'service', 'service', 'service', 'service', 'service', 'service', 'other', 'service', 'service']
RS_PAY_M = 3   # mes en que se pagan los registros (presentación y análisis)
