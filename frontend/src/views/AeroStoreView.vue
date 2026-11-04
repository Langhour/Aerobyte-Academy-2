<template>

  <div class="min-h-screen pb-24 bg-white dark:bg-slate-950 transition-colors">

    <!-- 2. Auto-Rotating Commercial Hero Showcase Banner (Changes every 3s) -->

    <section class="pt-4 pb-6 sm:pb-8 select-none">

      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">

        <div

          class="group relative w-full overflow-hidden rounded-2xl sm:rounded-3xl bg-[#102a49] shadow-xl border border-navy-800/80 aspect-[16/9] sm:aspect-[2.1/1] lg:aspect-[2.2/1] min-h-[380px] max-h-[540px] flex items-center"

          @mouseenter="pauseHeroCarousel"

          @mouseleave="resumeHeroCarousel"

        >

          <!-- Stacked Slides with Crossfade -->

          <div

            v-for="(slide, index) in heroSlides"

            :key="slide.id"

            class="absolute inset-0 w-full h-full transition-all duration-700 ease-in-out"

            :class="currentSlide === index ? 'opacity-100 z-10 pointer-events-auto scale-100' : 'opacity-0 z-0 pointer-events-none scale-105'"

          >

            <!-- Background Showcase Image (Staged Products on Left, Deep Navy Space on Right) -->

            <img

              :src="slide.image"

              :alt="slide.alt"

              class="absolute inset-0 w-full h-full object-cover object-left select-none pointer-events-none"

            />



            <!-- Content Grid overlaying the banner -->

            <div class="relative z-10 w-full px-6 sm:px-10 lg:px-14 py-8 sm:py-12 grid grid-cols-1 lg:grid-cols-12 gap-6 sm:gap-8 items-center h-full">

              <!-- Left spacer so all staged products remain completely visible without overlap -->

              <div class="hidden lg:block lg:col-span-6 xl:col-span-6 pointer-events-none"></div>



              <!-- Right: Big Punchy Typography & Action Button -->

              <div class="lg:col-span-6 xl:col-span-6 flex flex-col items-center justify-center text-center">

                


                <h1 class="text-3xl sm:text-5xl md:text-5xl lg:text-[54px] xl:text-[64px] font-black text-white tracking-tight uppercase leading-[1.05] drop-shadow-lg select-none">

                  <span class="whitespace-nowrap">{{ slide.title1 }}</span><br />

                  <span>{{ slide.title2 }}</span>

                </h1>



                <!-- Action Pill Button -->

                <button

                  type="button"

                  @click="selectSlideCategory(slide.category)"

                  class="mt-5 sm:mt-7 inline-flex items-center justify-center px-8 sm:px-11 py-3 sm:py-3.5 rounded-full font-black text-xs sm:text-sm uppercase tracking-wider shadow-2xl hover:scale-105 active:scale-95 transition-all duration-200 cursor-pointer"

                  :class="slide.btnClass"

                >

                  {{ t(slide.buttonText) }}

                </button>

              </div>

            </div>

          </div>



          <!-- Left Arrow Navigation Button -->

          <button

            type="button"

            @click="prevSlide"

            class="absolute left-3 sm:left-5 top-1/2 -translate-y-1/2 z-20 flex h-9 w-9 sm:h-11 sm:w-11 items-center justify-center rounded-full bg-black/30 hover:bg-black/60 text-white/80 hover:text-white backdrop-blur-md border border-white/10 opacity-0 group-hover:opacity-100 transition-all duration-200 cursor-pointer active:scale-95"

            aria-label="Previous slide"

          >

            <ChevronLeft class="h-5 w-5 sm:h-6 sm:w-6" />

          </button>



          <!-- Right Arrow Navigation Button -->

          <button

            type="button"

            @click="nextSlide"

            class="absolute right-3 sm:right-5 top-1/2 -translate-y-1/2 z-20 flex h-9 w-9 sm:h-11 sm:w-11 items-center justify-center rounded-full bg-black/30 hover:bg-black/60 text-white/80 hover:text-white backdrop-blur-md border border-white/10 opacity-0 group-hover:opacity-100 transition-all duration-200 cursor-pointer active:scale-95"

            aria-label="Next slide"

          >

            <ChevronRight class="h-5 w-5 sm:h-6 sm:w-6" />

          </button>



          <!-- Carousel Pagination Pill Indicators -->

          <div class="absolute bottom-4 sm:bottom-6 left-1/2 -translate-x-1/2 z-20 flex items-center gap-2 px-3 py-1.5 rounded-full bg-black/30 backdrop-blur-md border border-white/10">

            <button

              v-for="(slide, idx) in heroSlides"

              :key="slide.id"

              type="button"

              @click="goToSlide(idx)"

              class="h-2 rounded-full transition-all duration-300 cursor-pointer"

              :class="currentSlide === idx ? 'w-8 bg-amber-400 shadow-sm' : 'w-2 bg-white/40 hover:bg-white/70'"

              :aria-label="`Slide ${idx + 1}`"

            />

          </div>



          <!-- Bottom Auto-Play Progress Bar (3s cycle) -->

          <div class="absolute bottom-0 left-0 right-0 h-1 bg-white/10 z-20 overflow-hidden">

            <div

              :key="slideKey"

              class="h-full bg-amber-400 transition-all duration-100 ease-linear"

              :style="{ width: `${slideProgress}%` }"

            ></div>

          </div>



        </div>

      </div>

    </section>



    <!-- Header & Brand Bar -->

    <header id="catalog" class="border-b border-slate-100 dark:border-slate-800/80 pt-8 pb-6">

      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">

        <div class="flex flex-col md:flex-row md:items-end justify-between gap-6">

          <div>

            <div class="flex items-center gap-2 mb-2">

              <span class="text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">

                AEROBYTE ACADEMY • STORE

              </span>

              <span class="h-1 w-1 rounded-full bg-slate-300 dark:bg-slate-700"></span>

              <span class="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400">

                {{ products.length }} {{ t('Products') }}

              </span>

            </div>

            <h1 class="text-3xl sm:text-4xl md:text-5xl font-black tracking-tight text-slate-900 dark:text-white">

              {{ t('Hardware & Kits') }}

            </h1>

            <p class="mt-2 text-sm sm:text-base text-slate-500 dark:text-slate-400 max-w-2xl leading-relaxed">

              {{ t('Official hardware store for authentic robotics learning kits, drone parts, microcontrollers, brushless motors, and lab tools.') }}

            </p>

          </div>



          <!-- Minimalist Search Input -->

          <div class="w-full md:w-80 relative">

            <Search class="pointer-events-none absolute left-3.5 top-1/2 -translate-y-1/2 h-4 w-4 text-slate-400" />

            <input

              v-model="searchQuery"

              type="text"

              :placeholder="t('Search products...')"

              class="w-full rounded-full border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 py-2.5 pl-10 pr-9 text-xs sm:text-sm text-slate-900 dark:text-white placeholder:text-slate-400 focus:border-slate-400 dark:focus:border-slate-600 focus:outline-none transition"

            />

            <button

              v-if="searchQuery"

              type="button"

              @click="searchQuery = ''"

              class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-700 dark:hover:text-white"

            >

              <X class="w-3.5 h-3.5" />

            </button>

          </div>

        </div>



        <!-- Backdrop to close dropdowns when clicking outside (100% transparent, no blur) -->
        <div
          v-if="isSortDropdownOpen || isPriceDropdownOpen"
          class="fixed inset-0 z-40 bg-transparent cursor-default"
          @click="closeDropdowns"
        ></div>

        <!-- Shop.com Quick Filters Row (Exact Match to Reference Screenshots) -->
        <div class="mt-5 flex flex-wrap items-center justify-between gap-3 relative z-30 overflow-visible py-1">
          <div class="flex items-center gap-2 sm:gap-2.5 shrink-0">
            <!-- 1. Circular Filter Icon Button (Opens Filters Modal - Image 1) -->
            <button
              type="button"
              @click="openFiltersModal"
              :title="t('Filters')"
              class="h-9 w-9 sm:h-10 sm:w-10 rounded-full flex items-center justify-center transition-all cursor-pointer relative shrink-0 active:scale-95"
              :class="activeFiltersCount > 0
                ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 shadow-sm'
                : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-750 text-slate-700 dark:text-slate-300 border border-slate-200/70 dark:border-slate-700/70'"
            >
              <SlidersHorizontal class="w-4 h-4" />
              <span
                v-if="activeFiltersCount > 0"
                class="absolute -top-1 -right-1 h-4 w-4 rounded-full bg-rose-500 text-white text-[10px] font-extrabold flex items-center justify-center shadow-xs"
              >
                {{ activeFiltersCount }}
              </span>
            </button>

            <!-- 2. Sort by Dropdown Pill (Image 2) -->
            <div class="relative filter-dropdown-container" :class="{ 'z-50': isSortDropdownOpen }">
              <button
                type="button"
                @click.stop="toggleSortDropdown"
                class="h-9 sm:h-10 px-4 rounded-full text-xs sm:text-[13px] font-semibold flex items-center gap-1.5 transition-all cursor-pointer whitespace-nowrap active:scale-95 select-none"
                :class="sortBy !== 'featured' && sortBy !== 'best-selling'
                  ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 shadow-sm'
                  : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-750 text-slate-700 dark:text-slate-200 border border-slate-200/70 dark:border-slate-700/70'"
              >
                <span>{{ sortLabel }}</span>
                <ChevronDown class="w-3.5 h-3.5 transition-transform duration-200" :class="{ 'rotate-180': isSortDropdownOpen }" />
              </button>

              <!-- Sort Dropdown Menu (Matching Shop.com Image 2) -->
              <transition
                enter-active-class="transition ease-out duration-150"
                enter-from-class="transform opacity-0 scale-95"
                enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-100"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95"
              >
                <div
                  v-if="isSortDropdownOpen"
                  class="absolute top-full left-0 mt-2 z-50 w-72 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xl p-4 space-y-3"
                >
                  <div class="space-y-2.5">
                    <label
                      v-for="opt in sortOptions"
                      :key="opt.value"
                      @click="sortBy = opt.value"
                      class="flex items-center justify-between text-xs sm:text-[13px] font-medium text-slate-800 dark:text-slate-200 cursor-pointer select-none py-1 hover:text-slate-950 dark:hover:text-white"
                    >
                      <span>{{ opt.label }}</span>
                      <div
                        class="h-4 w-4 rounded-full border flex items-center justify-center transition-all"
                        :class="sortBy === opt.value
                          ? 'border-slate-900 dark:border-white'
                          : 'border-slate-300 dark:border-slate-600'"
                      >
                        <div
                          v-if="sortBy === opt.value"
                          class="h-2 w-2 rounded-full bg-slate-900 dark:bg-white"
                        ></div>
                      </div>
                      <input
                        type="radio"
                        name="sort-option"
                        :value="opt.value"
                        v-model="sortBy"
                        class="sr-only"
                      />
                    </label>
                  </div>

                  <!-- Footer Buttons -->
                  <div class="mt-3 flex items-center justify-between gap-2.5 pt-3 border-t border-slate-100 dark:border-slate-800">
                    <button
                      type="button"
                      @click="sortBy = 'best-selling'"
                      class="flex-1 py-2 px-3 rounded-full text-xs font-bold bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-300 transition cursor-pointer text-center"
                    >
                      {{ t('Reset') }}
                    </button>
                    <button
                      type="button"
                      @click="isSortDropdownOpen = false"
                      class="flex-1 py-2 px-3 rounded-full text-xs font-bold bg-slate-900 hover:bg-slate-800 text-white dark:bg-white dark:text-slate-900 transition cursor-pointer text-center"
                    >
                      {{ t('Done') }}
                    </button>
                  </div>
                </div>
              </transition>
            </div>

            <!-- 3. On sale Toggle Pill -->
            <button
              type="button"
              @click="onSaleOnly = !onSaleOnly"
              class="h-9 sm:h-10 px-4 rounded-full text-xs sm:text-[13px] font-semibold flex items-center gap-1.5 transition-all cursor-pointer whitespace-nowrap active:scale-95 select-none"
              :class="onSaleOnly
                ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 shadow-sm border border-slate-900 dark:border-white font-bold'
                : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-750 text-slate-700 dark:text-slate-200 border border-slate-200/70 dark:border-slate-700/70'"
            >
              <span>{{ t('On sale') }}</span>
            </button>

            <!-- 4. Price Dropdown Pill (Image 3) -->
            <div class="relative filter-dropdown-container" :class="{ 'z-50': isPriceDropdownOpen }">
              <button
                type="button"
                @click.stop="togglePriceDropdown"
                class="h-9 sm:h-10 px-4 rounded-full text-xs sm:text-[13px] font-semibold flex items-center gap-1.5 transition-all cursor-pointer whitespace-nowrap active:scale-95 select-none"
                :class="priceMin > 0 || priceMax < 100
                  ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 shadow-sm font-bold'
                  : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-750 text-slate-700 dark:text-slate-200 border border-slate-200/70 dark:border-slate-700/70'"
              >
                <span>{{ priceLabel }}</span>
                <ChevronDown class="w-3.5 h-3.5 transition-transform duration-200" :class="{ 'rotate-180': isPriceDropdownOpen }" />
              </button>

              <!-- Price Dropdown Menu (Matching Shop.com Image 3) -->
              <transition
                enter-active-class="transition ease-out duration-150"
                enter-from-class="transform opacity-0 scale-95"
                enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-100"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95"
              >
                <div
                  v-if="isPriceDropdownOpen"
                  class="absolute top-full left-0 mt-2 z-50 w-72 sm:w-80 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xl p-5 space-y-4"
                >
                  <!-- Purple Dual Slider -->
                  <div class="space-y-2">
                    <div class="relative w-full h-8 flex items-center select-none my-1">
                      <div class="absolute left-0 right-0 h-1.5 rounded-full bg-slate-200 dark:bg-slate-700"></div>
                      <div
                        class="absolute h-1.5 rounded-full bg-indigo-600"
                        :style="{
                          left: `${(priceMin / 100) * 100}%`,
                          right: `${100 - (priceMax / 100) * 100}%`
                        }"
                      ></div>
                      <input
                        type="range"
                        min="0"
                        max="100"
                        step="1"
                        v-model.number="priceMin"
                        @input="handlePriceMinChange"
                        class="shop-range-input z-10"
                      />
                      <input
                        type="range"
                        min="0"
                        max="100"
                        step="1"
                        v-model.number="priceMax"
                        @input="handlePriceMaxChange"
                        class="shop-range-input z-20"
                      />
                    </div>

                    <!-- Min & Max Input Boxes -->
                    <div class="flex items-center gap-3">
                      <div class="flex-1 flex items-center justify-center rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 px-3 py-2">
                        <span class="text-xs text-slate-400 mr-1">$</span>
                        <input
                          type="number"
                          min="0"
                          :max="priceMax"
                          v-model.number="priceMin"
                          class="w-full text-center text-xs sm:text-sm font-semibold bg-transparent focus:outline-none text-slate-800 dark:text-slate-100"
                        />
                      </div>
                      <span class="text-slate-400 font-bold">—</span>
                      <div class="flex-1 flex items-center justify-center rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 px-3 py-2">
                        <span class="text-xs text-slate-400 mr-1">$</span>
                        <input
                          type="number"
                          :min="priceMin"
                          max="100"
                          v-model.number="priceMax"
                          class="w-full text-center text-xs sm:text-sm font-semibold bg-transparent focus:outline-none text-slate-800 dark:text-slate-100"
                        />
                        <span v-if="priceMax >= 100" class="text-xs font-bold text-slate-400 ml-0.5">+</span>
                      </div>
                    </div>

                    <!-- Quick Price Presets -->
                    <div class="flex items-center gap-1.5 pt-1">
                      <button
                        type="button"
                        @click="priceMin = 0; priceMax = 25"
                        class="flex-1 py-1 px-2 rounded-full text-[11px] font-semibold transition cursor-pointer text-center"
                        :class="priceMin === 0 && priceMax === 25 ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 font-bold shadow-xs' : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700'"
                      >
                        {{ t('Under $25') }}
                      </button>
                      <button
                        type="button"
                        @click="priceMin = 25; priceMax = 50"
                        class="flex-1 py-1 px-2 rounded-full text-[11px] font-semibold transition cursor-pointer text-center"
                        :class="priceMin === 25 && priceMax === 50 ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 font-bold shadow-xs' : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700'"
                      >
                        $25 - $50
                      </button>
                      <button
                        type="button"
                        @click="priceMin = 50; priceMax = 100"
                        class="flex-1 py-1 px-2 rounded-full text-[11px] font-semibold transition cursor-pointer text-center"
                        :class="priceMin === 50 && priceMax === 100 ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 font-bold shadow-xs' : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700'"
                      >
                        {{ t('Over $50') }}
                      </button>
                    </div>
                  </div>

                  <!-- Footer Buttons -->
                  <div class="mt-2 flex items-center justify-between gap-2.5 pt-3 border-t border-slate-100 dark:border-slate-800">
                    <button
                      type="button"
                      @click="resetPriceFilter"
                      class="flex-1 py-2 px-3 rounded-full text-xs font-bold bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-750 text-slate-700 dark:text-slate-300 transition cursor-pointer text-center"
                    >
                      {{ t('Reset') }}
                    </button>
                    <button
                      type="button"
                      @click="isPriceDropdownOpen = false"
                      class="flex-1 py-2 px-3 rounded-full text-xs font-bold bg-slate-900 hover:bg-slate-800 text-white dark:bg-white dark:text-slate-900 transition cursor-pointer text-center"
                    >
                      {{ t('Done') }}
                    </button>
                  </div>
                </div>
              </transition>
            </div>

            <!-- 5. In-stock Toggle Pill -->
            <button
              type="button"
              @click="inStockOnly = !inStockOnly"
              class="h-9 sm:h-10 px-4 rounded-full text-xs sm:text-[13px] font-semibold flex items-center gap-1.5 transition-all cursor-pointer whitespace-nowrap active:scale-95 select-none"
              :class="inStockOnly
                ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 shadow-sm border border-slate-900 dark:border-white font-bold'
                : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-750 text-slate-700 dark:text-slate-200 border border-slate-200/70 dark:border-slate-700/70'"
            >
              <span>{{ t('In-stock') }}</span>
            </button>

            <!-- 6. Active Category Pill (If Selected) -->
            <button
              v-if="selectedCategory !== 'All'"
              type="button"
              @click="selectedCategory = 'All'"
              class="h-9 sm:h-10 px-4 rounded-full text-xs sm:text-[13px] font-semibold flex items-center gap-2 transition-all cursor-pointer whitespace-nowrap active:scale-95 select-none bg-slate-900 text-white dark:bg-white dark:text-slate-900 shadow-sm"
              :title="t('Click to clear category')"
            >
              <span>{{ t(selectedCategory) }}</span>
              <X class="w-3.5 h-3.5 opacity-70 hover:opacity-100" />
            </button>
          </div>

          <!-- Active Filters Summary & Reset -->
          <div v-if="activeFiltersCount > 0" class="flex items-center gap-2 shrink-0 text-xs">
            <button
              type="button"
              @click="resetFilters"
              class="text-xs font-semibold text-slate-500 hover:text-slate-900 dark:hover:text-white transition cursor-pointer underline flex items-center gap-1"
            >
              <X class="w-3.5 h-3.5" />
              <span>{{ t('Clear all') }} ({{ activeFiltersCount }})</span>
            </button>
          </div>
        </div>

      </div>

    </header>

    <!-- Full Filters Modal (Matching Shop.com Reference Image 1) -->
    <Teleport to="body">
      <transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition ease-in duration-150"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="isFiltersModalOpen"
          class="fixed inset-0 z-50 flex items-center justify-center p-4 sm:p-6"
        >
          <!-- Backdrop -->
          <div
            class="fixed inset-0 bg-slate-900/50 backdrop-blur-xs transition-opacity"
            @click="isFiltersModalOpen = false"
          ></div>

          <!-- Modal Card -->
          <div
            class="relative w-full max-w-md rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xl p-6 sm:p-7 overflow-hidden z-10"
          >
            <!-- Header -->
            <div class="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-slate-800">
              <h2 class="text-lg sm:text-xl font-bold text-slate-900 dark:text-white">{{ t('Filters') }}</h2>
              <button
                type="button"
                @click="isFiltersModalOpen = false"
                class="h-9 w-9 rounded-full bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 flex items-center justify-center text-slate-600 dark:text-slate-300 transition cursor-pointer"
              >
                <X class="w-4 h-4" />
              </button>
            </div>

            <div class="py-5 space-y-6 max-h-[72vh] overflow-y-auto no-scrollbar">
              <!-- 1. Quick Toggles (On sale, In-stock) -->
              <div class="flex items-center gap-2.5">
                <button
                  type="button"
                  @click="onSaleOnly = !onSaleOnly"
                  class="h-9 px-4 rounded-full text-xs font-semibold transition active:scale-95 cursor-pointer"
                  :class="onSaleOnly
                    ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 font-bold shadow-xs'
                    : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-750 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700'"
                >
                  {{ t('On sale') }}
                </button>
                <button
                  type="button"
                  @click="inStockOnly = !inStockOnly"
                  class="h-9 px-4 rounded-full text-xs font-semibold transition active:scale-95 cursor-pointer"
                  :class="inStockOnly
                    ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 font-bold shadow-xs'
                    : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-750 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700'"
                >
                  {{ t('In-stock') }}
                </button>
              </div>

              <!-- Categories Section -->
              <div class="space-y-3">
                <div class="flex items-center justify-between">
                  <h3 class="text-xs font-bold text-slate-500 uppercase tracking-wider">{{ t('Categories') }}</h3>
                  <span v-if="selectedCategory !== 'All'" class="text-[11px] font-semibold text-slate-400">
                    {{ t(selectedCategory) }}
                  </span>
                </div>
                <div class="flex flex-wrap gap-2">
                  <button
                    type="button"
                    @click="selectedCategory = 'All'"
                    class="h-9 px-3.5 rounded-full text-xs font-semibold transition active:scale-95 cursor-pointer whitespace-nowrap"
                    :class="selectedCategory === 'All'
                      ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 font-bold shadow-xs'
                      : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-750 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700'"
                  >
                    {{ t('All') }} ({{ products.length }})
                  </button>
                  <button
                    v-for="cat in categoryList"
                    :key="cat"
                    type="button"
                    @click="selectedCategory = cat"
                    class="h-9 px-3.5 rounded-full text-xs font-semibold transition active:scale-95 cursor-pointer whitespace-nowrap"
                    :class="selectedCategory === cat
                      ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 font-bold shadow-xs'
                      : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-750 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700'"
                  >
                    {{ t(cat) }}
                  </button>
                </div>
              </div>

              <!-- 2. Sort by Pills -->
              <div class="space-y-3">
                <h3 class="text-xs font-bold text-slate-500 uppercase tracking-wider">{{ t('Sort by') }}</h3>
                <div class="flex flex-wrap gap-2">
                  <button
                    v-for="opt in sortOptions"
                    :key="opt.value"
                    type="button"
                    @click="sortBy = opt.value"
                    class="h-9 px-3.5 rounded-full text-xs font-semibold transition active:scale-95 cursor-pointer"
                    :class="sortBy === opt.value
                      ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 font-bold shadow-xs'
                      : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-750 text-slate-700 dark:text-slate-300 border border-slate-200 dark:border-slate-700'"
                  >
                    {{ opt.label }}
                  </button>
                </div>
              </div>

              <!-- 3. Price Dual Slider -->
              <div class="space-y-3">
                <h3 class="text-xs font-bold text-slate-500 uppercase tracking-wider">{{ t('Price') }}</h3>
                
                <div class="relative w-full h-8 flex items-center select-none my-1">
                  <div class="absolute left-0 right-0 h-1.5 rounded-full bg-slate-200 dark:bg-slate-700"></div>
                  <div
                    class="absolute h-1.5 rounded-full bg-indigo-600"
                    :style="{
                      left: `${(priceMin / 100) * 100}%`,
                      right: `${100 - (priceMax / 100) * 100}%`
                    }"
                  ></div>
                  <input
                    type="range"
                    min="0"
                    max="100"
                    step="1"
                    v-model.number="priceMin"
                    @input="handlePriceMinChange"
                    class="shop-range-input z-10"
                  />
                  <input
                    type="range"
                    min="0"
                    max="100"
                    step="1"
                    v-model.number="priceMax"
                    @input="handlePriceMaxChange"
                    class="shop-range-input z-20"
                  />
                </div>

                <div class="flex items-center gap-3 pt-1">
                  <div class="flex-1 flex items-center justify-center rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 px-3 py-2">
                    <span class="text-xs text-slate-400 mr-1">$</span>
                    <input
                      type="number"
                      min="0"
                      :max="priceMax"
                      v-model.number="priceMin"
                      class="w-full text-center text-xs sm:text-sm font-semibold bg-transparent focus:outline-none text-slate-800 dark:text-slate-100"
                    />
                  </div>
                  <span class="text-slate-400 font-bold">—</span>
                  <div class="flex-1 flex items-center justify-center rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50/50 dark:bg-slate-800/50 px-3 py-2">
                    <span class="text-xs text-slate-400 mr-1">$</span>
                    <input
                      type="number"
                      :min="priceMin"
                      max="100"
                      v-model.number="priceMax"
                      class="w-full text-center text-xs sm:text-sm font-semibold bg-transparent focus:outline-none text-slate-800 dark:text-slate-100"
                    />
                    <span v-if="priceMax >= 100" class="text-xs font-bold text-slate-400 ml-0.5">+</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Footer Actions -->
            <div class="flex items-center gap-3 pt-4 border-t border-slate-100 dark:border-slate-800">
              <button
                type="button"
                @click="resetFilters"
                class="flex-1 py-2.5 px-4 rounded-full text-xs font-bold bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-750 text-slate-700 dark:text-slate-300 transition cursor-pointer text-center"
              >
                {{ t('Reset') }}
              </button>
              <button
                type="button"
                @click="isFiltersModalOpen = false"
                class="flex-1 py-2.5 px-4 rounded-full text-xs font-bold bg-slate-900 hover:bg-slate-800 text-white dark:bg-white dark:text-slate-900 transition cursor-pointer text-center"
              >
                {{ t('Done') }}
              </button>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>



    <!-- Main Content Grid Area -->

    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-8 sm:pt-10">

      

      <!-- Empty State -->

      <div

        v-if="filteredProducts.length === 0"

        class="py-24 text-center"

      >

        <div class="text-4xl mb-3">🔍</div>

        <h3 class="text-base font-bold text-slate-900 dark:text-white">

          {{ t('No products match your selected filters') }}

        </h3>

        <p class="text-xs text-slate-500 dark:text-slate-400 mt-1 max-w-sm mx-auto">

          {{ t('Try searching for a different keyword or resetting your filters.') }}

        </p>

        <button

          type="button"

          @click="resetFilters"

          class="mt-4 px-4 py-2 rounded-full bg-slate-900 text-white dark:bg-white dark:text-slate-900 text-xs font-bold transition cursor-pointer"

        >

          {{ t('Reset Filters') }}

        </button>

      </div>



      <!-- THE PRODUCT CARDS GRID (Matches Reference Screenshot Style) -->

      <div

        v-else

        class="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-4 xl:grid-cols-5 gap-4 sm:gap-5 lg:gap-6"

      >

        <div

          v-for="item in filteredProducts"

          :key="item.id"

          class="group flex flex-col justify-between"

        >

          <!-- 1. The Rounded Visual Card Box (Matches Screenshot) -->
          <div
            class="relative aspect-[4/5] w-full rounded-[20px] sm:rounded-[24px] bg-[#f5f5f7] dark:bg-slate-850/80 border border-slate-200/50 dark:border-slate-800/60 p-4 sm:p-6 flex items-center justify-center overflow-hidden transition-all duration-300 hover:shadow-md select-none"
          >
            <!-- Centered Floating Hardware / Product Visual Link -->
            <RouterLink
              :to="`/store/${item.id}`"
              class="absolute inset-0 flex items-center justify-center text-6xl sm:text-7xl group-hover:scale-108 transition-transform duration-300 drop-shadow-sm z-10 cursor-pointer"
            >
              <span>{{ item.icon }}</span>
            </RouterLink>

            <!-- Hover Action Buttons (Add to Cart & Heart Favorite - Visible on Hover) -->
            <div class="absolute bottom-3 right-3 z-20 flex items-center gap-1.5 transition-all duration-300 pointer-events-auto">
              <!-- Add to Cart Icon Button -->
              <button
                type="button"
                @click.stop.prevent="addToCart(item)"
                :title="t('Add to Bag')"
                class="h-7 w-7 sm:h-8 sm:w-8 rounded-full bg-slate-900 hover:bg-slate-800 text-white flex items-center justify-center shadow-md transition-all duration-200 cursor-pointer active:scale-90 transform translate-y-1 sm:translate-y-2 group-hover:translate-y-0 opacity-90 sm:opacity-0 sm:group-hover:opacity-100"
              >
                <ShoppingCart class="w-3.5 h-3.5 sm:w-4 sm:h-4" />
              </button>

              <!-- Heart Favorite Icon Button -->
              <button
                type="button"
                @click.stop.prevent="toggleFavorite(item.id)"
                :title="t('Favorite')"
                class="h-7 w-7 sm:h-8 sm:w-8 rounded-full flex items-center justify-center shadow-md transition-all duration-200 cursor-pointer active:scale-90 transform translate-y-1 sm:translate-y-2 group-hover:translate-y-0"
                :class="isFavorite(item.id)
                  ? 'opacity-100 translate-y-0 bg-red-500 text-white'
                  : 'opacity-90 sm:opacity-0 sm:group-hover:opacity-100 bg-slate-400/80 hover:bg-slate-500 text-white backdrop-blur-xs'"
              >
                <Heart class="w-3.5 h-3.5 sm:w-4 sm:h-4" :class="{ 'fill-white': isFavorite(item.id) }" />
              </button>
            </div>
          </div>

          <!-- 2. Typography & Details BELOW the Card (Matches Reference Screenshot) -->

          <div class="mt-2.5 sm:mt-3 px-0.5 space-y-0.5">

            <!-- Brand / Category Name (Subtle muted gray text, line 1) -->

            <div class="text-[11px] sm:text-xs font-medium text-slate-400 dark:text-slate-500 truncate">

              {{ item.brand || item.category }}

            </div>



            <!-- Product Title (Bold clean typography, line 2) -->

            <RouterLink
              :to="`/store/${item.id}`"


              class="text-xs sm:text-sm font-bold text-slate-900 dark:text-white line-clamp-1 hover:text-indigo-600 dark:hover:text-indigo-400 transition cursor-pointer block"

            >

              {{ item.name }}

            </RouterLink>



            <!-- Star Rating Row: Solid black stars + review count (line 3) -->

            <div class="flex items-center gap-1 text-[11px] sm:text-xs text-slate-900 dark:text-slate-100 font-bold">

              <span class="tracking-tighter">★★★★★</span>

              <span class="font-normal text-slate-500 dark:text-slate-400">({{ item.reviewsCount || item.reviews }})</span>

            </div>



            <!-- Clean Price (line 4) -->

            <div class="pt-0.5 flex items-baseline gap-1.5 text-xs sm:text-sm font-bold text-slate-900 dark:text-white">
              <span>${{ item.priceUsd.toFixed(2) }}</span>
              <span v-if="item.originalPriceUsd" class="text-[11px] text-slate-400 line-through font-normal">
                ${{ item.originalPriceUsd.toFixed(2) }}
              </span>
              <span v-if="item.onSale" class="text-[10px] font-black text-rose-500 uppercase">
                {{ t('Sale') }}
              </span>
              <span class="text-[10px] sm:text-[11px] font-normal text-slate-400">
                · {{ (item.priceUsd * 4100).toLocaleString() }}៛
              </span></div>

          </div>

        </div>

      </div>

    </main>



    <!-- Slide-Over Shopping Bag Drawer -->

    <div

      v-if="isCartOpen"

      class="fixed inset-0 z-50 overflow-hidden"

    >

      <div

        class="absolute inset-0 bg-slate-950/50 backdrop-blur-xs transition-opacity"

        @click="isCartOpen = false"

      ></div>



      <div class="fixed inset-y-0 right-0 max-w-full flex pl-10">

        <div class="w-screen max-w-md bg-white dark:bg-slate-900 shadow-2xl flex flex-col justify-between border-l border-slate-200 dark:border-slate-800">

          <!-- Drawer Header -->

          <div class="p-5 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">

            <div class="flex items-center gap-2">

              <ShoppingBag class="w-5 h-5 text-slate-900 dark:text-white" />

              <div>

                <h3 class="text-sm font-bold text-slate-900 dark:text-white">{{ t('Shopping Bag') }}</h3>

                <p class="text-[11px] text-slate-400">{{ totalCartItemsCount }} {{ t('item(s)') }}</p>

              </div>

            </div>



            <button

              type="button"

              @click="isCartOpen = false"

              class="p-2 text-slate-400 hover:text-slate-700 dark:hover:text-white cursor-pointer"

            >

              <X class="w-5 h-5" />

            </button>

          </div>



          <!-- Drawer Body: Empty or Items List -->

          <div class="flex-1 overflow-y-auto p-5 space-y-4">

            <div v-if="cartItems.length === 0" class="text-center py-20">

              <div class="text-4xl mb-3">🛍️</div>

              <h4 class="text-sm font-bold text-slate-900 dark:text-white">{{ t('Your Bag is Empty') }}</h4>

              <p class="text-xs text-slate-400 mt-1 max-w-xs mx-auto">

                Explore our authentic robotics kits, drone parts, and 3D filaments to start building.

              </p>

            </div>



            <div v-else class="space-y-3">

              <div

                v-for="item in cartItems"

                :key="item.id"

                class="flex items-center gap-3 p-3 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800"

              >

                <div class="h-14 w-14 rounded-xl bg-white dark:bg-slate-800 flex items-center justify-center text-2xl shrink-0 border border-slate-200/60 dark:border-slate-700/60">

                  {{ item.icon }}

                </div>



                <div class="flex-1 min-w-0">

                  <div class="text-[10px] text-slate-400 font-medium">{{ item.brand || item.category }}</div>

                  <h4 class="text-xs font-bold text-slate-900 dark:text-white truncate">{{ item.name }}</h4>

                  <div class="text-xs font-bold text-slate-900 dark:text-white mt-0.5">

                    ${{ (item.priceUsd * item.quantity).toFixed(2) }}

                  </div>



                  <!-- Stepper -->

                  <div class="flex items-center gap-2 mt-2">

                    <button

                      type="button"

                      @click="updateCartQuantity(item.id, item.quantity - 1)"

                      class="h-6 w-6 rounded-full border border-slate-200 dark:border-slate-700 flex items-center justify-center text-xs font-bold hover:bg-slate-100 dark:hover:bg-slate-700 cursor-pointer"

                    >-</button>

                    <span class="text-xs font-bold text-slate-800 dark:text-white w-6 text-center">{{ item.quantity }}</span>

                    <button

                      type="button"

                      @click="updateCartQuantity(item.id, item.quantity + 1)"

                      class="h-6 w-6 rounded-full border border-slate-200 dark:border-slate-700 flex items-center justify-center text-xs font-bold hover:bg-slate-100 dark:hover:bg-slate-700 cursor-pointer"

                    >+</button>

                  </div>

                </div>



                <button

                  type="button"

                  @click="removeFromCart(item.id)"

                  class="p-1.5 text-slate-400 hover:text-red-500 transition cursor-pointer"

                >

                  <Trash2 class="w-4 h-4" />

                </button>

              </div>



              <!-- Delivery Preference Selector -->

              <div class="mt-6 pt-4 border-t border-slate-100 dark:border-slate-800 space-y-2">

                <label class="block text-xs font-bold text-slate-900 dark:text-white">{{ t('Delivery Method') }}</label>

                <div class="grid grid-cols-1 gap-2">

                  <label

                    class="flex items-center justify-between p-2.5 rounded-xl border cursor-pointer transition text-xs"

                    :class="selectedDeliveryMethod === 'pickup'

                      ? 'border-slate-900 dark:border-white bg-slate-50 dark:bg-slate-800 font-bold'

                      : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/50'"

                  >

                    <div class="flex items-center gap-2">

                      <input type="radio" value="pickup" v-model="selectedDeliveryMethod" class="text-slate-900" />

                      <span>🏢 {{ t('AeroByte Lab Pickup') }}</span>

                    </div>

                    <span class="text-emerald-600 dark:text-emerald-400 font-bold text-[11px]">{{ t('Free') }}</span>

                  </label>



                  <label

                    class="flex items-center justify-between p-2.5 rounded-xl border cursor-pointer transition text-xs"

                    :class="selectedDeliveryMethod === 'phnom-penh'

                      ? 'border-slate-900 dark:border-white bg-slate-50 dark:bg-slate-800 font-bold'

                      : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/50'"

                  >

                    <div class="flex items-center gap-2">

                      <input type="radio" value="phnom-penh" v-model="selectedDeliveryMethod" class="text-slate-900" />

                      <span>🛵 {{ t('Phnom Penh Express') }}</span>

                    </div>

                    <span class="font-bold text-[11px] text-slate-700 dark:text-slate-300">+$1.50</span>

                  </label>



                  <label

                    class="flex items-center justify-between p-2.5 rounded-xl border cursor-pointer transition text-xs"

                    :class="selectedDeliveryMethod === 'province'

                      ? 'border-slate-900 dark:border-white bg-slate-50 dark:bg-slate-800 font-bold'

                      : 'border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/50'"

                  >

                    <div class="flex items-center gap-2">

                      <input type="radio" value="province" v-model="selectedDeliveryMethod" class="text-slate-900" />

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

            <div class="space-y-1 text-xs">

              <div class="flex items-center justify-between text-slate-500 dark:text-slate-400">

                <span>{{ t('Items Subtotal') }}:</span>

                <span class="font-bold text-slate-900 dark:text-white">${{ cartSubtotalUsd.toFixed(2) }}</span>

              </div>

              <div class="flex items-center justify-between text-slate-500 dark:text-slate-400">

                <span>{{ t('Delivery Fee') }}:</span>

                <span class="font-bold text-slate-900 dark:text-white">

                  {{ deliveryFeeUsd === 0 ? t('Free') : `$${deliveryFeeUsd.toFixed(2)}` }}

                </span>

              </div>

              <div class="pt-2 border-t border-slate-200 dark:border-slate-800 flex items-center justify-between text-base font-black text-slate-900 dark:text-white">

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

                class="w-full rounded-full bg-slate-900 hover:bg-slate-800 dark:bg-white dark:hover:bg-slate-100 dark:text-slate-900 text-white font-bold py-3 px-4 text-xs shadow-sm transition flex items-center justify-center gap-2"

              >

                <span>💬</span>

                <span>{{ t('Checkout Order on Telegram') }}</span>

              </a>



              <button

                type="button"

                @click="openCheckoutModal"

                class="w-full rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-bold py-2.5 px-4 text-xs transition cursor-pointer"

              >

                {{ t('Instant Web Order Form') }}

              </button>

            </div>

          </div>

        </div>

      </div>

    </div>



    <!-- Slide-Over Wishlist / Favorites Drawer -->
    <div
      v-if="isWishlistOpen"
      class="fixed inset-0 z-50 overflow-hidden"
    >
      <div
        class="absolute inset-0 bg-slate-950/50 backdrop-blur-xs transition-opacity"
        @click="isWishlistOpen = false"
      ></div>

      <div class="fixed inset-y-0 right-0 max-w-full flex pl-10">
        <div class="w-screen max-w-md bg-white dark:bg-slate-900 shadow-2xl flex flex-col justify-between border-l border-slate-200 dark:border-slate-800">
          <!-- Drawer Header -->
          <div class="p-5 border-b border-slate-100 dark:border-slate-800 flex items-center justify-between">
            <div class="flex items-center gap-2">
              <Heart class="w-5 h-5 text-rose-500 fill-rose-500" />
              <div>
                <h3 class="text-sm font-bold text-slate-900 dark:text-white">{{ t('Favorites & Wishlist') }}</h3>
                <p class="text-[11px] text-slate-400">{{ favoritesList.length }} {{ t('saved item(s)') }}</p>
              </div>
            </div>

            <button
              type="button"
              @click="isWishlistOpen = false"
              class="p-2 text-slate-400 hover:text-slate-700 dark:hover:text-white cursor-pointer"
            >
              <X class="w-5 h-5" />
            </button>
          </div>

          <!-- Drawer Body: Empty or Items List -->
          <div class="flex-1 overflow-y-auto p-5 space-y-4">
            <div v-if="favoritesList.length === 0" class="text-center py-20">
              <div class="w-16 h-16 rounded-full bg-rose-50 dark:bg-rose-950/40 text-rose-500 flex items-center justify-center mx-auto mb-3">
                <Heart class="w-8 h-8" />
              </div>
              <h4 class="text-sm font-bold text-slate-900 dark:text-white">{{ t('Your Wishlist is Empty') }}</h4>
              <p class="text-xs text-slate-400 mt-1 max-w-xs mx-auto">
                {{ t('Explore our hardware catalog and click the heart icon on any product to save it here.') }}
              </p>
              <button
                type="button"
                @click="isWishlistOpen = false"
                class="mt-4 px-4 py-2 rounded-full bg-slate-900 text-white dark:bg-white dark:text-slate-900 text-xs font-bold transition hover:opacity-90 cursor-pointer"
              >
                {{ t('Explore Products') }}
              </button>
            </div>

            <div v-else class="space-y-3">
              <div
                v-for="item in favoritesList"
                :key="item.id"
                class="flex items-center gap-3 p-3 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800 hover:border-slate-200 dark:hover:border-slate-700 transition"
              >
                <div class="h-14 w-14 rounded-xl bg-white dark:bg-slate-800 flex items-center justify-center text-2xl shrink-0 border border-slate-200/60 dark:border-slate-700/60">
                  {{ item.icon }}
                </div>

                <div class="flex-1 min-w-0">
                  <div class="text-[10px] text-slate-400 font-medium">{{ item.brand || item.category }}</div>
                  <h4 class="text-xs font-bold text-slate-900 dark:text-white truncate">{{ item.name }}</h4>
                  <div class="text-xs font-bold text-slate-900 dark:text-white mt-0.5">
                    ${{ item.priceUsd.toFixed(2) }}
                    <span class="text-[10px] font-normal text-slate-400 ml-1">
                      (៛ {{ (item.priceUsd * 4100).toLocaleString() }})
                    </span>
                  </div>

                  <div class="flex items-center gap-2 mt-2">
                    <button
                      type="button"
                      @click="addToCart(item)"
                      class="px-2.5 py-1 rounded-full bg-slate-900 hover:bg-slate-800 dark:bg-white dark:hover:bg-slate-100 dark:text-slate-900 text-white text-[11px] font-bold flex items-center gap-1 transition cursor-pointer"
                    >
                      <ShoppingBag class="w-3 h-3" />
                      <span>{{ t('Add to Bag') }}</span>
                    </button>
                    <RouterLink
                      :to="`/store/${item.id}`"
                      @click="isWishlistOpen = false"
                      class="text-[11px] font-semibold text-slate-500 hover:text-slate-900 dark:hover:text-white"
                    >
                      {{ t('Details') }}
                    </RouterLink>
                  </div>
                </div>

                <button
                  type="button"
                  @click="toggleFavorite(item.id)"
                  :title="t('Remove from Wishlist')"
                  class="p-2 text-rose-500 hover:text-rose-700 hover:bg-rose-50 dark:hover:bg-rose-950/50 rounded-lg transition cursor-pointer shrink-0"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

          <!-- Drawer Footer -->
          <div v-if="favoritesList.length > 0" class="p-5 border-t border-slate-100 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-850 space-y-2">
            <button
              type="button"
              @click="addAllFavoritesToCart"
              class="w-full rounded-full bg-slate-900 hover:bg-slate-800 dark:bg-white dark:hover:bg-slate-100 dark:text-slate-900 text-white font-bold py-3 px-4 text-xs shadow-sm transition flex items-center justify-center gap-2 cursor-pointer"
            >
              <ShoppingBag class="w-4 h-4" />
              <span>{{ t('Add All to Bag') }}</span>
            </button>
            <button
              type="button"
              @click="clearFavorites"
              class="w-full rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300 font-bold py-2.5 px-4 text-xs transition cursor-pointer text-center"
            >
              {{ t('Clear All Favorites') }}
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- PRODUCT QUICK VIEW MODAL -->

    <div

      v-if="quickViewProduct"

      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-xs overflow-y-auto"

      @click.self="quickViewProduct = null"

    >

      <div class="w-full max-w-xl rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 sm:p-8 shadow-2xl relative my-8">

        <button

          type="button"

          @click="quickViewProduct = null"

          class="absolute top-5 right-5 text-slate-400 hover:text-slate-700 dark:hover:text-white cursor-pointer"

        >

          <X class="w-5 h-5" />

        </button>



        <div class="grid grid-cols-1 sm:grid-cols-12 gap-6 items-start">

          <div class="sm:col-span-5 flex flex-col items-center">

            <div class="w-full aspect-[4/5] rounded-2xl bg-[#f5f5f7] dark:bg-slate-800 flex items-center justify-center text-7xl shadow-inner border border-slate-200/50 dark:border-slate-700">

              {{ quickViewProduct.icon }}

            </div>

            <div class="mt-3 text-xs text-slate-500 font-semibold">

              ● {{ quickViewProduct.inStock ? `${quickViewProduct.stockCount} in stock` : t('Pre-Order') }}

            </div>

          </div>



          <div class="sm:col-span-7 space-y-2.5">

            <div class="text-xs font-semibold text-slate-400 dark:text-slate-500">

              {{ quickViewProduct.brand }}

            </div>

            <h3 class="text-lg sm:text-xl font-extrabold text-slate-900 dark:text-white leading-snug">

              {{ quickViewProduct.name }}

            </h3>



            <div class="flex items-center gap-1 text-xs text-slate-900 dark:text-slate-100 font-bold">

              <span class="tracking-tighter">★★★★★</span>

              <span class="font-normal text-slate-500 dark:text-slate-400">({{ quickViewProduct.reviewsCount }})</span>

            </div>



            <div class="text-xl font-bold text-slate-900 dark:text-white py-1">

              ${{ quickViewProduct.priceUsd.toFixed(2) }}

              <span class="text-xs font-normal text-slate-400">

                (≈ {{ (quickViewProduct.priceUsd * 4100).toLocaleString() }} KHR)

              </span>

            </div>



            <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">

              {{ quickViewProduct.description }}

            </p>



            <!-- Specs Table -->

            <div v-if="quickViewProduct.specs" class="pt-2">

              <h4 class="text-xs font-bold text-slate-900 dark:text-white mb-1.5">{{ t('Technical Specifications') }}</h4>

              <div class="rounded-xl bg-slate-50 dark:bg-slate-800/60 p-2.5 text-xs space-y-1">

                <div

                  v-for="(val, key) in quickViewProduct.specs"

                  :key="key"

                  class="flex items-center justify-between text-[11px] py-0.5"

                >

                  <span class="text-slate-400 font-medium">{{ key }}:</span>

                  <span class="font-bold text-slate-900 dark:text-white">{{ val }}</span>

                </div>

              </div>

            </div>



            <!-- Actions -->

            <div class="pt-3 flex items-center gap-2">

              <button

                type="button"

                @click="addToCart(quickViewProduct); quickViewProduct = null"

                class="flex-1 rounded-full bg-slate-900 hover:bg-slate-800 dark:bg-white dark:hover:bg-slate-100 dark:text-slate-900 text-white font-bold py-2.5 px-4 text-xs transition cursor-pointer flex items-center justify-center gap-1.5"

              >

                <ShoppingBag class="w-4 h-4" />

                <span>{{ t('Add to Bag') }}</span>

              </button>

              <RouterLink
                :to="`/store/${quickViewProduct.id}`"
                @click="quickViewProduct = null"
                class="px-4 py-2.5 rounded-full border border-slate-200 dark:border-slate-700 hover:bg-slate-50 dark:hover:bg-slate-800 text-xs font-bold text-slate-700 dark:text-slate-200 transition cursor-pointer text-center whitespace-nowrap"
              >
                {{ t('Full Details') }} →
              </RouterLink>

            </div>

          </div>

        </div>

      </div>

    </div>



    <!-- QUICK CHECKOUT MODAL -->

    <div

      v-if="isCheckoutModalOpen"

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

          <h3 class="text-lg font-bold text-slate-900 dark:text-white">{{ t('Order Request Received!') }}</h3>

          <p class="text-xs text-slate-500 dark:text-slate-400 mt-2 max-w-xs mx-auto leading-relaxed">

            Our team will contact you via Telegram or phone shortly to confirm delivery or lab pickup in Phnom Penh.

          </p>



          <button

            type="button"

            @click="closeOrderModal"

            class="mt-6 w-full rounded-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 font-bold py-2.5 text-xs cursor-pointer transition"

          >

            {{ t('Done') }}

          </button>

        </div>



        <!-- Order Form State -->

        <div v-else>

          <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">

            <div class="text-2xl">🛍️</div>

            <div>

              <h3 class="text-base font-bold text-slate-900 dark:text-white">

                {{ t('Shopping Bag Checkout') }} ({{ totalCartItemsCount }} items)

              </h3>

              <p class="text-xs font-bold text-slate-900 dark:text-white">

                ${{ cartTotalUsd.toFixed(2) }}

              </p>

            </div>

          </div>



          <form @submit.prevent="submitOrder" class="mt-4 space-y-3">

            <div>

              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">{{ t('Full Name') }}</label>

              <input

                v-model="orderForm.name"

                type="text"

                required

                placeholder="e.g. Chan Dara"

                class="w-full rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 px-3.5 py-2 text-xs text-slate-900 dark:text-white focus:outline-none"

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

                  class="w-full rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 px-3.5 py-2 text-xs text-slate-900 dark:text-white focus:outline-none"

                />

              </div>

              <div>

                <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">{{ t('Telegram (Optional)') }}</label>

                <input

                  v-model="orderForm.telegram"

                  type="text"

                  placeholder="@username"

                  class="w-full rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 px-3.5 py-2 text-xs text-slate-900 dark:text-white focus:outline-none"

                />

              </div>

            </div>



            <div>

              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">{{ t('Delivery Address or Lab Pickup') }}</label>

              <textarea

                v-model="orderForm.address"

                rows="2"

                placeholder="Pick up at AeroByte Academy Lab, or delivery address in Phnom Penh..."

                class="w-full rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 px-3.5 py-2 text-xs text-slate-900 dark:text-white focus:outline-none"

              ></textarea>

            </div>



            <div class="pt-2 flex flex-col gap-2">

              <button

                type="submit"

                class="w-full rounded-full bg-slate-900 hover:bg-slate-800 dark:bg-white dark:hover:bg-slate-100 dark:text-slate-900 text-white font-bold py-3 text-xs transition cursor-pointer"

              >

                {{ t('Confirm Order') }}

              </button>



              <a

                :href="cartTelegramCheckoutLink"

                target="_blank"

                rel="noopener"

                class="w-full rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 font-bold py-2.5 px-4 text-xs transition flex items-center justify-center gap-2"

              >

                <span>💬</span>

                <span>{{ t('Order Directly on Telegram') }}</span>

              </a>

            </div>

          </form>

        </div>

      </div>

    </div>



    <!-- Floating Toast Notification -->

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

        class="fixed bottom-6 right-6 z-50 rounded-full bg-slate-900 text-white px-4 py-2.5 shadow-xl flex items-center gap-2 text-xs font-semibold"

      >

        <span>✓</span>

        <span>{{ toastMessage }}</span>

      </div>

    </transition>



    <!-- Floating Action Pills (Bottom-Left: Favorites & Shopping Bag) -->
    <div class="fixed bottom-6 left-6 z-40 flex flex-col gap-2.5 items-start pointer-events-none">
      <!-- Floating Favorites / Wishlist Pill Button (Upper this) -->
      <transition
        enter-active-class="transform ease-out duration-300 transition"
        enter-from-class="translate-y-6 opacity-0 scale-90"
        enter-to-class="translate-y-0 opacity-100 scale-100"
        leave-active-class="transition ease-in duration-200"
        leave-from-class="opacity-100 scale-100"
        leave-to-class="opacity-0 scale-90"
      >
        <button
          v-if="favoritesCount > 0"
          type="button"
          @click="isWishlistOpen = true"
          class="pointer-events-auto flex items-center gap-2 rounded-full bg-slate-900 text-white px-4 py-3 shadow-2xl hover:bg-slate-800 transition cursor-pointer border border-white/20 active:scale-95 group"
        >
          <Heart class="w-4 h-4 text-rose-500 fill-rose-500 group-hover:scale-110 transition-transform" />
          <span class="text-xs font-bold">{{ favoritesCount }} {{ favoritesCount === 1 ? t('in Favorite') : t('in Favorites') }}</span>
        </button>
      </transition>

      <!-- Floating Cart Pill Button (Lower) -->
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
          class="pointer-events-auto flex items-center gap-2 rounded-full bg-slate-900 text-white px-4 py-3 shadow-2xl hover:bg-slate-800 transition cursor-pointer border border-white/20 active:scale-95 group"
        >
          <ShoppingBag class="w-4 h-4 text-white group-hover:scale-110 transition-transform" />
          <span class="text-xs font-bold">{{ totalCartItemsCount }} {{ t('in Bag') }}</span>
          <span class="text-xs font-bold"> · ${{ cartTotalUsd.toFixed(2) }}</span>
        </button>
      </transition>
    </div>

  </div>

