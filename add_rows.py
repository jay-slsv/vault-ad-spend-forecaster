"""Append new daily rows to spend.csv and rebuild index.html.

Usage: python3 add_rows.py "2026-10-13,0,15000.12,120.5,174,4200.1,3100.9" ...
Each arg is date,meta,tiktok,asa,snapchat,liftoff,google (blank = 0). Existing dates are skipped.
"""
import subprocess
import sys
from pathlib import Path

here = Path(__file__).parent
csv_path = here / "spend.csv"
lines = csv_path.read_text().strip().split("\n")
have = {l.split(",")[0] for l in lines[1:]}
added = []
for arg in sys.argv[1:]:
    parts = [p.strip() for p in arg.split(",")]
    if len(parts) < 4 or parts[0] in have:
        continue
    parts += ["0"] * (7 - len(parts))
    parts = [parts[0]] + [str(float(p or 0)) for p in parts[1:7]]
    lines.append(",".join(parts))
    have.add(parts[0])
    added.append(parts[0])
lines = [lines[0]] + sorted(lines[1:])
csv_path.write_text("\n".join(lines) + "\n")
print("added:", added or "none")
subprocess.run([sys.executable, str(here / "build.py")], check=True)
