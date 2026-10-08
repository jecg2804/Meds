# -*- coding: utf-8 -*-
"""Inputs for the Panama public-tender medicines distributor model.
Every number carries a source tag: F = fact from an opened source; E = analyst estimate.
Scenario order everywhere: (pesimista, base, optimista).
"""

# ---------------------------------------------------------------- SKUs
# Channels: C1 = CSS centralizado (LPU 01-2026, 15 meses, anualizado x12/15)
#           C2 = MINSA centralizado (subasta en reversa 2026 si existe; si no, proxy = min(50% compra conjunta 2023, CC2023 - LPU))
#           C3 = CSS descentralizado (contratación menor / compra menor ágil, ene-2025..sep-2026, anualizado)
#           C4 = MINSA, patronatos y otros descentralizado (misma ventana; cobertura parcial)
# q = unidades/año ; p = precio unitario B/. (mediana o adjudicado)
SKUS = [
 dict(id='PCT500', name='Paracetamol 500 mg tableta', group='Bueno', inc=1,
      fob=0.0040, adder=0.00237, src_cost='B2 landed.csv: FOB = TNMSC L1 x1.4; adder LCL 200 USD/CBM',
      q1=23770516, p1=0.010, b1=3, q2=0, p2=0, q3=5810286, p3=0.020, q4=11102514, p4=0.020),
 dict(id='PCTSYR', name='Paracetamol 120-160 mg/5 ml jarabe (frasco 120 ml)', group='Bueno', inc=1,
      fob=0.17, adder=0.1629, src_cost='B2: TNMSC 60 ml x1.7 escalado a 120 ml; adder por volumen',
      q1=315718, p1=0.59, b1=4, q2=524358, p2=0.40, q3=0, p3=0, q4=61873, p4=0.95),
 dict(id='AMCTAB', name='Amoxicilina + clavulánico 500/125 mg tableta', group='Bueno', inc=1,
      fob=0.086, adder=0.00265, src_cost='B2: TNMSC empanelment L1 x1.4',
      q1=46534, p1=0.179, b1=1, q2=191135, p2=0.19, q3=0, p3=0, q4=30555, p4=0.29),
 dict(id='AMCSUS', name='Amoxicilina + clavulánico 400/57 mg/5 ml suspensión (100 ml)', group='Bueno', inc=1,
      fob=1.10, adder=0.1955, src_cost='B2: derivado de Jan Aushadhi MRP; baja confianza',
      q1=10217, p1=1.98, b1=2, q2=0, p2=0, q3=0, p3=0, q4=6891, p4=4.18),
 dict(id='CRO1G', name='Ceftriaxona 1 g vial', group='Bueno', inc=1,
      fob=0.20, adder=0.01837, src_cost='B2: Delhi RC 2022; exportaciones Seair 0.21-0.37',
      q1=194242, p1=0.239, b1=6, q2=201135, p2=0.25, q3=1671, p3=0.78, q4=119983, p4=0.613),
 dict(id='CTX1G', name='Cefotaxima 1 g vial', group='Bueno', inc=1,
      fob=0.11, adder=0.01807, src_cost='B2: derivado de Jan Aushadhi MRP',
      q1=168687, p1=0.259, b1=3, q2=177344, p2=0.27, q3=7200, p3=1.00, q4=79691, p4=0.53),
 dict(id='ALBSUS', name='Albendazol 400 mg/10 ml suspensión', group='Bueno', inc=1,
      fob=0.08, adder=0.03863, src_cost='B2: Delhi RC 2022 x1.35 (frasco 10 ml)',
      q1=18762, p1=1.81, b1=3, q2=194990, p2=1.86, q3=0, p3=0, q4=10114, p4=1.62),
 dict(id='MBZ100', name='Mebendazol 100 mg tableta', group='Bueno', inc=1,
      fob=0.008, adder=0.0015, src_cost='B2: derivado de Jan Aushadhi MRP',
      q1=188514, p1=0.13, b1=1, q2=179270, p2=0.13, q3=13714, p3=0.22, q4=1714, p4=0.164),
 dict(id='NYSSUS', name='Nistatina 100,000 UI/ml suspensión', group='Bueno', inc=1,
      fob=0.40, adder=0.05903, src_cost='E: sin precio público; supuesto a confirmar con Zywie',
      q1=14898, p1=3.18, b1=3, q2=18119, p2=3.39, q3=0, p3=0, q4=1856, p4=3.18),
 dict(id='HCTCRM', name='Hidrocortisona crema (línea corticoide baja potencia)', group='Bueno', inc=1,
      fob=0.16, adder=0.04923, src_cost='B2: derivado de Jan Aushadhi MRP (tubo 15 g)',
      q1=89267, p1=0.555, b1=5, q2=44276, p2=0.58, q3=634, p3=2.50, q4=1564, p4=1.875),
 dict(id='MOMCRM', name='Mometasona 0.1% crema (línea corticoide alta potencia)', group='Bueno', inc=1,
      fob=0.097, adder=0.04923, src_cost='E: Jan Aushadhi MRP INR 16.88/15 g x0.55',
      q1=65534, p1=1.02, b1=1, q2=34482, p2=0.65, q3=1840, p3=4.79, q4=343, p4=3.66),
 dict(id='AMI10', name='Amitriptilina 10 mg tableta', group='CNS', inc=0,
      fob=0.0039, adder=0.0015, src_cost='E: Jan Aushadhi MRP INR 0.681/tab x0.54',
      q1=325776, p1=0.12, b1=0, q2=152808, p2=0.12, q3=0, p3=0, q4=0, p4=0),
 dict(id='AMI25', name='Amitriptilina 25 mg tableta', group='CNS', inc=0,
      fob=0.0037, adder=0.00149, src_cost='B2: TNMSC L1 x1.4',
      q1=1953204, p1=0.027, b1=1, q2=0, p2=0, q3=0, p3=0, q4=3086, p4=0.40),
 dict(id='QTP25', name='Quetiapina 25 mg tableta', group='CNS', inc=0,
      fob=0.0058, adder=0.0015, src_cost='E: Jan Aushadhi MRP INR 1.031/tab x0.54',
      q1=0, p1=0, b1=0, q2=0, p2=0, q3=0, p3=0, q4=558798, p4=0.18),
 dict(id='QTP100', name='Quetiapina 100 mg tableta', group='CNS', inc=0,
      fob=0.0193, adder=0.0015, src_cost='E: Jan Aushadhi MRP INR 3.403/tab x0.54',
      q1=0, p1=0, b1=0, q2=0, p2=0, q3=0, p3=0, q4=509795, p4=0.13),
 dict(id='QTP200', name='Quetiapina 200 mg tableta', group='CNS', inc=0,
      fob=0.0345, adder=0.0015, src_cost='E: Jan Aushadhi MRP INR 6.094/tab x0.54',
      q1=1376100, p1=0.079, b1=3, q2=0, p2=0, q3=243829, p3=0.21, q4=28886, p4=0.20),
 dict(id='TPM100', name='Topiramato 100 mg tableta', group='CNS', inc=0,
      fob=0.016, adder=0.00153, src_cost='B2: derivado de Jan Aushadhi MRP',
      q1=443907, p1=0.065, b1=2, q2=0, p2=0, q3=26343, p3=1.02, q4=4640, p4=1.18),
 dict(id='CLF4', name='Clorfeniramina 4 mg tableta', group='Modi', inc=0,
      fob=0.0013, adder=0.00148, src_cost='B2: Delhi RC 2022',
      q1=2033363, p1=0.029, b1=4, q2=1721317, p2=0.01, q3=0, p3=0, q4=5891, p4=0.35),
 dict(id='PRD5', name='Prednisolona 5 mg tableta', group='Modi', inc=0,
      fob=0.0028, adder=0.0015, src_cost='E: Jan Aushadhi MRP INR 0.50/tab x0.54',
      q1=3497727, p1=0.016, b1=4, q2=0, p2=0, q3=139429, p3=0.24, q4=212682, p4=0.205),
]

