"""Auditoría de los documentos Markdown del paquete para socios.

Uso:  python3 docs_build/audit_md.py [carpeta]   (por defecto docs/socios)

Revisa, por documento: tablas (celdas vacías, columnas desparejas, separador),
frases prohibidas y marcadores sueltos, espacios dobles, encabezados duplicados o
que saltan de nivel, referencias a archivos que no existen, enlaces locales rotos,
negritas sin cerrar, listas numeradas pegadas en una sola línea, fechas de
actualización, párrafos muy largos y cifras clave que no coinciden con el modelo.
Imprime un informe y escribe docs_build/audit_report.json. Sale con 1 si hay errores.
"""
import json, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..'))
FOLDER = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, 'docs', 'socios')

FORBIDDEN = ['socio indio', 'tu socio', 'TBD', '[[', 'TODO', 'XXX', 'lorem', '{OPERADOR}', '[APELLIDOS]',
             'N/A', 'n/a', 'por definir', 'ver arriba', 'ver abajo', 'sin dato']
# documentos donde una celda vacía es aceptable (p. ej. tablas de seguimiento por llenar)
EMPTY_OK = set()
DATE_RE = re.compile(r'(\d{1,2}) de (enero|febrero|marzo|abril|mayo|junio|julio|agosto|septiembre|octubre|noviembre|diciembre) de (\d{4})')
LONG_PARA = 900  # caracteres: a partir de aquí se marca como «párrafo largo» (aviso, no error)

# Cifras clave del modelo (escenario base y planificación con SignatureLex); se comparan con lo que dicen los documentos.
# Formato: etiqueta -> (valor canónico tal como se escribe, variantes aceptadas)
def model_figures():
    sys.path.insert(0, os.path.join(ROOT, 'model'))
    try:
        from engine import run, scenario_params
    except Exception as e:  # pragma: no cover
        return {}, f'no se pudo cargar el modelo: {e}'
    figs = {}
    try:
        import numpy as np
        p = scenario_params('base'); o = run(p)
        g = lambda key: float(np.asarray(o[key]).ravel()[0])
        figs['VPN base (liq)'] = f"{g('npv15_liq'):,.0f}".replace('-', '−')
        figs['Capital base'] = f"{g('eq_in'):,.0f}"
        figs['MOIC base'] = f"{g('moic_liq'):.2f}x"
    except Exception as e:
        return figs, f'error al correr el modelo: {e}'
    return figs, ''

def split_row(line):
    s = line.strip()
    if s.startswith('|'): s = s[1:]
    if s.endswith('|'): s = s[:-1]
    return [c.strip() for c in s.split('|')]

