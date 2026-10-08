# -*- coding: utf-8 -*-
"""Builds the live Excel model (formulas) that mirrors engine.py in deterministic mode,
plus static result sheets (Monte Carlo, sensitivity, scenarios) exported from Python."""
import json, sys
import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.workbook.defined_name import DefinedName
from openpyxl.comments import Comment
from inputs import SKUS, P, FIXED, SETUP, ANNUAL_CHARGES, LIC_M, RS_PAY_M, FIXED_KIND, SETUP_KIND, ANNUAL_KIND

OUT = sys.argv[1] if len(sys.argv) > 1 else 'modelo.xlsx'
A = json.load(open('analysis.json'))
S3 = json.load(open('stats_v3.json'))     # 20,000-scenario Monte Carlo statistics (model v3)
S3.update(json.load(open('stats_v3b.json')))   # Bueno-financed variants with a different coordinator cost
IEK = json.load(open('ie_kelly.json'))
OC = json.load(open('option_c.json'))


F = 'Arial'
BLUE = Font(name=F, color='0000FF', size=10)
BLACK = Font(name=F, color='000000', size=10)
GREEN = Font(name=F, color='008000', size=10)
BOLD = Font(name=F, bold=True, size=10)
TITLE = Font(name=F, bold=True, size=14)
SUB = Font(name=F, bold=True, size=11, color='1F3864')
NOTE = Font(name=F, italic=True, size=9, color='595959')
YEL = PatternFill('solid', fgColor='FFFF00')
HEAD = PatternFill('solid', fgColor='D9E1F2')
GREY = PatternFill('solid', fgColor='F2F2F2')
thin = Side(style='thin', color='BFBFBF')
BOX = Border(top=thin, bottom=thin, left=thin, right=thin)
NUM = '#,##0;(#,##0);"-"'
NUM2 = '#,##0.00;(#,##0.00);"-"'
NUM4 = '0.0000;(0.0000);"-"'
PCT = '0.0%;(0.0%);"-"'
MULT = '0.00"x"'

wb = Workbook()
names = {}


def name(nm, ref):
    wb.defined_names[nm] = DefinedName(nm, attr_text=ref)
    names[nm] = ref


def hdr(ws, row, cols, labels, widths=None):
    for c, lab in zip(cols, labels):
        cell = ws.cell(row=row, column=c, value=lab)
        cell.font = BOLD; cell.fill = HEAD; cell.alignment = Alignment(wrap_text=True, vertical='center'); cell.border = BOX


def setw(ws, widths):
    for k, v in widths.items():
        ws.column_dimensions[k].width = v


def put(ws, r, c, v, font=BLACK, fmt=None, fill=None, wrap=False, comment=None):
    cell = ws.cell(row=r, column=c, value=v)
    cell.font = font
    if fmt: cell.number_format = fmt
    if fill: cell.fill = fill
    if wrap: cell.alignment = Alignment(wrap_text=True, vertical='top')
    if comment: cell.comment = Comment(comment, 'Modelo')
    return cell

# =============================================================== Léeme
ws = wb.active; ws.title = 'Léeme'
setw(ws, {'A': 110})
lines = [
 ('Modelo financiero: distribuidora de medicamentos para compras públicas en Panamá', TITLE),
 ('Preparado el 6 de octubre de 2026 como apoyo del plan de negocio. Cifras en balboas (B/. = US$).', NOTE),
 ('', None),
 ('Cómo usarlo', SUB),
 ('1. Elija el escenario en Supuestos!B3 (1 = pesimista, 2 = base, 3 = optimista). Todo el modelo se recalcula.', BLACK),
 ('2. Cambie cualquier valor azul de las columnas D, E o F de Supuestos, o la columna "Incluir" de SKUs, para probar otra hipótesis.', BLACK),
 ('3. Supuestos!B4 = 1 aplica las tarifas de la propuesta de SignatureLex en lugar de las de mercado.', BLACK),
 ('4. Resultados vivos: Valoración (VPN, TIR, múltiplo, capital requerido), Anual (estado de resultados e impuestos), Mensual (flujo de caja).', BLACK),
 ('5. Las hojas Escenarios, Monte Carlo y Sensibilidad son resultados fijos del motor en Python (20,000 simulaciones); no cambian al editar supuestos.', BLACK),
 ('', None),
 ('Convenciones', SUB),
 ('Texto azul = dato de entrada o supuesto editable. Negro = fórmula. Verde = vínculo a otra hoja. Relleno amarillo = supuestos clave.', BLACK),
 ('F = dato verificado en fuente abierta (URL en Fuentes o en la columna Fuente). E = estimación del analista, a validar.', BLACK),
 ('', None),
 ('Lógica del modelo (mes a mes, 60 meses desde la constitución de la S.A.)', SUB),
 ('Ventas descentralizadas = demanda anual pública x factor de mercado x precio de oferta x probabilidad de registro x participación x rampa.', BLACK),
 ('Ventas centralizadas = demanda x precio x probabilidad de ganar x realización de cantidades (LPU CSS y compra centralizada MINSA).', BLACK),
 ('Solo se oferta un producto en un canal si el margen bruto supera el mínimo (35% descentralizado, 20% centralizado).', BLACK),
 ('Inventario objetivo = meses de cobertura x costo del mes siguiente; compras pagadas con anticipo al ordenar y saldo al embarque (menos crédito del proveedor).', BLACK),
 ('Cobro = ventas de hace "días de cobro" meses. Fianzas de cumplimiento sobre la cantidad máxima del contrato (30% LPU, 20% MINSA) y fianza de propuesta de 10% en la LPU para renglones de más de B/.70,000, con el colateral exigido inmovilizado.', BLACK),
 ('Costos fijos con cargas laborales (28%) sobre regente y coordinador e ITBMS no recuperable (7%) sobre servicios; los gastos de arranque y el abogado de registros también llevan ITBMS.', BLACK),
 ('Aportes de capital = lo necesario para mantener la caja mínima. Dividendos a los meses 24, 36 y 48 si hay utilidades y caja.', BLACK),
 ('Valor terminal (mes 60): caja + recuperación del capital de trabajo (conservador) o múltiplo de la utilidad del año 5 (negocio en marcha).', BLACK),
 ('Impuestos: ISR 25%, pérdidas arrastrables 5 años al 20% anual con tope de 50% de la renta, CAIR si ventas > B/.1.5 millones, dividendos 10%, aviso de operación 2% del patrimonio cada año (pagado en marzo; el modelo no lo deduce de la renta).', BLACK),
 ('', None),
 ('Limitaciones', SUB),
 ('Sin precios de Zywie, el costo del producto parte de una referencia FOB por producto (hoja SKUs) hecha con precios públicos de India: licitaciones estatales para cinco productos (tres con un recargo de 35-40% para llevarlas a precio de exportación), precios de Jan Aushadhi para otros cinco y un supuesto para la nistatina. Esa referencia se multiplica por el índice del proveedor (1.25 en el caso base); la compuerta 0 (1.1 veces) y el descarte de la simulación (1.6 veces) se miden contra la misma referencia. La demanda usa compras 2025-2026 anualizadas; la del MINSA está incompleta.', BLACK),
 ('No incluye ventas al sector privado ni productos que exigen equivalencia terapéutica (bioequivalencia).', BLACK),
 ('Decisiones que favorecen el caso base (VPN al 15% con cada cambio por separado): ver la hoja Escenarios y el plan de negocio.', BLACK),
 ('Las variantes «Reestructurado» de la hoja Escenarios y la de Bueno financiando suponen un coordinador con sueldo de B/.1,000 al mes (más cargas); el caso base usa B/.1,500 y la simulación sortea entre 800 y 2,500.', BLACK),
]
for i, (t, f) in enumerate(lines, start=1):
    c = ws.cell(row=i, column=1, value=t)
    if f: c.font = f
    c.alignment = Alignment(wrap_text=True)

# =============================================================== Supuestos
ws = wb.create_sheet('Supuestos')
setw(ws, {'A': 13, 'B': 62, 'C': 9, 'D': 12, 'E': 12, 'F': 12, 'G': 12, 'H': 70, 'I': 10})
put(ws, 1, 1, 'Supuestos', TITLE)
put(ws, 3, 1, 'Escenario', BOLD); put(ws, 3, 2, 2, BLUE, fill=YEL, comment='1 = pesimista, 2 = base, 3 = optimista')
put(ws, 3, 3, '=CHOOSE($B$3,"Pesimista","Base","Optimista")', BLACK)
put(ws, 4, 1, 'SignatureLex', BOLD); put(ws, 4, 2, 0, BLUE, fill=YEL, comment='1 = usar tarifas de la propuesta de SignatureLex; 0 = tarifas de mercado')
put(ws, 4, 3, 'Usar tarifas de la propuesta de SignatureLex (1) o de mercado (0)', NOTE)
name('p_sc', "Supuestos!$B$3"); name('p_sl', "Supuestos!$B$4")
r = 6
hdr(ws, r, range(1, 9), ['Clave', 'Parámetro', 'Unidad', 'Pesimista', 'Base', 'Optimista', 'Usado', 'Fuente o base'])
r += 1
key_rows = {}
key_assumptions = {'sup_idx', 'share_dec', 'pwin_cen', 'dso_days', 'reg_m', 'cen_start', 'credit_days', 'adv', 'mkt', 'n2'}
for k, v in P.items():
    lab, unit, pes, base, opt, src = v
    put(ws, r, 1, k, NOTE)
    put(ws, r, 2, lab, BLACK, wrap=True)
    put(ws, r, 3, unit, BLACK)
    fmt = PCT if unit == '%' else (MULT if unit == 'x' else NUM)
    if k in ('sup_idx', 'log_mult', 'mkt', 'pf_dec', 'pf_cen', 'gc_mult', 'rel2'):
        fmt = '0.00'
    for j, val in enumerate((pes, base, opt)):
        put(ws, r, 4 + j, val, BLUE, fmt, fill=YEL if k in key_assumptions else None)
    if k == 'rs_law':
        f = '=IF(p_sl=1,1350,CHOOSE(p_sc,D{0},E{0},F{0}))'.format(r)
    elif k == 'rs_iea':
        f = '=IF(p_sl=1,1500,CHOOSE(p_sc,D{0},E{0},F{0}))'.format(r)
    else:
        f = '=CHOOSE(p_sc,D{0},E{0},F{0})'.format(r)
    put(ws, r, 7, f, BLACK, fmt)
    put(ws, r, 8, src, NOTE, wrap=True)
    name('p_' + k, f"Supuestos!$G${r}")
    key_rows[k] = r
    r += 1

