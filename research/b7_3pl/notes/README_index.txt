b7_3pl research folder (2026-10-05)
notes/facts_log.csv                 95 facts/estimates: id, unit, currency, date, exact URL, verification method
notes/cost_model_assumptions.csv    every model input (low/base/high) with basis code F/D/E and source ids
notes/cost_table.csv                5- and 15-pallet monthly cost table, 3PL vs own warehouse
notes/dnfd_3pl_hosts_2026-09-28.csv count of DNFD-licensed agencias hosted per logistics operator
notes/ocds_items_2019_2024.csv      PanamaCompra OCDS item-level hits (storage, rent, freight, cold chain, customs, racks)
notes/ocds_trips.csv                per-trip freight award items
notes/ocds_selected_records.txt     full records for public rental / customs / calibration contracts cited
scripts/                            ocds_scan.py, ocds_items.py, ocds_get.py, ocds_grep.py, ocds_trips.py, dnfd_hosts.py, cost_model.py
downloads/                          untrusted source files (PDF/HTML/JSONL) in per-source subfolders
Re-run model: python3 -I scripts/cost_model.py notes/
