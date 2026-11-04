<template>
  <div class="min-h-screen bg-white dark:bg-slate-950 transition-colors pb-24">
    <!-- Top Breadcrumb & Back Bar -->
    <div class="border-b border-slate-100 dark:border-slate-800/80 bg-white dark:bg-slate-950 sticky top-0 z-30 backdrop-blur-md bg-white/90 dark:bg-slate-950/90">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-3.5 flex items-center justify-between">
        <nav class="flex items-center gap-2 text-xs text-slate-500 dark:text-slate-400 truncate">
          <RouterLink
            to="/store"
            class="inline-flex items-center gap-1.5 font-bold text-slate-700 dark:text-slate-200 hover:text-indigo-600 dark:hover:text-indigo-400 transition"
          >
            <ChevronLeft class="w-4 h-4" />
            <span>{{ t('Back to Store') }}</span>
          </RouterLink>
          <span class="text-slate-300 dark:text-slate-700">/</span>
          <span class="text-slate-400 truncate hidden sm:inline">{{ product?.category }}</span>
          <span class="text-slate-300 dark:text-slate-700 hidden sm:inline">/</span>
          <span class="text-slate-900 dark:text-white font-semibold truncate max-w-[200px] sm:max-w-xs">{{ product?.name }}</span>
        </nav>

        <!-- Right Tools: Wishlist & Bag Button -->
        <div class="flex items-center gap-2">
          <button
            type="button"
            @click="product && toggleFavorite(product.id)"
            :title="isSaved ? t('Remove from Wishlist') : t('Save to Wishlist')"
            class="h-9 w-9 rounded-full border border-slate-200 dark:border-slate-800 flex items-center justify-center text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition cursor-pointer"
          >
            <Heart class="w-4 h-4" :class="{ 'fill-red-500 text-red-500': isSaved }" />
          </button>

          <button
            type="button"
            @click="isCartOpen = true"
            class="relative h-9 px-3.5 rounded-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 text-xs font-bold flex items-center gap-1.5 hover:opacity-90 transition cursor-pointer"
          >
            <ShoppingBag class="w-3.5 h-3.5" />
            <span>{{ t('Bag') }}</span>
            <span
              v-if="totalCartItemsCount > 0"
              class="ml-0.5 px-1.5 py-0.2 rounded-full bg-indigo-500 text-white text-[10px] font-extrabold"
            >
              {{ totalCartItemsCount }}
            </span>
          </button>
        </div>
      </div>
    </div>

    <!-- Product Not Found State -->
    <div v-if="!product" class="max-w-2xl mx-auto px-4 py-24 text-center">
      <div class="text-5xl mb-4">🔍</div>
      <h2 class="text-2xl font-black text-slate-900 dark:text-white">{{ t('Product Not Found') }}</h2>
      <p class="text-sm text-slate-500 dark:text-slate-400 mt-2">
        {{ t('The item you are searching for might have been moved or is currently unavailable.') }}
      </p>
      <RouterLink
        to="/store"
        class="mt-6 inline-flex items-center gap-2 px-6 py-3 rounded-full bg-slate-900 dark:bg-white text-white dark:text-slate-900 text-xs font-bold transition"
      >
        <ChevronLeft class="w-4 h-4" />
        <span>{{ t('Explore Aero Store Catalog') }}</span>
      </RouterLink>
    </div>

    <!-- MAIN PRODUCT DETAIL CONTAINER (Shop.com Reference Style) -->
    <main v-else class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 pt-6 sm:pt-10">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-14 items-start">
        
        <!-- ==========================================
             LEFT SIDE: VERTICAL THUMBNAIL RAIL + HERO SHOWCASE
             ========================================== -->
        <div class="lg:col-span-7 flex flex-col sm:flex-row gap-4 sm:gap-6 items-start">
          
          <!-- Vertical Thumbnail Strip (Matches Screenshot!) -->
          <div class="flex sm:flex-col gap-2.5 overflow-x-auto sm:overflow-visible order-2 sm:order-1 w-full sm:w-20 shrink-0 pb-2 sm:pb-0">
            <button
              v-for="(view, idx) in productGallery"
              :key="idx"
              type="button"
              @click="activeGalleryIdx = idx"
              class="relative h-16 w-16 sm:h-20 sm:w-20 rounded-2xl bg-[#f5f5f7] dark:bg-slate-900 border-2 transition-all flex flex-col items-center justify-center text-2xl sm:text-3xl shrink-0 cursor-pointer overflow-hidden p-1 group"
              :class="activeGalleryIdx === idx
                ? 'border-indigo-600 dark:border-indigo-500 shadow-sm scale-102 ring-2 ring-indigo-500/20'
                : 'border-slate-200/80 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 opacity-70 hover:opacity-100'"
            >
              <span>{{ view.icon }}</span>
              <span class="text-[9px] font-bold text-slate-500 dark:text-slate-400 tracking-tighter truncate w-full text-center px-1">
                {{ view.label }}
              </span>
            </button>
          </div>

          <!-- Main Hero Image Showcase Box (Rounded-3xl, centered hero & Cosmopolitan style badge!) -->
          <div class="relative flex-1 w-full rounded-[28px] sm:rounded-[36px] bg-[#f8f9fa] dark:bg-slate-900/90 border border-slate-200/80 dark:border-slate-800 p-8 sm:p-14 min-h-[400px] sm:min-h-[560px] flex items-center justify-center overflow-hidden order-1 sm:order-2 shadow-2xs select-none">

            <!-- Authentic Award / Recognition Seal (Top Right - Exact match to Cosmopolitan badge in screenshot!) -->
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

            <!-- Main Big Hardware Visual Icon -->
            <div class="flex flex-col items-center justify-center text-center transition-transform duration-300 hover:scale-105">
              <div class="text-8xl sm:text-9xl drop-shadow-md filter select-none">
                {{ activeView.icon || product.icon }}
              </div>
              <p class="mt-4 text-xs font-semibold text-slate-400 dark:text-slate-500 max-w-xs">
                {{ activeView.title }}
              </p>
            </div>

            <!-- Bottom Feature Micro-Pills -->
            <div class="absolute bottom-5 inset-x-5 flex flex-wrap items-center justify-center gap-2 pointer-events-none">
              <span
                v-for="tag in product.tags"
                :key="tag"
                class="px-2.5 py-1 rounded-full bg-white/80 dark:bg-slate-800/80 backdrop-blur-xs text-[10px] font-bold text-slate-600 dark:text-slate-300 border border-slate-200/50 dark:border-slate-700/60 shadow-2xs"
              >
                #{{ tag }}
              </span>
            </div>
          </div>
        </div>

        <!-- ==========================================
             RIGHT SIDE: BUY BOX & PRODUCT DETAILS
             ========================================== -->
        <div class="lg:col-span-5 space-y-6">
          
          <!-- Vendor / Brand Header Row (Matches screenshot header with brand avatar, name, rating & menu) -->
          <div class="flex items-center justify-between pb-1 border-b border-slate-100 dark:border-slate-800/80">
            <div class="flex items-center gap-2.5">
              <div class="h-9 w-9 rounded-full bg-slate-100 dark:bg-slate-800 flex items-center justify-center text-lg border border-slate-200 dark:border-slate-700 shadow-2xs">
                {{ product.brandLogo || '⚙️' }}
              </div>
              <div>
                <h4 class="text-xs font-extrabold text-slate-900 dark:text-white leading-tight">
                  {{ product.brand }}
                </h4>
                <div class="flex items-center gap-1 text-[11px] font-semibold text-slate-500 dark:text-slate-400">
                  <span>{{ product.brandRating || '4.9 ★ (3.1K)' }}</span>
                </div>
              </div>
            </div>

            <div class="relative">
              <button
                type="button"
                @click="isMoreMenuOpen = !isMoreMenuOpen"
                :title="t('More options')"
                class="h-8 w-8 rounded-full hover:bg-slate-100 dark:hover:bg-slate-800 text-slate-500 hover:text-slate-900 dark:text-slate-400 dark:hover:text-white flex items-center justify-center transition cursor-pointer select-none active:scale-95"
                :class="{ 'bg-slate-100 dark:bg-slate-800 text-slate-900 dark:text-white': isMoreMenuOpen }"
              >
                <MoreHorizontal class="w-4 h-4" />
              </button>

              <!-- Transparent Backdrop to dismiss dropdown -->
              <div
                v-if="isMoreMenuOpen"
                class="fixed inset-0 z-30 bg-transparent cursor-default"
                @click="isMoreMenuOpen = false"
              ></div>

              <!-- 3-Dot Dropdown Card (Matches screenshot with speech bubble & Contact Fellow!) -->
              <transition
                enter-active-class="transition ease-out duration-150"
                enter-from-class="transform opacity-0 scale-95"
                enter-to-class="transform opacity-100 scale-100"
                leave-active-class="transition ease-in duration-100"
                leave-from-class="transform opacity-100 scale-100"
                leave-to-class="transform opacity-0 scale-95"
              >
                <div
                  v-if="isMoreMenuOpen"
                  class="absolute right-0 top-full mt-2 z-40 w-48 rounded-2xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 shadow-2xl p-1.5 select-none"
                >
                  <a
                    :href="contactFellowLink"
                    target="_blank"
                    rel="noopener noreferrer"
                    @click="isMoreMenuOpen = false"
                    class="w-full flex items-center gap-3 px-3.5 py-2.5 rounded-xl text-xs sm:text-[13px] font-semibold text-slate-900 dark:text-white hover:bg-slate-100/80 dark:hover:bg-slate-800 transition cursor-pointer"
                  >
                    <MessageCircle class="w-4 h-4 text-slate-900 dark:text-white stroke-[2.2]" />
                    <span>{{ t('Contact Fellow') }}</span>
                  </a>
                </div>
              </transition>
            </div>
          </div>

          <!-- Product Title & Rating -->
          <div class="space-y-1.5">
            <h1 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white tracking-tight leading-tight">
              {{ product.name }}
            </h1>

            <div class="flex items-center gap-2 pt-0.5">
              <div class="flex items-center text-slate-900 dark:text-slate-100 font-black text-sm tracking-tighter">
                ★★★★★
              </div>
              <a href="#reviews" class="text-xs font-semibold text-slate-500 dark:text-slate-400 hover:underline">
                {{ product.reviewsCount }} {{ t('ratings') }}
              </a>
              <span class="text-slate-300 dark:text-slate-700">•</span>
              <span class="text-xs font-semibold text-emerald-600 dark:text-emerald-400">{{ t('Verified Hardware') }}</span>
            </div>

            <!-- Price Row -->
            <div class="pt-2 flex items-baseline gap-2.5">
              <span class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white">
                ${{ product.priceUsd.toFixed(2) }}
              </span>
              <span class="text-xs sm:text-sm font-semibold text-slate-400 dark:text-slate-500">
                (≈ {{ (product.priceUsd * 4100).toLocaleString() }} KHR)
              </span>
            </div>
          </div>

          <!-- Variant 1: Color / Finish Swatches (Matches screenshot!) -->
          <div v-if="product.colorOptions?.length" class="space-y-2 pt-1">
            <div class="flex items-center justify-between text-xs font-bold text-slate-900 dark:text-white">
              <span>{{ t('Color') }}: <span class="font-normal text-slate-500 dark:text-slate-400">{{ selectedColor.name }}</span></span>
            </div>

            <div class="flex items-center gap-2.5">
              <button
                v-for="color in product.colorOptions"
                :key="color.name"
                type="button"
                @click="selectedColor = color"
                class="relative h-11 w-11 rounded-full border-2 transition-all p-1 flex items-center justify-center cursor-pointer group"
                :class="selectedColor.name === color.name
                  ? 'border-indigo-600 dark:border-indigo-400 ring-2 ring-indigo-500/20 scale-105'
                  : 'border-slate-200 dark:border-slate-800 hover:border-slate-400 dark:hover:border-slate-600'"
                :title="color.name"
              >
                <span class="h-full w-full rounded-full flex items-center justify-center text-sm shadow-inner" :class="color.colorClass">
                  {{ color.icon }}
                </span>
              </button>
            </div>
          </div>

          <!-- Variant 2: Version / Specification Selection (AeroByte CustomSelect) -->
          <div v-if="product.sizeOptions?.length" class="space-y-2 pt-1">
            <div class="text-xs font-bold text-slate-900 dark:text-white flex items-center justify-between">
              <span>{{ t('Version') }}: <span class="font-normal text-slate-500 dark:text-slate-400">{{ selectedSize }}</span></span>
            </div>

            <div class="w-full">
              <CustomSelect
                v-model="selectedSize"
                :options="product.sizeOptions"
                size="sm"
                trigger-class="!py-2.5 !px-3.5 rounded-xl border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 text-xs font-bold text-slate-800 dark:text-slate-200 shadow-2xs hover:border-slate-300 dark:hover:border-slate-700"
                menu-class="shadow-xl border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800"
              />
            </div>
          </div>

          <!-- Quantity Stepper Row -->
          <div class="space-y-2 pt-1">
            <div class="text-xs font-bold text-slate-900 dark:text-white">
              {{ t('Quantity') }}
            </div>

            <div class="inline-flex items-center rounded-full border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 p-1">
              <button
                type="button"
                @click="quantity = Math.max(1, quantity - 1)"
                class="h-8 w-8 rounded-full hover:bg-white dark:hover:bg-slate-800 flex items-center justify-center text-sm font-black text-slate-700 dark:text-slate-300 transition cursor-pointer"
              >
                -
              </button>
              <span class="w-10 text-center text-xs font-extrabold text-slate-900 dark:text-white">
                {{ quantity }}
              </span>
              <button
                type="button"
                @click="quantity = Math.min(product.stockCount || 99, quantity + 1)"
                class="h-8 w-8 rounded-full hover:bg-white dark:hover:bg-slate-800 flex items-center justify-center text-sm font-black text-slate-700 dark:text-slate-300 transition cursor-pointer"
              >
                +
              </button>
            </div>
          </div>

          <!-- PRIMARY ACTION BUTTONS (Exact Shop.com Design Match!) -->
          <div class="space-y-3 pt-2">
            <!-- 1. Full-Width Purple Add to Cart Button -->
            <button
              type="button"
              @click="handleAddToCart"
              class="w-full py-4 rounded-full bg-[#5046E5] hover:bg-[#4338CA] text-white font-extrabold text-sm tracking-wide shadow-lg hover:shadow-indigo-500/25 active:scale-[0.99] transition-all cursor-pointer flex items-center justify-center gap-2"
            >
              <ShoppingBag class="w-4 h-4" />
              <span>{{ t('Add to cart') }}</span>
            </button>

            <!-- 2. Full-Width Black Buy Now Button -->
            <button
              type="button"
              @click="handleBuyNow"
              class="w-full py-4 rounded-full bg-slate-950 dark:bg-white text-white dark:text-slate-950 hover:bg-slate-800 dark:hover:bg-slate-100 font-extrabold text-sm tracking-wide shadow-md active:scale-[0.99] transition-all cursor-pointer flex items-center justify-center gap-2"
            >
              <Zap class="w-4 h-4 text-amber-400 dark:text-amber-500" />
              <span>{{ t('Buy now') }}</span>
            </button>

            <!-- 3. Twin Secondary Action Buttons: Save & Share (Exact Match!) -->
            <div class="grid grid-cols-2 gap-3 pt-1">
              <button
                type="button"
                @click="toggleFavorite(product.id)"
                class="py-2.5 px-4 rounded-full border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 text-xs font-bold text-slate-800 dark:text-slate-200 flex items-center justify-center gap-2 transition cursor-pointer"
              >
                <Heart class="w-4 h-4" :class="{ 'fill-red-500 text-red-500': isSaved }" />
                <span>{{ isSaved ? t('Saved') : t('Save') }}</span>
              </button>

              <button
                type="button"
                @click="copyProductLink"
                class="py-2.5 px-4 rounded-full border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 hover:bg-slate-50 dark:hover:bg-slate-800 text-xs font-bold text-slate-800 dark:text-slate-200 flex items-center justify-center gap-2 transition cursor-pointer"
              >
                <Share2 class="w-4 h-4" />
                <span>{{ t('Share') }}</span>
              </button>
            </div>
          </div>

          <!-- COLLAPSIBLE ACCORDION SECTIONS (Description, Specs, Box, Delivery) -->
          <div class="pt-4 divide-y divide-slate-100 dark:divide-slate-800/80 border-t border-slate-100 dark:border-slate-800/80">
            
            <!-- 1. Description Accordion -->
            <div class="py-3.5">
              <button
                type="button"
                @click="toggleAccordion('desc')"
                class="w-full flex items-center justify-between text-left text-sm font-extrabold text-slate-900 dark:text-white cursor-pointer"
              >
                <span>{{ t('Description') }}</span>
                <ChevronUp v-if="accordionOpen.desc" class="w-4 h-4 text-slate-400" />
                <ChevronDown v-else class="w-4 h-4 text-slate-400" />
              </button>

              <div v-show="accordionOpen.desc" class="mt-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed space-y-3">
                <p>{{ product.longDescription || product.description }}</p>
                <p>{{ product.description }}</p>
              </div>
            </div>

            <!-- 2. Technical Specifications Accordion -->
            <div class="py-3.5">
              <button
                type="button"
                @click="toggleAccordion('specs')"
                class="w-full flex items-center justify-between text-left text-sm font-extrabold text-slate-900 dark:text-white cursor-pointer"
              >
                <span>{{ t('Technical Specifications') }}</span>
                <ChevronUp v-if="accordionOpen.specs" class="w-4 h-4 text-slate-400" />
                <ChevronDown v-else class="w-4 h-4 text-slate-400" />
              </button>

              <div v-show="accordionOpen.specs" class="mt-3">
                <div class="rounded-2xl bg-slate-50 dark:bg-slate-900/60 p-3.5 border border-slate-100 dark:border-slate-800 divide-y divide-slate-200/60 dark:divide-slate-800 text-xs">
                  <div
                    v-for="(val, key) in product.specs"
                    :key="key"
                    class="py-2 flex items-center justify-between first:pt-0 last:pb-0"
                  >
                    <span class="font-medium text-slate-400">{{ key }}</span>
                    <span class="font-extrabold text-slate-900 dark:text-white text-right">{{ val }}</span>
                  </div>
                </div>
              </div>
            </div>

            <!-- 3. What's in the Box Accordion -->
            <div class="py-3.5">
              <button
                type="button"
                @click="toggleAccordion('box')"
                class="w-full flex items-center justify-between text-left text-sm font-extrabold text-slate-900 dark:text-white cursor-pointer"
              >
                <span>{{ t('What\'s in the Box') }}</span>
                <ChevronUp v-if="accordionOpen.box" class="w-4 h-4 text-slate-400" />
                <ChevronDown v-else class="w-4 h-4 text-slate-400" />
              </button>

              <div v-show="accordionOpen.box" class="mt-3">
                <ul class="space-y-2 text-xs sm:text-sm text-slate-600 dark:text-slate-300">
                  <li
                    v-for="(item, i) in (product.whatsInBox || ['1x Original Hardware Unit', '1x Quick Start Guide'])"
                    :key="i"
                    class="flex items-start gap-2"
                  >
                    <span class="text-indigo-600 dark:text-indigo-400 font-bold">✓</span>
                    <span>{{ item }}</span>
                  </li>
                </ul>
              </div>
            </div>

            <!-- 4. Shipping & Lab Pickup Accordion -->
            <div class="py-3.5">
              <button
                type="button"
                @click="toggleAccordion('shipping')"
                class="w-full flex items-center justify-between text-left text-sm font-extrabold text-slate-900 dark:text-white cursor-pointer"
              >
                <span>{{ t('Shipping & Lab Pickup') }}</span>
                <ChevronUp v-if="accordionOpen.shipping" class="w-4 h-4 text-slate-400" />
                <ChevronDown v-else class="w-4 h-4 text-slate-400" />
              </button>

              <div v-show="accordionOpen.shipping" class="mt-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 space-y-2">
                <div class="flex items-start gap-2">
                  <span class="text-base">🏢</span>
                  <div>
                    <strong class="text-slate-900 dark:text-white">{{ t('Free Lab Pickup') }}</strong>:
                    <p class="text-[11px] sm:text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                      {{ t('Collect your tested hardware directly at AeroByte Academy Campus, Phnom Penh.') }}
                    </p>
                  </div>
                </div>

                <div class="flex items-start gap-2 pt-1">
                  <span class="text-base">🚚</span>
                  <div>
                    <strong class="text-slate-900 dark:text-white">{{ t('Express Phnom Penh Delivery') }}</strong>:
                    <p class="text-[11px] sm:text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                      {{ t('Same-day / next-day delivery via Grab/VET Express ($1.50). Nationwide provinces ($2.50).') }}
                    </p>
                  </div>
                </div>
              </div>
            </div>

          </div>

        </div>

      </div>

      <!-- ==========================================
           CUSTOMER REVIEWS & RATINGS SECTION
           ========================================== -->
      <section id="reviews" class="mt-16 sm:mt-24 pt-12 border-t border-slate-200/80 dark:border-slate-800 scroll-mt-24">
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-8">
          <div>
            <h2 class="text-2xl sm:text-3xl font-black text-slate-900 dark:text-white tracking-tight">
              {{ t('Customer Reviews') }}
            </h2>
            <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
              {{ t('Verified feedback from students, makers, and lab engineers in Cambodia.') }}
            </p>
          </div>

          <button
            type="button"
            @click="openWriteReview"
            class="inline-flex items-center gap-2 px-5 py-2.5 rounded-full bg-slate-900 hover:bg-slate-800 dark:bg-white dark:hover:bg-slate-100 text-white dark:text-slate-900 text-xs sm:text-sm font-bold shadow-md transition active:scale-95 cursor-pointer w-fit"
          >
            <MessageSquare class="w-4 h-4" />
            <span>{{ t('Write a Review') }}</span>
          </button>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 lg:gap-12 items-start">
          <!-- LEFT SUMMARY CARD (lg:col-span-4) -->
          <div class="lg:col-span-4 rounded-3xl bg-slate-50/80 dark:bg-slate-900/60 border border-slate-200/70 dark:border-slate-800 p-6 sm:p-7 space-y-6">
            <div class="flex items-baseline gap-3">
              <span class="text-5xl font-black text-slate-900 dark:text-white tracking-tight">4.9</span>
              <div>
                <div class="flex items-center text-amber-400 text-lg tracking-tighter">
                  ★★★★★
                </div>
                <div class="text-[11px] font-semibold text-slate-400 mt-0.5">
                  {{ t('Based on') }} {{ product.reviewsCount || '1.2K' }} {{ t('ratings') }}
                </div>
              </div>
            </div>

            <!-- Star Progress Breakdown -->
            <div class="space-y-2 text-xs">
              <div
                v-for="bar in [
                  { star: 5, pct: 88, count: '88%' },
                  { star: 4, pct: 9, count: '9%' },
                  { star: 3, pct: 2, count: '2%' },
                  { star: 2, pct: 1, count: '<1%' },
                  { star: 1, pct: 0, count: '0%' }
                ]"
                :key="bar.star"
                class="flex items-center gap-2.5 text-slate-600 dark:text-slate-400"
              >
                <span class="w-7 font-bold text-slate-700 dark:text-slate-300 text-right">{{ bar.star }} ★</span>
                <div class="flex-1 h-2 rounded-full bg-slate-200 dark:bg-slate-800 overflow-hidden">
                  <div class="h-full rounded-full bg-amber-400" :style="{ width: `${bar.pct}%` }"></div>
                </div>
                <span class="w-8 text-[11px] text-slate-400 text-right font-medium">{{ bar.count }}</span>
              </div>
            </div>

            <!-- Recommendation callout -->
            <div class="pt-4 border-t border-slate-200/70 dark:border-slate-800 flex items-center gap-3">
              <div class="h-10 w-10 rounded-2xl bg-emerald-100 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0">
                <Check class="w-5 h-5 stroke-[2.5]" />
              </div>
              <div>
                <div class="text-xs font-bold text-slate-900 dark:text-white">98% Recommendation</div>
                <div class="text-[11px] text-slate-400 mt-0.5">Students recommend this hardware for practical labs</div>
              </div>
            </div>
          </div>

          <!-- RIGHT REVIEWS FEED (lg:col-span-8) -->
          <div class="lg:col-span-8 space-y-5">
            <!-- Filter Pills -->
            <div class="flex items-center gap-2 overflow-x-auto pb-1 no-scrollbar">
              <button
                type="button"
                @click="selectedReviewFilter = 'all'"
                class="h-8 px-3.5 rounded-full text-xs font-semibold transition active:scale-95 cursor-pointer whitespace-nowrap"
                :class="selectedReviewFilter === 'all'
                  ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 font-bold shadow-xs'
                  : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300'"
              >
                {{ t('All Reviews') }} ({{ allReviews.length }})
              </button>

              <button
                type="button"
                @click="selectedReviewFilter = 5"
                class="h-8 px-3.5 rounded-full text-xs font-semibold transition active:scale-95 cursor-pointer whitespace-nowrap"
                :class="selectedReviewFilter === 5
                  ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 font-bold shadow-xs'
                  : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300'"
              >
                5 ★ ({{ allReviews.filter(r => r.rating === 5).length }})
              </button>

              <button
                type="button"
                @click="selectedReviewFilter = 4"
                class="h-8 px-3.5 rounded-full text-xs font-semibold transition active:scale-95 cursor-pointer whitespace-nowrap"
                :class="selectedReviewFilter === 4
                  ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 font-bold shadow-xs'
                  : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300'"
              >
                4 ★ ({{ allReviews.filter(r => r.rating === 4).length }})
              </button>

              <button
                type="button"
                @click="selectedReviewFilter = 'verified'"
                class="h-8 px-3.5 rounded-full text-xs font-semibold transition active:scale-95 cursor-pointer whitespace-nowrap"
                :class="selectedReviewFilter === 'verified'
                  ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900 font-bold shadow-xs'
                  : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 text-slate-600 dark:text-slate-300'"
              >
                ✓ {{ t('Verified Buyer') }}
              </button>
            </div>

            <!-- Review Cards -->
            <div class="space-y-4">
              <article
                v-for="rev in filteredReviews"
                :key="rev.id"
                class="rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/80 dark:border-slate-800 p-5 sm:p-6 shadow-2xs space-y-3 transition hover:border-slate-300 dark:hover:border-slate-700"
              >
                <!-- Reviewer Header -->
                <div class="flex items-start justify-between gap-3">
                  <div class="flex items-center gap-3">
                    <div
                      class="h-10 w-10 rounded-full flex items-center justify-center font-bold text-white text-xs shrink-0 shadow-xs"
                      :class="rev.avatarColor || 'bg-indigo-600'"
                    >
                      {{ rev.author.split(' ').map(n => n[0]).join('').slice(0, 2) }}
                    </div>
                    <div>
                      <div class="flex items-center gap-2">
                        <span class="text-xs sm:text-sm font-bold text-slate-900 dark:text-white">{{ rev.author }}</span>
                        <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200/60 dark:border-emerald-800">
                          <Check class="w-2.5 h-2.5 stroke-[3]" />
                          <span>{{ rev.badge || t('Verified Student') }}</span>
                        </span>
                      </div>
                      <div class="flex items-center gap-2 mt-0.5 text-[11px] text-slate-400">
                        <span>{{ rev.date }}</span>
                        <span v-if="rev.variant">•</span>
                        <span v-if="rev.variant">{{ rev.variant }}</span>
                      </div>
                    </div>
                  </div>

                  <!-- Stars -->
                  <div class="flex items-center text-amber-400 text-sm tracking-tight">
                    <span v-for="s in 5" :key="s" :class="s <= rev.rating ? 'text-amber-400' : 'text-slate-200 dark:text-slate-700'">★</span>
                  </div>
                </div>

                <!-- Review Content -->
                <div class="space-y-1.5">
                  <h4 class="text-xs sm:text-sm font-bold text-slate-900 dark:text-white">
                    {{ rev.title }}
                  </h4>
                  <p class="text-xs sm:text-[13px] text-slate-600 dark:text-slate-300 leading-relaxed">
                    {{ rev.content }}
                  </p>
                </div>

                <!-- Helpful Button -->
                <div class="pt-2 flex items-center gap-2">
                  <button
                    type="button"
                    @click="toggleHelpful(rev)"
                    class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full text-xs font-semibold transition active:scale-95 cursor-pointer"
                    :class="rev.userHelpful
                      ? 'bg-indigo-50 dark:bg-indigo-950/80 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800'
                      : 'bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-750 text-slate-600 dark:text-slate-400'"
                  >
                    <ThumbsUp class="w-3.5 h-3.5" :class="{ 'fill-indigo-600 dark:fill-indigo-400': rev.userHelpful }" />
                    <span>{{ t('Helpful') }} ({{ rev.helpfulCount }})</span>
                  </button>
                </div>
              </article>
            </div>
          </div>
        </div>

        <!-- Write Review Modal -->
        <div
          v-if="isWriteReviewOpen"
          class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-950/60 backdrop-blur-xs overflow-y-auto"
          @click.self="isWriteReviewOpen = false"
        >
          <div class="w-full max-w-lg rounded-3xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 p-6 sm:p-7 shadow-2xl relative my-8">
            <button
              type="button"
              @click="isWriteReviewOpen = false"
              class="absolute top-5 right-5 text-slate-400 hover:text-slate-700 dark:hover:text-white cursor-pointer"
            >
              <X class="w-5 h-5" />
            </button>

            <h3 class="text-lg font-bold text-slate-900 dark:text-white">{{ t('Write a Review') }}</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
              Share your feedback for <span class="font-bold text-slate-800 dark:text-slate-200">{{ product.name }}</span>
            </p>

            <form @submit.prevent="submitNewReview" class="mt-5 space-y-4">
              <!-- Rating Picker -->
              <div>
                <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1.5">{{ t('Your Rating') }}</label>
                <div class="flex items-center gap-1.5">
                  <button
                    v-for="star in 5"
                    :key="star"
                    type="button"
                    @click="reviewForm.rating = star"
                    @mouseenter="reviewHoverRating = star"
                    @mouseleave="reviewHoverRating = 0"
                    class="text-2xl transition cursor-pointer"
                    :class="(reviewHoverRating || reviewForm.rating) >= star ? 'text-amber-400' : 'text-slate-200 dark:text-slate-700'"
                  >
                    ★
                  </button>
                  <span class="text-xs font-bold text-slate-600 dark:text-slate-400 ml-2">
                    {{ reviewHoverRating || reviewForm.rating }} / 5 Stars
                  </span>
                </div>
              </div>

              <!-- Name -->
              <div>
                <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">{{ t('Your Name') }}</label>
                <input
                  v-model="reviewForm.name"
                  type="text"
                  required
                  placeholder="e.g. Sokha Chan"
                  class="w-full rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 px-3.5 py-2.5 text-xs text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
                />
              </div>

              <!-- Title -->
              <div>
                <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">{{ t('Review Title') }}</label>
                <input
                  v-model="reviewForm.title"
                  type="text"
                  placeholder="e.g. Great kit for STEM coursework"
                  class="w-full rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 px-3.5 py-2.5 text-xs text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20"
                />
              </div>

              <!-- Comment -->
              <div>
                <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">{{ t('Your Review') }}</label>
                <textarea
                  v-model="reviewForm.content"
                  rows="4"
                  required
                  placeholder="Write your honest review about component quality, assembly, and performance..."
                  class="w-full rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-800 px-3.5 py-2.5 text-xs text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-indigo-500/20 resize-none"
                ></textarea>
              </div>

              <div class="flex items-center gap-3 pt-2">
                <button
                  type="button"
                  @click="isWriteReviewOpen = false"
                  class="flex-1 py-2.5 rounded-full border border-slate-200 dark:border-slate-700 text-xs font-bold text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 transition cursor-pointer"
                >
                  {{ t('Cancel') }}
                </button>
                <button
                  type="submit"
                  class="flex-1 py-2.5 rounded-full bg-slate-900 hover:bg-slate-800 text-white dark:bg-white dark:text-slate-900 text-xs font-bold transition shadow-md cursor-pointer"
                >
                  {{ t('Submit Review') }}
                </button>
              </div>
            </form>
          </div>
        </div>
      </section>


      <!-- ==========================================
           BOTTOM SEARCH PILL PROMPT (Exact match to Shop.com screenshot!)
           ========================================== -->
      <div class="mt-16 sm:mt-24 pt-8 border-t border-slate-100 dark:border-slate-800 flex justify-center">
        <div class="w-full max-w-xl">
          <RouterLink
            to="/store#catalog"
            class="w-full flex items-center justify-between px-6 py-4 rounded-full bg-slate-50 dark:bg-slate-900 border border-slate-200 dark:border-slate-800 text-slate-500 dark:text-slate-400 hover:border-slate-300 dark:hover:border-slate-700 hover:shadow-md transition text-xs sm:text-sm group"
          >
            <span>{{ t('What are you shopping for today?') }}</span>
            <span class="h-8 w-8 rounded-full bg-slate-200 dark:bg-slate-800 text-slate-900 dark:text-white flex items-center justify-center group-hover:translate-x-1 transition-transform">
              →
            </span>
          </RouterLink>
        </div>
      </div>

      <!-- ==========================================
           RELATED PRODUCTS SECTION
           ========================================== -->
      <section class="mt-14 pt-10 border-t border-slate-100 dark:border-slate-800">
        <div class="flex items-center justify-between mb-6">
          <div>
            <h3 class="text-lg sm:text-xl font-black text-slate-900 dark:text-white">
              {{ t('You Might Also Like') }}
            </h3>
            <p class="text-xs text-slate-400 mt-0.5">
              {{ t('More authentic hardware & kits from') }} {{ product.category }}
            </p>
          </div>
          <RouterLink
            to="/store"
            class="text-xs font-bold text-indigo-600 dark:text-indigo-400 hover:underline"
          >
            {{ t('View all products →') }}
          </RouterLink>
        </div>

        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 sm:gap-6">
          <RouterLink
            v-for="rel in relatedProducts"
            :key="rel.id"
            :to="`/store/${rel.id}`"
            class="group flex flex-col justify-between"
          >
            <div class="relative aspect-[4/5] rounded-2xl bg-[#f5f5f7] dark:bg-slate-900 border border-slate-200/60 dark:border-slate-800 p-4 flex items-center justify-center overflow-hidden transition-all duration-300 group-hover:shadow-md">
              <span class="text-6xl group-hover:scale-108 transition-transform duration-300 select-none">
                {{ rel.icon }}
              </span>
            </div>
            <div class="mt-2.5 px-0.5 space-y-0.5">
              <div class="text-[10px] text-slate-400 font-medium truncate">{{ rel.brand }}</div>
              <h4 class="text-xs font-bold text-slate-900 dark:text-white truncate group-hover:text-indigo-600 dark:group-hover:text-indigo-400">
                {{ rel.name }}
              </h4>
              <div class="text-xs font-black text-slate-900 dark:text-white">
                ${{ rel.priceUsd.toFixed(2) }}
              </div>
            </div>
          </RouterLink>
        </div>
      </section>
    </main>

    <!-- Slide-Over Shopping Bag Drawer (Shared with Store) -->
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

          <div class="flex-1 overflow-y-auto p-5 space-y-4">
            <div v-if="cartItems.length === 0" class="text-center py-20">
              <div class="text-4xl mb-3">🛍️</div>
              <h4 class="text-sm font-bold text-slate-900 dark:text-white">{{ t('Your Bag is Empty') }}</h4>
              <p class="text-xs text-slate-400 mt-1 max-w-xs mx-auto">
                {{ t('Explore our authentic robotics kits, drone parts, and 3D filaments to start building.') }}
              </p>
            </div>

            <div v-else class="space-y-3">
              <div
                v-for="item in cartItems"
                :key="item.cartKey || item.id"
                class="flex items-center gap-3 p-3 rounded-2xl bg-slate-50 dark:bg-slate-800/50 border border-slate-100 dark:border-slate-800"
              >
                <div class="h-14 w-14 rounded-xl bg-white dark:bg-slate-800 flex items-center justify-center text-2xl shrink-0 border border-slate-200/60 dark:border-slate-700/60">
                  {{ item.icon }}
                </div>

                <div class="flex-1 min-w-0">
                  <div class="text-[10px] text-slate-400 font-medium">{{ item.brand || item.category }}</div>
                  <h4 class="text-xs font-bold text-slate-900 dark:text-white truncate">{{ item.name }}</h4>
                  <div v-if="item.selectedVariant" class="text-[10px] font-semibold text-indigo-600 dark:text-indigo-400">
                    {{ item.selectedVariant }}
                  </div>
                  <div class="text-xs font-bold text-slate-900 dark:text-white mt-0.5">
                    ${{ (item.priceUsd * item.quantity).toFixed(2) }}
                  </div>

                  <div class="flex items-center gap-2 mt-2">
                    <button
                      type="button"
                      @click="updateCartQuantity(item.cartKey || item.id, item.quantity - 1)"
                      class="h-6 w-6 rounded-full border border-slate-200 dark:border-slate-700 flex items-center justify-center text-xs font-bold hover:bg-slate-100 dark:hover:bg-slate-700 cursor-pointer"
                    >-</button>
                    <span class="text-xs font-bold text-slate-800 dark:text-white w-6 text-center">{{ item.quantity }}</span>
                    <button
                      type="button"
                      @click="updateCartQuantity(item.cartKey || item.id, item.quantity + 1)"
                      class="h-6 w-6 rounded-full border border-slate-200 dark:border-slate-700 flex items-center justify-center text-xs font-bold hover:bg-slate-100 dark:hover:bg-slate-700 cursor-pointer"
                    >+</button>
                  </div>
                </div>

                <button
                  type="button"
                  @click="removeFromCart(item.cartKey || item.id)"
                  class="p-1.5 text-slate-400 hover:text-red-500 transition cursor-pointer"
                >
                  <Trash2 class="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>

          <div v-if="cartItems.length > 0" class="p-5 border-t border-slate-100 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-900/60 space-y-3">
            <div class="flex items-center justify-between text-base font-black text-slate-900 dark:text-white">
              <span>{{ t('Total Amount') }}:</span>
              <div class="text-right">
                <div>${{ cartTotalUsd.toFixed(2) }}</div>
                <div class="text-[10px] font-semibold text-slate-400">
                  ≈ {{ (cartTotalUsd * 4100).toLocaleString() }} KHR
                </div>
              </div>
            </div>

            <a
              :href="cartTelegramCheckoutLink"
              target="_blank"
              rel="noopener"
              class="w-full rounded-full bg-slate-900 hover:bg-slate-800 dark:bg-white dark:hover:bg-slate-100 dark:text-slate-900 text-white font-bold py-3.5 px-4 text-xs shadow-md transition flex items-center justify-center gap-2"
            >
              <span>💬</span>
              <span>{{ t('Checkout Order on Telegram') }}</span>
            </a>
          </div>
        </div>
      </div>
    </div>

    <!-- Toast Notification -->
    <div
      v-if="toastMessage"
      class="fixed bottom-6 right-6 z-50 flex items-center gap-2 rounded-2xl bg-slate-900 dark:bg-white text-white dark:text-slate-900 px-4 py-3 text-xs font-bold shadow-xl border border-slate-700 dark:border-slate-200 animate-bounce"
    >
      <span>✨</span>
      <span>{{ toastMessage }}</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, reactive } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from '../i18n'