r += 1
put(ws, r, 1, 'Costos fijos mensuales (B/./mes)', SUB); r += 1
hdr(ws, r, range(1, 11), ['#', 'Concepto', 'Inicio', 'Pesimista', 'Base', 'Optimista', 'Usado (con cargas o ITBMS)', 'Fuente o base', 'Mes inicio', 'Tipo'])
r += 1
f_first = r
KLAB = {'staff': 'sueldo + cargas laborales', 'service': 'servicio + ITBMS', 'other': 'otro'}
KF = {'staff': '*(1+p_oncost)', 'service': '*(1+p_itbms_srv)', 'other': ''}
for i, fx in enumerate(FIXED, start=1):
    lab, pes, base, opt, rule, src = fx
    kd = FIXED_KIND[i - 1]
    put(ws, r, 1, i, NOTE); put(ws, r, 2, lab, BLACK, wrap=True)
    put(ws, r, 3, {'m1': 'mes 1', 'lic': 'licencia', 'prep': 'registros - 1'}[rule], BLACK)
    for j, val in enumerate((pes, base, opt)):
        put(ws, r, 4 + j, val, BLUE, NUM)
    put(ws, r, 7, f'=CHOOSE(p_sc,D{r},E{r},F{r}){KF[kd]}', BLACK, NUM)
    put(ws, r, 8, src, NOTE, wrap=True)
    start = '1' if rule == 'm1' else ('c_lic_m' if rule == 'lic' else 'MAX(c_reg_m-1,1)')
    put(ws, r, 9, '=' + start, BLACK, NUM)
    put(ws, r, 10, KLAB[kd], NOTE)
    r += 1
f_last = r - 1
put(ws, r, 2, 'Total costos fijos a plena operación', BOLD); put(ws, r, 7, f'=SUM(G{f_first}:G{f_last})', BOLD, NUM)
name('f_used', f"Supuestos!$G${f_first}:$G${f_last}"); name('f_start', f"Supuestos!$I${f_first}:$I${f_last}")
name('f_total', f"Supuestos!$G${r}")
r += 2
put(ws, r, 1, 'Gastos de arranque, una sola vez (B/.)', SUB); r += 1
hdr(ws, r, range(1, 11), ['#', 'Concepto', 'Mes', 'Pesimista', 'Base', 'Optimista', 'Usado (con ITBMS)', 'Fuente o base', 'SignatureLex', 'Tipo'])
r += 1
u_first = r
for i, s in enumerate(SETUP, start=1):
    lab, pes, base, opt, month, slq, src = s
    kd = SETUP_KIND[i - 1]
    put(ws, r, 1, i, NOTE); put(ws, r, 2, lab, BLACK, wrap=True); put(ws, r, 3, month, BLUE, NUM)
    for j, val in enumerate((pes, base, opt)):
        put(ws, r, 4 + j, val, BLUE, NUM)
    put(ws, r, 9, slq, BLUE, NUM)
    put(ws, r, 7, f'=IF(AND(p_sl=1,I{r}>0),I{r},CHOOSE(p_sc,D{r},E{r},F{r})){KF[kd]}', BLACK, NUM)
    put(ws, r, 8, src, NOTE, wrap=True)
    put(ws, r, 10, KLAB[kd], NOTE)
    r += 1
u_last = r - 1
put(ws, r, 2, 'Total arranque (incluye fase 0)', BOLD); put(ws, r, 7, f'=SUM(G{u_first}:G{u_last})', BOLD, NUM)
name('u_used', f"Supuestos!$G${u_first}:$G${u_last}"); name('u_month', f"Supuestos!$C${u_first}:$C${u_last}")
name('c_phase0', f"Supuestos!$G${u_first}")
r += 2
put(ws, r, 1, 'Cargos anuales (meses 1, 13, 25, 37 y 49; el aviso de operación se calcula aparte sobre el patrimonio)', SUB); r += 1
a_first = r
for (lab, val, src), kd in zip(ANNUAL_CHARGES, ANNUAL_KIND):
    put(ws, r, 2, lab, BLACK); put(ws, r, 5, val, BLUE, NUM); put(ws, r, 7, f'=E{r}{KF[kd]}', BLACK, NUM); put(ws, r, 8, src, NOTE)
    put(ws, r, 10, KLAB[kd], NOTE); r += 1
put(ws, r, 2, 'Total cargos anuales', BOLD); put(ws, r, 7, f'=SUM(G{a_first}:G{r-1})', BOLD, NUM); name('c_annual', f"Supuestos!$G${r}")
r += 2
put(ws, r, 1, 'Valores calculados (no editar)', SUB); r += 1
calc = [
 ('c_lic_m', 'Mes de la licencia de operación', str(LIC_M)),
 ('c_rs_pay_m', 'Mes en que se pagan los registros de la primera ola', str(RS_PAY_M)),
 ('c_lead_m', 'Tiempo de reposición (meses)', 'ROUND(p_lead_days/30,0)'),
 ('c_dso_m', 'Días de cobro (meses)', 'ROUND(p_dso_days/30,0)'),
 ('c_credit_m', 'Crédito del proveedor (meses)', 'ROUND(p_credit_days/30,0)'),
 ('c_ship_m', 'Embarque a stock (meses)', 'ROUND(p_ship_m,0)'),
 ('c_reg_m', 'Mes de registros (entero)', 'ROUND(p_reg_m,0)'),
 ('c_first_dec', 'Primer mes con ventas descentralizadas', 'c_reg_m+c_lead_m'),
 ('c_cen_start', 'Primer mes con contrato centralizado', 'MAX(ROUND(p_cen_start,0),c_first_dec)'),
 ('c_rt', 'Meses de trámite del registro', 'MAX(c_reg_m-c_rs_pay_m,1)'),
 ('c_m2', 'Mes de registros de la segunda ola', 'ROUND(p_m2,0)'),
 ('c_first_dec2', 'Primer mes con ventas de la segunda ola', 'c_m2+c_rt+c_lead_m'),
 ('c_n1', 'Productos presentados en la primera ola', 'MAX(SUM(SKUs!$D$6:$D$24),1)'),
 ('c_k2', 'Factor de escala de la segunda ola', 'p_n2*p_rel2/c_n1'),
 ('c_rs_unit', 'Costo total por registro (B/.; ITBMS sobre el abogado)', 'p_rs_off+p_rs_iea+p_rs_law*(1+p_itbms_srv)+p_rs_smp'),
 ('c_bid_m', 'Meses de colateral de la fianza de propuesta (entero)', 'ROUND(p_bid_m,0)'),
 ('c_n_reg1', 'Registros aprobados esperados, primera ola', 'SUM(SKUs!$D$6:$D$24)*p_rs_succ'),
 ('c_n_reg2', 'Registros aprobados esperados, segunda ola', 'p_n2*p_rs_succ'),
]
for nm, lab, f in calc:
    put(ws, r, 1, nm, NOTE); put(ws, r, 2, lab, BLACK); put(ws, r, 7, '=' + f, BLACK, '0.00' if nm == 'c_k2' else NUM)
    name(nm, f"Supuestos!$G${r}"); r += 1
ws.freeze_panes = 'C7'

# =============================================================== SKUs
ws = wb.create_sheet('SKUs')
cols = ['ID', 'Producto', 'Grupo', 'Incluir (1/0)', 'FOB base (B/./u)', 'Logística (B/./u)', 'Fuente del costo',
        'CSS LPU: unid./año', 'CSS LPU: precio', 'MINSA central: unid./año', 'MINSA central: precio',
        'CSS desc.: unid./año', 'CSS desc.: precio', 'MINSA/patronatos desc.: unid./año', 'MINSA/patronatos desc.: precio',
        'Costo puesto en Panamá', 'Precio oferta LPU', 'Precio oferta MINSA central', 'Precio oferta CSS desc.', 'Precio oferta MINSA desc.',
        'Margen LPU', 'Margen MINSA central', 'Margen CSS desc.', 'Margen MINSA desc.',
        'Oferta LPU', 'Oferta MINSA central', 'Oferta CSS desc.', 'Oferta MINSA desc.',
        'Ventas CSS desc. (madurez)', 'Ventas MINSA desc. (madurez)', 'Ventas LPU si gana', 'Ventas MINSA central si gana',
        'Costo CSS desc.', 'Costo MINSA desc.', 'Costo LPU', 'Costo MINSA central',
        'Ventas esperadas año maduro', 'Utilidad bruta esperada', 'Costo FOB (para Zywie)', 'Oferta LPU con fianza de propuesta (B/./año)']
