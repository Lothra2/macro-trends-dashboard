"""
Fix regions to match v1 + add missing markets (Singapore, HK, Taiwan, Czech Republic, Romania)
Run: python fix_regions.py
"""
import json, os

DIR = os.path.dirname(os.path.abspath(__file__))
PATH = os.path.join(DIR, 'data', 'data.json')

# ── Region mapping to match v1 exactly ────────────────────────────────
REGIONS = {
    "US":"Americas","CA":"Americas",
    "BR":"LATAM","MX":"LATAM","AR":"LATAM","CO":"LATAM","CL":"LATAM",
    "PE":"LATAM","GT":"LATAM","CR":"LATAM","UY":"LATAM",
    "GB":"WE","DE":"WE","FR":"WE","IT":"WE","ES":"WE",
    "NL":"WE","SE":"WE","CH":"WE","BE":"WE",
    "PL":"EEMEA","TR":"EEMEA","RU":"EEMEA","SA":"EEMEA","AE":"EEMEA",
    "ZA":"EEMEA","KE":"EEMEA","EG":"EEMEA","NG":"EEMEA","PK":"EEMEA",
    "CZ":"EEMEA","RO":"EEMEA",
    "CN":"APAC","JP":"APAC","KR":"APAC","AU":"APAC","IN":"APAC",
    "ID":"APAC","TH":"APAC","MY":"APAC","VN":"APAC","PH":"APAC",
    "NZ":"APAC","BD":"APAC","SG":"APAC","HK":"APAC","TW":"APAC",
}

