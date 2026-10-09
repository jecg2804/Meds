# -*- coding: utf-8 -*-
"""PDF para imprimir o mandar: Markdown -> HTML (pandoc) -> PDF (Chromium sin interfaz). El HTML queda en build/ (no versionado)."""
import os
import re
import subprocess
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
BUILD = os.path.join(ROOT, 'build')
CHROME = os.environ.get('CHROME', '/opt/pw-browsers/chromium')
PDFS = [  # (markdown, pdf, idioma, título)
    ('docs/socios_panama/1_Resumen_para_socios_e_inversionistas.md', 'docs/socios_panama/1_Resumen_para_socios_e_inversionistas.pdf', 'es',
     'Resumen para socios e inversionistas'),
    ('docs/compartido_todos/Panama_project_overview_and_requirements.md', 'docs/compartido_todos/Panama_project_overview_and_requirements.pdf', 'en',
     'Panama generics project: overview'),
]
CSS = """
@page { size: Letter; margin: 16mm 15mm 16mm 15mm; }
body { font-family: 'DejaVu Sans', Arial, sans-serif; font-size: 9.6pt; line-height: 1.38; color: #1d1d1f; }
h1 { font-size: 17pt; margin: 0 0 6pt 0; color: #0b3d6e; }
h2 { font-size: 12.5pt; margin: 14pt 0 5pt 0; color: #0b3d6e; border-bottom: 1px solid #c9d6e3; padding-bottom: 2pt; }
h3 { font-size: 11pt; margin: 10pt 0 4pt 0; color: #0b3d6e; }
p, li { margin: 3pt 0; }
em { color: #444; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 8pt 0; font-size: 8.4pt; page-break-inside: auto; }
th, td { border: 1px solid #c9d6e3; padding: 3pt 4pt; vertical-align: top; text-align: left; }
th { background: #e8eff6; }
tr { page-break-inside: avoid; }
code, pre { font-family: 'DejaVu Sans Mono', monospace; font-size: 8.2pt; }
pre { background: #f5f7f9; border: 1px solid #dde3e9; padding: 6pt; white-space: pre-wrap; }
a { color: #0b3d6e; word-break: break-all; }
"""


def build(md_rel, pdf_rel, lang, title):
    md = open(os.path.join(ROOT, md_rel), encoding='utf-8').read()
    html = subprocess.run(['pandoc', '-f', 'gfm', '-t', 'html', '--wrap=none'], input=md.encode('utf-8'), capture_output=True, check=True).stdout.decode('utf-8')
    doc = f'<!doctype html><html lang="{lang}"><head><meta charset="utf-8"><title>{title}</title><style>{CSS}</style></head><body>{html}</body></html>'
    os.makedirs(BUILD, exist_ok=True)
    hp = os.path.join(BUILD, os.path.basename(pdf_rel).replace('.pdf', '.html'))
    open(hp, 'w', encoding='utf-8').write(doc)
    out = os.path.join(ROOT, pdf_rel)
    subprocess.run([CHROME, '--headless=new', '--no-sandbox', '--disable-gpu', '--no-pdf-header-footer', f'--print-to-pdf={out}', 'file://' + hp],
                   check=True, capture_output=True, timeout=180)
    n = subprocess.run(['pdfinfo', out], capture_output=True, text=True).stdout
    pages = re.search(r'Pages:\s+(\d+)', n)
    print(f"{pdf_rel}: {os.path.getsize(out):,} bytes, {pages.group(1) if pages else '?'} páginas")


if __name__ == '__main__':
    for args in PDFS:
        build(*args)
