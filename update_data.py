"""
Market Intelligence Hub — Data Update Script
Run: python update_data.py
Requires: pip install openpyxl requests

Updates data.json and data.js from data/data.json (or fetches fresh data).
Generates macro_data.xlsx from the JSON.
"""
import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, 'data')
JSON_PATH = os.path.join(DATA_DIR, 'data.json')
JS_PATH = os.path.join(DATA_DIR, 'data.js')
XLSX_PATH = os.path.join(DATA_DIR, 'macro_data.xlsx')


def load_data():
    with open(JSON_PATH, 'r', encoding='utf-8-sig') as f:
        return json.load(f)


def write_js(data):
    js_content = (
        "// Market Intelligence Hub — Macro Data\n"
        "// DO NOT edit manually — regenerate via: python update_data.py\n"
        f"window.MIH_DATA = {json.dumps(data, separators=(',', ':'))};\n"
    )
    with open(JS_PATH, 'w', encoding='utf-8') as f:
        f.write(js_content)
    print(f"  data.js written ({len(data['markets'])} markets)")


def write_excel(data):
    try:
        import openpyxl
        from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
    except ImportError:
        print("  openpyxl not installed. Run: pip install openpyxl")
        return

    wb = openpyxl.Workbook()

    # ── Sheet 1: Markets ──
    ws = wb.active
    ws.title = "Markets"

    headers = [
        'ID', 'Market', 'Region', 'GDP Growth %', 'Inflation %',
        'Population (M)', 'Urbanization %', 'GDP pc PPP (USD)',
        'Unemployment %', 'E-commerce %', 'Big Mac (USD)',
        'FMCG Signal', 'Current Account % GDP'
    ]

    header_fill = PatternFill('solid', fgColor='0B1E3D')
    header_font = Font(bold=True, color='FFFFFF', name='Calibri', size=10)
    thin = Side(border_style='thin', color='E2E8F0')
    cell_border = Border(left=thin, right=thin, top=thin, bottom=thin)

    signal_colors = {
        'Growing': 'DCFCE7', 'Stable': 'DBEAFE',
        'Pressured': 'FEF3C7', 'Volatile': 'FFE4E6'
    }

    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = cell_border

    for row, m in enumerate(data['markets'], 2):
        vals = [
            m['id'], m['name'], m['region'],
            m['gdp_growth'], m['inflation'],
            m['population_m'], m['urbanization_pct'],
            m['gdp_pc_ppp'], m['unemployment_pct'],
            m['ecommerce_pct'],
            m['big_mac_usd'] if m['big_mac_usd'] is not None else 'N/A',
            m['fmcg_signal'], m['current_account_pct']
        ]
        for col, v in enumerate(vals, 1):
            cell = ws.cell(row=row, column=col, value=v)
            cell.border = cell_border
            cell.alignment = Alignment(horizontal='center' if col != 2 else 'left', vertical='center')
            if col == 12:  # FMCG Signal
                color = signal_colors.get(str(v), 'FFFFFF')
                cell.fill = PatternFill('solid', fgColor=color)
                cell.font = Font(bold=True, name='Calibri', size=10)

    # Column widths
    widths = [6, 18, 10, 13, 12, 15, 14, 16, 14, 13, 13, 13, 20]
    for col, w in enumerate(widths, 1):
        ws.column_dimensions[openpyxl.utils.get_column_letter(col)].width = w

    ws.row_dimensions[1].height = 22
    ws.freeze_panes = 'C2'

    # ── Sheet 2: Historical GDP ──
    ws2 = wb.create_sheet("Historical GDP Growth")
    years = ['2022', '2023', '2024', '2025']
    ws2.append(['Market', 'Region'] + years)
    for cell in ws2[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')
    for m in data['markets']:
        h = m.get('historical', {}).get('gdp_growth', {})
        ws2.append([m['name'], m['region']] + [h.get(y) for y in years])

    # ── Sheet 3: Historical Inflation ──
    ws3 = wb.create_sheet("Historical Inflation")
    ws3.append(['Market', 'Region'] + years)
    for cell in ws3[1]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal='center')
    for m in data['markets']:
        h = m.get('historical', {}).get('inflation', {})
        ws3.append([m['name'], m['region']] + [h.get(y) for y in years])

    # ── Sheet 4: Metadata ──
    ws4 = wb.create_sheet("Metadata")
    ws4.append(['Field', 'Value'])
    ws4.append(['Vintage', data['metadata']['vintage']])
    ws4.append(['Compiled', data['metadata']['compiled_date']])
    ws4.append(['Markets', len(data['markets'])])
    ws4.append(['', ''])
    ws4.append(['Sources', ''])
    for s in data['metadata']['primary_sources']:
        ws4.append(['', s])
    ws4.append(['', ''])
    ws4.append(['Notes', ''])
    for n in data['metadata']['notes']:
        ws4.append(['', n])

    wb.save(XLSX_PATH)
    print(f"  macro_data.xlsx written")


def main():
    print("Market Intelligence Hub — Data Update")
    print(f"  Reading: {JSON_PATH}")

    if not os.path.exists(JSON_PATH):
        print("  ERROR: data.json not found")
        sys.exit(1)

    data = load_data()
    print(f"  Loaded {len(data['markets'])} markets (vintage: {data['metadata']['vintage']})")

    write_js(data)
    write_excel(data)

    print("\nDone. To update data from official sources, ask Claude Code: 'actualiza los datos macro'")


if __name__ == '__main__':
    main()
