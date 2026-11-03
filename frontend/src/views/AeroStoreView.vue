<template>
  <div class="min-h-screen pb-24 bg-slate-50 dark:bg-slate-950 transition-colors">
    <!-- 1. Top Announcement Bar -->
    <div class="bg-gradient-to-r from-navy-900 via-navy-800 to-indigo-900 text-white text-xs sm:text-sm py-2 px-4 shadow-xs">
      <div class="mx-auto max-w-7xl flex flex-wrap items-center justify-between gap-2">
        <div class="flex items-center gap-2">
          <span class="inline-flex items-center justify-center h-5 w-5 rounded-full bg-indigo-500/30 text-amber-300">
            <Sparkles class="w-3.5 h-3.5" />
          </span>
          <span class="font-medium text-slate-100">
            <strong class="text-white font-bold">AeroByte Student Discount:</strong>
            {{ t('Enrolled students receive 10% instant rebate on all lab kits & filaments with code') }}
            <code class="px-1.5 py-0.5 rounded bg-white/20 text-white font-mono text-[11px] font-bold">AEROSTUDENT</code>
          </span>
        </div>

        <div class="flex items-center gap-3 text-[11px] sm:text-xs">
          <span class="hidden md:inline-flex items-center gap-1.5 text-slate-300">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-400"></span>
            </span>
            {{ t('Phnom Penh Lab Open for Same-Day Pickup') }}
          </span>
          <a
            href="https://t.me/aerobyte_academy"
            target="_blank"
            rel="noopener"
            class="underline hover:text-indigo-200 transition font-semibold"
          >
            {{ t('Telegram Support') }} &rarr;
          </a>
        </div>
      </div>
    </div>

    <!-- 2. Hero Section (Elevated Hardware Lab Brand) -->
    <section class="courses-hero px-4 pt-8 pb-10 sm:pt-12 sm:pb-14 border-b border-slate-200/80 dark:border-slate-800/80">
      <div class="mx-auto max-w-7xl text-center">
        <!-- Sub-brand Tag -->
        <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-white dark:bg-slate-800/80 border border-slate-200 dark:border-slate-700 shadow-2xs mb-5">
          <span class="h-2 w-2 rounded-full bg-indigo-600 dark:bg-indigo-400"></span>
          <span class="text-[11px] font-bold uppercase tracking-wider text-navy-900 dark:text-indigo-300">
            {{ t('Official Hardware Store • Phnom Penh Lab') }}
          </span>
        </div>

        <!-- Logo & Branding -->
        <div class="flex justify-center mb-5">
          <img
            src="/assets/brand/aero-store.png"
            alt="Aero Store"
            class="h-24 sm:h-32 md:h-40 w-auto object-contain mx-auto transition-transform duration-300 hover:scale-105 dark:invert drop-shadow-sm"
          />
        </div>

        <h1 class="text-2xl sm:text-4xl md:text-5xl font-extrabold tracking-tight text-navy-900 dark:text-white">
          {{ t('Official Maker & Robotics Hardware Store') }}
        </h1>

        <p class="mx-auto mt-3 max-w-3xl text-sm sm:text-base leading-relaxed text-slate-600 dark:text-slate-300">
          {{ t('Official hardware store for authentic robotics learning kits, drone parts, microcontrollers, brushless motors, and lab tools.') }}
        </p>

        <!-- Search Bar with Live Tags -->
        <div class="relative mx-auto mt-7 max-w-2xl">
          <div class="relative flex items-center">
            <Search class="pointer-events-none absolute left-4 h-5 w-5 text-slate-400" />
            <input
              v-model="searchQuery"
              type="text"
              :placeholder="t('Search robotics kits, drone parts, sensors...')"
              class="w-full rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800/90 py-3.5 sm:py-4 pl-12 pr-28 text-sm sm:text-base text-slate-800 dark:text-white shadow-card transition placeholder:text-slate-400 dark:placeholder:text-slate-500 focus:border-navy-800 dark:focus:border-indigo-500 focus:outline-none focus:ring-2 focus:ring-navy-900/10 dark:focus:ring-indigo-500/20"
            />
            <div class="absolute right-3 flex items-center gap-1.5">
              <button
                v-if="searchQuery"
                type="button"
                :aria-label="t('Clear search')"
                @click="searchQuery = ''"
                class="p-1 rounded-md text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition"
              >
                <X class="h-4 w-4" />
              </button>
              <button
                type="button"
                @click="isCartOpen = true"
                class="relative flex items-center gap-1.5 rounded-xl bg-navy-900 dark:bg-indigo-600 px-3 py-1.5 text-xs font-bold text-white shadow-xs hover:bg-navy-800 dark:hover:bg-indigo-500 transition cursor-pointer"
              >
                <ShoppingBag class="w-3.5 h-3.5" />
                <span class="hidden sm:inline">{{ t('Bag') }}</span>
                <span
                  v-if="totalCartItemsCount > 0"
                  class="ml-0.5 px-1.5 py-0.2 rounded-full bg-amber-400 text-slate-900 font-extrabold text-[10px]"
                >
                  {{ totalCartItemsCount }}
                </span>
              </button>
            </div>
          </div>

          <!-- Quick Hot Search Chips -->
          <div class="mt-3 flex flex-wrap items-center justify-center gap-1.5 text-xs">
            <span class="text-slate-400 font-medium text-[11px]">{{ t('Popular:') }}</span>
            <button
              v-for="chip in popularChips"
              :key="chip"
              type="button"
              @click="searchQuery = chip"
              class="px-2.5 py-1 rounded-lg bg-white/70 dark:bg-slate-800/70 border border-slate-200/60 dark:border-slate-700/60 text-slate-600 dark:text-slate-300 hover:border-navy-800 hover:text-navy-900 dark:hover:border-indigo-400 dark:hover:text-white transition text-[11px] font-semibold"
            >
              {{ chip }}
            </button>
          </div>
        </div>

        <!-- 4 Key Trust Pillars Grid -->
        <div class="mx-auto mt-8 max-w-5xl grid grid-cols-2 md:grid-cols-4 gap-3 sm:gap-4 text-left">
          <div class="p-3.5 sm:p-4 rounded-xl bg-white/80 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/80 shadow-2xs backdrop-blur-xs flex items-center gap-3">
            <div class="h-10 w-10 shrink-0 rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-navy-900 dark:text-indigo-400 flex items-center justify-center">
              <Truck class="w-5 h-5" />
            </div>
            <div>
              <h4 class="text-xs font-bold text-navy-900 dark:text-white">{{ t('Fast Phnom Penh Delivery') }}</h4>
              <p class="text-[11px] text-slate-500 dark:text-slate-400">{{ t('Same-day lab pickup') }}</p>
            </div>
          </div>

          <div class="p-3.5 sm:p-4 rounded-xl bg-white/80 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/80 shadow-2xs backdrop-blur-xs flex items-center gap-3">
            <div class="h-10 w-10 shrink-0 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center">
              <ShieldCheck class="w-5 h-5" />
            </div>
            <div>
              <h4 class="text-xs font-bold text-navy-900 dark:text-white">{{ t('Lab Tested Quality') }}</h4>
              <p class="text-[11px] text-slate-500 dark:text-slate-400">{{ t('100% Genuine hardware') }}</p>
            </div>
          </div>

          <div class="p-3.5 sm:p-4 rounded-xl bg-white/80 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/80 shadow-2xs backdrop-blur-xs flex items-center gap-3">
            <div class="h-10 w-10 shrink-0 rounded-xl bg-amber-50 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400 flex items-center justify-center">
              <Cpu class="w-5 h-5" />
            </div>
            <div>
              <h4 class="text-xs font-bold text-navy-900 dark:text-white">{{ t('Course Compatible') }}</h4>
              <p class="text-[11px] text-slate-500 dark:text-slate-400">{{ t('Pre-flashed & verified') }}</p>
            </div>
          </div>

          <div class="p-3.5 sm:p-4 rounded-xl bg-white/80 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/80 shadow-2xs backdrop-blur-xs flex items-center gap-3">
            <div class="h-10 w-10 shrink-0 rounded-xl bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 flex items-center justify-center">
              <MessageCircle class="w-5 h-5" />
            </div>
            <div>
              <h4 class="text-xs font-bold text-navy-900 dark:text-white">{{ t('Engineer Support') }}</h4>
              <p class="text-[11px] text-slate-500 dark:text-slate-400">{{ t('Direct Telegram help') }}</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. Category Spotlight Tabs Strip (Quick Click Nav) -->
    <div class="sticky top-16 z-30 bg-white/95 dark:bg-slate-900/95 backdrop-blur-md border-b border-slate-200 dark:border-slate-800 py-3 shadow-2xs">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="flex items-center justify-between gap-3 overflow-x-auto no-scrollbar py-0.5">
          <div class="flex items-center gap-2 shrink-0">
            <button
              type="button"
              @click="selectedCategory = 'All'"
              class="px-3.5 py-1.5 rounded-xl text-xs font-bold transition flex items-center gap-1.5 whitespace-nowrap cursor-pointer"
              :class="selectedCategory === 'All'
                ? 'bg-navy-900 text-white dark:bg-indigo-600 shadow-xs'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'"
            >
              <span>🌐</span>
              <span>{{ t('All Products') }}</span>
              <span class="px-1.5 py-0.2 rounded-full text-[10px] bg-white/20 text-white">
                {{ products.length }}
              </span>
            </button>

            <button
              v-for="cat in categoryList"
              :key="cat"
              type="button"
              @click="selectedCategory = cat"
              class="px-3.5 py-1.5 rounded-xl text-xs font-bold transition flex items-center gap-1.5 whitespace-nowrap cursor-pointer"
              :class="selectedCategory === cat
                ? 'bg-navy-900 text-white dark:bg-indigo-600 shadow-xs'
                : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700'"
            >
              <span>{{ getCategoryIcon(cat) }}</span>
              <span>{{ t(cat) }}</span>
              <span
                class="px-1.5 py-0.2 rounded-full text-[10px]"
                :class="selectedCategory === cat ? 'bg-white/20 text-white' : 'bg-slate-200 dark:bg-slate-700 text-slate-600 dark:text-slate-400'"
              >
                {{ countByCategory(cat) }}
              </span>
            </button>
          </div>

          <!-- Quick Bag Trigger on mobile/sticky bar -->
          <button
            type="button"
            @click="isCartOpen = true"
            class="shrink-0 flex items-center gap-2 px-3 py-1.5 rounded-xl bg-navy-50 dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-xs font-bold text-navy-900 dark:text-indigo-300 hover:bg-navy-100 dark:hover:bg-slate-700 transition"
          >
            <ShoppingCart class="w-4 h-4 text-navy-900 dark:text-indigo-400" />
            <span class="hidden sm:inline">{{ t('Bag') }}</span>
            <span class="font-extrabold text-navy-900 dark:text-white">
              ${{ cartSubtotalUsd.toFixed(2) }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- 4. Featured Product Spotlight Banner -->
    <div v-if="!searchQuery && selectedCategory === 'All'" class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-6 sm:pt-8">
      <div class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-navy-900 via-navy-800 to-indigo-950 p-6 sm:p-8 text-white shadow-card">
        <!-- Background decorative circuit glow -->
        <div class="absolute -right-10 -bottom-10 h-64 w-64 rounded-full bg-indigo-500/10 blur-3xl pointer-events-none"></div>
        <div class="absolute top-0 right-1/4 h-32 w-32 rounded-full bg-cyan-500/10 blur-2xl pointer-events-none"></div>

        <div class="relative z-10 grid grid-cols-1 lg:grid-cols-12 gap-6 items-center">
          <div class="lg:col-span-8 space-y-3">
            <div class="flex flex-wrap items-center gap-2">
              <span class="px-2.5 py-0.5 rounded-full bg-amber-400 text-slate-900 text-[10px] font-black uppercase tracking-wider">
                {{ t('Featured Kit of the Month') }}
              </span>
              <span class="px-2.5 py-0.5 rounded-full bg-white/10 backdrop-blur-xs text-white text-[10px] font-semibold">
                {{ t('Curriculum Tested in AeroByte Lab') }}
              </span>
            </div>

            <h2 class="text-xl sm:text-2xl md:text-3xl font-black tracking-tight text-white">
              AeroByte Starter Robotics Lab Kit (ESP32 Edition)
            </h2>

            <p class="text-xs sm:text-sm text-slate-300 max-w-2xl leading-relaxed">
              Complete hands-on engineering bundle equipped with ESP32 Wi-Fi & Bluetooth microcontroller, dual H-bridge motor shield, ultrasonic obstacle sensors, 2WD chassis, servo, and pre-flashed lab code.
            </p>

            <div class="flex flex-wrap items-center gap-3 pt-2">
              <div class="flex items-baseline gap-2">
                <span class="text-2xl sm:text-3xl font-black text-white">$45.00</span>
                <span class="text-xs font-semibold text-slate-400">≈ 184,500 KHR</span>
              </div>

              <div class="flex items-center gap-2">
                <button
                  type="button"
                  @click="openQuickView(products[0])"
                  class="rounded-xl bg-white text-navy-900 hover:bg-slate-100 font-bold px-4 py-2 text-xs shadow-xs transition cursor-pointer flex items-center gap-1.5"
                >
                  <Eye class="w-3.5 h-3.5" />
                  <span>{{ t('Inspect Specs') }}</span>
                </button>
                <button
                  type="button"
                  @click="addToCart(products[0])"
                  class="rounded-xl bg-indigo-600 hover:bg-indigo-500 text-white font-bold px-4 py-2 text-xs shadow-xs transition cursor-pointer flex items-center gap-1.5"
                >
                  <ShoppingBag class="w-3.5 h-3.5" />
                  <span>{{ t('Add to Bag') }}</span>
                </button>
              </div>
            </div>
          </div>

          <div class="lg:col-span-4 flex justify-center">
            <div class="relative h-44 w-44 sm:h-52 sm:w-52 rounded-2xl bg-white/5 border border-white/10 backdrop-blur-md flex items-center justify-center text-7xl sm:text-8xl shadow-2xl transition-transform duration-500 hover:rotate-3 hover:scale-105">
              <span>🤖</span>
              <div class="absolute -bottom-2 -right-2 px-2.5 py-1 rounded-lg bg-emerald-500 text-white text-[11px] font-bold shadow-md">
                14 {{ t('in stock') }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 5. Main Catalog Layout (Sidebar 3 cols + Grid 9 cols) -->
    <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-6 sm:pt-8">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 sm:gap-8 items-start">
        
        <!-- Left Filter Sidebar (3 cols) -->
        <aside class="lg:col-span-3 bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/80 dark:border-slate-800 p-5 shadow-card lg:sticky lg:top-32 space-y-5">
          <!-- Sidebar Header -->
          <div class="flex items-center justify-between pb-3.5 border-b border-slate-100 dark:border-slate-800">
            <div class="flex items-center gap-2">
              <SlidersHorizontal class="w-4 h-4 text-navy-900 dark:text-indigo-400" />
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
              class="text-[11px] font-semibold text-slate-400 hover:text-navy-900 dark:hover:text-white transition cursor-pointer flex items-center gap-1"
            >
              <RotateCcw class="w-3 h-3" />
              <span>{{ t('Clear All') }}</span>
            </button>
          </div>

          <!-- Stock Filter Toggle Switch -->
          <div class="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-slate-800">
            <div class="flex flex-col">
              <span class="text-xs font-bold text-navy-900 dark:text-slate-200">{{ t('In Stock Only') }}</span>
              <span class="text-[10px] text-slate-400">{{ t('Ready for instant dispatch') }}</span>
            </div>
            <button
              type="button"
              @click="inStockOnly = !inStockOnly"
              class="relative inline-flex h-6 w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none"
              :class="inStockOnly ? 'bg-navy-900 dark:bg-indigo-600' : 'bg-slate-200 dark:bg-slate-700'"
            >
              <span
                class="pointer-events-none inline-block h-5 w-5 transform rounded-full bg-white shadow-md ring-0 transition duration-200 ease-in-out"
                :class="inStockOnly ? 'translate-x-5' : 'translate-x-0'"
              />
            </button>
          </div>

          <!-- 1. Categories Filter -->
          <div class="pb-4 border-b border-slate-100 dark:border-slate-800">
            <h3 class="text-xs font-bold uppercase tracking-wider text-navy-900 dark:text-slate-300 mb-2.5">
              {{ t('Category') }}
            </h3>
            <div class="space-y-1">
              <label
                class="flex items-center justify-between px-2.5 py-1.5 -mx-2.5 rounded-xl cursor-pointer select-none transition group"
                :class="selectedCategory === 'All' ? 'bg-navy-50 dark:bg-slate-800 font-bold' : 'hover:bg-slate-50 dark:hover:bg-slate-800/50'"
              >
                <div class="flex items-center gap-2.5">
                  <input
                    type="radio"
                    name="store-category"
                    value="All"
                    :checked="selectedCategory === 'All'"
                    @change="selectedCategory = 'All'"
                    class="w-4 h-4 text-navy-900 dark:text-indigo-500 focus:ring-navy-900 cursor-pointer"
                  />
                  <span class="text-xs text-slate-700 dark:text-slate-200 group-hover:text-navy-900 dark:group-hover:text-white">
                    {{ t('All Products') }}
                  </span>
                </div>
                <span class="text-[10px] font-semibold text-slate-400">
                  {{ products.length }}
                </span>
              </label>

              <label
                v-for="cat in categoryList"
                :key="cat"
                class="flex items-center justify-between px-2.5 py-1.5 -mx-2.5 rounded-xl cursor-pointer select-none transition group"
                :class="selectedCategory === cat ? 'bg-navy-50 dark:bg-slate-800 font-bold' : 'hover:bg-slate-50 dark:hover:bg-slate-800/50'"
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
                  <span class="text-xs text-slate-700 dark:text-slate-200 group-hover:text-navy-900 dark:group-hover:text-white">
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
          <div class="pb-4 border-b border-slate-100 dark:border-slate-800">
            <h3 class="text-xs font-bold uppercase tracking-wider text-navy-900 dark:text-slate-300 mb-2.5">
              {{ t('Price Range') }}
            </h3>
            <div class="space-y-1">
              <label
                v-for="p in priceOptions"
                :key="p.id"
                class="flex items-center gap-2.5 px-2.5 py-1.5 -mx-2.5 rounded-xl cursor-pointer select-none transition group"
                :class="selectedPriceRange === p.id ? 'bg-navy-50 dark:bg-slate-800 font-bold' : 'hover:bg-slate-50 dark:hover:bg-slate-800/50'"
              >
                <input
                  type="radio"
                  name="store-price"
                  :value="p.id"
                  v-model="selectedPriceRange"
                  class="w-4 h-4 text-navy-900 dark:text-indigo-500 focus:ring-navy-900 cursor-pointer"
                />
                <span class="text-xs text-slate-700 dark:text-slate-200 group-hover:text-navy-900 dark:group-hover:text-white">
                  {{ t(p.label) }}
                </span>
              </label>
            </div>
          </div>

          <!-- 3. Tech Specification Tag Filter -->
          <div class="pb-4 border-b border-slate-100 dark:border-slate-800">
            <h3 class="text-xs font-bold uppercase tracking-wider text-navy-900 dark:text-slate-300 mb-2.5">
              {{ t('Tags & Protocols') }}
            </h3>
            <div class="flex flex-wrap gap-1.5">
              <button
                v-for="tag in popularChips"
                :key="tag"
                type="button"
                @click="toggleTagFilter(tag)"
                class="px-2 py-1 rounded-md text-[10px] font-semibold transition cursor-pointer"
                :class="selectedTag === tag
                  ? 'bg-navy-900 text-white dark:bg-indigo-600'
                  : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-slate-700'"
              >
                #{{ tag }}
              </button>
            </div>
          </div>

          <!-- 4. Engineer Advice Callout Box -->
          <div class="rounded-xl bg-gradient-to-br from-indigo-50/80 to-navy-50/80 dark:from-slate-800/80 dark:to-indigo-950/40 p-4 border border-indigo-100 dark:border-slate-700 text-left">
            <div class="flex items-center gap-2 mb-1.5 text-navy-900 dark:text-indigo-300 font-bold text-xs">
              <span>👨‍🔧</span>
              <span>{{ t('Need Lab Guidance?') }}</span>
            </div>
            <p class="text-[11px] text-slate-600 dark:text-slate-300 leading-relaxed mb-3">
              {{ t('Unsure which motor, ESC, or controller matches your project? Send your schematic to our lab mentors.') }}
            </p>
            <a
              href="https://t.me/aerobyte_academy"
              target="_blank"
              rel="noopener"
              class="w-full inline-flex items-center justify-center gap-1.5 rounded-lg bg-navy-900 hover:bg-navy-800 dark:bg-indigo-600 dark:hover:bg-indigo-500 text-white font-bold py-2 px-3 text-xs shadow-xs transition"
            >
              <MessageCircle class="w-3.5 h-3.5" />
              <span>{{ t('Chat with Lab Mentors') }}</span>
            </a>
          </div>
        </aside>

        <!-- Right Catalog Content (9 cols) -->
        <main class="lg:col-span-9 min-h-[720px] space-y-6">
          <!-- Catalog Toolbar: Count + Filter Chips + View Mode + Sort -->
          <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-4 border-b border-slate-200 dark:border-slate-800">
            <div class="flex flex-wrap items-center gap-2">
              <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 font-medium">
                {{ t('Showing') }}
                <span class="text-navy-900 dark:text-white font-bold">{{ filteredProducts.length }}</span>
                {{ t('product(s)') }}
              </p>

              <!-- Active Filter Chips -->
              <span
                v-if="selectedCategory !== 'All'"
                class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-navy-100 dark:bg-indigo-950/60 text-navy-900 dark:text-indigo-300 text-[11px] font-semibold"
              >
                {{ t(selectedCategory) }}
                <button type="button" @click="selectedCategory = 'All'" class="hover:text-red-500">×</button>
              </span>

              <span
                v-if="selectedPriceRange !== 'all'"
                class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-slate-200 dark:bg-slate-700 text-slate-700 dark:text-slate-200 text-[11px] font-semibold"
              >
                {{ getPriceLabel(selectedPriceRange) }}
                <button type="button" @click="selectedPriceRange = 'all'" class="hover:text-red-500">×</button>
              </span>

              <span
                v-if="selectedTag"
                class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full bg-indigo-100 dark:bg-indigo-900/60 text-indigo-800 dark:text-indigo-300 text-[11px] font-semibold"
              >
                #{{ selectedTag }}
                <button type="button" @click="selectedTag = ''" class="hover:text-red-500">×</button>
              </span>
            </div>

            <div class="flex items-center gap-3">
              <!-- Grid / List Switcher -->
              <div class="hidden sm:flex items-center rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-0.5">
                <button
                  type="button"
                  @click="viewMode = 'grid'"
                  :class="viewMode === 'grid' ? 'bg-navy-900 text-white dark:bg-indigo-600' : 'text-slate-500 hover:text-slate-900 dark:text-slate-400'"
                  class="p-1.5 rounded-md transition"
                  title="Grid View"
                >
                  <Grid class="w-3.5 h-3.5" />
                </button>
                <button
                  type="button"
                  @click="viewMode = 'list'"
                  :class="viewMode === 'list' ? 'bg-navy-900 text-white dark:bg-indigo-600' : 'text-slate-500 hover:text-slate-900 dark:text-slate-400'"
                  class="p-1.5 rounded-md transition"
                  title="List View"
                >
                  <List class="w-3.5 h-3.5" />
                </button>
              </div>

              <!-- Sort Dropdown -->
              <div class="flex items-center gap-1.5 text-xs text-slate-500 dark:text-slate-400">
                <span class="hidden md:inline">{{ t('Sort by:') }}</span>
                <select
                  v-model="sortBy"
                  class="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-1.5 text-xs font-semibold text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-1 focus:ring-navy-800 dark:focus:ring-indigo-500 cursor-pointer shadow-2xs"
                >
                  <option value="featured">{{ t('Featured') }}</option>
                  <option value="price-low">{{ t('Price: Low to High') }}</option>
                  <option value="price-high">{{ t('Price: High to Low') }}</option>
                  <option value="rating">{{ t('Top Rated') }}</option>
                  <option value="reviews">{{ t('Most Reviews') }}</option>
                </select>
              </div>
            </div>
          </div>

          <!-- Empty Search / Filter State -->
          <div
            v-if="filteredProducts.length === 0"
            class="bg-white dark:bg-slate-900 rounded-3xl border border-dashed border-slate-200 dark:border-slate-800 p-12 text-center shadow-2xs"
          >
            <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-slate-100 dark:bg-slate-800 text-3xl mb-3">
              🔍
            </div>
            <h3 class="text-base font-bold text-navy-900 dark:text-white">
              {{ t('No products match your selected filters') }}
            </h3>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-sm mx-auto">
              {{ t('Try searching for a different keyword or resetting your filters.') }}
            </p>
            <button
              type="button"
              @click="resetFilters"
              class="mt-4 inline-flex items-center gap-1.5 px-4 py-2 rounded-xl bg-navy-900 dark:bg-indigo-600 text-white text-xs font-bold hover:bg-navy-800 transition cursor-pointer"
            >
              <RotateCcw class="w-3.5 h-3.5" />
              <span>{{ t('Reset Filters') }}</span>
            </button>
          </div>

          <!-- 6. GRID VIEW MODE -->
          <div
            v-else-if="viewMode === 'grid'"
            class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5"
          >
            <article
              v-for="item in filteredProducts"
              :key="item.id"
              class="group bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/80 dark:border-slate-800/90 overflow-hidden shadow-card hover:shadow-card-hover dark:shadow-slate-950/40 transition-all duration-300 flex flex-col justify-between hover:border-slate-300 dark:hover:border-indigo-500/50"
            >
              <!-- Top Showcase Visual Container -->
              <div class="relative block h-48 w-full overflow-hidden p-4 border-b border-slate-100 dark:border-slate-800/80 bg-gradient-to-b"
                   :class="item.bgGradient || 'from-slate-50 to-slate-100/60 dark:from-slate-800/40 dark:to-slate-900'">
                <!-- Visual Icon / Component Graphic -->
                <div class="flex h-full w-full items-center justify-center text-6xl group-hover:scale-110 transition-transform duration-300 drop-shadow-md">
                  <span>{{ item.icon }}</span>
                </div>

                <!-- Category Pill (Top-Left) -->
                <span class="absolute top-3 left-3 px-2.5 py-0.5 rounded-md bg-navy-900/85 dark:bg-slate-950/85 backdrop-blur-sm text-white text-[10px] font-bold uppercase tracking-wider">
                  {{ t(item.category) }}
                </span>

                <!-- Highlight Badge (Top-Right) -->
                <span
                  v-if="item.badge"
                  class="absolute top-3 right-3 px-2 py-0.5 rounded-md bg-amber-400 text-slate-900 text-[10px] font-black shadow-xs"
                >
                  {{ item.badge }}
                </span>

                <!-- Quick Action Overlay (Right Side on Hover) -->
                <div class="absolute right-3 bottom-3 flex items-center gap-1.5 opacity-90 sm:opacity-0 sm:group-hover:opacity-100 transition-opacity">
                  <button
                    type="button"
                    @click="openQuickView(item)"
                    :title="t('Quick View')"
                    class="h-8 w-8 rounded-lg bg-white/90 dark:bg-slate-800/90 backdrop-blur-xs text-navy-900 dark:text-white flex items-center justify-center hover:bg-navy-900 hover:text-white dark:hover:bg-indigo-600 transition shadow-xs cursor-pointer"
                  >
                    <Eye class="w-4 h-4" />
                  </button>
                  <button
                    type="button"
                    @click="toggleFavorite(item.id)"
                    :title="t('Favorite')"
                    class="h-8 w-8 rounded-lg bg-white/90 dark:bg-slate-800/90 backdrop-blur-xs flex items-center justify-center transition shadow-xs cursor-pointer"
                    :class="isFavorite(item.id) ? 'text-red-500' : 'text-slate-600 dark:text-slate-300 hover:text-red-500'"
                  >
                    <Heart class="w-4 h-4" :class="{ 'fill-red-500': isFavorite(item.id) }" />
                  </button>
                </div>

                <!-- Stock Status Indicator (Bottom-Left) -->
                <div class="absolute bottom-3 left-3 flex items-center gap-1.5 px-2 py-0.5 rounded-md bg-white/90 dark:bg-slate-900/90 backdrop-blur-xs border border-slate-200/50 dark:border-slate-700/50 text-[10px] font-bold">
                  <span class="relative flex h-2 w-2">
                    <span v-if="item.inStock" class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                    <span class="relative inline-flex rounded-full h-2 w-2" :class="item.inStock ? 'bg-emerald-500' : 'bg-amber-500'"></span>
                  </span>
                  <span :class="item.inStock ? 'text-emerald-700 dark:text-emerald-300' : 'text-amber-700 dark:text-amber-300'">
                    {{ item.inStock ? `${item.stockCount} in stock` : t('Pre-Order') }}
                  </span>
                </div>
              </div>

              <!-- Product Details Body -->
              <div class="p-4 flex-1 flex flex-col justify-between">
                <div>
                  <h3
                    @click="openQuickView(item)"
                    class="text-sm font-bold text-navy-900 dark:text-white line-clamp-2 hover:text-indigo-600 dark:hover:text-indigo-400 transition cursor-pointer"
                  >
                    {{ item.name }}
                  </h3>

                  <p class="mt-1.5 text-xs text-slate-500 dark:text-slate-400 leading-relaxed line-clamp-2">
                    {{ item.description }}
                  </p>

                  <!-- Rating & Reviews -->
                  <div class="mt-2.5 flex items-center gap-1.5 text-xs">
                    <div class="flex items-center text-amber-500 font-bold">
                      <Star class="w-3.5 h-3.5 fill-amber-400 text-amber-400 inline mr-1" />
                      <span>{{ item.rating.toFixed(1) }}</span>
                    </div>
                    <span class="text-slate-400 text-[11px]">({{ item.reviews }} {{ t('reviews') }})</span>
                  </div>

                  <!-- Spec Badges -->
                  <div class="mt-3 flex flex-wrap gap-1">
                    <span
                      v-for="tag in item.tags.slice(0, 3)"
                      :key="tag"
                      class="rounded-md bg-slate-100 dark:bg-slate-800 px-2 py-0.5 text-[10px] font-semibold text-slate-600 dark:text-slate-300"
                    >
                      {{ tag }}
                    </span>
                  </div>
                </div>

                <!-- Price Block & Cart Actions -->
                <div class="mt-4 pt-3.5 border-t border-slate-100 dark:border-slate-800/80 flex items-center justify-between gap-2">
                  <div>
                    <div class="text-base sm:text-lg font-black text-navy-900 dark:text-white">
                      ${{ item.priceUsd.toFixed(2) }}
                    </div>
                    <div class="text-[10px] font-semibold text-slate-400">
                      ≈ {{ (item.priceUsd * 4100).toLocaleString() }} KHR
                    </div>
                  </div>

                  <div class="flex items-center gap-1.5">
                    <button
                      type="button"
                      @click="addToCart(item)"
                      :title="t('Add to Bag')"
                      class="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-navy-900 dark:text-white hover:bg-slate-50 dark:hover:bg-slate-700 p-2 text-xs shadow-2xs transition cursor-pointer"
                    >
                      <ShoppingBag class="w-4 h-4" />
                    </button>
                    <button
                      type="button"
                      @click="openOrder(item)"
                      class="rounded-xl bg-navy-900 hover:bg-navy-800 dark:bg-indigo-600 dark:hover:bg-indigo-500 text-white font-bold px-3 py-2 text-xs shadow-xs transition cursor-pointer flex items-center gap-1"
                    >
                      <span>{{ t('Order') }}</span>
                    </button>
                  </div>
                </div>
              </div>
            </article>
          </div>

          <!-- 7. LIST VIEW MODE -->
          <div v-else class="space-y-4">
            <article
              v-for="item in filteredProducts"
              :key="item.id"
              class="group bg-white dark:bg-slate-900 rounded-2xl border border-slate-200/80 dark:border-slate-800/90 overflow-hidden shadow-card hover:shadow-card-hover dark:shadow-slate-950/40 transition-all p-4 flex flex-col sm:flex-row items-center justify-between gap-5"
            >
              <div class="flex items-center gap-4 w-full sm:w-auto">
                <div class="relative h-24 w-24 shrink-0 rounded-xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-4xl shadow-2xs">
                  <span>{{ item.icon }}</span>
                  <span
                    v-if="item.badge"
                    class="absolute -top-1.5 -right-1.5 px-1.5 py-0.2 rounded bg-amber-400 text-slate-900 text-[9px] font-black"
                  >
                    {{ item.badge }}
                  </span>
                </div>

                <div class="flex-1">
                  <div class="flex items-center gap-2">
                    <span class="text-[10px] font-bold uppercase tracking-wider text-navy-900 dark:text-indigo-400">
                      {{ t(item.category) }}
                    </span>
                    <span class="text-[10px] text-emerald-600 dark:text-emerald-400 font-bold">
                      ● {{ item.inStock ? `${item.stockCount} in stock` : t('Pre-Order') }}
                    </span>
                  </div>

                  <h3
                    @click="openQuickView(item)"
                    class="text-sm sm:text-base font-bold text-navy-900 dark:text-white hover:text-indigo-600 dark:hover:text-indigo-400 transition cursor-pointer"
                  >
                    {{ item.name }}
                  </h3>

                  <p class="mt-1 text-xs text-slate-500 dark:text-slate-400 line-clamp-1 max-w-xl">
                    {{ item.description }}
                  </p>

                  <div class="mt-2 flex items-center gap-2">
                    <div class="flex items-center text-amber-500 text-xs font-bold">
                      <Star class="w-3.5 h-3.5 fill-amber-400 text-amber-400 inline mr-1" />
                      {{ item.rating }}
                    </div>
                    <span class="text-[10px] text-slate-400">({{ item.reviews }} {{ t('reviews') }})</span>
                    <span class="text-slate-300 dark:text-slate-700">|</span>
                    <span
                      v-for="tag in item.tags.slice(0, 3)"
                      :key="tag"
                      class="text-[10px] text-slate-500 dark:text-slate-400 bg-slate-100 dark:bg-slate-800 px-1.5 py-0.5 rounded"
                    >
                      {{ tag }}
                    </span>
                  </div>
                </div>
              </div>

              <!-- List Mode Price & Actions -->
              <div class="flex items-center justify-between sm:justify-end gap-4 w-full sm:w-auto pt-3 sm:pt-0 border-t sm:border-t-0 border-slate-100 dark:border-slate-800">
                <div class="text-left sm:text-right">
                  <div class="text-lg font-black text-navy-900 dark:text-white">
                    ${{ item.priceUsd.toFixed(2) }}
                  </div>
                  <div class="text-[10px] font-semibold text-slate-400">
                    ≈ {{ (item.priceUsd * 4100).toLocaleString() }} KHR
                  </div>
                </div>

                <div class="flex items-center gap-2">
                  <button
                    type="button"
                    @click="openQuickView(item)"
                    :title="t('Quick View')"
                    class="p-2 rounded-xl border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition cursor-pointer"
                  >
                    <Eye class="w-4 h-4" />
                  </button>
                  <button
                    type="button"
                    @click="addToCart(item)"
                    class="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-navy-900 dark:text-white font-bold px-3 py-2 text-xs shadow-2xs transition cursor-pointer flex items-center gap-1.5"
                  >
                    <ShoppingBag class="w-3.5 h-3.5" />
                    <span>{{ t('Add') }}</span>
                  </button>
                  <button
                    type="button"
                    @click="openOrder(item)"
                    class="rounded-xl bg-navy-900 hover:bg-navy-800 dark:bg-indigo-600 dark:hover:bg-indigo-500 text-white font-bold px-4 py-2 text-xs shadow-xs transition cursor-pointer"
                  >
                    {{ t('Order') }}
                  </button>
                </div>
              </div>
            </article>
          </div>
        </main>
      </div>
    </div>

    <!-- 8. Aero Store Guarantee & FAQ Section -->
    <section class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 mt-16 sm:mt-24">
      <div class="rounded-3xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 sm:p-10 shadow-card">
        <div class="text-center max-w-2xl mx-auto mb-10">
          <span class="text-xs font-bold uppercase tracking-wider text-navy-900 dark:text-indigo-400">
            {{ t('AeroByte Hardware Guarantee') }}
          </span>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-navy-900 dark:text-white mt-1">
            {{ t('Why Choose Aero Store for Your Engineering Lab?') }}
          </h2>
          <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-2">
            Every component in our catalog is benchmarked on AeroByte Academy laboratory test benches and used in national robotics competitions.
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
          <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60">
            <div class="text-3xl mb-3">🔬</div>
            <h3 class="text-sm font-bold text-navy-900 dark:text-white">{{ t('Lab Calibrated & Flashed') }}</h3>
            <p class="text-xs text-slate-600 dark:text-slate-300 mt-1.5 leading-relaxed">
              Flight controllers, ESC stacks, and ESP32 boards are pre-tested with official firmware (Betaflight / Arduino) before dispatch.
            </p>
          </div>

          <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60">
            <div class="text-3xl mb-3">🏫</div>
            <h3 class="text-sm font-bold text-navy-900 dark:text-white">{{ t('School & Team Bulk B.O.M.') }}</h3>
            <p class="text-xs text-slate-600 dark:text-slate-300 mt-1.5 leading-relaxed">
              We supply university labs, high schools, and STEM maker spaces with bulk component packaging and official VAT receipts.
            </p>
          </div>

          <div class="p-5 rounded-2xl bg-slate-50 dark:bg-slate-800/60 border border-slate-200/80 dark:border-slate-700/60">
            <div class="text-3xl mb-3">⚡</div>
            <h3 class="text-sm font-bold text-navy-900 dark:text-white">{{ t('Express Phnom Penh Delivery') }}</h3>
            <p class="text-xs text-slate-600 dark:text-slate-300 mt-1.5 leading-relaxed">
              Order before 2:00 PM for same-day delivery via Grab / Virak Buntham, or pick up directly at the Ta Khmau Academy Lab.
            </p>
          </div>
        </div>

        <!-- FAQ Accordion -->
        <div class="mt-10 pt-8 border-t border-slate-100 dark:border-slate-800">
          <h3 class="text-sm sm:text-base font-bold text-navy-900 dark:text-white mb-4">
            {{ t('Frequently Asked Hardware Questions') }}
          </h3>
          <div class="space-y-3">
            <div
              v-for="(faq, idx) in faqs"
              :key="idx"
              class="rounded-xl border border-slate-200/80 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/40 p-4"
            >
              <h4 class="text-xs sm:text-sm font-bold text-navy-900 dark:text-white flex items-center justify-between">
                <span>{{ faq.q }}</span>
              </h4>
              <p class="text-xs text-slate-600 dark:text-slate-300 mt-1.5 leading-relaxed">
                {{ faq.a }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- 9. SLIDE-OVER SHOPPING BAG DRAWER -->
    <div
      v-if="isCartOpen"
      class="fixed inset-0 z-50 overflow-hidden"
    >
      <div
        class="absolute inset-0 bg-slate-950/60 backdrop-blur-xs transition-opacity"
        @click="isCartOpen = false"
      ></div>

      <div class="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div class="w-screen max-w-md bg-white dark:bg-slate-900 shadow-2xl flex flex-col justify-between border-l border-slate-200 dark:border-slate-800">
          <!-- Drawer Header -->
          <div class="p-5 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between bg-slate-50/50 dark:bg-slate-850">
            <div class="flex items-center gap-2">
              <div class="p-2 rounded-xl bg-navy-900 dark:bg-indigo-600 text-white">
                <ShoppingBag class="w-4 h-4" />
              </div>
              <div>
                <h3 class="text-sm font-bold text-navy-900 dark:text-white">{{ t('Hardware Shopping Bag') }}</h3>
                <p class="text-[11px] text-slate-400">{{ totalCartItemsCount }} {{ t('item(s)') }}</p>
              </div>
            </div>

            <button
              type="button"
              @click="isCartOpen = false"
              class="p-2 rounded-lg text-slate-400 hover:text-slate-700 dark:hover:text-white cursor-pointer"
            >
              <X class="w-5 h-5" />
            </button>
          </div>

          <!-- Drawer Body: Empty or Items List -->
          <div class="flex-1 overflow-y-auto p-5 space-y-4">
            <div v-if="cartItems.length === 0" class="text-center py-16">
              <div class="text-5xl mb-3">🛍️</div>
              <h4 class="text-sm font-bold text-navy-900 dark:text-white">{{ t('Your Bag is Empty') }}</h4>
              <p class="text-xs text-slate-400 mt-1 max-w-xs mx-auto">
                Explore our robotics kits, drone parts, and 3D filaments to start building.
              </p>
              <button
                type="button"
                @click="isCartOpen = false"
                class="mt-4 px-4 py-2 rounded-xl bg-navy-900 dark:bg-indigo-600 text-white text-xs font-bold hover:bg-navy-800 transition cursor-pointer"
              >
                {{ t('Browse Catalog') }}
              </button>
            </div>

            <div v-else class="space-y-3">
              <div
                v-for="item in cartItems"
                :key="item.id"
                class="flex items-center gap-3 p-3 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/50"
              >
                <div class="h-14 w-14 rounded-lg bg-white dark:bg-slate-800 flex items-center justify-center text-2xl shrink-0 shadow-2xs border border-slate-200/60 dark:border-slate-700/60">
                  {{ item.icon }}
                </div>

                <div class="flex-1 min-w-0">
                  <h4 class="text-xs font-bold text-navy-900 dark:text-white truncate">{{ item.name }}</h4>
                  <div class="text-xs font-black text-navy-900 dark:text-white mt-0.5">
                    ${{ (item.priceUsd * item.quantity).toFixed(2) }}
                    <span class="text-[10px] text-slate-400 font-normal">(${{ item.priceUsd.toFixed(2) }} ea)</span>
                  </div>

                  <!-- Stepper -->
                  <div class="flex items-center gap-2 mt-2">
                    <button
                      type="button"
                      @click="updateCartQuantity(item.id, item.quantity - 1)"
                      class="h-6 w-6 rounded-md border border-slate-200 dark:border-slate-700 flex items-center justify-center text-xs font-bold hover:bg-slate-100 dark:hover:bg-slate-700 cursor-pointer"
                    >-</button>
                    <span class="text-xs font-bold text-slate-800 dark:text-white w-6 text-center">{{ item.quantity }}</span>
                    <button
                      type="button"
                      @click="updateCartQuantity(item.id, item.quantity + 1)"
                      class="h-6 w-6 rounded-md border border-slate-200 dark:border-slate-700 flex items-center justify-center text-xs font-bold hover:bg-slate-100 dark:hover:bg-slate-700 cursor-pointer"
                    >+</button>
                  </div>
                </div>

                <button
                  type="button"
                  @click="removeFromCart(item.id)"
                  class="p-1.5 text-slate-400 hover:text-red-500 transition cursor-pointer"
                  title="Remove item"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>

              <!-- Delivery Preference Selector -->
              <div class="mt-6 pt-4 border-t border-slate-100 dark:border-slate-800 space-y-2">
                <label class="block text-xs font-bold text-navy-900 dark:text-white">{{ t('Delivery Method') }}</label>
                <div class="grid grid-cols-1 gap-2">
                  <label
                    class="flex items-center justify-between p-2.5 rounded-xl border cursor-pointer transition text-xs"
                    :class="selectedDeliveryMethod === 'pickup'
                      ? 'border-navy-900 dark:border-indigo-500 bg-navy-50/50 dark:bg-slate-800 font-bold'
                      : 'border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800/50'"
                  >
                    <div class="flex items-center gap-2">
                      <input type="radio" value="pickup" v-model="selectedDeliveryMethod" class="text-navy-900" />
                      <span>🏢 {{ t('AeroByte Lab Pickup') }}</span>
                    </div>
                    <span class="text-emerald-600 dark:text-emerald-400 font-bold text-[11px]">{{ t('Free') }}</span>
                  </label>

                  <label
                    class="flex items-center justify-between p-2.5 rounded-xl border cursor-pointer transition text-xs"
                    :class="selectedDeliveryMethod === 'phnom-penh'
                      ? 'border-navy-900 dark:border-indigo-500 bg-navy-50/50 dark:bg-slate-800 font-bold'
                      : 'border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800/50'"
                  >
                    <div class="flex items-center gap-2">
                      <input type="radio" value="phnom-penh" v-model="selectedDeliveryMethod" class="text-navy-900" />
                      <span>🛵 {{ t('Phnom Penh Express') }}</span>
                    </div>
                    <span class="font-bold text-[11px] text-slate-700 dark:text-slate-300">+$1.50</span>
                  </label>

                  <label
                    class="flex items-center justify-between p-2.5 rounded-xl border cursor-pointer transition text-xs"
                    :class="selectedDeliveryMethod === 'province'
                      ? 'border-navy-900 dark:border-indigo-500 bg-navy-50/50 dark:bg-slate-800 font-bold'
                      : 'border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800/50'"
                  >
                    <div class="flex items-center gap-2">
                      <input type="radio" value="province" v-model="selectedDeliveryMethod" class="text-navy-900" />
                      <span>🚚 {{ t('Nationwide Provinces') }}</span>
                    </div>
                    <span class="font-bold text-[11px] text-slate-700 dark:text-slate-300">+$2.50</span>
                  </label>
                </div>
              </div>
            </div>
          </div>

          <!-- Drawer Footer: Subtotal & Actions -->
          <div v-if="cartItems.length > 0" class="p-5 border-t border-slate-100 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-850 space-y-3">
            <div class="space-y-1.5 text-xs">
              <div class="flex items-center justify-between text-slate-500 dark:text-slate-400">
                <span>{{ t('Items Subtotal') }}:</span>
                <span class="font-bold text-slate-800 dark:text-slate-200">${{ cartSubtotalUsd.toFixed(2) }}</span>
              </div>
              <div class="flex items-center justify-between text-slate-500 dark:text-slate-400">
                <span>{{ t('Delivery Fee') }}:</span>
                <span class="font-bold text-slate-800 dark:text-slate-200">
                  {{ deliveryFeeUsd === 0 ? t('Free') : `$${deliveryFeeUsd.toFixed(2)}` }}
                </span>
              </div>
              <div class="pt-2 border-t border-slate-200/60 dark:border-slate-700/60 flex items-center justify-between text-base font-black text-navy-900 dark:text-white">
                <span>{{ t('Total Amount') }}:</span>
                <div class="text-right">
                  <div>${{ cartTotalUsd.toFixed(2) }}</div>
                  <div class="text-[10px] font-semibold text-slate-400">
                    ≈ {{ (cartTotalUsd * 4100).toLocaleString() }} KHR
                  </div>
                </div>
              </div>
            </div>

            <div class="space-y-2 pt-2">
              <a
                :href="cartTelegramCheckoutLink"
                target="_blank"
                rel="noopener"
                class="w-full rounded-xl bg-navy-900 hover:bg-navy-800 dark:bg-indigo-600 dark:hover:bg-indigo-500 text-white font-bold py-3 px-4 text-xs shadow-md shadow-navy-950/20 transition flex items-center justify-center gap-2"
              >
                <span>💬</span>
                <span>{{ t('Checkout Order on Telegram') }}</span>
              </a>

              <button
                type="button"
                @click="openCheckoutModal"
                class="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-bold py-2.5 px-4 text-xs transition cursor-pointer"
              >
                {{ t('Instant Web Order Form') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 10. PRODUCT QUICK VIEW MODAL (Rich Specifications & Checklist) -->
    <div
      v-if="quickViewProduct"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-xs overflow-y-auto"
      @click.self="quickViewProduct = null"
    >
      <div class="w-full max-w-2xl rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 sm:p-8 shadow-2xl relative my-8">
        <button
          type="button"
          @click="quickViewProduct = null"
          class="absolute top-5 right-5 text-slate-400 hover:text-slate-700 dark:hover:text-white cursor-pointer"
        >
          <X class="w-5 h-5" />
        </button>

        <div class="grid grid-cols-1 md:grid-cols-12 gap-6 items-start">
          <!-- Modal Left Visual -->
          <div class="md:col-span-5 flex flex-col items-center">
            <div class="w-full h-52 rounded-2xl bg-gradient-to-br from-slate-100 to-slate-200/60 dark:from-slate-800 dark:to-slate-900 flex items-center justify-center text-7xl shadow-inner border border-slate-200/60 dark:border-slate-700">
              {{ quickViewProduct.icon }}
            </div>

            <div class="mt-4 flex items-center justify-between w-full text-xs">
              <span class="px-2.5 py-1 rounded-md bg-emerald-50 dark:bg-emerald-950/80 text-emerald-700 dark:text-emerald-300 font-bold">
                ● {{ quickViewProduct.inStock ? `${quickViewProduct.stockCount} Units in Stock` : t('Pre-Order') }}
              </span>
              <span class="text-amber-500 font-bold">
                ★ {{ quickViewProduct.rating }} ({{ quickViewProduct.reviews }} {{ t('reviews') }})
              </span>
            </div>
          </div>

          <!-- Modal Right Details -->
          <div class="md:col-span-7 space-y-3">
            <span class="text-[10px] font-bold uppercase tracking-wider text-navy-900 dark:text-indigo-400">
              {{ t(quickViewProduct.category) }}
            </span>
            <h3 class="text-lg sm:text-xl font-extrabold text-navy-900 dark:text-white leading-snug">
              {{ quickViewProduct.name }}
            </h3>

            <div class="flex items-baseline gap-2 py-1">
              <span class="text-2xl font-black text-navy-900 dark:text-white">
                ${{ quickViewProduct.priceUsd.toFixed(2) }}
              </span>
              <span class="text-xs font-semibold text-slate-400">
                ≈ {{ (quickViewProduct.priceUsd * 4100).toLocaleString() }} KHR
              </span>
            </div>

            <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
              {{ quickViewProduct.description }}
            </p>

            <!-- Technical Specifications Table -->
            <div v-if="quickViewProduct.specs" class="pt-2">
              <h4 class="text-xs font-bold text-navy-900 dark:text-white mb-2">{{ t('Technical Specifications') }}</h4>
              <div class="rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-850 p-2.5 text-xs space-y-1">
                <div
                  v-for="(val, key) in quickViewProduct.specs"
                  :key="key"
                  class="flex items-center justify-between text-[11px] py-0.5 border-b border-slate-100 dark:border-slate-800 last:border-0"
                >
                  <span class="text-slate-500 dark:text-slate-400 font-medium">{{ key }}:</span>
                  <span class="font-bold text-navy-900 dark:text-slate-200">{{ val }}</span>
                </div>
              </div>
            </div>

            <!-- What's in the Box Checklist -->
            <div v-if="quickViewProduct.whatsInside" class="pt-2">
              <h4 class="text-xs font-bold text-navy-900 dark:text-white mb-1.5">{{ t("What's in the Box") }}</h4>
              <ul class="text-[11px] text-slate-600 dark:text-slate-300 space-y-1">
                <li
                  v-for="(item, i) in quickViewProduct.whatsInside"
                  :key="i"
                  class="flex items-center gap-1.5"
                >
                  <Check class="w-3.5 h-3.5 text-emerald-500 shrink-0" />
                  <span>{{ item }}</span>
                </li>
              </ul>
            </div>

            <!-- Actions -->
            <div class="pt-4 flex items-center gap-3">
              <button
                type="button"
                @click="addToCart(quickViewProduct); quickViewProduct = null"
                class="flex-1 rounded-xl bg-navy-900 hover:bg-navy-800 dark:bg-indigo-600 dark:hover:bg-indigo-500 text-white font-bold py-2.5 px-4 text-xs shadow-xs transition cursor-pointer flex items-center justify-center gap-2"
              >
                <ShoppingBag class="w-4 h-4" />
                <span>{{ t('Add to Bag') }}</span>
              </button>

              <button
                type="button"
                @click="openOrder(quickViewProduct); quickViewProduct = null"
                class="flex-1 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-800 dark:text-white font-bold py-2.5 px-4 text-xs transition cursor-pointer text-center"
              >
                {{ t('Instant Order') }}
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 11. QUICK ORDER / CHECKOUT MODAL -->
    <div
      v-if="activeModalProduct || isCheckoutModalOpen"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-xs overflow-y-auto"
      @click.self="closeOrderModal"
    >
      <div class="w-full max-w-lg rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 sm:p-7 shadow-2xl relative my-8">
        <button
          type="button"
          @click="closeOrderModal"
          class="absolute top-5 right-5 text-slate-400 hover:text-slate-700 dark:hover:text-white cursor-pointer"
        >
          <X class="w-5 h-5" />
        </button>

        <!-- Order Success State -->
        <div v-if="orderSubmitted" class="text-center py-6">
          <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-emerald-100 dark:bg-emerald-950/80 text-emerald-600 dark:text-emerald-400 text-3xl mb-3">
            <CheckCircle2 class="w-8 h-8" />
          </div>
          <h3 class="text-lg font-bold text-navy-900 dark:text-white">{{ t('Order Request Received!') }}</h3>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-2 max-w-xs mx-auto leading-relaxed">
            Our team will contact you via Telegram or phone shortly to confirm delivery or lab pickup in Phnom Penh.
          </p>

          <div class="mt-4 p-3 rounded-xl bg-slate-50 dark:bg-slate-800 text-left text-xs font-mono border border-slate-200 dark:border-slate-700">
            <div class="text-slate-400 text-[10px] uppercase font-bold">{{ t('Order Reference') }}</div>
            <div class="font-bold text-navy-900 dark:text-white">AERO-{{ Math.floor(100000 + Math.random() * 900000) }}</div>
          </div>

          <button
            type="button"
            @click="closeOrderModal"
            class="mt-6 w-full rounded-xl bg-navy-900 dark:bg-indigo-600 text-white font-bold py-2.5 text-xs cursor-pointer hover:bg-navy-800 transition"
          >
            {{ t('Done') }}
          </button>
        </div>

        <!-- Order Form State -->
        <div v-else>
          <!-- Summary Header -->
          <div class="flex items-start gap-4 border-b border-slate-100 dark:border-slate-800 pb-4">
            <div class="h-14 w-14 rounded-xl bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-3xl shrink-0">
              {{ activeModalProduct ? activeModalProduct.icon : '🛍️' }}
            </div>
            <div>
              <span class="text-[10px] font-bold uppercase tracking-wider text-navy-900 dark:text-indigo-400">
                {{ activeModalProduct ? activeModalProduct.category : `${totalCartItemsCount} ${t('Items in Bag')}` }}
              </span>
              <h3 class="text-base font-bold text-navy-900 dark:text-white">
                {{ activeModalProduct ? activeModalProduct.name : t('Shopping Bag Checkout') }}
              </h3>
              <p class="text-xs font-black text-navy-900 dark:text-white mt-0.5">
                ${{ currentModalPrice.toFixed(2) }}
                <span class="text-[11px] font-normal text-slate-400">
                  (≈ {{ (currentModalPrice * 4100).toLocaleString() }} KHR)
                </span>
              </p>
            </div>
          </div>

          <!-- Checkout Form -->
          <form @submit.prevent="submitOrder" class="mt-4 space-y-3">
            <!-- Items in Cart Preview (if multi-item bag checkout) -->
            <div v-if="!activeModalProduct && cartItems.length > 0" class="rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/40 p-3 max-h-32 overflow-y-auto space-y-1.5 text-xs">
              <div class="text-[10px] uppercase font-bold text-slate-400 mb-1">{{ t('Bag Summary') }}:</div>
              <div
                v-for="cItem in cartItems"
                :key="cItem.id"
                class="flex items-center justify-between text-slate-700 dark:text-slate-300"
              >
                <span class="truncate mr-2">{{ cItem.name }} (x{{ cItem.quantity }})</span>
                <span class="font-bold shrink-0">${{ (cItem.priceUsd * cItem.quantity).toFixed(2) }}</span>
              </div>
            </div>

            <!-- Quantity (if single item) -->
            <div v-if="activeModalProduct">
              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">{{ t('Quantity') }}</label>
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
              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">{{ t('Full Name') }}</label>
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
                <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">{{ t('Phone Number') }}</label>
                <input
                  v-model="orderForm.phone"
                  type="tel"
                  required
                  placeholder="012 345 678"
                  class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs text-slate-900 dark:text-white focus:outline-navy-900 dark:focus:outline-indigo-500"
                />
              </div>
              <div>
                <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">{{ t('Telegram (Optional)') }}</label>
                <input
                  v-model="orderForm.telegram"
                  type="text"
                  placeholder="@username"
                  class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs text-slate-900 dark:text-white focus:outline-navy-900 dark:focus:outline-indigo-500"
                />
              </div>
            </div>

            <div>
              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">{{ t('Delivery Address or Lab Pickup') }}</label>
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
                {{ t('Confirm Order') }}
              </button>

              <a
                :href="activeModalProduct ? telegramOrderLink : cartTelegramCheckoutLink"
                target="_blank"
                rel="noopener"
                class="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-bold py-2.5 px-4 text-xs transition flex items-center justify-center gap-2"
              >
                <span>💬</span>
                <span>{{ t('Order Directly on Telegram') }}</span>
              </a>
            </div>
          </form>
        </div>
      </div>
    </div>

    <!-- 12. Floating Toast Notification -->
    <transition
      enter-active-class="transform ease-out duration-300 transition"
      enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
      enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
      leave-active-class="transition ease-in duration-100"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="toastMessage"
        class="fixed bottom-6 right-6 z-50 rounded-2xl bg-navy-900 dark:bg-indigo-600 text-white px-4 py-3 shadow-2xl flex items-center gap-3 border border-white/20 text-xs font-semibold"
      >
        <span>✨</span>
        <span>{{ toastMessage }}</span>
      </div>
    </transition>
    <!-- 13. Floating Cart Pill Button (Visible when bag has items) -->
    <transition
      enter-active-class="transform ease-out duration-300 transition"
      enter-from-class="translate-y-6 opacity-0 scale-90"
      enter-to-class="translate-y-0 opacity-100 scale-100"
      leave-active-class="transition ease-in duration-200"
      leave-from-class="opacity-100 scale-100"
      leave-to-class="opacity-0 scale-90"
    >
      <button
        v-if="totalCartItemsCount > 0"
        type="button"
        @click="isCartOpen = true"
        class="fixed bottom-6 left-6 z-40 flex items-center gap-2.5 rounded-full bg-navy-900 dark:bg-indigo-600 px-4 py-3 text-white shadow-2xl hover:bg-navy-800 dark:hover:bg-indigo-500 transition-all duration-300 hover:scale-105 cursor-pointer border border-white/20 active:scale-95"
      >
        <span class="relative">
          <ShoppingBag class="w-5 h-5 text-amber-300" />
          <span class="absolute -top-1.5 -right-1.5 h-4 w-4 rounded-full bg-amber-400 text-slate-900 text-[10px] font-black flex items-center justify-center">
            {{ totalCartItemsCount }}
          </span>
        </span>
        <span class="text-xs font-bold">{{ t('Bag') }}</span>
        <span class="text-xs font-black text-amber-300">${{ cartTotalUsd.toFixed(2) }}</span>
      </button>
    </transition>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import {
  Search,
  X,
  ShoppingBag,
  ShoppingCart,
  Star,
  SlidersHorizontal,
  RotateCcw,
  Eye,
  Heart,
  Grid,
  List,
  Check,
  CheckCircle2,
  Trash2,
  Truck,
  ShieldCheck,
  Cpu,
  MessageCircle,
  Sparkles
} from 'lucide-vue-next'
import { useI18n } from '../i18n'

const { t } = useI18n()

// View & Filter States
const searchQuery = ref('')
const selectedCategory = ref('All')
const selectedPriceRange = ref('all')
const inStockOnly = ref(false)
const selectedTag = ref('')
const sortBy = ref('featured')
const viewMode = ref('grid') // 'grid' | 'list'

// Cart State (Slide-over drawer) with localStorage persistence
const savedCart = typeof localStorage !== 'undefined' ? localStorage.getItem('aerobyte_store_cart') : null
let initialCart = []
try {
  if (savedCart) initialCart = JSON.parse(savedCart)
} catch {
  initialCart = []
}
const isCartOpen = ref(false)
const cartItems = ref(initialCart)
const selectedDeliveryMethod = ref('pickup') // 'pickup' | 'phnom-penh' | 'province'

function persistCart() {
  try {
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem('aerobyte_store_cart', JSON.stringify(cartItems.value))
    }
  } catch {}
}

// Wishlist / Favorites State with localStorage persistence
const savedFavs = typeof localStorage !== 'undefined' ? localStorage.getItem('aerobyte_store_favs') : null
let initialFavs = []
try {
  if (savedFavs) initialFavs = JSON.parse(savedFavs)
} catch {
  initialFavs = []
}
const favorites = ref(new Set(initialFavs))

function persistFavorites() {
  try {
    if (typeof localStorage !== 'undefined') {
      localStorage.setItem('aerobyte_store_favs', JSON.stringify([...favorites.value]))
    }
  } catch {}
}

// Modals State
const activeModalProduct = ref(null)
const quickViewProduct = ref(null)
const isCheckoutModalOpen = ref(false)
const orderQuantity = ref(1)
const orderSubmitted = ref(false)
const toastMessage = ref('')

// Order Form
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

// Popular Hot Search Chips
const popularChips = [
  'ESP32',
  'Arduino',
  'FPV',
  'Carbon Fiber',
  'Soldering',
  'PLA',
  '6S Motors',
  'LiPo'
]

// Price Range Options
const priceOptions = [
  { id: 'all', label: 'All Prices' },
  { id: 'under-20', label: 'Under $20' },
  { id: '20-50', label: '$20 to $50' },
  { id: '50-80', label: '$50 to $80' },
  { id: '80-plus', label: '$80 and Above' }
]

// Authentic Products Dataset
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
    stockCount: 14,
    icon: '🤖',
    bgGradient: 'from-blue-500/10 via-indigo-500/5 to-slate-900/10',
    description: 'All-in-one learning kit with ESP32 board, dual motor driver shield, ultrasonic sensors, chassis, servo, and breadboard wires.',
    tags: ['ESP32', 'Robotics', 'Lab Ready', 'Wi-Fi'],
    specs: {
      'MCU': 'ESP32 Dual-Core 240MHz',
      'Connectivity': 'Wi-Fi 802.11 b/g/n + BLE 4.2',
      'Motor Driver': 'Dual H-Bridge L298N Shield',
      'Chassis': 'Laser-cut Acrylic Smart Car Chassis',
      'Power': 'Dual 18650 Battery Holder'
    },
    whatsInside: [
      'ESP32-WROOM-32D Development Board',
      'Dual H-Bridge Motor Driver Shield',
      'HC-SR04 Ultrasonic Distance Sensor',
      'SG90 Micro Servo 9g',
      'Smart Car Acrylic Chassis + 2 DC Motors',
      'OLED 0.96" I2C Display Module',
      'Premium 40-pin Jumper Wire Bundle'
    ]
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
    stockCount: 18,
    icon: '💡',
    bgGradient: 'from-cyan-500/10 via-blue-500/5 to-slate-900/10',
    description: 'Arduino Uno compatible controller, OLED display, DHT11 temp/humidity sensor, relay module, and 30+ components for IoT projects.',
    tags: ['Arduino', 'Sensors', 'Beginner', 'IoT'],
    specs: {
      'Controller': 'ATmega328P Uno Compatible',
      'Display': '0.96" I2C OLED (128x64)',
      'Sensors': 'DHT11, PIR Motion, Light LDR',
      'Actuators': '5V Relay Module, Active Buzzer',
      'Breadboard': '830-Point Solderless'
    },
    whatsInside: [
      'Arduino Uno Compatible Board',
      '0.96" I2C OLED Display',
      'DHT11 Temp & Humidity Sensor',
      'PIR Motion Sensor Module',
      '5V Single-Channel Relay Module',
      '830-Point Breadboard + 65 Jumper Wires',
      'Component Kit with 50+ Resistors & LEDs'
    ]
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
    stockCount: 9,
    icon: '🚁',
    bgGradient: 'from-violet-500/10 via-purple-500/5 to-slate-900/10',
    description: '3K pure matte carbon fiber, 5mm arms, lightweight aerodynamic racing frame designed for 2207 brushless motors.',
    tags: ['FPV', 'Carbon Fiber', 'Racing', '5-Inch'],
    specs: {
      'Material': 'Toray 3K Matte Carbon Fiber',
      'Wheelbase': '225mm True-X Geometry',
      'Arm Thickness': '5.0mm Chamfered Edges',
      'Stack Mounting': '20x20mm & 30.5x30.5mm',
      'Weight': '118g with hardware'
    },
    whatsInside: [
      '3K Carbon Fiber Base & Top Plates',
      '4x 5mm Removable Carbon Arms',
      'Anodized Aluminum Standoffs (M3)',
      'TPU Action Cam & FPV Antenna Mount',
      'Silicone Battery Anti-Slip Pad',
      'High-Tensile Steel Screw Set'
    ]
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
    stockCount: 7,
    icon: '⚡',
    bgGradient: 'from-amber-500/10 via-orange-500/5 to-slate-900/10',
    description: 'Betaflight OSD, barometer, blackbox logging, 3-6S LiPo input, with BLHeli_S 50A continuous current handling.',
    tags: ['Flight Controller', 'Betaflight', '6S', 'ESC 50A'],
    specs: {
      'MCU': 'STM32F405 168MHz',
      'Gyro / IMU': 'BMI270 6-Axis Low-Noise',
      'ESC Current': '50A Continuous (60A Burst)',
      'Firmware': 'Betaflight / BLHeli_S',
      'Input Voltage': '3S - 6S LiPo (10V-26V)'
    },
    whatsInside: [
      'F405 V3 Flight Controller Board',
      '50A 4-in-1 BLHeli_S ESC Board',
      'Rubycon 1000uF 35V Low ESR Capacitor',
      'XT60 Pigtail Cable (12AWG Silicone)',
      '8-Pin ESC to FC Harness Cable',
      'Anti-Vibration Silicone Dampening Grommets'
    ]
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
    stockCount: 11,
    icon: '⚙️',
    bgGradient: 'from-emerald-500/10 via-teal-500/5 to-slate-900/10',
    description: 'High torque hollow titanium shaft, N52H curved magnets, super smooth throttle curve for FPV freestyle and racing.',
    tags: ['6S Motors', 'High Torque', 'Pack of 4', '1950KV'],
    specs: {
      'Stator Size': '2207 (Titanium Shaft)',
      'KV Rating': '1950KV (Optimized for 6S)',
      'Magnets': 'N52H Curved Arc Neodymium',
      'Bearings': 'NSK 9x4x4mm Japanese High-Speed',
      'Max Thrust': '1,920g per motor'
    },
    whatsInside: [
      '4x 2207 1950KV Brushless Motors',
      '4x M5 Low-Profile Flange Lock Nuts',
      '16x M3x8mm Motor Mounting Screws',
      'Pre-tinned 20AWG Silicone Lead Wires'
    ]
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
    stockCount: 42,
    icon: '📡',
    bgGradient: 'from-blue-500/10 via-indigo-500/5 to-slate-900/10',
    description: '2.4GHz Wi-Fi + Bluetooth BLE dual-core MCU, modern Type-C interface, breadboard friendly pinout.',
    tags: ['Wi-Fi', 'Bluetooth', 'Type-C', 'ESP32'],
    specs: {
      'Processor': 'Xtensa Dual-Core 32-bit LX6 240MHz',
      'Wireless': 'Wi-Fi 802.11 b/g/n + Bluetooth 4.2 BLE',
      'Memory': '4MB SPI Flash, 520KB SRAM',
      'USB Port': 'Modern USB Type-C (CH340 Driver)',
      'GPIO': '30 General-Purpose I/O Pins'
    },
    whatsInside: [
      'ESP32-WROOM-32D Development Board (Pre-soldered headers)',
      'Anti-static ESD Protective Bag',
      'Quick Reference Pinout Card'
    ]
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
    stockCount: 6,
    icon: '🍓',
    bgGradient: 'from-rose-500/10 via-pink-500/5 to-slate-900/10',
    description: 'Quad-core 64-bit ARM Cortex-A72, dual 4K micro-HDMI, Gigabit Ethernet, USB 3.0 for computer vision & autonomous drones.',
    tags: ['AI / Vision', 'Linux', 'ROS', '4GB RAM'],
    specs: {
      'Processor': 'Broadcom BCM2711 Quad-Core 1.5GHz 64-bit',
      'RAM': '4GB LPDDR4-3200 SDRAM',
      'Video': 'Dual Micro-HDMI Ports (up to 4Kp60)',
      'Connectivity': 'Gigabit Ethernet, Wi-Fi 5GHz, BT 5.0',
      'USB Ports': '2x USB 3.0, 2x USB 2.0'
    },
    whatsInside: [
      'Raspberry Pi 4 Model B (4GB RAM Board)',
      'Official Quick Start User Guide',
      'Safety & Compliance Document'
    ]
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
    stockCount: 15,
    icon: '🔥',
    bgGradient: 'from-orange-500/10 via-amber-500/5 to-slate-900/10',
    description: 'OLED screen, 8-second rapid heating to 300°C, PID temperature stabilization, auto-sleep mode, and ergonomic silicone grip.',
    tags: ['Soldering', 'Lab Grade', 'Type-C', 'OLED'],
    specs: {
      'Power Output': '65W PD / QC Compatible',
      'Temperature Range': '100°C to 400°C (±2% stability)',
      'Heat-up Time': '8 Seconds from 25°C to 300°C',
      'Display': '0.96" OLED Status Screen',
      'Power Input': 'USB Type-C (9V-20V)'
    },
    whatsInside: [
      'Digital Smart Soldering Iron Body',
      'Fine Precision Chisel Tip',
      'Silicone Ergonomic Heat-Resistant Grip',
      'Mini Metal Safety Stand & Brass Wire Cleaner',
      'USB-C to C 100W Braided Cable'
    ]
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
    stockCount: 12,
    icon: '🔋',
    bgGradient: 'from-emerald-500/10 via-teal-500/5 to-slate-900/10',
    description: 'Supports LiPo, LiFe, Li-ion, NiMH battery packs. Built-in internal resistance meter and storage discharge mode.',
    tags: ['Charger', 'LiPo', 'Safety', '80W'],
    specs: {
      'Supported Chemistries': 'LiPo / LiFe / Li-ion (1-6S), NiMH (1-15S)',
      'Charge Power': '80W (0.1A - 6.0A Adjustable)',
      'Balance Current': '300mA per cell',
      'Safety Features': 'Internal Resistance Meter, Over-voltage Cutoff',
      'Input Voltage': 'DC 11.0V - 18.0V'
    },
    whatsInside: [
      '80W Smart Multi-Chemistry Balance Charger',
      'Multi-plug Charge Cable Adapter Set (XT60, T-Plug, JST)',
      'Alligator Clip DC Input Cable',
      'Illustrated English User Manual'
    ]
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
    stockCount: 30,
    icon: '🧵',
    bgGradient: 'from-teal-500/10 via-cyan-500/5 to-slate-900/10',
    description: '1.75mm diameter, high impact resistance, zero warping, optimized for mechanical parts, robotics arms, and drone brackets.',
    tags: ['PLA', '1kg Spool', 'High Precision', '1.75mm'],
    specs: {
      'Filament Diameter': '1.75mm (±0.02mm tolerance)',
      'Net Weight': '1.0 kg (2.2 lbs) on Spool',
      'Print Temperature': '205°C - 225°C',
      'Bed Temperature': '50°C - 60°C',
      'Material Properties': 'Modified high-impact PLA (No warping)'
    },
    whatsInside: [
      '1kg Vacuum Sealed Spool with Desiccant',
      'Spool Gauge Scale',
      'Resealable Zip Bag for Long-term Moisture Protection'
    ]
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
    stockCount: 16,
    icon: '🌀',
    bgGradient: 'from-purple-500/10 via-violet-500/5 to-slate-900/10',
    description: 'Perfect for FPV drone bumpers, action camera vibration dampeners, robotic gripper pads, and protective sleeves.',
    tags: ['Flexible 95A', 'Crash Proof', 'Vibration Free', 'TPU'],
    specs: {
      'Hardness': 'Shore 95A High Elasticity',
      'Diameter': '1.75mm (±0.03mm precision)',
      'Elongation at Break': '550%',
      'Nozzle Temp': '220°C - 240°C',
      'Best Uses': 'Drone bumpers, camera mounts, robotic gripper pads'
    },
    whatsInside: [
      '1kg Spool in Vacuum Sealed Foil Bag',
      'Drying Silica Packet',
      'Print Profile Recommended Settings Sheet'
    ]
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
    stockCount: 14,
    icon: '🧰',
    bgGradient: 'from-blue-500/10 via-indigo-500/5 to-slate-900/10',
    description: 'True RMS auto-ranging multimeter, flush wire cutters, ESD anti-static tweezers, desoldering pump, and storage carry case.',
    tags: ['Multimeter', 'Tools', 'Anti-Static', 'Lab Grade'],
    specs: {
      'Multimeter Type': 'True-RMS Auto-Ranging 6000 Counts',
      'Measurement': 'DC/AC Voltage, Resistance, Continuity, Diode',
      'Safety Rating': 'CAT III 600V',
      'Tools Included': 'Flush Cutters, ESD Tweezers, Desoldering Pump',
      'Case': 'Shockproof Zippered EVA Case'
    },
    whatsInside: [
      'True-RMS Digital Multimeter with Gold-Plated Probes',
      'Flush Wire Cutters (Spring Loaded)',
      '2x ESD Anti-Static Precision Tweezers',
      'High-Suction Aluminum Desoldering Pump',
      'Premium EVA Protective Carry Bag'
    ]
  }
]

// Store FAQs
const faqs = [
  {
    q: 'How do I pick up my hardware or receive delivery?',
    a: 'You can choose Free Same-Day Lab Pickup at AeroByte Academy in Ta Khmau / Phnom Penh, or express Grab/courier delivery across Phnom Penh ($1.50) and nationwide delivery across all provinces ($2.50).'
  },
  {
    q: 'Are these parts genuine and tested before shipping?',
    a: 'Yes. 100% of our microcontrollers, motors, and ESC stacks are authentic and pre-tested by AeroByte Academy engineers on our laboratory test benches to ensure zero defective parts.'
  },
  {
    q: 'Do you offer student and school lab bulk discounts?',
    a: 'Yes! AeroByte Academy students get 10% off using code AEROSTUDENT. For high school STEM clubs, universities, or bulk bills of materials, message our team directly on Telegram for educational pricing.'
  },
  {
    q: 'What payment methods do you accept?',
    a: 'We accept ABA KHQR, ACLEDA, Wing, and Cash on Delivery / Lab Pickup.'
  }
]

// Category Helper
function getCategoryIcon(cat) {
  switch (cat) {
    case 'Student Lab Kits': return '🤖'
    case 'FPV Drone Hardware': return '🚁'
    case 'Microcontrollers & Sensors': return '📡'
    case 'Brushless Motors & ESCs': return '⚙️'
    case 'Tools & Equipment': return '🔥'
    case '3D Filaments & Parts': return '🧵'
    default: return '📦'
  }
}

function countByCategory(cat) {
  return products.filter(p => p.category === cat).length
}

function getPriceLabel(id) {
  const opt = priceOptions.find(p => p.id === id)
  return opt ? t(opt.label) : id
}

// Active Filter Count
const activeFilterCount = computed(() => {
  let count = 0
  if (selectedCategory.value !== 'All') count++
  if (selectedPriceRange.value !== 'all') count++
  if (inStockOnly.value) count++
  if (selectedTag.value) count++
  if (searchQuery.value.trim() !== '') count++
  return count
})

function toggleTagFilter(tag) {
  selectedTag.value = selectedTag.value === tag ? '' : tag
}

function resetFilters() {
  searchQuery.value = ''
  selectedCategory.value = 'All'
  selectedPriceRange.value = 'all'
  inStockOnly.value = false
  selectedTag.value = ''
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

  // Tag filter
  if (selectedTag.value) {
    list = list.filter(p =>
      p.tags.some(t => t.toLowerCase().includes(selectedTag.value.toLowerCase()))
    )
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
  } else if (sortBy.value === 'reviews') {
    list.sort((a, b) => b.reviews - a.reviews)
  }

  return list
})

// Wishlist Favorites Management
function toggleFavorite(productId) {
  if (favorites.value.has(productId)) {
    favorites.value.delete(productId)
    showToast('Removed from favorites')
  } else {
    favorites.value.add(productId)
    showToast('Saved to your favorites')
  }
  persistFavorites()
}

function isFavorite(productId) {
  return favorites.value.has(productId)
}

// Shopping Cart Management
function addToCart(product) {
  const existing = cartItems.value.find(item => item.id === product.id)
  if (existing) {
    existing.quantity += 1
  } else {
    cartItems.value.push({
      ...product,
      quantity: 1
    })
  }
  persistCart()
  showToast(`Added ${product.name} to your bag!`)
}

function updateCartQuantity(productId, newQty) {
  if (newQty <= 0) {
    removeFromCart(productId)
    return
  }
  const item = cartItems.value.find(i => i.id === productId)
  if (item) {
    item.quantity = newQty
    persistCart()
  }
}

function removeFromCart(productId) {
  cartItems.value = cartItems.value.filter(i => i.id !== productId)
  persistCart()
}

const totalCartItemsCount = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + item.quantity, 0)
})

