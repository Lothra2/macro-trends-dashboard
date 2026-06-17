# Market Intelligence Hub

Static site package for publishing the three Market Intelligence Hub HTML dashboards.

## Pages

- `/macro-dashboard/` — Global FMCG Macro Dashboard
- `/historical-trends/` — Historical Macro Trends
- `/retailer-intelligence/` — Retailer Intelligence 2025

## Local preview

Run from the project root:

```bash
python -m http.server 8080
```

Open:

```text
http://localhost:8080
```

## Data files

The dashboards load data from:

- `data/data.js`
- `data/data.json`
- `data/macro_data.xlsx`

To regenerate the data files:

```bash
pip install openpyxl requests
python update_data.py
```

## Public hosting note

Do not publish real API keys in `config.js`. Any key inside browser JavaScript is visible to users. Keep `config.js` with placeholder keys for public hosting, or move AI calls behind a private backend before adding real keys.

## GitHub Pages

This project is ready for GitHub Pages. Publish the repository from the root folder and enable Pages from the `main` branch, root folder.

The `.nojekyll` file is included so GitHub Pages serves the static files exactly as uploaded.
