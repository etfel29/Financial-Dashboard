# Financial Dashboard

A live financial dashboard hosted on GitHub Pages, auto-updated every weekday after market close via GitHub Actions.

## What it tracks
- **S&P 500, NASDAQ 100, NYSE Composite** — price, daily change, YTD return
- **VIX** — volatility index with level indicator
- **LEI** — Conference Board Leading Economic Index (updated monthly)
- **Unemployment rate** — latest BLS figure (updated monthly)
- **Magnificent 7** — AAPL, MSFT, NVDA, GOOGL, AMZN, META, TSLA prices and YTD returns

## How it works
1. GitHub Actions runs `fetch_data.py` every weekday at 5:30 PM ET
2. The script uses `yfinance` to pull live quotes and injects them into `index.html`
3. The updated file is committed and pushed automatically
4. GitHub Pages serves the result at your Pages URL

## Updating year-start prices
Each January 1st, update the `YEAR_START` dictionary in `fetch_data.py` with the Dec 31 closing prices for accurate YTD calculations.

## Manual trigger
Go to **Actions → Update Dashboard → Run workflow** to refresh data on demand.