const cartSubtotalUsd = computed(() => {
  return cartItems.value.reduce((sum, item) => sum + item.priceUsd * item.quantity, 0)
})

const deliveryFeeUsd = computed(() => {
  if (selectedDeliveryMethod.value === 'phnom-penh') return 1.50
  if (selectedDeliveryMethod.value === 'province') return 2.50
  return 0.00
})

const cartTotalUsd = computed(() => {
  return cartSubtotalUsd.value + deliveryFeeUsd.value
})

// Toast helper
let toastTimeout = null
function showToast(msg) {
  toastMessage.value = msg
  if (toastTimeout) clearTimeout(toastTimeout)
  toastTimeout = setTimeout(() => {
    toastMessage.value = ''
  }, 2500)
}

// Quick View Modal
function openQuickView(product) {
  quickViewProduct.value = product
}

// Order Single Item Modal
function openOrder(item) {
  activeModalProduct.value = item
  orderQuantity.value = 1
  orderSubmitted.value = false
}

function openCheckoutModal() {
  isCartOpen.value = false
  isCheckoutModalOpen.value = true
  orderSubmitted.value = false
}

function closeOrderModal() {
  if (orderSubmitted.value && !activeModalProduct.value) {
    cartItems.value = []
    persistCart()
  }
  activeModalProduct.value = null
  isCheckoutModalOpen.value = false
  orderSubmitted.value = false
}

