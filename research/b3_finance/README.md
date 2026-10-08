# b3_finance — research workspace (2026-10-05)

Scope: cash cycle, financing costs, bonds and taxes for a supplier selling imported generic medicines to MINSA / CSS / hospital patronatos (Panama).

## Notes (read in this order)
- notes/05_parameter_table.md — model parameters (low/base/high) with source type (F = fact from opened source, E = estimate)
- notes/01_payment_times.md — actual payment times: Aredis/CSS debts 2023, MINSA payables 2024, MEF payables Mar-2026, Contraloría refrendo times 2025–2026, DPO proxy
- notes/02_legal_payment_and_bonds.md — Ley 22 (Texto Único 2020) + DE 439/2020 + DE 27/2024 + Contraloría Decreto 21-LEG/2018: payment term, moratory interest, cesión de crédito, bonds, penalties, insurer underwriting requirements
- notes/03_financing.md — SBP official rate files (1072-A reference rate, credit rates), FECI, factoring market (Balboa Factoring audited FS 2025), Banco General tariff (L/C, guarantees, overdrafts)
- notes/04_taxes.md — ISR 25% & CAIR, dividend/complementario, Aviso de Operación, Tasa Única, municipal, ITBMS (medicine exemption + exporter-assimilated rule), CSS & labor on-costs

## Downloads (untrusted; each in its own folder with url.txt)
downloads/<name>/{doc.pdf|page.html|raw, page.txt, url.txt}; SBP Excel files in downloads/sbp_xlsx_*/.
Scripts used: scripts/fetch.sh, scripts/html2txt.py, scripts/dump_xlsx.py (run with python3 -I).

## Access limits respected
- Gaceta Oficial pdfTemp links returned error pages (not retried beyond once).
- CSS transparency portal (403 to curl; WebFetch permission not granted) — not read.
- MITRADEL site 403; UMECIT article behind bot challenge — skipped.
- PanamaCompra robots.txt disallows crawling beyond home — not crawled.
- WebSearch budget for the turn exhausted mid-research; later sources were reached only by navigating known primary sites/sitemaps.
