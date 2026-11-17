import subprocess

# 1. Base content from aed19b2
base_content = subprocess.check_output(
    ['git', 'show', 'aed19b2:frontend/src/views/AdminContentView.vue'],
    text=True,
    encoding='utf-8'
)

# 2. Source from 0d6cba4
src_content = subprocess.check_output(
    ['git', 'show', '0d6cba4:frontend/src/views/AdminContentView.vue'],
    text=True,
    encoding='utf-8'
)
src_lines = src_content.splitlines()

# Extract store_orders template
s_start = next(i for i, l in enumerate(src_lines) if "activeSection === 'store_orders'" in l)
depth = 0
s_end = s_start
for i in range(s_start, len(src_lines)):
    if '<section' in src_lines[i]:
        depth += 1
    if '</section>' in src_lines[i]:
        depth -= 1
        if depth == 0:
            s_end = i
            break
store_section_text = '\n'.join(src_lines[s_start:s_end+1])

# Extract store_order modal
m_start = next(i for i, l in enumerate(src_lines) if "storeOrderModalOpen && selectedStoreOrder" in l)
while m_start > 0 and not src_lines[m_start].strip().startswith('<div') and not src_lines[m_start].strip().startswith('<!-- Modal: Store'):
    m_start -= 1
div_idx = m_start + 1 if src_lines[m_start].strip().startswith('<!--') else m_start
depth = 0
m_end = div_idx
for i in range(div_idx, len(src_lines)):
    if '<div' in src_lines[i]:
        depth += 1
    if '</div>' in src_lines[i]:
        depth -= 1
        if depth == 0:
            m_end = i
            break
store_modal_text = '\n'.join(src_lines[m_start:m_end+1])

# Extract store_orders script
sc_start = next(i for i, l in enumerate(src_lines) if "STORE HARDWARE ORDERS STATE & ACTIONS" in l)
while sc_start > 0 and not src_lines[sc_start].strip().startswith('// ---'):
    sc_start -= 1

sc_end = next(i for i, l in enumerate(src_lines) if i > sc_start + 10 and src_lines[i].strip().startswith('// ---'))
store_script_text = '\n'.join(src_lines[sc_start:sc_end])

print(f"store_section_text: {len(store_section_text.splitlines())} lines")
print(f"store_modal_text: {len(store_modal_text.splitlines())} lines")
print(f"store_script_text: {len(store_script_text.splitlines())} lines")

# Assemble new content from aed19b2
base_lines = base_content.splitlines()

# A. Add ShoppingBag to lucide-vue-next imports
imp_end = next(i for i, l in enumerate(base_lines) if "} from 'lucide-vue-next'" in l)
if not any("ShoppingBag" in l for l in base_lines[:imp_end]):
    base_lines.insert(imp_end, "  ShoppingBag,")

# B. Insert store section right before top-level activeSection === 'payments' section!
pay_idx = next(i for i, l in enumerate(base_lines) if "activeSection === 'payments'" in l)
# Check that pay_idx is the section tag
assert '<section' in base_lines[pay_idx]
base_lines.insert(pay_idx, store_section_text + "\n")

# C. Insert store modal before </template>
tmpl_close = next(i for i, l in enumerate(base_lines) if "</template>" in l)
base_lines.insert(tmpl_close, store_modal_text + "\n")

# D. Insert store script before // AERO FLY ADMIN STATE & ACTIONS
fly_script_idx = next(i for i, l in enumerate(base_lines) if "AERO FLY ADMIN STATE & ACTIONS" in l)
while fly_script_idx > 0 and not base_lines[fly_script_idx].strip().startswith('// ---'):
    fly_script_idx -= 1
base_lines.insert(fly_script_idx, store_script_text + "\n")

new_content = '\n'.join(base_lines)

# E. Update navigationModules: add store_orders in academy.sections
new_content = new_content.replace(
"""      { id: 'students', title: 'Student Enrollments', icon: Users },
      { id: 'payments', title: 'Payments & QR Checkout', icon: CreditCard },""",
"""      { id: 'students', title: 'Student Enrollments', icon: Users },
      { id: 'store_orders', title: 'Store Hardware Orders', icon: ShoppingBag },
      { id: 'payments', title: 'Payments & QR Checkout', icon: CreditCard },"""
)

