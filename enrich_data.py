"""
Market Intelligence Hub — Data Enrichment Script
Adds extended KPIs and historical data to data.json
Run: python enrich_data.py
"""
import json, os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR   = os.path.join(SCRIPT_DIR, 'data')
JSON_IN    = os.path.join(DATA_DIR, 'data.json')
JSON_OUT   = os.path.join(DATA_DIR, 'data.json')

# ── EXTENDED KPIs per market (keyed by market id) ─────────────────────
EXTENDED = {
  # id : (median_age, priv_consump_pct, govt_debt_pct, trade_openness_pct,
  #        fdi_pct, internet_pct, mobile_per_100, gini, coke_usd, bm_index_vs_us_pct, retailer_insight)
  "CN": (39.5,38,86,38,  1.0,78,121,38.5,1.05,-39,"Platform commerce dominates; premium tier expanding in Tier 1-2 cities"),
  "JP": (49.1,55,254,41, 0.5,93,162,32.9,2.15,-46,"Aging premium market; convenience channel drives frequency over basket size"),
  "KR": (44.5,50,55,82,  0.8,97,140,31.4,1.85,-34,"Ultra-high digital penetration; K-beauty and health driving premiumization"),
  "AU": (38.7,53,43,47,  2.5,96,118,34.4,2.20,-16,"Post-inflationary normalization; private label growing, discretionary under pressure"),
  "IN": (28.9,60,86,47,  1.5,52,85,35.7,1.00,-55,"Fastest consumer market expansion; rural distribution breakthrough opportunity"),
  "ID": (30.2,57,39,39,  2.2,73,128,37.9,1.15,-56,"Young consumer base fueling FMCG volume; modern trade penetration accelerating"),
  "TH": (40.1,51,60,107, 2.0,89,183,43.3,1.25,-31,"Tourism recovery supporting premium; domestic consumption stable at low growth"),
  "MY": (30.2,58,61,142, 4.5,97,141,41.2,1.10,-48,"Digital-savvy middle class; halal certification drives premium differentiation"),
  "VN": (32.5,66,38,185, 4.5,79,146,35.7,0.95,-48,"High-velocity growth market; urbanization and income gains expanding addressable market"),
  "PH": (25.7,74,60,55,  2.1,73,138,42.3,0.90,-50,"Young archipelago market; sari-sari channel dominant outside Metro Manila"),
  "NZ": (38.2,57,47,58,  2.0,98,130,33.9,2.30,-18,"Mild contraction; consumer confidence recovering but premiumization stalled"),
  "PK": (20.4,83,75,30,  0.8,40,80,29.6,0.85,-35,"Post-crisis demand recovery; inflation normalization helping basket reconstruction"),
  "BD": (27.9,69,40,37,  0.6,42,103,33.4,0.75,None,"High inflation compressing margins; value tiers gaining at expense of mid-range"),
  "GB": (40.5,62,102,64, 2.8,98,119,35.1,2.80,-1,"Post-cost-crisis stability; discounters locked in gains, premium showing resilience"),
  "DE": (46.8,52,64,88,  1.5,93,133,31.7,1.95,-9,"Structural contraction; consumers anchored in value, discounters at record share"),
  "FR": (42.3,54,111,72, 3.0,94,112,32.4,1.90,-9,"Slow growth; private label at record high, brand loyalty under sustained pressure"),
  "IT": (47.3,59,139,63, 1.8,91,133,34.8,1.80,-12,"Stagnation with tourism upside; north-south consumption divide widening"),
  "ES": (44.9,57,105,68, 3.5,96,117,33.9,1.65,-12,"Outperforming eurozone; tourism-linked categories driving above-trend growth"),
  "NL": (43.0,46,46,152, 5.0,98,121,28.2,2.00,-12,"Stable, high-income market; sustainability premiums holding despite inflation legacy"),
  "PL": (42.0,58,53,120, 3.0,91,148,30.2,1.40,-10,"Post-inflation rebound; Central European hub driving volume growth"),
  "SE": (41.2,46,32,89,  2.5,97,128,29.3,2.35,-2,"Credit-constrained consumers; housing correction weighing on discretionary"),
  "TR": (33.5,57,29,62,  1.5,82,96,41.9,2.50,-8,"Inflation normalizing but consumer trust fragile; value-seeking entrenched"),
  "RU": (40.3,52,19,47, -1.0,89,163,36.0,1.20,-61,"Isolated market; import substitution reshaping category mix, local brands gaining"),
  "US": (38.9,68,122,27, 2.0,96,122,39.4,2.20,0,"Bifurcated recovery; premium and value growing, squeezed middle tier losing share"),
  "CA": (41.7,56,107,65, 3.5,94,91,33.3,2.10,-6,"Immigration-driven demand growth offsetting per-capita consumption softness"),
  "BR": (34.7,64,89,37,  3.5,84,103,52.9,1.50,-30,"Volume recovery led by Northeast; food inflation moderating, basket rebuilding"),
  "MX": (30.0,67,51,79,  2.5,81,95,45.4,1.30,-21,"US trade uncertainty clouding outlook; domestic consumption holding on remittances"),
  "AR": (32.4,64,60,37,  2.0,87,130,40.7,1.80,20,"Stabilization after hyperinflation peak; consumers rebuilding basket cautiously"),
  "CO": (31.1,71,57,38,  3.5,73,130,51.5,1.70,-11,"Urban recovery underway; rural channels returning after political-risk discount"),
  "CL": (36.7,64,36,58,  5.0,90,138,44.9,1.60,-22,"Steady state; constrained by high household debt, premiumization selective"),
  "PE": (30.5,64,33,53,  2.5,74,142,41.7,1.55,-22,"Political uncertainty discount; commodity-linked economy stabilizing"),
  "GT": (22.0,82,29,66,  1.5,60,120,48.3,1.20,-31,"Remittance-fueled growth; value channels dominant, modern trade underpenetrated"),
  "CR": (34.2,67,63,86,  4.0,85,179,47.2,1.75,2,"Strong growth with high urbanization; digital commerce gaining rapidly"),
  "UY": (36.5,71,62,50,  2.5,88,161,40.6,2.00,19,"Small premium market; high wages support branded goods consumption"),
  "SA": (30.2,42,26,71,  3.5,100,129,45.9,1.60,-12,"Vision 2030 driving modern retail investment; tourism and entertainment lifting categories"),
  "AE": (34.0,35,30,189, 4.0,100,200,32.5,1.80,-15,"Hyper-connected premium hub; tourism and expat population driving mixed-basket growth"),
  "ZA": (28.1,61,75,62,  1.5,74,160,63.0,1.25,-52,"Structural unemployment prevents mass-market recovery; top quintile holding volume"),
  "KE": (20.1,78,68,44,  1.5,43,137,38.7,1.00,None,"Growing urban middle class; M-Pesa-enabled commerce reshaping distribution"),
  "EG": (25.5,82,95,40,  2.0,75,105,31.9,0.85,-54,"Currency normalization helping import categories; affordability remains key constraint"),
  "NG": (18.1,71,38,38,  0.5,55,90,35.1,0.70,None,"Inflation eroding real consumption; informal trade dominant, pricing power limited"),
  "CH": (43.0,52,17,120, 3.0,97,131,33.1,3.50,38,"Highest Big Mac in world; stable premium market with CHF strength advantage"),
  "BE": (41.7,54,106,185, 8.0,96,112,25.0,2.10,-9,"Dense market with pan-European logistics hub; promotion-sensitive consumer base"),
}

