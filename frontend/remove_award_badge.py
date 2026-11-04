import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('frontend/src/views/ProductDetailView.vue', 'r', encoding='utf-8') as f:
    c = f.read()

target = """            <!-- Authentic Award / Recognition Seal (Top Right - Exact match to Cosmopolitan badge in screenshot!) -->
            <div
              v-if="product.awardBadge"
              class="absolute top-5 right-5 z-20 w-22 h-22 sm:w-24 sm:h-24 rounded-full bg-slate-950 text-white flex flex-col items-center justify-center p-2 text-center shadow-xl border border-white/20 transform rotate-6 select-none pointer-events-none"
            >
              <div class="text-[7.5px] uppercase tracking-widest text-slate-400 font-extrabold">{{ product.awardTitle || 'AEROBYTE' }}</div>
              <div class="text-[10px] sm:text-[11px] font-black uppercase tracking-tight text-white leading-tight my-0.5">
                {{ product.badge || 'VERIFIED' }}
              </div>
              <div class="text-[7px] uppercase tracking-wider text-amber-400 font-bold">{{ product.awardSubtitle || 'LAB CERTIFIED' }}</div>
              <div class="text-[8px] mt-0.5 opacity-60">★ 2026 ★</div>
            </div>

"""

assert target in c, "target award badge block not found!"
c = c.replace(target, "")

with open('frontend/src/views/ProductDetailView.vue', 'w', encoding='utf-8') as f:
    f.write(c)

print("Award badge removed successfully!")