function submitOrder() {
  orderSubmitted.value = true
}

const currentModalPrice = computed(() => {
  if (activeModalProduct.value) {
    return activeModalProduct.value.priceUsd * orderQuantity.value
  }
  return cartTotalUsd.value
})

// Single Item Telegram Order Link
const telegramOrderLink = computed(() => {
  if (!activeModalProduct.value) return 'https://t.me/aerobyte_academy'
  const totalUsd = (activeModalProduct.value.priceUsd * orderQuantity.value).toFixed(2)
  const totalKhr = (activeModalProduct.value.priceUsd * orderQuantity.value * 4100).toLocaleString()
  const msg = encodeURIComponent(
    `Hello AeroByte Academy! I want to order from Aero Store:\n\n` +
    `🛒 Item: ${activeModalProduct.value.name}\n` +
    `📦 Quantity: ${orderQuantity.value}\n` +
    `💰 Total: $${totalUsd} (≈ ${totalKhr} KHR)\n\n` +
    `👤 Customer: ${orderForm.value.name || 'N/A'}\n` +
    `📞 Phone: ${orderForm.value.phone || 'N/A'}\n` +
    `💬 Telegram: ${orderForm.value.telegram || 'N/A'}\n` +
    `📍 Delivery / Pickup: ${orderForm.value.address || 'Ta Khmau Lab Pickup'}`
  )
  return `https://t.me/aerobyte_academy?text=${msg}`
})

