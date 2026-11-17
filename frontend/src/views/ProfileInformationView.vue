<!-- AeroByte Academy - User Profile & Account Management with Terms of Use & Privacy Policy views -->
<template>
  <div class="bg-slate-50 dark:bg-slate-950 min-h-screen transition-colors">
    <section class="border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 transition-colors">
      <div class="mx-auto max-w-7xl px-3 py-6 sm:px-6 sm:py-8 lg:px-8">
        <nav aria-label="Breadcrumb" class="text-xs font-medium text-slate-500 dark:text-slate-400">
          <RouterLink to="/courses" class="transition hover:text-navy-900 dark:hover:text-white">Home</RouterLink>
          <span class="mx-2 text-slate-300 dark:text-slate-600" aria-hidden="true">/</span>
          <span class="text-navy-900 dark:text-white font-semibold">{{ activeSectionTitle }}</span>
        </nav>
        <div class="mt-5 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p class="text-xs font-bold uppercase tracking-[0.16em] text-navy-600 dark:text-indigo-400">{{ t('Your account') }}</p>
            <h1 class="mt-2 text-3xl font-extrabold tracking-tight text-navy-900 dark:text-white sm:text-4xl">
              {{ activeSectionTitle }}
            </h1>
            <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-500 dark:text-slate-400">
              {{ activeSectionDescription }}
            </p>
          </div>
          <span
            class="inline-flex w-fit items-center gap-2 rounded-full border border-emerald-100 dark:border-emerald-800/80 bg-emerald-50 dark:bg-emerald-950/50 px-3 py-1.5 text-xs font-semibold text-emerald-700 dark:text-emerald-300"
          >
            <ShieldCheck class="h-4 w-4" aria-hidden="true" />
            {{ t('Your information stays private') }}
          </span>
        </div>
      </div>
    </section>

    <div class="mx-auto grid max-w-7xl gap-6 px-3 py-5 sm:px-6 sm:py-8 lg:grid-cols-[280px_minmax(0,1fr)] lg:px-8">
      <aside class="space-y-5">
        <section class="overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs">
          <div class="h-20 bg-gradient-to-r from-navy-900 via-navy-800 to-[#315d89]"></div>
          <div class="-mt-9 px-5 pb-5">
            <div class="relative group/avatar w-fit">
              <div
                class="flex h-[76px] w-[76px] items-center justify-center rounded-2xl border-4 border-white dark:border-slate-900 bg-navy-50 dark:bg-slate-800 text-xl font-extrabold text-navy-800 dark:text-white shadow-md overflow-hidden relative cursor-pointer"
                aria-label="Profile avatar"
                :title="t('Change profile photo')"
                @click="triggerAvatarUpload"
              >
                <img
                  v-if="profile.avatarUrl && !avatarLoadFailed"
                  :src="resolveImageUrl(profile.avatarUrl)"
                  :alt="profile.fullName"
                  class="h-full w-full object-cover"
                  @error="onAvatarError"
                />
                <span v-else>{{ initials }}</span>
                <div v-if="avatarUploading" class="absolute inset-0 bg-black/50 flex items-center justify-center">
                  <RefreshCw class="w-5 h-5 text-white animate-spin" />
                </div>
              </div>
            </div>
            <h2 class="mt-3 text-base font-bold text-navy-900 dark:text-white">{{ profile.fullName || 'Your name' }}</h2>
            <p class="mt-1 break-all text-xs text-slate-500 dark:text-slate-400">
              {{ profile.email || 'Add your email address' }}
            </p>
            <div class="mt-5 border-t border-slate-100 dark:border-slate-800 pt-4">
              <div class="flex items-center justify-between text-xs">
                <span class="font-semibold text-slate-600 dark:text-slate-300">{{ t('Profile completeness') }}</span>
                <span class="font-bold text-navy-900 dark:text-white">{{ completion }}%</span>
              </div>
              <div
                class="mt-2 h-2 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800"
                role="progressbar"
                :aria-valuenow="completion"
                aria-valuemin="0"
                aria-valuemax="100"
                aria-label="Profile completeness"
              >
                <div
                  class="h-full rounded-full bg-accent-green transition-all duration-300"
                  :style="{ width: `${completion}%` }"
                ></div>
              </div>
              <p class="mt-2 text-xs leading-5 text-slate-500 dark:text-slate-400">
                {{ t('A complete profile helps our team support your learning journey.') }}
              </p>
            </div>
          </div>
        </section>

        <nav class="overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-2 shadow-xs" :aria-label="t('Account navigation')">
          <button
            v-for="item in accountSections"
            :key="item.id"
            type="button"
            class="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-semibold transition cursor-pointer"
            :class="activeSection === item.id
              ? 'bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-white font-bold'
              : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/60 hover:text-navy-900 dark:hover:text-white'"
            :aria-current="activeSection === item.id ? 'page' : undefined"
            @click="selectSection(item.id)"
          >
            <component :is="item.icon" class="h-4 w-4 shrink-0" aria-hidden="true" />
            {{ t(item.label) }}
            <span
              v-if="item.id === 'history' && courseHistory.length"
              class="ml-auto rounded-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 px-2 py-0.5 text-[11px] text-slate-500 dark:text-slate-400"
            >
              {{ courseHistory.length }}
            </span>
            <span
              v-if="item.id === 'orders' && storeOrders.length"
              class="ml-auto rounded-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 px-2 py-0.5 text-[11px] text-slate-500 dark:text-slate-400"
            >
              {{ storeOrders.length }}
            </span>
          </button>
          <div class="my-2 border-t border-slate-100 dark:border-slate-800"></div>
          <button
            type="button"
            class="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-semibold text-red-600 dark:text-red-400 transition hover:bg-red-50 dark:hover:bg-red-950/40 cursor-pointer"
            @click="logoutDialogOpen = true"
          >
            <LogOut class="h-4 w-4" aria-hidden="true" />
            {{ t('Log out') }}
          </button>
        </nav>

        <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-xs">
          <div class="flex items-start gap-3">
            <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
              <GraduationCap class="h-5 w-5" aria-hidden="true" />
            </span>
            <div>
              <h2 class="text-base font-extrabold leading-snug text-navy-900 dark:text-white">
                {{ t('Ready for your next step?') }}
              </h2>
              <p class="mt-1 text-xs leading-5 text-slate-500 dark:text-slate-400">
                {{ t('Explore hands-on courses designed for curious minds.') }}
              </p>
              <RouterLink
                to="/courses"
                class="mt-3 inline-flex items-center gap-1.5 text-xs font-bold text-navy-800 dark:text-indigo-400 transition hover:text-accent-orange"
              >
                {{ t('Browse courses') }}
                <ArrowRight class="h-3.5 w-3.5" aria-hidden="true" />
              </RouterLink>
            </div>
          </div>
        </section>
      </aside>

      <div class="min-w-0">
        <!-- Hidden file input for avatar upload -->
        <input
          ref="avatarFileInput"
          type="file"
          accept="image/png,image/jpeg,image/webp,image/gif"
          class="hidden"
          aria-hidden="true"
          @change="handleAvatarChange"
        />
        <div
          v-if="notice"
          class="mb-5 flex items-start gap-2 rounded-xl border px-4 py-3 text-sm"
          :class="noticeType === 'error'
            ? 'border-red-200 dark:border-red-900/50 bg-red-50 dark:bg-red-950/40 text-red-700 dark:text-red-300'
            : 'border-emerald-200 dark:border-emerald-900/50 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300'"
          role="status"
        >
          <Check v-if="noticeType === 'success'" class="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
          <span>{{ notice }}</span>
        </div>

        <section v-if="activeSection === 'history'" class="space-y-5">
          <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 class="text-xl font-extrabold text-navy-900 dark:text-white">{{ t('Course history') }}</h2>
              <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">{{ t('Review your registrations and payment status.') }}</p>
            </div>
            <button
              v-if="courseHistory.length"
              type="button"
              class="inline-flex w-fit items-center gap-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs font-semibold text-slate-700 dark:text-slate-300 transition hover:bg-slate-50 dark:hover:bg-slate-700 cursor-pointer"
              :disabled="historyLoading"
              @click="loadCourseHistory"
            >
              <RefreshCw class="h-3.5 w-3.5" :class="{ 'animate-spin': historyLoading }" aria-hidden="true" />
              {{ t('Refresh history') }}
            </button>
          </div>

          <div
            v-if="historyError"
            class="rounded-xl border border-amber-200 dark:border-amber-900/50 bg-amber-50 dark:bg-amber-950/40 px-4 py-3 text-sm text-amber-800 dark:text-amber-300"
            role="status"
          >
            {{ historyError }}
          </div>

          <div
            v-if="!historyLoading && !courseHistory.length"
            class="rounded-2xl border border-dashed border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-6 py-12 text-center"
          >
            <span class="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
              <BookOpen class="h-6 w-6" aria-hidden="true" />
            </span>
            <h3 class="mt-4 text-base font-bold text-navy-900 dark:text-white">{{ t('No course history yet') }}</h3>
            <p class="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500 dark:text-slate-400">
              {{ t('Courses you register for will appear here.') }}
            </p>
            <RouterLink
              to="/courses"
              class="mt-5 inline-flex items-center gap-2 rounded-lg bg-navy-900 dark:bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-navy-800 dark:hover:bg-indigo-700"
            >
              {{ t('Browse courses') }}
              <ArrowRight class="h-4 w-4" aria-hidden="true" />
            </RouterLink>
          </div>

          <div v-else class="space-y-4">
            <article
              v-for="enrollment in courseHistory"
              :key="enrollment.enrollment_id"
              class="overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs"
            >
              <div class="flex flex-col gap-4 p-4 sm:flex-row sm:items-center sm:p-5">
                <img
                  :src="resolveImageUrl(enrollment.course_image)"
                  :alt="enrollment.course_title"
                  class="h-28 w-full rounded-xl bg-slate-100 dark:bg-slate-800 object-cover sm:h-20 sm:w-28"
                />
                <div class="min-w-0 flex-1">
                  <div class="flex flex-wrap items-center gap-2">
                    <span
                      class="rounded-full px-2.5 py-1 text-[11px] font-bold capitalize"
                      :class="statusClasses(enrollment.status)"
                    >
                      {{ t(enrollment.status) }}
                    </span>
                    <span class="text-xs text-slate-400 dark:text-slate-500">{{ formatCambodiaTime(enrollment.created_at) }}</span>
                  </div>
                  <h3 class="mt-2 text-base font-bold text-navy-900 dark:text-white">{{ enrollment.course_title }}</h3>
                  <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">
                    {{ t('Enrollment reference') }}: {{ enrollment.enrollment_id }}
                  </p>
                </div>
                <div class="flex items-center justify-between gap-4 border-t border-slate-100 dark:border-slate-800 pt-3 sm:flex-col sm:items-end sm:border-0 sm:pt-0">
                  <span class="text-base font-extrabold text-navy-900 dark:text-white">
                    ${{ enrollment.amount_due.toFixed(2) }}
                  </span>
                  <RouterLink
                    v-if="enrollment.status === 'pending'"
                    :to="{ name: 'ScanToPay', params: { enrollmentId: enrollment.enrollment_id } }"
                    class="text-xs font-bold text-navy-800 dark:text-indigo-400 hover:underline"
                  >
                    {{ t('Continue payment') }}
                  </RouterLink>
                  <RouterLink
                    v-else-if="enrollment.status === 'paid' || enrollment.status === 'confirmed'"
                    :to="{ name: 'PaymentSuccessful', params: { enrollmentId: enrollment.enrollment_id } }"
                    class="text-xs font-bold text-navy-800 dark:text-indigo-400 hover:underline"
                  >
                    {{ t('View receipt') }}
                  </RouterLink>
                  <RouterLink
                    v-else
                    :to="{ name: 'PaymentExpired', params: { enrollmentId: enrollment.enrollment_id } }"
                    class="text-xs font-bold text-navy-800 dark:text-indigo-400 hover:underline"
                  >
                    {{ t('View details') }}
                  </RouterLink>
                </div>
              </div>
            </article>
          </div>
        </section>

        <!-- MY ORDERS SECTION -->
        <section v-else-if="activeSection === 'orders'" class="space-y-5">
          <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 class="text-xl font-extrabold text-navy-900 dark:text-white">{{ t('My orders') }}</h2>
              <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">{{ t('Review your store purchases and hardware orders.') }}</p>
            </div>
            <div class="flex items-center gap-2">
              <RouterLink
                to="/store"
                class="inline-flex w-fit items-center gap-1.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs font-semibold text-slate-700 dark:text-slate-300 transition hover:bg-slate-50 dark:hover:bg-slate-700 cursor-pointer"
              >
                <ShoppingBag class="h-3.5 w-3.5 text-slate-500" />
                {{ t('Visit Aero Store') }}
              </RouterLink>
              <button
                v-if="storeOrders.length"
                type="button"
                class="inline-flex w-fit items-center gap-1.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs font-semibold text-slate-700 dark:text-slate-300 transition hover:bg-slate-50 dark:hover:bg-slate-700 cursor-pointer"
                :disabled="ordersLoading"
                @click="loadStoreOrders"
              >
                <RefreshCw class="h-3.5 w-3.5" :class="{ 'animate-spin': ordersLoading }" aria-hidden="true" />
                {{ t('Refresh') }}
              </button>
            </div>
          </div>

          <!-- Empty Orders State -->
          <div
            v-if="!ordersLoading && !storeOrders.length"
            class="rounded-2xl border border-dashed border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-6 py-12 text-center"
          >
            <span class="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
              <ShoppingBag class="h-6 w-6" aria-hidden="true" />
            </span>
            <h3 class="mt-4 text-base font-bold text-navy-900 dark:text-white">{{ t('No store orders yet') }}</h3>
            <p class="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500 dark:text-slate-400">
              {{ t('Hardware kits, drone components, and 3D printing supplies you order will appear here.') }}
            </p>
            <RouterLink
              to="/store"
              class="mt-5 inline-flex items-center gap-2 rounded-lg bg-navy-900 dark:bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-navy-800 dark:hover:bg-indigo-700"
            >
              {{ t('Visit Aero Store') }}
              <ArrowRight class="h-4 w-4" aria-hidden="true" />
            </RouterLink>
          </div>

          <!-- Orders List -->
          <div v-else class="space-y-4">
            <article
              v-for="order in storeOrders"
              :key="order.id"
              class="overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs"
            >
              <div class="border-b border-slate-100 dark:border-slate-800 px-5 py-3.5 flex flex-wrap items-center justify-between gap-3 bg-slate-50/50 dark:bg-slate-800/40">
                <div class="flex items-center gap-3">
                  <span class="font-mono text-xs font-bold text-navy-900 dark:text-white">
                    #{{ order.id }}
                  </span>
                  <span class="text-xs text-slate-400">·</span>
                  <span class="text-xs text-slate-500 dark:text-slate-400">
                    {{ formatCambodiaTime(order.date) }}
                  </span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/60">
                    <span class="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                    {{ order.status || 'Confirmed' }}
                  </span>
                </div>
              </div>

              <div class="p-5 space-y-4">
                <!-- Order items -->
                <div class="divide-y divide-slate-100 dark:divide-slate-800">
                  <div
                    v-for="item in order.items"
                    :key="item.id"
                    class="py-3 flex items-center justify-between gap-3 first:pt-0 last:pb-0"
                  >
                    <div class="flex items-center gap-3">
                      <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-slate-100 dark:bg-slate-800 text-lg border border-slate-200/50 dark:border-slate-700/50">
                        {{ item.icon }}
                      </div>
                      <div>
                        <h4 class="text-xs sm:text-sm font-bold text-slate-900 dark:text-white line-clamp-1">
                          {{ item.name }}
                        </h4>
                        <p class="text-[11px] text-slate-400">
                          Qty: {{ item.quantity }} × ${{ Number(item.priceUsd).toFixed(2) }}
                        </p>
                      </div>
                    </div>
                    <span class="text-xs sm:text-sm font-extrabold text-slate-900 dark:text-white">
                      ${{ (item.priceUsd * item.quantity).toFixed(2) }}
                    </span>
                  </div>
                </div>

                <!-- Footer Summary -->
                <div class="border-t border-slate-100 dark:border-slate-800 pt-3 flex flex-wrap items-center justify-between gap-3 text-xs">
                  <div class="text-slate-500 dark:text-slate-400">
                    <span class="font-semibold">{{ t('Fulfillment') }}:</span>
                    {{ order.fulfillment === 'pickup' ? t('Same-Day Lab Pickup (Phnom Penh)') : t('Express Delivery') }}
                  </div>
                  <div class="flex items-baseline gap-2">
                    <span class="text-slate-500 dark:text-slate-400 font-semibold">{{ t('Order Total') }}:</span>
                    <span class="text-base font-black text-navy-900 dark:text-white">${{ Number(order.total || 0).toFixed(2) }}</span>
                    <span class="text-[11px] text-slate-400">({{ Math.round((order.total || 0) * 4100).toLocaleString() }} ៛)</span>
                  </div>
                </div>
              </div>
            </article>
          </div>
        </section>

        <section v-else-if="activeSection === 'settings'" class="space-y-5">
          <div>
            <h2 class="text-xl font-extrabold text-navy-900 dark:text-slate-100">{{ t('Settings') }}</h2>
            <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">{{ t('Manage your language and local profile preferences.') }}</p>
          </div>

          <!-- Theme Mode Switch Card -->
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs transition-colors">
            <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800/80 px-5 py-5 sm:px-7">
              <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 dark:bg-slate-800 text-amber-500 dark:text-amber-400">
                <Sun v-if="!isDark" class="h-5 w-5" aria-hidden="true" />
                <Moon v-else class="h-5 w-5 text-indigo-400" aria-hidden="true" />
              </span>
              <div>
                <h3 class="text-sm font-bold text-navy-900 dark:text-slate-100">{{ t('Theme mode') }}</h3>
                <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">{{ t('Choose between light and dark mode for your experience.') }}</p>
              </div>
            </div>
            <div class="flex items-center justify-between px-5 py-5 sm:px-7">
              <div>
                <span class="text-sm font-semibold text-slate-800 dark:text-slate-200 block">{{ isDark ? t('Dark mode') : t('Light mode') }}</span>
                <span class="text-xs text-slate-400 dark:text-slate-500 block mt-0.5">
                  {{ isDark ? t('Dark theme is currently active') : t('Light theme is currently active') }}
                </span>
              </div>

              <!-- Only Toggle Switch Control -->
              <button
                type="button"
                role="switch"
                :aria-checked="isDark"
                :aria-label="isDark ? t('Switch to light mode') : t('Switch to dark mode')"
                @click="toggleTheme"
                class="relative inline-flex h-8 w-14 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-300 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-navy-800 dark:focus-visible:ring-indigo-400 shadow-inner"
                :class="isDark ? 'bg-indigo-600' : 'bg-slate-300 dark:bg-slate-700'"
              >
                <span class="sr-only">{{ t('Theme mode') }}</span>
                <span
                  aria-hidden="true"
                  class="pointer-events-none inline-flex h-7 w-7 transform items-center justify-center rounded-full bg-white shadow-md ring-0 transition duration-300 ease-in-out"
                  :class="isDark ? 'translate-x-6' : 'translate-x-0'"
                >
                  <Moon v-if="isDark" class="h-4 w-4 text-indigo-600" />
                  <Sun v-else class="h-4 w-4 text-amber-500" />
                </span>
              </button>
            </div>
          </section>

          <!-- Language Setting Card -->
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs transition-colors">
            <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800/80 px-5 py-5 sm:px-7">
              <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
                <Globe2 class="h-5 w-5" aria-hidden="true" />
              </span>
              <div>
                <h3 class="text-sm font-bold text-navy-900 dark:text-slate-100">{{ t('Language') }}</h3>
                <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">{{ t('Choose the language used across the site.') }}</p>
              </div>
            </div>
            <div class="flex flex-col gap-3 px-5 py-5 sm:flex-row sm:items-center sm:justify-between sm:px-7">
              <span class="text-sm font-medium text-slate-700 dark:text-slate-200">{{ t('Display language') }}</span>
              <div ref="languageDropdownRef" class="relative sm:w-56">
                <button
                  type="button"
                  @click="languageDropdownOpen = !languageDropdownOpen"
                  class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 text-xs bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 flex items-center justify-between text-left focus:outline-none focus:ring-2 focus:ring-navy-800 transition cursor-pointer"
                  :class="languageDropdownOpen ? 'border-navy-800 ring-2 ring-navy-800/20' : 'hover:border-slate-300 dark:hover:border-slate-600'"
                >
                  <span class="font-medium">
                    {{ locale === 'kh' ? 'KH - ភាសាខ្មែរ' : 'EN - English' }}
                  </span>
                  <ChevronDown class="w-4 h-4 text-slate-400 transition-transform duration-200 shrink-0" :class="{ 'rotate-180 text-navy-800': languageDropdownOpen }" />
                </button>

                <div
                  v-if="languageDropdownOpen"
                  class="absolute left-0 right-0 top-full z-30 mt-1.5 overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-1.5 shadow-xl space-y-1"
                >
                  <button
                    type="button"
                    @click="setLocale('en'); languageDropdownOpen = false"
                    class="flex w-full items-center justify-between rounded-xl px-3 py-2 text-xs transition cursor-pointer"
                    :class="locale === 'en'
                      ? 'bg-navy-50 dark:bg-slate-700 text-navy-900 dark:text-white font-bold'
                      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/60 font-medium'"
                  >
                    <span>EN - {{ t('English') }}</span>
                    <Check v-if="locale === 'en'" class="w-4 h-4 text-navy-900 dark:text-white shrink-0" />
                  </button>
                  <button
                    type="button"
                    @click="setLocale('kh'); languageDropdownOpen = false"
                    class="flex w-full items-center justify-between rounded-xl px-3 py-2 text-xs transition cursor-pointer"
                    :class="locale === 'kh'
                      ? 'bg-navy-50 dark:bg-slate-700 text-navy-900 dark:text-white font-bold'
                      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/60 font-medium'"
                  >
                    <span>KH - {{ t('Khmer') }}</span>
                    <Check v-if="locale === 'kh'" class="w-4 h-4 text-navy-900 dark:text-white shrink-0" />
                  </button>
                </div>
              </div>
            </div>
          </section>

          <!-- Terms & Policies Card in Settings -->
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs transition-colors">
            <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800/80 px-5 py-5 sm:px-7">
              <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
                <Scale class="h-5 w-5" aria-hidden="true" />
              </span>
              <div>
                <h3 class="text-sm font-bold text-navy-900 dark:text-slate-100">{{ t('Terms & Policies') }}</h3>
                <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">{{ t('Review the agreements that govern your account and data privacy.') }}</p>
              </div>
            </div>
            <div class="grid gap-3 p-5 sm:grid-cols-2 sm:p-7">
              <button
                type="button"
                @click="selectSection('terms')"
                class="flex items-center justify-between rounded-xl border border-slate-200 dark:border-slate-700/80 bg-slate-50/50 dark:bg-slate-800/40 p-4 text-left transition hover:border-navy-800 dark:hover:border-indigo-500 hover:bg-white dark:hover:bg-slate-800 cursor-pointer"
              >
                <div class="flex items-center gap-3">
                  <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-indigo-400">
                    <Scale class="h-4 w-4" />
                  </span>
                  <div>
                    <span class="text-xs font-bold text-navy-900 dark:text-white block">{{ t('Terms of use') }}</span>
                    <span class="text-[11px] text-slate-400 dark:text-slate-500 block mt-0.5">{{ t('Student agreements & lab safety') }}</span>
                  </div>
                </div>
                <ArrowRight class="h-4 w-4 text-slate-400 shrink-0" />
              </button>
              <button
                type="button"
                @click="selectSection('privacy')"
                class="flex items-center justify-between rounded-xl border border-slate-200 dark:border-slate-700/80 bg-slate-50/50 dark:bg-slate-800/40 p-4 text-left transition hover:border-navy-800 dark:hover:border-indigo-500 hover:bg-white dark:hover:bg-slate-800 cursor-pointer"
              >
                <div class="flex items-center gap-3">
                  <span class="flex h-8 w-8 items-center justify-center rounded-lg bg-emerald-50 dark:bg-emerald-950/40 text-emerald-600 dark:text-emerald-400">
                    <ShieldCheck class="h-4 w-4" />
                  </span>
                  <div>
                    <span class="text-xs font-bold text-navy-900 dark:text-white block">{{ t('Privacy Policy') }}</span>
                    <span class="text-[11px] text-slate-400 dark:text-slate-500 block mt-0.5">{{ t('How we handle and secure your data') }}</span>
                  </div>
                </div>
                <ArrowRight class="h-4 w-4 text-slate-400 shrink-0" />
              </button>
            </div>
          </section>

          <section class="rounded-2xl border border-red-200 dark:border-red-900/50 bg-white dark:bg-slate-900 p-5 sm:p-7">
            <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h3 class="text-sm font-bold text-slate-900 dark:text-white">{{ t('Local profile data') }}</h3>
                <p class="mt-1 max-w-xl text-xs leading-5 text-slate-500 dark:text-slate-400">
                  {{ t('Your profile and history are stored in this browser for this demo.') }}
                </p>
              </div>
              <button
                type="button"
                class="inline-flex w-fit items-center gap-2 rounded-lg border border-red-200 dark:border-red-900/50 px-3.5 py-2 text-xs font-semibold text-red-600 dark:text-red-400 transition hover:bg-red-50 dark:hover:bg-red-950/40 cursor-pointer"
                @click="clearLocalProfile"
              >
                <Trash2 class="h-3.5 w-3.5" aria-hidden="true" />
                {{ t('Clear profile') }}
              </button>
            </div>
          </section>
        </section>

        <!-- TERMS OF USE SECTION (FULL CONTENT MATCHING /terms) -->
        <section v-else-if="activeSection === 'terms'" class="space-y-6">
          <!-- Section 1: Overview & Acceptance -->
            <article id="profile-terms-acceptance" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
              <div class="flex items-center gap-3 mb-4">
                <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                  <FileText class="h-5 w-5" />
                </span>
                <h3 class="text-lg font-bold text-navy-900 dark:text-white">1. {{ t('Acceptance of Terms') }}</h3>
              </div>
              <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                <p>
                  Welcome to AeroByte Academy. By creating an account, browsing our course catalog, registering for classes, or using our physical robotics maker labs in Phnom Penh, you agree to comply with and be bound by these Terms of Use.
                </p>
                <p>
                  If you do not agree with any part of these terms, you must discontinue the use of our services and website immediately.
                </p>
              </div>
            </article>

            <!-- Section 2: Account Responsibilities -->
            <article id="profile-terms-accounts" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
              <div class="flex items-center gap-3 mb-4">
                <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                  <ShieldCheck class="h-5 w-5" />
                </span>
                <h3 class="text-lg font-bold text-navy-900 dark:text-white">2. {{ t('Account Registration & Security') }}</h3>
              </div>
              <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                <p>
                  When creating an account or enrolling in a course, you agree to:
                </p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-600 dark:text-slate-300">
                  <li>Provide accurate, current, and complete personal and contact information.</li>
                  <li>Maintain the confidentiality of your login credentials and password.</li>
                  <li>Promptly notify AeroByte Academy of any unauthorized access or security breach.</li>
                  <li>Ensure that course certificates and student credentials accurately represent the individual who completed the learning program.</li>
                </ul>
              </div>
            </article>

            <!-- Section 3: Course Enrollment & Lab Guidelines -->
            <article id="profile-terms-lab-safety" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
              <div class="flex items-center gap-3 mb-4">
                <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-amber-50 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300">
                  <AlertCircle class="h-5 w-5" />
                </span>
                <h3 class="text-lg font-bold text-navy-900 dark:text-white">3. {{ t('Lab Safety Guidelines & Equipment Use') }}</h3>
              </div>
              <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                <p>
                  Hands-on engineering involves working directly with electrical circuits, microcontrollers, motors, actuators, and soldering stations. All enrolled students agree to:
                </p>
                <div class="rounded-xl border border-amber-200 bg-amber-50/50 p-4 space-y-2 dark:border-amber-900/60 dark:bg-amber-950/30">
                  <p class="font-bold text-amber-900 dark:text-amber-200 text-xs sm:text-sm flex items-center gap-2">
                    <AlertCircle class="h-4 w-4 shrink-0 text-amber-600 dark:text-amber-400" />
                    {{ t('Maker Lab Protocol') }}
                  </p>
                  <ul class="list-disc pl-5 space-y-1 text-xs text-amber-950 dark:text-amber-300">
                    <li>Follow instructor safety briefings before operating soldering equipment or high-current power supplies.</li>
                    <li>Wear protective eyewear when soldering or using mechanical 3D fabrication tools.</li>
                    <li>Handle electronic hardware kits (ESP32, Arduino, sensors, and custom PCBs) with due care to prevent electrostatic discharge (ESD) damage.</li>
                  </ul>
                </div>
                <p>
                  AeroByte Academy reserves the right to suspend or remove any student from lab sessions if safety guidelines are willfully disregarded.
                </p>
              </div>
            </article>

            <!-- Section 4: Fees, Payments & QR Checkout -->
            <article id="profile-terms-payments" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
              <div class="flex items-center gap-3 mb-4">
                <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                  <CheckCircle2 class="h-5 w-5" />
                </span>
                <h3 class="text-lg font-bold text-navy-900 dark:text-white">4. {{ t('Tuition, Fees & Payment') }}</h3>
              </div>
              <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                <p>
                  Course registration is officially confirmed only upon receipt of verified payment:
                </p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-600 dark:text-slate-300">
                  <li><strong>Transparent Pricing:</strong> Enrollment totals include the course tuition, itemized administration fee, physical certification fee, and student access card fee.</li>
                  <li><strong>KHQR & Bakong:</strong> Real-time payments are verified via standard Cambodian banking QR codes. Payment sessions remain open for 15 minutes before expiration.</li>
                  <li><strong>Promotional Coupons:</strong> Valid coupon codes must be applied before final payment checkout. Discounts cannot be retroactively claimed after payment completion.</li>
                </ul>
              </div>
            </article>

            <!-- Section 5: Refunds & Cancellations -->
            <article id="profile-terms-refunds" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
              <div class="flex items-center gap-3 mb-4">
                <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                  <Scale class="h-5 w-5" />
                </span>
                <h3 class="text-lg font-bold text-navy-900 dark:text-white">5. {{ t('Refund & Transfer Policy') }}</h3>
              </div>
              <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                <p>
                  We understand that schedules can shift. Our refund and transfer policy is structured as follows:
                </p>
                <div class="grid gap-3 sm:grid-cols-2">
                  <div class="rounded-xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-800/60">
                    <p class="font-bold text-navy-900 dark:text-white text-xs sm:text-sm">7+ Days Before Cohort Start</p>
                    <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">100% full tuition refund or complimentary batch transfer upon written request.</p>
                  </div>
                  <div class="rounded-xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-800/60">
                    <p class="font-bold text-navy-900 dark:text-white text-xs sm:text-sm">Within 7 Days of Start</p>
                    <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">Tuition credit applied toward any future cohort within 12 calendar months.</p>
                  </div>
                </div>
                <p class="text-xs text-slate-500 dark:text-slate-400">
                  Once a cohort has commenced and kit hardware has been distributed, course fees become non-refundable.
                </p>
              </div>
            </article>

            <!-- Section 6: Intellectual Property -->
            <article id="profile-terms-ip" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
              <div class="flex items-center gap-3 mb-4">
                <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                  <Sparkles class="h-5 w-5" />
                </span>
                <h3 class="text-lg font-bold text-navy-900 dark:text-white">6. {{ t('Intellectual Property') }}</h3>
              </div>
              <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                <p>
                  All course slide decks, proprietary schematics, firmware modules, and instructional curricula provided by AeroByte Academy are copyrighted and intended solely for your personal educational use.
                </p>
                <p>
                  <strong>Student Project Ownership:</strong> You retain 100% ownership of your original robot code, mechanical modifications, and unique prototypes developed during our project labs.
                </p>
              </div>
            </article>

            <!-- Contact Box -->
            <div class="rounded-2xl border border-navy-100 bg-gradient-to-r from-navy-900 to-[#1e3a5f] p-6 sm:p-8 text-white shadow-card dark:border-slate-800 dark:from-slate-900 dark:to-indigo-950">
              <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h3 class="text-lg font-bold">{{ t('Have questions regarding our terms?') }}</h3>
                  <p class="mt-1 text-xs sm:text-sm text-slate-300">
                    Our academic and admissions team is available to assist you.
                  </p>
                </div>
                <RouterLink
                  to="/contact"
                  class="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-5 py-2.5 text-xs font-bold text-navy-900 hover:bg-slate-100 dark:bg-indigo-600 dark:text-white dark:hover:bg-indigo-500 transition shrink-0"
                >
                  <Mail class="h-4 w-4" />
                  <span>{{ t('Contact Academy') }}</span>
                </RouterLink>
              </div>
            </div>
        </section>

        <!-- PRIVACY POLICY SECTION (FULL CONTENT MATCHING /privacy) -->
        <section v-else-if="activeSection === 'privacy'" class="space-y-6">
          <!-- Section 1: Overview -->
            <article id="profile-privacy-overview" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
              <div class="flex items-center gap-3 mb-4">
                <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
                  <ShieldCheck class="h-5 w-5" />
                </span>
                <h3 class="text-lg font-bold text-navy-900 dark:text-white">1. {{ t('Overview & Commitment') }}</h3>
              </div>
              <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                <p>
                  At AeroByte Academy, we take your trust and privacy seriously. This Privacy Policy details how we collect, use, and protect your information when you enroll in our courses, register an account, or interact with our learning platform.
                </p>
                <p>
                  Our core principle is simple: we collect only the information necessary to provide an exceptional educational experience and issue authentic certifications.
                </p>
              </div>
            </article>

            <!-- Section 2: Information We Collect -->
            <article id="profile-privacy-collection" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
              <div class="flex items-center gap-3 mb-4">
                <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                  <FileText class="h-5 w-5" />
                </span>
                <h3 class="text-lg font-bold text-navy-900 dark:text-white">2. {{ t('Information We Collect') }}</h3>
              </div>
              <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                <p>We collect information you directly provide when registering and enrolling:</p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-600 dark:text-slate-300">
                  <li><strong>Identity & Contact:</strong> Full name (used for official certificates), email address, phone number, and Telegram username (used for cohort announcements and lab coordination).</li>
                  <li><strong>Academic & Experience Background:</strong> Age group, highest academic qualification, and coding experience (used by mentors to tailor lab exercises).</li>
                  <li><strong>Payment Transaction Data:</strong> KHQR transaction references, payment timestamps, and receipt numbers. <em>We never store credit card numbers or banking account passwords.</em></li>
                </ul>
              </div>
            </article>

            <!-- Section 3: How We Use Data -->
            <article id="profile-privacy-usage" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
              <div class="flex items-center gap-3 mb-4">
                <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                  <CheckCircle2 class="h-5 w-5" />
                </span>
                <h3 class="text-lg font-bold text-navy-900 dark:text-white">3. {{ t('How We Use Your Information') }}</h3>
              </div>
              <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                <p>Your data is used strictly for academic and operational purposes:</p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-600 dark:text-slate-300">
                  <li>Processing course registrations and assigning students to cohort lab batches.</li>
                  <li>Sending essential transactional messages: payment receipts, lab kit pickup schedules, and password reset codes.</li>
                  <li>Issuing digital and physical AeroByte Academy course completion certificates.</li>
                  <li>Providing responsive technical and student support through email and Telegram.</li>
                </ul>
              </div>
            </article>

            <!-- Section 4: Data Security -->
            <article id="profile-privacy-security" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
              <div class="flex items-center gap-3 mb-4">
                <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
                  <Lock class="h-5 w-5" />
                </span>
                <h3 class="text-lg font-bold text-navy-900 dark:text-white">4. {{ t('Data Protection & Storage') }}</h3>
              </div>
              <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                <p>
                  We employ standard industry security protocols to protect your personal information against unauthorized disclosure, alteration, or destruction:
                </p>
                <div class="rounded-xl border border-emerald-200 bg-emerald-50/50 p-4 space-y-2 dark:border-emerald-900/60 dark:bg-emerald-950/30">
                  <p class="font-bold text-emerald-950 dark:text-emerald-200 text-xs sm:text-sm flex items-center gap-2">
                    <ShieldCheck class="h-4 w-4 shrink-0 text-emerald-600 dark:text-emerald-400" />
                    {{ t('Our Security Standards') }}
                  </p>
                  <ul class="list-disc pl-5 space-y-1 text-xs text-emerald-950 dark:text-emerald-300">
                    <li>Encrypted HTTPS/TLS transmission for all web sessions and form submissions.</li>
                    <li>Hashed and salted password storage with industry-standard cryptographic algorithms.</li>
                    <li>Strict access controls limiting student record access to authorized instructors and academy administrators.</li>
                  </ul>
                </div>
              </div>
            </article>

            <!-- Section 5: Third-Party Integrations -->
            <article id="profile-privacy-third-party" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
              <div class="flex items-center gap-3 mb-4">
                <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                  <Scale class="h-5 w-5" />
                </span>
                <h3 class="text-lg font-bold text-navy-900 dark:text-white">5. {{ t('Third-Party Service Providers') }}</h3>
              </div>
              <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                <p>
                  To provide seamless modern services, we integrate with trusted infrastructure providers:
                </p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-600 dark:text-slate-300">
                  <li><strong>Transactional Email (Resend):</strong> Used solely to dispatch verified password reset security emails and account verification codes.</li>
                  <li><strong>Google Sign-In:</strong> For optional one-click single sign-on authentication.</li>
                  <li><strong>Bakong / National Banking Rails:</strong> For standardized KHQR payment processing.</li>
                </ul>
                <p class="text-xs text-slate-500 dark:text-slate-400">
                  We never share your information with third-party advertisers or telemarketing brokers.
                </p>
              </div>
            </article>

            <!-- Section 6: Your Rights & Profile Management -->
            <article id="profile-privacy-rights" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
              <div class="flex items-center gap-3 mb-4">
                <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                  <UserCheck class="h-5 w-5" />
                </span>
                <h3 class="text-lg font-bold text-navy-900 dark:text-white">6. {{ t('Your Data Rights & Control') }}</h3>
              </div>
              <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
                <p>
                  You have full control over your educational record and profile:
                </p>
                <ul class="list-disc pl-5 space-y-1.5 text-slate-600 dark:text-slate-300">
                  <li><strong>Access & Update:</strong> Modify your contact details, education level, and phone number anytime from your <button type="button" @click="selectSection('profile')" class="text-navy-800 dark:text-indigo-400 font-bold underline cursor-pointer">Profile Information</button> tab.</li>
                  <li><strong>Data Portability:</strong> Request an export of your enrollment records and certificate verifications.</li>
                  <li><strong>Account Deletion:</strong> Request full erasure of your account data by contacting our administrative desk.</li>
                </ul>
              </div>
            </article>

            <!-- Contact Box -->
            <div class="rounded-2xl border border-navy-100 bg-gradient-to-r from-navy-900 to-[#1e3a5f] p-6 sm:p-8 text-white shadow-card dark:border-slate-800 dark:from-slate-900 dark:to-indigo-950">
              <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
                <div>
                  <h3 class="text-lg font-bold">{{ t('Questions about your data privacy?') }}</h3>
                  <p class="mt-1 text-xs sm:text-sm text-slate-300">
                    Reach out to our privacy officer directly for data inquiries or account deletion requests.
                  </p>
                </div>
                <RouterLink
                  to="/contact"
                  class="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-5 py-2.5 text-xs font-bold text-navy-900 hover:bg-slate-100 dark:bg-indigo-600 dark:text-white dark:hover:bg-indigo-500 transition shrink-0"
                >
                  <Mail class="h-4 w-4" />
                  <span>{{ t('Contact Academy') }}</span>
                </RouterLink>
              </div>
            </div>
        </section>

        <form v-else-if="isEditing" class="space-y-5" @submit.prevent="saveProfile">
          <!-- Profile Photo Card in Editing Mode -->
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs overflow-hidden">
            <div class="flex flex-col sm:flex-row items-center sm:items-start gap-5 p-5 sm:p-6">
              <div class="relative group shrink-0">
                <div class="flex h-20 w-20 sm:h-24 sm:w-24 items-center justify-center rounded-2xl border-2 border-slate-200 dark:border-slate-700 bg-navy-50 dark:bg-slate-800 text-2xl font-black text-navy-800 dark:text-white shadow-xs overflow-hidden">
                  <img
                    v-if="(draft.avatarUrl || profile.avatarUrl) && !avatarLoadFailed"
                    :src="resolveImageUrl(draft.avatarUrl || profile.avatarUrl)"
                    :alt="draft.fullName || profile.fullName"
                    class="h-full w-full object-cover"
                    @error="onAvatarError"
                  />
                  <span v-else>{{ initials }}</span>
                </div>
                <button
                  type="button"
                  class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center text-white text-xs font-bold rounded-2xl cursor-pointer"
                  :title="t('Change profile photo')"
                  @click="triggerAvatarUpload"
                >
                  <Camera class="w-5 h-5 mb-1" />
                  <span>{{ t('Change') }}</span>
                </button>
              </div>

              <div class="space-y-1.5 text-center sm:text-left flex-1 min-w-0">
                <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2">
                  <h3 class="text-sm font-bold text-navy-900 dark:text-white">{{ t('Profile photo') }}</h3>
                  <span v-if="(draft.avatarUrl || profile.avatarUrl) && !avatarLoadFailed" class="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/50 px-2 py-0.5 rounded-full border border-emerald-200 dark:border-emerald-800/60">
                    Active
                  </span>
                </div>
                <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed max-w-lg">
                  {{ t('Upload a photo or avatar image. Recommended size: at least 256x256 px (JPG, PNG, or WebP).') }}
                </p>
                <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2.5 pt-2">
                  <button
                    type="button"
                    class="inline-flex items-center gap-1.5 rounded-lg bg-navy-900 dark:bg-indigo-600 px-3.5 py-2 text-xs font-semibold text-white hover:bg-navy-800 dark:hover:bg-indigo-500 shadow-2xs transition cursor-pointer"
                    :disabled="avatarUploading"
                    @click="triggerAvatarUpload"
                  >
                    <RefreshCw v-if="avatarUploading" class="h-3.5 w-3.5 animate-spin" />
                    <Upload v-else class="h-3.5 w-3.5" />
                    <span>{{ avatarUploading ? 'Uploading...' : (((draft.avatarUrl || profile.avatarUrl) && !avatarLoadFailed) ? t('Change photo') : t('Upload photo')) }}</span>
                  </button>
                  <button
                    v-if="(draft.avatarUrl || profile.avatarUrl) && !avatarLoadFailed"
                    type="button"
                    class="inline-flex items-center gap-1.5 rounded-lg border border-red-200 dark:border-red-900/60 bg-red-50/60 dark:bg-red-950/40 px-3.5 py-2 text-xs font-semibold text-red-700 dark:text-red-400 hover:bg-red-100 dark:hover:bg-red-900/50 transition cursor-pointer"
                    @click="removeAvatar"
                  >
                    <Trash2 class="h-3.5 w-3.5" />
                    <span>{{ t('Remove photo') }}</span>
                  </button>
                </div>
              </div>
            </div>
          </section>
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs">
            <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 px-5 py-5 sm:px-7">
              <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
                <UserRound class="h-5 w-5" aria-hidden="true" />
              </span>
              <div>
                <h2 class="text-base font-bold text-navy-900 dark:text-white">{{ t('Personal details') }}</h2>
                <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-400">{{ t('Your contact and personal information.') }}</p>
              </div>
            </div>
            <div class="grid gap-x-5 gap-y-4 px-5 py-6 sm:grid-cols-2 sm:px-7">
              <label class="block">
                <span class="mb-1.5 block text-xs font-semibold text-slate-700 dark:text-slate-200">{{ t('Full name') }} <span class="text-red-500">*</span></span>
                <input
                  v-model.trim="draft.fullName"
                  autocomplete="name"
                  required
                  maxlength="120"
                  :placeholder="t('Enter full name')"
                  class="profile-input"
                />
              </label>
              <label class="block">
                <span class="mb-1.5 block text-xs font-semibold text-slate-700 dark:text-slate-200">{{ t('Email address') }} <span class="text-red-500">*</span></span>
                <input
                  v-model.trim="draft.email"
                  type="email"
                  autocomplete="email"
                  required
                  maxlength="254"
                  placeholder="you@example.com"
                  class="profile-input"
                />
              </label>
              <div>
                <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                  {{ t('Phone number') }}
                </label>
                <input
                  v-model="draft.phone"
                  type="tel"
                  inputmode="tel"
                  autocomplete="tel"
                  maxlength="20"
                  @keypress="onPhoneKeypress"
                  @input="onPhoneInput"
                  placeholder="+855 12 345 678"
                  class="profile-input"
                />
                <p class="mt-1 text-[10px] text-slate-400 dark:text-slate-500">
                  {{ t('Numbers and "+" sign only (e.g. +85512345678)') }}
                </p>
              </div>
              <label class="block">
                <span class="mb-1.5 block text-xs font-semibold text-slate-700 dark:text-slate-200">{{ t('Telegram username') }}</span>
                <input
                  v-model.trim="draft.telegram"
                  maxlength="64"
                  placeholder="@yourusername"
                  class="profile-input"
                />
              </label>
              <label class="block">
                <span class="mb-1.5 block text-xs font-semibold text-slate-700 dark:text-slate-200">{{ t('Date of birth') }}</span>
                <DatePicker
                  v-model="draft.dateOfBirth"
                  :placeholder="t('Select date of birth')"
                  :min-year="1950"
                  :max-year="new Date().getFullYear()"
                />
              </label>
              <label class="block">
                <span class="mb-1.5 block text-xs font-semibold text-slate-700 dark:text-slate-200">{{ t('City or province') }}</span>
                <input
                  v-model.trim="draft.location"
                  autocomplete="address-level2"
                  maxlength="100"
                  :placeholder="t('e.g. Phnom Penh')"
                  class="profile-input"
                />
              </label>
            </div>
          </section>

          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs">
            <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 px-5 py-5 sm:px-7">
              <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
                <GraduationCap class="h-5 w-5" aria-hidden="true" />
              </span>
              <div>
                <h2 class="text-base font-bold text-navy-900 dark:text-white">{{ t('Learning background') }}</h2>
                <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-400">{{ t('Your education and experience.') }}</p>
              </div>
            </div>
            <div class="grid gap-x-5 gap-y-4 px-5 py-6 sm:grid-cols-2 sm:px-7">
              <div ref="qualificationDropdownRef" class="relative">
                <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                  {{ t('Highest qualification') }}
                </label>
                <button
                  type="button"
                  @click="qualificationDropdownOpen = !qualificationDropdownOpen; experienceDropdownOpen = false"
                  class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 text-xs bg-white dark:bg-slate-800 text-slate-900 dark:text-white flex items-center justify-between text-left focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500 transition cursor-pointer"
                  :class="qualificationDropdownOpen ? 'border-navy-800 dark:border-indigo-500 ring-2 ring-navy-800/20' : 'hover:border-slate-300 dark:hover:border-slate-600'"
                >
                  <span :class="draft.qualification ? 'text-slate-800 dark:text-white font-medium' : 'text-slate-400 dark:text-slate-500'">
                    {{ t(draft.qualification) || t('Select your education level') }}
                  </span>
                  <ChevronDown class="w-4 h-4 text-slate-400 transition-transform duration-200 shrink-0" :class="{ 'rotate-180 text-navy-800 dark:text-indigo-400': qualificationDropdownOpen }" />
                </button>

                <div
                  v-if="qualificationDropdownOpen"
                  class="absolute left-0 right-0 top-full z-30 mt-1.5 overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-1.5 shadow-xl space-y-1"
                >
                  <button
                    v-for="option in qualificationOptions"
                    :key="option"
                    type="button"
                    @click="selectQualification(option)"
                    class="flex w-full items-center justify-between rounded-xl px-3 py-2 text-xs transition cursor-pointer"
                    :class="draft.qualification === option
                      ? 'bg-navy-50 dark:bg-slate-700 text-navy-900 dark:text-white font-bold'
                      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/60 hover:text-navy-900 dark:hover:text-white font-medium'"
                  >
                    <span>{{ t(option) }}</span>
                    <Check v-if="draft.qualification === option" class="w-4 h-4 text-navy-900 dark:text-white shrink-0" />
                  </button>
                </div>

                <input
                  v-if="draft.qualification === 'Other'"
                  v-model.trim="draft.qualificationOther"
                  required
                  maxlength="120"
                  :aria-label="t('Please specify your qualification')"
                  :placeholder="t('Please specify your qualification')"
                  class="profile-input mt-3"
                />
              </div>
              <label class="block">
                <span class="mb-1.5 block text-xs font-semibold text-slate-700 dark:text-slate-200">{{ t('Current occupation') }}</span>
                <input
                  v-model.trim="draft.occupation"
                  maxlength="120"
                  :placeholder="t('e.g. Student, Engineer')"
                  class="profile-input"
                  @keypress="(e) => { if (/[0-9\u17E0-\u17E9]/.test(e.key)) e.preventDefault() }"
                  @input="draft.occupation = draft.occupation.replace(/[0-9\u17E0-\u17E9]/g, '')"
                />
              </label>
              <div ref="experienceDropdownRef" class="relative sm:col-span-2">
                <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                  {{ t('Coding experience') }}
                </label>
                <button
                  type="button"
                  @click="experienceDropdownOpen = !experienceDropdownOpen; qualificationDropdownOpen = false"
                  class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 text-xs bg-white dark:bg-slate-800 text-slate-900 dark:text-white flex items-center justify-between text-left focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500 transition cursor-pointer"
                  :class="experienceDropdownOpen ? 'border-navy-800 dark:border-indigo-500 ring-2 ring-navy-800/20' : 'hover:border-slate-300 dark:hover:border-slate-600'"
                >
                  <span :class="draft.experience ? 'text-slate-800 dark:text-white font-medium' : 'text-slate-400 dark:text-slate-500'">
                    {{ t(draft.experience) || t('Choose your experience level') }}
                  </span>
                  <ChevronDown class="w-4 h-4 text-slate-400 transition-transform duration-200 shrink-0" :class="{ 'rotate-180 text-navy-800 dark:text-indigo-400': experienceDropdownOpen }" />
                </button>

                <div
                  v-if="experienceDropdownOpen"
                  class="absolute left-0 right-0 top-full z-30 mt-1.5 overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-1.5 shadow-xl space-y-1"
                >
                  <button
                    v-for="option in experienceOptions"
                    :key="option"
                    type="button"
                    @click="selectExperience(option)"
                    class="flex w-full items-center justify-between rounded-xl px-3 py-2 text-xs transition cursor-pointer"
                    :class="draft.experience === option
                      ? 'bg-navy-50 dark:bg-slate-700 text-navy-900 dark:text-white font-bold'
                      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/60 hover:text-navy-900 dark:hover:text-white font-medium'"
                  >
                    <span>{{ t(option) }}</span>
                    <Check v-if="draft.experience === option" class="w-4 h-4 text-navy-900 dark:text-white shrink-0" />
                  </button>
                </div>
              </div>
            </div>
          </section>

          <div class="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
            <button
              type="button"
              class="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2.5 text-sm font-semibold text-slate-700 dark:text-slate-300 transition hover:bg-slate-50 dark:hover:bg-slate-700 cursor-pointer"
              @click="cancelEditing"
            >
              <X class="h-4 w-4" aria-hidden="true" />
              {{ t('Cancel') }}
            </button>
            <button
              type="submit"
              class="inline-flex items-center justify-center gap-2 rounded-lg bg-navy-900 dark:bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-navy-800 dark:hover:bg-indigo-700 cursor-pointer"
            >
              <Check class="h-4 w-4" aria-hidden="true" />
              {{ t('Save changes') }}
            </button>
          </div>
        </form>

        <div v-else class="space-y-5">
          <!-- Profile Photo Card -->
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs overflow-hidden">
            <div class="flex flex-col sm:flex-row items-center sm:items-start gap-5 p-5 sm:p-6">
              <div class="relative group shrink-0">
                <div class="flex h-20 w-20 sm:h-24 sm:w-24 items-center justify-center rounded-2xl border-2 border-slate-200 dark:border-slate-700 bg-navy-50 dark:bg-slate-800 text-2xl font-black text-navy-800 dark:text-white shadow-xs overflow-hidden">
                  <img
                    v-if="profile.avatarUrl && !avatarLoadFailed"
                    :src="resolveImageUrl(profile.avatarUrl)"
                    :alt="profile.fullName"
                    class="h-full w-full object-cover"
                    @error="onAvatarError"
                  />
                  <span v-else>{{ initials }}</span>
                </div>
                <button
                  type="button"
                  class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center text-white text-xs font-bold rounded-2xl cursor-pointer"
                  :title="t('Change profile photo')"
                  @click="triggerAvatarUpload"
                >
                  <Camera class="w-5 h-5 mb-1" />
                  <span>{{ t('Change') }}</span>
                </button>
              </div>

              <div class="space-y-1.5 text-center sm:text-left flex-1 min-w-0">
                <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2">
                  <h3 class="text-sm font-bold text-navy-900 dark:text-white">{{ t('Profile photo') }}</h3>
                  <span v-if="profile.avatarUrl && !avatarLoadFailed" class="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/50 px-2 py-0.5 rounded-full border border-emerald-200 dark:border-emerald-800/60">
                    Active
                  </span>
                </div>
                <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed max-w-lg">
                  {{ t('Upload a photo or avatar image. Recommended size: at least 256x256 px (JPG, PNG, or WebP).') }}
                </p>
                <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2.5 pt-2">
                  <button
                    type="button"
                    class="inline-flex items-center gap-1.5 rounded-lg bg-navy-900 dark:bg-indigo-600 px-3.5 py-2 text-xs font-semibold text-white hover:bg-navy-800 dark:hover:bg-indigo-500 shadow-2xs transition cursor-pointer"
                    :disabled="avatarUploading"
                    @click="triggerAvatarUpload"
                  >
                    <RefreshCw v-if="avatarUploading" class="h-3.5 w-3.5 animate-spin" />
                    <Upload v-else class="h-3.5 w-3.5" />
                    <span>{{ avatarUploading ? 'Uploading...' : (profile.avatarUrl && !avatarLoadFailed ? t('Change photo') : t('Upload photo')) }}</span>
                  </button>
                  <button
                    v-if="profile.avatarUrl && !avatarLoadFailed"
                    type="button"
                    class="inline-flex items-center gap-1.5 rounded-lg border border-red-200 dark:border-red-900/60 bg-red-50/60 dark:bg-red-950/40 px-3.5 py-2 text-xs font-semibold text-red-700 dark:text-red-400 hover:bg-red-100 dark:hover:bg-red-900/50 transition cursor-pointer"
                    @click="removeAvatar"
                  >
                    <Trash2 class="h-3.5 w-3.5" />
                    <span>{{ t('Remove photo') }}</span>
                  </button>
                </div>
              </div>
            </div>
          </section>

          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs">
            <div class="flex flex-col gap-4 border-b border-slate-100 dark:border-slate-800 px-5 py-5 sm:flex-row sm:items-center sm:justify-between sm:px-7">
              <div class="flex items-center gap-3">
                <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
                  <UserRound class="h-5 w-5" aria-hidden="true" />
                </span>
                <div>
                  <h2 class="text-base font-bold text-navy-900 dark:text-white">{{ t('Personal details') }}</h2>
                  <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-400">{{ t('Your contact and personal information.') }}</p>
                </div>
              </div>
              <button
                type="button"
                class="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs font-semibold text-navy-900 dark:text-white transition hover:border-navy-800 dark:hover:border-slate-600 hover:bg-navy-50 dark:hover:bg-slate-700 cursor-pointer"
                @click="startEditing"
              >
                <Pencil class="h-3.5 w-3.5" aria-hidden="true" />
                {{ hasProfile ? t('Edit profile') : t('Add profile details') }}
              </button>
            </div>
            <dl class="grid gap-x-6 sm:grid-cols-2">
              <ProfileDetail label="Full name" :value="profile.fullName" :icon="UserRound" />
              <ProfileDetail label="Email address" :value="profile.email" :icon="Mail" />
              <ProfileDetail label="Phone number" :value="profile.phone" :icon="Phone" />
              <ProfileDetail label="Telegram username" :value="profile.telegram" :icon="Send" />
              <ProfileDetail label="Date of birth" :value="formattedDate" :icon="CalendarDays" />
              <ProfileDetail label="City or province" :value="profile.location" :icon="MapPin" />
            </dl>
          </section>

          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs">
            <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 px-5 py-5 sm:px-7">
              <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
                <GraduationCap class="h-5 w-5" aria-hidden="true" />
              </span>
              <div>
                <h2 class="text-base font-bold text-navy-900 dark:text-white">{{ t('Learning background') }}</h2>
                <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-400">{{ t('Your education and experience.') }}</p>
              </div>
            </div>
            <dl class="grid gap-x-6 sm:grid-cols-2">
              <ProfileDetail label="Highest qualification" :value="displayQualification" :icon="GraduationCap" />
              <ProfileDetail label="Current occupation" :value="profile.occupation" :icon="BriefcaseBusiness" />
              <ProfileDetail label="Coding experience" :value="profile.experience" :icon="Code2" />
            </dl>
          </section>

          <p class="px-1 text-xs leading-5 text-slate-500 dark:text-slate-400">
            {{ t('Your account details and profile information are securely saved to your account.') }}
          </p>

          <!-- Terms & Privacy Trust Card for Profile information -->
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-xs transition-colors">
            <div class="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
              <div class="flex items-center gap-3">
                <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-emerald-50 dark:bg-emerald-950/40 text-emerald-700 dark:text-emerald-300">
                  <ShieldCheck class="h-5 w-5" aria-hidden="true" />
                </span>
                <div>
                  <h3 class="text-xs font-bold text-navy-900 dark:text-white sm:text-sm">
                    {{ t('Terms & Privacy for your Profile') }}
                  </h3>
                  <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                    {{ t('Your profile information is protected under our') }}
                    <button type="button" @click="selectSection('terms')" class="font-semibold text-navy-800 dark:text-indigo-400 hover:underline cursor-pointer">
                      {{ t('Terms of use') }}
                    </button>
                    {{ t('and') }}
                    <button type="button" @click="selectSection('privacy')" class="font-semibold text-navy-800 dark:text-indigo-400 hover:underline cursor-pointer">
                      {{ t('Privacy Policy') }}
                    </button>.
                  </p>
                </div>
              </div>
              <div class="flex items-center gap-2 self-start sm:self-auto shrink-0">
                <button
                  type="button"
                  @click="selectSection('terms')"
                  class="rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-3 py-1.5 text-xs font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 transition cursor-pointer"
                >
                  {{ t('Terms of use') }}
                </button>
                <button
                  type="button"
                  @click="selectSection('privacy')"
                  class="rounded-lg border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-3 py-1.5 text-xs font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 transition cursor-pointer"
                >
                  {{ t('Privacy Policy') }}
                </button>
              </div>
            </div>
          </section>
        </div>
      </div>
    </div>

    <div
      v-if="logoutDialogOpen"
      class="fixed inset-0 z-[60] flex items-center justify-center bg-slate-950/40 px-4 py-6"
      @click.self="logoutDialogOpen = false"
    >
      <section
        role="dialog"
        aria-modal="true"
        :aria-labelledby="'logout-dialog-title'"
        class="w-full max-w-md rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-6 shadow-xl"
      >
        <div class="flex h-11 w-11 items-center justify-center rounded-xl bg-red-50 dark:bg-red-950/60 text-red-600 dark:text-red-400">
          <LogOut class="h-5 w-5" aria-hidden="true" />
        </div>
        <h2 id="logout-dialog-title" class="mt-4 text-lg font-bold text-navy-900 dark:text-white">{{ t('Log out of your account?') }}</h2>
        <p class="mt-2 text-sm leading-6 text-slate-500 dark:text-slate-400">
          {{ t('You will be signed out of this account on this device.') }}
        </p>
        <div class="mt-6 flex justify-end gap-3">
          <button
            type="button"
            class="rounded-lg border border-slate-300 dark:border-slate-600 px-4 py-2.5 text-sm font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 cursor-pointer"
            @click="logoutDialogOpen = false"
          >
            {{ t('Cancel') }}
          </button>
          <button
            type="button"
            class="rounded-lg bg-red-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-red-700 cursor-pointer"
            @click="confirmLogout"
          >
            {{ t('Log out') }}
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, defineComponent, h, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useLanguage } from '../i18n'
import DatePicker from '../components/common/DatePicker.vue'
import { accountService, enrollmentService } from '../services/api'
import { formatCambodiaTime } from '../utils/date'
import { resolveImageUrl } from '../utils/image'
import { useTheme } from '../composables/useTheme'
import {
  AlertCircle,
  ArrowRight,
  BookOpen,
  BriefcaseBusiness,
  CalendarDays,
  Camera,
  Check,
  CheckCircle2,
  ChevronDown,
  Code2,
  FileText,
  GraduationCap,
  Globe2,
  HelpCircle,
  Lock,
  LogOut,
  Mail,
  MapPin,
  Moon,
  Pencil,
  Phone,
  RefreshCw,
  Scale,
  Send,
  Settings,
  ShieldCheck,
  ShoppingBag,
  Sparkles,
  Sun,
  Trash2,
  Upload,
  UserCheck,
  UserRound,
  X,
} from 'lucide-vue-next'