put(ws, 1, 1, 'Portafolio y economía por producto', TITLE)
put(ws, 2, 1, 'Demanda pública anualizada 2025-26 (r2e); precios medianos o adjudicados; costos puestos con referencias de India (B2). Ventas a madurez antes de rampa y erosión.', NOTE)
put(ws, 3, 1, 'Canales: LPU = licitación de precio único CSS; MINSA central = subasta en reversa o compra conjunta; desc. = contratación menor y compra menor ágil.', NOTE)
hdr(ws, 5, range(1, len(cols) + 1), cols)
ws.row_dimensions[5].height = 60
for i, s in enumerate(SKUS):
    r = 6 + i
    vals = [s['id'], s['name'], s['group'], s['inc'], s['fob'], s['adder'], s['src_cost'], s['q1'], s['p1'], s['q2'], s['p2'], s['q3'], s['p3'], s['q4'], s['p4']]
    for j, v in enumerate(vals, start=1):
        fmt = NUM if j in (8, 10, 12, 14) else (NUM4 if j in (5, 6, 9, 11, 13, 15) else None)
        put(ws, r, j, v, BLUE if j >= 4 and j != 7 else BLACK, fmt, wrap=(j in (2, 7)))
    put(ws, r, 16, f'=E{r}*p_sup_idx*(1+p_pack)+F{r}*p_log_mult', BLACK, NUM4)
    put(ws, r, 17, f'=I{r}*p_pf_cen', BLACK, NUM4)
    put(ws, r, 18, f'=K{r}*p_pf_cen', BLACK, NUM4)
    put(ws, r, 19, f'=M{r}*p_pf_dec', BLACK, NUM4)
    put(ws, r, 20, f'=O{r}*p_pf_dec', BLACK, NUM4)
    for j, pc in enumerate(('Q', 'R', 'S', 'T')):
        put(ws, r, 21 + j, f'=IF({pc}{r}>0,1-P{r}/{pc}{r},-9)', BLACK, PCT)
    for j, (qc, gc, mn) in enumerate((('H', 'U', 'p_gm_cen'), ('J', 'V', 'p_gm_cen'), ('L', 'W', 'p_gm_dec'), ('N', 'X', 'p_gm_dec'))):
        put(ws, r, 25 + j, f'=IF(AND($D{r}=1,{qc}{r}>0,{gc}{r}>={mn}),1,0)', BLACK, '0')
    put(ws, r, 29, f'=AA{r}*L{r}*p_mkt*S{r}*p_rs_succ*p_share_dec', BLACK, NUM)
    put(ws, r, 30, f'=AB{r}*N{r}*p_mkt*T{r}*p_rs_succ*p_share_dec', BLACK, NUM)
    put(ws, r, 31, f'=Y{r}*H{r}*p_mkt*Q{r}*p_rs_succ*p_realiz', BLACK, NUM)
    put(ws, r, 32, f'=Z{r}*J{r}*p_mkt*R{r}*p_rs_succ*p_realiz', BLACK, NUM)
    put(ws, r, 33, f'=IF(S{r}>0,AC{r}*P{r}/S{r},0)', BLACK, NUM)
    put(ws, r, 34, f'=IF(T{r}>0,AD{r}*P{r}/T{r},0)', BLACK, NUM)
    put(ws, r, 35, f'=IF(Q{r}>0,AE{r}*P{r}/Q{r},0)', BLACK, NUM)
    put(ws, r, 36, f'=IF(R{r}>0,AF{r}*P{r}/R{r},0)', BLACK, NUM)
    put(ws, r, 37, f'=AC{r}+AD{r}+AE{r}*p_pwin_cen+AF{r}*p_pwin_cen*p_minsa_occ', BLACK, NUM)
    put(ws, r, 38, f'=(AC{r}-AG{r})+(AD{r}-AH{r})+(AE{r}-AI{r})*p_pwin_cen+(AF{r}-AJ{r})*p_pwin_cen*p_minsa_occ', BLACK, NUM)
    put(ws, r, 39, f'=IF(P{r}>0,E{r}*p_sup_idx*(1+p_pack)/P{r},0)', BLACK, PCT)
    put(ws, r, 40, f'=IF(AND(Y{r}=1,H{r}*I{r}*15/12>70000),H{r}*p_mkt*Q{r}*p_rs_succ,0)', BLACK, NUM)
last = 6 + len(SKUS) - 1
tr = last + 1
put(ws, tr, 2, 'Totales (productos incluidos)', BOLD)
for c in range(29, 39):
    L = CL(c)
    put(ws, tr, c, f'=SUM({L}6:{L}{last})', BOLD, NUM)
put(ws, tr, 39, f'=IF(SUM(AG6:AJ{last})>0,SUMPRODUCT(AG6:AG{last}+AH6:AH{last}+AI6:AI{last}+AJ6:AJ{last},AM6:AM{last})/SUM(AG6:AJ{last}),0)', BOLD, PCT)
name('s_Rd', f"SKUs!$AC${tr}:$AD${tr}")
put(ws, tr, 40, f'=SUM(AN6:AN{last})', BOLD, NUM)
for nm, c in (('s_Rd3', 'AC'), ('s_Rd4', 'AD'), ('s_Rc1', 'AE'), ('s_Rc2', 'AF'), ('s_Rd3k', 'AG'), ('s_Rd4k', 'AH'), ('s_Rc1k', 'AI'), ('s_Rc2k', 'AJ'), ('s_fob_share', 'AM'), ('s_rev_exp', 'AK'), ('s_gp_exp', 'AL'), ('s_bid', 'AN')):
    name(nm, f"SKUs!${c}${tr}")
setw(ws, {'A': 8, 'B': 40, 'C': 8, 'D': 8, 'G': 34})
for c in range(5, 41):
    if CL(c) != 'G':
        ws.column_dimensions[CL(c)].width = 11
ws.freeze_panes = 'C6'

# =============================================================== Mensual
ws = wb.create_sheet('Mensual')
setw(ws, {'A': 46, 'B': 9})
put(ws, 1, 1, 'Flujo mensual (B/.)', TITLE)
M0 = 3  # column C = month 0; month m -> column 3+m
def mc_(m): return CL(3 + m)
R = {}
rows = ['mes', 'anio', 'eros', 'activo', 'ramp1', 'ramp2', 'cen_on', 'cen2_on', 'mult_dec', 'mult_cen', 'v_dec', 'v_cen', 'ventas',
        'k_dec', 'k_cen', 'costo', 'inv', 'llegadas', 'pago_ant', 'pago_sal', 'pagos', 'cobranza', 'var', 'fijos', 'posreg', 'setup',
        'registros', 'anuales', 'afianzado', 'fianza_prop', 'colateral', 'dcol', 'prima', 'factoring', 'perdida_cierre', 'uai', 'imp_pagado',
        'aviso', 'caja_pre', 'caja_min', 'aporte', 'dividendo', 'caja', 'flujo_inv']
labels = {'mes': 'Mes', 'anio': 'Año', 'eros': 'Factor de erosión de precios', 'activo': 'Negocio activo (1/0)',
          'ramp1': 'Rampa primera ola', 'ramp2': 'Rampa segunda ola', 'cen_on': 'Contratos centralizados activos', 'cen2_on': 'Centralizado segunda ola',
          'mult_dec': 'Multiplicador descentralizado (olas)', 'mult_cen': 'Multiplicador centralizado (olas)',
          'v_dec': 'Ventas descentralizadas', 'v_cen': 'Ventas centralizadas', 'ventas': 'VENTAS TOTALES',
          'k_dec': 'Costo de ventas descentralizado', 'k_cen': 'Costo de ventas centralizado', 'costo': 'COSTO DE VENTAS',
          'inv': 'Inventario objetivo al cierre (costo)', 'llegadas': 'Mercancía recibida (costo, incl. mermas)',
          'pago_ant': 'Pago de anticipos al proveedor', 'pago_sal': 'Pago de saldos al proveedor', 'pagos': 'PAGOS AL PROVEEDOR',
          'cobranza': 'COBRANZA (incl. liquidación de inventario al cierre)', 'var': 'Gastos variables (distribución y multas)',
          'fijos': 'Costos fijos', 'posreg': 'Análisis posregistro', 'setup': 'Gastos de arranque', 'registros': 'Registros sanitarios',
          'anuales': 'Cargos anuales', 'afianzado': 'Monto afianzado (cumplimiento, sobre la cantidad máxima)',
          'fianza_prop': 'Fianza de propuesta vigente (LPU)', 'aviso': 'Impuesto de aviso de operación pagado', 'colateral': 'Colateral inmovilizado',
          'dcol': 'Cambio en colateral', 'prima': 'Prima de fianzas', 'factoring': 'Costo de factoring',
          'perdida_cierre': 'Pérdida de inventario por cierre', 'uai': 'UTILIDAD ANTES DE IMPUESTOS', 'imp_pagado': 'Impuesto sobre la renta pagado',
          'caja_pre': 'Caja antes de aportes', 'caja_min': 'Caja mínima requerida', 'aporte': 'APORTE DE CAPITAL', 'dividendo': 'DIVIDENDO PAGADO',
          'caja': 'CAJA AL CIERRE', 'flujo_inv': 'FLUJO DE LOS ACCIONISTAS (sin valor terminal)'}
for i, k in enumerate(rows):
    R[k] = 3 + i
    put(ws, R[k], 1, labels[k], BOLD if labels[k].isupper() or k in ('ventas', 'costo', 'uai', 'aporte', 'caja') else BLACK)