</template>



<script setup>
import { ref, computed, onMounted, onUnmounted, watch } from 'vue'

import {
  Search,
  X,
  ShoppingBag,
  ShoppingCart,
  Heart,
  Plus,
  Trash2,
  CheckCircle2,
  ChevronLeft,
  ChevronRight,
  SlidersHorizontal,
  ChevronDown,
  Check
} from 'lucide-vue-next'

import { useI18n } from '../i18n'
import CustomSelect from '../components/common/CustomSelect.vue'
import { accountService } from '../services/api'



const { t } = useI18n()



// Auto-Rotating Hero Carousel (every 3 seconds)

const heroSlides = [

  {

    id: 'store-showcase',

    image: '/assets/brand/store-hero-showcase.jpg',

    alt: 'AeroByte Maker Kit Hardware Showcase',

    tag: 'MAKER HARDWARE & ROBOTICS',

    title1: 'AERO STORE',

    title2: '2026!',

    buttonText: 'SHOP ALL',

    category: 'All',

    btnClass: 'bg-amber-400 hover:bg-amber-300 text-[#102a49]',

  },

  {

    id: 'store-drone',

    image: '/assets/brand/store-hero-drone.jpg',

    alt: 'FPV Racing Drone Hardware & Kits',

    tag: 'FPV RACING & AERIAL TECH',

    title1: 'FPV DRONE',

    title2: 'RACING LAB',

    buttonText: 'EXPLORE DRONES',

    category: 'FPV Drone Hardware',

    btnClass: 'bg-cyan-400 hover:bg-cyan-300 text-slate-950',

  },

  {

    id: 'store-robotics',

    image: '/assets/brand/store-hero-robotics.jpg',

    alt: 'STEM Robotics & Microcontroller Kits',

    tag: 'AI & SMART ROVER KITS',

    title1: 'STEM ROBOTICS',

    title2: '& AI KITS',

    buttonText: 'VIEW ROBOTICS',

    category: 'Microcontrollers & Sensors',

    btnClass: 'bg-emerald-400 hover:bg-emerald-300 text-slate-950',

  },

  {

    id: 'store-tools',

    image: '/assets/brand/store-hero-tools.jpg',

    alt: '3D Filaments & Electronics Lab Tools',

    tag: 'PRECISION LAB & PROTOTYPING',

    title1: '3D FILAMENTS',

    title2: '& LAB TOOLS',

    buttonText: 'DISCOVER TOOLS',

    category: 'Tools & Equipment',

    btnClass: 'bg-amber-400 hover:bg-amber-300 text-[#102a49]',

  },

]



