# Round 2 (r2a) procurement pull: summary

Compiled 2026-10-06. Sources: public PanamaCompra v3 API, legacy PanamaCompra V2 endpoints and the ANTAI API. No log-in, no forms, no web search.
- **F** = fact from an opened source; the URL is given or is in the CSV row.
- **E** = my estimate or calculation.
- Currency is B/. (balboa = USD).

## Task 4: CSS LPU 01-2026 as a whole (2025-1-10-01-99-SPU-000009)

**F inputs:**
- Bids: https://apisv3.panamacompra.gob.pa/documentos-actos-publico/cuadroPropuesta/12/procesoVistaCuadroPropuesta/712894
- Items: https://apisv3.panamacompra.gob.pa/procesos-configuracion/pagina-componentes-publico/12/procesoVistaPliego/712894
- Award acta: Res. DNC-044-2026-DG of 29-01-2026 (in the portal: https://www.panamacompra.gob.pa/Inicio/#/busqueda-numero-licitacion/2025-1-10-01-99-SPU-000009)
- Scope: 354 listed renglones, of which 6 were excluded by Adenda 1 (reference price 0). That leaves **348 net renglones**, 709 priced bids and 57 bidders.

**E** (my tabulation of the F data; per-renglón file r2a_lpu01_2026_renglon_stats.csv):

| Bids per renglón | Renglones | Share | Awarded | Median award ÷ reference |
|---|---|---|---|---|
| 0 | 35 | 10.1% | 0 | – |
| 1 | 128 | 36.8% | 113 | 1.000 |
| 2 | 81 | 23.3% | 76 | 0.923 |
| 3+ | 104 | 29.9% | 94 | 0.904 |
| **Total** | **348** | | **283 (81.3%)**; 65 void (18.7%)* | **0.963** (IQR 0.849–1.000) |

\* The resolution's count of 71 void renglones includes the 6 renglones that Adenda 1 excluded.

- **Value:** B/.77.95M awarded against B/.86.73M of reference for the same renglones, a value-weighted ratio of 0.899. Total net reference was B/.91.98M.
- **Winning price ÷ median bid:** median 0.989.
- **India-origin products** (origin as declared in each bid's free text):
  - 61 of 283 awards (21.6%) and B/.7.05M (9.0% of awarded value). Excluding the two largest renglones (apalutamida from Puerto Rico, B/.20.8M, and ácido hialurónico from Ukraine, B/.15.2M), India's value share is 16.8%.
  - India supplied 151 of 709 bids (21.3%), the most of any country, offered by 27 different bidding companies.
  - Indian products won 40% of the time they were bid, against 64% for Mexican products.
  - 14 winners (4.9%) declared no origin, so India's share is a lower bound.
- **Winners:** 44 different companies. Most renglones: PISA 31, Pharma Supplies 24, Rigar 21. Most value: IMPA-DOEL B/.24.4M, Interfarma B/.16.9M.

## Task 1: 2026 MINSA–CSS joint purchase under DE 16 of 9-Mar-2026

**F: no act exists on PanamaCompra as of 2026-10-06.** Searches run (raw results in raw/search, raw/ps and raw/v2):
1. Legacy V2 listing of joint-purchase acts (IdTipoBusqueda 71, all years): only 5 acts. These are 2025-7-0-01-08-CL-000008, 2024-7-0-01-08-CL-000005, 2024-7-0-01-99-CL-000004 (cancelled), 2023-7-0-01-08-CL-000003 and 2023-7-0-01-08-CL-000002. Type 70 lists only 2023–24 acts.
2. V3 process types 23 and 24 (critical-shortage tenders, "CL Desabastecimiento Crítico"): 0 processes in 2026, nationwide and for MINSA and CSS.
3. 864 act-number probes on the joint entity "7-0" for 2025 and 2026: only CL-000008 (2025) exists.
4. Title searches returned nothing relevant for "COMISCA", "compra conjunta", "conjunta", "desabastecimiento", "escasez", "Decreto Ejecutivo 16", "listado conjunto", "negociación conjunta", "subasta" and "atención primaria".
5. 18 sampled MINSA 2026 tenders cite only DE 27/2024 and DE 439/2020.
6. ANTAI 2026 monthly reports contain no reference to DE 16.

The output files r2a_cc2026_renglones.csv (43 rows) and r2a_cc2026_bids.csv (72 rows) therefore hold the **nearest 2026 proxies**. Every row is marked `de16_compra_conjunta = NO`.

- **MINSA reverse auctions, 2026-0-12-01-08-SSR-000001…000033** (F; likely the announced primary-care "subasta en reversa"):
  - 31 acts (19 medicines, 12 supplies): 26 adjudicado, 4 desierto, 1 cancelled. Published from April 2026 (SSR-000018 on 08-04-2026), auctions May–June, awards May–July.
  - Losing bids are in each auction report, which logs every bid. Example, SSR-000018 paracetamol 120–160 mg/5 ml: 524,358 bottles, reference 0.60. Final bids: Palm **0.40** (winner), LIFAR 0.41, Genimve 0.51, Rigar 0.55. Res. 064-M of 29-05-2026. Report: https://apisv3.panamacompra.gob.pa/procesos-contratacion-archivos/v2/download-file-21F2213F-5354-F111-80EB-0017A477FC64-ZA-101-1AZ-10368555-ZA-101-1AZ-10368555
  - Other results: sitagliptina 100 mg, 3.6M tablets, 5 bidders, Saro **0.2489** (ref 0.50). Lisinopril 20 mg, 4.93M tablets, 0.0298, single bidder.
  - E: B/.6.31M awarded vs B/.8.22M reference; median award ÷ reference 0.917. 11 of 30 auctions had a single participant.
  - Manufacturer and origin are not published for these auctions.
- **CSS and MINSA exceptional procedures for shortages or urgency (SPE)** (F): 12 medicine direct awards at the reference price, worth B/.6.04M. Example: CSS 2026-1-10-01-99-SPE-000058, irbesartán 300 mg, 5,000,000 tablets @ **0.06** (Grupo Valo), 33% above the LPU 11-2026 price of 0.045. Detail: https://apisv3.panamacompra.gob.pa/procesos-configuracion/pagina-componentes-publico/15/procesoVistaPliego/1042900

## Task 2: Commercial terms

Full quotes with page references are in **r2a_pliego_terms.md**. All F:

| Term | LPU 01-2026 | 2024 joint purchase | MINSA reverse auction 2026 |
|---|---|---|---|
| Payment | 90 days after invoice | 90 days | 90 days |
| First delivery | 45 days after refrendo to CEDIS, then 30-day call-offs | 10 working days (immediate items), else 30/45 days | 45 days, then February 2027 |
| Minimum shelf life | 18 months (default) | 18 months | 18 months |
| Late-delivery fines | 10/12/15% ÷ 30 per day | Ley 51 | 10/12/15% ÷ 30 per day |
| Bid bond | 10% | none | none |
| Performance bond | 30% | 15% | 20% |
| Quantities | Estimates; minimum commitment 60%, cut to **50% by Adenda 1**, with broad exceptions | 70% guaranteed | Fixed contract quantities |

No tender requires GMP, CPP (except 2024 biologics) or physical samples. A certificate of analysis is asked for only at delivery, "si aplica".

## Task 3: 2026 awards not captured in Round 1

r2a_prices_2026_update.csv has 81 rows, of which 76 are usable after excluding 5 pack-price rows. Columns match prices.csv. Awards Jan–Sep 2026, harvested from 1,569 candidate 2026 processes. By channel (E tabulation):
- **Centralized, 3 rows:**
  - LPU 01-2026 linagliptina 5 mg: 0.65, IMPA-DOEL, 2 bids.
  - LPU 01-2026 prednisona/prednisolona 5 mg: **0.016**, LMG Health (India), 4 bids.
  - SSR-000018 paracetamol syrup: 0.40.
- **Contratación menor, 73 rows:**
  - Paracetamol 500 mg: median 0.08 (26 rows; MINSA hospitals 0.02–0.05).
  - Prednisona 5 mg: 0.18–0.29, all Mediequipos, single bids.
  - Linagliptina: 0.80–1.17.
  - Quetiapina 25 mg: 0.13–0.75.
  - Topiramato 100 mg: 2.75 (Centro Ann Sullivan).
  - Ceftriaxona 1 g: 0.46–4.0.
- **Compra menor ágil and excepcional:** no target-SKU awards beyond those already in Round 1.

## Files

All in /tmp/claude-0/-home-claude/2629068a-9884-5985-86af-4e8c2e8b881c/scratchpad/research/r2a_procurement/:
- r2a_cc2026_renglones.csv
- r2a_cc2026_bids.csv
- r2a_pliego_terms.md
- r2a_prices_2026_update.csv
- r2a_lpu01_2026_renglon_stats.csv
- r2a_summary.md
- raw/: pliegos, auction reports, JSON caches and searches

Scripts are in scratchpad/scripts_r2a/.
