<template>
  <div class="pb-16 dark:bg-slate-900 transition-colors">
    <!-- Hero Section (Matches Courses Page) -->
    <section class="courses-hero px-4 pb-10 pt-8 text-center sm:px-6 sm:pb-16 sm:pt-14 lg:px-8">
      <div class="mx-auto max-w-7xl">
        <div class="flex justify-center mb-6 sm:mb-8">
          <img
            src="/assets/brand/aero-store.png"
            alt="Aero Store"
            class="h-28 sm:h-36 md:h-44 w-auto object-contain mx-auto transition-transform duration-300 hover:scale-105 dark:invert"
          />
        </div>


        <p class="mx-auto mt-2.5 sm:mt-4 max-w-3xl text-sm sm:text-base leading-relaxed text-slate-600 dark:text-slate-300 sm:text-lg">
          {{ t('Official hardware store for authentic robotics learning kits, drone parts, microcontrollers, brushless motors, and lab tools.') }}
        </p>

        <!-- Search Bar (Matches Courses Page) -->
        <div class="relative mx-auto mt-6 sm:mt-9 max-w-[784px]">
          <Search class="pointer-events-none absolute left-4 sm:left-5 top-1/2 h-4 w-4 sm:h-5 sm:w-5 -translate-y-1/2 text-slate-400" />
          <input
            v-model="searchQuery"
            type="text"
            :placeholder="t('Search robotics kits, drone parts, sensors...')"
            class="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 py-3 sm:py-[18px] pl-11 sm:pl-14 pr-10 sm:pr-12 text-sm sm:text-base text-slate-800 dark:text-white shadow-xs transition placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500"
          />
          <button
            v-if="searchQuery"
            type="button"
            :aria-label="t('Clear search')"
            @click="searchQuery = ''"
            class="absolute right-3.5 sm:right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
          >
            <X class="h-4 w-4 sm:h-5 sm:w-5" />
          </button>
        </div>


      </div>
    </section>

    <!-- Main Layout: Sidebar (3 cols) + Product Grid (9 cols) - Matches Courses Page -->
    <div class="mx-auto grid max-w-7xl grid-cols-1 items-start gap-6 lg:gap-8 px-3 sm:px-6 lg:grid-cols-12 lg:px-8 pt-5 sm:pt-8">
      
      <!-- Left Filter Sidebar -->
      <aside class="lg:col-span-3 bg-white rounded-xl sm:rounded-2xl border border-slate-200/80 p-4 sm:p-5 shadow-card lg:sticky lg:top-24 dark:bg-slate-800 dark:border-slate-700 dark:shadow-slate-900/20">
        <!-- Sidebar Header -->
        <div class="flex items-center justify-between pb-3 sm:pb-4 border-b border-slate-100 dark:border-slate-700 mb-4">
          <div class="flex items-center gap-2 select-none">
            <h2 class="text-sm font-bold text-navy-900 dark:text-white">{{ t('Filters') }}</h2>
            <span
              v-if="activeFilterCount > 0"
              class="px-2 py-0.5 rounded-full bg-navy-100 dark:bg-indigo-900/60 text-[10px] font-bold text-navy-800 dark:text-indigo-300"
            >
              {{ activeFilterCount }}
            </span>
          </div>

          <button
            v-if="activeFilterCount > 0"
            type="button"
            @click="resetFilters"
            class="text-[11px] font-semibold text-slate-400 hover:text-navy-900 dark:hover:text-white transition cursor-pointer"
          >
            {{ t('Clear All') }}
          </button>
        </div>

        <div class="space-y-5">
          <!-- 1. Categories Filter -->
          <div class="pb-5 border-b border-slate-100 dark:border-slate-700">
            <h3 class="text-xs font-bold uppercase tracking-wider text-navy-900 mb-2 dark:text-slate-200 select-none">
              {{ t('Category') }}
            </h3>
            <div class="space-y-1">
              <label
                v-for="cat in categoryList"
                :key="cat"
                class="flex items-center justify-between px-2 py-1.5 -mx-2 rounded-lg cursor-pointer select-none hover:bg-slate-50 dark:hover:bg-slate-700/60 transition group"
              >
                <div class="flex items-center gap-2.5">
                  <input
                    type="radio"
                    name="store-category"
                    :value="cat"
                    :checked="selectedCategory === cat"
                    @change="selectedCategory = cat"
                    class="w-4 h-4 text-navy-900 dark:text-indigo-500 focus:ring-navy-900 cursor-pointer"
                  />
                  <span class="text-xs text-slate-600 dark:text-slate-300 group-hover:text-navy-900 dark:group-hover:text-white transition">
                    {{ t(cat) }}
                  </span>
                </div>
                <span class="text-[10px] font-semibold text-slate-400">
                  {{ countByCategory(cat) }}
                </span>
              </label>
            </div>
          </div>

          <!-- 2. Price Range Filter -->
          <div class="pb-5 border-b border-slate-100 dark:border-slate-700">
            <h3 class="text-xs font-bold uppercase tracking-wider text-navy-900 mb-2 dark:text-slate-200 select-none">
              {{ t('Price Range') }}
            </h3>
            <div class="space-y-1">
              <label
                v-for="p in priceOptions"
                :key="p.id"
                class="flex items-center gap-2.5 px-2 py-1.5 -mx-2 rounded-lg cursor-pointer select-none hover:bg-slate-50 dark:hover:bg-slate-700/60 transition group"
              >
                <input
                  type="radio"
                  name="store-price"
                  :value="p.id"
                  v-model="selectedPriceRange"
                  class="w-4 h-4 text-navy-900 dark:text-indigo-500 focus:ring-navy-900 cursor-pointer"
                />
                <span class="text-xs text-slate-600 dark:text-slate-300 group-hover:text-navy-900 dark:group-hover:text-white transition">
                  {{ t(p.label) }}
                </span>
              </label>
            </div>
          </div>


        </div>
      </aside>

      <!-- Right Catalog Content (9 cols) -->
      <main class="lg:col-span-9 min-h-[720px]">
        <!-- Catalog Subheader: Count + Sort -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-6 pb-3 border-b border-slate-100 dark:border-slate-800">
          <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
            {{ t('Showing') }}
            <span class="text-navy-900 dark:text-white font-bold">{{ filteredProducts.length }}</span>
            {{ t('product(s)') }}
          </p>

          <div class="flex items-center gap-2">
            <span class="text-xs text-slate-400">{{ t('Sort by:') }}</span>
            <select
              v-model="sortBy"
              class="rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-1.5 text-xs font-semibold text-slate-700 dark:text-slate-200 focus:outline-none focus:ring-1 focus:ring-navy-800"
            >
              <option value="featured">{{ t('Featured') }}</option>
              <option value="price-low">{{ t('Price: Low to High') }}</option>
              <option value="price-high">{{ t('Price: High to Low') }}</option>
              <option value="rating">{{ t('Top Rated') }}</option>
            </select>
          </div>
        </div>

        <!-- Empty State -->
        <div
          v-if="filteredProducts.length === 0"
          class="bg-navy-50/50 dark:bg-slate-800/60 rounded-2xl border border-dashed border-slate-200 dark:border-slate-700 p-12 text-center"
        >
          <div class="text-3xl mb-2">🔍</div>
          <p class="text-sm font-bold text-navy-900 dark:text-white">
            {{ t('No products match your selected filters') }}
          </p>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
            {{ t('Try searching for a different keyword or resetting your filters.') }}
          </p>
          <button
            type="button"
            @click="resetFilters"
            class="mt-4 px-4 py-2 rounded-lg bg-navy-900 dark:bg-indigo-600 text-white text-xs font-semibold hover:bg-navy-800 transition cursor-pointer"
          >
            {{ t('Reset Filters') }}
          </button>
        </div>

        <!-- Product Cards Grid (Matches CourseCard style) -->
        <div v-else class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
          <article
            v-for="item in filteredProducts"
            :key="item.id"
            class="group bg-white dark:bg-slate-800 rounded-2xl border border-slate-200/80 dark:border-slate-700/80 overflow-hidden shadow-card hover:shadow-card-hover dark:shadow-slate-900/30 transition-all duration-300 flex flex-col justify-between"
          >
            <!-- Thumbnail Visual -->
            <div class="relative block h-44 w-full overflow-hidden bg-slate-50 dark:bg-slate-800/80 p-4 border-b border-slate-100 dark:border-slate-700/60">
              <div class="flex h-full w-full items-center justify-center text-5xl group-hover:scale-110 transition-transform duration-300">
                <span>{{ item.icon }}</span>
              </div>

              <!-- Category Badge (Top-Left) -->
              <span class="absolute top-3 left-3 px-2 py-0.5 rounded-md bg-navy-900/90 dark:bg-slate-900/90 backdrop-blur-sm text-white text-[10px] font-bold uppercase tracking-wider">
                {{ t(item.category) }}
              </span>

              <!-- Badge / Discount (Top-Right) -->
              <span
                v-if="item.badge"
                class="absolute top-3 right-3 px-2 py-0.5 rounded-md bg-navy-900 dark:bg-indigo-600 text-white text-[10px] font-bold shadow-xs"
              >
                {{ item.badge }}
              </span>

              <!-- Availability (Bottom-Right) -->
              <span class="absolute bottom-3 right-3 px-2 py-0.5 rounded-md bg-emerald-50 dark:bg-emerald-950/80 text-emerald-700 dark:text-emerald-300 border border-emerald-200/80 dark:border-emerald-800 text-[10px] font-bold">
                {{ item.inStock ? t('In Stock') : t('Pre-Order') }}
              </span>
            </div>

            <!-- Card Body -->
            <div class="p-4 flex-1 flex flex-col justify-between">
              <div>
                <h3 class="text-sm font-bold text-navy-900 dark:text-white line-clamp-2">
                  {{ item.name }}
                </h3>
                <p class="mt-1.5 text-xs text-slate-500 dark:text-slate-400 leading-relaxed line-clamp-2">
                  {{ item.description }}
                </p>

                <!-- Rating -->
                <div class="mt-2.5 flex items-center gap-1.5 text-xs">
                  <span class="text-amber-500 font-bold">★ {{ item.rating }}</span>
                  <span class="text-slate-400 text-[11px]">({{ item.reviews }} {{ t('reviews') }})</span>
                </div>

                <!-- Tags -->
                <div class="mt-3 flex flex-wrap gap-1">
                  <span
                    v-for="tag in item.tags"
                    :key="tag"
                    class="rounded bg-slate-100 dark:bg-slate-700 px-1.5 py-0.5 text-[10px] font-medium text-slate-600 dark:text-slate-300"
                  >
                    {{ tag }}
                  </span>
                </div>
              </div>

              <!-- Card Footer: Price & Action -->
              <div class="mt-4 pt-3.5 border-t border-slate-100 dark:border-slate-700/60 flex items-center justify-between">
                <div>
                  <div class="text-base sm:text-lg font-black text-navy-900 dark:text-white">
                    ${{ item.priceUsd.toFixed(2) }}
                  </div>
                  <div class="text-[10px] font-semibold text-slate-400">
                    ≈ {{ (item.priceUsd * 4100).toLocaleString() }} KHR
                  </div>
                </div>

                <button
                  type="button"
                  @click="openOrder(item)"
                  class="rounded-xl bg-navy-900 hover:bg-navy-800 dark:bg-indigo-600 dark:hover:bg-indigo-500 text-white font-bold px-3.5 py-2 text-xs shadow-xs transition cursor-pointer flex items-center gap-1.5"
                >
                  <ShoppingBag class="w-3.5 h-3.5" />
                  <span>{{ t('Order') }}</span>
                </button>
              </div>
            </div>
          </article>
        </div>
      </main>
    </div>

    <!-- Quick Order Modal -->
    <div
      v-if="activeModalProduct"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-xs"
      @click.self="activeModalProduct = null"
    >
      <div class="w-full max-w-lg rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 shadow-2xl relative">
        <button
          type="button"
          @click="activeModalProduct = null"
          class="absolute top-4 right-4 text-slate-400 hover:text-slate-700 dark:hover:text-white cursor-pointer"
        >
          <X class="w-5 h-5" />
        </button>

        <div v-if="orderSubmitted" class="text-center py-8">
          <div class="text-5xl mb-3">✅</div>
          <h3 class="text-lg font-bold text-navy-900 dark:text-white">Order Request Received!</h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-2 max-w-xs mx-auto">
            Our team will contact you via Telegram or phone within 1 hour to confirm delivery or lab pickup.
          </p>
          <button
            type="button"
            @click="activeModalProduct = null"
            class="mt-5 rounded-xl bg-navy-900 dark:bg-indigo-600 text-white font-bold px-6 py-2.5 text-xs cursor-pointer"
          >
            Done
          </button>
        </div>

        <div v-else>
          <div class="flex items-start gap-4 border-b border-slate-100 dark:border-slate-800 pb-4">
            <div class="h-16 w-16 rounded-xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-3xl shrink-0">
              {{ activeModalProduct.icon }}
            </div>
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-navy-900 dark:text-indigo-400">
                {{ activeModalProduct.category }}
              </span>
              <h3 class="text-base font-bold text-navy-900 dark:text-white">{{ activeModalProduct.name }}</h3>
              <p class="text-xs font-black text-navy-900 dark:text-white mt-1">
                ${{ (activeModalProduct.priceUsd * orderQuantity).toFixed(2) }}
                <span class="text-[11px] font-normal text-slate-400">
                  (≈ {{ (activeModalProduct.priceUsd * orderQuantity * 4100).toLocaleString() }} KHR)
                </span>
              </p>
            </div>
          </div>

          <form @submit.prevent="submitOrder" class="mt-4 space-y-3">
            <div>
              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Quantity</label>
              <div class="flex items-center gap-2">
                <button
                  type="button"
                  @click="orderQuantity = Math.max(1, orderQuantity - 1)"
                  class="h-8 w-8 rounded-lg border border-slate-200 dark:border-slate-700 flex items-center justify-center font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer"
                >-</button>
                <span class="w-10 text-center font-bold text-sm text-navy-900 dark:text-white">{{ orderQuantity }}</span>
                <button
                  type="button"
                  @click="orderQuantity++"
                  class="h-8 w-8 rounded-lg border border-slate-200 dark:border-slate-700 flex items-center justify-center font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer"
                >+</button>
              </div>
            </div>

            <div>
              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Full Name</label>
              <input
                v-model="orderForm.name"
                type="text"
                required
                placeholder="e.g. Chan Dara"
                class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs text-slate-900 dark:text-white focus:outline-navy-900 dark:focus:outline-indigo-500"
              />
            </div>

            <div class="grid grid-cols-2 gap-3">
              <div>
                <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Phone Number</label>
                <input
                  v-model="orderForm.phone"
                  type="tel"
                  required
                  placeholder="012 345 678"
                  class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs text-slate-900 dark:text-white focus:outline-navy-900 dark:focus:outline-indigo-500"
                />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Telegram (Optional)</label>
                <input
                  v-model="orderForm.telegram"
                  type="text"
                  placeholder="@username"
                  class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs text-slate-900 dark:text-white focus:outline-navy-900 dark:focus:outline-indigo-500"
                />
              </div>
            </div>

            <div>
              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Delivery Address or Lab Pickup</label>
              <textarea
                v-model="orderForm.address"
                rows="2"
                placeholder="Pick up at AeroByte Academy Lab, or delivery address in Phnom Penh..."
                class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs text-slate-900 dark:text-white focus:outline-navy-900 dark:focus:outline-indigo-500"
              ></textarea>
            </div>

            <div class="pt-2 flex flex-col gap-2">
              <button
                type="submit"
                class="w-full rounded-xl bg-navy-900 hover:bg-navy-800 dark:bg-indigo-600 dark:hover:bg-indigo-500 text-white font-bold py-3 text-xs shadow-md shadow-navy-950/20 transition cursor-pointer"
              >
                Confirm Order
              </button>

              <a
                :href="telegramOrderLink"
                target="_blank"
                rel="noopener"
                class="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-bold py-2.5 px-4 text-xs transition flex items-center justify-center gap-2"
              >
                <span>💬</span>
                <span>Order Directly on Telegram</span>
              </a>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { Search, X, ShoppingBag } from 'lucide-vue-next'
