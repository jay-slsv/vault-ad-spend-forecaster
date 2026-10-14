"""Upsert daily SPEND rows into spend.csv and rebuild index.html.

Usage: python3 add_rows.py "2026-10-13,meta,tiktok,asa,snapchat,liftoff,google,point2web,winklelab" ...
Blank = 0. Existing dates are REPLACED (spend columns only; cash columns are kept), so restated
values and Winkle Lab estimates self-correct. Cash columns are loaded separately by load_cash.py.
"""
import subprocess
import sys

import store

here = store.here
rows = store.load()
changed = []
for arg in sys.argv[1:]:
    parts = [p.strip() for p in arg.split(",")]
    if len(parts) < 4:
        continue
    parts += ["0"] * (9 - len(parts))
    spend = [store.num(p) for p in parts[1:9]]
    row = rows.get(parts[0]) or [parts[0]] + [""] * (store.NCOLS - 1)
    if row[1:9] != spend:
        changed.append(parts[0])
    row[1:9] = spend
    rows[parts[0]] = row
store.save(rows)
print("added or updated:", changed or "none")
subprocess.run([sys.executable, str(here / "build.py")], check=True)
