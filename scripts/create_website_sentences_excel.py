import os
import re
import json
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

with open('translations.json', 'r', encoding='utf-8') as f:
    translations = json.load(f)

PAGE_MAPPINGS = {
    'HomeView.vue': 'Home Page',
    'CoursesView.vue': 'Courses Catalog',
    'CourseDetailsView.vue': 'Course Details',
    'CourseEnrollmentView.vue': 'Course Enrollment & Registration',
    'ScanToPayView.vue': 'Scan to Pay & Checkout',
    'PaymentSuccessfulView.vue': 'Payment Confirmation / Success',
    'PaymentExpiredView.vue': 'Payment Expired Notice',
    'AboutView.vue': 'About AeroByte Academy',
    'QuestionsView.vue': 'Questions & FAQs',
    'TermsAndConditionsView.vue': 'Terms & Conditions',
    'PrivacyPolicyView.vue': 'Privacy Policy',
    'AccountAccessView.vue': 'Account Login & Password Reset',
    'ProfileInformationView.vue': 'Student Profile & Course History',
    'AdminContentView.vue': 'Admin Portal & Management',
    'Navbar.vue': 'Header & Navigation',
    'Footer.vue': 'Footer & Legal Notice',
}

views_dir = 'frontend/src/views'
components_dir = 'frontend/src/components'

# Ignore technical developer strings
EXCLUDE_TECHNICAL = {
    'Main navigation', 'Course categories', 'Footer navigation', 'Pagination',
    'Page', 'Previous page', 'Next page', 'Hide sidebar', 'Show sidebar',
    'Collapse sidebar', 'Expand sidebar', 'records', 'course', 'courses',
    'Actions', 'Status', 'No.', 'Student', 'Education', 'Close', 'Transaction',
    'confirmed', 'cancelled', 'payment pending', 'refunded', 'pending', 'paid',
    'Active', 'Inactive', 'Reset'
}

seen_sentences = set()
website_sentences = []

def extract_sentences(file_path, page_name):
    if not os.path.exists(file_path):
        return
    with open(file_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    matches = re.findall(r'''t\(\s*['"]([^'"]+?)['"]\s*\)''', text)
    for en in matches:
        en_str = en.strip()
        if not en_str or en_str in EXCLUDE_TECHNICAL:
            continue
        kh_str = translations.get(en_str, '')
        if not kh_str:
            continue
            
        words = en_str.split()
        
        # Determine if it's a real sentence or significant website copy
        is_sentence = (
            len(words) >= 3 or
            en_str.endswith(('.', '?', '!', ':', '...')) or
            len(en_str) > 25
        )
        
        if not is_sentence:
            continue
            
        if en_str.endswith('?'):
            c_type = 'Question / FAQ'
        elif len(words) >= 8 or en_str.endswith('.'):
            c_type = 'Sentence / Paragraph'
        elif 'Please' in en_str or 'required' in en_str.lower() or 'select' in en_str.lower():
            c_type = 'Form Instruction / Notice'
        else:
            c_type = 'Headline / Section Title'
            
        key = (page_name, en_str)
        if key not in seen_sentences:
            seen_sentences.add(key)
            website_sentences.append({
                'page': page_name,
                'type': c_type,
                'words': len(words),
                'en': en_str,
                'kh': kh_str,
            })

for filename, page_name in PAGE_MAPPINGS.items():
    if os.path.exists(os.path.join(views_dir, filename)):
        extract_sentences(os.path.join(views_dir, filename), page_name)
    elif os.path.exists(os.path.join(components_dir, filename)):
        extract_sentences(os.path.join(components_dir, filename), page_name)

# Sort by Page, then sentence length descending
website_sentences.sort(key=lambda x: (x['page'], -x['words']))

wb = openpyxl.Workbook()

# Sheet 1: Real Website Sentences
ws1 = wb.active
ws1.title = "Website Sentences by Page"
ws1.views.sheetView[0].showGridLines = True

headers = [
    "No.",
    "Website Page / Location",
    "Content Type",
    "English Website Sentence",
    "Current Khmer Translation (អត្ថបទខ្មែរបច្ចុប្បន្ន)",
    "New Khmer Translation (EDIT HERE)",
    "Word Count"
]

ws1.append(headers)
ws1.row_dimensions[1].height = 36

header_fill_navy = PatternFill(start_color="102A49", end_color="102A49", fill_type="solid")
header_fill_edit = PatternFill(start_color="D97706", end_color="D97706", fill_type="solid") # Warm amber for the edit column
header_font = Font(name="Segoe UI", size=11, bold=True, color="FFFFFF")

thin_border = Border(
    left=Side(style='thin', color='CBD5E1'),
    right=Side(style='thin', color='CBD5E1'),
    top=Side(style='thin', color='CBD5E1'),
    bottom=Side(style='thin', color='CBD5E1')
)

for col_idx in range(1, len(headers) + 1):
    c = ws1.cell(row=1, column=col_idx)
    c.fill = header_fill_edit if col_idx == 6 else header_fill_navy
    c.font = header_font
    c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)

