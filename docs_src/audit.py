# -*- coding: utf-8 -*-
"""Auditoría automática de los documentos generados. Falla (código 1) si hay errores."""
import os
import re
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOCS = {
    'docs/socios_panama/1_Resumen_para_socios_e_inversionistas.md': 'es',
    'docs/socios_panama/2_Plan_de_negocio.md': 'es',
    'docs/socios_panama/3_Debida_diligencia_del_proveedor.md': 'es',
    'docs/socios_panama/4_Negociacion_con_Rutul_Patel.md': 'es',
    'docs/socios_panama/5_Seguimiento_operativo.md': 'es',
    'docs/compartido_todos/Panama_project_overview_and_requirements.md': 'rutul',
    'private/Bitacora_negocio.md': 'private',
}
FORBIDDEN_ALL = [r'\{\{', r'\{%', r'socio indio', r'\bTBD\b', r'ver abajo', r'\bXXX\b', r'\bnan\b', r'\bNaN\b', r'pasó de \d', r'versión anterior']
# nombres privados: viven en private/nombres_privados.txt (no versionado), uno por línea; solo pueden aparecer en la bitácora
_pn = os.path.join(ROOT, 'private', 'nombres_privados.txt')
FORBIDDEN_SHARED = [re.escape(x.strip()) for x in open(_pn, encoding='utf-8')] if os.path.exists(_pn) else []
FORBIDDEN_SHARED = [x for x in FORBIDDEN_SHARED if x]
FORBIDDEN_RUTUL = [r'Bueno', r'Sanand', r'Dudhwewala', r'Deepti', r'Bhargava', r'\bModi\b', r'NSQ', r'nephew', r'minister',
                   r'Boyd', r'probability', r'NPV', r'net present', r'ceiling', r'loss', r'Lorisol', r'K-20', r'Tofler', r'Falconebiz']
VOSEO = [r'\btenés\b', r'\bpodés\b', r'\bquerés\b', r'\bsabés\b', r'\bvos\b', r'\bdecime\b', r'\bmirá\b', r'\bfijate\b']
errors, warns = [], []


def check_tables(path, lines):
    i = 0
    while i < len(lines):
        if lines[i].startswith('|') and i + 1 < len(lines) and re.match(r'^\|\s*-{3}', lines[i + 1]):
            ncol = lines[i].count('|')
            j = i
            while j < len(lines) and lines[j].startswith('|'):
                row = lines[j]
                if row.count('|') != ncol and not ('`' in row):
                    errors.append(f'{path}:{j + 1}: tabla con {row.count("|") - 1} columnas en vez de {ncol - 1}')
                cells = [c.strip() for c in row.strip().strip('|').split('|')]
                if any(c == '' for c in cells):
                    errors.append(f'{path}:{j + 1}: celda vacía')
                j += 1
            i = j
        else:
            i += 1


def check_sources(path, text):
    m = re.search(r'^## (Fuentes|Sources)\s*$', text, re.M)
    if not m:
        if '[1]' in text:
            errors.append(f'{path}: cita fuentes pero no tiene sección de fuentes')
        return
    body, refs = text[:m.start()], text[m.end():]
    listed = set(int(x) for x in re.findall(r'^(\d+)\. ', refs, re.M))
    cited = set(int(x) for x in re.findall(r'\[(\d+)\]', body))
    for c in sorted(cited - listed):
        errors.append(f'{path}: cita [{c}] sin fuente en la lista')
    for l in sorted(listed - cited):
        warns.append(f'{path}: fuente {l} listada pero no citada en el texto')
    for u in re.findall(r'<([^>]+)>', refs):
        if not u.startswith('http'):
            errors.append(f'{path}: enlace mal formado: {u[:60]}')


for rel, kind in DOCS.items():
    path = os.path.join(ROOT, rel)
    if not os.path.exists(path):
        errors.append(f'falta {rel}'); continue
    text = open(path, encoding='utf-8').read()
    lines = text.split('\n')
    pats = FORBIDDEN_ALL + ([] if kind == 'private' else FORBIDDEN_SHARED) + (FORBIDDEN_RUTUL if kind == 'rutul' else []) + (VOSEO if kind != 'rutul' else [])
    for p in pats:
        for mm in re.finditer(p, text, flags=(re.I if kind == 'rutul' else 0)):
            ln = text[:mm.start()].count('\n') + 1
            errors.append(f'{rel}:{ln}: patrón prohibido «{p}»: …{text[max(0, mm.start() - 30):mm.end() + 30]}…'.replace('\n', ' '))
    check_tables(rel, lines)
    check_sources(rel, text)
    if not lines[0].startswith('# '):
        errors.append(f'{rel}: no empieza con un título')
    if re.search(r'\n{3,}', text):
        warns.append(f'{rel}: líneas en blanco repetidas')

print(f'Auditoría: {len(errors)} errores, {len(warns)} avisos')
for e in errors:
    print('ERROR', e)
for w in warns:
    print('aviso', w)
sys.exit(1 if errors else 0)
