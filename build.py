import csv
import json
from pathlib import Path

here = Path(__file__).parent
rows = []
for r in list(csv.reader(open(here / "spend.csv")))[1:]:
    vals = [float(x) for x in r[1:]] + [0.0] * (6 - len(r[1:]))
    rows.append([r[0]] + vals)
rows.sort(key=lambda r: r[0])
html = (here / "template.html").read_text().replace("/*DATA*/[]", json.dumps(rows, separators=(",", ":")))
(here / "index.html").write_text(html)
print(f"built index.html with {len(rows)} days, last {rows[-1][0]}")
