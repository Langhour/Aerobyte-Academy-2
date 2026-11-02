"""
AeroByte Academy — Sync Translations from Excel / Google Sheets to i18n.js
Usage:
    python scripts/sync_translations_from_excel.py [optional_path_to_excel_file]

This script reads any edited translations in Column E ("New Khmer Translation (EDIT HERE)")
from the Excel file and updates frontend/src/i18n.js automatically.
"""

import sys
import os
import openpyxl
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_EXCEL = os.path.join(ROOT_DIR, "Aerobyte_Academy_Translations.xlsx")
I18N_PATH = os.path.join(ROOT_DIR, "frontend", "src", "i18n.js")

excel_path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_EXCEL

if not os.path.exists(excel_path):
    print(f"Error: Excel file not found at {excel_path}")
    sys.exit(1)

print(f"Reading translations from: {excel_path}")
wb = openpyxl.load_workbook(excel_path, data_only=True)

updates = {}

# We check all sheets (or the master sheet, or individual page sheets)
for sheet_name in wb.sheetnames:
    if sheet_name == "Instructions & Summary":
        continue
    ws = wb[sheet_name]
    # Header is on row 1
    # Col 3: English (key)
    # Col 5: New Khmer Translation (edit here)
    for row in range(2, ws.max_row + 1):
        en_key = ws.cell(row=row, column=3).value
        new_khmer = ws.cell(row=row, column=5).value
        
        if en_key and new_khmer:
            new_khmer_str = str(new_khmer).strip()
            if new_khmer_str:
                updates[str(en_key).strip()] = new_khmer_str

print(f"Found {len(updates)} translation corrections in the spreadsheet.")

if not updates:
    print("No new translations found in Column E ('New Khmer Translation (EDIT HERE)').")
    print("To make corrections, open the spreadsheet, type your new Khmer words in Column E, and run this script again.")
    sys.exit(0)

# Read i18n.js
with open(I18N_PATH, "r", encoding="utf-8") as f:
    content = f.read()

# Update each key
applied_count = 0
for en_key, new_val in updates.items():
    # Escape quotes in key and val for regex
    escaped_val = new_val.replace("\\", "\\\\").replace("'", "\\'")
    
    # Try single quoted key
    pattern_sq = re.compile(rf"(^\s*'{re.escape(en_key)}'\s*:\s*)(['\"].*?['\"]|\s*'.*?'\s*),?", re.MULTILINE)
    # Try unquoted key (if key was an identifier)
    pattern_uq = re.compile(rf"(^\s*{re.escape(en_key)}\s*:\s*)(['\"].*?['\"]|\s*'.*?'\s*),?", re.MULTILINE)
    
    if pattern_sq.search(content):
        content = pattern_sq.sub(rf"\1'{escaped_val}',", content)
        applied_count += 1
    elif pattern_uq.search(content):
        content = pattern_uq.sub(rf"\1'{escaped_val}',", content)
        applied_count += 1
    else:
        print(f"  Note: Key '{en_key}' not found in i18n.js directly; appending or skipping.")

with open(I18N_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully applied {applied_count} translation updates to {I18N_PATH}!")