# ── EXTENDED HISTORICAL (add 2018–2021 for GDP growth + inflation) ─────
# Format: {id: {gdp:{2018:x,...}, inflation:{2018:x,...}}}
HISTORICAL_EXT = {
  "CN": {"gdp":{"2018":6.7,"2019":6.0,"2020":2.2,"2021":8.4},"inf":{"2018":2.1,"2019":2.9,"2020":2.5,"2021":0.9}},
  "JP": {"gdp":{"2018":0.6,"2019":-0.4,"2020":-4.3,"2021":2.1},"inf":{"2018":1.0,"2019":0.5,"2020":0.0,"2021":-0.2}},
  "KR": {"gdp":{"2018":2.9,"2019":2.2,"2020":-0.7,"2021":4.3},"inf":{"2018":1.5,"2019":0.4,"2020":0.5,"2021":2.5}},
  "AU": {"gdp":{"2018":2.8,"2019":1.9,"2020":-2.2,"2021":5.2},"inf":{"2018":2.0,"2019":1.6,"2020":0.9,"2021":2.8}},
  "IN": {"gdp":{"2018":6.5,"2019":6.5,"2020":-5.8,"2021":9.1},"inf":{"2018":3.9,"2019":3.7,"2020":6.2,"2021":5.5}},
  "ID": {"gdp":{"2018":5.2,"2019":5.0,"2020":-2.1,"2021":3.7},"inf":{"2018":3.2,"2019":2.8,"2020":2.0,"2021":1.6}},
  "TH": {"gdp":{"2018":4.1,"2019":2.4,"2020":-6.1,"2021":1.5},"inf":{"2018":1.1,"2019":0.7,"2020":-0.8,"2021":1.2}},
  "MY": {"gdp":{"2018":4.7,"2019":4.3,"2020":-5.6,"2021":3.1},"inf":{"2018":1.0,"2019":0.7,"2020":-1.1,"2021":2.5}},
  "VN": {"gdp":{"2018":7.1,"2019":7.0,"2020":2.9,"2021":2.6},"inf":{"2018":3.5,"2019":2.8,"2020":3.2,"2021":1.8}},
  "PH": {"gdp":{"2018":6.3,"2019":6.1,"2020":-9.5,"2021":5.7},"inf":{"2018":5.2,"2019":2.5,"2020":2.6,"2021":3.9}},
  "NZ": {"gdp":{"2018":3.2,"2019":2.4,"2020":-2.1,"2021":5.6},"inf":{"2018":1.6,"2019":1.6,"2020":1.7,"2021":3.9}},
  "PK": {"gdp":{"2018":5.5,"2019":3.1,"2020":-0.5,"2021":5.7},"inf":{"2018":4.7,"2019":10.6,"2020":10.7,"2021":8.9}},
  "BD": {"gdp":{"2018":7.9,"2019":8.2,"2020":3.5,"2021":6.9},"inf":{"2018":5.8,"2019":5.5,"2020":5.7,"2021":5.6}},
  "GB": {"gdp":{"2018":1.7,"2019":1.7,"2020":-11.0,"2021":7.5},"inf":{"2018":2.5,"2019":1.8,"2020":0.9,"2021":2.6}},
  "DE": {"gdp":{"2018":1.5,"2019":1.1,"2020":-4.6,"2021":2.9},"inf":{"2018":1.9,"2019":1.4,"2020":0.4,"2021":3.2}},
  "FR": {"gdp":{"2018":1.8,"2019":1.9,"2020":-7.9,"2021":6.8},"inf":{"2018":2.1,"2019":1.3,"2020":0.5,"2021":2.1}},
  "IT": {"gdp":{"2018":0.9,"2019":0.5,"2020":-9.0,"2021":7.0},"inf":{"2018":1.2,"2019":0.6,"2020":-0.1,"2021":1.9}},
  "ES": {"gdp":{"2018":2.4,"2019":2.0,"2020":-11.3,"2021":5.5},"inf":{"2018":1.7,"2019":0.8,"2020":-0.3,"2021":3.0}},
  "NL": {"gdp":{"2018":2.4,"2019":2.0,"2020":-3.9,"2021":4.9},"inf":{"2018":1.7,"2019":2.7,"2020":1.1,"2021":2.7}},
  "PL": {"gdp":{"2018":5.1,"2019":4.5,"2020":-2.0,"2021":5.9},"inf":{"2018":1.8,"2019":2.3,"2020":3.4,"2021":5.2}},
  "SE": {"gdp":{"2018":2.0,"2019":2.0,"2020":-2.8,"2021":5.1},"inf":{"2018":2.0,"2019":1.7,"2020":0.5,"2021":2.7}},
  "TR": {"gdp":{"2018":3.0,"2019":0.9,"2020":1.8,"2021":11.4},"inf":{"2018":16.3,"2019":15.2,"2020":12.3,"2021":19.6}},
  "RU": {"gdp":{"2018":2.8,"2019":2.2,"2020":-2.7,"2021":5.6},"inf":{"2018":2.9,"2019":4.5,"2020":3.4,"2021":6.7}},
  "US": {"gdp":{"2018":3.0,"2019":2.5,"2020":-2.8,"2021":5.9},"inf":{"2018":2.4,"2019":1.8,"2020":1.2,"2021":4.7}},
  "CA": {"gdp":{"2018":2.4,"2019":1.9,"2020":-5.1,"2021":5.0},"inf":{"2018":2.3,"2019":1.9,"2020":0.7,"2021":3.4}},
  "BR": {"gdp":{"2018":1.8,"2019":1.2,"2020":-3.3,"2021":5.0},"inf":{"2018":3.7,"2019":3.7,"2020":3.2,"2021":8.3}},
  "MX": {"gdp":{"2018":2.2,"2019":-0.2,"2020":-8.3,"2021":4.9},"inf":{"2018":4.9,"2019":3.6,"2020":3.4,"2021":5.7}},
  "AR": {"gdp":{"2018":-2.6,"2019":-2.0,"2020":-9.9,"2021":10.4},"inf":{"2018":34.3,"2019":53.5,"2020":42.0,"2021":48.4}},
  "CO": {"gdp":{"2018":2.6,"2019":3.3,"2020":-7.0,"2021":10.6},"inf":{"2018":3.2,"2019":3.5,"2020":1.6,"2021":3.5}},
  "CL": {"gdp":{"2018":3.9,"2019":1.1,"2020":-6.1,"2021":11.7},"inf":{"2018":2.4,"2019":2.3,"2020":3.0,"2021":4.5}},
  "PE": {"gdp":{"2018":4.0,"2019":2.2,"2020":-11.0,"2021":13.3},"inf":{"2018":1.3,"2019":2.1,"2020":1.8,"2021":4.0}},
  "GT": {"gdp":{"2018":3.1,"2019":3.8,"2020":0.5,"2021":8.0},"inf":{"2018":3.8,"2019":3.8,"2020":3.2,"2021":4.3}},
  "CR": {"gdp":{"2018":2.7,"2019":2.3,"2020":-4.1,"2021":7.8},"inf":{"2018":2.2,"2019":2.1,"2020":0.7,"2021":3.3}},
  "UY": {"gdp":{"2018":1.5,"2019":0.4,"2020":-7.2,"2021":5.3},"inf":{"2018":7.6,"2019":7.9,"2020":9.8,"2021":7.7}},
  "SA": {"gdp":{"2018":2.4,"2019":0.3,"2020":-4.1,"2021":3.2},"inf":{"2018":2.5,"2019":-2.1,"2020":3.4,"2021":3.1}},
  "AE": {"gdp":{"2018":1.3,"2019":1.1,"2020":-6.1,"2021":4.2},"inf":{"2018":3.1,"2019":-1.9,"2020":-2.1,"2021":0.2}},
  "ZA": {"gdp":{"2018":0.8,"2019":0.1,"2020":-6.3,"2021":4.9},"inf":{"2018":4.6,"2019":4.1,"2020":3.3,"2021":4.5}},
  "KE": {"gdp":{"2018":6.3,"2019":5.4,"2020":-0.3,"2021":7.6},"inf":{"2018":4.7,"2019":5.2,"2020":5.3,"2021":6.1}},
  "EG": {"gdp":{"2018":5.3,"2019":5.6,"2020":3.6,"2021":3.3},"inf":{"2018":20.9,"2019":13.9,"2020":5.7,"2021":4.5}},
  "NG": {"gdp":{"2018":1.9,"2019":2.2,"2020":-1.8,"2021":3.4},"inf":{"2018":12.1,"2019":11.4,"2020":13.2,"2021":17.0}},
  "CH": {"gdp":{"2018":3.0,"2019":1.2,"2020":-2.5,"2021":5.4},"inf":{"2018":0.9,"2019":0.4,"2020":-0.7,"2021":0.6}},
  "BE": {"gdp":{"2018":1.5,"2019":1.7,"2020":-5.7,"2021":6.3},"inf":{"2018":2.3,"2019":1.4,"2020":0.4,"2021":3.2}},
}