import {
  ChevronLeft,
  ChevronDown,
  ChevronUp,
  Heart,
  ShoppingBag,
  MoreHorizontal,
  MessageCircle,
  Share2,
  Star,
  ThumbsUp,
  Check,
  MessageSquare,
  Zap,
  Trash2,
  X
} from 'lucide-vue-next'
import CustomSelect from '../components/common/CustomSelect.vue'
import { getProductById, getRelatedProducts } from '../data/products'
import { useStoreCart } from '../composables/useStoreCart'

const route = useRoute()
const router = useRouter()
const { t } = useI18n()

const {
  isCartOpen,
  cartItems,
  addToCart,
  updateCartQuantity,
  removeFromCart,
  toggleFavorite,
  isFavorite,
  totalCartItemsCount,
  cartTotalUsd,
  cartTelegramCheckoutLink,
  toastMessage,
  showToast
} = useStoreCart()

// Fetch product by route param :id
const isMoreMenuOpen = ref(false)
const contactFellowLink = computed(() => {
  const pName = product.value ? product.value.name : 'Hardware Kit'
  const pPrice = product.value ? `$${product.value.priceUsd}` : ''
  const msg = `Hello AeroByte Fellow! I have a question about ${pName} (${pPrice}).`
  return `https://t.me/aerobyte_academy?text=${encodeURIComponent(msg)}`
})
const productId = computed(() => String(route.params.id || ''))
const product = computed(() => getProductById(productId.value))