# ---------------------------------------------------------------- scalar parameters
# key: (label, unit, pes, base, opt, source)
P = {
 # timing
 'reg_m':      ('Mes en que salen los registros sanitarios (desde la constitución)', 'mes', 9, 6, 5, 'Base = plazo de 5-6 meses planteado por el socio panameño; pesimista = supuesto de riesgo'),
 'lead_days':  ('Tiempo de reposición: orden al proveedor hasta stock en Panamá', 'días', 120, 90, 75, 'E: producción + flete marítimo + aduana; confirmar con Zywie y el agente de carga'),
 'ship_m':     ('Meses entre embarque (B/L) y stock disponible', 'meses', 2, 2, 2, 'E: tránsito marítimo con transbordo + desaduanaje'),
 'ramp_m':     ('Meses para llegar a la participación madura en compras descentralizadas', 'meses', 18, 12, 9, 'E: curva de aprendizaje; descalificación de nuevos 56% vs 34% (OCDS MINSA 2022-23)'),
 'cen_start':  ('Mes del primer contrato centralizado (LPU CSS / subasta MINSA)', 'mes', 27, 15, 12, 'E: la LPU 01-2026 vence a mediados de 2027; la siguiente se licitaría alrededor de esa fecha'),
 # market
 'mkt':        ('Factor de mercado (demanda futura vs datos 2025-26)', 'x', 0.75, 0.90, 1.00, 'F: presupuesto CSS 2027 de medicamentos -28.6% (Prensa, 4-sep-2026); E: ajuste'),
 'share_dec':  ('Participación madura en compras descentralizadas (valor)', '%', 0.10, 0.22, 0.32, 'E: P(ganar|ofertar) entrantes 17%, establecidos 26% (OCDS MINSA 2020-24)'),
 'pwin_cen':   ('Probabilidad de ganar un renglón centralizado ofertado', '%', 0.15, 0.30, 0.45, 'E: P(ganar|precio más bajo y calificado) 95%; entrantes descalificados 56%'),
 'realiz':     ('Cantidad realmente comprada vs máxima del contrato', '%', 0.55, 0.75, 0.90, 'F: compromiso mínimo CSS 50% con excepciones amplias (Adenda 1 LPU 01-2026)'),
 'minsa_occ':  ('Probabilidad de que MINSA haga su compra centralizada en el año', '%', 0.30, 0.50, 0.70, 'F: compra conjunta 2025 fracasó; DE 16 de 2026 sin acto publicado a oct-2026'),
 'pf_dec':     ('Precio de oferta descentralizado vs mediana actual', 'x', 0.80, 0.90, 0.95, 'F: precio ganador / mediana de ofertas = 0.91 (B1)'),
 'pf_cen':     ('Precio de oferta centralizado vs adjudicado actual', 'x', 0.90, 0.95, 1.00, 'F: adjudicado / referencia 0.963 en LPU 01-2026; E: descuento para desplazar'),
 'erosion':    ('Caída anual de precios a partir del año 2', '%', 0.06, 0.03, 0.00, 'E: presión fiscal CSS; ahorro de 16% en LPU 2026 vs estimado'),
 'gm_dec':     ('Margen bruto mínimo para ofertar (descentralizado)', '%', 0.35, 0.35, 0.35, 'Regla de decisión'),
 'gm_cen':     ('Margen bruto mínimo para ofertar (centralizado)', '%', 0.20, 0.20, 0.20, 'Regla de decisión'),
 # supply & cost
 'sup_idx':    ('Índice de precio del proveedor vs referencia FOB India', 'x', 1.80, 1.25, 1.00, 'E: Zywie no ha dado precios; 1.0 = referencia B2 (licitaciones indias x1.4)'),
 'pack':       ('Sobrecosto por empaque y etiquetado para Panamá', '%', 0.10, 0.05, 0.03, 'F: pliegos exigen "PROPIEDAD DE CSS/MINSA" y rotulado del acto; E: costo'),
 'log_mult':   ('Multiplicador de costo logístico (flete LCL, aduana, acarreo)', 'x', 1.50, 1.00, 0.80, 'E: sin cotización LCL India-Panamá; B2 usa 200 USD/CBM'),
 'dist':       ('Distribución local a hospitales y almacenes (% ventas)', '%', 0.06, 0.04, 0.03, 'E: B7 viajes 80-600 USD; pliegos exigen entrega en almacenes'),
 'penal':      ('Multas por atraso y reposiciones (% ventas)', '%', 0.02, 0.005, 0.0, 'F: multa 10-15%/30 por día (pliegos); E: frecuencia'),
 'expiry':     ('Mermas y vencimientos (% del costo comprado)', '%', 0.08, 0.03, 0.015, 'F: exigen 18 meses de vida útil al entregar; E: frecuencia'),
 'baddebt':    ('Incobrables y vigencias expiradas (% ventas)', '%', 0.02, 0.005, 0.0, 'F: CSS debía US$48-60 millones a proveedores en 2023'),
 # working capital
 'dso_days':   ('Días de cobro: entrega hasta cobro', 'días', 240, 150, 105, 'F: pliegos pagan a 90 días de la cuenta; E: recepción + atraso'),
 'cover_m':    ('Cobertura de inventario para compras descentralizadas', 'meses', 4, 3, 2, 'E: entregas en días en compras menores; reposición de ~3 meses'),
 'cen_stock_m':('Inventario para contratos centralizados', 'meses', 2, 2, 1, 'F: LPU exige reserva de al menos 1 mes; E: más seguridad'),
 'adv':        ('Anticipo al proveedor al colocar la orden', '%', 1.00, 0.30, 0.00, 'E: práctica común de exportadores indios con clientes nuevos'),
 'credit_days':('Crédito del proveedor desde el embarque', 'días', 0, 0, 120, 'E: Zywie no lo ha ofrecido; objetivo de negociación'),
 'bond_css':   ('Fianza de cumplimiento LPU CSS (% del contrato)', '%', 0.30, 0.30, 0.30, 'F: pliego LPU 01-2026 cl. 11'),
 'bond_minsa': ('Fianza de cumplimiento MINSA (% del contrato)', '%', 0.20, 0.20, 0.20, 'F: pliego subasta en reversa MINSA 2026 cl. 9.1'),
 'collat':     ('Colateral en efectivo exigido por la aseguradora (% de la fianza)', '%', 1.00, 0.50, 0.25, 'F: aseguradoras piden pagaré, codeudor y colateral líquido; E: porcentaje'),
 'bond_prem':  ('Prima anual de la fianza', '%', 0.030, 0.016, 0.0107, 'F: Banco General 1.07%-1.605% anual (mar-2026)'),
 'bid_bond':   ('Fianza de propuesta en la LPU (% de la oferta, renglones con referencia > B/.70,000)', '%', 0.10, 0.10, 0.10, 'F: pliego LPU 01-2026 cl. 8.14 (vigencia 180 días hábiles); subasta MINSA y compra conjunta 2024 sin fianza de propuesta'),
 'bid_m':      ('Meses de colateral de la fianza de propuesta antes de iniciar cada contrato de la LPU', 'meses', 4, 3, 2, 'E: oferta, evaluación, adjudicación y refrendo'),
 'mincash_m':  ('Caja mínima operativa (meses de costos fijos)', 'meses', 3, 3, 3, 'Política financiera'),
 # registrations
 'rs_off':     ('Tasas oficiales por registro (DNFD 500 + MEF + Colegio)', 'B/.', 570, 570, 570, 'F: DE 27 art. 15; MEF y Colegio guía MINSA 2012'),
 'rs_iea':     ('Análisis de control previo IEA por producto', 'B/.', 1500, 600, 300, 'F: rango oficial 200-1,000 (2012); E: cotizar con el IEA'),
 'rs_law':     ('Honorario y gastos del abogado por registro', 'B/.', 1350, 800, 500, 'F: SignatureLex 600 + 750; arancel mínimo 500'),
 'rs_smp':     ('Muestras y courier por registro', 'B/.', 300, 150, 100, 'E'),
 'rs_succ':    ('Registros aprobados / registros presentados', '%', 0.70, 0.85, 0.95, 'E: expedientes débiles, observaciones de la DNFD'),
 'postreg':    ('Análisis posregistro por producto (2 en 5 años), por año', 'B/.', 600, 240, 120, 'F: Ley 419 art. 67; E: costo'),
 'n2':         ('Productos de la segunda ola (sin equivalencia terapéutica, fabricante verificado)', 'SKU', 0, 6, 12, 'E: candidatos del catálogo con compras públicas: ibuprofeno 400, ambroxol jarabe, gliclazida 80, amoxicilina susp., loratadina, diclofenaco, eritromicina, cefepima'),
 'm2':         ('Mes en que se presentan los registros de la segunda ola', 'mes', 24, 18, 15, 'Decisión: solo si la primera ola cumple la compuerta'),
 'rel2':       ('Ingreso por producto de la segunda ola vs promedio de la primera', 'x', 0.5, 0.7, 1.0, 'E: los mejores productos van en la primera ola'),
 'fact_share': ('Porcentaje de las ventas que se factoriza', '%', 0.0, 0.0, 0.0, 'Opción de financiamiento; Ley 22 art. 97 permite ceder créditos'),
 'fact_cost':  ('Costo mensual del factoring sobre el monto cedido', '%', 0.015, 0.0125, 0.010, 'F: Balboa Factoring 2025: 14.6%-18.3% anual'),
 'stop_det':   ('Mes de cierre del negocio (61 = no se cierra)', 'mes', 61, 61, 61, 'Compuerta operativa: cerrar si nueve meses después de la primera venta las ventas anualizadas no cubren el umbral'),
 'inv_liq':    ('Recuperación del inventario si se cierra', '%', 0.5, 0.5, 0.5, 'E: venta a otros distribuidores o devolución parcial'),
 # tax & valuation
 'isr':        ('Impuesto sobre la renta', '%', 0.25, 0.25, 0.25, 'F: Código Fiscal art. 699'),
 'divtax':     ('Impuesto de dividendos', '%', 0.10, 0.10, 0.10, 'F: Código Fiscal art. 733'),
 'aviso':      ('Impuesto de aviso de operación (% del patrimonio al cierre de cada año; mínimo B/.100; pagado en marzo)', '%', 0.02, 0.02, 0.02, 'F: Ley 8 de 2010 art. 69 (Código Fiscal art. 1004); base = activos menos pasivos (PwC). En el modelo no se deduce de la renta'),
 'oncost':     ('Cargas laborales sobre sueldos del regente y del coordinador', '%', 0.28, 0.28, 0.28, 'F: CSS patronal 13.25% (sube a 15.25% en 2029, Ley 462 de 2025), seguro educativo 1.5%, riesgos profesionales, XIII mes y prima de antigüedad (PwC 2026; Código de Trabajo); E: promedio del horizonte'),
 'itbms_srv':  ('ITBMS no recuperable sobre servicios contratados', '%', 0.07, 0.07, 0.0, 'F: ITBMS 7% (DGI); recuperable como "asimilado a exportador" solo si la S.A. se dedica exclusivamente a importar medicamentos y vende todo en Panamá (Ley 8 de 2010 art. 80)'),
 'payout':     ('Porcentaje distribuible que se reparte cada año', '%', 0.80, 0.80, 0.80, 'Política'),
 'disc':       ('Tasa de descuento anual para el VPN', '%', 0.30, 0.30, 0.30, 'E: retorno exigido a una pyme nueva con riesgo de socio y de cobro'),
 'recov':      ('Recuperación del capital de trabajo al cierre (cobro, inventario, colateral)', '%', 0.80, 0.90, 0.95, 'E'),
 'gc_mult':    ('Múltiplo de la utilidad neta del año 5 (negocio en marcha)', 'x', 0.0, 3.0, 4.0, 'E: distribuidora pequeña con un solo cliente estatal'),
 # ownership
 'patel_eq':   ('Participación de Patel en la S.A.', '%', 0.50, 0.50, 0.50, 'F: propuesta de Patel (50/50)'),
 'patel_cash': ('Porcentaje del capital que aporta Patel', '%', 0.50, 0.50, 0.50, 'F: Patel pide dividir costos 50/50'),
 'jaime_frac': ('Fracción de Jaime dentro del 50% panameño', '%', 1/3, 1/3, 1/3, 'F: tres socios panameños por partes iguales'),
 'zy_markup':  ('Margen de Zywie sobre el precio de fábrica (dentro del índice del proveedor)', '%', 0.25, 0.15, 0.05, 'E: comercializadora intermediaria'),
}