import { useI18n } from '../i18n'

const { t } = useI18n()

// Search and Filter State
const searchQuery = ref('')
const selectedCategory = ref('All')
const selectedPriceRange = ref('all')
const inStockOnly = ref(false)
const sortBy = ref('featured')

// Modal State
const activeModalProduct = ref(null)
const orderQuantity = ref(1)
const orderSubmitted = ref(false)
const orderForm = ref({
  name: '',
  phone: '',
  telegram: '',
  address: ''
})

// Categories
const categoryList = [
  'Student Lab Kits',
  'FPV Drone Hardware',
  'Microcontrollers & Sensors',
  'Brushless Motors & ESCs',
  'Tools & Equipment',
  '3D Filaments & Parts'
]

// Price Options
const priceOptions = [
  { id: 'all', label: 'All Prices' },
  { id: 'under-20', label: 'Under $20' },
  { id: '20-50', label: '$20 to $50' },
  { id: '50-80', label: '$50 to $80' },
  { id: '80-plus', label: '$80 and Above' }
]

// Products Dataset
const products = [
  {
    id: 'starter-robotics-kit',
    name: 'AeroByte Starter Robotics Lab Kit',
    category: 'Student Lab Kits',
    priceUsd: 45.0,
    rating: 5.0,
    reviews: 28,
    badge: 'Best Seller',
    inStock: true,
    icon: '🤖',
    description: 'All-in-one learning kit with ESP32 board, dual motor driver shield, ultrasonic sensors, chassis, servo, and breadboard wires.',
    tags: ['ESP32', 'Robotics', 'Lab Ready']
  },
  {
    id: 'iot-maker-kit',
    name: 'AeroByte Advanced Arduino IoT Maker Kit',
    category: 'Student Lab Kits',
    priceUsd: 35.0,
    rating: 4.9,
    reviews: 19,
    badge: 'Essential',
    inStock: true,
    icon: '💡',
    description: 'Arduino Uno compatible controller, OLED display, DHT11 temp/humidity sensor, relay module, and 30+ components for IoT projects.',
    tags: ['Arduino', 'Sensors', 'Beginner']
  },
  {
    id: 'drone-frame-5in',
    name: 'Aero 5" FPV Racing Drone Frame (Carbon Fiber)',
    category: 'FPV Drone Hardware',
    priceUsd: 29.0,
    rating: 4.8,
    reviews: 14,
    badge: 'Pure 3K Carbon',
    inStock: true,
    icon: '🚁',
    description: '3K pure matte carbon fiber, 5mm arms, lightweight aerodynamic racing frame designed for 2207 brushless motors.',
    tags: ['FPV', 'Carbon Fiber', 'Racing']
  },
  {
    id: 'f405-esc-stack',
    name: 'F405 V3 Flight Controller + 50A 4-in-1 ESC Stack',
    category: 'FPV Drone Hardware',
    priceUsd: 62.0,
    rating: 4.9,
    reviews: 22,
    badge: 'Top Tier',
    inStock: true,
    icon: '⚡',
    description: 'Betaflight OSD, barometer, blackbox logging, 3-6S LiPo input, with BLHeli_S 50A continuous current handling.',
    tags: ['Flight Controller', 'Betaflight', '6S']
  },
  {
    id: 'brushless-motor-pack',
    name: 'Brushless Motor 2207 1950KV (Set of 4 for 6S)',
    category: 'Brushless Motors & ESCs',
    priceUsd: 54.0,
    rating: 5.0,
    reviews: 16,
    badge: 'Power Edition',
    inStock: true,
    icon: '⚙️',
    description: 'High torque hollow titanium shaft, N52H curved magnets, super smooth throttle curve for FPV freestyle and racing.',
    tags: ['6S Motors', 'High Torque', 'Pack of 4']
  },
  {
    id: 'esp32-dual-core',
    name: 'ESP32-WROOM-32D Development Board Type-C',
    category: 'Microcontrollers & Sensors',
    priceUsd: 6.5,
    rating: 4.9,
    reviews: 45,
    badge: 'Popular',
    inStock: true,
    icon: '📡',
    description: '2.4GHz Wi-Fi + Bluetooth BLE dual-core MCU, modern Type-C interface, breadboard friendly pinout.',
    tags: ['Wi-Fi', 'Bluetooth', 'Type-C']
  },
  {
    id: 'raspberry-pi-4',
    name: 'Raspberry Pi 4 Model B (4GB RAM)',
    category: 'Microcontrollers & Sensors',
    priceUsd: 68.0,
    rating: 4.9,
    reviews: 31,
    badge: 'Official',
    inStock: true,
    icon: '🍓',
    description: 'Quad-core 64-bit ARM Cortex-A72, dual 4K micro-HDMI, Gigabit Ethernet, USB 3.0 for computer vision & autonomous drones.',
    tags: ['AI / Vision', 'Linux', 'ROS']
  },
  {
    id: 'digital-soldering-station',
    name: 'Digital Precision Soldering Station (65W Type-C)',
    category: 'Tools & Equipment',
    priceUsd: 38.0,
    rating: 4.9,
    reviews: 18,
    badge: 'Lab Favorite',
    inStock: true,
    icon: '🔥',
    description: 'OLED screen, 8-second rapid heating to 300°C, PID temperature stabilization, auto-sleep mode, and ergonomic silicone grip.',
    tags: ['Soldering', 'Lab Grade', 'Type-C']
  },
  {
    id: 'lipo-balance-charger',
    name: 'Smart LiPo Battery Balance Charger (6S 80W)',
    category: 'Tools & Equipment',
    priceUsd: 32.0,
    rating: 4.8,
    reviews: 24,
    badge: 'Essential',
    inStock: true,
    icon: '🔋',
    description: 'Supports LiPo, LiFe, Li-ion, NiMH battery packs. Built-in internal resistance meter and storage discharge mode.',
    tags: ['Charger', 'LiPo', 'Safety']
  },
  {
    id: 'aeropla-filament-1kg',
    name: 'AeroPLA Tough 3D Printing Filament (1kg Spool)',
    category: '3D Filaments & Parts',
    priceUsd: 16.0,
    rating: 4.9,
    reviews: 37,
    badge: 'Tough Spec',
    inStock: true,
    icon: '🧵',
    description: '1.75mm diameter, high impact resistance, zero warping, optimized for mechanical parts, robotics arms, and drone brackets.',
    tags: ['PLA', '1kg Spool', 'High Precision']
  },
  {
    id: 'tpu-flexible-filament',
    name: 'TPU Flexible 95A Filament (1kg High Elasticity)',
    category: '3D Filaments & Parts',
    priceUsd: 22.0,
    rating: 4.8,
    reviews: 12,
    badge: 'Crash Proof',
    inStock: true,
    icon: '🌀',
    description: 'Perfect for FPV drone bumpers, action camera vibration dampeners, robotic gripper pads, and protective sleeves.',
    tags: ['Flexible 95A', 'Crash Proof', 'Vibration Free']
  },
  {
    id: 'multimeter-tool-kit',
    name: 'Maker Multimeter & Electronics Tool Kit',
    category: 'Tools & Equipment',
    priceUsd: 26.0,
    rating: 4.8,
    reviews: 15,
    badge: 'Kit Special',
    inStock: true,
    icon: '🧰',
    description: 'True RMS auto-ranging multimeter, flush wire cutters, ESD anti-static tweezers, desoldering pump, and storage carry case.',
    tags: ['Multimeter', 'Tools', 'Anti-Static']
  }
]