const currentSlide = ref(0)

const slideKey = ref(0)

const slideProgress = ref(0)

let carouselTimer = null

let progressTimer = null



function nextSlide() {

  currentSlide.value = (currentSlide.value + 1) % heroSlides.length

  resetProgress()

}



function prevSlide() {

  currentSlide.value = (currentSlide.value - 1 + heroSlides.length) % heroSlides.length

  resetProgress()

}



function goToSlide(index) {

  currentSlide.value = index

  resetProgress()

}



function resetProgress() {

  slideProgress.value = 0

  slideKey.value++

}



function startHeroCarousel() {

  stopHeroCarousel()

  resetProgress()



  // Progress update every 50ms for smooth 3000ms bar

  progressTimer = setInterval(() => {

    slideProgress.value = Math.min(100, slideProgress.value + (100 / (3000 / 50)))

  }, 50)



  // Switch image automatically every 3 seconds

  carouselTimer = setInterval(() => {

    nextSlide()

  }, 3000)

}



function stopHeroCarousel() {

  if (carouselTimer) clearInterval(carouselTimer)

  if (progressTimer) clearInterval(progressTimer)

  carouselTimer = null

  progressTimer = null

}



function pauseHeroCarousel() {

  stopHeroCarousel()

}



function resumeHeroCarousel() {

  startHeroCarousel()

}