# Fixed monthly costs: (label, pes, base, opt, start_rule, source)
# start_rule: 'm1' month 1, 'lic' license month (3), 'prep' = reg_m - 1
FIXED = [
 ('Regente farmacéutico (medio tiempo, mínimo 4 h/día)', 1200, 700, 450, 'lic', 'F: DE 27 art. 382; SignatureLex 400-500; Paylab 1,339-3,228 tiempo completo'),
 ('3PL farmacéutico licenciado: cuota mínima', 1200, 600, 300, 'lic', 'B7: mínimo 300-1,200; sin cotización firme'),
 ('Contabilidad e impuestos', 450, 300, 200, 'm1', 'E'),
 ('Auditoría anual (requisito de fianzas y Registro de Oferentes), prorrateada', 400, 250, 150, 'm1', 'F: DE 27 art. 725 exige estados certificados por CPA; E: costo'),
 ('Asesoría legal por hora (sin iguala mensual)', 800, 300, 150, 'm1', 'E; SignatureLex propone iguala de 2,000'),
 ('Coordinador de licitaciones y operaciones (medio tiempo)', 2500, 1500, 800, 'prep', 'E: alguien debe vigilar PanamaCompra a diario y armar ofertas'),
 ('Seguros (responsabilidad civil y de producto)', 200, 100, 75, 'lic', 'E'),
 ('Software, banca, telecomunicaciones y administración', 200, 120, 80, 'm1', 'E'),
 ('Impuesto municipal', 200, 100, 100, 'm1', 'F: tope PwC; E: tramo'),
]
LIC_M = 3
# cost type of each fixed line: 'staff' carries employer on-costs, 'service' carries non-recoverable ITBMS, 'other' neither
FIXED_KIND = ['staff', 'service', 'service', 'service', 'service', 'staff', 'other', 'service', 'other']
ANNUAL_CHARGES = [('Tasa única S.A.', 300, 'F: DGI'), ('Agente residente', 250, 'F: mercado 250-350')]
ANNUAL_KIND = ['other', 'service']
# the aviso de operación is computed each year on equity (parameter 'aviso'), no longer a flat annual charge

