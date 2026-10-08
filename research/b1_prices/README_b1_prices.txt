B1 - Panama public-tender awarded unit prices for target generics (built 2026-10-05)
==================================================================================

MAIN FILES
- prices.csv          1,122 rows; one row per awarded line (or, for the MINSA-CSS joint-purchase bid tables, one row per renglon with bids only).
                      Key columns: sku_code, target_sku (Y = exact target SKU; N = related variant), molecule/strength/form/unit,
                      buying_entity/unit, act_number, framework_or_origin_act, date, procedure_type, quantity,
                      reference_unit_price_BPA, awarded_unit_price_BPA, awarded_total_BPA, awarded_company,
                      winner_manufacturer, winner_origin_country, n_bidders, all_bid_prices_BPA, median_bid_BPA,
                      winner_to_median_bid, delivery_term, source_system, source_url, data_status, notes.
                      All prices are in B/. (balboa = USD 1:1), per dispensing unit (tablet/capsule, vial, bottle, tube), VAT 0.
- summary_by_sku.csv  Per SKU: n awarded observations (framework call-offs at the same price de-duplicated), min/median/max,
                      quantity-weighted average, total quantity, median winner/median-bid ratio, median n bidders, CSS LPU award,
                      joint-purchase lowest bids.  Rows tagged "HIGH OUTLIER" (>6x SKU median; pack/unit errors) are excluded.
- bids_detail.csv     2,914 individual bids (bidder, unit price, cumple flag, award flag, manufacturer, country of origin when declared).

SOURCES (all public, unauthenticated; no login, forms or CAPTCHAs)
1. PanamaCompra v3 public API (the JSON the portal itself calls):
   - search:  POST https://apisv3.panamacompra.gob.pa/busqueda/proceso-lista-publico  (body: {"registrosPorPagina":50,"valorSiguiente":"","filtro":{"titulo":"<term>","fechaDesde":"2024-01-01","fechaHasta":"2026-10-05","idEstado":0,"idTipoProceso":-1,"idProvincia":0}})
   - detail:  GET  https://apisv3.panamacompra.gob.pa/procesos-configuracion/pagina-componentes-publico/{idTipoProceso}/procesoVistaPliego/{idProcesosContratacionFlujos}
              -> items (cantidad, precioReferencia total, precio unit), awarded offers, related "proceso original" (cotizacion en linea)
   - bids:    GET  https://apisv3.panamacompra.gob.pa/documentos-actos-publico/cuadroPropuesta/{tp}/procesoVistaCuadroPropuesta/{flujo}
   - award:   POST https://apisv3.panamacompra.gob.pa/ps/adjudicacion/acta/preview-publico/get-page
   - lookup:  GET  https://apisv3.panamacompra.gob.pa/busqueda/proceso-sistema/{numProceso}
   - Human-readable portal page for any act: https://www.panamacompra.gob.pa/Inicio/#/busqueda-numero-licitacion/{numProceso}
2. PanamaCompra legacy V2 (ASMX, form-encoded METHOD=1&VALUE={json}):
   - https://www.panamacompra.gob.pa/Security/pliegoCargo.asmx/ListarDependencias (pliego, items, attachments)
   - https://www.panamacompra.gob.pa/Security/pliegoCargo.asmx/CuadroComparativoLc (bid tables; prices rounded to 2 dp; no award flag)
3. ANTAI transparency platform (monthly "Actos publicos relativos a contrataciones publicas", Ley 6/2002 art. 11):
   - list:  GET https://monitoreo.antai.gob.pa/api/entities/{id}/submissions?period_month=M&period_year=Y&enabled=1&with_entity_documentation=1
   - table: https://monitoreo.antai.gob.pa/api/public-act-contractings/download/{tableId}/csv  (also /pdf, /xlsx)
   - entities: CSS=20, MINSA=100, Hospital Santo Tomas=91, Hospital del Nino=90, Instituto Oncologico Nacional=101
4. datosabiertos.gob.pa CSS "Inventario trimestral de medicamentos" (PRECIO UNITARIO B/. = CSS book cost), used only as cross-check.

CAVEATS
- LPU (licitacion por precio unico) quantities are 15-month estimated needs, not purchase commitments.
- ANTAI unit column is rounded to 2 decimals; awarded_unit_price_BPA uses total/quantity where available.
- ANTAI lines with quantity = 1 (contract totals, e.g. LPU 01-2026 lines) were excluded.
- V2 joint-purchase cuadros do not flag winners; rows are labelled "BIDS ONLY". Winners appear in ANTAI call-off rows (framework_or_origin_act).
- Country of origin is parsed from free-text bidder descriptions; blank/garbled when the bidder did not state it in a standard way.

RAW DATA: raw/ (antai/, antai_enum/ (CSV exports 2024-01..2026-09), panamacompra/ (search, harvest, api, v2), pc_attach/, datosabiertos/)
SCRIPTS:  ../../scripts_b1/ (antai_enum.py, antai_scan.py, pc_search.py, pc_harvest.py, parse_cuadro.py, parse_v2_cuadro.py, v2_enrich.py, consolidate.py)