// Gallery Active Index
const activeGalleryIdx = ref(0)
const productGallery = computed(() => {
  if (!product.value) return []
  return product.value.gallery || [
    { label: 'Front', icon: product.value.icon, title: product.value.name }
  ]
})

const activeView = computed(() => {
  if (!productGallery.value.length) return {}
  return productGallery.value[activeGalleryIdx.value] || productGallery.value[0]
})

// Variant states
const selectedColor = ref(null)
const selectedSize = ref('')
const quantity = ref(1)

// Accordion open/close states
const accordionOpen = reactive({
  desc: true,
  specs: true,
  box: false,
  shipping: false
})

function toggleAccordion(key) {
  accordionOpen[key] = !accordionOpen[key]
}

// Watch for product changes to reset selections
watch(
  product,
  (p) => {
    if (p) {
      activeGalleryIdx.value = 0
      selectedColor.value = p.colorOptions?.[0] || null
      selectedSize.value = p.sizeOptions?.[0] || ''
      quantity.value = 1
    }
  },
  { immediate: true }
)

const isSaved = computed(() => {
  if (!product.value) return false
  return isFavorite(product.value.id)
})

const relatedProducts = computed(() => {
  if (!product.value) return []
  return getRelatedProducts(product.value.id, product.value.category, 4)
})

