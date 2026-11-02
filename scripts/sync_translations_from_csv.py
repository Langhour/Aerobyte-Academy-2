"""
AeroByte Academy — Sync Translations from CSV files to frontend/src/i18n.js
Usage:
    python scripts/sync_translations_from_csv.py [optional_path_to_csv_folder_or_file]

This script reads any edited Khmer translations from CSV files in `translations_csv/`
and automatically updates `frontend/src/i18n.js`.
"""

import os
import sys
import csv
import re

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV_DIR = os.path.join(ROOT_DIR, "translations_csv")
I18N_PATH = os.path.join(ROOT_DIR, "frontend", "src", "i18n.js")

target_path = sys.argv[1] if len(sys.argv) > 1 else CSV_DIR

csv_files = []
if os.path.isfile(target_path):
    csv_files = [target_path]
elif os.path.isdir(target_path):
    for f in sorted(os.listdir(target_path)):
        if f.endswith(".csv") and not f.startswith("Instructions"):
            csv_files.append(os.path.join(target_path, f))
else:
    print(f"Error: Path not found at {target_path}")
    sys.exit(1)

updates = {}

for file_path in csv_files:
    # If processing master and individual sheets, master or individual sheets work
    with open(file_path, "r", encoding="utf-8-sig") as f:
        reader = csv.reader(f)
        header = next(reader, None)
        if not header:
            continue
        
        # Determine column indices
        col_en = 2
        col_cur_kh = 3
        col_new_kh = 4
        for idx, col_name in enumerate(header):
            c_lower = col_name.lower()
            if "english" in c_lower:
                col_en = idx
            elif "new khmer" in c_lower:
                col_new_kh = idx
            elif "current khmer" in c_lower:
                col_cur_kh = idx

        for row in reader:
            if len(row) <= col_en:
                continue
            en_key = row[col_en].strip()
            if not en_key:
                continue

            new_kh = row[col_new_kh].strip() if len(row) > col_new_kh else ""
            cur_kh = row[col_cur_kh].strip() if len(row) > col_cur_kh else ""

            # Prioritize 'New Khmer Translation', fallback to 'Current Khmer Translation'
            chosen_kh = new_kh if new_kh else cur_kh
            if chosen_kh:
                updates[en_key] = chosen_kh

print(f"Loaded {len(updates)} translations from CSV files.")

if not updates:
    print("No translations found to apply.")
    sys.exit(0)

with open(I18N_PATH, "r", encoding="utf-8") as f:
    content = f.read()

applied_count = 0
for en_key, kh_val in updates.items():
    escaped_val = kh_val.replace("\\", "\\\\").replace("'", "\\'")
    
    # Try single-quoted key pattern
    pattern_sq = re.compile(rf"(^\s*'{re.escape(en_key)}'\s*:\s*)(['\"].*?['\"]|\s*'.*?'\s*),?", re.MULTILINE)
    # Try unquoted key pattern
    pattern_uq = re.compile(rf"(^\s*{re.escape(en_key)}\s*:\s*)(['\"].*?['\"]|\s*'.*?'\s*),?", re.MULTILINE)
    
    if pattern_sq.search(content):
        content = pattern_sq.sub(rf"\1'{escaped_val}',", content)
        applied_count += 1
    elif pattern_uq.search(content):
        content = pattern_uq.sub(rf"\1'{escaped_val}',", content)
        applied_count += 1

with open(I18N_PATH, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully synced {applied_count} translations to {I18N_PATH}!")
