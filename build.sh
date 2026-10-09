#!/usr/bin/env bash
# Regenera todo: números del modelo -> Excel -> documentos -> auditoría -> PDF.
# Uso: bash build.sh            (unos 30 segundos; la simulación usa 2 procesos)
set -euo pipefail
cd "$(dirname "$0")"
python3 model/build_numbers.py
(cd model && python3 build_xlsx.py ../outputs/Modelo_financiero.xlsx >/dev/null && echo "outputs/Modelo_financiero.xlsx regenerado")
python3 docs_src/render.py
python3 docs_src/audit.py
python3 docs_src/build_pdf.py
