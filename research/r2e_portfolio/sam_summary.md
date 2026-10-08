# Portfolio SAM summary – Indian generics (PICS/Zywie + Modi catalogs) vs Panamanian public demand

Built 2026-10-06 from local files only (scripts in `r2e_portfolio/scripts/`; every figure traces to a CSV row in this folder). Currency B/. (= USD). **Annualized** = max quantity × 12 / term months (LPU 15, compra conjunta 24, MINSA SSR 12 assumed); decentralized = awarded quantity Jan-2025…Sep-2026 × 12/21. Value = annualized qty × award price (else lowest bid, else reference price – flagged in `value_basis`). Only **exact** catalog matches (molecule + strength + form + release) are counted; `strength_diff` is shown as an upside variant; `review` rows are never counted.

## 0. Counts

| Item | Count |
|---|---|
| Catalog rows (product × strength × form) | 713 (PICS 596, Modi 117) |
| Distinct catalog SKUs (molecules+strength+form, PICS∪Modi) | 653 |
| DE 16 renglones parsed | 376 |
| DE 16 – exact | 45 |
| DE 16 – strength_diff | 6 |
| DE 16 – review | 4 |
| DE 16 – molecule_only | 47 |
| DE 16 – none | 274 |
| DE 16 exact – of which TE-required (Y/check/combo-check) / controlled | 23 / 3 |
| CC 2023 CL-000002 – renglones in file / exact / strength_diff / review | 268 / 35 / 5 / 1 |
| CC 2023 CL-000003 – renglones in file / exact / strength_diff / review | 142 / 19 / 5 / 0 |
| CC 2024 CL-000005 – renglones in file / exact / strength_diff / review | 205 / 21 / 3 / 3 |
| CC 2025 CL-000008 – renglones in file / exact / strength_diff / review | 21 / 4 / 0 / 0 |
| LPU 01-2026 – renglones in file / exact / strength_diff / review | 354 / 37 / 7 / 2 |
| LPU 11-2026 – renglones in file / exact / strength_diff / review | 133 / 26 / 5 / 3 |
| MINSA SSR 2026 – renglones in file / exact / strength_diff / review | 19 / 4 / 1 / 0 |
| SPE 2026 (exceptional, reference only) – renglones in file / exact / strength_diff / review | 12 / 1 / 0 / 0 |
| Decentralized: catalog SKUs with ≥1 exact-matched awarded line (2023-26) | 89 |