// Multi-Item Cart Telegram Checkout Link
const cartTelegramCheckoutLink = computed(() => {
  if (cartItems.value.length === 0) return 'https://t.me/aerobyte_academy'
  const itemsText = cartItems.value
    .map(i => `• ${i.name} (x${i.quantity}) - $${(i.priceUsd * i.quantity).toFixed(2)}`)
    .join('\n')
  const totalKhr = (cartTotalUsd.value * 4100).toLocaleString()
  const deliveryLabel = selectedDeliveryMethod.value === 'pickup'
    ? 'Lab Pickup (Free)'
    : selectedDeliveryMethod.value === 'phnom-penh'
      ? 'Phnom Penh Express ($1.50)'
      : 'Provinces Courier ($2.50)'

  const msg = encodeURIComponent(
    `Hello AeroByte Academy! I want to order items from Aero Store:\n\n` +
    `${itemsText}\n\n` +
    `🚚 Delivery: ${deliveryLabel}\n` +
    `💰 Total Amount: $${cartTotalUsd.value.toFixed(2)} (≈ ${totalKhr} KHR)\n\n` +
    `👤 Name: ${orderForm.value.name || 'N/A'}\n` +
    `📞 Phone: ${orderForm.value.phone || 'N/A'}\n` +
    `📍 Address / Notes: ${orderForm.value.address || 'Ta Khmau Lab Pickup'}`
  )
  return `https://t.me/aerobyte_academy?text=${msg}`
})
</script>

<style scoped>
.no-scrollbar::-webkit-scrollbar {
  display: none;
}
.no-scrollbar {
  -ms-overflow-style: none;
  scrollbar-width: none;
}
</style>
