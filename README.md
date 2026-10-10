# Meds: distribuidora de genéricos para compras públicas en Panamá

Repositorio del negocio: modelo financiero (motor mensual de 60 meses y simulación de Monte Carlo), generador de documentos, investigación con fuentes y entregables. **Debe ser privado**: contiene debida diligencia sobre empresas reales y el guion de negociación.

## Documentos (Markdown; PDF solo para imprimir o mandar)

| Audiencia | Carpeta | Documentos |
| --- | --- | --- |
| Todos, incluido Rutul Patel (inglés) | `docs/compartido_todos/` | `Panama_project_overview_and_requirements.md` (+ PDF) |
| Socios panameños e inversionistas (español) | `docs/socios_panama/` | 1 Resumen (+ PDF), 2 Plan de negocio, 3 Debida diligencia del proveedor, 4 Negociación con Rutul Patel, 5 Seguimiento operativo |
| Privado de Jaime | `private/` (no se sube) | Bitácora del negocio |

## Mapa

| Carpeta | Qué hay |
| --- | --- |
| `model/` | `inputs.py` (supuestos con rango pesimista, base y optimista y su fuente), `engine.py` (flujo de caja mensual vectorizado), `mc.py` (sorteos y compuertas), `structures.py` (simulación por estructura del trato), `analysis.py` (escenarios, sensibilidad, qué pasaría si, techos de precio), `build_numbers.py` (escribe `outputs/numbers.json`), `build_xlsx.py` (Excel con fórmulas vivas) |
| `docs_src/` | Plantillas Jinja2 de cada documento (`templates/`), `render.py`, `audit.py` (falla si hay celdas vacías, citas sin fuente, nombres privados o datos internos en el documento para Rutul) y `build_pdf.py` |
| `docs/` | Documentos generados (no se editan a mano) |
| `outputs/` | `numbers.json` (única fuente de cifras de los documentos) y `Modelo_financiero.xlsx` |
| `research/` | Notas y datos de cada ronda de investigación; `verificacion_2026-10-09/` tiene el registro de 487 afirmaciones verificadas con fuente y fecha, y los datos que alimentan el modelo |

## Cómo regenerar todo

```bash
pip install numpy scipy openpyxl jinja2   # pandoc y chromium para el PDF
bash build.sh
```

Cambios de supuestos → `model/inputs.py`. Cambios de texto → `docs_src/templates/`. Nada de cifras a mano: todas salen de `outputs/numbers.json`.

## Convenciones

- Español neutro de Panamá; B/. para balboas; «Rutul Patel» o «Patel».
- Toda cifra lleva su naturaleza: F (dato verificado), R (referencia indirecta), E (estimación).
- En el documento para Rutul nunca aparece el nombre de la fábrica ni la investigación sobre ella; `audit.py` lo bloquea.
- Ningún mensaje a terceros sale sin la aprobación de Jaime.