# Setup one-offs: (label, pes, base, opt, month, signaturelex_quote, source)
SETUP = [
 ('Due diligence de fabricante y documentos (fase 0, antes de constituir)', 6000, 2500, 1000, 0, 0, 'E: auditoría virtual de planta y verificación documental'),
 ('Constitución, libros, poderes, RUC, aviso de operación y municipal', 3500, 2500, 1500, 1, 5700, 'F: SignatureLex ~5,700; Díaz & Asociados 1,500 (S.A. operativa)'),
 ('Pacto de accionistas, contrato de suministro exclusivo y acuerdo de calidad', 4000, 2500, 1500, 1, 1750, 'F: SignatureLex 1,500 + 1% escalonado; E'),
 ('Diagnóstico regulatorio inicial y matriz de portafolio', 650, 650, 500, 1, 650, 'F: SignatureLex 500 + 150'),
 ('Apoyo para abrir cuenta bancaria', 3150, 300, 0, 1, 3150, 'F: SignatureLex 3,000 + 150'),
 ('Licencia de operación: tasa oficial 250 + planos, SOP e inspección', 4000, 1750, 1000, 2, 4000, 'F: DE 27 art. 15 (200 + 50); SignatureLex 3,500 + 500'),
 ('Revisión del 3PL y acuerdo de calidad', 2650, 750, 400, 2, 2650, 'F: SignatureLex 2,500 + 150'),
 ('Programa de cumplimiento y anticorrupción', 3150, 1500, 800, 2, 3150, 'F: SignatureLex 3,000 + 150'),
 ('Certificado de BPA', 100, 100, 100, 3, 100, 'F: DE 27 art. 15'),
 ('Registro patronal CSS y contratos laborales', 900, 300, 100, 3, 900, 'F: SignatureLex 750 + 150'),
 ('PanamaCompra, Registro Nacional de Oferentes y proveedor CSS', 2700, 500, 0, 4, 2700, 'F: SignatureLex 3 x (750 + 150); trámites sin tasa oficial'),
]
# professional services carry ITBMS; official fees do not (the BPA certificate is an official fee)
SETUP_KIND = ['service', 'service', 'service', 'service', 'service', 'service', 'service', 'service', 'other', 'service', 'service']
RS_PAY_M = 3   # month when registration costs are paid (filing + IEA)