put(ws, 2, 3, 'Mes 0', NOTE)
rng60 = lambda k: f"$D${R[k]}:$BK${R[k]}"
name('m_mes', f"Mensual!$D${R['mes']}:$BK${R['mes']}")
for m in range(0, 62):
    c = 3 + m; L = CL(c); Lp = CL(c - 1); Ln = CL(c + 1)
    f = {}
    f['mes'] = m
    if m == 0:
        put(ws, R['mes'], c, 0, BLACK, '0')
        put(ws, R['flujo_inv'], c, '=-c_phase0', BLACK, NUM)
        put(ws, R['caja'], c, 0, BLACK, NUM)
        put(ws, R['inv'], c, 0, BLACK, NUM)
        put(ws, R['colateral'], c, 0, BLACK, NUM)
        continue
    put(ws, R['mes'], c, m, BOLD, '0')
    mm = f'{L}${R["mes"]}'
    put(ws, R['anio'], c, f'=INT((MIN({mm},60)-1)/12)+1', BLACK, '0')
    put(ws, R['eros'], c, f'=(1-p_erosion)^({L}{R["anio"]}-1)', BLACK, '0.000')
    put(ws, R['activo'], c, f'=IF({mm}<=ROUND(p_stop_det,0),1,0)', BLACK, '0')
    put(ws, R['ramp1'], c, f'=MAX(0,MIN(1,({mm}-c_first_dec+1)/p_ramp_m))', BLACK, '0.00')
    put(ws, R['ramp2'], c, f'=MAX(0,MIN(1,({mm}-c_first_dec2+1)/p_ramp_m))', BLACK, '0.00')
    put(ws, R['cen_on'], c, f'=IF({mm}>=c_cen_start,1,0)', BLACK, '0')
    put(ws, R['cen2_on'], c, f'=IF({mm}>=MAX(c_cen_start,c_first_dec2),1,0)', BLACK, '0')
    put(ws, R['mult_dec'], c, f'=1+c_k2*{L}{R["ramp2"]}', BLACK, '0.00')
    put(ws, R['mult_cen'], c, f'=1+c_k2*{L}{R["cen2_on"]}', BLACK, '0.00')
    put(ws, R['v_dec'], c, f'=(s_Rd3+s_Rd4)/12*{L}{R["ramp1"]}*{L}{R["mult_dec"]}*{L}{R["eros"]}*{L}{R["activo"]}', BLACK, NUM)
    put(ws, R['v_cen'], c, f'=(s_Rc1*p_pwin_cen+s_Rc2*p_pwin_cen*p_minsa_occ)/12*{L}{R["cen_on"]}*{L}{R["mult_cen"]}*{L}{R["eros"]}*{L}{R["activo"]}', BLACK, NUM)
    put(ws, R['ventas'], c, f'={L}{R["v_dec"]}+{L}{R["v_cen"]}', BOLD, NUM)
    put(ws, R['k_dec'], c, f'=(s_Rd3k+s_Rd4k)/12*{L}{R["ramp1"]}*{L}{R["mult_dec"]}*{L}{R["activo"]}', BLACK, NUM)
    put(ws, R['k_cen'], c, f'=(s_Rc1k*p_pwin_cen+s_Rc2k*p_pwin_cen*p_minsa_occ)/12*{L}{R["cen_on"]}*{L}{R["mult_cen"]}*{L}{R["activo"]}', BLACK, NUM)
    put(ws, R['costo'], c, f'={L}{R["k_dec"]}+{L}{R["k_cen"]}', BOLD, NUM)
    if m == 61:
        for k in ('inv', 'llegadas'):
            pass
        continue
    put(ws, R['inv'], c, (f'=IF(AND({mm}>=c_first_dec,{mm}<=ROUND(p_stop_det,0)),(s_Rd3k+s_Rd4k)/12*{Ln}{R["ramp1"]}*{Ln}{R["mult_dec"]}*p_cover_m'
                          f'+(s_Rc1k*p_pwin_cen+s_Rc2k*p_pwin_cen*p_minsa_occ)/12*{Ln}{R["cen_on"]}*{Ln}{R["mult_cen"]}*p_cen_stock_m,0)'), BLACK, NUM)
    put(ws, R['llegadas'], c, f'=IF({mm}>ROUND(p_stop_det,0),0,{L}{R["costo"]}*(1+p_expiry)+{L}{R["inv"]}-{Lp}{R["inv"]})', BLACK, NUM)
    put(ws, R['pago_ant'], c, f'=p_adv*IFERROR(INDEX({rng60("llegadas")},1,{mm}+c_lead_m),0)', BLACK, NUM)
    put(ws, R['pago_sal'], c, f'=IF(AND({mm}+c_ship_m-c_credit_m>=1,{mm}+c_ship_m-c_credit_m<=60),(1-p_adv)*INDEX({rng60("llegadas")},1,{mm}+c_ship_m-c_credit_m),0)', BLACK, NUM)
    put(ws, R['pagos'], c, f'={L}{R["pago_ant"]}+{L}{R["pago_sal"]}', BOLD, NUM)
    put(ws, R['cobranza'], c, (f'=(1-p_fact_share)*IF({mm}-c_dso_m>=1,INDEX({rng60("ventas")},1,{mm}-c_dso_m),0)*(1-p_baddebt)'
                               f'+p_fact_share*IF({mm}-1>=1,INDEX({rng60("ventas")},1,{mm}-1),0)*(1-p_baddebt)*(1-p_fact_cost*c_dso_m)'
                               f'+IF({mm}=ROUND(p_stop_det,0)+1,INDEX({rng60("inv")},1,ROUND(p_stop_det,0))*p_inv_liq,0)'), BOLD, NUM)
    put(ws, R['var'], c, f'=(p_dist+p_penal)*{L}{R["ventas"]}', BLACK, NUM)
    put(ws, R['fijos'], c, f'=IF({mm}>ROUND(p_stop_det,0)+3,0,SUMPRODUCT(f_used*({mm}>=f_start)))', BLACK, NUM)
    put(ws, R['posreg'], c, f'=IF({mm}>ROUND(p_stop_det,0)+3,0,c_n_reg1*p_postreg/12*IF({mm}>=c_reg_m,1,0)+c_n_reg2*p_postreg/12*IF({mm}>=c_m2+c_rt,1,0))', BLACK, NUM)
    put(ws, R['setup'], c, f'=SUMIF(u_month,{mm},u_used)', BLACK, NUM)
    put(ws, R['registros'], c, f'=IF({mm}=c_rs_pay_m,SUM(SKUs!$D$6:$D$24)*c_rs_unit,0)+IF({mm}=MAX(1,MIN(60,c_m2)),p_n2*c_rs_unit,0)', BLACK, NUM)
    put(ws, R['anuales'], c, f'=IF({mm}>ROUND(p_stop_det,0)+3,0,IF(OR({mm}=1,{mm}=13,{mm}=25,{mm}=37,{mm}=49),c_annual,0))', BLACK, NUM)
    put(ws, R['afianzado'], c, f'=(s_Rc1*p_pwin_cen*p_bond_css*15/12+s_Rc2*p_pwin_cen*p_minsa_occ*p_bond_minsa)/p_realiz*{L}{R["cen_on"]}*{L}{R["mult_cen"]}*{L}{R["activo"]}', BLACK, NUM)
    put(ws, R['fianza_prop'], c, f'=p_bid_bond*s_bid*15/12*{L}{R["mult_cen"]}*IF(AND({mm}>=c_cen_start-c_bid_m,MOD({mm}-(c_cen_start-c_bid_m),15)<c_bid_m),1,0)*{L}{R["activo"]}', BLACK, NUM)
    put(ws, R['colateral'], c, f'=({L}{R["afianzado"]}+{L}{R["fianza_prop"]})*p_collat', BLACK, NUM)
    put(ws, R['dcol'], c, f'={L}{R["colateral"]}-{Lp}{R["colateral"]}', BLACK, NUM)
    put(ws, R['prima'], c, f'=({L}{R["afianzado"]}+{L}{R["fianza_prop"]})*p_bond_prem/12', BLACK, NUM)
    put(ws, R['factoring'], c, f'=p_fact_share*{L}{R["ventas"]}*(1-p_baddebt)*p_fact_cost*c_dso_m', BLACK, NUM)
    put(ws, R['perdida_cierre'], c, f'=IF({mm}=ROUND(p_stop_det,0)+1,INDEX({rng60("inv")},1,ROUND(p_stop_det,0))*(1-p_inv_liq),0)', BLACK, NUM)
    put(ws, R['uai'], c, (f'={L}{R["ventas"]}-{L}{R["costo"]}*(1+p_expiry)-{L}{R["var"]}-{L}{R["ventas"]}*p_baddebt-{L}{R["factoring"]}'
                          f'-{L}{R["fijos"]}-{L}{R["posreg"]}-{L}{R["setup"]}-{L}{R["registros"]}-{L}{R["anuales"]}-{L}{R["prima"]}-{L}{R["perdida_cierre"]}'), BOLD, NUM)
    put(ws, R['imp_pagado'], c, f'=IF({mm}=15,Anual!$C$14,IF({mm}=27,Anual!$D$14,IF({mm}=39,Anual!$E$14,IF({mm}=51,Anual!$F$14,0))))', GREEN, NUM)
    if m in (15, 27, 39, 51):
        yy = (m - 3) // 12; c12 = CL(3 + 12 * yy); ycl = CL(2 + yy)
        put(ws, R['aviso'], c, (f'=IF({mm}<=ROUND(p_stop_det,0)+3,MAX(100,p_aviso*MAX(0,SUM($D${R["aporte"]}:${c12}${R["aporte"]})'
                                f'+SUM(Anual!$C$15:${ycl}$15)-SUM($D${R["dividendo"]}:${c12}${R["dividendo"]}))),0)'), BLACK, NUM)
    else:
        put(ws, R['aviso'], c, 0, BLACK, NUM)
    put(ws, R['caja_pre'], c, (f'={Lp}{R["caja"]}+{L}{R["cobranza"]}-{L}{R["pagos"]}-{L}{R["var"]}-{L}{R["fijos"]}-{L}{R["posreg"]}-{L}{R["setup"]}'
                               f'-{L}{R["registros"]}-{L}{R["anuales"]}-{L}{R["dcol"]}-{L}{R["prima"]}-{L}{R["imp_pagado"]}-{L}{R["aviso"]}'), BLACK, NUM)
    put(ws, R['caja_min'], c, f'=p_mincash_m*{L}{R["fijos"]}', BLACK, NUM)
    put(ws, R['aporte'], c, f'=MAX(0,{L}{R["caja_min"]}-{L}{R["caja_pre"]})', BOLD, NUM)
    if m in (24, 36, 48):
        y = m // 12
        ycol = CL(2 + y)
        put(ws, R['dividendo'], c, (f'=p_payout*MAX(0,MIN({L}{R["caja_pre"]}+{L}{R["aporte"]}-2*{L}{R["caja_min"]}-Anual!${ycol}$14,'
                                     f'SUM(Anual!$C$15:${ycol}$15)-SUM($D${R["dividendo"]}:{Lp}${R["dividendo"]})))'), BOLD, NUM)
    else:
        put(ws, R['dividendo'], c, 0, BLACK, NUM)
    put(ws, R['caja'], c, f'={L}{R["caja_pre"]}+{L}{R["aporte"]}-{L}{R["dividendo"]}', BOLD, NUM)
    put(ws, R['flujo_inv'], c, f'=-{L}{R["aporte"]}+{L}{R["dividendo"]}*(1-p_divtax)', BLACK, NUM)
for c in range(3, 65):
    ws.column_dimensions[CL(c)].width = 10
ws.freeze_panes = 'C4'
for k in ('mes', 'ventas', 'costo', 'uai', 'aporte', 'caja'):
    for c in range(1, 65):
        ws.cell(row=R[k], column=c).fill = GREY
put(ws, R['flujo_inv'] + 2, 1, 'La columna del mes 61 solo sirve para mirar el costo del mes siguiente al fijar el inventario del mes 60.', NOTE)