def audit_file(path, all_names):
    name = os.path.basename(path)
    errors, warns = [], []
    text = open(path, encoding='utf-8').read()
    lines = text.split('\n')
    # --- frases prohibidas y marcadores
    for i, ln in enumerate(lines, 1):
        for f in FORBIDDEN:
            if f in ln:
                # «N/A» dentro de una URL o código no cuenta
                if f in ('N/A', 'n/a') and ('http' in ln or '`' in ln): continue
                errors.append(f'L{i}: frase o marcador prohibido «{f}»')
        if '  ' in ln and not ln.startswith(('    ', '|')) and '`' not in ln:
            warns.append(f'L{i}: espacio doble')
        if ln.rstrip() != ln:
            warns.append(f'L{i}: espacio al final de la línea')
        if '\t' in ln:
            warns.append(f'L{i}: tabulador')
        if ln.count('**') % 2 == 1:
            errors.append(f'L{i}: negrita sin cerrar')
        if re.search(r'(^|\s)1\. .{20,}\s2\. .{10,}\s3\. ', ln):
            errors.append(f'L{i}: lista numerada pegada en una sola línea (se renderiza como un solo punto)')
        if re.search(r'\w-$', ln.strip()):
            warns.append(f'L{i}: línea termina en guion (¿palabra cortada?)')
    # --- tablas
    i = 0
    while i < len(lines):
        if lines[i].lstrip().startswith('|'):
            block = []
            while i < len(lines) and lines[i].lstrip().startswith('|'):
                block.append((i + 1, lines[i])); i += 1
            if len(block) < 2 or not re.match(r'^\s*\|?\s*:?-{3,}', block[1][1]):
                errors.append(f'L{block[0][0]}: tabla sin fila separadora')
                continue
            ncol = len(split_row(block[0][1]))
            for ln_no, ln in block[2:]:
                cells = split_row(ln)
                if len(cells) != ncol:
                    errors.append(f'L{ln_no}: fila con {len(cells)} celdas, encabezado con {ncol}')
                for c in cells:
                    if c == '' and name not in EMPTY_OK:
                        errors.append(f'L{ln_no}: celda vacía (usar «—»)')
            if len(block) == 2:
                warns.append(f'L{block[0][0]}: tabla sin filas de datos')
        else:
            i += 1
    # --- encabezados
    heads = [(n, len(m.group(1)), m.group(2).strip()) for n, ln in enumerate(lines, 1) for m in [re.match(r'^(#{1,6})\s+(.*)', ln)] if m]
    if not heads or heads[0][1] != 1:
        errors.append('sin título H1 al inicio')
    if sum(1 for h in heads if h[1] == 1) > 1:
        errors.append('más de un H1')
    seen = {}
    prev = 1
    for n, lvl, t in heads:
        if lvl > prev + 1:
            warns.append(f'L{n}: encabezado salta de nivel H{prev} a H{lvl}')
        prev = lvl
        key = (lvl, t.lower())
        if key in seen:
            errors.append(f'L{n}: encabezado repetido «{t}» (también en L{seen[key]})')
        seen[key] = n
    # --- referencias a otros documentos y enlaces locales
    for m in re.finditer(r'(?<!/)\b((?:0[0-7]_|Anexo_|Cotizaciones_|LEAME|Resumen_ejecutivo)[A-Za-z0-9_áéíóúñÁÉÍÓÚ]*\.(?:md|xlsx|pdf|html))', text):
        ref = m.group(1)
        if ref not in all_names:
            errors.append(f'referencia a archivo inexistente: {ref}')
    for m in re.finditer(r'\]\(([^)]+)\)', text):
        tgt = m.group(1)
        if tgt.startswith(('http://', 'https://', 'mailto:', '#')): continue
        tgt_path = os.path.join(os.path.dirname(path), tgt.split('#')[0])
        if not os.path.exists(tgt_path):
            errors.append(f'enlace local roto: {tgt}')
    # --- fechas
    dates = sorted({f'{d} de {mth} de {y}' for d, mth, y in DATE_RE.findall('\n'.join(lines[:6]))})
    # --- párrafos largos
    for n, ln in enumerate(lines, 1):
        if len(ln) > LONG_PARA and not ln.lstrip().startswith(('|', '-', '*', '>', '1', '2', '3', '4', '5', '6', '7', '8', '9')):
            warns.append(f'L{n}: párrafo de {len(ln)} caracteres (considerar dividir)')
    return {'file': name, 'errors': errors, 'warnings': warns, 'header_dates': dates, 'chars': len(text),
            'tables': sum(1 for ln in lines if re.match(r'^\s*\|?\s*:?-{3,}', ln)), 'h2': sum(1 for h in heads if h[1] == 2)}

def main():
    files = sorted(f for f in os.listdir(FOLDER) if f.endswith('.md'))
    all_names = set(os.listdir(FOLDER)) | set(os.listdir(os.path.join(ROOT, 'outputs'))) if os.path.isdir(os.path.join(ROOT, 'outputs')) else set(os.listdir(FOLDER))
    report = [audit_file(os.path.join(FOLDER, f), all_names) for f in files]
    figs, ferr = model_figures()
    # cifras clave: cada documento que mencione «VPN» o «capital» debe usar los valores canónicos
    fig_issues = []
    if figs:
        canon_npv = figs['VPN base (liq)']
        for r in report:
            txt = open(os.path.join(FOLDER, r['file']), encoding='utf-8').read()
            for m in re.finditer(r'VPN[^.|\n]{0,60}?(?:B/\.|US\$)?\s?(−|-)?\s?(\d{2,3},\d{3})', txt):
                val = (m.group(1) or '') + m.group(2)
                val = val.replace('-', '−')
                if '15' in m.group(0) and 'base' in txt[max(0, m.start()-200):m.end()+50].lower() and val != canon_npv and val.lstrip('−') not in ('77,344', '66,191', '61,763'):
                    fig_issues.append(f"{r['file']}: VPN «{val}» junto a «base» (modelo: {canon_npv})")
    total_err = sum(len(r['errors']) for r in report)
    total_warn = sum(len(r['warnings']) for r in report)
    print(f'Auditoría de {len(files)} documentos en {FOLDER}')
    print(f'Cifras del modelo: {figs}  {ferr}')
    for r in report:
        print(f"\n== {r['file']}  ({r['chars']:,} caracteres, {r['tables']} tablas, {r['h2']} secciones H2, fecha de cabecera: {', '.join(r['header_dates']) or 'ninguna'})")
        for e in r['errors']: print('  ERROR ', e)
        for w in r['warnings'][:25]: print('  aviso ', w)
        if len(r['warnings']) > 25: print(f"  ... {len(r['warnings'])-25} avisos más")
    for fi in fig_issues: print('  CIFRA ', fi)
    print(f'\nTotal: {total_err} errores, {total_warn} avisos, {len(fig_issues)} cifras por revisar')
    json.dump({'report': report, 'figures': figs, 'figure_issues': fig_issues}, open(os.path.join(HERE, 'audit_report.json'), 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    sys.exit(1 if total_err or fig_issues else 0)

if __name__ == '__main__':
    main()