function handleAddToCart() {
  if (!product.value) return
  const variantSummary = [
    selectedColor.value?.name,
    selectedSize.value
  ].filter(Boolean).join(' / ')

  addToCart(product.value, quantity.value, variantSummary)
  isCartOpen.value = true
}

function handleBuyNow() {
  if (!product.value) return
  handleAddToCart()
  // Immediate telegram checkout or prompt
  const telegramUrl = cartTelegramCheckoutLink.value
  if (typeof window !== 'undefined') {
    window.open(telegramUrl, '_blank')
  }
}

// Reviews Logic & Dataset
const defaultReviews = [
  {
    id: 'rev-1',
    author: 'Vireak S.',
    avatarColor: 'bg-emerald-600',
    rating: 5,
    title: 'Exceptional quality for robotics coursework!',
    content: 'Bought this kit for my final year embedded systems project at ITC. All components are authentic, ESP32 flashed without issue, and motor shield handles 2S Li-ion batteries smoothly. Fast lab pickup in Phnom Penh!',
    date: '2 days ago',
    verified: true,
    badge: 'Verified Student',
    variant: 'Standard Kit',
    helpfulCount: 28,
    userHelpful: false
  },
  {
    id: 'rev-2',
    author: 'Sophea Meng',
    avatarColor: 'bg-indigo-600',
    rating: 5,
    title: 'Well packaged & beginner-friendly documentation',
    content: 'Very impressed with the hardware build. The motor driver and chassis fit together seamlessly. Customer service on Telegram answered my wiring questions within 10 minutes.',
    date: '1 week ago',
    verified: true,
    badge: 'Lab Fellow',
    variant: 'Pro with Sensors',
    helpfulCount: 19,
    userHelpful: false
  },
  {
    id: 'rev-3',
    author: 'Dara Kim',
    avatarColor: 'bg-amber-600',
    rating: 5,
    title: 'Solid precision hardware, zero issues',
    content: 'Genuine authentic parts. Tested the telemetry via Wi-Fi dashboard and latency was under 20ms. Exactly what our university STEM club needed.',
    date: '2 weeks ago',
    verified: true,
    badge: 'Verified Student',
    variant: 'Standard Kit',
    helpfulCount: 12,
    userHelpful: false
  },
  {
    id: 'rev-4',
    author: 'Bona Chen',
    avatarColor: 'bg-purple-600',
    rating: 4,
    title: 'Great value, fast delivery in Phnom Penh',
    content: 'Ordered via Grab delivery and arrived within 2 hours. Kit is complete with extra screws and standoffs. Would love to see additional sensor attachments in the future.',
    date: '3 weeks ago',
    verified: true,
    badge: 'Verified Buyer',
    variant: 'Standard Kit',
    helpfulCount: 8,
    userHelpful: false
  }
]

