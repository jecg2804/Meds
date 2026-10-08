#!/usr/bin/env bash
# Regenera todo el paquete para socios desde las fuentes:
#   Markdown (docs/socios/*.md)  →  HTML intermedio (build/)  →  PDF (docs/socios/*.pdf)
# y corre la auditoría de los Markdown. Uso: bash docs_build/build_all.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
export SOCIOS_OUT="$ROOT/docs/socios" BUILD_DIR="$ROOT/build"
mkdir -p "$BUILD_DIR"

echo "== 1. Documentos Markdown (motor + exports + ediciones de auditoría)"
python3 "$ROOT/docs_build/build_docs.py" | tail -14
python3 "$ROOT/docs_build/exec/build_exec_md.py"

echo "== 2. Auditoría de los Markdown"
python3 "$ROOT/docs_build/audit_md.py" "$SOCIOS_OUT" | tail -3

echo "== 3. HTML intermedio (resumen ejecutivo con gráficos y paquete navegable)"
python3 "$ROOT/docs_build/exec/charts.py"
python3 "$ROOT/docs_build/exec/build_exec.py"
python3 "$ROOT/docs_build/build_html.py" "$SOCIOS_OUT" | head -3

echo "== 4. PDF para socios (Chromium)"
CHROME="$(command -v chromium || command -v chromium-browser || command -v google-chrome || true)"
if [ -z "$CHROME" ] && [ -x /opt/pw-browsers/chromium ]; then CHROME=/opt/pw-browsers/chromium; fi
if [ -n "$CHROME" ]; then
  for f in Farma_paquete_socios Resumen_ejecutivo_socios_inversionistas; do
    "$CHROME" --headless=new --no-sandbox --disable-gpu --no-pdf-header-footer \
      --print-to-pdf="$SOCIOS_OUT/$f.pdf" "file://$BUILD_DIR/$f.html" >/dev/null 2>&1 || echo "PDF falló: $f"
    ls -la "$SOCIOS_OUT/$f.pdf" | awk '{print $5, $9}'
  done
else
  echo "Chromium no disponible: no se generaron PDF"
fi
echo "== listo"
