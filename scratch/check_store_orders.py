with open('frontend/src/views/AdminContentView.vue', encoding='utf-8') as f:
    lines = f.readlines()

s_start = next(i for i, l in enumerate(lines) if "activeSection === 'store_orders'" in l)
print('store_orders template starts at line:', s_start + 1)
depth = 0
s_end = s_start
for i in range(s_start, len(lines)):
    if '<section' in lines[i]:
        depth += 1
    if '</section>' in lines[i]:
        depth -= 1
        if depth == 0:
            s_end = i
            print('store_orders template ends at line:', s_end + 1)
            break

# Also find store orders modal
modal_lines = [i for i, l in enumerate(lines) if "storeOrderModalOpen" in l]
print('storeOrderModalOpen lines:', [m + 1 for m in modal_lines])

# Find script lines for store orders
script_lines = [i for i, l in enumerate(lines) if "STORE HARDWARE ORDERS STATE" in l]
print('Script lines:', [s + 1 for s in script_lines])