const { locale, setLocale, t } = useLanguage()
const { isDark, toggleTheme, setTheme } = useTheme()
const router = useRouter()
const accountSections = [
  { id: 'profile', label: 'Profile information', icon: UserRound },
  { id: 'history', label: 'Course history', icon: BookOpen },
  { id: 'orders', label: 'My orders', icon: ShoppingBag },
  { id: 'settings', label: 'Settings', icon: Settings },
  { id: 'terms', label: 'Terms of use', icon: Scale },
  { id: 'privacy', label: 'Privacy Policy', icon: ShieldCheck },
]

const activeSectionTitle = computed(() => {
  switch (activeSection.value) {
    case 'history': return t('Course history')
    case 'orders': return t('My orders')
    case 'settings': return t('Settings')
    case 'terms': return t('Terms of use')
    case 'privacy': return t('Privacy Policy')
    default: return t('Profile information')
  }
})

const activeSectionDescription = computed(() => {
  switch (activeSection.value) {
    case 'history': return t('Review your registrations and payment status.')
    case 'orders': return t('Review your store purchases and hardware orders.')
    case 'settings': return t('Manage your language and local profile preferences.')
    case 'terms': return t('Review our terms, student commitments, and platform guidelines.')
    case 'privacy': return t('Learn how AeroByte Academy collects, safeguards, and handles your personal and learning data.')
    default: return t('Keep your contact and learning details up to date so we can make your AeroByte experience more personal.')
  }
})
const emptyProfile = () => ({
  fullName: '',
  email: '',
  avatarUrl: '',
  phone: '',
  telegram: '',
  dateOfBirth: '',
  location: '',
  qualification: '',
  qualificationOther: '',
  occupation: '',
  experience: '',
})

