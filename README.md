# Meds — distribuidora de medicamentos para compras públicas en Panamá

Repositorio privado del negocio. Contiene el modelo financiero (motor de 60 meses + simulación Monte Carlo), el generador del paquete de documentos para socios, las notas de investigación con sus fuentes y los entregables.

**Debe permanecer privado**: `model/build_xlsx.py` y las notas de investigación contienen parámetros personales y debida diligencia sobre personas reales.

## Mapa

| Carpeta | Qué hay | Quién la toca |
| --- | --- | --- |
| `model/` | `inputs.py` (SKUs, precios de referencia, supuestos con rango pes/base/opt y fuente), `engine.py` (flujo de caja mensual vectorizado), `mc.py`/`run_mc.py`/`stats_v3.py` (Monte Carlo, 20,000 escenarios), `build_xlsx.py` (Excel con fórmulas vivas), `ie_kelly.py`, `option_c.py`; resultados `*.json` | Claude (orquestador) |
| `docs_build/` | `build_docs.py` + `audit_edits.py` generan el paquete `docs/socios/` a partir de `exports/` (los cuatro documentos originales) y del motor | Claude |
| `docs/socios/` | El paquete para socios (00–07 + anexos). **Fuente de verdad** de lo que se publica en Google Drive como Google Docs | Se lee; no se edita a mano (se regenera) |
| `research/` | Notas y datos de cada ronda de investigación con URL y fecha: precios adjudicados (PanamaCompra), costo puesto en Panamá, finanzas y pagos, competencia, regulación, debida diligencia del socio, 3PL, procurement 2026 | Claude |
| `outputs/` | Excel entregables: modelo para socios (sin cifras personales), hoja de datos de fábrica, cuestionario del 3PL en blanco | Se copian a Drive a mano |

## Cómo regenerar todo

```bash
pip install numpy openpyxl            # pandoc opcional para HTML
python3 docs_build/build_docs.py      # escribe docs/socios/ (o $SOCIOS_OUT)
python3 model/run_mc.py && python3 model/stats_v3.py   # recalcula la simulación (minutos)
python3 model/build_xlsx.py           # reconstruye el Excel completo (requiere los parámetros personales)
```

Las cifras de los documentos salen del motor en tiempo de build; no se editan números a mano. Cambios de supuestos → `model/inputs.py`; cambios de texto → `docs_build/audit_edits.py` (reemplazos con fecha) o `exports/`.

## Flujo de actualización (una ronda)

1. Lo que mande Rutul o una cotización → se anota en la tabla de seguimiento (06) y, si cambia un supuesto, en `inputs.py`.
2. `build_docs.py` → `docs/socios/`; recalcular el Excel.
3. Commit con mensaje que diga qué cambió y por qué (fuente).
4. Publicar: proyecto de Claude (`socios/`), Google Drive «Farma – Socios Panamá / 00 Plan y análisis» (Google Docs regenerados desde el HTML), bitácora.

## Convenciones

- Español neutro de Panamá; B/. para balboas; fechas completas.
- Toda cifra lleva su naturaleza: tarifa publicada, norma, referencia indirecta, supuesto presupuestario, estimación compuesta.
- Nada que vaya a Rutul sale de este repositorio salvo lo que está en `outputs/` (hoja de datos y cuestionario) y, cuando exista, la propuesta de términos.
