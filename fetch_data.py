#!/usr/bin/env python3
"""
fetch_data.py
Fetches live market data via yfinance and injects it into index.html
as a window.DASHBOARD_DATA object.
"""

import json
import re
import sys
from datetime import datetime, timezone
import yfinance as yf

TICKERS = {
    "sp500": "^GSPC",
    "ndx":   "^NDX",
    "nya":   "^NYA",
    "vix":   "^VIX",
}

MAG7 = [
    ("AAPL",  "Apple"),
    ("MSFT",  "Microsoft"),
    ("NVDA",  "Nvidia"),
    ("GOOGL", "Alphabet"),
    ("AMZN",  "Amazon"),
    ("META",  "Meta"),
    ("TSLA",  "Tesla"),
]

# Year-start prices for YTD calc (Dec 31 2025 closes — update each Jan 1)
YEAR_START = {
    "^GSPC": 5881.63,
    "^NDX":  21021.43,
    "^NYA":  20169.00,
    "AAPL":  243.01,
    "MSFT":  420.87,
    "NVDA":  134.25,
    "GOOGL": 191.88,
    "AMZN":  224.95,
    "META":  589.34,
    "TSLA":  403.84,
}


def fetch_quote(symbol):
    t = yf.Ticker(symbol)
    info = t.fast_info
    price     = info.last_price
    prev      = info.previous_close
    day_chg   = price - prev
    day_pct   = (day_chg / prev) * 100 if prev else 0
    yr_start  = YEAR_START.get(symbol)
    ytd_pct   = ((price - yr_start) / yr_start) * 100 if yr_start else 0
    return {
        "price":      round(price, 2),
        "day_change": round(day_chg, 2),
        "day_pct":    round(day_pct, 2),
        "ytd_pct":    round(ytd_pct, 2),
    }


def build_data():
    data = {}
    for key, sym in TICKERS.items():
        print(f"  Fetching {sym}...", file=sys.stderr)
        data[key] = fetch_quote(sym)

    mag7 = []
    for ticker, name in MAG7:
        print(f"  Fetching {ticker}...", file=sys.stderr)
        q = fetch_quote(ticker)
        mag7.append({"ticker": ticker, "name": name, **q})
    data["mag7"] = mag7

    now = datetime.now(timezone.utc)
    data["as_of"] = now.strftime("%-d %b %Y, %H:%M UTC")
    return data


def inject(data, html_path="index.html"):
    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    json_blob = json.dumps(data, indent=2)
    script_tag = f"<script>\n  window.DASHBOARD_DATA = {json_blob};\n</script>"

    # Replace existing injected block or insert before closing </body>
    pattern = r"<script>\s*window\.DASHBOARD_DATA\s*=[\s\S]*?</script>"
    if re.search(pattern, html):
        html = re.sub(pattern, script_tag, html)
    else:
        html = html.replace("</body>", script_tag + "\n</body>")

    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"  Injected data into {html_path}", file=sys.stderr)


if __name__ == "__main__":
    print("Fetching market data...", file=sys.stderr)
    data = build_data()
    inject(data)
    print("Done.", file=sys.stderr)