const account = ref(null)
const profile = reactive(emptyProfile())
const draft = reactive(emptyProfile())
const storageKey = computed(() => account.value ? `aerobyte-profile:${account.value.id}` : 'aerobyte-profile')
const storageEmailKey = computed(() => account.value?.email ? `aerobyte-profile:${account.value.email.toLowerCase()}` : null)
const historyStorageKey = computed(() => account.value ? `aerobyte-course-history:${account.value.id}` : 'aerobyte-course-history')
const historyEmailKey = computed(() => account.value?.email ? `aerobyte-course-history:${account.value.email.toLowerCase()}` : null)
const isEditing = ref(false)
const notice = ref('')
const noticeType = ref('success')
const activeSection = ref('profile')
const storeOrders = ref([])
const ordersLoading = ref(false)

async function loadStoreOrders() {
  ordersLoading.value = true
  try {
    // 1. Fetch persistent orders from database
    const { data } = await accountService.getUserOrders()
    const serverOrders = Array.isArray(data) ? data : []

    // 2. Check if there are local orders created before login that can be synced
    try {
      const raw = localStorage.getItem('aerobyte_store_orders')
      const localOrders = raw ? JSON.parse(raw) : []
      const serverOrderIds = new Set(serverOrders.map((o) => o.id))
      for (const localOrder of localOrders) {
        if (!serverOrderIds.has(localOrder.id)) {
          try {
            await accountService.createStoreOrder({
              id: localOrder.id,
              name: localOrder.customer?.name || localOrder.name || account.value?.name || 'Customer',
              phone: localOrder.customer?.phone || localOrder.phone || account.value?.phone || '',
              telegram: localOrder.customer?.telegram || localOrder.telegram || '',
              address: localOrder.customer?.address || localOrder.address || '',
              fulfillment: localOrder.fulfillment || 'pickup',
              items: localOrder.items || [],
              subtotal: localOrder.subtotal || 0,
              delivery_fee: localOrder.delivery_fee || localOrder.deliveryFee || 0,
              discount: localOrder.discount || 0,
              total: localOrder.total || 0,
            })
            serverOrders.unshift(localOrder)
          } catch (syncErr) {
            console.warn('Could not sync local order to database:', syncErr)
          }
        }
      }
    } catch (_) {}

    storeOrders.value = serverOrders
    try {
      localStorage.setItem('aerobyte_store_orders', JSON.stringify(serverOrders))
    } catch {}
    return
  } catch (e) {
    console.warn('Could not fetch store orders from server, using local cache:', e)
  } finally {
    ordersLoading.value = false
  }

  try {
    const raw = localStorage.getItem('aerobyte_store_orders')
    storeOrders.value = raw ? JSON.parse(raw) : []
  } catch (e) {
    console.error('Failed to parse store orders', e)
    storeOrders.value = []
  }
}