# =============================================================== Anual
ws = wb.create_sheet('Anual')
setw(ws, {'A': 4, 'B': 52, 'C': 13, 'D': 13, 'E': 13, 'F': 13, 'G': 13, 'H': 13})
put(ws, 1, 2, 'Estado de resultados e impuestos (B/.)', TITLE)
hdr(ws, 3, range(2, 9), ['Concepto', 'Año 1', 'Año 2', 'Año 3', 'Año 4', 'Año 5', 'Total'])
lines = [
 (4, 'Ventas', 'ventas', 1),
 (5, 'Costo de ventas (incl. mermas)', None, -1),
 (6, 'Gastos variables, incobrables y factoring', None, -1),
 (7, 'Costos fijos y cargos anuales', None, -1),
 (8, 'Arranque y registros sanitarios', None, -1),
 (9, 'Fianzas, posregistro y pérdidas por cierre', None, -1),
 (10, 'Utilidad antes de impuestos', 'uai', 1),
]
def ysum(row_key, y):
    a = CL(3 + 12 * (y - 1) + 1); b = CL(3 + 12 * y)
    return f"SUM(Mensual!{a}{R[row_key]}:{b}{R[row_key]})"
for y in range(1, 6):
    c = 2 + y
    a = CL(3 + 12 * (y - 1) + 1); b = CL(3 + 12 * y)
    put(ws, 4, c, '=' + ysum('ventas', y), GREEN, NUM)
    put(ws, 5, c, f'=-{ysum("costo", y)}*(1+p_expiry)', GREEN, NUM)
    put(ws, 6, c, f'=-({ysum("var", y)}+{ysum("ventas", y)}*p_baddebt+{ysum("factoring", y)})', GREEN, NUM)
    put(ws, 7, c, f'=-({ysum("fijos", y)}+{ysum("anuales", y)})', GREEN, NUM)
    put(ws, 8, c, f'=-({ysum("setup", y)}+{ysum("registros", y)})', GREEN, NUM)
    put(ws, 9, c, f'=-({ysum("prima", y)}+{ysum("posreg", y)}+{ysum("perdida_cierre", y)})', GREEN, NUM)
    put(ws, 10, c, '=' + ysum('uai', y), GREEN, NUM)
    # loss pool: 20% of each prior loss within 5 years
    prior = '+'.join([f'0.2*MAX(0,-{CL(2 + k)}10)' for k in range(1, y)]) or '0'
    put(ws, 11, c, f'={prior}', BLACK, NUM)
    put(ws, 12, c, f'=MIN(0.5*MAX(0,{CL(c)}10),{CL(c)}11)', BLACK, NUM)
    put(ws, 13, c, f'=MAX(0,{CL(c)}10)-{CL(c)}12', BLACK, NUM)
    put(ws, 14, c, f'=MAX(p_isr*{CL(c)}13,IF({CL(c)}4>1500000,0.011675*{CL(c)}4,0))', BLACK, NUM)
    put(ws, 15, c, f'={CL(c)}10-{CL(c)}14', BOLD, NUM)
    put(ws, 16, c, f'=IF({CL(c)}4>0,{CL(c)}15/{CL(c)}4,0)', BLACK, PCT)
for y in range(1, 6):
    put(ws, 17, 2 + y, '=' + ysum('aviso', y), GREEN, NUM)
put(ws, 17, 2, 'Memo: impuesto de aviso de operación pagado (no se deduce de la renta en el modelo)', NOTE)
put(ws, 17, 8, '=SUM(C17:G17)', BOLD, NUM)
labs = {11: 'Pérdidas acumuladas deducibles este año (20% de cada pérdida previa)', 12: 'Deducción aplicada (tope 50% de la renta)',
        13: 'Renta gravable', 14: 'Impuesto sobre la renta (o CAIR si ventas > B/.1.5 millones)', 15: 'Utilidad neta', 16: 'Margen neto'}
for r_, lab in [(l[0], l[1]) for l in lines] + list(labs.items()):
    put(ws, r_, 2, lab, BOLD if r_ in (4, 10, 15) else BLACK)
for r_ in range(4, 16):
    if r_ in (11, 12):
        continue
    put(ws, r_, 8, f'=SUM(C{r_}:G{r_})', BOLD, NUM)
put(ws, 18, 2, 'Punto de equilibrio (ventas anuales que cubren fijos)', SUB)
put(ws, 19, 2, 'Costos fijos anuales a plena operación', BLACK); put(ws, 19, 3, '=f_total*12+c_annual+c_n_reg1*p_postreg', BLACK, NUM)
put(ws, 20, 2, 'Margen bruto promedio del portafolio', BLACK); put(ws, 20, 3, '=IF(s_rev_exp>0,s_gp_exp/s_rev_exp,0)', BLACK, PCT)
put(ws, 21, 2, 'Gastos variables (% ventas)', BLACK); put(ws, 21, 3, '=p_dist+p_penal+p_baddebt+p_expiry*(1-C20)', BLACK, PCT)
put(ws, 22, 2, 'Ventas de equilibrio (B/./año)', BOLD); put(ws, 22, 3, '=IF(C20-C21>0,C19/(C20-C21),0)', BOLD, NUM)
put(ws, 23, 2, 'Ventas esperadas de la primera ola en madurez (B/./año)', BLACK); put(ws, 23, 3, '=s_rev_exp', GREEN, NUM)

# =============================================================== Valoración
ws = wb.create_sheet('Valoración')
setw(ws, {'A': 4, 'B': 62, 'C': 16, 'D': 60})
put(ws, 1, 2, 'Valoración y capital requerido', TITLE)
put(ws, 2, 2, '=CONCATENATE("Escenario activo: ",Supuestos!C3,IF(p_sl=1," | tarifas SignatureLex"," | tarifas de mercado"))', BOLD)
last_col = CL(63)
rows_v = [
 (4, 'Capital aportado por los socios durante 60 meses', f'=SUM(Mensual!D{R["aporte"]}:{last_col}{R["aporte"]})', NUM),
 (5, 'Gasto de fase 0 (antes de constituir, lo pagan los socios)', '=c_phase0', NUM),
 (6, 'Dividendos pagados (antes del 10%)', f'=SUM(Mensual!D{R["dividendo"]}:{last_col}{R["dividendo"]})', NUM),
 (7, 'Caja al mes 60', f'=Mensual!{last_col}{R["caja"]}', NUM),
 (8, 'Cuentas por cobrar al mes 60', f'=SUMPRODUCT((m_mes>60-c_dso_m)*Mensual!$D${R["ventas"]}:$BK${R["ventas"]})*(1-p_baddebt)*(1-p_fact_share)+p_fact_share*Mensual!{last_col}{R["ventas"]}*(1-p_baddebt)*(1-p_fact_cost*c_dso_m)', NUM),
 (9, 'Inventario al mes 60', f'=Mensual!{last_col}{R["inv"]}', NUM),
 (10, 'Colateral de fianzas al mes 60', f'=Mensual!{last_col}{R["colateral"]}', NUM),
 (11, 'Cuentas por pagar al proveedor al mes 60', f'=SUMPRODUCT((m_mes>60-MAX(0,c_credit_m-c_ship_m))*Mensual!$D${R["llegadas"]}:$BK${R["llegadas"]})*(1-p_adv)', NUM),
 (12, 'Capital de trabajo neto al mes 60', '=C8+C9+C10-C11', NUM),
 (13, 'Impuesto sobre la renta y aviso de operación del año 5 por pagar', '=Anual!G14+IF(60<=ROUND(p_stop_det,0)+3,MAX(100,p_aviso*MAX(0,C4+SUM(Anual!C15:G15)-C6)),0)', NUM),
 (14, 'Valor terminal conservador (caja + recuperación del capital de trabajo)', '=C7+p_recov*C12-C13', NUM),
 (15, 'Valor terminal como negocio en marcha (caja + múltiplo de la utilidad del año 5)', '=C7-C13+p_gc_mult*MAX(0,Anual!G15)', NUM),
 (16, 'Valor terminal usado en el caso "en marcha" (el mayor)', '=MAX(C14,C15)', NUM),
 (17, 'Valor terminal neto del impuesto de dividendos (conservador)', '=C14-p_divtax*MAX(0,C14-C4)', NUM),
 (18, 'Valor terminal neto del impuesto de dividendos (en marcha)', '=C16-p_divtax*MAX(0,C16-C4)', NUM),
]
for r_, lab, f, fmt in rows_v:
    put(ws, r_, 2, lab, BLACK); put(ws, r_, 3, f, GREEN if 'Mensual' in f or 'Anual' in f else BLACK, fmt)
# investor flow rows (month 0..60)
put(ws, 21, 2, 'Flujo de los accionistas, conservador (mes 0 a 60, sigue a la derecha)', SUB)
put(ws, 22, 2, 'Flujo de los accionistas, en marcha', SUB)
for m in range(0, 61):
    c = 3 + m
    L = CL(c)
    src = f'Mensual!{CL(3 + m)}{R["flujo_inv"]}'
    put(ws, 20, c, m, BOLD, '0')
    put(ws, 21, c, f'={src}' + ('+$C$17' if m == 60 else ''), GREEN, NUM)
    put(ws, 22, c, f'={src}' + ('+$C$18' if m == 60 else ''), GREEN, NUM)
    ws.column_dimensions[L].width = 11 if c > 3 else 16
fl = f'$C$21:${CL(63)}$21'; fg = f'$C$22:${CL(63)}$22'
res_rows = [
 (24, 'VPN al 15% anual (conservador)', f'=SUMPRODUCT({fl},1/(1+0.15)^($C$20:${CL(63)}$20/12))', NUM),
 (25, 'VPN a la tasa de descuento del escenario (conservador)', f'=SUMPRODUCT({fl},1/(1+p_disc)^($C$20:${CL(63)}$20/12))', NUM),
 (26, 'VPN al 15% anual (en marcha)', f'=SUMPRODUCT({fg},1/(1+0.15)^($C$20:${CL(63)}$20/12))', NUM),
 (27, 'TIR anual (conservador)', f'=IFERROR((1+IRR({fl},0.01))^12-1,IFERROR((1+IRR({fl},-0.1))^12-1,IFERROR((1+IRR({fl},-0.19))^12-1,"n.d.")))', PCT),
 (28, 'TIR anual (en marcha)', f'=IFERROR((1+IRR({fg},0.01))^12-1,IFERROR((1+IRR({fg},-0.1))^12-1,IFERROR((1+IRR({fg},-0.19))^12-1,"n.d.")))', PCT),
 (29, 'Múltiplo del capital (lo que vuelve / lo que se pone), conservador', f'=IF(-SUMIF({fl},"<0")>0,SUMIF({fl},">0")/-SUMIF({fl},"<0"),0)', MULT),
 (30, 'Capital máximo acumulado (pico de necesidad de caja de los socios)', f'=-MIN(C34:{CL(63)}34)', NUM),
 (31, 'Ganancia de Zywie por su margen sobre el precio de fábrica (60 meses)', f'=SUM(Mensual!D{R["llegadas"]}:{CL(63)}{R["llegadas"]})*s_fob_share*p_zy_markup/(1+p_zy_markup)', NUM),
]
for r_, lab, f, fmt in res_rows:
    put(ws, r_, 2, lab, BOLD); c = put(ws, r_, 3, f, BLACK, fmt); c.fill = YEL