# F. Navigation routing
new_content = new_content.replace(
    "if (['dashboard', 'courses', 'students', 'payments', 'promos'].includes(activeSection.value)) {",
    "if (['dashboard', 'courses', 'students', 'store_orders', 'payments', 'promos'].includes(activeSection.value)) {"
)
new_content = new_content.replace(
    "if (['dashboard', 'courses', 'students', 'payments', 'promos'].includes(targetId)) {",
    "if (['dashboard', 'courses', 'students', 'store_orders', 'payments', 'promos'].includes(targetId)) {"
)
new_content = new_content.replace(
    "  } else if (targetId === 'payments') {\n    fetchPayments()\n  } else if (targetId === 'promos') {",
    "  } else if (targetId === 'store_orders') {\n    fetchStoreOrders()\n  } else if (targetId === 'payments') {\n    fetchPayments()\n  } else if (targetId === 'promos') {"
)

# G. Badges
new_content = new_content.replace(
    "  if (sectionId === 'students') return pendingEnrollmentsCount.value\n  if (sectionId === 'payments') return pendingPaymentsCount.value",
    "  if (sectionId === 'students') return pendingEnrollmentsCount.value\n  if (sectionId === 'store_orders') return pendingStoreOrdersCount.value\n  if (sectionId === 'payments') return pendingPaymentsCount.value"
)
new_content = new_content.replace(
    "  if (sectionId === 'students') {\n    return 'bg-amber-100 dark:bg-amber-950/80 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800'\n  }",
    "  if (sectionId === 'students' || sectionId === 'store_orders') {\n    return 'bg-amber-100 dark:bg-amber-950/80 text-amber-700 dark:text-amber-300 border border-amber-200 dark:border-amber-800'\n  }"
)
new_content = new_content.replace(
    "    if (moduleId === 'academy') {\n    return pendingEnrollmentsCount.value + pendingPaymentsCount.value\n  }",
    "    if (moduleId === 'academy') {\n    return pendingEnrollmentsCount.value + pendingPaymentsCount.value + pendingStoreOrdersCount.value\n  }"
)

# H. OnMounted
new_content = new_content.replace(
    "    fetchPayments()\n    lastKnownEnrollmentIds = new Set((enrollments.value || []).map(e => e.enrollment_id))\n    lastKnownPaymentIds = new Set((payments.value || []).map(p => `${p.transaction_id || p.enrollment_id}-${p.status}`))\n    fetchPrintOrders()",
    "    fetchPayments()\n    fetchStoreOrders()\n    lastKnownEnrollmentIds = new Set((enrollments.value || []).map(e => e.enrollment_id))\n    lastKnownPaymentIds = new Set((payments.value || []).map(p => `${p.transaction_id || p.enrollment_id}-${p.status}`))\n    fetchPrintOrders()"
)

# I. Merge server print orders with defaultPrintOrders
new_content = new_content.replace(
"""async function fetchPrintOrders() {
  isLoadingPrintOrders.value = true
  try {
    const res = await adminService.getPrintOrders()
    if (res?.data?.orders && res.data.orders.length > 0) {
      printOrdersList.value = res.data.orders
      localStorage.setItem('aerobyte_admin_print_orders', JSON.stringify(res.data.orders))
    }
  } catch (err) {
    console.warn('Could not fetch print orders from backend, using cached state:', err)
  } finally {
    isLoadingPrintOrders.value = false
  }
}""",
"""async function fetchPrintOrders() {
  isLoadingPrintOrders.value = true
  try {
    const res = await adminService.getPrintOrders()
    const serverOrders = res?.data?.orders || []
    const serverIds = new Set(serverOrders.map(o => o.order_number || o.id))
    const combined = [...serverOrders]
    for (const d of defaultPrintOrders) {
      if (!serverIds.has(d.order_number) && !serverIds.has(d.id)) {
        combined.push(d)
      }
    }
    printOrdersList.value = combined
    localStorage.setItem('aerobyte_admin_print_orders', JSON.stringify(combined))
  } catch (err) {
    console.warn('Could not fetch print orders from backend, using cached state:', err)
  } finally {
    isLoadingPrintOrders.value = false
  }
}"""
)

# Write to AdminContentView.vue
with open('frontend/src/views/AdminContentView.vue', 'w', encoding='utf-8') as f:
    f.write(new_content)

print(f"Successfully merged! Output lines: {len(new_content.splitlines())}")
