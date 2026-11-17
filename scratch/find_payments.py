with open('frontend/src/views/AdminContentView.vue', encoding='utf-8') as f:
    lines = f.readlines()
for i, l in enumerate(lines):
    if "activeSection === 'payments'" in l:
        print(f"Line {i+1}: {l.strip()}")