put(ws, 33, 2, 'Flujo acumulado (conservador, sin valor terminal)', BLACK)
put(ws, 34, 2, 'Flujo acumulado de los accionistas', BLACK)
for m in range(0, 61):
    c = 3 + m; L = CL(c)
    put(ws, 34, c, f'=SUM($C$21:{L}21)-IF({m}=60,$C$17,0)', BLACK, NUM)

put(ws, 36, 2, 'Vista de Jaime (participación y aportes según el trato)', SUB)
put(ws, 37, 2, 'Participación de Jaime en las utilidades', BLACK); put(ws, 37, 3, '=(1-p_patel_eq)*p_jaime_frac', BLACK, PCT)
put(ws, 38, 2, 'Porcentaje del capital que aporta Jaime', BLACK); put(ws, 38, 3, '=(1-p_patel_cash)*p_jaime_frac', BLACK, PCT)
put(ws, 39, 2, 'Capital total que pondría Jaime (incluye su tercio de la fase 0)', BOLD); put(ws, 39, 3, '=C4*C38+C5*p_jaime_frac', BOLD, NUM)
put(ws, 40, 2, 'Lo que recibiría Jaime (dividendos y valor terminal netos, conservador)', BOLD); put(ws, 40, 3, '=(C6*(1-p_divtax)+C17)*C37', BOLD, NUM)
put(ws, 41, 2, 'Resultado neto de Jaime en 5 años (sin descontar)', BOLD); c = put(ws, 41, 3, '=C40-C39', BOLD, NUM); c.fill = YEL
put(ws, 42, 2, 'Capital del socio como % del patrimonio líquido de referencia (B/.100,000)', BLACK); put(ws, 42, 3, '=C39/100000', BLACK, PCT)
put(ws, 44, 2, 'Reparto del valor económico entre Patel y el lado panameño (nominal, 60 meses, conservador)', SUB)
put(ws, 45, 2, 'Valor neto para todos los accionistas (lo que vuelve menos lo que se pone)', BLACK); put(ws, 45, 3, f'=SUM({fl})', BLACK, NUM)
put(ws, 46, 2, 'Patel: margen de Zywie + su parte de lo distribuido - su parte del capital', BLACK)
put(ws, 46, 3, f'=C31+p_patel_eq*SUMIF(Valoración!$D$21:${CL(63)}$21,">0")-p_patel_cash*C4', BLACK, NUM)
put(ws, 47, 2, 'Lado panameño (3 socios): su parte de lo distribuido - su parte del capital - fase 0', BLACK)
put(ws, 47, 3, f'=(1-p_patel_eq)*SUMIF(Valoración!$D$21:${CL(63)}$21,">0")-(1-p_patel_cash)*C4-C5', BLACK, NUM)
put(ws, 48, 2, 'Porcentaje del valor total que se lleva Patel', BOLD); put(ws, 48, 3, '=IF(C46+C47<>0,C46/(C46+C47),0)', BOLD, PCT)
put(ws, 49, 2, 'Nota: si el valor neto total es negativo, el porcentaje no tiene interpretación útil; mire los montos.', NOTE)

# =============================================================== Escenarios (static)
ws = wb.create_sheet('Escenarios')
setw(ws, {'A': 4, 'B': 52, 'C': 14, 'D': 14, 'E': 14})
put(ws, 1, 2, 'Resultados por escenario (valores fijos del motor en Python)', TITLE)
put(ws, 2, 2, 'Para recalcular en vivo, cambie Supuestos!B3. Estos valores sirven de referencia y de control cruzado.', NOTE)
hdr(ws, 4, range(2, 6), ['Indicador', 'Pesimista', 'Base', 'Optimista'])
ind = [('Ventas año 1', lambda d: d['revY'][0], NUM), ('Ventas año 2', lambda d: d['revY'][1], NUM), ('Ventas año 3', lambda d: d['revY'][2], NUM),
       ('Ventas año 5', lambda d: d['revY'][4], NUM), ('Utilidad neta año 1', lambda d: d['NI'][0], NUM), ('Utilidad neta año 3', lambda d: d['NI'][2], NUM),
       ('Utilidad neta año 5', lambda d: d['NI'][4], NUM), ('Capital aportado (60 meses)', lambda d: d['eq_in'], NUM),
       ('Pico de necesidad de caja de los socios', lambda d: d['peak_cum_neg'], NUM), ('VPN al 15% (conservador)', lambda d: d['npv15'], NUM),
       ('VPN al 30% (conservador)', lambda d: d['npv30'], NUM), ('VPN al 15% (en marcha)', lambda d: d['npv15_gc'], NUM),
       ('TIR (conservador)', lambda d: d['irr'], PCT), ('TIR (en marcha)', lambda d: d['irr_gc'], PCT),
       ('Múltiplo del capital (conservador)', lambda d: d['moic'], MULT), ('Dividendos pagados', lambda d: d['divs'], NUM),
       ('Ganancia de Zywie por su margen', lambda d: d['zywie'], NUM)]
for i, (lab, fn, fmt) in enumerate(ind):
    r_ = 5 + i
    put(ws, r_, 2, lab, BLACK)
    for j, sc in enumerate(('det_pes', 'det_base', 'det_opt')):
        put(ws, r_, 3 + j, fn(A[sc]), BLACK, fmt)
r_ = 5 + len(ind) + 2
put(ws, r_, 2, 'Qué pasa si... (cambio de un supuesto sobre la base)', SUB); r_ += 1
hdr(ws, r_, range(2, 8), ['Cambio', 'Capital aportado', 'VPN 15%', 'TIR', 'Múltiplo', 'Ventas año 3'])
for w in A['whatif']:
    r_ += 1
    put(ws, r_, 2, w['tag'], BLACK)
    for j, (k, fmt) in enumerate((('eq', NUM), ('npv15', NUM), ('irr', PCT), ('moic', MULT), ('rev3', NUM))):
        put(ws, r_, 3 + j, w[k], BLACK, fmt)
setw(ws, {'F': 12, 'G': 14})

# =============================================================== Monte Carlo (static)
ws = wb.create_sheet('Monte Carlo')
setw(ws, {'A': 4, 'B': 46, 'C': 15, 'D': 15, 'E': 15, 'F': 15, 'G': 15, 'H': 15, 'I': 15})
put(ws, 1, 2, 'Simulación de Monte Carlo (20,000 escenarios por estrategia)', TITLE)
put(ws, 2, 2, 'Cada escenario sortea todos los supuestos (distribución triangular pesimista-base-optimista), los registros aprobados, cada renglón centralizado ganado o perdido, fallas del socio o de la planta y las compuertas de decisión.', NOTE)
order = [('A_comprometido', 'S.A. propia como la propone Patel, sin compuertas'),
         ('A_por_etapas', 'S.A. propia, con fase 0 y compuerta operativa'),
         ('A_por_etapas_reestructurado', '+ crédito del proveedor y precio a libro abierto'),
         ('A_por_etapas_reestructurado_SNC', '+ 6 productos SNC con fabricante verificado'),
         ('A_bueno_financia_SNC', '+ Bueno paga registros y da 180 días de crédito'),
         ('bueno_coord0', '+ sin coordinador pagado (un socio opera)'),
         ('C', 'Registros propios y venta por un distribuidor establecido')]
hdr(ws, 4, range(2, 10), ['Estrategia', 'VPN 15% promedio', 'Prob. de perder dinero', 'Prob. de perder más que la fase 0', 'Múltiplo mediano', 'Múltiplo p90', 'Capital pico mediano*', 'Capital pico p90*'])
for i, (k, lab) in enumerate(order):
    d = S3[k]; r_ = 5 + i
    put(ws, r_, 2, lab, BLACK, wrap=True)
    put(ws, r_, 3, d['npv15'], BLACK, NUM); put(ws, r_, 4, d['p_loss'], BLACK, PCT); put(ws, r_, 5, d['p_loss_b'], BLACK, PCT)
    put(ws, r_, 6, d['moic_pcts'][2], BLACK, MULT); put(ws, r_, 7, d['moic_pcts'][4], BLACK, MULT)
    put(ws, r_, 8, d['peak_med_go'], BLACK, NUM); put(ws, r_, 9, d['peak_p90_go'], BLACK, NUM)
put(ws, 5 + len(order), 2, '* Máximo acumulado que aportan los socios, en los escenarios que pasan la fase 0. La probabilidad de perder y el múltiplo incluyen los casos que se detienen en la fase 0 (pierden solo esa fase).', NOTE)
ws.merge_cells(start_row=5 + len(order), start_column=2, end_row=5 + len(order), end_column=9)
r_ = 5 + len(order) + 1
put(ws, r_, 2, 'Percentiles del VPN al 15% (B/.)', SUB); r_ += 1
hdr(ws, r_, range(2, 10), ['Estrategia', 'p5', 'p10', 'p25', 'p50', 'p75', 'p90', 'p95'])
for k, lab in order:
    r_ += 1; d = S3[k]
    put(ws, r_, 2, lab, BLACK, wrap=True)
    for j in range(7):
        put(ws, r_, 3 + j, d['npv_pcts'][j], BLACK, NUM)