function selectSlideCategory(cat) {

  if (cat && cat !== 'All') {

    selectedCategory.value = cat

  } else {

    selectedCategory.value = 'All'

  }

  const el = document.getElementById('catalog')

  if (el) {

    el.scrollIntoView({ behavior: 'smooth' })

  }

}



onMounted(() => {
  startHeroCarousel()
  if (typeof window !== 'undefined') {
    window.addEventListener('click', handleWindowClick)
  }
})

onUnmounted(() => {
  stopHeroCarousel()
  if (typeof window !== 'undefined') {
    window.removeEventListener('click', handleWindowClick)
  }
})





// Filters
const searchQuery = ref('')
const selectedCategory = ref('All')
const inStockOnly = ref(false)
const onSaleOnly = ref(false)
const selectedPriceRange = ref('all')
const sortBy = ref('featured')
const isSortDropdownOpen = ref(false)
const isPriceDropdownOpen = ref(false)
const isFiltersModalOpen = ref(false)
const priceMin = ref(0)
const priceMax = ref(100)

const activeFiltersCount = computed(() => {
  let count = 0
  if (selectedCategory.value !== 'All') count++
  if (inStockOnly.value) count++
  if (onSaleOnly.value) count++
  if (priceMin.value > 0 || priceMax.value < 100) count++
  if (sortBy.value !== 'featured' && sortBy.value !== 'best-selling') count++
  return count
})

