"""Shared reader/writer for spend.csv.

Columns: date, 8 spend channels, then 5 cash columns that mirror admin's Net Cash After Marketing:
cashin (card payments + wallet top-ups), withdrawals, shipped (shipped card cost),
fees (payment processor fees), ugc (UGC marketing).
Cash columns are blank for days that have no cash data yet.
"""
import csv
from pathlib import Path

here = Path(__file__).parent
CSV = here / "spend.csv"
NCOLS = 14
HEADER = [
    "date", "meta", "tiktok", "asa", "snapchat", "liftoff", "google", "point2web", "winklelab",
    "cashin", "withdrawals", "shipped", "fees", "ugc",
]


def load():
    rows = {}
    for r in list(csv.reader(open(CSV)))[1:]:
        r = r + [""] * (NCOLS - len(r))
        rows[r[0]] = r[:NCOLS]
    return rows


def save(rows):
    w = csv.writer(open(CSV, "w", newline=""))
    w.writerow(HEADER)
    for k in sorted(rows):
        w.writerow(rows[k])


def num(x):
    return str(round(float(x or 0), 2))