r_ += 2
put(ws, r_, 2, 'Lo que arriesga Jaime (1/3 de la fase 0; 1/6 del capital posterior y de las utilidades en la S.A.; 1/3 en la opción de registros)', SUB); r_ += 1
hdr(ws, r_, range(2, 10), ['Estrategia', 'Capital promedio (todos los escenarios)', 'Capital promedio si el trato sigue', 'Capital p90 si sigue', 'Resultado neto promedio', 'Prob. de que pierda', 'Prob. de perder más que la fase 0', 'Kelly vs depósito 4%'])
jorder = order[:6] + [('A_bueno_financia_SNC_70_30', '+ Patel aporta 70% del efectivo (sigue 50/50 en acciones)'), ('A_bueno_financia_SNC_80_20', '+ Patel aporta 80% del efectivo (sigue 50/50 en acciones)')] + order[6:]
for k, lab in jorder:
    r_ += 1; d = S3[k]
    put(ws, r_, 2, lab, BLACK, wrap=True)
    put(ws, r_, 3, d['j_in_mean'], BLACK, NUM); put(ws, r_, 4, d['j_in_mean_go'], BLACK, NUM); put(ws, r_, 5, d['j_in_p90_go'], BLACK, NUM)
    put(ws, r_, 6, d['j_net_mean'], BLACK, NUM); put(ws, r_, 7, d['j_ploss'], BLACK, PCT); put(ws, r_, 8, d['j_ploss_b'], BLACK, PCT)
    put(ws, r_, 9, d['k4']['amount'], BLACK, NUM)
put(ws, r_ + 1, 2, 'Capital de la opción de registros = un tercio del máximo acumulado (no hay caja común). Kelly: monto esperado que maximiza el crecimiento del patrimonio de B/.100,000; cuando el óptimo cae en el límite de no quebrar en el peor escenario, el monto es ese límite.', NOTE)
ws.merge_cells(start_row=r_ + 1, start_column=2, end_row=r_ + 1, end_column=9)
r_ += 3
put(ws, r_, 2, 'Supuestos de riesgo de la simulación', SUB); r_ += 1
B = S3['A_bueno_financia_SNC']; B11 = S3['bueno_cap11']; ET = S3['A_por_etapas']; SN = S3['A_por_etapas_reestructurado_SNC']
for t in ['Planta con problemas de BPM: 15% de probabilidad; si la fase 0 no lo detecta (detecta 80%), provoca una falla de calidad entre los meses 12 y 36, se ejecuta la fianza y se pierde el inventario.',
          'Ruptura con el proveedor por otras causas: 4% anual desde el mes 6, con ejecución de fianzas.',
          'Fase 0: se descarta el trato si se detecta el problema de planta o si el índice de precio del proveedor supera 1.6.',
          f"Compuerta operativa: 9 meses después de la primera venta, si las ventas anualizadas (más contratos centralizados adjudicados) no llegan a B/.90,000, se cierra y no se hace la segunda ola. Con la rampa base de 12 meses equivale a unos B/.108,000 en madurez, algo más que el equilibrio de B/.{A['breakeven']['be_revenue']:,.0f}.",
          f"Cierres por compuerta: por etapas, {ET['p_nogo']:.0%} en la fase 0 y {ET['p_gate']:.0%} en la operativa; en las versiones con los productos del sistema nervioso, {SN['p_nogo']:.0%} y {SN['p_gate']*100:.1f}%.",
          f"Con el tope de precio de 1.1 veces de la compuerta 0 del plan (en vez de 1.6) en la versión con Bueno financiando, cuyo precio a libro abierto va de 0.95 a 1.30 veces la referencia, {B11['p_nogo']:.0%} de los escenarios se detiene en la fase 0, la probabilidad de perder más que la fase 0 queda en {B11['p_loss_b']:.0%} y el VPN esperado en B/.{B11['npv15']:,.0f}.",
          'Correlaciones: participación descentralizada y probabilidad de ganar centralizado (0.6); mercado débil y mayor caída de precios (0.4).']:
    put(ws, r_, 2, t, BLACK, wrap=True); ws.merge_cells(start_row=r_, start_column=2, end_row=r_, end_column=9); ws.row_dimensions[r_].height = 30; r_ += 1

# =============================================================== Sensibilidad (static tornado)
ws = wb.create_sheet('Sensibilidad')
setw(ws, {'A': 4, 'B': 66, 'C': 14, 'D': 14, 'E': 14, 'F': 14, 'G': 14})
put(ws, 1, 2, 'Sensibilidad del VPN al 15% (un supuesto a la vez, el resto en la base)', TITLE)
put(ws, 2, 2, f"VPN base: B/.{A['tornado']['base_npv15']:,.0f}. Capital base: B/.{A['tornado']['base_eq']:,.0f}.", NOTE)
hdr(ws, 4, range(2, 8), ['Supuesto', 'Valor pesimista', 'Valor optimista', 'VPN pesimista', 'VPN optimista', 'Rango'])
for i, t in enumerate(A['tornado']['rows']):
    r_ = 5 + i
    put(ws, r_, 2, t['label'], BLACK, wrap=True)
    put(ws, r_, 3, t['pes_val'], BLACK); put(ws, r_, 4, t['opt_val'], BLACK)
    put(ws, r_, 5, t['npv_pes'], BLACK, NUM); put(ws, r_, 6, t['npv_opt'], BLACK, NUM); put(ws, r_, 7, f'=F{r_}-E{r_}', BLACK, NUM)

# =============================================================== Trato (static alternatives)
ws = wb.create_sheet('Trato')
setw(ws, {'A': 4, 'B': 58, 'C': 16, 'D': 16, 'E': 16, 'F': 16})
put(ws, 1, 2, 'Estructuras de trato comparadas', TITLE)
put(ws, 2, 2, 'Efecto del margen de Zywie sobre el reparto del valor (caso base, mismo método que Valoración!C44:C48: lo distribuido menos el capital aportado).', NOTE)
hdr(ws, 4, range(2, 7), ['Margen de Zywie sobre fábrica', 'Ganancia de Zywie (60 m)', 'Valor para Patel', 'Valor para el lado panameño', 'Parte de Patel en el total'])
for i, sp in enumerate(A['value_split']):
    r_ = 5 + i
    put(ws, r_, 2, sp['mk'], BLUE, PCT); put(ws, r_, 3, sp['zywie'], BLACK, NUM); put(ws, r_, 4, sp['patel'], BLACK, NUM)
    put(ws, r_, 5, sp['panama'], BLACK, NUM); put(ws, r_, 6, sp['share'], BLACK, PCT)
put(ws, 12, 2, 'Lectura: con 50/50 en acciones y capital y sin margen de Zywie, Patel recibe la mitad. Cada punto de margen de Zywie traslada valor del lado panameño al indio, aunque el capital se divida 50/50.', NOTE)
put(ws, 14, 2, 'Opción de registros propios y distribuidor establecido (participación del distribuidor en la utilidad bruta)', SUB)
hdr(ws, 15, range(2, 7), ['Escenario y regalía', 'Capital pico', 'VPN 15%', 'TIR', 'Múltiplo'])
rr = 16
for k, v in OC.items():
    sc, rho = k.split('_')
    put(ws, rr, 2, f"{ {'pes':'Pesimista','base':'Base','opt':'Optimista'}[sc] }, regalía {float(rho):.0%} de la utilidad bruta", BLACK)
    put(ws, rr, 3, v['peak'], BLACK, NUM); put(ws, rr, 4, v['npv15'], BLACK, NUM)
    put(ws, rr, 5, v['irr'] if v['irr'] == v['irr'] else 'n.d.', BLACK, PCT); put(ws, rr, 6, v['moic'], BLACK, MULT)
    rr += 1

# =============================================================== Capital personal (static Kelly)
ws = wb.create_sheet('Capital personal')
setw(ws, {'A': 4, 'B': 60, 'C': 16, 'D': 16, 'E': 16, 'F': 18})
put(ws, 1, 2, 'Cuánto capital personal tiene sentido arriesgar', TITLE)
put(ws, 2, 2, 'Criterio de Kelly sobre la distribución simulada (20,000 escenarios) con un patrimonio líquido de referencia de B/.100,000: monto esperado que maximiza el crecimiento del patrimonio. Si el trato se detiene en la fase 0, Jaime solo pierde su parte de esa fase.', NOTE)
hdr(ws, 4, range(2, 7), ['Estrategia', 'Capital promedio de Jaime si el trato sigue', 'Resultado neto promedio', 'Kelly vs depósito al 4%/año', 'Kelly vs alternativa al 15%/año'])
def kfmt(k): return k['amount']
krows = [('S.A. como la propone Patel', 'A_comprometido'), ('S.A. por etapas, reestructurada + SNC', 'A_por_etapas_reestructurado_SNC'),
         ('S.A. con Bueno financiando registros y crédito', 'A_bueno_financia_SNC'), ('Lo anterior, sin coordinador pagado', 'bueno_coord0'),
         ('Bueno financiando, con tasa de victoria de 17% y precio de 1.25 veces', 'bueno_pwin17_sup125'),
         ('Bueno financiando, con tope de precio de 1.1 veces en la fase 0', 'bueno_cap11'),
         ('Bueno financiando, Patel aporta 70% del efectivo (50/50 en acciones)', 'A_bueno_financia_SNC_70_30'),
         ('Registros propios + distribuidor (Jaime con 1/3)', 'C')]
for i, (lab, k) in enumerate(krows):
    r_ = 5 + i; d = S3[k]
    put(ws, r_, 2, lab, BLACK)
    put(ws, r_, 3, d['j_in_mean_go'], BLACK, NUM); put(ws, r_, 4, d['j_net_mean'], BLACK, NUM)
    put(ws, r_, 5, d['k4']['amount'], BLACK, NUM); put(ws, r_, 6, d['k15']['amount'], BLACK, NUM)
put(ws, 13, 2, 'Kelly va de todo a nada según los supuestos. Con Bueno financiando y capital 50/50 cae en el límite de no quebrar en el peor escenario simulado; con el tope de precio de 1.1 veces, o frente a 15% si Patel aporta 70% del efectivo, es un óptimo interior. El tope de 15% de los ahorros es una decisión de prudencia, no un resultado del modelo.', NOTE)
put(ws, 16, 2, 'Calculadora en vivo', SUB)
put(ws, 17, 2, 'Patrimonio líquido de referencia del socio (B/.)', BLACK); put(ws, 17, 3, 100000, BLUE, NUM, fill=YEL)
put(ws, 18, 2, 'Reserva para la otra oportunidad de negocio (B/.)', BLACK); put(ws, 18, 3, 25000, BLUE, NUM, fill=YEL)
put(ws, 19, 2, 'Tope recomendado para esta inversión (% de ahorros)', BLACK); put(ws, 19, 3, 0.15, BLUE, PCT, fill=YEL)
put(ws, 20, 2, 'Tope en balboas', BOLD); put(ws, 20, 3, '=MIN(C17*C19,C17-C18)', BOLD, NUM)
put(ws, 21, 2, 'Capital que le pediría el escenario activo (Valoración!C39)', BLACK); put(ws, 21, 3, "='Valoración'!C39", GREEN, NUM)
put(ws, 22, 2, '¿Cabe dentro del tope?', BOLD); put(ws, 22, 3, '=IF(C21<=C20,"Sí","No: hay que cambiar el trato o no entrar")', BOLD)