const sortLabel = computed(() => {
  if (sortBy.value === 'best-selling') return t('Best selling')
  if (sortBy.value === 'newest') return t('Newest')
  if (sortBy.value === 'price-low') return t('Price: Low - High')
  if (sortBy.value === 'price-high') return t('Price: High - Low')
  return t('Sort by')
})

const priceLabel = computed(() => {
  if (priceMin.value > 0 && priceMax.value < 100) {
    return `${priceMin.value} - ${priceMax.value}`
  }
  if (priceMin.value > 0) {
    return `Over ${priceMin.value}`
  }
  if (priceMax.value < 100) {
    return `Under ${priceMax.value}`
  }
  return t('Price')
})

function handlePriceMinChange() {
  if (priceMin.value > priceMax.value - 2) {
    priceMin.value = priceMax.value - 2
  }
}

function handlePriceMaxChange() {
  if (priceMax.value < priceMin.value + 2) {
    priceMax.value = priceMin.value + 2
  }
}

function resetPriceFilter() {
  priceMin.value = 0
  priceMax.value = 100
}

function toggleSortDropdown() {
  isPriceDropdownOpen.value = false
  isSortDropdownOpen.value = !isSortDropdownOpen.value
}

function togglePriceDropdown() {
  isSortDropdownOpen.value = false
  isPriceDropdownOpen.value = !isPriceDropdownOpen.value
}