const courseHistory = ref([])
const historyLoading = ref(false)
const historyError = ref('')
const logoutDialogOpen = ref(false)
const avatarFileInput = ref(null)
const avatarUploading = ref(false)
const avatarLoadFailed = ref(false)

const qualificationDropdownRef = ref(null)
const qualificationDropdownOpen = ref(false)
const experienceDropdownRef = ref(null)
const experienceDropdownOpen = ref(false)
const languageDropdownRef = ref(null)
const languageDropdownOpen = ref(false)

const qualificationOptions = [
  'High school',
  'Undergraduate / University',
  'Graduate degree',
  'Other',
]

const experienceOptions = [
  'New to coding',
  'Some experience',
  'Confident coder',
  'Experienced developer',
]

function selectQualification(option) {
  draft.qualification = option
  qualificationDropdownOpen.value = false
}

function selectExperience(option) {
  draft.experience = option
  experienceDropdownOpen.value = false
}

function onPhoneKeypress(event) {
  if (event.ctrlKey || event.metaKey || event.altKey) {
    return
  }
  // Allow digits 0-9
  if (event.key >= '0' && event.key <= '9') {
    return
  }
  // Allow '+' only if it is the first character and no '+' exists yet
  if (event.key === '+') {
    const target = event.target
    if (target.selectionStart === 0 && !target.value.includes('+')) {
      return
    }
  }
  event.preventDefault()
}