Res. 985 check (parsed 173/173 entries incl. #149 sitagliptina and #151 sofosbuvir+ledipasvir): all 23 actives the brief lists as ON are on the list; none of the 18 listed as NOT appear (as single or combination).

## (a) Annualized value of matched demand by segment

**Centralized, de-duplicated** (one demand estimate per SKU and buyer: CSS = latest of LPU 01/11-2026 → CC 2025 → CC 2024; MINSA = SSR 2026; CC 2023 joint MINSA+CSS only if the SKU is in no later act; CC 2023 CL-000002 renglones re-tendered in CL-000003 counted once). **Decentralized**: CSS = all CSS units (ANTAI, complete); MINSA/patronatos = Hospital del Niño + ION (ANTAI, complete) + MINSA regions/hospitals only where harvested (partial).

| Segment | Central renglones | Central B/./yr (exact, latest cycle) | Central (+strength_diff upside) | Central national proxy* | Decentral SKUs | Decentral CSS B/./yr | Decentral MINSA/pat B/./yr | **Total exact B/./yr** (latest cycle + decentral) |
|---|---|---|---|---|---|---|---|---|
| First wave (TE not required, not controlled) | 38 | 3,377,861 | 3,726,835 | 4,958,326 | 55 | 379,613 | 677,700 | **4,435,174** |
| TE-required (Y + 'check'/'combo-check') | 33 | 4,939,234 | 5,339,346 | 5,547,229 | 32 | 1,967,680 | 678,905 | **7,585,819** |
| Controlled (Y + 'likely') | 4 | 278,570 | 278,570 | 278,570 | 7 | 29,680 | 52,365 | **360,614** |
| Sterile injectables | 4 | 190,002 | 190,002 | 296,222 | 5 | 7,969 | 92,595 | **290,566** |
| Beta-lactams | 8 | 611,990 | 614,503 | 1,175,906 | 10 | 7,969 | 181,792 | **801,751** |
| All matched | 73 | 8,520,598 | 9,269,683 | 10,709,058 | 89 | 2,376,150 | 1,368,239 | **12,264,986** |

*National proxy = per SKU the larger of (latest-cycle value) and (CC 2023 joint MINSA+CSS value). MINSA has no 2026 joint purchase yet (DE 16's compra conjunta is unpublished) and SSR 2026 covers only 19 medicines, so for most SKUs MINSA's centralized demand is visible only in CC 2023; the latest-cycle column therefore understates national demand (e.g. albendazol 40 mg/ml: LPU 01-2026 ≈19k bottles/yr vs CC 2023 ≈390k/yr).

Segments overlap (e.g. a cephalosporin vial is both sterile and beta-lactam; a TE-required psychotropic can be controlled); only *First wave* + *TE-required* + *Controlled-only* partition the total.

Per-act (not de-duplicated) annualized value of exact matches, for reference:

| Act | Term (m) | Exact renglones | Annualized B/. | of which awarded basis | lowest-bid basis | reference basis |
|---|---|---|---|---|---|---|
| CC 2023 CL-000002 | 24 | 35 | 6,484,939 | 806,328 | 5,678,611 | 0 |
| CC 2023 CL-000003 | 24 | 19 | 1,343,501 | 285,834 | 1,057,667 | 0 |
| CC 2024 CL-000005 | 24 | 21 | 2,831,054 | 609,413 | 2,221,641 | 0 |
| CC 2025 CL-000008 | 24 | 4 | 350,114 | 263,612 | 86,502 | 0 |
| LPU 01-2026 | 15 | 35 | 2,777,566 | 2,279,672 | 419,708 | 78,186 |
| LPU 11-2026 | 15 | 26 | 4,042,777 | 3,944,857 | 0 | 97,920 |
| MINSA SSR 2026 | 12 | 4 | 912,418 | 912,418 | 0 | 0 |

## (b) Thin competition only (≤2 bidders or desierto)

| Segment | Central renglones (thin) | Central B/./yr (thin) | share of central segment | Decentral B/./yr on lines with ≤2 bidders* |
|---|---|---|---|---|
| First wave (TE not required, not controlled) | 19 | 1,584,870 | 47% | 623,400 |
| TE-required (Y + 'check'/'combo-check') | 16 | 1,890,231 | 38% | 1,599,784 |
| Controlled (Y + 'likely') | 3 | 249,371 | 90% | 74 |
| Sterile injectables | 1 | 60,497 | 32% | 38,121 |
| Beta-lactams | 4 | 350,605 | 57% | 78,998 |
| All matched | 37 | 3,678,604 | 43% | 2,223,185 |

*Decentralized bidder counts exist only for PanamaCompra-sourced lines (B1/R2A/2026 harvest): 522 of 736 in-window matched lines (70% of value); ANTAI rows carry no bidder count, so the decentralized thin-competition figure is a lower bound.

## (c) Top 40 opportunities (exact SKUs, annualized value at current prices)

| # | SKU (molecules \| strength \| form) | Total B/./yr | Central B/./yr | Central price | Central bidders (median) | Decentral B/./yr | Decentral median price | TE | Ctrl | Landed (base) | GM vs central | GM vs decentral |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | rosuvastatina \| 10 mg \| tablet | 1,735,400 | 492,020 | 0.018 | 6.0 | 1,243,380 | 0.100 | Y | N | – | – | – |
| 2 | dapagliflozina \| 10 mg \| tablet | 1,501,890 | 1,086,197 | 0.430 | 9.0 | 415,692 | 0.640 | Y | N | – | – | – |
| 3 | paracetamol \| 500 mg \| tablet | 576,424 | 237,705 | 0.010 | 3.0 | 338,719 | 0.020 | N | N | 0.0064 /tablet | 36% | 68% |
| 4 | acido fusidico \| 2 % \| cream/ointment | 532,447 | 459,420 | 1.970 | 1.0 | 73,027 | 9.400 | Y | N | – | – | – |
| 5 | amlodipina \| 5 mg \| tablet | 486,447 | 204,076 | 0.005 | 4.0 | 282,371 | 0.020 | Y | N | 0.0037 /tablet | 26% | 82% |
| 6 | lisinopril \| 20 mg \| tablet | 463,479 | 373,010 | 0.021 | 3.0 | 90,469 | 0.030 | Y | N | – | – | – |
| 7 | paracetamol \| 24 mg/ml \| syrup/oral liquid | 438,533 | 396,017 | 0.471 | 4.0 | 42,516 | 0.950 | N | N | 0.3329 /120 ml bottle | 29% | 65% |
| 8 | ibuprofeno \| 400 mg \| tablet | 371,424 | 359,210 | 0.030 | 3.0 | 12,213 | 0.030 | N | N | – | – | – |
| 9 | claritromicina \| 500 mg \| tablet | 359,899 | 320,583 | 0.382 | 3.0 | 39,316 | 0.600 | Y | N | – | – | – |
| 10 | ambroxol \| 3 mg/ml \| syrup/oral liquid | 308,741 | 301,102 | 0.940 | 3.0 | 7,639 | 3.320 | N | N | – | – | – |
| 11 | gliclazida \| 80 mg \| tablet | 280,540 | 234,460 | 0.038 | 2.0 | 46,080 | 0.260 | N | N | – | – | – |
| 12 | carvedilol \| 6.25 mg \| tablet | 277,464 | 185,472 | 0.028 | 3.0 | 91,992 | 0.060 | Y | N | – | – | – |
| 13 | amoxicilina \| 50 mg/ml \| suspension | 272,047 | 261,548 | 1.730 | 2.0 | 10,499 | 2.740 | N | N | – | – | – |
| 14 | clozapina \| 100 mg \| tablet | 260,747 | 260,747 | 0.394 | 2.0 | 0 | – | Y | N | – | – | – |
| 15 | clindamicina \| 300 mg \| capsule | 225,716 | 184,552 | 0.088 | 2.0 | 41,164 | 0.375 | Y | N | – | – | – |
| 16 | diazepam \| 5 mg \| tablet | 217,467 | 188,609 | 0.125 | 2.0 | 28,857 | 0.500 | N | Y | – | – | – |
| 17 | omeprazol \| 20 mg \| capsule | 197,533 | 109,786 | 0.012 | 5.0 | 87,747 | 0.160 | Y | N | 0.0075 /capsule | 37% | 95% |
| 18 | itraconazol \| 100 mg \| capsule | 185,581 | 185,581 | 1.097 | 1.0 | 0 | – | Y | N | – | – | – |
| 19 | quetiapina \| 200 mg \| tablet | 171,464 | 108,712 | 0.079 | 3.0 | 62,752 | 0.200 | N | N | – | – | – |
| 20 | amoxicilina \| 500 mg \| capsule | 168,883 | 131,881 | 0.033 | 5.0 | 37,002 | 0.130 | N | N | – | – | – |
| 21 | carbamazepina \| 200 mg \| tablet | 154,546 | 130,492 | 0.077 | 1.0 | 24,053 | 0.250 | Y | N | – | – | – |
| 22 | haloperidol \| 5 mg \| tablet | 135,798 | 135,798 | 0.468 | 1.0 | 0 | – | Y | N | – | – | – |
| 23 | fluoxetina \| 20 mg \| tablet | 130,790 | 130,141 | 0.052 | 2.0 | 649 | 0.320 | Y | N | – | – | – |
| 24 | prednisolona \| 5 mg \| tablet | 106,336 | 55,964 | 0.016 | 4.0 | 50,372 | 0.240 | N | N | – | – | – |
| 25 | ciprofloxacina \| 500 mg \| tablet | 106,042 | 71,948 | 0.037 | 6.0 | 34,094 | 0.500 | Y | N | – | – | – |
| 26 | furosemida \| 40 mg \| tablet | 104,462 | 103,592 | 0.025 | 1.0 | 870 | 0.200 | Y | N | – | – | – |
| 27 | pramipexol \| 0.25 mg \| tablet | 102,397 | 98,625 | 0.600 | 1.0 | 3,771 | 0.550 | N | N | – | – | – |
| 28 | linagliptina \| 5 mg \| tablet | 97,966 | 63,492 | 0.650 | 2.0 | 34,474 | 0.885 | N | N | – | – | – |
| 29 | diclofenaco \| 50 mg \| tablet | 88,806 | 88,435 | 0.014 | 4.0 | 371 | 0.200 | N | N | – | – | – |
| 30 | metronidazol \| 500 mg \| tablet | 87,135 | 79,566 | 0.030 | 10.0 | 7,570 | 0.500 | Y | N | – | – | – |
| 31 | divalproato de sodio \| 500 mg \| tablet | 84,087 | 0 | – | – | 84,087 | 0.210 | Y | N | – | – | – |
| 32 | ceftriaxona \| 1000 mg \| injection_powder | 82,725 | 46,424 | 0.239 | 6.0 | 36,301 | 0.450 | N | N | 0.2184 /vial | 9% | 51% |
| 33 | cefotaxima \| 1000 mg \| injection_powder | 79,805 | 43,690 | 0.259 | 3.0 | 36,115 | 0.700 | N | N | 0.1281 /vial | 51% | 82% |
| 34 | amitriptilina \| 10 mg \| tablet | 78,186 | 78,186 | 0.240 | 0.0 | 0 | – | N | N | – | – | – |
| 35 | mometasona \| 0.1 % \| cream/ointment | 76,918 | 66,844 | 1.020 | 1.0 | 10,074 | 4.790 | N | N | – | – | – |
| 36 | eritromicina \| 500 mg \| tablet | 71,633 | 71,633 | 0.200 | 7.0 | 0 | – | N | N | – | – | – |
| 37 | loratadina \| 10 mg \| tablet | 70,680 | 66,084 | 0.008 | 3.0 | 4,597 | 0.480 | N | N | – | – | – |
| 38 | clobetasol \| 0.05 % \| cream/ointment | 66,430 | 45,469 | 1.460 | 2.0 | 20,961 | 5.390 | N | N | – | – | – |
| 39 | cefepima \| 1000 mg \| injection_powder | 65,631 | 60,497 | 0.700 | 4.0 | 5,134 | 0.830 | N | N | – | – | – |
| 40 | quetiapina \| 100 mg \| tablet | 62,434 | 0 | – | – | 62,434 | 0.130 | N | N | – | – | – |

Central price = annualized value ÷ annualized qty over the de-duplicated renglones (award where known, else lowest bid). Landed = `b2_landed/landed.csv` landed_base (per unit stated there; bottle sizes for liquids/creams must match the tender presentation). GM = 1 − landed/price, before registration, TE, QC, bonds and distribution costs.

## (d) India-origin share of LPU 01-2026 and how Indian makers go to market

- LPU 01-2026 (2025-1-10-01-99-SPU-000009): 348 net renglones, 283 awarded, awarded value B/.77.95M (award price × max qty).
- **India-origin winners: 61 of 283 awards (21.6%), B/.7.05M (9.0% of awarded value)**; excluding the two largest renglones (APALUTAMIDA 60MG, TABLETA V.O. (PUERTO RICO, B/.20.79M); Derivados de Acido Hialurónico de alto p (UCRANIA, B/.15.19M)) India's value share is 16.8%. 12 awards declare no parsable origin, so India is a lower bound.
- India-origin bids: 147 of 709 priced bids (20.7%), on 107 renglones, by 27 distinct Panamanian bidders; Indian bids won 41% of the time.
- Across all centralized bid tables (LPU 01-2026, LPU 11-2026, CC 2023 CL-2/CL-3, CC 2024 CL-5, CC 2025 CL-8), **61 Indian manufacturers appear through a single Panamanian distributor and 15 through two or more** (63% of India-origin bids come from single-distributor manufacturers).

Manufacturer → distributors (bids/wins), all centralized bid tables 2023-2026, India-origin bids (by act: `india_mfr_distributors.csv`; CC winners known only where a CSS ANTAI contract confirms them, so CC wins are understated):

| Manufacturer (normalized) | # distributors | Bids | Wins | Distributors (bids/wins) |
|---|---|---|---|---|
| HETERO | 1 | 54 | 17 | SEVEN PHARMA (54/17) |
| AUROCHEM | 4 | 31 | 13 | LANCO (12/6); INVERSIONES TAGORE PANAMA (9/6); GEOMEDIC PHARMACEUTICA (5/1); INVERSIONES Y SERVICIOS NACIONALES (5/0) |
| BRAWN | 2 | 21 | 10 | BEST MEDICAL (15/10); EUROGENERICOS DE PANAMA (6/0) |
| ACULIFE | 1 | 10 | 5 | PHARMA SUPPLIES (10/5) |
| ASPIRO | 1 | 9 | 0 | SEVEN PHARMA (9/0) |
| DR REDDY | 1 | 8 | 2 | LANCO (8/2) |
| APEX DRUG | 1 | 7 | 3 | GENIMVE PHARMA (7/3) |
| CAPLIN | 2 | 7 | 3 | NUTRIMED (4/0); LANCO (3/3) |
| SWISS | 5 | 7 | 2 | SERFASA (2/0); JAYOR PANAMA (2/1); DROGUERIA SARO (1/1); INVERSIONES Y SERVICIOS NACIONALES (1/0); GEOMEDIC PHARMACEUTICA (1/0) |
| FLAGSHIP | 2 | 7 | 5 | PHARMA SUPPLIES (6/4); INVERSIONES TAGORE PANAMA (1/1) |
| CELON | 1 | 6 | 3 | SEVEN PHARMA (6/3) |
| MACLEODS | 2 | 6 | 1 | VESALIUS PHARMA (5/1); INTERNACIONAL BIO FARMACEUTICA (1/0) |
| CIPLA | 1 | 6 | 3 | PHARMA SUPPLIES (6/3) |
| TITAN | 3 | 5 | 0 | PHARMA SUPPLIES (3/0); DROGUERIA SARO (1/0); INTERNACIONAL BIO FARMACEUTICA (1/0) |
| SAKAR | 1 | 5 | 0 | VESALIUS PHARMA (5/0) |
| UNIQUE | 1 | 5 | 1 | JAYOR PANAMA (5/1) |
| SHILPA | 4 | 5 | 1 | DARE (2/0); CENFARMA (1/0); PHARMA SUPPLIES (1/0); US PHARMACY SYSTEMS (1/1) |
| KWALITY | 3 | 5 | 2 | PROQUIFAR (2/0); SERFASA (2/1); DROGUERIA E IMPORTADORA ALEMANA (1/1) |
| EMIL PHARMACEUTICAL | 2 | 4 | 1 | LANCO (3/0); LMG HEALTH S DE R L (1/1) |
| PANACEA | 1 | 4 | 0 | NUTRIMED (4/0) |
| REMUS | 3 | 4 | 2 | LANCO (2/1); BEST MEDICAL (1/0); PHARMA SUPPLIES (1/1) |
| FRESENIUS KABI | 1 | 4 | 1 | NUTRIMED (4/1) |
| SUN PHARMACEUTICAL | 1 | 4 | 0 | PHARMA CHIMIQUE DE PANAMA IMPORT EXPORT (4/0) |
| GLAND | 1 | 3 | 0 | REPRICO (3/0) |
| MEDICO REMEDIES | 1 | 3 | 0 | DISTRIBUIDORA CABADI (3/0) |
| AUROBINDO | 2 | 3 | 1 | LANCO (2/1); IMEXSATEC (1/0) |
| DIVINE | 1 | 3 | 1 | PHARMA SUPPLIES (3/1) |
| MYLAN | 1 | 3 | 1 | PHARMA CHIMIQUE DE PANAMA IMPORT EXPORT (3/1) |
| WEXFORD | 1 | 3 | 1 | FARMACEUTICOS (3/1) |
| GUFIC | 2 | 3 | 0 | DARE (2/0); US PHARMACY SYSTEMS (1/0) |

Distributors carrying the most Indian manufacturers (same bid tables):

| Distributor | # Indian manufacturers | Indian bids | Wins |
|---|---|---|---|
| SEVEN PHARMA | 7 | 75 | 23 |
| LANCO | 12 | 46 | 15 |
| PHARMA SUPPLIES | 12 | 36 | 17 |
| INVERSIONES TAGORE PANAMA | 7 | 17 | 9 |
| BEST MEDICAL | 3 | 17 | 10 |
| NUTRIMED | 5 | 16 | 1 |
| PHARMA CHIMIQUE DE PANAMA IMPORT EXPORT | 3 | 12 | 2 |
| INTERNACIONAL BIO FARMACEUTICA | 4 | 11 | 4 |
| VESALIUS PHARMA | 2 | 10 | 1 |
| GENIMVE PHARMA | 2 | 9 | 4 |
| JAYOR PANAMA | 2 | 8 | 2 |
| GEOMEDIC PHARMACEUTICA | 2 | 6 | 1 |

## (e) Data caveats

- LPU quantities are 15-month *maximum* estimates; CSS commits to only 50% (Adenda 1) with broad exceptions, so realized volume is below the annualized figures. Compra-conjunta quantities carry a 70% purchase guarantee; MINSA SSR quantities are fixed contract quantities whose period is not stated – a 12-month term is assumed.
- Centralized acts overlap in time and buyer (CC 2023 = MINSA+CSS 2024-25; CC 2024/2025 = CSS 2024-25; LPU 2026 = CSS 2026-27; SSR = MINSA 2026-27). The de-duplicated total keeps one cycle per SKU and buyer; summing acts would double count.
- Compra-conjunta bid tables (PanamaCompra V2) carry no award flag; winners were taken from CSS ANTAI contract rows only when the contracted price equals one of the bids (found for 93 of 636 CC renglones). Otherwise the lowest bid is used and flagged; MINSA-side CC awards are not visible.
- LPU 11-2026 bid file lists only the 132 renglones that received bids (157 in the act); the other 25, and CC renglones without bids, cannot be matched. The LPU 11 global renglón number is not in the file (index used).
- Decentralized coverage differs by buyer: CSS ANTAI rows cover every CSS unit (complete); Hospital del Niño and ION ANTAI rows are complete for those patronatos; MINSA regions/hospitals appear only through target-SKU harvests (B1 prices.csv, R2A) and the keyword-selected 2026 PanamaCompra harvest – MINSA decentralized demand is therefore understated, and OCDS MINSA data stop in April 2024. Hospital Santo Tomás ANTAI rows carry no quantities and were not usable.
- ANTAI unit prices are rounded; unit price = total ÷ quantity. Lines flagged as pack prices or >6× / <1/6 of the SKU median are excluded from all decentralized statistics (counts in `*_n_excluded_flagged`).
- Matching is rule-based on Spanish descriptions (INN lexicon, strength/volume normalization, form & release parsing). Liquids without a stated volume are read per 5 ml (catalog convention), which matters for metronidazole/ondansetron/co-trimoxazole suspensions; bottle sizes (60/100/120 ml) and tube sizes are not part of the match and must be checked against each pliego.
- TE flag uses Res. 985 (3-Jul-2025) by active ingredient; Art. 9 exempts some dosage forms (topicals, solutions) – topical TE flags are marked for confirmation. Sodium valproate is 'check' (Res. 985 lists divalproato #46 and valproato de magnesio #168).
- 'Controlled' follows UN 1961/1971 schedules (benzodiazepines, Z-drugs, opioids, phenobarbital, methylphenidate); pregabalin, modafinil, tofisopam, ephedrine/pseudoephedrine are 'likely' pending DNFD confirmation.
- Modi Lifecare catalogue is an image-only PDF and was transcribed by eye from 300-dpi renders (OCR as cross-check); PICS strengths split across lines were re-assembled by a layout parser and reviewed row by row. DE 16 OCR damage (numbers, '5'→'S', glued words, lost line breaks) was corrected manually for 61 renglones (column `ocr_corrected`).
- Landed costs (b2) exist for 18 items; 15 map to catalog SKUs with matched public demand (losartan 50 mg and atorvastatin 20 mg have no exact match in these acts; nystatin has a logistics adder only; metformin 850 mg is not in the catalogs). They are base-case estimates excluding registration, bioequivalence, QC testing, bonds and local distribution, so the GM column is a ceiling.

## QA – spot-check and error rate

- First pass: every DE 16 renglón with a catalog hit (59) and every matched centralized renglón (~180) was read by eye against the catalog item. **13 errors found (≈5%) and fixed**: (1) 'I.V. O GRANISETRON'/'I.M. O I.V.' parsed as oral route – ondansetron and tramadol injections read as oral liquids (DE16 #30 wrongly strength_diff); (2) OCR 'AVIBACTAMO.5G' hid avibactam – ceftazidime-avibactam (DE16 #54) wrongly strength_diff to ceftazidime; (3) 'cápsula o comprimido de liberación modificada' read as IR-or-MR – phenytoin MR (DE16 #148) wrongly exact to IR tablets (now review); (4) duloxetine gastro-resistant treated as a release mismatch (DE16 #120, LPU 11, CC 2024: molecule_only → strength_diff); (5) 'COMPRIMDO DISPERSABLE' typo – olanzapine ODT (DE16 #273) missed; (6) 'liberación convencional o con capa entérica' read as MR – diclofenac 50 mg (LPU 01 r136, CC 2023 r125) wrongly review; (7) four compra-conjunta winners mis-attributed by text similarity (cefotaxima @33.00, carbamazepina @4.76, diazepam @0.43, amlodipina @0.06 – none equal to any bid) – winner rule now requires same molecule/strength and a contracted price equal to a bid. Earlier, a regex bug that prevented all multi-word INN aliases from matching was caught in unit tests.
- Post-fix: two reproducible random samples of 40 matches each (seeds 20261006 and 777; 24 DE 16, 28 centralized, 28 decentralized lines – `spotcheck_sample_seed*.csv`) were reviewed by eye: **0/80 errors**.
- Cross-check: LPU 01-2026 India-origin award share (61/283, B/.7.05M, 9.0%; 16.8% ex top-2) reproduces the R2A sibling tabulation exactly; India-origin bids 147 vs R2A's 151 (free-text origin parsing).

## Files

- `catalog.csv` – deliverable 1
- `de16_matches.csv` – deliverable 2
- `centralized_matches.csv` – deliverable 3 (exact/strength_diff/review rows)
- `central_renglones_all.csv` – all centralized renglones with match level and value
- `central_bids_long.csv` – all centralized bids with origin/manufacturer
- `decentralized_matches.csv` – deliverable 4
- `decentralized_obs.csv` – decentralized observation level (traceability)
- `first_wave_demand.csv` – deliverable 6
- `sam_centralized_dedup.csv` – rows used in the de-duplicated centralized SAM
- `top_opportunities.csv` – full ranking behind section (c)
- `india_mfr_distributors.csv` – section (d) by act
- `res985_list.csv` – parsed Res. 985 list (173 entries)
- `spotcheck_sample_seed*.csv` – random match samples reviewed by eye