function openFiltersModal() {
  closeDropdowns()
  isFiltersModalOpen.value = true
}

function closeDropdowns() {
  isSortDropdownOpen.value = false
  isPriceDropdownOpen.value = false
}

function handleWindowClick(e) {
  if (!e.target.closest || !e.target.closest('.filter-dropdown-container')) {
    closeDropdowns()
  }
}

const sortOptions = computed(() => [
  { value: 'best-selling', label: t('Best selling') },
  { value: 'newest', label: t('Newest') },
  { value: 'price-low', label: t('Price: Low - High') },
  { value: 'price-high', label: t('Price: High - Low') }
])



// Cart with LocalStorage persistence

const savedCart = typeof localStorage !== 'undefined' ? localStorage.getItem('aerobyte_store_cart') : null

let initialCart = []

try {

  if (savedCart) initialCart = JSON.parse(savedCart)

} catch {

  initialCart = []

}

const isCartOpen = ref(false)
const isWishlistOpen = ref(false)
const showFavoritesOnly = ref(false)

const cartItems = ref(initialCart)

const selectedDeliveryMethod = ref('pickup')



function persistCart() {

  try {

    if (typeof localStorage !== 'undefined') {

      localStorage.setItem('aerobyte_store_cart', JSON.stringify(cartItems.value))

    }

  } catch {}

}