function onPhoneInput(event) {
  const raw = event.target.value
  let filtered = raw.replace(/[^0-9+]/g, '')
  if (filtered.includes('+')) {
    filtered = (filtered.startsWith('+') ? '+' : '') + filtered.replace(/\+/g, '')
  }
  draft.phone = filtered
  event.target.value = filtered
}

function handleDropdownClickOutside(event) {
  if (qualificationDropdownRef.value && !qualificationDropdownRef.value.contains(event.target)) {
    qualificationDropdownOpen.value = false
  }
  if (experienceDropdownRef.value && !experienceDropdownRef.value.contains(event.target)) {
    experienceDropdownOpen.value = false
  }
  if (languageDropdownRef.value && !languageDropdownRef.value.contains(event.target)) {
    languageDropdownOpen.value = false
  }
}

const completion = computed(() => {
  const fields = [
    Boolean(profile.fullName?.trim()),
    Boolean(profile.email?.trim()),
    Boolean(profile.avatarUrl?.trim()),
    Boolean(profile.phone?.trim()),
    Boolean(profile.telegram?.trim()),
    Boolean(profile.dateOfBirth?.trim()),
    Boolean(profile.location?.trim()),
    Boolean(
      profile.qualification?.trim() &&
      (profile.qualification !== 'Other' || profile.qualificationOther?.trim())
    ),
    Boolean(profile.occupation?.trim()),
    Boolean(profile.experience?.trim()),
  ]
  const completedCount = fields.filter(Boolean).length
  return Math.round((completedCount / fields.length) * 100)
})
const hasProfile = computed(() => Object.values(profile).some((value) => value.trim()))
const displayQualification = computed(() =>
  profile.qualification === 'Other'
    ? profile.qualificationOther || t('Other')
    : profile.qualification,
)
const initials = computed(() => {
  const names = profile.fullName.trim().split(/\s+/).filter(Boolean)
  return names.length ? names.slice(0, 2).map((name) => name[0].toUpperCase()).join('') : 'AA'
})
const formattedDate = computed(() => {
  if (!profile.dateOfBirth) return ''
  const date = new Date(`${profile.dateOfBirth}T00:00:00`)
  return Number.isNaN(date.getTime())
    ? profile.dateOfBirth
    : new Intl.DateTimeFormat('en', { dateStyle: 'long' }).format(date)
})

