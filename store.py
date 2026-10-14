"""Shared reader/writer for spend.csv.

Columns: date, 8 spend channels, then cashin (card + wallet top-ups), withdrawals, inventory.
Cash columns are blank for days that have no cash data yet.
"""
import csv
from pathlib import Path

here = Path(__file__).parent
CSV = here / "spend.csv"
HEADER = [
    "date", "meta", "tiktok", "asa", "snapchat", "liftoff", "google", "point2web", "winklelab",
    "cashin", "withdrawals", "inventory",
]


def load():
    rows = {}
    for r in list(csv.reader(open(CSV)))[1:]:
        r = r + [""] * (12 - len(r))
        rows[r[0]] = r[:12]
    return rows


def save(rows):
    w = csv.writer(open(CSV, "w", newline=""))
    w.writerow(HEADER)
    for k in sorted(rows):
        w.writerow(rows[k])


def num(x):
    return str(round(float(x or 0), 2))