def main():
    with open(JSON_IN,'r',encoding='utf-8-sig') as f:
        data = json.load(f)

    for m in data['markets']:
        mid = m['id']
        ext = EXTENDED.get(mid)
        if ext:
            (median_age, priv_c, govt_d, trade_op, fdi,
             internet, mobile, gini, coke, bm_idx, insight) = ext
            m['median_age']             = median_age
            m['private_consumption_pct'] = priv_c
            m['govt_debt_pct']           = govt_d
            m['trade_openness_pct']      = trade_op
            m['fdi_pct']                 = fdi
            m['internet_pct']            = internet
            m['mobile_per_100']          = mobile
            m['gini']                    = gini
            m['coke_price_usd']          = coke
            m['big_mac_index_vs_us']     = bm_idx   # None if no McDonald's
            m['retailer_insight']        = insight

        hext = HISTORICAL_EXT.get(mid, {})
        if hext and 'historical' in m:
            existing_gdp = m['historical'].get('gdp_growth', {})
            existing_inf = m['historical'].get('inflation', {})
            merged_gdp = {**hext.get('gdp',{}), **existing_gdp}
            merged_inf = {**hext.get('inf',{}), **existing_inf}
            m['historical']['gdp_growth'] = dict(sorted(merged_gdp.items()))
            m['historical']['inflation']  = dict(sorted(merged_inf.items()))

    # Update metadata notes
    data['metadata']['notes'].append(
        "Extended KPIs added 2026-05-14: median_age (UN WPP 2024), private_consumption_pct (World Bank), "
        "govt_debt_pct (IMF), trade_openness_pct (World Bank), fdi_pct (UNCTAD), internet_pct (ITU), "
        "mobile_per_100 (ITU/GSMA), gini (World Bank latest), coke_price_usd (Numbeo 2025), "
        "big_mac_index_vs_us (The Economist Jan 2025), retailer_insight (analyst synthesis)"
    )
    data['metadata']['notes'].append(
        "Historical data extended to 2018-2025 for GDP growth and inflation"
    )

    with open(JSON_OUT,'w',encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, separators=(',',':'))

    print(f"Enriched {len(data['markets'])} markets with extended KPIs and historical data (2018-2025)")

if __name__ == '__main__':
    main()