const ProfileDetail = defineComponent({
  props: {
    label: { type: String, required: true },
    value: { type: String, default: '' },
    icon: { type: [Object, Function], required: true },
  },
  setup(props) {
    return () =>
      h('div', { class: 'flex gap-3 border-b border-slate-100 dark:border-slate-800 px-5 py-4 last:border-0 sm:px-7' }, [
        h('span', { class: 'mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-slate-50 dark:bg-slate-800 text-slate-500 dark:text-slate-400' }, [
          h(props.icon, { class: 'h-4 w-4', 'aria-hidden': 'true' }),
        ]),
        h('div', { class: 'min-w-0' }, [
          h('dt', { class: 'text-[11px] font-semibold uppercase tracking-wide text-slate-400 dark:text-slate-400' }, props.label),
          h('dd', { class: ['mt-1 break-words text-sm font-medium', props.value ? 'text-slate-700 dark:text-slate-200' : 'text-slate-400 dark:text-slate-500'] }, props.value || t('Not added yet')),
        ]),
      ])
  },
})

function copyProfile(target, source) {
  Object.keys(target).forEach((key) => {
    target[key] = typeof source[key] === 'string' ? source[key] : ''
  })
}

onMounted(async () => {
  // 1. Instant local pre-hydration on tick 0 before any network request
  try {
    const findCached = () => {
      const direct = localStorage.getItem('aerobyte-profile-current') || localStorage.getItem('aerobyte-profile')
      if (direct) {
        try {
          const parsed = JSON.parse(direct)
          if (parsed && (parsed.fullName || parsed.email || parsed.phone)) return parsed
        } catch (_) {}
      }
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i)
        if (k && k.startsWith('aerobyte-profile:')) {
          try {
            const parsed = JSON.parse(localStorage.getItem(k) || '{}')
            if (parsed && (parsed.fullName || parsed.email || parsed.phone)) return parsed
          } catch (_) {}
        }
      }
      return null
    }
    const localCached = findCached()
    if (localCached) {
      copyProfile(profile, localCached)
      copyProfile(draft, localCached)
    }
  } catch (_) {}

  // 2. Fetch authenticated session from server
  try {
    const { data } = await accountService.getSession()
    if (!data.authenticated) {
      await router.replace({ path: '/account', query: { mode: 'signin' } })
      return
    }
    account.value = data.user

    const pendingEnrollRedirect = sessionStorage.getItem('aerobyte_enroll_redirect')
    if (pendingEnrollRedirect && pendingEnrollRedirect.startsWith('/')) {
      sessionStorage.removeItem('aerobyte_enroll_redirect')
      await router.replace(pendingEnrollRedirect)
      return
    }

    // Merge server data with local cache
    let cached = {}
    try {
      const raw = (storageEmailKey.value && localStorage.getItem(storageEmailKey.value)) ||
                  (storageKey.value && localStorage.getItem(storageKey.value)) ||
                  localStorage.getItem('aerobyte-profile-current') ||
                  localStorage.getItem('aerobyte-profile')
      if (raw) {
        cached = JSON.parse(raw)
        copyProfile(profile, cached)
      }
    } catch (_) {}

    // Server data takes precedence if present
    if (account.value.name) profile.fullName = account.value.name
    if (account.value.email) profile.email = account.value.email
    if (account.value.avatar_url) profile.avatarUrl = account.value.avatar_url
    if (account.value.phone) profile.phone = account.value.phone
    if (account.value.telegram) profile.telegram = account.value.telegram
    if (account.value.date_of_birth) profile.dateOfBirth = account.value.date_of_birth
    if (account.value.gender) profile.gender = account.value.gender
    if (account.value.location) profile.location = account.value.location
    if (account.value.qualification) profile.qualification = account.value.qualification
    if (account.value.qualification_other) profile.qualificationOther = account.value.qualification_other
    if (account.value.occupation) profile.occupation = account.value.occupation
    if (account.value.experience) profile.experience = account.value.experience

    // If server had missing fields that were restored from local cache, auto-sync back to server!
    const hasLocalRestore = (
      (!account.value.phone && profile.phone) ||
      (!account.value.telegram && profile.telegram) ||
      (!account.value.date_of_birth && profile.dateOfBirth) ||
      (!account.value.gender && profile.gender) ||
      (!account.value.location && profile.location) ||
      (!account.value.qualification && profile.qualification) ||
      (!account.value.occupation && profile.occupation) ||
      (!account.value.experience && profile.experience)
    )
    if (hasLocalRestore) {
      accountService.updateProfile({
        full_name: profile.fullName,
        email: profile.email,
        avatar_url: profile.avatarUrl,
        phone: profile.phone,
        telegram: profile.telegram,
        date_of_birth: profile.dateOfBirth,
        gender: profile.gender,
        location: profile.location,
        qualification: profile.qualification,
        qualification_other: profile.qualificationOther,
        occupation: profile.occupation,
        experience: profile.experience,
      }).catch((err) => console.warn('Background profile auto-sync failed:', err))
    }

    // Save back to local storage under all keys
    try {
      localStorage.setItem('aerobyte-profile-current', JSON.stringify(profile))
      if (storageEmailKey.value) localStorage.setItem(storageEmailKey.value, JSON.stringify(profile))
      if (storageKey.value) localStorage.setItem(storageKey.value, JSON.stringify(profile))
      localStorage.setItem('aerobyte-profile', JSON.stringify(profile))
    } catch (_) {}

    copyProfile(draft, profile)
    loadCourseHistory()
    loadStoreOrders()
  } catch (error) {
    console.warn('Could not load session from server, maintaining cached state:', error)
    if (!profile.fullName && !profile.email) {
      notice.value = t('Unable to load your account. Please try again.')
      noticeType.value = 'error'
    }
  }

  window.addEventListener('storage', loadStoreOrders)
  window.addEventListener('aerobyte-orders-updated', loadStoreOrders)
  const targetSection = router.currentRoute.value.query.section
  if (['orders', 'history', 'settings', 'terms', 'privacy'].includes(targetSection)) {
    activeSection.value = targetSection
  }
  document.addEventListener('click', handleDropdownClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleDropdownClickOutside)
  window.removeEventListener('storage', loadStoreOrders)
  window.removeEventListener('aerobyte-orders-updated', loadStoreOrders)
})