const customReviews = ref([])

function loadCustomReviews() {
  if (typeof localStorage === 'undefined') return
  try {
    const raw = localStorage.getItem(`aerobyte_reviews_${productId.value}`)
    customReviews.value = raw ? JSON.parse(raw) : []
  } catch {
    customReviews.value = []
  }
}

watch(productId, () => {
  loadCustomReviews()
}, { immediate: true })

const allReviews = computed(() => {
  return [...customReviews.value, ...defaultReviews]
})

const selectedReviewFilter = ref('all')

const filteredReviews = computed(() => {
  if (selectedReviewFilter.value === 'all') return allReviews.value
  if (selectedReviewFilter.value === 'verified') return allReviews.value.filter(r => r.verified)
  return allReviews.value.filter(r => r.rating === selectedReviewFilter.value)
})

const isWriteReviewOpen = ref(false)
const reviewForm = reactive({
  name: '',
  rating: 5,
  title: '',
  content: ''
})
const reviewHoverRating = ref(0)

function openWriteReview() {
  reviewForm.name = ''
  reviewForm.rating = 5
  reviewForm.title = ''
  reviewForm.content = ''
  reviewHoverRating.value = 0
  isWriteReviewOpen.value = true
}

function submitNewReview() {
  if (!reviewForm.name.trim() || !reviewForm.content.trim()) return

  const newRev = {
    id: 'rev-' + Date.now(),
    author: reviewForm.name.trim(),
    avatarColor: 'bg-indigo-700',
    rating: reviewForm.rating,
    title: reviewForm.title.trim() || t('Verified Review'),
    content: reviewForm.content.trim(),
    date: 'Just now',
    verified: true,
    badge: 'Verified Buyer',
    variant: selectedSize.value || 'Standard Kit',
    helpfulCount: 0,
    userHelpful: false
  }

  customReviews.value.unshift(newRev)
  try {
    localStorage.setItem(
      `aerobyte_reviews_${productId.value}`,
      JSON.stringify(customReviews.value)
    )
  } catch {}

  isWriteReviewOpen.value = false
  showToast(t('Thank you! Your review has been submitted.'))
}

function toggleHelpful(review) {
  if (review.userHelpful) {
    review.helpfulCount--
    review.userHelpful = false
  } else {
    review.helpfulCount++
    review.userHelpful = true
  }
}


function copyProductLink() {
  if (typeof window === 'undefined') return
  const url = window.location.href
  if (navigator.clipboard) {
    navigator.clipboard.writeText(url)
    showToast('Product link copied to clipboard!')
  }
}
</script>