// Active filter count
const activeFilterCount = computed(() => {
  let count = 0
  if (selectedCategory.value !== 'All') count++
  if (selectedPriceRange.value !== 'all') count++
  if (inStockOnly.value) count++
  if (searchQuery.value.trim() !== '') count++
  return count
})

function countByCategory(cat) {
  return products.filter(p => p.category === cat).length
}

function resetFilters() {
  searchQuery.value = ''
  selectedCategory.value = 'All'
  selectedPriceRange.value = 'all'
  inStockOnly.value = false
  sortBy.value = 'featured'
}

// Filtered & Sorted Products
const filteredProducts = computed(() => {
  let list = [...products]

  // Search filter
  if (searchQuery.value.trim() !== '') {
    const q = searchQuery.value.toLowerCase()
    list = list.filter(p =>
      p.name.toLowerCase().includes(q) ||
      p.description.toLowerCase().includes(q) ||
      p.category.toLowerCase().includes(q) ||
      p.tags.some(t => t.toLowerCase().includes(q))
    )
  }

  // Category filter
  if (selectedCategory.value !== 'All') {
    list = list.filter(p => p.category === selectedCategory.value)
  }

  // Price Range filter
  if (selectedPriceRange.value === 'under-20') {
    list = list.filter(p => p.priceUsd < 20)
  } else if (selectedPriceRange.value === '20-50') {
    list = list.filter(p => p.priceUsd >= 20 && p.priceUsd <= 50)
  } else if (selectedPriceRange.value === '50-80') {
    list = list.filter(p => p.priceUsd > 50 && p.priceUsd <= 80)
  } else if (selectedPriceRange.value === '80-plus') {
    list = list.filter(p => p.priceUsd > 80)
  }

  // Stock filter
  if (inStockOnly.value) {
    list = list.filter(p => p.inStock)
  }

  // Sorting
  if (sortBy.value === 'price-low') {
    list.sort((a, b) => a.priceUsd - b.priceUsd)
  } else if (sortBy.value === 'price-high') {
    list.sort((a, b) => b.priceUsd - a.priceUsd)
  } else if (sortBy.value === 'rating') {
    list.sort((a, b) => b.rating - a.rating)
  }

  return list
})

function openOrder(item) {
  activeModalProduct.value = item
  orderQuantity.value = 1
  orderSubmitted.value = false
}

function submitOrder() {
  orderSubmitted.value = true
}

const telegramOrderLink = computed(() => {
  if (!activeModalProduct.value) return 'https://t.me/aerobyte_academy'
  const totalUsd = (activeModalProduct.value.priceUsd * orderQuantity.value).toFixed(2)
  const totalKhr = (activeModalProduct.value.priceUsd * orderQuantity.value * 4100).toLocaleString()
  const msg = encodeURIComponent(
    `Hello AeroByte Academy! I want to order from Aero Store:\n` +
    `Product: ${activeModalProduct.value.name}\n` +
    `Quantity: ${orderQuantity.value}\n` +
    `Total: $${totalUsd} (${totalKhr} KHR)\n` +
    `Name: ${orderForm.value.name || 'N/A'}\n` +
    `Phone: ${orderForm.value.phone || 'N/A'}\n` +
    `Address / Pickup: ${orderForm.value.address || 'Phnom Penh'}`
  )
  return `https://t.me/aerobyte_academy?text=${msg}`
})
</script>
