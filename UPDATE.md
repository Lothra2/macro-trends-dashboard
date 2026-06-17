# Data Update Instructions

## How to update all dashboard data

Tell Claude Code: **"actualiza los datos macro"** — Claude fetches fresh data from official sources and regenerates everything automatically.

### What gets updated
- `data/data.json` — raw JSON (primary data store)
- `data/data.js` — JavaScript module loaded by dashboards
- `data/macro_data.xlsx` — Excel file for manual review

### Manual update via script
```bash
python update_data.py
```
Requires: `pip install openpyxl requests`

### Data sources (official)
| Indicator | Source |
|---|---|
| GDP Growth / Inflation | IMF WEO (imf.org/en/publications/weo) |
| GDP per capita PPP | IMF WEO Database |
| Population | UN WPP (population.un.org) |
| Urbanization | UN WUP (population.un.org) |
| Unemployment | ILO ILOSTAT (ilostat.ilo.org) |
| Big Mac Price | The Economist Index |
| E-commerce % | Euromonitor / regional reports |
| Current Account | IMF / TheGlobalEconomy.com |

### API Key setup (config.js)
Edit `config.js` and replace `YOUR_GROK_API_KEY_HERE` with your x.ai API key.
To use GPT-5 instead, enter the key in the Settings panel within the Retailer Intelligence dashboard.