// Favorites with LocalStorage persistence

const savedFavs = typeof localStorage !== 'undefined' ? localStorage.getItem('aerobyte_store_favs') : null

let initialFavs = []

try {

  if (savedFavs) initialFavs = JSON.parse(savedFavs)

} catch {

  initialFavs = []

}

const favorites = ref(new Set(initialFavs))
const favoritesCount = computed(() => favorites.value.size)



function persistFavorites() {

  try {

    if (typeof localStorage !== 'undefined') {

      localStorage.setItem('aerobyte_store_favs', JSON.stringify([...favorites.value]))

    }

  } catch {}

}



// Modals State

const quickViewProduct = ref(null)

const isCheckoutModalOpen = ref(false)

const orderSubmitted = ref(false)

const toastMessage = ref('')



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



// Products Dataset tailored with Brand, TikTok badge, Award badge & Reviews matching the reference screenshot!

const products = [

  {

    id: 'starter-robotics-kit',

    brand: 'AeroByte Lab',

    name: 'Starter Robotics Lab Kit (ESP32 Edition)',

    category: 'Student Lab Kits',

    priceUsd: 45.0,
    originalPriceUsd: 55.0,
    onSale: true,

    rating: 5.0,

    reviewsCount: '5.5K',

    badge: 'BEST SELLER',

    badgeType: 'tiktok',

    awardBadge: true,

    inStock: true,

    stockCount: 14,

    icon: '🤖',

    description: 'All-in-one learning kit with ESP32 board, dual motor driver shield, ultrasonic sensors, chassis, servo, and breadboard wires.',

    tags: ['ESP32', 'Robotics', 'Lab Ready'],

    specs: {

      'MCU': 'ESP32 Dual-Core 240MHz',

      'Connectivity': 'Wi-Fi 802.11 b/g/n + BLE 4.2',

      'Motor Driver': 'Dual H-Bridge L298N Shield',

      'Chassis': 'Laser-cut Acrylic Smart Car'

    }

  },

  {

    id: 'iot-maker-kit',

    brand: 'AeroByte Lab',

    name: 'Advanced Arduino IoT Maker Kit',

    category: 'Student Lab Kits',

    priceUsd: 35.0,
    originalPriceUsd: 42.0,
    onSale: true,

    rating: 4.9,

    reviewsCount: '1.7K',

    badge: null,

    awardBadge: false,

    inStock: true,

    stockCount: 18,

    icon: '💡',

    description: 'Arduino Uno compatible controller, OLED display, DHT11 temp/humidity sensor, relay module, and 30+ components for IoT projects.',

    tags: ['Arduino', 'Sensors', 'Beginner'],

    specs: {

      'Controller': 'ATmega328P Uno Compatible',

      'Display': '0.96" I2C OLED (128x64)',

      'Sensors': 'DHT11, PIR Motion, Light LDR'

    }

  },

  {

    id: 'drone-frame-5in',

    brand: 'Aero Fly',

    name: '5" FPV Racing Drone Frame (Carbon Fiber)',

    category: 'FPV Drone Hardware',

    priceUsd: 29.0,
    originalPriceUsd: 36.0,
    onSale: true,

    rating: 4.8,

    reviewsCount: '900',

    badge: '3K CARBON',

    badgeType: 'normal',

    awardBadge: false,

    inStock: true,

    stockCount: 9,

    icon: '🚁',

    description: '3K pure matte carbon fiber, 5mm arms, lightweight aerodynamic racing frame designed for 2207 brushless motors.',

    tags: ['FPV', 'Carbon Fiber', 'Racing'],

    specs: {

      'Material': 'Toray 3K Matte Carbon Fiber',

      'Wheelbase': '225mm True-X Geometry',

      'Arm Thickness': '5.0mm Chamfered Edges'

    }

  },

  {

    id: 'f405-esc-stack',

    brand: 'Aero Fly',

    name: 'F405 V3 Flight Controller + 50A 4-in-1 ESC',

    category: 'FPV Drone Hardware',

    priceUsd: 62.0,

    rating: 4.9,

    reviewsCount: '92.1K',

    badge: null,

    awardBadge: false,

    inStock: true,

    stockCount: 7,

    icon: '⚡',

    description: 'Betaflight OSD, barometer, blackbox logging, 3-6S LiPo input, with BLHeli_S 50A continuous current handling.',

    tags: ['Flight Controller', 'Betaflight', '6S'],

    specs: {

      'MCU': 'STM32F405 168MHz',

      'ESC Current': '50A Continuous',

      'Firmware': 'Betaflight / BLHeli_S'

    }

  },

  {

    id: 'brushless-motor-pack',

    brand: 'Aero Fly',

    name: 'Brushless Motor 2207 1950KV (Set of 4)',

    category: 'Brushless Motors & ESCs',

    priceUsd: 54.0,

    rating: 5.0,

    reviewsCount: '41.1K',

    badge: 'POWER EDITION',

    badgeType: 'normal',

    awardBadge: true,

    inStock: true,

    stockCount: 11,

    icon: '⚙️',

    description: 'High torque hollow titanium shaft, N52H curved magnets, super smooth throttle curve for FPV freestyle and racing.',

    tags: ['6S Motors', 'High Torque'],

    specs: {

      'Stator Size': '2207 (Titanium Shaft)',

      'KV Rating': '1950KV (Optimized for 6S)',

      'Max Thrust': '1,920g per motor'

    }

  },

  {

    id: 'esp32-dual-core',

    brand: 'Espressif',

    name: 'ESP32-WROOM-32D Development Board',

    category: 'Microcontrollers & Sensors',

    priceUsd: 6.5,

    rating: 4.9,

    reviewsCount: '12.4K',

    badge: 'TOP SELLER',

    badgeType: 'normal',

    awardBadge: false,

    inStock: true,

    stockCount: 42,

    icon: '📡',

    description: '2.4GHz Wi-Fi + Bluetooth BLE dual-core MCU, modern Type-C interface, breadboard friendly pinout.',

    tags: ['Wi-Fi', 'Bluetooth', 'Type-C'],

    specs: {

      'Processor': 'Xtensa Dual-Core 32-bit LX6 240MHz',

      'USB Port': 'Modern USB Type-C',

      'GPIO': '30 General-Purpose I/O Pins'

    }

  },

  {

    id: 'raspberry-pi-4',

    brand: 'Raspberry Pi',

    name: 'Raspberry Pi 4 Model B (4GB RAM)',

    category: 'Microcontrollers & Sensors',

    priceUsd: 68.0,

    rating: 4.9,

    reviewsCount: '8.3K',

    badge: 'OFFICIAL',

    badgeType: 'normal',

    awardBadge: true,

    inStock: true,

    stockCount: 6,

    icon: '🍓',

    description: 'Quad-core 64-bit ARM Cortex-A72, dual 4K micro-HDMI, Gigabit Ethernet, USB 3.0 for computer vision & autonomous drones.',

    tags: ['AI / Vision', 'Linux', 'ROS'],

    specs: {

      'Processor': 'Quad-Core 1.5GHz 64-bit',

      'RAM': '4GB LPDDR4-3200 SDRAM',

      'Video': 'Dual Micro-HDMI Ports (up to 4Kp60)'

    }

  },

  {

    id: 'digital-soldering-station',

    brand: 'Aero Tools',

    name: 'Precision Digital Soldering Iron (65W)',

    category: 'Tools & Equipment',

    priceUsd: 38.0,

    rating: 4.9,

    reviewsCount: '3.1K',

    badge: null,

    awardBadge: false,

    inStock: true,

    stockCount: 15,

    icon: '🔥',

    description: 'OLED screen, 8-second rapid heating to 300°C, PID temperature stabilization, auto-sleep mode, and ergonomic silicone grip.',

    tags: ['Soldering', 'Lab Grade', 'Type-C'],

    specs: {

      'Power Output': '65W PD / QC Compatible',

      'Heat-up Time': '8 Seconds from 25°C to 300°C',

      'Display': '0.96" OLED Status Screen'

    }

  },

  {

    id: 'lipo-balance-charger',

    brand: 'Aero Tools',

    name: 'Smart LiPo Balance Charger (6S 80W)',

    category: 'Tools & Equipment',

    priceUsd: 32.0,

    rating: 4.8,

    reviewsCount: '1.9K',

    badge: null,

    awardBadge: false,

    inStock: true,

    stockCount: 12,

    icon: '🔋',

    description: 'Supports LiPo, LiFe, Li-ion, NiMH battery packs. Built-in internal resistance meter and storage discharge mode.',

    tags: ['Charger', 'LiPo', 'Safety'],

    specs: {

      'Supported': 'LiPo / LiFe / Li-ion (1-6S)',

      'Charge Power': '80W (0.1A - 6.0A Adjustable)'

    }

  },

  {

    id: 'aeropla-filament-1kg',

    brand: 'Aero Print',

    name: 'AeroPLA Tough 3D Printing Filament (1kg)',

    category: '3D Filaments & Parts',

    priceUsd: 16.0,

    rating: 4.9,

    reviewsCount: '6.7K',

    badge: 'VIRAL',

    badgeType: 'tiktok',

    awardBadge: true,

    inStock: true,

    stockCount: 30,

    icon: '🧵',

    description: '1.75mm diameter, high impact resistance, zero warping, optimized for mechanical parts, robotics arms, and drone brackets.',

    tags: ['PLA', '1kg Spool'],

    specs: {

      'Diameter': '1.75mm (±0.02mm tolerance)',

      'Net Weight': '1.0 kg (2.2 lbs) on Spool',

      'Print Temp': '205°C - 225°C'

    }

  },

  {

    id: 'tpu-flexible-filament',

    brand: 'Aero Print',

    name: 'TPU Flexible 95A Filament (1kg Elasticity)',

    category: '3D Filaments & Parts',

    priceUsd: 22.0,

    rating: 4.8,

    reviewsCount: '1.1K',

    badge: null,

    awardBadge: false,

    inStock: true,

    stockCount: 16,

    icon: '🌀',

    description: 'Perfect for FPV drone bumpers, action camera vibration dampeners, robotic gripper pads, and protective sleeves.',

    tags: ['Flexible 95A', 'Crash Proof'],

    specs: {

      'Hardness': 'Shore 95A High Elasticity',

      'Diameter': '1.75mm (±0.03mm precision)'

    }

  },

  {

    id: 'multimeter-tool-kit',

    brand: 'Aero Tools',

    name: 'True-RMS Multimeter & Electronics Tool Kit',

    category: 'Tools & Equipment',

    priceUsd: 26.0,

    rating: 4.8,

    reviewsCount: '2.4K',

    badge: 'KIT VALUE',

    badgeType: 'normal',

    awardBadge: false,

    inStock: true,

    stockCount: 14,

    icon: '🧰',

    description: 'True RMS auto-ranging multimeter, flush wire cutters, ESD anti-static tweezers, desoldering pump, and storage carry case.',

    tags: ['Multimeter', 'Tools'],

    specs: {

      'Multimeter Type': 'True-RMS Auto-Ranging 6000 Counts',

      'Safety Rating': 'CAT III 600V'

    }

  }

]



