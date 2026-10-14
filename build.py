import json

import store

here = store.here
rows = []
for date, r in sorted(store.load().items()):
    spend = [float(x or 0) for x in r[1:9]]
    cash = [float(x) if x != "" else None for x in r[9:14]]
    rows.append([date] + spend + cash)
html = (here / "template.html").read_text().replace("/*DATA*/[]", json.dumps(rows, separators=(",", ":")))
(here / "index.html").write_text(html)
print(f"built index.html with {len(rows)} days, last {rows[-1][0]}")