for idx, rec in enumerate(website_sentences, 1):
    is_even = (idx % 2 == 0)
    bg_color = "F8FAFC" if is_even else "FFFFFF"
    row_fill = PatternFill(start_color=bg_color, end_color=bg_color, fill_type="solid")
    edit_fill = PatternFill(start_color="FEF3C7" if is_even else "FFFBEB", end_color="FEF3C7" if is_even else "FFFBEB", fill_type="solid") # Soft yellow edit area
    
    ws1.append([
        idx,
        rec['page'],
        rec['type'],
        rec['en'],
        rec['kh'],
        "", # User can edit here
        rec['words']
    ])
    
    r_idx = idx + 1
    ws1.cell(row=r_idx, column=1).alignment = Alignment(horizontal="center", vertical="center")
    ws1.cell(row=r_idx, column=2).alignment = Alignment(horizontal="left", vertical="center")
    ws1.cell(row=r_idx, column=3).alignment = Alignment(horizontal="center", vertical="center")
    ws1.cell(row=r_idx, column=4).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    ws1.cell(row=r_idx, column=5).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    ws1.cell(row=r_idx, column=6).alignment = Alignment(horizontal="left", vertical="center", wrap_text=True)
    ws1.cell(row=r_idx, column=7).alignment = Alignment(horizontal="center", vertical="center")
    
    for c_i in range(1, 8):
        cell = ws1.cell(row=r_idx, column=c_i)
        cell.fill = edit_fill if c_i == 6 else row_fill
        cell.border = thin_border
        cell.font = Font(name="Segoe UI", size=10)

ws1.column_dimensions['A'].width = 8
ws1.column_dimensions['B'].width = 30
ws1.column_dimensions['C'].width = 24
ws1.column_dimensions['D'].width = 65
ws1.column_dimensions['E'].width = 65
ws1.column_dimensions['F'].width = 65
ws1.column_dimensions['G'].width = 14

ws1.freeze_panes = 'A2'
ws1.auto_filter.ref = f"A1:G{len(website_sentences) + 1}"

# Save
out_path = "ALL_ENGLISH_AND_KHMER_TRANSLATIONS.xlsx"
wb.save(out_path)
print(f"Generated clean website sentences Excel: {len(website_sentences)} entries.")

import shutil
downloads_path = r"C:\Users\Langhour\Downloads\ALL_ENGLISH_AND_KHMER_TRANSLATIONS.xlsx"
shutil.copy2(out_path, downloads_path)

desktop_path = r"C:\Users\Langhour\OneDrive\Desktop\ALL_ENGLISH_AND_KHMER_TRANSLATIONS.xlsx"
shutil.copy2(out_path, desktop_path)

brain_path = r"C:\Users\Langhour\.gemini\antigravity\brain\9091b263-867a-4e70-af68-9df7f36f5bcc\ALL_ENGLISH_AND_KHMER_TRANSLATIONS.xlsx"
shutil.copy2(out_path, brain_path)
print("Updated Desktop, Downloads, and Artifacts!")
