import json
import os
import shutil
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

with open('translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Translations (EN - KH)"

# Ensure grid lines are visible
ws.views.sheetView[0].showGridLines = True

headers = [
    "No.",
    "English Text (Original)",
    "Khmer Translation (អត្ថបទខ្មែរ)",
    "Length (EN)",
    "Length (KH)"
]

ws.append(headers)

# Styling Definitions
header_fill = PatternFill(start_color="102A49", end_color="102A49", fill_type="solid")
header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")
header_alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

thin_border = Border(
    left=Side(style='thin', color='E2E8F0'),
    right=Side(style='thin', color='E2E8F0'),
    top=Side(style='thin', color='E2E8F0'),
    bottom=Side(style='thin', color='E2E8F0')
)

ws.row_dimensions[1].height = 32

for col_idx in range(1, len(headers) + 1):
    cell = ws.cell(row=1, column=col_idx)
    cell.fill = header_fill
    cell.font = header_font
    cell.alignment = header_alignment

row_num = 1
for en_text, kh_text in translations.items():
    row_num += 1
    en_clean = str(en_text).strip()
    kh_clean = str(kh_text).strip()
    
    ws.append([
        row_num - 1,
        en_clean,
        kh_clean,
        len(en_clean),
        len(kh_clean)
    ])

# Style data rows
for row_idx in range(2, row_num + 1):
    is_even = (row_idx % 2 == 0)
    bg_color = "F8FAFC" if is_even else "FFFFFF"
    row_fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    
    # No.
    c1 = ws.cell(row=row_idx, column=1)
    c1.fill = row_fill
    c1.border = thin_border
    c1.font = Font(name="Segoe UI", size=10, bold=True, color="64748B")
    c1.alignment = Alignment(horizontal="center", vertical="center")
    
    # English
    c2 = ws.cell(row=row_idx, column=2)
    c2.fill = row_fill
    c2.border = thin_border
    c2.font = Font(name="Segoe UI", size=10, color="0F172A")
    c2.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    
    # Khmer
    c3 = ws.cell(row=row_idx, column=3)
    c3.fill = row_fill
    c3.border = thin_border
    c3.font = Font(name="Segoe UI", size=10, color="0F172A")
    c3.alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    
    # Length EN
    c4 = ws.cell(row=row_idx, column=4)
    c4.fill = row_fill
    c4.border = thin_border
    c4.font = Font(name="Segoe UI", size=9, color="94A3B8")
    c4.alignment = Alignment(horizontal="center", vertical="center")
    
    # Length KH
    c5 = ws.cell(row=row_idx, column=5)
    c5.fill = row_fill
    c5.border = thin_border
    c5.font = Font(name="Segoe UI", size=9, color="94A3B8")
    c5.alignment = Alignment(horizontal="center", vertical="center")

# Set Column Widths
ws.column_dimensions['A'].width = 8
ws.column_dimensions['B'].width = 52
ws.column_dimensions['C'].width = 58
ws.column_dimensions['D'].width = 14
ws.column_dimensions['E'].width = 14

# Freeze Top Header Row
ws.freeze_panes = 'A2'

# Enable Excel Auto-Filter on header
ws.auto_filter.ref = f"A1:E{row_num}"

out_path = "ALL_ENGLISH_AND_KHMER_TRANSLATIONS.xlsx"
wb.save(out_path)
print(f"Successfully generated {out_path} with {row_num - 1} translation rows.")

# Also copy to artifacts directory
artifact_dir = r"C:\Users\Langhour\.gemini\antigravity\brain\9091b263-867a-4e70-af68-9df7f36f5bcc"
if os.path.exists(artifact_dir):
    artifact_copy = os.path.join(artifact_dir, "ALL_ENGLISH_AND_KHMER_TRANSLATIONS.xlsx")
    shutil.copy2(out_path, artifact_copy)
    print(f"Copied to artifact dir: {artifact_copy}")

# Cleanup temp json
if os.path.exists("translations.json"):
    os.remove("translations.json")