# ── New markets to add ─────────────────────────────────────────────────
NEW_MARKETS = [
  {
    "id":"SG","name":"Singapore","region":"APAC",
    "gdp_growth":2.2,"inflation":2.17,"population_m":5.9,"urbanization_pct":100.0,
    "gdp_pc_ppp":133000,"unemployment_pct":2.0,"ecommerce_pct":11.2,
    "big_mac_usd":5.38,"fmcg_signal":"Stable","current_account_pct":17.5,
    "median_age":43.0,"private_consumption_pct":36,"govt_debt_pct":171,
    "trade_openness_pct":320,"fdi_pct":22.0,"internet_pct":99,"mobile_per_100":155,
    "gini":37.4,"coke_price_usd":2.10,"big_mac_index_vs_us":-7,
    "retailer_insight":"Premium hub and regional FMCG HQ; ultra-high digital adoption with limited volume upside",
    "historical":{
      "gdp_growth":{"2018":3.7,"2019":0.7,"2020":-3.9,"2021":8.9,"2022":3.8,"2023":1.1,"2024":2.7,"2025":2.2},
      "inflation":{"2018":0.4,"2019":0.6,"2020":-0.2,"2021":2.3,"2022":6.1,"2023":4.8,"2024":2.4,"2025":2.17}
    }
  },
  {
    "id":"HK","name":"Hong Kong","region":"APAC",
    "gdp_growth":2.5,"inflation":1.60,"population_m":7.5,"urbanization_pct":100.0,
    "gdp_pc_ppp":69000,"unemployment_pct":3.0,"ecommerce_pct":42.0,
    "big_mac_usd":4.87,"fmcg_signal":"Stable","current_account_pct":6.5,
    "median_age":47.3,"private_consumption_pct":66,"govt_debt_pct":4,
    "trade_openness_pct":380,"fdi_pct":35.0,"internet_pct":94,"mobile_per_100":300,
    "gini":53.9,"coke_price_usd":2.50,"big_mac_index_vs_us":-16,
    "retailer_insight":"Aging premium market; high inequality masks strong top-tier FMCG demand in core urban corridors",
    "historical":{
      "gdp_growth":{"2018":2.8,"2019":-1.7,"2020":-6.5,"2021":6.4,"2022":-3.5,"2023":3.3,"2024":2.5,"2025":2.5},
      "inflation":{"2018":2.4,"2019":2.9,"2020":0.3,"2021":1.6,"2022":1.9,"2023":2.1,"2024":1.7,"2025":1.60}
    }
  },
  {
    "id":"TW","name":"Taiwan","region":"APAC",
    "gdp_growth":3.2,"inflation":2.10,"population_m":23.4,"urbanization_pct":79.8,
    "gdp_pc_ppp":72000,"unemployment_pct":3.5,"ecommerce_pct":30.0,
    "big_mac_usd":3.34,"fmcg_signal":"Stable","current_account_pct":14.1,
    "median_age":44.0,"private_consumption_pct":50,"govt_debt_pct":33,
    "trade_openness_pct":115,"fdi_pct":1.5,"internet_pct":90,"mobile_per_100":120,
    "gini":33.6,"coke_price_usd":1.60,"big_mac_index_vs_us":-42,
    "retailer_insight":"Mature tech-forward FMCG market; semiconductor boom driving premium consumer upgrade cycle",
    "historical":{
      "gdp_growth":{"2018":2.8,"2019":3.0,"2020":3.3,"2021":6.5,"2022":2.6,"2023":1.3,"2024":4.3,"2025":3.2},
      "inflation":{"2018":1.3,"2019":0.6,"2020":-0.2,"2021":2.0,"2022":3.0,"2023":2.5,"2024":2.2,"2025":2.10}
    }
  },
  {
    "id":"CZ","name":"Czech Republic","region":"EEMEA",
    "gdp_growth":1.0,"inflation":2.35,"population_m":10.9,"urbanization_pct":74.4,
    "gdp_pc_ppp":53000,"unemployment_pct":2.9,"ecommerce_pct":22.0,
    "big_mac_usd":4.81,"fmcg_signal":"Stable","current_account_pct":0.5,
    "median_age":44.0,"private_consumption_pct":50,"govt_debt_pct":44,
    "trade_openness_pct":155,"fdi_pct":2.5,"internet_pct":92,"mobile_per_100":130,
    "gini":26.0,"coke_price_usd":1.35,"big_mac_index_vs_us":-17,
    "retailer_insight":"Stable Central European market; high e-commerce penetration and value-conscious consumers",
    "historical":{
      "gdp_growth":{"2018":2.9,"2019":2.3,"2020":-5.6,"2021":3.6,"2022":2.4,"2023":0.0,"2024":1.3,"2025":1.0},
      "inflation":{"2018":2.0,"2019":2.8,"2020":3.2,"2021":3.8,"2022":15.1,"2023":10.7,"2024":2.5,"2025":2.35}
    }
  },
  {
    "id":"RO","name":"Romania","region":"EEMEA",
    "gdp_growth":2.5,"inflation":4.96,"population_m":18.6,"urbanization_pct":54.5,
    "gdp_pc_ppp":42000,"unemployment_pct":5.6,"ecommerce_pct":11.0,
    "big_mac_usd":3.92,"fmcg_signal":"Stable","current_account_pct":-6.5,
    "median_age":43.5,"private_consumption_pct":65,"govt_debt_pct":52,
    "trade_openness_pct":90,"fdi_pct":3.5,"internet_pct":88,"mobile_per_100":115,
    "gini":34.0,"coke_price_usd":1.20,"big_mac_index_vs_us":-32,
    "retailer_insight":"Emerging EU market with rising wages; modern trade expanding rapidly in urban centers",
    "historical":{
      "gdp_growth":{"2018":4.4,"2019":4.1,"2020":-3.7,"2021":5.8,"2022":4.6,"2023":2.1,"2024":0.8,"2025":2.5},
      "inflation":{"2018":4.6,"2019":3.8,"2020":2.6,"2021":5.0,"2022":13.8,"2023":10.4,"2024":5.8,"2025":4.96}
    }
  },
]

def main():
    with open(PATH,'r',encoding='utf-8-sig') as f:
        data = json.load(f)

    existing_ids = {m['id'] for m in data['markets']}

    # Add new markets
    added = 0
    for nm in NEW_MARKETS:
        if nm['id'] not in existing_ids:
            data['markets'].append(nm)
            added += 1
            print(f"  Added: {nm['name']} ({nm['id']})")

    # Fix regions for all markets
    updated = 0
    for m in data['markets']:
        new_r = REGIONS.get(m['id'])
        if new_r and m.get('region') != new_r:
            print(f"  Region: {m['name']} {m.get('region')} -> {new_r}")
            m['region'] = new_r
            updated += 1

    # Sort markets by region then name
    region_order = {'Americas':0,'LATAM':1,'WE':2,'EEMEA':3,'APAC':4}
    data['markets'].sort(key=lambda m: (region_order.get(m['region'],9), m['name']))

    data['metadata']['notes'].append(
        f"Regions aligned to v1 structure: Americas/LATAM/WE/EEMEA/APAC. "
        f"Added {added} markets: Singapore, Hong Kong, Taiwan, Czech Republic, Romania."
    )

    with open(PATH,'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',',':'))

    print(f"\nDone: {added} added, {updated} regions fixed. Total: {len(data['markets'])} markets.")

if __name__ == '__main__':
    main()
