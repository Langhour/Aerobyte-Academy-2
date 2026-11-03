<template>
  <div class="min-h-screen pb-24 bg-white dark:bg-slate-950 transition-colors">
    <!-- Top Announcement Bar (Minimalist Luxury Style) -->
    <div class="border-b border-slate-100 dark:border-slate-800/80 bg-slate-50 dark:bg-slate-900/60 py-2.5 px-4 text-xs text-slate-700 dark:text-slate-300">
      <div class="mx-auto max-w-7xl flex flex-wrap items-center justify-between gap-3">
        <div class="flex items-center gap-2">
          <span class="inline-flex h-2 w-2 rounded-full bg-emerald-500 animate-pulse"></span>
          <span class="font-medium">
            <strong class="font-bold text-slate-900 dark:text-white">AeroByte Hardware Lab:</strong>
            {{ t('Authentic robotics kits, drone parts & filaments. Free same-day lab pickup in Phnom Penh.') }}
          </span>
        </div>

        <div class="flex items-center gap-4 text-[11px] sm:text-xs">
          <span class="hidden md:inline text-slate-500 dark:text-slate-400">
            {{ t('Student Code:') }} <code class="font-bold text-slate-900 dark:text-white bg-slate-200/80 dark:bg-slate-800 px-1.5 py-0.5 rounded">AEROSTUDENT</code> (-10%)
          </span>
          <button
            type="button"
            @click="isCartOpen = true"
            class="flex items-center gap-1.5 font-bold text-slate-900 dark:text-white hover:text-indigo-600 dark:hover:text-indigo-400 transition cursor-pointer"
          >
            <ShoppingBag class="w-3.5 h-3.5" />
            <span>{{ t('Bag') }} ({{ totalCartItemsCount }})</span>
          </button>
        </div>
      </div>
    </div>

    <!-- 2. Commercial Hero Showcase Banner (AeroByte Official Dark Blue #102a49) -->
    <section class="px-3 sm:px-6 lg:px-8 pt-4 pb-6 sm:pb-10">
      <div class="mx-auto w-full max-w-[1640px]">
        <div class="relative overflow-hidden rounded-[28px] sm:rounded-[36px] bg-[#102a49] shadow-2xl border border-navy-800/80 aspect-[16/9] sm:aspect-[2/1] lg:aspect-[2.1/1] xl:aspect-[2.2/1] min-h-[440px] sm:min-h-[520px] lg:min-h-[560px] max-h-[640px] flex items-center">
          
          <!-- Background Showcase Image (Staged Products on Left, Deep Navy Space on Right - 100% Bright, Sharp & Natural) -->
          <img
            src="/assets/brand/store-hero-showcase.jpg"
            alt="AeroByte Maker Kit Hardware Showcase"
            class="absolute inset-0 w-full h-full object-cover object-left select-none"
          />

          <!-- Content Grid overlaying the banner -->
          <div class="relative z-10 w-full px-6 sm:px-10 lg:px-16 py-10 sm:py-16 grid grid-cols-1 lg:grid-cols-12 gap-8 items-center h-full">
            <!-- Left spacer so all staged products (Box, Drone, PCB & 3D Printer) remain completely visible without overlap -->
            <div class="hidden lg:block lg:col-span-6 xl:col-span-6 pointer-events-none"></div>

            <!-- Right: Big Punchy Typography & "SHOP ALL" Button -->
            <div class="lg:col-span-6 xl:col-span-6 flex flex-col items-center justify-center text-center">
              <h1 class="text-3xl sm:text-5xl md:text-6xl lg:text-7xl xl:text-[80px] font-black text-white tracking-tight uppercase leading-[1.05] drop-shadow-md select-none">
                <span class="whitespace-nowrap">AERO STORE</span><br />
                2026!
              </h1>

              <!-- Yellow/Amber SHOP ALL Pill Button -->
              <a
                href="#catalog"
                class="mt-6 sm:mt-8 inline-flex items-center justify-center px-10 sm:px-12 py-3.5 sm:py-4.5 rounded-full bg-amber-400 hover:bg-amber-300 text-[#102a49] font-black text-sm sm:text-base uppercase tracking-wider shadow-2xl hover:shadow-amber-400/30 hover:scale-105 active:scale-95 transition-all duration-200 cursor-pointer"
              >
                SHOP ALL
              </a>
            </div>
          </div>

        </div>
      </div>
    </section>

    <!-- Header & Brand Bar -->
    <header id="catalog" class="border-b border-slate-100 dark:border-slate-800/80 pt-8 pb-6 px-4 sm:px-6 lg:px-8">
      <div class="mx-auto max-w-7xl">
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

        <!-- Category Horizontal Filter Bar (Clean Minimalist Pills) -->
        <div class="mt-7 flex items-center justify-between gap-3 border-t border-slate-100 dark:border-slate-800/80 pt-4 overflow-x-auto no-scrollbar">
          <div class="flex items-center gap-1.5 sm:gap-2 shrink-0">
            <button
              type="button"
              @click="selectedCategory = 'All'"
              class="px-3.5 py-1.5 rounded-full text-xs font-semibold transition cursor-pointer whitespace-nowrap"
              :class="selectedCategory === 'All'
                ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900'
                : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'"
            >
              {{ t('All') }} ({{ products.length }})
            </button>

            <button
              v-for="cat in categoryList"
              :key="cat"
              type="button"
              @click="selectedCategory = cat"
              class="px-3.5 py-1.5 rounded-full text-xs font-semibold transition cursor-pointer whitespace-nowrap"
              :class="selectedCategory === cat
                ? 'bg-slate-900 text-white dark:bg-white dark:text-slate-900'
                : 'text-slate-600 dark:text-slate-400 hover:bg-slate-100 dark:hover:bg-slate-800'"
            >
              {{ t(cat) }}
            </button>
          </div>

          <!-- Secondary Quick Filters (In Stock Only + Sort) -->
          <div class="flex items-center gap-3 shrink-0 pl-4 border-l border-slate-200 dark:border-slate-800 text-xs text-slate-600 dark:text-slate-400">
            <label class="flex items-center gap-1.5 cursor-pointer select-none">
              <input
                type="checkbox"
                v-model="inStockOnly"
                class="rounded text-slate-900 focus:ring-0 cursor-pointer"
              />
              <span class="font-medium text-[11px] sm:text-xs">{{ t('In Stock Only') }}</span>
            </label>

            <select
              v-model="sortBy"
              class="rounded-lg border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 px-2.5 py-1 text-xs font-semibold text-slate-800 dark:text-slate-200 focus:outline-none cursor-pointer"
            >
              <option value="featured">{{ t('Featured') }}</option>
              <option value="price-low">{{ t('Price: Low to High') }}</option>
              <option value="price-high">{{ t('Price: High to Low') }}</option>
              <option value="rating">{{ t('Top Rated') }}</option>
            </select>
          </div>
        </div>
      </div>
    </header>

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
            @click="openQuickView(item)"
            class="relative aspect-[4/5] w-full rounded-[20px] sm:rounded-[24px] bg-[#f5f5f7] dark:bg-slate-850/80 border border-slate-200/50 dark:border-slate-800/60 p-4 sm:p-6 flex items-center justify-center overflow-hidden transition-all duration-300 hover:shadow-md cursor-pointer select-none"
          >
            <!-- Badge 1: Viral / Special Badge (Top-Left) -->
            <div
              v-if="item.badge"
              class="absolute top-3 left-3 z-10"
            >
              <div
                v-if="item.badgeType === 'tiktok'"
                class="flex items-center gap-1 px-2 py-0.5 rounded-full bg-slate-900 text-white text-[9px] font-bold tracking-tight shadow-2xs"
              >
                <span>💚</span>
                <span>VIRAL ON TikTok</span>
              </div>
              <div
                v-else
                class="px-2 py-0.5 rounded-full bg-slate-900/90 text-white text-[9px] font-bold tracking-tight backdrop-blur-xs"
              >
                {{ item.badge }}
              </div>
            </div>

            <!-- Badge 2: Award / Seal Badge (Top-Right) -->
            <div
              v-if="item.awardBadge"
              class="absolute top-3 right-3 z-10 h-7 w-7 rounded-full bg-slate-900 text-white text-[8px] font-extrabold flex items-center justify-center text-center p-0.5 shadow-2xs leading-tight"
            >
              ★ LAB
            </div>

            <!-- Centered Floating Hardware / Product Visual -->
            <div class="flex h-full w-full items-center justify-center text-6xl sm:text-7xl group-hover:scale-108 transition-transform duration-300 drop-shadow-sm">
              <span>{{ item.icon }}</span>
            </div>

            <!-- Hover Action Buttons (Heart Favorite & Add to Cart - Visible on Hover) -->
            <div class="absolute bottom-3 right-3 z-20 flex items-center gap-1.5 transition-all duration-300">
              <!-- Add to Cart Icon Button -->
              <button
                type="button"
                @click.stop="addToCart(item)"
                :title="t('Add to Bag')"
                class="h-7 w-7 sm:h-8 sm:w-8 rounded-full bg-slate-900 hover:bg-slate-800 text-white flex items-center justify-center shadow-md transition-all duration-200 cursor-pointer active:scale-90 transform translate-y-1 sm:translate-y-2 group-hover:translate-y-0 opacity-90 sm:opacity-0 sm:group-hover:opacity-100"
              >
                <ShoppingCart class="w-3.5 h-3.5 sm:w-4 sm:h-4" />
              </button>

              <!-- Heart Favorite Icon Button (matches Reference Card 5!) -->
              <button
                type="button"
                @click.stop="toggleFavorite(item.id)"
                :title="t('Favorite')"
                class="h-7 w-7 sm:h-8 sm:w-8 rounded-full flex items-center justify-center shadow-md transition-all duration-200 cursor-pointer active:scale-90 transform translate-y-1 sm:translate-y-2 group-hover:translate-y-0"
                :class="isFavorite(item.id)
                  ? 'opacity-100 translate-y-0 bg-red-500 text-white'
                  : 'opacity-90 sm:opacity-0 sm:group-hover:opacity-100 bg-slate-400/80 hover:bg-slate-500 text-white backdrop-blur-xs'"
              >
                <Heart class="w-3.5 h-3.5 sm:w-4 sm:h-4" :class="{ 'fill-white': isFavorite(item.id) }" />
              </button>
            </div>

            <!-- Quick Add Pill (Bottom-Left on Hover) -->
            <div
              class="absolute bottom-3 left-3 z-20 px-2.5 py-1 rounded-full bg-slate-900/90 hover:bg-slate-900 text-white text-[10px] sm:text-[11px] font-bold backdrop-blur-xs opacity-0 sm:group-hover:opacity-100 transition-all duration-200 transform translate-y-1 sm:translate-y-2 group-hover:translate-y-0 shadow-sm flex items-center gap-1 cursor-pointer"
              @click.stop="addToCart(item)"
            >
              <Plus class="w-3 h-3" />
              <span>{{ t('Quick Add') }}</span>
            </div>
          </div>

          <!-- 2. Typography & Details BELOW the Card (Matches Reference Screenshot) -->
          <div class="mt-2.5 sm:mt-3 px-0.5 space-y-0.5">
            <!-- Brand / Category Name (Subtle muted gray text, line 1) -->
            <div class="text-[11px] sm:text-xs font-medium text-slate-400 dark:text-slate-500 truncate">
              {{ item.brand || item.category }}
            </div>

            <!-- Product Title (Bold clean typography, line 2) -->
            <h3
              @click="openQuickView(item)"
              class="text-xs sm:text-sm font-bold text-slate-900 dark:text-white line-clamp-1 hover:text-indigo-600 dark:hover:text-indigo-400 transition cursor-pointer"
            >
              {{ item.name }}
            </h3>

            <!-- Star Rating Row: Solid black stars + review count (line 3) -->
            <div class="flex items-center gap-1 text-[11px] sm:text-xs text-slate-900 dark:text-slate-100 font-bold">
              <span class="tracking-tighter">★★★★★</span>
              <span class="font-normal text-slate-500 dark:text-slate-400">({{ item.reviewsCount || item.reviews }})</span>
            </div>

            <!-- Clean Price (line 4) -->
            <div class="pt-0.5 flex items-baseline gap-1.5 text-xs sm:text-sm font-bold text-slate-900 dark:text-white">
              <span>${{ item.priceUsd.toFixed(2) }}</span>
              <span class="text-[10px] sm:text-[11px] font-normal text-slate-400">
                · {{ (item.priceUsd * 4100).toLocaleString() }}៛
              </span>
            </div>
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

    <!-- Floating Cart Pill Button (Bottom-Right when items > 0) -->
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
        class="fixed bottom-6 left-6 z-40 flex items-center gap-2 rounded-full bg-slate-900 text-white px-4 py-3 shadow-2xl hover:bg-slate-800 transition cursor-pointer border border-white/20 active:scale-95"
      >
        <ShoppingBag class="w-4 h-4" />
        <span class="text-xs font-bold">{{ totalCartItemsCount }} {{ t('in Bag') }}</span>
        <span class="text-xs font-bold">· ${{ cartTotalUsd.toFixed(2) }}</span>
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
  Heart,
  Plus,
  Trash2,
  CheckCircle2
} from 'lucide-vue-next'
import { useI18n } from '../i18n'

const { t } = useI18n()

// Filters
const searchQuery = ref('')
const selectedCategory = ref('All')
const inStockOnly = ref(false)
const sortBy = ref('featured')

// Cart with LocalStorage persistence
const savedCart = typeof localStorage !== 'undefined' ? localStorage.getItem('aerobyte_store_cart') : null
let initialCart = []
try {
  if (savedCart) initialCart = JSON.parse(savedCart)
} catch {
  initialCart = []
}
const isCartOpen = ref(false)
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
  sortBy.value = 'featured'
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

  if (sortBy.value === 'price-low') {
    list.sort((a, b) => a.priceUsd - b.priceUsd)
  } else if (sortBy.value === 'price-high') {
    list.sort((a, b) => b.priceUsd - a.priceUsd)
  } else if (sortBy.value === 'rating') {
    list.sort((a, b) => b.rating - a.rating)
  }

  return list
})

// Favorites Management
function toggleFavorite(productId) {
  if (favorites.value.has(productId)) {
    favorites.value.delete(productId)
    showToast('Removed from wishlist')
  } else {
    favorites.value.add(productId)
    showToast('Saved to your wishlist')
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

function submitOrder() {
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
</style>
