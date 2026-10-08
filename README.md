# Meds — distribuidora de medicamentos para compras públicas en Panamá

Repositorio privado del negocio. Contiene el modelo financiero (motor de 60 meses + simulación Monte Carlo), el generador del paquete de documentos para socios, las notas de investigación con sus fuentes y los entregables.

**Debe permanecer privado**: `model/build_xlsx.py` y las notas de investigación contienen parámetros personales y debida diligencia sobre personas reales.

## Formato (regla fijada el 8 de octubre de 2026)

- **Markdown es la fuente y el formato de lectura** (`docs/socios/*.md`): se lee en GitHub, en el proyecto de Claude, en Google Drive y en cualquier editor. Punto de entrada: `docs/socios/LEAME.md`.
- **PDF para imprimir o enviar a socios**: `docs/socios/Farma_paquete_socios.pdf` (todo el paquete) y `docs/socios/Resumen_ejecutivo_socios_inversionistas.pdf` (cuatro páginas con gráficos). Se generan desde el Markdown pasando por un HTML intermedio en `build/` (no versionado).
- No se usan Google Docs ni Word; nada se edita a mano en el PDF.

## Mapa

| Carpeta | Qué hay | Quién la toca |
| --- | --- | --- |
| `model/` | `inputs.py` (SKUs, precios de referencia, supuestos con rango pes/base/opt y fuente), `engine.py` (flujo de caja mensual vectorizado), `mc.py`/`run_mc.py`/`stats_v3.py` (Monte Carlo, 20,000 escenarios), `build_xlsx.py` (Excel con fórmulas vivas), `analysis.py` (sensibilidad, palancas, descomposición), `ie_kelly.py`, `option_c.py`; resultados `*.json` | Claude (orquestador) |
| `docs_build/` | `build_docs.py` + `audit_edits.py` (pasadas 1 y 2) + `audit_edits2.py` (pasada 3: índice único, tablas nuevas, correcciones) generan el paquete `docs/socios/` a partir de `exports/` y del motor; `audit_md.py` audita los Markdown; `build_html.py` arma el HTML intermedio; `exec/` genera el resumen ejecutivo (Markdown y HTML con gráficos); `build_all.sh` corre todo | Claude |
| `docs/socios/` | El paquete para socios: `LEAME.md`, 00–07, anexos, `Cotizaciones_3PL_seguimiento.md`, `Resumen_ejecutivo_socios_inversionistas.md` y los dos PDF. **Fuente de verdad** de lo que se publica en Google Drive y en el proyecto de Claude | Se lee; no se edita a mano (se regenera) salvo `Cotizaciones_3PL_seguimiento.md` |
| `research/` | Notas y datos de cada ronda de investigación con URL y fecha: precios adjudicados (PanamaCompra), costo puesto en Panamá, finanzas y pagos, competencia, regulación, debida diligencia del socio, 3PL, procurement 2026 | Claude |
| `outputs/` | Excel entregables: modelo para socios (sin cifras personales), hoja de datos de fábrica, cuestionario del 3PL en blanco | Se suben a Drive (los pequeños) o viajan por chat |

## Cómo regenerar todo

```bash
pip install numpy openpyxl matplotlib   # pandoc y chromium para el PDF
bash docs_build/build_all.sh            # Markdown → auditoría → HTML intermedio → PDF
python3 model/run_mc.py && python3 model/stats_v3.py   # recalcula la simulación (minutos)
python3 model/build_xlsx.py             # reconstruye el Excel completo (requiere los parámetros personales)
```

Las cifras de los documentos salen del motor en tiempo de build; no se editan números a mano. Cambios de supuestos → `model/inputs.py`; cambios de texto → `docs_build/audit_edits2.py` (reemplazos con anclaje, fallan si el texto cambió) o `exports/`. La auditoría (`audit_md.py`) revisa celdas vacías, columnas desparejas, frases prohibidas, encabezados, referencias rotas y cifras clave contra el modelo; el build falla si hay errores.

## Flujo de actualización (una ronda)

1. Lo que mande Rutul o una cotización → se anota en la tabla de seguimiento (06 o `Cotizaciones_3PL_seguimiento.md`) y, si cambia un supuesto, en `inputs.py`.
2. `bash docs_build/build_all.sh` → `docs/socios/` (Markdown y PDF).
3. Commit con mensaje que diga qué cambió y por qué (fuente).
4. Publicar: proyecto de Claude (`socios/`), Google Drive `Farma/02 Socios Panamá/00 Plan y análisis (socios)` (los mismos `.md`), bitácora.

## Convenciones

- Español neutro de Panamá; B/. para balboas; fechas completas; «Rutul Patel» o «Patel», nunca otra forma.
- Toda cifra lleva su naturaleza: tarifa publicada, norma, referencia indirecta, supuesto presupuestario, estimación compuesta.
- Celdas sin dato llevan «—»; nada de marcadores («ver abajo», «TBD») ni gráficos sin gráfico.
- Nada que vaya a Rutul sale de este repositorio salvo lo que está en `outputs/` (hoja de datos y cuestionario) y, cuando exista, la propuesta de términos.
