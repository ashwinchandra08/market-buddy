# Market Buddy 📈🐾

[![ci](https://github.com/ashwinchandra08/market-buddy/actions/workflows/ci.yml/badge.svg)](https://github.com/ashwinchandra08/market-buddy/actions/workflows/ci.yml)
[![license: MIT](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

A daily **India + US market dashboard** for an e-ink Kindle (built for a jailbroken **Paperwhite 3, FW 5.16.2.1.1**),
with a Pokémon whose mood follows the market – five moods from *very happy* to *scary*.

```
GitHub Actions (cron) ─ yfinance ─► mood score ─► Pillow (1072×1448 grayscale PNG) ─► GitHub Pages
                                                                                         │ HTTPS
Kindle (plugged in) ◄─ KUAL script: curl meta.txt → curl dash.png → fbink paint ◄───────┘
```

Shows: Nifty 50, Sensex, Bank Nifty, S&P 500, Nasdaq, Dow (each with a *today* and a *5-day* sparkline),
plus USD/INR, Brent, gold, India VIX and the US 10-year yield. Open/closed badges for both markets.

## Quick start

### 1. Put it on GitHub
```bash
git init -b main
git add .
git commit -m "Initial commit"
# create an empty PUBLIC repo named market-buddy on github.com (no README/license), then:
git remote add origin https://github.com/<you>/market-buddy.git
git push -u origin main
```
Then on GitHub:
1. **Settings → Pages → Build and deployment → Source: GitHub Actions**
2. **Actions → render-dashboard → Run workflow**
3. Open `https://<you>.github.io/market-buddy/` – your dashboard should appear.

Replace `YOUR_USER` in this README's badges, and the name in `LICENSE` if you want your own copyright line.

### 2. Preview locally (no network needed)
```bash
pip install -r requirements.txt -r requirements-dev.txt
python -m src.main --mock --bias 0.9        # happy day  -> site/dash.png
python -m src.main --mock --bias -1.5       # scary day
python -m src.main --mock --force-tier 3    # force any mood 0..4
python -m pytest -q
```
Real data: `python -m src.main` (yfinance, needs internet).

### 3. Set up the Kindle
See **[kindle/marketbuddy/README.md](kindle/marketbuddy/README.md)** – it lists the three files you must add
yourself (`fbink`, `curl`, `cacert.pem`) and **how to exit back to the normal Kindle UI**.

## Configuration (`config.yaml`)
Indices, macro strip, mood thresholds, and which Pokémon (PokeAPI ids) appear for each mood.
Nothing is hard-coded to a particular person's holdings.

### Mood rules
Blended score = 50 % Nifty 50 % change + 50 % S&P 500 % change (uses whichever is available).
`≥ +1.0` very happy · `≥ +0.25` happy · `≥ −0.25` calm · `> −1.0` worried · otherwise scary.
A volatility spike (India VIX or VIX up ≥ 8 %) lowers the mood one tier.
The page is always light-themed (best for e-ink).

## Project layout
```
src/            fetch, mood, render, sprites, fallback mascot, mock data
tests/          pytest
.github/        render (cron → Pages), ci, keepalive, issue template
kindle/         KUAL extension (shell scripts) + Kindle-side README
```

## Limitations
- **Kindle scripts are untested on real hardware by the scaffold's author**; the renderer, mood logic and workflow
  are tested with mock data. Use *Self-check* and *Test* first and read `marketbuddy.log`.
- yfinance is unofficial: it may break or rate-limit. Failed symbols fall back to the last good value (marked `*`).
- Open/closed badges use regular trading hours + data freshness (handles holidays); not an official calendar.
- A Kindle that is always plugged in can wear its battery; keep it near 80 % if you can.

## Legal
MIT licensed (see [LICENSE](LICENSE)). Pokémon is © Nintendo / Creatures / GAME FREAK; this project is unofficial and
does not distribute artwork – see [NOTICE.md](NOTICE.md). Market data is informational only, **not investment advice**.

## Contributing
See [CONTRIBUTING.md](CONTRIBUTING.md). Issues and PRs welcome.
