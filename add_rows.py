"""Upsert daily rows into spend.csv and rebuild index.html.

Usage: python3 add_rows.py "2026-10-13,0,15000.12,120.5,174,4200.1,3100.9,60,75" ...
Each arg is date,meta,tiktok,asa,snapchat,liftoff,google,point2web,winklelab (blank = 0).
Existing dates are REPLACED, so restated values and Winkle Lab estimates self-correct.
"""
import subprocess
import sys
from pathlib import Path

here = Path(__file__).parent
csv_path = here / "spend.csv"
lines = csv_path.read_text().strip().split("\n")
by_date = {l.split(",")[0]: l for l in lines[1:]}
changed = []
for arg in sys.argv[1:]:
    parts = [p.strip() for p in arg.split(",")]
    if len(parts) < 4:
        continue
    parts += ["0"] * (9 - len(parts))
    parts = [parts[0]] + [str(float(p or 0)) for p in parts[1:9]]
    new = ",".join(parts)
    if by_date.get(parts[0]) != new:
        changed.append(parts[0])
    by_date[parts[0]] = new
lines = [lines[0]] + [by_date[k] for k in sorted(by_date)]
csv_path.write_text("\n".join(lines) + "\n")
print("added or updated:", changed or "none")
subprocess.run([sys.executable, str(here / "build.py")], check=True)
