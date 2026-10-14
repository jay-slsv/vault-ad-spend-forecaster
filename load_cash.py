"""Load daily cash columns (cash in, withdrawals, inventory) into spend.csv and rebuild.

Usage: python3 load_cash.py path/to/netcash.json
The JSON is a list of {day, card, deposits, withdrawals, inventory} rows (Toronto days) from the
analytics replica. Only days that already have a spend row are written, so a cash day never
appears on the page without its spend.
"""
import json
import subprocess
import sys

import store

here = store.here
data = json.load(open(sys.argv[1]))
rows = store.load()
updated, skipped = [], []
for r in data:
    row = rows.get(r["day"])
    if row is None:
        skipped.append(r["day"])
        continue
    new = [
        store.num(float(r["card"] or 0) + float(r["deposits"] or 0)),
        store.num(r["withdrawals"]),
        store.num(r["inventory"]),
    ]
    if row[9:12] != new:
        updated.append(r["day"])
    row[9:12] = new
store.save(rows)
print("cash updated:", len(updated), "last:", updated[-1] if updated else "none")
print("skipped (no spend row yet):", skipped)
subprocess.run([sys.executable, str(here / "build.py")], check=True)