function selectSection(section) {
  activeSection.value = section
  notice.value = ''
  if (section !== 'profile') isEditing.value = false
  if (section === 'history' && !courseHistory.value.length) loadCourseHistory()
  if (section === 'orders') loadStoreOrders()
}

function statusClasses(status) {
  if (status === 'paid' || status === 'confirmed') return 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400'
  if (status === 'expired' || status === 'cancelled') return 'bg-red-50 text-red-700 dark:bg-red-950/40 dark:text-red-400'
  return 'bg-amber-50 text-amber-700 dark:bg-amber-950/40 dark:text-amber-400'
}

async function loadCourseHistory() {
  historyLoading.value = true
  historyError.value = ''
  try {
    let savedIds = []
    try {
      const parsed1 = JSON.parse(localStorage.getItem(historyStorageKey.value) || '[]')
      const parsed2 = JSON.parse((historyEmailKey.value && localStorage.getItem(historyEmailKey.value)) || '[]')
      const parsed3 = JSON.parse(localStorage.getItem('aerobyte-course-history') || '[]')
      const allParsed = [...(Array.isArray(parsed1) ? parsed1 : []), ...(Array.isArray(parsed2) ? parsed2 : []), ...(Array.isArray(parsed3) ? parsed3 : [])]
      savedIds = [...new Set(allParsed.filter((id) => typeof id === 'string' && id))]
    } catch (_) {}

    // Fetch user enrollments from the database by account email and/or cached IDs
    const userEmail = account.value?.email || profile.email || ''
    const { data } = await accountService.getUserEnrollments({
      email: userEmail,
      ids: savedIds.join(','),
    })

    const records = Array.isArray(data) ? data : []
    courseHistory.value = records

    // Cache enrollment IDs locally for offline fallback
    try {
      const allIds = [...new Set([...records.map((r) => r.enrollment_id), ...savedIds])]
      if (allIds.length > 0) {
        localStorage.setItem(historyStorageKey.value, JSON.stringify(allIds))
        if (historyEmailKey.value) {
          localStorage.setItem(historyEmailKey.value, JSON.stringify(allIds))
        }
        localStorage.setItem('aerobyte-course-history', JSON.stringify(allIds))
      }
    } catch (_) {}
  } catch (error) {
    console.error('Could not load course history:', error)
    historyError.value = t('Could not load course history. Please try refreshing.')
  } finally {
    historyLoading.value = false
  }
}