function resetFilters() {
  searchQuery.value = ''
  selectedCategory.value = 'All'
  inStockOnly.value = false
  onSaleOnly.value = false
  priceMin.value = 0
  priceMax.value = 100
  sortBy.value = 'best-selling'
  showFavoritesOnly.value = false
  closeDropdowns()
}



// Filtered & Sorted Products

const filteredProducts = computed(() => {

  let list = [...products]



  if (searchQuery.value.trim() !== '') {

    const q = searchQuery.value.toLowerCase()

    list = list.filter(p =>

      p.name.toLowerCase().includes(q) ||

      (p.brand && p.brand.toLowerCase().includes(q)) ||

      p.category.toLowerCase().includes(q)

    )

  }



  if (selectedCategory.value !== 'All') {

    list = list.filter(p => p.category === selectedCategory.value)

  }



    if (inStockOnly.value) {
    list = list.filter(p => p.inStock)
  }

  if (onSaleOnly.value) {
    list = list.filter(p => p.onSale || (p.originalPriceUsd && p.originalPriceUsd > p.priceUsd))
  }

  if (priceMin.value > 0) {
    list = list.filter(p => p.priceUsd >= priceMin.value)
  }
  if (priceMax.value < 100) {
    list = list.filter(p => p.priceUsd <= priceMax.value)
  }

  if (showFavoritesOnly.value) {
    list = list.filter(p => favorites.value.has(p.id))
  }

  if (sortBy.value === 'price-low') {
    list.sort((a, b) => a.priceUsd - b.priceUsd)
  } else if (sortBy.value === 'price-high') {
    list.sort((a, b) => b.priceUsd - a.priceUsd)
  } else if (sortBy.value === 'best-selling') {
    list.sort((a, b) => (parseFloat(b.reviewsCount) || 0) - (parseFloat(a.reviewsCount) || 0))
  } else if (sortBy.value === 'newest') {
    list.sort((a, b) => (b.stockCount || 0) - (a.stockCount || 0))
  }



  return list

})



// Favorites Management
const favoritesList = computed(() => {
  return products.filter(p => favorites.value.has(p.id))
})

function toggleFavorite(productId) {
  const next = new Set(favorites.value)
  if (next.has(productId)) {
    next.delete(productId)
    showToast('Removed from wishlist')
  } else {
    next.add(productId)
    showToast('Saved to your wishlist')
  }
  favorites.value = next
  persistFavorites()
}

function isFavorite(productId) {
  return favorites.value.has(productId)
}

function clearFavorites() {
  favorites.value = new Set()
  persistFavorites()
  showToast('Cleared all favorites')
}

function addAllFavoritesToCart() {
  if (favoritesList.value.length === 0) return
  favoritesList.value.forEach(item => {
    addToCart(item)
  })
  showToast(`Added ${favoritesList.value.length} favorite item(s) to bag`)
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

  showToast(`Added ${product.name} to bag`)

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



let toastTimeout = null

function showToast(msg) {

  toastMessage.value = msg

  if (toastTimeout) clearTimeout(toastTimeout)

  toastTimeout = setTimeout(() => {

    toastMessage.value = ''

  }, 2200)

}



function openQuickView(product) {

  quickViewProduct.value = product

}



function openCheckoutModal() {

  isCartOpen.value = false

  isCheckoutModalOpen.value = true

  orderSubmitted.value = false

}



function closeOrderModal() {

  if (orderSubmitted.value) {

    cartItems.value = []

    persistCart()

  }

  isCheckoutModalOpen.value = false

  orderSubmitted.value = false

}



async function submitOrder() {
  const newOrder = {
    id: 'AERO-' + Math.floor(100000 + Math.random() * 900000),
    date: new Date().toISOString(),
    customer: { ...orderForm.value },
    fulfillment: selectedDeliveryMethod.value,
    items: cartItems.value.map(item => ({
      id: item.id,
      name: item.name,
      priceUsd: item.priceUsd,
      quantity: item.quantity,
      icon: item.icon || '📦'
    })),
    subtotal: cartSubtotalUsd.value,
    deliveryFee: deliveryFeeUsd.value,
    total: cartTotalUsd.value,
    status: 'confirmed'
  }

  // 1. Save to database via API
  try {
    await accountService.createStoreOrder({
      id: newOrder.id,
      name: orderForm.value.name,
      phone: orderForm.value.phone,
      telegram: orderForm.value.telegram,
      address: orderForm.value.address,
      fulfillment: selectedDeliveryMethod.value,
      items: newOrder.items,
      subtotal: cartSubtotalUsd.value,
      delivery_fee: deliveryFeeUsd.value,
      total: cartTotalUsd.value,
    })
  } catch (err) {
    console.warn('Backend order storage fallback to localStorage:', err)
  }

  // 2. Also keep in localStorage for immediate sync & offline resilience
  try {
    const existing = JSON.parse(localStorage.getItem('aerobyte_store_orders') || '[]')
    existing.unshift(newOrder)
    localStorage.setItem('aerobyte_store_orders', JSON.stringify(existing))
    window.dispatchEvent(new CustomEvent('aerobyte-orders-updated', { detail: newOrder }))
  } catch (e) {
    console.error('Failed to save order to localStorage', e)
  }
  orderSubmitted.value = true
}



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


.shop-range-input {
  position: absolute;
  left: 0;
  top: 0;
  width: 100%;
  height: 100%;
  appearance: none;
  background: transparent;
  pointer-events: none;
  margin: 0;
}
.shop-range-input::-webkit-slider-thumb {
  pointer-events: auto;
  appearance: none;
  width: 18px;
  height: 18px;
  border-radius: 9999px;
  background-color: #6366f1;
  border: 2px solid #ffffff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.25);
  cursor: pointer;
  transition: transform 0.1s;
}
.shop-range-input::-webkit-slider-thumb:active {
  transform: scale(1.15);
}
.shop-range-input::-moz-range-thumb {
  pointer-events: auto;
  width: 18px;
  height: 18px;
  border-radius: 9999px;
  background-color: #6366f1;
  border: 2px solid #ffffff;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.25);
  cursor: pointer;
}

</style>