# =============================================================== Operación (IE)
ws = wb.create_sheet('Operación')
setw(ws, {'A': 4, 'B': 44, 'C': 14, 'D': 14, 'E': 14, 'F': 14, 'G': 14})
put(ws, 1, 2, 'Operación: volumen físico, embarques y vida útil', TITLE)
hdr(ws, 3, range(2, 8), ['Producto (primera ola, madurez base)', 'Unidades/año', 'Ventas/año', 'm³/año', 'Costo/año', 'B/. por m³'])
for i, rw in enumerate(IEK['ie']):
    r_ = 4 + i
    put(ws, r_, 2, rw['id'], BLACK); put(ws, r_, 3, rw['units'], BLACK, NUM); put(ws, r_, 4, rw['rev'], BLACK, NUM)
    put(ws, r_, 5, rw['cbm'], BLACK, '0.0'); put(ws, r_, 6, rw['cogs'], BLACK, NUM); put(ws, r_, 7, rw['val_density'], BLACK, NUM)
r_ = 4 + len(IEK['ie'])
put(ws, r_, 2, 'Total', BOLD); put(ws, r_, 5, f'=SUM(E4:E{r_-1})', BOLD, '0.0'); put(ws, r_, 6, f'=SUM(F4:F{r_-1})', BOLD, NUM)
tot_r = r_
r_ += 2
put(ws, r_, 2, 'Lote económico de embarque (EOQ)', SUB); r_ += 1
put(ws, r_, 2, 'Costo fijo por embarque (corredor, terminal, acarreo, documentos)', BLACK); put(ws, r_, 3, 1000, BLUE, NUM); s_r = r_; r_ += 1
put(ws, r_, 2, 'Costo de capital anual', BLACK); put(ws, r_, 3, 0.15, BLUE, PCT); k_r = r_; r_ += 1
put(ws, r_, 2, 'Almacenaje 3PL por m³ al mes', BLACK); put(ws, r_, 3, 16, BLUE, NUM); st_r = r_; r_ += 1
put(ws, r_, 2, 'Riesgo de merma anual sobre el valor', BLACK); put(ws, r_, 3, 0.03, BLUE, PCT); x_r = r_; r_ += 1
put(ws, r_, 2, 'Valor por m³ del portafolio', BLACK); put(ws, r_, 3, f'=F{tot_r}/E{tot_r}', BLACK, NUM); v_r = r_; r_ += 1
put(ws, r_, 2, 'Costo de mantener 1 m³ un año', BLACK); put(ws, r_, 3, f'=C{k_r}*C{v_r}+12*C{st_r}+C{x_r}*C{v_r}', BLACK, NUM); h_r = r_; r_ += 1
put(ws, r_, 2, 'Lote económico (m³ por embarque)', BOLD); put(ws, r_, 3, f'=SQRT(2*E{tot_r}*C{s_r}/C{h_r})', BOLD, '0.0'); q_r = r_; r_ += 1
put(ws, r_, 2, 'Embarques por año', BOLD); put(ws, r_, 3, f'=E{tot_r}/C{q_r}', BOLD, '0.0'); r_ += 2
put(ws, r_, 2, 'Presupuesto de vida útil (regla de 18 meses al entregar)', SUB); r_ += 1
put(ws, r_, 2, 'Vida útil aprobada del producto (meses)', BLACK); put(ws, r_, 3, 24, BLUE, '0', fill=YEL); sl_r = r_; r_ += 1
put(ws, r_, 2, 'Vida útil mínima exigida al entregar (pliegos)', BLACK); put(ws, r_, 3, 18, BLUE, '0'); mn_r = r_; r_ += 1
put(ws, r_, 2, 'Liberación en fábrica y despacho (meses)', BLACK); put(ws, r_, 3, 1, BLUE, '0.0'); a_r = r_; r_ += 1
put(ws, r_, 2, 'Tránsito y aduana (meses)', BLACK); put(ws, r_, 3, '=p_ship_m', GREEN, '0.0'); b_r = r_; r_ += 1
put(ws, r_, 2, 'Pedido a entrega en hospital (meses)', BLACK); put(ws, r_, 3, 0.25, BLUE, '0.00'); c_r = r_; r_ += 1
put(ws, r_, 2, 'Tiempo máximo que puede pasar en bodega (meses)', BOLD); cc = put(ws, r_, 3, f'=C{sl_r}-C{mn_r}-C{a_r}-C{b_r}-C{c_r}', BOLD, '0.00'); cc.fill = YEL; r_ += 2
put(ws, r_, 2, 'Con 24 meses de vida útil solo caben 2.75 meses en bodega: reposición mensual y poco inventario. Con 36 meses caben casi 15 meses: embarques trimestrales en contenedor.', NOTE)

# =============================================================== Fuentes
ws = wb.create_sheet('Fuentes')
setw(ws, {'A': 4, 'B': 70, 'C': 100})
put(ws, 1, 2, 'Fuentes principales', TITLE)
src = [
 ('PanamaCompra: LPU 01-2026 CSS (348 renglones, ofertas y adjudicación)', 'https://apisv3.panamacompra.gob.pa/documentos-actos-publico/cuadroPropuesta/12/procesoVistaCuadroPropuesta/712894'),
 ('PanamaCompra: LPU 11-2026 CSS', 'https://apisv3.panamacompra.gob.pa/documentos-actos-publico/cuadroPropuesta/12/procesoVistaCuadroPropuesta/712187'),
 ('Pliego LPU 01-2026 (pago a 90 días, 18 meses de vida útil, fianza de cumplimiento 30%)', 'https://apisv3.panamacompra.gob.pa/procesos-contratacion-archivos/v2/download-file-2325E044-04B2-F011-80EA-0017A477FC74-ZA-101-1AZ-8120731-ZA-101-1AZ-8120731'),
 ('Pliego subasta en reversa MINSA 2026 (fianza 20%)', 'https://apisv3.panamacompra.gob.pa/procesos-contratacion-archivos/v2/download-file-41E2472E-8233-F111-80EA-0017A477FC64-ZA-101-1AZ-9715601-ZA-101-1AZ-9715601'),
 ('Compra conjunta 2024, pliego (fianza 15%, 70% de compra garantizada)', 'https://www.panamacompra.gob.pa/includes/veranexo.aspx?idattach=Pjc6Ojg4Njo='),
 ('ANTAI: reportes mensuales de contrataciones (CSS, MINSA, patronatos)', 'https://monitoreo.antai.gob.pa/'),
 ('Decreto Ejecutivo 27 de 2024 (tasas, licencias, registros, compras)', 'https://www.minsa.gob.pa/sites/default/files/general/decreto_ejecutivo_27_de_10_de_mayo_de_2024.pdf'),
 ('Ley 419 de 2024', 'https://dnfd.minsa.gob.pa/sites/default/files/2025-08/Ley%20419%20de%201%20de%20febrero%20de%202024.pdf'),
 ('Resolución 985 de 2025 (173 principios activos con equivalencia terapéutica)', 'https://www.minsa.gob.pa/sites/default/files/general/resolucion_985_go30317_08072025.pdf'),
 ('Resolución 181 de 2025 (BPA)', 'https://dnfd.minsa.gob.pa/sites/default/files/2026-02/Resolucion%20181%20de%2014%20de%20agosto%20de%202025%20procedimiento%20de%20BPA.pdf'),
 ('DGI: Informe 930 de precios de transferencia (art. 762-I del Código Fiscal)', 'https://dgi.mef.gob.pa/Internacional/I930.php'),
 ('Presupuesto CSS 2027 de medicamentos', 'https://www.prensa.com/sociedad/presupuesto-2027-de-la-css-contempla-925-millones-menos-para-medicamentos/'),
 ('Panamá América: gestiones de cobro en la Contraloría de 188.5 a 5.4 días', 'https://www.panamaamerica.com.pa/sociedad/gestiones-de-cobro-en-la-contraloria-pasan-de-1885-dias-en-la-administracion-cortizo-54'),
 ('Panamá América: la CSS reconoce pagos pendientes a proveedores (marzo de 2026)', 'https://www.panamaamerica.com.pa/sociedad/la-css-es-un-reflejo-de-la-economia-nacional-asegura-dino-mon-1259540/amp'),
 ('Ley 8 de 2010, art. 69 (Código Fiscal art. 1004): impuesto de aviso de operación, 2% del capital', 'https://docs.panama.justia.com/federales/leyes/8-de-2010-mar-15-2010.pdf'),
 ('PwC Tax Summaries Panamá: base del aviso de operación (patrimonio)', 'https://taxsummaries.pwc.com/panama/corporate/other-taxes'),
 ('CDSCO: alertas de calidad marzo 2024 (Bueno Salud Care)', 'https://cdsco.gov.in/opencms/resources/UploadCDSCOWeb/2018/UploadAlertsFiles/List%20of%20Drug%20Alert%20-March-2024.pdf'),
 ('Precios de referencia India: TNMSC e-018/2024', 'https://tnmsc.tn.gov.in/linkfiles/news_events/N2502472.pdf'),
 ('Fletes CMA CGM subcontinente indio a Manzanillo (2026)', 'https://www.ajot.com/news/cma-cgm-fak-rates-from-the-indian-subcontinent-to-latin-america-and-north-europe-the-mediterranean-north-africa'),
 ('DNFD: lista de establecimientos con licencia (sep-2026)', 'https://dnfd.minsa.gob.pa/'),
 ('Banco General: tarifas de garantías (fianzas) 2026', 'https://www.bgeneral.com/'),
]
hdr(ws, 3, range(2, 4), ['Fuente', 'Enlace'])
for i, (lab, url) in enumerate(src):
    put(ws, 4 + i, 2, lab, BLACK, wrap=True); put(ws, 4 + i, 3, url, BLACK)

wb.save(OUT)
print('saved', OUT, 'names', len(names), 'Mensual rows', R)