function clearLocalProfile() {
  try {
    localStorage.removeItem('aerobyte-profile-current')
    if (storageKey.value) localStorage.removeItem(storageKey.value)
    if (storageEmailKey.value) localStorage.removeItem(storageEmailKey.value)
    localStorage.removeItem('aerobyte-profile')
  } catch (error) {
    console.error('Could not clear saved profile:', error)
    notice.value = t('Could not clear profile information from this browser.')
    noticeType.value = 'error'
    return
  }
  copyProfile(profile, { ...emptyProfile(), fullName: account.value?.name || '', email: account.value?.email || '' })
  copyProfile(draft, profile)
  window.dispatchEvent(new Event('aerobyte-profile-updated'))
  notice.value = t('Profile information cleared from this browser.')
  noticeType.value = 'success'
}

async function confirmLogout() {
  try {
    await accountService.logout()
  } catch (error) {
    console.error('Could not sign out of the account:', error)
    notice.value = t('Unable to sign out right now. Please try again.')
    noticeType.value = 'error'
    logoutDialogOpen.value = false
    return
  }

  try {
    localStorage.removeItem('aerobyte-profile-current')
    if (storageKey.value) localStorage.removeItem(storageKey.value)
    if (storageEmailKey.value) localStorage.removeItem(storageEmailKey.value)
    localStorage.removeItem('aerobyte-profile')
  } catch (_) {}

  copyProfile(profile, emptyProfile())
  copyProfile(draft, emptyProfile())
  courseHistory.value = []
  window.dispatchEvent(new Event('aerobyte-profile-updated'))
  window.dispatchEvent(new Event('aerobyte-auth-updated'))
  account.value = null
  logoutDialogOpen.value = false
  router.push('/courses')
}

function startEditing() {
  notice.value = ''
  avatarLoadFailed.value = false
  qualificationDropdownOpen.value = false
  experienceDropdownOpen.value = false
  copyProfile(draft, profile)
  if (!draft.avatarUrl && profile.avatarUrl) {
    draft.avatarUrl = profile.avatarUrl
  }
  isEditing.value = true
}

function cancelEditing() {
  qualificationDropdownOpen.value = false
  experienceDropdownOpen.value = false
  copyProfile(draft, profile)
  isEditing.value = false
}

function triggerAvatarUpload() {
  avatarFileInput.value?.click()
}

function onAvatarError() {
  avatarLoadFailed.value = true
  if (profile.avatarUrl) {
    console.warn('Avatar image failed to load, clearing broken avatar reference:', profile.avatarUrl)
    profile.avatarUrl = ''
    draft.avatarUrl = ''
    if (account.value) account.value.avatar_url = ''
    try {
      const clearCache = (k) => {
        if (!k) return
        const s = JSON.parse(localStorage.getItem(k) || '{}')
        s.avatarUrl = ''
        localStorage.setItem(k, JSON.stringify(s))
      }
      clearCache('aerobyte-profile-current')
      clearCache(storageEmailKey.value)
      clearCache(storageKey.value)
      clearCache('aerobyte-profile')
      window.dispatchEvent(new Event('aerobyte-profile-updated'))
      window.dispatchEvent(new Event('aerobyte-auth-updated'))
    } catch (_) {}
    accountService.updateProfile({
      full_name: profile.fullName,
      email: profile.email,
      avatar_url: '',
    }).catch(() => {})
  }
}

async function handleAvatarChange(event) {
  const file = event.target.files?.[0]
  if (!file) return
  if (!file.type.startsWith('image/')) {
    notice.value = t('Please select a valid image file (JPG, PNG, WEBP).')
    noticeType.value = 'error'
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    notice.value = t('Image file size must be less than 5MB.')
    noticeType.value = 'error'
    return
  }

  avatarUploading.value = true
  avatarLoadFailed.value = false
  notice.value = ''

  const previewUrl = URL.createObjectURL(file)
  profile.avatarUrl = previewUrl
  draft.avatarUrl = previewUrl

  try {
    const userEmail = account.value?.email || profile.email || ''
    const { data } = await accountService.uploadAvatar(file, userEmail)
    if (data.avatar_url) {
      profile.avatarUrl = data.avatar_url
      draft.avatarUrl = data.avatar_url
      if (account.value) {
        account.value.avatar_url = data.avatar_url
      }
      avatarLoadFailed.value = false
      const updateAvatarCache = (key) => {
        if (!key) return
        try {
          const s = JSON.parse(localStorage.getItem(key) || '{}')
          s.avatarUrl = data.avatar_url
          localStorage.setItem(key, JSON.stringify(s))
        } catch (_) {}
      }
      updateAvatarCache('aerobyte-profile-current')
      updateAvatarCache(storageEmailKey.value)
      updateAvatarCache(storageKey.value)
      updateAvatarCache('aerobyte-profile')
      window.dispatchEvent(new Event('aerobyte-profile-updated'))
      window.dispatchEvent(new Event('aerobyte-auth-updated'))
      notice.value = t('Profile photo updated successfully!')
      noticeType.value = 'success'
    }
  } catch (error) {
    console.error('Failed to upload avatar to server:', error)
    profile.avatarUrl = ''
    draft.avatarUrl = ''
    avatarLoadFailed.value = false
    const detail = error.response?.data?.detail
    const detailMsg = Array.isArray(detail)
      ? (detail[0]?.msg || '')
      : (typeof detail === 'string' ? detail : (error.message || ''))
    notice.value = detailMsg || t('Failed to upload avatar image. Please try again.')
    noticeType.value = 'error'
  } finally {
    avatarUploading.value = false
    if (event.target) event.target.value = ''
  }
}

async function removeAvatar() {
  avatarLoadFailed.value = false
  profile.avatarUrl = ''
  draft.avatarUrl = ''
  if (account.value) {
    account.value.avatar_url = ''
  }
  try {
    await accountService.updateProfile({
      full_name: profile.fullName,
      email: profile.email,
      avatar_url: '',
    })
  } catch (e) {
    console.warn('Could not clear avatar on server:', e)
  }
  const clearAvatarCache = (key) => {
    if (!key) return
    try {
      const s = JSON.parse(localStorage.getItem(key) || '{}')
      s.avatarUrl = ''
      localStorage.setItem(key, JSON.stringify(s))
    } catch (_) {}
  }
  clearAvatarCache('aerobyte-profile-current')
  clearAvatarCache(storageEmailKey.value)
  clearAvatarCache(storageKey.value)
  clearAvatarCache('aerobyte-profile')
  window.dispatchEvent(new Event('aerobyte-profile-updated'))
  window.dispatchEvent(new Event('aerobyte-auth-updated'))
  notice.value = t('Profile photo removed.')
  noticeType.value = 'success'
}

async function saveProfile() {
  const nextProfile = { ...draft }
  if (nextProfile.occupation) {
    nextProfile.occupation = nextProfile.occupation.replace(/[0-9\u17E0-\u17E9]/g, '').trim()
  }

  // Preserve existing avatar if not explicitly changed
  if (!nextProfile.avatarUrl && profile.avatarUrl) {
    nextProfile.avatarUrl = profile.avatarUrl
  }
  if (!nextProfile.avatarUrl && account.value?.avatar_url) {
    nextProfile.avatarUrl = account.value.avatar_url
  }

  let avatarToSend = nextProfile.avatarUrl
  if (avatarToSend && (avatarToSend.startsWith('data:') || avatarToSend.startsWith('blob:'))) {
    avatarToSend = (profile.avatarUrl && !profile.avatarUrl.startsWith('data:') && !profile.avatarUrl.startsWith('blob:'))
      ? profile.avatarUrl
      : (account.value?.avatar_url || '')
  }

  try {
    const { data } = await accountService.updateProfile({
      full_name: nextProfile.fullName,
      email: nextProfile.email,
      avatar_url: avatarToSend,
      phone: nextProfile.phone,
      telegram: nextProfile.telegram,
      date_of_birth: nextProfile.dateOfBirth,
      gender: nextProfile.gender,
      location: nextProfile.location,
      qualification: nextProfile.qualification,
      qualification_other: nextProfile.qualificationOther,
      occupation: nextProfile.occupation,
      experience: nextProfile.experience,
    })
    account.value = data.user
    nextProfile.fullName = data.user.name
    nextProfile.email = data.user.email
    if (data.user.avatar_url !== undefined) {
      nextProfile.avatarUrl = data.user.avatar_url
    }
    if (data.user.phone !== undefined) nextProfile.phone = data.user.phone
    if (data.user.telegram !== undefined) nextProfile.telegram = data.user.telegram
    if (data.user.date_of_birth !== undefined) nextProfile.dateOfBirth = data.user.date_of_birth
    if (data.user.gender !== undefined) nextProfile.gender = data.user.gender
    if (data.user.location !== undefined) nextProfile.location = data.user.location
    if (data.user.qualification !== undefined) nextProfile.qualification = data.user.qualification
    if (data.user.qualification_other !== undefined) nextProfile.qualificationOther = data.user.qualification_other
    if (data.user.occupation !== undefined) nextProfile.occupation = data.user.occupation
    if (data.user.experience !== undefined) nextProfile.experience = data.user.experience
  } catch (error) {
    console.error('Could not update the account profile:', error)
    notice.value = error.response?.data?.detail || t('Your account details could not be updated. Please try again.')
    noticeType.value = 'error'
    return
  }

  try {
    localStorage.setItem('aerobyte-profile-current', JSON.stringify(nextProfile))
    if (storageEmailKey.value) localStorage.setItem(storageEmailKey.value, JSON.stringify(nextProfile))
    if (storageKey.value) localStorage.setItem(storageKey.value, JSON.stringify(nextProfile))
    localStorage.setItem('aerobyte-profile', JSON.stringify(nextProfile))
  } catch (error) {
    console.warn('Could not cache additional profile details to local storage:', error)
  }

  copyProfile(profile, nextProfile)
  avatarLoadFailed.value = false
  window.dispatchEvent(new Event('aerobyte-profile-updated'))
  window.dispatchEvent(new Event('aerobyte-auth-updated'))
  isEditing.value = false
  notice.value = t('Profile details saved.')
  noticeType.value = 'success'
}
</script>

<style>
.profile-input {
  display: block;
  width: 100%;
  border: 1px solid #cbd5e1;
  border-radius: 0.5rem;
  background: #fff;
  padding: 0.625rem 0.75rem;
  color: #334155;
  font-size: 0.875rem;
  outline: none;
  transition: border-color 150ms ease, box-shadow 150ms ease, background-color 150ms ease, color 150ms ease;
}

.profile-input::placeholder {
  color: #94a3b8;
}

.profile-input:focus {
  border-color: #27466d;
  box-shadow: 0 0 0 3px rgb(39 70 109 / 0.12);
}

html.dark .profile-input {
  background-color: #1e293b !important;
  border-color: #334155 !important;
  color: #f8fafc !important;
}

html.dark .profile-input::placeholder {
  color: #64748b !important;
}

html.dark .profile-input:focus {
  border-color: #6366f1 !important;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
}
</style>
