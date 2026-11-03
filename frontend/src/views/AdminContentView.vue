<template>
  <div class="h-screen overflow-hidden bg-slate-50 dark:bg-slate-950 flex flex-col lg:flex-row transition-colors">
    <!-- Unauthenticated State -->
    <main v-if="!authenticated" class="flex-1 flex items-center justify-center p-6 courses-hero min-h-screen">
      <section class="w-full max-w-md rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-6 shadow-card sm:p-8">
        <h1 class="text-2xl font-extrabold tracking-tight text-navy-900 dark:text-white">{{ t('Checking admin access') }}</h1>
        <p v-if="!errorMessage" class="mt-2 text-sm leading-6 text-slate-600 dark:text-slate-300">{{ t('Verifying your administrator session...') }}</p>
        <p v-else class="mt-3 rounded-lg bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900/40 px-3 py-2 text-sm text-red-700 dark:text-red-300" role="alert">{{ errorMessage }}</p>
        <RouterLink
          v-if="errorMessage"
          to="/account?mode=signin"
          class="mt-5 inline-flex text-sm font-semibold text-navy-800 dark:text-indigo-400 underline underline-offset-4 hover:text-navy-600 dark:hover:text-indigo-300"
        >
          {{ t('Go to sign in') }}
        </RouterLink>
      </section>
    </main>

    <!-- Authenticated Admin Layout (Sidebar + Main Content) -->
    <template v-else>
      <!-- Mobile Top Bar -->
      <div class="lg:hidden sticky top-0 z-40 bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-4 py-3 flex items-center justify-between shadow-2xs">
        <div class="flex items-center gap-2.5">
          <img src="/aerobyte-logo.png" alt="" class="h-8 w-10 object-contain transition duration-200 dark:brightness-0 dark:invert" />
          <span class="block text-sm font-extrabold text-navy-900 dark:text-white leading-tight">AeroByte Academy</span>
        </div>
        <button
          type="button"
          class="p-2 rounded-lg text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition"
          :aria-label="sidebarOpen ? 'Close menu' : 'Open menu'"
          @click="sidebarOpen = !sidebarOpen"
        >
          <X v-if="sidebarOpen" class="w-5 h-5" />
          <Menu v-else class="w-5 h-5" />
        </button>
      </div>

      <!-- Mobile Backdrop Overlay -->
      <div
        v-if="sidebarOpen"
        class="lg:hidden fixed inset-0 z-40 bg-slate-900/40 backdrop-blur-xs transition-opacity"
        @click="sidebarOpen = false"
      ></div>

      <!-- LEFT SIDEBAR (Desktop Mini Collapsible + Mobile Slide-over) -->
      <aside
        class="fixed inset-y-0 left-0 z-50 bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 flex flex-col transition-all duration-300 ease-in-out lg:static lg:relative lg:h-full lg:shrink-0 select-none shadow-sm lg:shadow-none lg:overflow-visible"
        :class="[
          sidebarOpen ? 'translate-x-0 w-72' : '-translate-x-full lg:translate-x-0',
          sidebarCollapsed ? 'lg:w-20' : 'lg:w-72'
        ]"
      >
        <!-- Logo Header (Fixed 76px height with button anchored directly to bottom border line in both states) -->
        <div
          class="relative h-[76px] px-5 border-b border-slate-100 dark:border-slate-800 bg-white dark:bg-slate-900 shrink-0 flex items-center transition-all"
          :class="sidebarCollapsed ? 'justify-center px-3' : 'justify-start'"
        >
          <!-- Expanded View: Logo + Text -->
          <RouterLink
            v-if="!sidebarCollapsed"
            to="/courses"
            class="flex items-center gap-2.5 text-base font-extrabold tracking-tight text-navy-900 dark:text-white group min-w-0"
          >
            <img src="/aerobyte-logo.png" alt="AeroByte Logo" class="h-9 w-11 object-contain shrink-0 transition duration-200 dark:brightness-0 dark:invert" />
            <span class="text-base font-extrabold tracking-tight text-navy-900 dark:text-white truncate">AeroByte Academy</span>
          </RouterLink>

          <!-- Collapsed View: Just Logo Icon -->
          <RouterLink
            v-else
            to="/courses"
            class="flex items-center justify-center hover:opacity-85 transition"
            title="AeroByte Academy"
          >
            <img src="/aerobyte-logo.png" alt="AeroByte Logo" class="h-9 w-11 object-contain shrink-0 transition duration-200 dark:brightness-0 dark:invert" />
          </RouterLink>

          <!-- Floating Border Toggle Arrow Button anchored to bottom-0 of the logo header (Always exactly centered on the horizontal border line in both open and closed navigation) -->
          <button
            type="button"
            class="hidden lg:flex absolute -right-3.5 bottom-0 translate-y-1/2 z-30 w-7 h-7 rounded-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 shadow-md hover:shadow-lg items-center justify-center text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white hover:bg-slate-50 dark:hover:bg-slate-700 transition cursor-pointer"
            :title="sidebarCollapsed ? t('Expand sidebar') : t('Collapse sidebar')"
            :aria-label="sidebarCollapsed ? t('Expand sidebar') : t('Collapse sidebar')"
            @click="toggleSidebarCollapse"
          >
            <ChevronRight v-if="sidebarCollapsed" class="w-3.5 h-3.5" />
            <ChevronLeft v-else class="w-3.5 h-3.5" />
          </button>
        </div>

        <!-- Section Category Header -->
        <div
          v-if="!sidebarCollapsed"
          class="p-3 text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 shrink-0 px-4 pt-4"
        >
          {{ t('Admin sections') }}
        </div>
        <div v-else class="h-3 shrink-0"></div>

        <nav class="relative flex-1 px-2.5 space-y-1.5 overflow-y-auto lg:overflow-visible">
          <!-- Smooth Spring Sliding Highlight Box -->
          <div
            v-if="highlightStyle.height"
            class="absolute left-2.5 right-2.5 rounded-xl bg-navy-900 dark:bg-blue-600 shadow-sm pointer-events-none transition-all duration-300 z-0"
            :style="highlightStyle"
            aria-hidden="true"
          ></div>

          <div
            v-for="(section, idx) in adminSections"
            :key="section.id"
            :ref="el => { if (el) navItemRefs[idx] = el }"
            class="relative group z-10"
          >
            <!-- Navigation Button -->
            <button
              type="button"
              class="w-full flex items-center rounded-xl text-left text-xs font-bold transition-all duration-150 cursor-pointer border"
              :class="[
                sidebarCollapsed ? 'justify-center p-3' : 'gap-3 px-3.5 py-3',
                activeSection === section.id
                  ? 'text-white border-transparent'
                  : 'text-slate-600 dark:text-slate-400 border-transparent hover:text-navy-900 dark:hover:text-white hover:bg-slate-100/90 dark:hover:bg-slate-800/80 hover:border-slate-200/70 dark:hover:border-slate-700/60 hover:shadow-2xs'
              ]"
              :title="sidebarCollapsed ? t(section.title) : undefined"
              @click="selectSection(section.id)"
            >
              <!-- Icon with active / hover effect -->
              <component
                :is="section.icon"
                class="shrink-0 transition-transform duration-150"
                :class="[
                  activeSection === section.id
                    ? 'text-white'
                    : 'text-slate-400 group-hover:text-navy-900 dark:group-hover:text-white group-hover:scale-110',
                  sidebarCollapsed ? 'w-5 h-5' : 'w-4 h-4'
                ]"
              />

              <!-- Label (visible when expanded) -->
              <span v-if="!sidebarCollapsed" class="truncate flex-1">{{ t(section.title) }}</span>

              <!-- Animated Arrow Indicator (visible when expanded) -->
              <ChevronRight
                v-if="!sidebarCollapsed"
                class="w-3.5 h-3.5 shrink-0 transition-all duration-150"
                :class="activeSection === section.id
                  ? 'opacity-100 text-white translate-x-0'
                  : 'opacity-0 -translate-x-1.5 group-hover:opacity-100 group-hover:translate-x-0 text-slate-400 group-hover:text-navy-900 dark:group-hover:text-white'"
              />
            </button>

            <!-- Floating Preview Card on Hover (Desktop) -->
            <div
              class="hidden lg:block absolute left-full top-0 ml-3 z-50 w-64 p-4 rounded-2xl bg-white dark:bg-slate-800 border border-slate-200/90 dark:border-slate-700 shadow-xl opacity-0 translate-x-1 pointer-events-none group-hover:opacity-100 group-hover:translate-x-0 transition-all duration-200 ease-out"
            >
              <div class="flex items-center gap-2 mb-1.5">
                <component :is="section.icon" class="w-4 h-4 text-navy-800 dark:text-indigo-400" />
                <h4 class="font-extrabold text-xs text-navy-900 dark:text-white">{{ t(section.title) }}</h4>
              </div>
              <p class="text-[11px] leading-relaxed text-slate-600 dark:text-slate-300 mb-2.5">{{ t(section.summary) }}</p>
              
              <div class="space-y-1 pt-2 border-t border-slate-100 dark:border-slate-700">
                <p v-for="feat in section.features.slice(0, 3)" :key="feat" class="text-[10px] text-slate-500 dark:text-slate-400 flex items-center gap-1.5">
                  <span class="w-1.5 h-1.5 rounded-full bg-navy-600 dark:bg-indigo-400 shrink-0"></span>
                  <span class="truncate">{{ t(feat) }}</span>
                </p>
              </div>

              <div class="mt-2.5 pt-2 border-t border-slate-100 dark:border-slate-700 flex items-center justify-between text-[10px]">
                <span class="text-slate-400">{{ activeSection === section.id ? t('Currently Active') : t('Click to View') }}</span>
                <span
                  class="font-bold px-2 py-0.5 rounded border"
                  :class="activeSection === section.id
                    ? 'text-navy-800 dark:text-indigo-300 bg-navy-50 dark:bg-indigo-950/50 border-navy-200 dark:border-indigo-800'
                    : 'text-emerald-700 dark:text-emerald-300 bg-emerald-50 dark:bg-emerald-950/50 border-emerald-200 dark:border-emerald-800'"
                >
                  {{ activeSection === section.id ? t('Active') : t('Open') }}
                </span>
              </div>
            </div>
          </div>
        </nav>

        <!-- Sidebar Footer Controls -->
        <div class="p-2.5 border-t border-slate-100 dark:border-slate-800 bg-slate-50/60 dark:bg-slate-900/60 shrink-0 space-y-2">
          <!-- Language Switcher in Sidebar -->
          <div
            v-if="!sidebarCollapsed"
            class="flex items-center justify-between px-2.5 py-1.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700 shadow-2xs"
          >
            <span class="text-xs font-bold text-slate-700 dark:text-slate-200 flex items-center gap-1.5">
              <Globe class="w-3.5 h-3.5 text-slate-400 dark:text-slate-500" />
              <span>{{ t('Language') }}</span>
            </span>
            <div class="flex items-center gap-1 rounded-lg bg-slate-100 dark:bg-slate-900/80 p-0.5 border border-slate-200/50 dark:border-slate-700/50">
              <button
                type="button"
                @click="setLocale('en')"
                class="px-2 py-0.5 rounded-md text-[11px] font-bold transition-all cursor-pointer"
                :class="locale === 'en'
                  ? 'bg-white dark:bg-slate-700 text-navy-900 dark:text-white shadow-2xs font-extrabold'
                  : 'text-slate-500 dark:text-slate-400 hover:text-navy-900 dark:hover:text-white'"
              >
                EN
              </button>
              <button
                type="button"
                @click="setLocale('kh')"
                class="px-2 py-0.5 rounded-md text-[11px] font-bold transition-all cursor-pointer"
                :class="locale === 'kh'
                  ? 'bg-white dark:bg-slate-700 text-navy-900 dark:text-white shadow-2xs font-extrabold'
                  : 'text-slate-500 dark:text-slate-400 hover:text-navy-900 dark:hover:text-white'"
              >
                KH
              </button>
            </div>
          </div>
          <!-- Language Toggle Button in Mini / Collapsed Mode -->
          <div v-else class="flex justify-center py-0.5">
            <button
              type="button"
              @click="setLocale(locale === 'en' ? 'kh' : 'en')"
              class="flex h-7 w-7 items-center justify-center rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-[10px] font-black text-navy-900 dark:text-white hover:bg-slate-50 dark:hover:bg-slate-700 transition cursor-pointer shadow-2xs"
              :title="locale === 'en' ? t('Switch to Khmer') : t('Switch to English')"
            >
              {{ locale.toUpperCase() }}
            </button>
          </div>

          <!-- Animated Cat Light/Dark Switch -->
          <div
            v-if="!sidebarCollapsed"
            class="flex items-center justify-between px-2.5 py-1.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700 shadow-2xs"
          >
            <span class="text-xs font-bold text-slate-700 dark:text-slate-200 flex items-center gap-1.5">
              <span>{{ t('Theme') }}</span>
              <span class="text-[10px] text-slate-400 font-normal">({{ isDark ? t('Dark') : t('Light') }})</span>
            </span>
            <CatThemeSwitch compact />
          </div>
          <!-- Cat Head Only Switch in Mini / Collapsed Mode -->
          <div v-else class="flex justify-center py-1">
            <CatThemeSwitch head-only />
          </div>

          <!-- Public Site Link -->
          <RouterLink
            to="/courses"
            class="w-full flex items-center rounded-lg text-xs font-semibold text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white hover:bg-white dark:hover:bg-slate-800 transition border border-transparent hover:border-slate-200 dark:hover:border-slate-700"
            :class="sidebarCollapsed ? 'justify-center p-2.5' : 'justify-between px-3 py-2'"
            :title="sidebarCollapsed ? t('Explore Courses') : undefined"
          >
            <span class="flex items-center gap-2">
              <ExternalLink class="w-3.5 h-3.5 text-slate-400" />
              <span v-if="!sidebarCollapsed">{{ t('Explore Courses') }}</span>
            </span>
            <span v-if="!sidebarCollapsed" class="text-[10px] text-slate-400 font-medium">{{ t('Public') }}</span>
          </RouterLink>

          <!-- Sign Out Button -->
          <button
            type="button"
            :disabled="busy"
            class="w-full flex items-center justify-center rounded-lg text-xs font-bold text-red-600 dark:text-red-400 hover:text-red-700 bg-red-50/80 dark:bg-red-950/30 hover:bg-red-100 dark:hover:bg-red-900/40 transition border border-red-100 dark:border-red-900/40 cursor-pointer disabled:opacity-60"
            :class="sidebarCollapsed ? 'p-2.5' : 'gap-2 px-3 py-2.5'"
            :title="sidebarCollapsed ? t('Sign out') : undefined"
            @click="signOut"
          >
            <LogOut class="w-3.5 h-3.5" />
            <span v-if="!sidebarCollapsed">{{ busy ? t('Signing out...') : t('Sign out') }}</span>
          </button>
        </div>
      </aside>

      <!-- RIGHT MAIN CONTENT AREA -->
      <div class="flex-1 min-w-0 flex flex-col h-full overflow-y-auto courses-hero">
        <!-- Header Bar: Title on Left, Controls & Cat Theme Switch on Right -->
        <header class="px-6 sm:px-8 pt-6 pb-2 flex flex-col sm:flex-row sm:items-center justify-between shrink-0 bg-transparent gap-4">
          <div class="flex items-center gap-3">
            <h1
              class="text-xl sm:text-2xl font-extrabold text-navy-900 dark:text-white tracking-tight u040-main-title"
              :class="{ 'swap': isTitleSwapping }"
            >
              {{ t(currentSection.title) }}
            </h1>
          </div>

          <div class="flex items-center gap-3">
            <!-- Pill Search on Far Right for Courses & Schedules -->
            <div v-if="activeSection === 'courses'" class="relative w-full sm:w-72 lg:w-80">
              <Search class="w-4 h-4 text-slate-400 dark:text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2 pointer-events-none" />
              <input
                v-model="courseSearch"
                type="text"
                role="searchbox"
                enterkeyhint="search"
                class="w-full pl-10 pr-9 py-2 text-xs rounded-full border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white placeholder-slate-400 dark:placeholder-slate-500 shadow-2xs focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500 transition-all"
                :placeholder="t('Search...')"
                :aria-label="t('Search courses by title, category, slug, or status')"
              />
              <button
                v-if="courseSearch"
                type="button"
                class="absolute right-3 top-1/2 -translate-y-1/2 p-0.5 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                :aria-label="t('Clear search')"
                @click="courseSearch = ''"
              >
                <X class="w-3.5 h-3.5" />
              </button>
            </div>

            <!-- Language Switcher in Header -->
            <div class="hidden sm:flex items-center gap-0.5 rounded-xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-0.5 shadow-2xs">
              <button
                type="button"
                @click="setLocale('en')"
                class="px-2 py-0.5 rounded-lg text-xs font-bold transition-all cursor-pointer"
                :class="locale === 'en'
                  ? 'bg-navy-900 dark:bg-indigo-600 text-white shadow-2xs font-extrabold'
                  : 'text-slate-500 dark:text-slate-400 hover:text-navy-900 dark:hover:text-white'"
              >
                EN
              </button>
              <button
                type="button"
                @click="setLocale('kh')"
                class="px-2 py-0.5 rounded-lg text-xs font-bold transition-all cursor-pointer"
                :class="locale === 'kh'
                  ? 'bg-navy-900 dark:bg-indigo-600 text-white shadow-2xs font-extrabold'
                  : 'text-slate-500 dark:text-slate-400 hover:text-navy-900 dark:hover:text-white'"
              >
                KH
              </button>
            </div>

            <!-- Animated Cat Light/Dark Switch in Header -->
            <div class="hidden sm:flex items-center pl-1">
              <CatThemeSwitch />
            </div>
          </div>
        </header>

        <!-- Main Body Content (Full Width) -->
        <main class="flex-1 p-4 sm:p-6 lg:px-8 lg:pt-4 lg:pb-6 w-full space-y-6">
          <p v-if="errorMessage" class="rounded-xl bg-red-50 dark:bg-red-950/40 p-4 text-xs font-semibold text-red-700 dark:text-red-300 border border-red-200 dark:border-red-900/40" role="alert">{{ errorMessage }}</p>
          <p v-if="successMessage && activeSection !== 'courses'" class="rounded-xl bg-emerald-50 dark:bg-emerald-950/40 p-4 text-xs font-semibold text-emerald-800 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800" role="status">{{ successMessage }}</p>

        <section v-if="activeSection === 'dashboard'" class="w-full pb-8">
          <div class="mb-6 grid gap-4 sm:grid-cols-2 xl:grid-cols-4 w-full">
            <article class="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm">
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400">{{ t('Total revenue') }}</p>
              <p class="mt-2 text-3xl font-extrabold text-navy-900 dark:text-white">${{ Number(overview.total_revenue || 0).toFixed(2) }}</p>
            </article>
            <article class="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm">
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400">{{ t('Active enrollments') }}</p>
              <p class="mt-2 text-3xl font-extrabold text-navy-900 dark:text-white">{{ overview.active_enrollments || 0 }}</p>
            </article>
            <article class="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm">
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400">{{ t('Pending QR scans') }}</p>
              <p class="mt-2 text-3xl font-extrabold text-navy-900 dark:text-white">{{ overview.pending_qr_scans || 0 }}</p>
            </article>
            <article class="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm">
              <p class="text-sm font-medium text-slate-500 dark:text-slate-400">{{ t('Published courses') }}</p>
              <p class="mt-2 text-3xl font-extrabold text-navy-900 dark:text-white">{{ overview.published_courses || 0 }}</p>
            </article>
          </div>

          <!-- Interactive Analytics & Graph Section (Replaces redundant nav cards) -->
          <div class="grid gap-6 lg:grid-cols-12 mb-6 w-full">
            <!-- Left Chart: Revenue & Enrollment Growth Trends (8 Cols) -->
            <article class="lg:col-span-8 rounded-2xl border border-slate-200 bg-white p-5 sm:p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900 flex flex-col justify-between">
              <!-- Chart Header -->
              <div class="flex flex-wrap items-center justify-between gap-3 pb-4 border-b border-slate-100 dark:border-slate-800">
                <div>
                  <div class="flex items-center gap-2">
                    <span class="p-1.5 rounded-lg bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-indigo-400">
                      <TrendingUp class="w-4 h-4" />
                    </span>
                    <h2 class="text-base font-extrabold text-navy-900 dark:text-white">{{ t('Revenue & Enrollment Trends') }}</h2>
                  </div>
                  <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">
                    {{ t('Monthly financial growth and registered student volume over time.') }}
                  </p>
                </div>

                <!-- Metric Toggle Pills -->
                <div class="flex items-center gap-1.5 rounded-xl bg-slate-100 dark:bg-slate-800 p-1 text-xs font-semibold">
                  <button
                    type="button"
                    class="px-3 py-1.5 rounded-lg transition"
                    :class="chartMetric === 'revenue' ? 'bg-white dark:bg-slate-700 text-navy-900 dark:text-white shadow-xs font-bold' : 'text-slate-500 dark:text-slate-400 hover:text-navy-900 dark:hover:text-white'"
                    @click="chartMetric = 'revenue'"
                  >
                    {{ t('Revenue ($)') }}
                  </button>
                  <button
                    type="button"
                    class="px-3 py-1.5 rounded-lg transition"
                    :class="chartMetric === 'students' ? 'bg-white dark:bg-slate-700 text-navy-900 dark:text-white shadow-xs font-bold' : 'text-slate-500 dark:text-slate-400 hover:text-navy-900 dark:hover:text-white'"
                    @click="chartMetric = 'students'"
                  >
                    {{ t('Enrollments') }}
                  </button>
                </div>
              </div>

              <!-- Key Summary Badges above chart -->
              <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 my-4">
                <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800">
                  <span class="text-[11px] font-semibold text-slate-500 dark:text-slate-400">{{ t('Current Month Revenue') }}</span>
                  <div class="mt-1 flex items-baseline gap-2">
                    <span class="text-xl font-extrabold text-navy-900 dark:text-white">${{ (monthlyChartData[monthlyChartData.length - 1]?.revenue || 0).toFixed(2) }}</span>
                    <span class="inline-flex items-center text-[10px] font-bold text-emerald-600 dark:text-emerald-400">
                      <ArrowUpRight class="w-3 h-3" /> +18.4%
                    </span>
                  </div>
                </div>
                <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800">
                  <span class="text-[11px] font-semibold text-slate-500 dark:text-slate-400">{{ t('Monthly Growth Rate') }}</span>
                  <div class="mt-1 flex items-baseline gap-2">
                    <span class="text-xl font-extrabold text-navy-900 dark:text-white">+24.5%</span>
                    <span class="text-[10px] font-semibold text-slate-400">{{ t('vs Q2 avg') }}</span>
                  </div>
                </div>
                <div class="col-span-2 sm:col-span-1 p-3 rounded-xl bg-slate-50 dark:bg-slate-800/60 border border-slate-100 dark:border-slate-800">
                  <span class="text-[11px] font-semibold text-slate-500 dark:text-slate-400">{{ t('Avg Order Value') }}</span>
                  <div class="mt-1 flex items-baseline gap-2">
                    <span class="text-xl font-extrabold text-navy-900 dark:text-white">$110.00</span>
                    <span class="text-[10px] font-semibold text-slate-400">{{ t('/ student') }}</span>
                  </div>
                </div>
              </div>

              <!-- SVG Interactive Curve Chart -->
              <div class="relative w-full pt-2">
                <svg viewBox="0 0 650 220" class="w-full h-56 sm:h-64 overflow-visible select-none" preserveAspectRatio="none">
                  <defs>
                    <linearGradient id="revenueGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stop-color="#4f46e5" stop-opacity="0.28" />
                      <stop offset="60%" stop-color="#4f46e5" stop-opacity="0.08" />
                      <stop offset="100%" stop-color="#4f46e5" stop-opacity="0" />
                    </linearGradient>
                    <linearGradient id="studentGradient" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="0%" stop-color="#0284c7" stop-opacity="0.32" />
                      <stop offset="60%" stop-color="#0284c7" stop-opacity="0.10" />
                      <stop offset="100%" stop-color="#0284c7" stop-opacity="0" />
                    </linearGradient>
                  </defs>

                  <!-- Horizontal grid lines -->
                  <g class="stroke-slate-200/80 dark:stroke-slate-700/60" stroke-dasharray="3 3">
                    <line x1="50" y1="20" x2="630" y2="20" />
                    <line x1="50" y1="70" x2="630" y2="70" />
                    <line x1="50" y1="120" x2="630" y2="120" />
                    <line x1="50" y1="170" x2="630" y2="170" />
                  </g>

                  <!-- Y-Axis Labels -->
                  <g class="fill-slate-400 dark:fill-slate-500 text-[10px] font-medium" text-anchor="end">
                    <text x="42" y="24">{{ chartMetric === 'revenue' ? `$${maxChartRevenue}` : maxChartStudents }}</text>
                    <text x="42" y="74">{{ chartMetric === 'revenue' ? `$${Math.round(maxChartRevenue * 0.66)}` : Math.round(maxChartStudents * 0.66) }}</text>
                    <text x="42" y="124">{{ chartMetric === 'revenue' ? `$${Math.round(maxChartRevenue * 0.33)}` : Math.round(maxChartStudents * 0.33) }}</text>
                    <text x="42" y="174">0</text>
                  </g>

                  <!-- Area Path -->
                  <path
                    :d="chartMetric === 'revenue' ? revenueAreaPath : studentsAreaPath"
                    :fill="chartMetric === 'revenue' ? 'url(#revenueGradient)' : 'url(#studentGradient)'"
                    class="transition-all duration-300"
                  />

                  <!-- Smooth Line Path -->
                  <path
                    :d="chartMetric === 'revenue' ? revenueLinePath : studentsLinePath"
                    fill="none"
                    :stroke="chartMetric === 'revenue' ? '#4f46e5' : '#0284c7'"
                    stroke-width="3"
                    stroke-linecap="round"
                    stroke-linejoin="round"
                    class="transition-all duration-300"
                  />

                  <!-- Data Nodes -->
                  <g v-for="pt in chartPoints" :key="pt.index">
                    <!-- Vertical hover line guide -->
                    <line
                      v-if="hoveredPoint?.index === pt.index"
                      :x1="pt.x"
                      y1="20"
                      :x2="pt.x"
                      y2="170"
                      class="stroke-indigo-400/60 dark:stroke-indigo-400/60"
                      stroke-width="1.5"
                      stroke-dasharray="2 2"
                    />

                    <!-- Interactive point circle -->
                    <circle
                      :cx="pt.x"
                      :cy="chartMetric === 'revenue' ? pt.yRevenue : pt.yStudents"
                      :r="hoveredPoint?.index === pt.index ? 6 : 4"
                      :fill="chartMetric === 'revenue' ? '#4f46e5' : '#0284c7'"
                      class="stroke-white dark:stroke-slate-900 transition-all cursor-pointer"
                      :stroke-width="hoveredPoint?.index === pt.index ? 3 : 2"
                      @mouseenter="hoveredPoint = pt"
                      @mouseleave="hoveredPoint = null"
                    />

                    <!-- X-Axis Label -->
                    <text
                      :x="pt.x"
                      y="195"
                      text-anchor="middle"
                      class="fill-slate-500 dark:fill-slate-400 text-[11px] font-semibold cursor-pointer"
                      :class="{ 'fill-navy-900 dark:fill-white font-bold': hoveredPoint?.index === pt.index }"
                      @mouseenter="hoveredPoint = pt"
                      @mouseleave="hoveredPoint = null"
                    >
                      {{ pt.label }}
                    </text>
                  </g>
                </svg>

                <!-- Floating Tooltip Card -->
                <div
                  v-if="hoveredPoint"
                  class="absolute z-20 pointer-events-none rounded-xl border border-slate-200/90 dark:border-slate-700 bg-white/95 dark:bg-slate-800/95 p-3 shadow-lg backdrop-blur-sm -translate-x-1/2 -translate-y-full transition-all duration-150"
                  :style="{
                    left: `${(hoveredPoint.x / 650) * 100}%`,
                    top: `${((chartMetric === 'revenue' ? hoveredPoint.yRevenue : hoveredPoint.yStudents) / 220) * 100}%`,
                    marginTop: '-12px'
                  }"
                >
                  <p class="text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-400">{{ hoveredPoint.fullLabel }}</p>
                  <p class="text-sm font-extrabold text-navy-900 dark:text-white mt-0.5">
                    ${{ hoveredPoint.revenue.toFixed(2) }}
                  </p>
                  <p class="text-[11px] font-semibold text-slate-500 dark:text-slate-300">
                    {{ hoveredPoint.students }} {{ t('enrollments') }}
                  </p>
                </div>
              </div>

              <!-- Chart Footer Legend -->
              <div class="mt-3 pt-3 border-t border-slate-100 dark:border-slate-800 flex flex-wrap items-center justify-between text-xs text-slate-500 dark:text-slate-400">
                <div class="flex items-center gap-4">
                  <span class="inline-flex items-center gap-2">
                    <span class="w-3 h-3 rounded-full bg-indigo-600"></span>
                    <span>{{ t('Revenue Trajectory') }}</span>
                  </span>
                  <span class="inline-flex items-center gap-2">
                    <span class="w-3 h-3 rounded-full bg-sky-500"></span>
                    <span>{{ t('Student Intake Volume') }}</span>
                  </span>
                </div>
                <span class="text-[11px] text-slate-400">{{ t('Real-time sync') }}</span>
              </div>
            </article>

            <!-- Right Chart: Category Distribution & Donut Breakdown (4 Cols) -->
            <article class="lg:col-span-4 rounded-2xl border border-slate-200 bg-white p-5 sm:p-6 shadow-sm dark:border-slate-800 dark:bg-slate-900 flex flex-col justify-between">
              <div>
                <div class="flex items-center justify-between gap-2 pb-3 border-b border-slate-100 dark:border-slate-800">
                  <div class="flex items-center gap-2">
                    <span class="p-1.5 rounded-lg bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-indigo-400">
                      <PieChart class="w-4 h-4" />
                    </span>
                    <h2 class="text-base font-extrabold text-navy-900 dark:text-white">{{ t('Course Categories') }}</h2>
                  </div>
                  <span class="text-xs font-bold text-slate-400">{{ categoryDistribution.total }} {{ t('courses') }}</span>
                </div>

                <!-- Donut Chart Container -->
                <div class="relative my-4 flex items-center justify-center">
                  <svg viewBox="0 0 120 120" class="w-40 h-40 transform -rotate-90">
                    <!-- Base background circle -->
                    <circle
                      cx="60"
                      cy="60"
                      r="46"
                      fill="none"
                      class="stroke-slate-100 dark:stroke-slate-800"
                      stroke-width="12"
                    />
                    <!-- Slices -->
                    <circle
                      v-for="slice in categoryDistribution.slices"
                      :key="slice.name"
                      cx="60"
                      cy="60"
                      r="46"
                      fill="none"
                      :stroke="slice.color"
                      stroke-width="12"
                      :stroke-dasharray="slice.dashArray"
                      :stroke-dashoffset="slice.dashOffset"
                      stroke-linecap="round"
                      class="transition-all duration-500"
                    />
                  </svg>

                  <!-- Center Text inside Donut -->
                  <div class="absolute inset-0 flex flex-col items-center justify-center text-center pointer-events-none">
                    <span class="text-2xl font-extrabold text-navy-900 dark:text-white leading-none">
                      {{ categoryDistribution.total }}
                    </span>
                    <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400 mt-1">
                      {{ t('Total') }}
                    </span>
                  </div>
                </div>

                <!-- Category Breakdown Progress Bars -->
                <div class="space-y-2.5 mt-2">
                  <div
                    v-for="cat in categoryDistribution.categories"
                    :key="cat.name"
                    class="space-y-1"
                  >
                    <div class="flex items-center justify-between text-xs">
                      <div class="flex items-center gap-2">
                        <span class="w-2 h-2 rounded-full shrink-0" :style="{ backgroundColor: cat.color }"></span>
                        <span class="font-bold text-slate-700 dark:text-slate-300">{{ t(cat.name) }}</span>
                      </div>
                      <div class="flex items-center gap-2 text-slate-500 dark:text-slate-400 font-semibold">
                        <span>{{ cat.count }}</span>
                        <span class="text-[10px] text-slate-400">({{ cat.percent }}%)</span>
                      </div>
                    </div>
                    <div class="h-1.5 w-full rounded-full bg-slate-100 dark:bg-slate-800 overflow-hidden">
                      <div
                        class="h-full rounded-full transition-all duration-500"
                        :style="{ width: `${cat.percent}%`, backgroundColor: cat.color }"
                      ></div>
                    </div>
                  </div>
                </div>
              </div>

              <!-- Category Card Footer -->
              <div class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
                <span class="text-[11px]">{{ t('Hardware & Software Labs') }}</span>
                <button
                  type="button"
                  class="font-bold text-navy-800 dark:text-indigo-400 hover:underline cursor-pointer"
                  @click="selectSection('courses')"
                >
                  {{ t('Manage courses') }} &rarr;
                </button>
              </div>
            </article>
          </div>
          <div class="mt-6 grid gap-5 lg:grid-cols-3">
            <article class="flex flex-col h-80 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm">
              <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800 shrink-0">
                <h2 class="text-base font-extrabold text-navy-900 dark:text-white">{{ t('Recent enrollments') }}</h2>
                <span class="text-xs font-semibold text-slate-400 dark:text-slate-500">{{ (overview.recent_enrollments || []).length }}</span>
              </div>
              <div class="mt-2 flex-1 overflow-y-auto pr-1 divide-y divide-slate-100 dark:divide-slate-800 admin-scroll-box">
                <p v-for="student in overview.recent_enrollments || []" :key="student.enrollment_id" class="flex justify-between items-center gap-3 py-2 text-sm">
                  <span class="truncate font-medium text-slate-800 dark:text-slate-200" :title="`${student.student_name} · ${student.course_title}`">{{ student.student_name }} · {{ student.course_title }}</span>
                  <span class="shrink-0 text-xs font-semibold px-2 py-0.5 rounded" :class="student.status === 'paid' ? 'bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300' : 'bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400'">{{ t(student.status) }}</span>
                </p>
                <p v-if="!overview.recent_enrollments?.length" class="py-6 text-center text-sm text-slate-500 dark:text-slate-400">{{ t('No enrollments yet.') }}</p>
              </div>
            </article>
            <article class="flex flex-col h-80 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm">
              <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800 shrink-0">
                <h2 class="text-base font-extrabold text-navy-900 dark:text-white">{{ t('Top selling courses') }}</h2>
                <span class="text-xs font-semibold text-slate-400 dark:text-slate-500">{{ (overview.top_courses || []).length }}</span>
              </div>
              <div class="mt-2 flex-1 overflow-y-auto pr-1 admin-scroll-box">
                <ol class="space-y-3 py-1">
                  <li v-for="(course, index) in overview.top_courses || []" :key="course.title" class="flex items-center justify-between text-sm">
                    <span class="truncate font-medium text-slate-700 dark:text-slate-200 pr-2" :title="course.title">{{ index + 1 }}. {{ course.title }}</span>
                    <span class="shrink-0 text-xs font-medium text-slate-500 dark:text-slate-400">{{ course.enrollments }} {{ t('enrollments') }}</span>
                  </li>
                  <li v-if="!overview.top_courses?.length" class="py-6 text-center text-sm text-slate-500 dark:text-slate-400">{{ t('No enrollment data yet.') }}</li>
                </ol>
              </div>
            </article>
            <article class="flex flex-col h-80 rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-sm">
              <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800 shrink-0">
                <h2 class="text-base font-extrabold text-navy-900 dark:text-white">{{ t('Activity Feed') }}</h2>
                <span class="text-xs font-semibold text-slate-400 dark:text-slate-500">{{ (overview.activity || []).length }}</span>
              </div>
              <div class="mt-2 flex-1 overflow-y-auto pr-1 admin-scroll-box">
                <div class="space-y-3 py-1">
                  <div v-for="(event, index) in overview.activity || []" :key="`${event.created_at}-${index}`" class="border-l-2 border-navy-200 dark:border-indigo-500/60 pl-3">
                    <p class="text-sm font-semibold text-slate-800 dark:text-slate-200">{{ t(event.action) }}</p>
                    <p class="text-xs text-slate-500 dark:text-slate-400">{{ event.details }}</p>
                    <p class="text-[10px] text-slate-400 dark:text-slate-500">{{ formatCambodiaTime(event.created_at) }}</p>
                  </div>
                  <p v-if="!overview.activity?.length" class="py-6 text-center text-sm text-slate-500 dark:text-slate-400">{{ t('No recent activity.') }}</p>
                </div>
              </div>
            </article>
          </div>
        </section>

        <section v-else-if="activeSection === 'students'" class="w-full pb-8">
          <div class="overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-card">
            <div class="flex flex-wrap items-center justify-between gap-4 border-b border-slate-100 dark:border-slate-800 p-5">
              <div><h2 class="text-lg font-extrabold text-navy-900 dark:text-white">{{ t('Student enrollments') }}</h2><p class="mt-1 text-sm text-slate-500 dark:text-slate-400">{{ enrollments.length }} {{ t('records') }}</p></div>
              <div class="flex items-center gap-2.5">
                <input v-model.trim="studentSearch" class="admin-input w-48 sm:w-64 max-w-xs" :placeholder="t('Search students')" :aria-label="t('Search students')" />
                <button
                  type="button"
                  class="inline-flex items-center gap-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2 text-xs sm:text-sm font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 hover:border-slate-400 dark:hover:border-slate-600 transition cursor-pointer shadow-2xs whitespace-nowrap shrink-0"
                  @click="exportRoster"
                >
                  <FileSpreadsheet class="w-4 h-4 text-emerald-600 dark:text-emerald-400 shrink-0" />
                  <span class="whitespace-nowrap">{{ t('Export roster Excel') }}</span>
                </button>
              </div>
            </div>
            <div class="overflow-x-auto max-h-[580px] overflow-y-auto admin-scroll-box">
              <table class="min-w-full divide-y divide-slate-100 dark:divide-slate-800 text-left text-sm">
                <thead class="sticky top-0 z-10 bg-slate-50/95 dark:bg-slate-800/95 backdrop-blur-xs text-xs uppercase text-slate-500 dark:text-slate-400 shadow-2xs">
                  <tr>
                    <th class="px-4 py-3">{{ t('Student') }}</th>
                    <th class="px-4 py-3">{{ t('Education') }}</th>
                    <th class="px-4 py-3">{{ t('Course & schedule') }}</th>
                    <th class="px-4 py-3">{{ t('Status') }}</th>
                    <th class="px-4 py-3 text-right">{{ t('Actions') }}</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
                  <tr
                    v-for="record in paginatedEnrollments"
                    :key="record.enrollment_id"
                    class="hover:bg-slate-50/70 dark:hover:bg-slate-800/40 transition"
                  >
                    <td class="px-4 py-3">
                      <p class="font-bold text-slate-800 dark:text-white">{{ record.student_name }}</p>
                      <p class="text-xs text-slate-500 dark:text-slate-400">{{ record.email }} · {{ record.phone_number || record.phone_telegram }}</p>
                      <p class="text-xs text-slate-500 dark:text-slate-400">{{ record.gender }} · {{ record.age_range }}</p>
                    </td>
                    <td class="px-4 py-3 text-slate-600 dark:text-slate-300">
                      {{ record.highest_qualification }}
                      <p class="text-xs text-slate-400 dark:text-slate-500">{{ record.current_occupation }}</p>
                    </td>
                    <td class="px-4 py-3 text-slate-600 dark:text-slate-300">
                      {{ record.course_title }}
                      <p class="text-xs text-slate-400 dark:text-slate-500">{{ record.preferred_schedule }} · {{ record.preferred_start_date }}</p>
                    </td>
                    <td class="px-4 py-3 min-w-[140px]">
                      <CustomSelect
                        size="sm"
                        :model-value="record.enrollment_status"
                        :options="[
                          { value: 'pending', label: t('pending') },
                          { value: 'confirmed', label: t('confirmed') },
                          { value: 'cancelled', label: t('cancelled') }
                        ]"
                        :trigger-class="record.enrollment_status === 'confirmed' ? 'border-emerald-300 bg-emerald-50 text-emerald-800 font-bold dark:bg-emerald-950/60 dark:text-emerald-300 dark:border-emerald-700' : record.enrollment_status === 'cancelled' ? 'border-red-300 bg-red-50 text-red-800 font-bold dark:bg-red-950/60 dark:text-red-300 dark:border-red-700' : 'border-amber-300 bg-amber-50 text-amber-800 font-bold dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-700'"
                        @change="changeEnrollmentStatus(record, $event)"
                      />
                    </td>
                    <td class="px-4 py-3 text-right">
                      <button
                        type="button"
                        class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold bg-sky-50 dark:bg-slate-800 text-navy-800 dark:text-sky-300 hover:bg-sky-100 dark:hover:bg-slate-700 transition border border-sky-200/70 dark:border-slate-700 shadow-2xs cursor-pointer whitespace-nowrap"
                        @click="showStudentDetails(record)"
                      >
                        {{ t('View details') }}
                      </button>
                    </td>
                  </tr>
                  <tr v-if="!filteredEnrollments.length">
                    <td colspan="5" class="px-4 py-10 text-center text-slate-500 dark:text-slate-400">
                      {{ t('No matching enrollments.') }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
            <!-- Pagination Bar matching wireframe -->
            <div class="p-3 sm:p-4 border-t border-slate-100 dark:border-slate-800">
              <AdminPagination
                v-model:current-page="studentPage"
                :total-pages="totalStudentPages"
                :total-items="filteredEnrollments.length"
                :page-size="studentPerPage"
              />
            </div>
          </div>

          <!-- Student Details Interactive Modal Dialog -->
          <div
            v-if="selectedStudent"
            class="fixed inset-0 z-[70] flex items-center justify-center p-3 sm:p-5 bg-slate-950/60 backdrop-blur-xs transition-opacity"
            @click.self="selectedStudent = null"
          >
            <div
              role="dialog"
              aria-modal="true"
              :aria-label="t('Student details')"
              class="w-full max-w-2xl max-h-[92vh] flex flex-col rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150 my-auto"
            >
              <!-- Modal Sticky Header -->
              <div class="flex items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-800 p-4 sm:p-5 bg-slate-50/80 dark:bg-slate-800/60 shrink-0">
                <div class="flex items-center gap-3 min-w-0">
                  <div class="w-11 h-11 rounded-xl bg-gradient-to-br from-navy-800 to-[#1e3a61] text-white font-black flex items-center justify-center shrink-0 text-sm shadow-xs">
                    {{ (selectedStudent.student_name || 'S').slice(0, 2).toUpperCase() }}
                  </div>
                  <div class="min-w-0">
                    <h3 class="font-extrabold text-navy-900 dark:text-white text-base sm:text-lg truncate">
                      {{ selectedStudent.student_name }}
                    </h3>
                    <div class="flex flex-wrap items-center gap-1.5 sm:gap-2 mt-0.5 text-xs text-slate-500 dark:text-slate-400">
                      <span class="font-mono text-slate-700 dark:text-slate-300 font-semibold">{{ selectedStudent.enrollment_id }}</span>
                      <span>&bull;</span>
                      <span
                        class="inline-flex items-center px-2 py-0.5 rounded-md font-bold text-[11px]"
                        :class="selectedStudent.enrollment_status === 'confirmed' ? 'bg-emerald-100 text-emerald-800 dark:bg-emerald-950/70 dark:text-emerald-300' : selectedStudent.enrollment_status === 'cancelled' ? 'bg-red-100 text-red-800 dark:bg-red-950/70 dark:text-red-300' : 'bg-amber-100 text-amber-800 dark:bg-amber-950/70 dark:text-amber-300'"
                      >
                        {{ t(selectedStudent.enrollment_status) }}
                      </span>
                      <span>&bull;</span>
                      <span
                        class="inline-flex items-center px-2 py-0.5 rounded-md font-semibold text-[11px]"
                        :class="selectedStudent.status === 'paid' ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/50 dark:text-emerald-400' : selectedStudent.status === 'expired' ? 'bg-red-50 text-red-700 dark:bg-red-950/50 dark:text-red-400' : 'bg-amber-50 text-amber-700 dark:bg-amber-950/50 dark:text-amber-400'"
                      >
                        {{ t('Payment') }}: {{ t(selectedStudent.status) }}
                      </span>
                    </div>
                  </div>
                </div>

                <button
                  type="button"
                  class="rounded-xl p-2 text-slate-400 hover:text-slate-700 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition cursor-pointer"
                  @click="selectedStudent = null"
                  :aria-label="t('Close')"
                >
                  <X class="w-5 h-5" />
                </button>
              </div>

              <!-- Quick Action Bar -->
              <div class="flex flex-wrap items-center justify-between gap-2.5 px-4 sm:px-5 py-2.5 bg-sky-50/60 dark:bg-slate-800/40 border-b border-slate-100 dark:border-slate-800 shrink-0">
                <div class="flex items-center gap-2">
                  <button
                    v-if="selectedStudent.enrollment_status !== 'confirmed'"
                    type="button"
                    class="rounded-lg bg-emerald-600 px-3.5 py-1.5 text-xs font-bold text-white hover:bg-emerald-700 shadow-xs transition cursor-pointer inline-flex items-center gap-1.5"
                    @click="changeEnrollmentStatus(selectedStudent, 'confirmed')"
                  >
                    ✓ {{ t('Confirm enrollment & payment') }}
                  </button>
                  <span
                    v-else
                    class="rounded-lg bg-emerald-100 dark:bg-emerald-950/60 dark:border dark:border-emerald-700 px-3 py-1.5 text-xs font-bold text-emerald-800 dark:text-emerald-300 inline-flex items-center gap-1.5"
                  >
                    ✓ {{ t('Confirmed & Paid') }}
                  </span>
                </div>

                <div class="flex items-center gap-2">
                  <button
                    type="button"
                    class="inline-flex items-center gap-1.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-1.5 text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 transition shadow-2xs cursor-pointer"
                    @click="copyStudentContact(selectedStudent)"
                  >
                    <component :is="copiedStudentInfo ? Check : Copy" class="w-3.5 h-3.5 text-slate-600 dark:text-slate-300" />
                    <span>{{ copiedStudentInfo ? t('Copied!') : t('Copy contact') }}</span>
                  </button>
                  <a
                    :href="`/payment/success/${selectedStudent.enrollment_id}`"
                    target="_blank"
                    rel="noopener"
                    class="inline-flex items-center gap-1.5 rounded-lg border border-sky-300 dark:border-sky-800 bg-sky-50 dark:bg-sky-950/50 px-3 py-1.5 text-xs font-semibold text-sky-800 dark:text-sky-300 hover:bg-sky-100 dark:hover:bg-sky-900/60 transition shadow-2xs"
                  >
                    <ExternalLink class="w-3.5 h-3.5" />
                    <span>{{ t('View / Print Receipt') }}</span>
                  </a>
                </div>
              </div>

              <!-- Modal Scrollable Content with internal smooth scroll -->
              <div class="flex-1 overflow-y-auto p-4 sm:p-5 admin-scroll-box space-y-4">
                <!-- Group 1: Enrolled Course & Schedule -->
                <div class="rounded-xl border border-sky-100 dark:border-slate-800 bg-sky-50/30 dark:bg-slate-800/30 p-3.5 sm:p-4 space-y-2">
                  <div class="flex items-center justify-between">
                    <p class="text-xs font-bold uppercase tracking-wider text-navy-900 dark:text-sky-300">
                      {{ t('Course & schedule') }}
                    </p>
                    <span v-if="selectedStudent.amount_due" class="text-xs font-black text-navy-900 dark:text-white">
                      {{ t('Tuition') }}: ${{ Number(selectedStudent.amount_due).toFixed(2) }}
                    </span>
                  </div>
                  <div class="grid gap-2 sm:grid-cols-2 text-xs">
                    <div>
                      <span class="text-slate-400 dark:text-slate-500 font-medium">{{ t('Course') }}:</span>
                      <p class="font-bold text-slate-800 dark:text-white mt-0.5">{{ selectedStudent.course_title }}</p>
                    </div>
                    <div>
                      <span class="text-slate-400 dark:text-slate-500 font-medium">{{ t('Schedule & shift') }}:</span>
                      <p class="font-semibold text-slate-800 dark:text-white mt-0.5">{{ selectedStudent.preferred_schedule }} &bull; {{ selectedStudent.time_slot || t('Shift 1') }}</p>
                    </div>
                    <div>
                      <span class="text-slate-400 dark:text-slate-500 font-medium">{{ t('Start Date') }}:</span>
                      <p class="font-semibold text-slate-800 dark:text-slate-200 mt-0.5">{{ selectedStudent.preferred_start_date || t('Upcoming Batch') }}</p>
                    </div>
                    <div v-if="selectedStudent.transaction_id">
                      <span class="text-slate-400 dark:text-slate-500 font-medium">{{ t('Transaction') }}:</span>
                      <p class="font-mono font-semibold text-slate-800 dark:text-slate-200 mt-0.5">{{ selectedStudent.transaction_id }}</p>
                    </div>
                  </div>
                </div>

                <!-- Group 2: Personal & Contact Information -->
                <div class="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-3.5 sm:p-4 space-y-2">
                  <p class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                    {{ t('Personal & Contact Information') }}
                  </p>
                  <dl class="grid gap-3 text-xs sm:grid-cols-2">
                    <div>
                      <dt class="font-medium text-slate-400 dark:text-slate-500">{{ t('Email') }}</dt>
                      <dd class="mt-0.5 font-semibold text-slate-800 dark:text-slate-200">{{ selectedStudent.email || '—' }}</dd>
                    </div>
                    <div>
                      <dt class="font-medium text-slate-400 dark:text-slate-500">{{ t('Phone Number') }}</dt>
                      <dd class="mt-0.5 font-semibold text-slate-800 dark:text-slate-200">{{ selectedStudent.phone_number || selectedStudent.phone_telegram || '—' }}</dd>
                    </div>
                    <div>
                      <dt class="font-medium text-slate-400 dark:text-slate-500">{{ t('Telegram username') }}</dt>
                      <dd class="mt-0.5 font-semibold text-slate-800 dark:text-slate-200">{{ selectedStudent.phone_telegram || '—' }}</dd>
                    </div>
                    <div>
                      <dt class="font-medium text-slate-400 dark:text-slate-500">{{ t('Gender') }} · {{ t('Age Range') }}</dt>
                      <dd class="mt-0.5 font-semibold text-slate-800 dark:text-slate-200">{{ selectedStudent.gender || '—' }} · {{ selectedStudent.age_range || '—' }}</dd>
                    </div>
                    <div>
                      <dt class="font-medium text-slate-400 dark:text-slate-500">{{ t('Date of birth') }}</dt>
                      <dd class="mt-0.5 font-semibold text-slate-800 dark:text-slate-200">{{ selectedStudent.date_of_birth || '—' }}</dd>
                    </div>
                    <div class="sm:col-span-2">
                      <dt class="font-medium text-slate-400 dark:text-slate-500">{{ t('Address') }}</dt>
                      <dd class="mt-0.5 font-semibold text-slate-800 dark:text-slate-200">{{ selectedStudent.address || '—' }}</dd>
                    </div>
                  </dl>
                </div>

                <!-- Group 3: Education & Experience -->
                <div class="rounded-xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-3.5 sm:p-4 space-y-2">
                  <p class="text-xs font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                    {{ t('Education & Background') }}
                  </p>
                  <dl class="grid gap-3 text-xs sm:grid-cols-2">
                    <div>
                      <dt class="font-medium text-slate-400 dark:text-slate-500">{{ t('Highest Qualification') }}</dt>
                      <dd class="mt-0.5 font-semibold text-slate-800 dark:text-slate-200">{{ selectedStudent.highest_qualification || '—' }}</dd>
                    </div>
                    <div>
                      <dt class="font-medium text-slate-400 dark:text-slate-500">{{ t('Current Occupation / School') }}</dt>
                      <dd class="mt-0.5 font-semibold text-slate-800 dark:text-slate-200">{{ selectedStudent.current_occupation || '—' }}</dd>
                    </div>
                    <div class="sm:col-span-2">
                      <dt class="font-medium text-slate-400 dark:text-slate-500">{{ t('Previous Robotics / Coding Experience') }}</dt>
                      <dd class="mt-0.5 whitespace-pre-wrap text-slate-800 dark:text-slate-200">{{ selectedStudent.coding_experience || '—' }}</dd>
                    </div>
                    <div v-if="selectedStudent.special_requirements" class="sm:col-span-2">
                      <dt class="font-medium text-slate-400 dark:text-slate-500">{{ t('Special Requirements or Notes') }}</dt>
                      <dd class="mt-0.5 whitespace-pre-wrap text-slate-800 dark:text-slate-200">{{ selectedStudent.special_requirements }}</dd>
                    </div>
                  </dl>
                </div>
              </div>

              <!-- Modal Footer -->
              <div class="border-t border-slate-100 dark:border-slate-800 p-3.5 sm:p-4 bg-slate-50/70 dark:bg-slate-800/60 flex items-center justify-between gap-3 shrink-0">
                <span class="text-[11px] text-slate-400 dark:text-slate-500">
                  <span v-if="selectedStudent.created_at">{{ formatCambodiaTime(selectedStudent.created_at) }}</span>
                </span>
                <button
                  type="button"
                  class="rounded-lg bg-slate-200 dark:bg-slate-700 px-4 py-2 text-xs font-bold text-slate-800 dark:text-slate-200 hover:bg-slate-300 dark:hover:bg-slate-600 transition cursor-pointer"
                  @click="selectedStudent = null"
                >
                  {{ t('Close') }}
                </button>
              </div>
            </div>
          </div>
        </section>

        <section v-else-if="activeSection === 'payments'" class="w-full pb-8">
          <div class="overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-card">
            <div class="border-b border-slate-100 dark:border-slate-800 p-5"><h2 class="text-lg font-extrabold text-navy-900 dark:text-white">{{ t('Payments & QR Checkout') }}</h2><p class="mt-1 text-sm text-slate-500 dark:text-slate-400">{{ t('Manual status changes should only be made after checking your payment provider.') }}</p></div>
            <div class="overflow-x-auto"><table class="min-w-full divide-y divide-slate-100 dark:divide-slate-800 text-left text-sm">
              <thead class="bg-slate-50 dark:bg-slate-800/80 text-xs uppercase text-slate-500 dark:text-slate-400"><tr><th class="px-4 py-3">{{ t('Transaction') }}</th><th class="px-4 py-3">{{ t('Student / course') }}</th><th class="px-4 py-3">{{ t('Log fields') }}</th><th class="px-4 py-3">{{ t('Subtotal / discount / final') }}</th><th class="px-4 py-3">{{ t('Status') }}</th></tr></thead>
              <tbody class="divide-y divide-slate-100 dark:divide-slate-800"><tr v-for="payment in paginatedPayments" :key="payment.transaction_id">
                <td class="px-4 py-3 font-mono text-xs text-slate-800 dark:text-slate-200">{{ payment.transaction_id }}<p class="mt-1 text-slate-500 dark:text-slate-400">{{ formatCambodiaTime(payment.created_at) }}</p></td>
                <td class="px-4 py-3 font-semibold text-slate-900 dark:text-white">{{ payment.student_name }}<p class="text-xs font-normal text-slate-500 dark:text-slate-400">{{ payment.course_title }}</p></td>
                <td class="px-4 py-3 text-xs text-slate-600 dark:text-slate-300">{{ payment.email }}<p>{{ payment.enrollment_id }}</p><p v-if="payment.coupon_code">{{ t('Coupon') }}: {{ payment.coupon_code }}</p><div class="mt-2 border-l border-slate-200 dark:border-slate-700 pl-2"><p v-for="(event, index) in payment.payment_history || []" :key="`${event.created_at}-${index}`" class="mt-1">{{ t(event.status) }} · {{ formatCambodiaTime(event.created_at) }}</p></div></td>
                <td class="px-4 py-3 text-slate-800 dark:text-slate-200">${{ Number(payment.original_price).toFixed(2) }} / -${{ Number(payment.discount_amount).toFixed(2) }} / <strong>${{ Number(payment.amount_due).toFixed(2) }}</strong><p class="mt-0.5 text-[11px] text-slate-400 dark:text-slate-400 font-normal">{{ t('Fees') }}: +${{ (Number(payment.administration_fee || 7.5) + Number(payment.certification_fee || 5) + Number(payment.card_fee || 2.5)).toFixed(2) }}</p></td>
                <td class="px-4 py-3 min-w-[140px]">
                  <CustomSelect
                    size="sm"
                    :model-value="payment.status"
                    :options="[
                      { value: 'pending', label: t('Pending Scan') },
                      { value: 'paid', label: t('Paid') },
                      { value: 'expired', label: t('Expired') },
                      { value: 'refunded', label: t('Refunded') }
                    ]"
                    :trigger-class="payment.status === 'paid' ? 'border-emerald-300 bg-emerald-50 text-emerald-800 font-bold dark:bg-emerald-950/60 dark:text-emerald-300 dark:border-emerald-700' : payment.status === 'expired' ? 'border-red-300 bg-red-50 text-red-800 font-bold dark:bg-red-950/60 dark:text-red-300 dark:border-red-700' : payment.status === 'refunded' ? 'border-purple-300 bg-purple-50 text-purple-800 font-bold dark:bg-purple-950/60 dark:text-purple-300 dark:border-purple-700' : 'border-amber-300 bg-amber-50 text-amber-800 font-bold dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-700'"
                    @change="changePaymentStatus(payment, $event)"
                  />
                </td>
              </tr><tr v-if="!payments.length"><td colspan="5" class="px-4 py-10 text-center text-slate-500 dark:text-slate-400">{{ t('No payments recorded yet.') }}</td></tr></tbody>
            </table></div>
            <!-- Pagination Bar matching wireframe -->
            <div class="p-3 sm:p-4 border-t border-slate-100 dark:border-slate-800">
              <AdminPagination
                v-model:current-page="paymentPage"
                :total-pages="totalPaymentPages"
                :total-items="payments.length"
                :page-size="paymentPerPage"
              />
            </div>
          </div>
        </section>

        <section v-else-if="activeSection === 'promos'" class="w-full grid gap-6 pb-8 lg:grid-cols-[minmax(0,1fr)_minmax(320px,0.75fr)]">
          <div class="overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-card">
            <div class="border-b border-slate-100 dark:border-slate-800 p-5"><h2 class="text-lg font-extrabold text-navy-900 dark:text-white">{{ t('Promo & Coupon Engine') }}</h2></div>
            <div class="overflow-x-auto"><table class="min-w-full divide-y divide-slate-100 dark:divide-slate-800 text-left text-sm"><thead class="bg-slate-50 dark:bg-slate-800/80 text-xs uppercase text-slate-500 dark:text-slate-400"><tr><th class="px-4 py-3">{{ t('Code') }}</th><th class="px-4 py-3">{{ t('Discount') }}</th><th class="px-4 py-3">{{ t('Usage / expiry') }}</th><th class="px-4 py-3">{{ t('Status') }}</th><th class="px-4 py-3"></th></tr></thead><tbody class="divide-y divide-slate-100 dark:divide-slate-800"><tr v-for="coupon in paginatedCoupons" :key="coupon.code"><td class="px-4 py-3 font-mono font-bold text-slate-900 dark:text-white">{{ coupon.code }}</td><td class="px-4 py-3 text-slate-800 dark:text-slate-200">{{ coupon.discount_type === 'percent' ? `${coupon.value}%` : `$${coupon.value}` }}</td><td class="px-4 py-3 text-slate-700 dark:text-slate-300">{{ coupon.usage_count }} / {{ coupon.max_usage ?? '∞' }}<p class="text-xs text-slate-500 dark:text-slate-400">{{ coupon.expires_at || t('No expiry') }}</p></td><td class="px-4 py-3"><button type="button" class="rounded-full px-3 py-1 text-xs font-bold transition" :class="coupon.active ? 'bg-emerald-50 dark:bg-emerald-950/50 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800' : 'bg-slate-100 dark:bg-slate-800 text-slate-500 dark:text-slate-400 border border-slate-200 dark:border-slate-700'" @click="toggleCoupon(coupon)">{{ coupon.active ? t('Active') : t('Inactive') }}</button></td><td class="px-4 py-3"><button type="button" class="text-xs font-semibold text-navy-800 dark:text-indigo-400 hover:underline" @click="editCoupon(coupon)">{{ t('Edit') }}</button><button type="button" class="ml-3 text-xs font-semibold text-red-700 dark:text-red-400 hover:underline" @click="removeCoupon(coupon)">{{ t('Delete') }}</button></td></tr><tr v-if="!coupons.length"><td colspan="5" class="px-4 py-8 text-center text-slate-500 dark:text-slate-400">{{ t('No coupons saved.') }}</td></tr></tbody></table></div>
            <!-- Pagination Bar matching wireframe -->
            <div class="p-3 sm:p-4 border-t border-slate-100 dark:border-slate-800">
              <AdminPagination
                v-model:current-page="couponPage"
                :total-pages="totalCouponPages"
                :total-items="coupons.length"
                :page-size="couponPerPage"
              />
            </div>
          </div>
          <form class="h-fit rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-card" @submit.prevent="saveCoupon">
            <h2 class="text-lg font-extrabold text-navy-900 dark:text-white">{{ editingCoupon ? t('Edit coupon') : t('Create coupon') }}</h2>
            <div class="mt-4 space-y-4">
              <label class="block"><span class="admin-label dark:text-slate-100">{{ t('Code') }}</span><input v-model.trim="couponForm.code" required maxlength="40" class="admin-input uppercase" :disabled="Boolean(editingCoupon)" /></label>
              <div class="block">
                <span class="admin-label dark:text-slate-100">{{ t('Discount type') }}</span>
                <CustomSelect
                  v-model="couponForm.discount_type"
                  :options="[
                    { value: 'percent', label: t('Percent') },
                    { value: 'fixed', label: t('Fixed amount') }
                  ]"
                />
              </div>
              <label class="block"><span class="admin-label dark:text-slate-100">{{ t('Discount value') }}</span><input v-model.number="couponForm.value" type="number" min="0.01" :max="couponForm.discount_type === 'percent' ? 100 : 1000000" step="0.01" required class="admin-input" /></label>
              <label class="block"><span class="admin-label dark:text-slate-100">{{ t('Max usage limit') }}</span><input v-model.number="couponForm.max_usage" type="number" min="1" class="admin-input" :placeholder="t('Unlimited')" /></label>
              <div class="block">
                <span class="admin-label dark:text-slate-100">{{ t('Expiry date') }}</span>
                <DatePicker
                  v-model="couponForm.expires_at"
                  :placeholder="t('Select expiry date (optional)')"
                  :min-year="new Date().getFullYear() - 1"
                  :max-year="new Date().getFullYear() + 10"
                  align="right"
                />
              </div>
              <label class="flex items-center gap-2 text-sm font-semibold text-slate-700 dark:text-slate-200"><input v-model="couponForm.active" type="checkbox" />{{ t('Active') }}</label>
              <p v-if="couponError" role="alert" class="rounded-lg bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900/40 p-3 text-sm text-red-700 dark:text-red-300">{{ couponError }}</p>
              <div class="flex gap-3"><button type="submit" :disabled="busy" class="admin-primary-button">{{ busy ? t('Saving...') : t('Save coupon') }}</button><button v-if="editingCoupon" type="button" class="rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 text-sm font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700" @click="resetCoupon">{{ t('Cancel') }}</button></div>
            </div>
          </form>
        </section>

        <!-- ========================================== -->
        <!-- USER ACCOUNTS SECTION                      -->
        <!-- ========================================== -->
        <section v-else-if="activeSection === 'users'" class="w-full pb-8 space-y-6">
          <!-- Top KPI Stat Cards -->
          <div class="grid grid-cols-2 gap-3 sm:gap-5 lg:grid-cols-4">
            <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 sm:p-5 shadow-xs flex items-center gap-3.5">
              <div class="flex h-11 w-11 sm:h-12 sm:w-12 shrink-0 items-center justify-center rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400">
                <Users class="h-5 w-5 sm:h-6 sm:w-6" />
              </div>
              <div class="min-w-0">
                <p class="text-[11px] sm:text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">{{ t('Total Users') }}</p>
                <p class="text-xl sm:text-2xl font-black text-navy-900 dark:text-white mt-0.5">{{ totalUsersCount.toLocaleString() }}</p>
              </div>
            </div>

            <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 sm:p-5 shadow-xs flex items-center gap-3.5">
              <div class="flex h-11 w-11 sm:h-12 sm:w-12 shrink-0 items-center justify-center rounded-xl bg-sky-50 dark:bg-sky-950/60 text-sky-600 dark:text-sky-400">
                <Mail class="h-5 w-5 sm:h-6 sm:w-6" />
              </div>
              <div class="min-w-0">
                <p class="text-[11px] sm:text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">{{ t('Email / Password Users') }}</p>
                <p class="text-xl sm:text-2xl font-black text-navy-900 dark:text-white mt-0.5">{{ emailUsersCount.toLocaleString() }}</p>
              </div>
            </div>

            <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 sm:p-5 shadow-xs flex items-center gap-3.5">
              <div class="flex h-11 w-11 sm:h-12 sm:w-12 shrink-0 items-center justify-center rounded-xl bg-amber-50 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400">
                <Globe class="h-5 w-5 sm:h-6 sm:w-6" />
              </div>
              <div class="min-w-0">
                <p class="text-[11px] sm:text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">{{ t('Google Accounts') }}</p>
                <p class="text-xl sm:text-2xl font-black text-navy-900 dark:text-white mt-0.5">{{ googleUsersCount.toLocaleString() }}</p>
              </div>
            </div>

            <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 sm:p-5 shadow-xs flex items-center gap-3.5">
              <div class="flex h-11 w-11 sm:h-12 sm:w-12 shrink-0 items-center justify-center rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400">
                <ShieldCheck class="h-5 w-5 sm:h-6 sm:w-6" />
              </div>
              <div class="min-w-0">
                <p class="text-[11px] sm:text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">{{ t('Verified Accounts') }}</p>
                <p class="text-xl sm:text-2xl font-black text-navy-900 dark:text-white mt-0.5">{{ verifiedUsersCount.toLocaleString() }}</p>
              </div>
            </div>
          </div>

          <!-- Main User Directory Card -->
          <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-card overflow-hidden">
            <!-- Header Bar -->
            <div class="flex flex-wrap items-center justify-between gap-4 p-5 border-b border-slate-100 dark:border-slate-800">
              <div>
                <h2 class="text-lg font-extrabold text-navy-900 dark:text-white flex items-center gap-2">
                  <UserCog class="w-5 h-5 text-indigo-600 dark:text-indigo-400" />
                  <span>{{ t('User Accounts') }}</span>
                </h2>
                <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">
                  {{ filteredUsers.length }} {{ t('users total') }}
                </p>
              </div>

              <div class="flex items-center gap-2.5">
                <button
                  type="button"
                  @click="loadUsersData"
                  class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs font-semibold text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white hover:bg-slate-50 dark:hover:bg-slate-700 transition cursor-pointer"
                >
                  <RefreshCw class="w-3.5 h-3.5" :class="{ 'animate-spin': usersLoading }" />
                  <span>{{ t('Refresh') }}</span>
                </button>
              </div>
            </div>

            <!-- Search & Filters Toolbar -->
            <div class="flex flex-col sm:flex-row items-center justify-between gap-3 p-4 bg-slate-50/60 dark:bg-slate-800/30 border-b border-slate-100 dark:border-slate-800">
              <div class="relative w-full sm:w-80">
                <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-slate-400" />
                <input
                  v-model="userSearch"
                  type="text"
                  :placeholder="t('Search user by name, email, phone, or telegram...')"
                  class="w-full pl-9 pr-3 py-1.5 text-xs rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500"
                />
              </div>

              <div class="flex flex-wrap items-center gap-2.5 w-full sm:w-auto justify-end">
                <div class="flex items-center gap-1.5">
                  <span class="text-xs font-semibold text-slate-500 dark:text-slate-400">{{ t('Sign-in Method') }}:</span>
                  <select
                    v-model="userMethodFilter"
                    class="px-2.5 py-1.5 text-xs rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white font-medium focus:outline-none"
                  >
                    <option value="all">{{ t('All Methods') }}</option>
                    <option value="email">{{ t('Email / Password') }}</option>
                    <option value="google">{{ t('Google') }}</option>
                  </select>
                </div>

                <div class="flex items-center gap-1.5">
                  <span class="text-xs font-semibold text-slate-500 dark:text-slate-400">{{ t('Verification') }}:</span>
                  <select
                    v-model="userVerifiedFilter"
                    class="px-2.5 py-1.5 text-xs rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white font-medium focus:outline-none"
                  >
                    <option value="all">{{ t('All Statuses') }}</option>
                    <option value="verified">{{ t('Verified') }}</option>
                    <option value="unverified">{{ t('Unverified') }}</option>
                  </select>
                </div>
              </div>
            </div>

            <!-- Users Data Table -->
            <div class="overflow-x-auto admin-scroll-box">
              <table class="w-full text-left border-collapse">
                <thead>
                  <tr class="border-b border-slate-200 dark:border-slate-800 text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-400 bg-slate-50/70 dark:bg-slate-800/40">
                    <th class="py-3 px-4">{{ t('User') }}</th>
                    <th class="py-3 px-4">{{ t('Sign-in Method') }}</th>
                    <th class="py-3 px-4">{{ t('Contact Info') }}</th>
                    <th class="py-3 px-4">{{ t('Profile Details') }}</th>
                    <th class="py-3 px-4">{{ t('Status') }}</th>
                    <th class="py-3 px-4">{{ t('Registered') }}</th>
                    <th class="py-3 px-4 text-right">{{ t('Actions') }}</th>
                  </tr>
                </thead>
                <tbody class="divide-y divide-slate-100 dark:divide-slate-800 text-xs text-slate-600 dark:text-slate-300">
                  <tr v-for="user in paginatedUsers" :key="user.id" class="hover:bg-slate-50/60 dark:hover:bg-slate-800/50 transition">
                    <!-- User avatar, name, email -->
                    <td class="py-3 px-4">
                      <div class="flex items-center gap-3">
                        <div class="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-navy-800 text-white font-bold flex items-center justify-center shrink-0 text-xs shadow-xs overflow-hidden">
                          <img v-if="user.avatar_url" :src="resolveImageUrl(user.avatar_url)" alt="" class="w-full h-full object-cover" />
                          <span v-else>{{ (user.full_name || 'U').slice(0, 2).toUpperCase() }}</span>
                        </div>
                        <div class="min-w-0">
                          <p class="font-bold text-navy-900 dark:text-white truncate max-w-[160px]">{{ user.full_name }}</p>
                          <p class="text-[11px] text-slate-500 dark:text-slate-400 truncate max-w-[160px]">{{ user.email }}</p>
                        </div>
                      </div>
                    </td>

                    <!-- Sign-in Method -->
                    <td class="py-3 px-4">
                      <span
                        class="inline-flex items-center gap-1 px-2.5 py-1 rounded-full text-[10px] font-bold"
                        :class="user.google_sub
                          ? 'bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-300 border border-amber-200 dark:border-amber-800'
                          : 'bg-indigo-50 text-indigo-700 dark:bg-indigo-950/60 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800'"
                      >
                        <Globe v-if="user.google_sub" class="w-3 h-3" />
                        <Mail v-else class="w-3 h-3" />
                        <span>{{ user.sign_in_method }}</span>
                      </span>
                    </td>

                    <!-- Contact Info -->
                    <td class="py-3 px-4">
                      <div class="space-y-0.5 text-[11px]">
                        <p v-if="user.phone" class="font-semibold text-slate-800 dark:text-slate-200">{{ user.phone }}</p>
                        <p v-if="user.telegram" class="text-slate-500 dark:text-slate-400">@{{ user.telegram.replace(/^@/, '') }}</p>
                        <p v-if="user.location" class="text-slate-400 dark:text-slate-500">{{ user.location }}</p>
                        <span v-if="!user.phone && !user.telegram && !user.location" class="text-slate-400 italic">-</span>
                      </div>
                    </td>

                    <!-- Profile Details -->
                    <td class="py-3 px-4">
                      <div class="space-y-0.5 text-[11px]">
                        <p v-if="user.occupation" class="font-medium text-slate-800 dark:text-slate-200">{{ user.occupation }}</p>
                        <p v-if="user.qualification" class="text-slate-500 dark:text-slate-400">{{ t(user.qualification) }}</p>
                        <p v-if="user.date_of_birth" class="text-slate-400 dark:text-slate-500">{{ user.date_of_birth }}</p>
                        <span v-if="!user.occupation && !user.qualification && !user.date_of_birth" class="text-slate-400 italic">-</span>
                      </div>
                    </td>

                    <!-- Status -->
                    <td class="py-3 px-4">
                      <span
                        class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-[10px] font-bold"
                        :class="user.is_verified === 1
                          ? 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/60 dark:text-emerald-400 border border-emerald-200/80 dark:border-emerald-800/80'
                          : 'bg-amber-50 text-amber-700 dark:bg-amber-950/60 dark:text-amber-400 border border-amber-200/80 dark:border-amber-800/80'"
                      >
                        <span class="w-1.5 h-1.5 rounded-full" :class="user.is_verified === 1 ? 'bg-emerald-500' : 'bg-amber-500'"></span>
                        <span>{{ user.is_verified === 1 ? t('Verified') : t('Unverified') }}</span>
                      </span>
                    </td>

                    <!-- Registered At -->
                    <td class="py-3 px-4 text-slate-500 dark:text-slate-400 whitespace-nowrap text-[11px]">
                      {{ formatCambodiaTime(user.created_at) }}
                    </td>

                    <!-- Actions -->
                    <td class="py-3 px-4 text-right">
                      <div class="flex items-center justify-end gap-1">
                        <button
                          type="button"
                          class="p-1.5 rounded-lg text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition cursor-pointer"
                          :title="t('Edit Profile')"
                          @click="openEditUserModal(user)"
                        >
                          <Pencil class="w-4 h-4" />
                        </button>
                        <button
                          type="button"
                          class="p-1.5 rounded-lg text-amber-600 dark:text-amber-400 hover:text-amber-700 dark:hover:text-amber-300 hover:bg-amber-50 dark:hover:bg-amber-950/40 transition cursor-pointer"
                          :title="t('Change Password')"
                          @click="openChangePasswordModal(user)"
                        >
                          <KeyRound class="w-4 h-4" />
                        </button>
                        <button
                          type="button"
                          class="p-1.5 rounded-lg text-red-600 dark:text-red-400 hover:text-red-700 dark:hover:text-red-300 hover:bg-red-50 dark:hover:bg-red-950/40 transition cursor-pointer"
                          :title="t('Delete User')"
                          @click="openDeleteUserModal(user)"
                        >
                          <Trash2 class="w-4 h-4" />
                        </button>
                      </div>
                    </td>
                  </tr>

                  <tr v-if="!paginatedUsers.length">
                    <td colspan="7" class="py-12 text-center text-xs text-slate-400 dark:text-slate-500">
                      {{ t('No user accounts found.') }}
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Pagination Bar -->
            <div v-if="filteredUsers.length > userPerPage" class="p-3 sm:p-4 border-t border-slate-100 dark:border-slate-800">
              <AdminPagination
                v-model:current-page="userPage"
                :total-pages="totalUserPages"
                :total-items="filteredUsers.length"
                :page-size="userPerPage"
              />
            </div>
          </div>

          <!-- Interactive Modal: Edit User Profile -->
          <div
            v-if="editingUser"
            class="fixed inset-0 z-[70] flex items-center justify-center p-3 sm:p-5 bg-slate-950/60 backdrop-blur-xs transition-opacity"
            @click.self="editingUser = null"
          >
            <div
              role="dialog"
              aria-modal="true"
              class="w-full max-w-2xl max-h-[92vh] flex flex-col rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150 my-auto"
            >
              <!-- Modal Sticky Header -->
              <div class="flex items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-800 p-4 sm:p-5 bg-slate-50/80 dark:bg-slate-800/60 shrink-0">
                <div class="flex items-center gap-3 min-w-0">
                  <div class="w-10 h-10 rounded-xl bg-gradient-to-br from-indigo-600 to-navy-800 text-white font-black flex items-center justify-center shrink-0 text-sm shadow-xs">
                    {{ (userEditForm.full_name || 'U').slice(0, 2).toUpperCase() }}
                  </div>
                  <div class="min-w-0">
                    <h3 class="font-extrabold text-navy-900 dark:text-white text-base truncate">
                      {{ t('Edit User Profile') }}
                    </h3>
                    <p class="text-xs text-slate-500 dark:text-slate-400 truncate">
                      {{ userEditForm.email }}
                    </p>
                  </div>
                </div>

                <button
                  type="button"
                  class="rounded-xl p-2 text-slate-400 hover:text-slate-700 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition cursor-pointer"
                  @click="editingUser = null"
                  :aria-label="t('Close')"
                >
                  <X class="w-5 h-5" />
                </button>
              </div>

              <!-- Form Scrollable Body -->
              <form @submit.prevent="saveUserEdit" class="flex-1 overflow-y-auto p-5 space-y-4 admin-scroll-box">
                <p v-if="userEditError" role="alert" class="rounded-xl bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900/40 p-3 text-xs text-red-700 dark:text-red-300">
                  {{ userEditError }}
                </p>

                <div class="grid gap-3 sm:grid-cols-2">
                  <label class="block">
                    <span class="admin-label dark:text-slate-100">{{ t('Full Name') }} *</span>
                    <input v-model.trim="userEditForm.full_name" type="text" required maxlength="120" class="admin-input" />
                  </label>

                  <label class="block">
                    <span class="admin-label dark:text-slate-100">{{ t('Email Address') }} *</span>
                    <input v-model.trim="userEditForm.email" type="email" required maxlength="254" class="admin-input" />
                  </label>

                  <label class="block">
                    <span class="admin-label dark:text-slate-100">{{ t('Phone Number') }}</span>
                    <input v-model.trim="userEditForm.phone" type="text" maxlength="50" class="admin-input" :placeholder="t('Enter phone number')" />
                  </label>

                  <label class="block">
                    <span class="admin-label dark:text-slate-100">{{ t('Telegram') }}</span>
                    <input v-model.trim="userEditForm.telegram" type="text" maxlength="80" class="admin-input" placeholder="@username" />
                  </label>

                  <label class="block">
                    <span class="admin-label dark:text-slate-100">{{ t('Date of Birth') }}</span>
                    <input v-model.trim="userEditForm.date_of_birth" type="text" maxlength="30" class="admin-input" placeholder="YYYY-MM-DD" />
                  </label>

                  <label class="block">
                    <span class="admin-label dark:text-slate-100">{{ t('Location') }}</span>
                    <input v-model.trim="userEditForm.location" type="text" maxlength="100" class="admin-input" :placeholder="t('e.g. Phnom Penh')" />
                  </label>

                  <label class="block sm:col-span-2">
                    <span class="admin-label dark:text-slate-100">{{ t('Highest Academic Qualification') }}</span>
                    <select v-model="userEditForm.qualification" class="admin-input">
                      <option value="">{{ t('Please specify your qualification') }}</option>
                      <option value="High School">{{ t('High School') }}</option>
                      <option value="Undergraduate / University">{{ t('Undergraduate / University') }}</option>
                      <option value="Bachelor's Degree">{{ t("Bachelor's Degree") }}</option>
                      <option value="Other">{{ t('Other') }}</option>
                    </select>
                  </label>

                  <label class="block">
                    <span class="admin-label dark:text-slate-100">{{ t('Current Occupation') }}</span>
                    <input v-model.trim="userEditForm.occupation" type="text" maxlength="100" class="admin-input" :placeholder="t('e.g. Student, Engineer')" />
                  </label>

                  <label class="block">
                    <span class="admin-label dark:text-slate-100">{{ t('Coding Experience') }}</span>
                    <input v-model.trim="userEditForm.experience" type="text" maxlength="100" class="admin-input" :placeholder="t('Briefly describe any prior experience...')" />
                  </label>

                  <div class="sm:col-span-2 pt-2">
                    <label class="flex items-center gap-2.5 text-xs font-semibold text-slate-700 dark:text-slate-200 cursor-pointer">
                      <input v-model="userEditForm.is_verified" type="checkbox" class="w-4 h-4 rounded text-indigo-600 focus:ring-indigo-500" />
                      <span>{{ t('Email Verified') }} ({{ t('allows student sign-in without code') }})</span>
                    </label>
                  </div>
                </div>

                <!-- Footer buttons -->
                <div class="flex items-center justify-end gap-2.5 pt-4 border-t border-slate-100 dark:border-slate-800">
                  <button
                    type="button"
                    class="rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2 text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 transition cursor-pointer"
                    @click="editingUser = null"
                  >
                    {{ t('Cancel') }}
                  </button>
                  <button
                    type="submit"
                    :disabled="userEditBusy"
                    class="admin-primary-button cursor-pointer"
                  >
                    {{ userEditBusy ? t('Saving...') : t('Save changes') }}
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- Interactive Modal: Change User Password -->
          <div
            v-if="passwordTargetUser"
            class="fixed inset-0 z-[70] flex items-center justify-center p-3 sm:p-5 bg-slate-950/60 backdrop-blur-xs transition-opacity"
            @click.self="passwordTargetUser = null"
          >
            <div
              role="dialog"
              aria-modal="true"
              class="w-full max-w-md flex flex-col rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150 my-auto"
            >
              <div class="flex items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-800 p-4 sm:p-5 bg-amber-50/60 dark:bg-amber-950/30 shrink-0">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-xl bg-amber-500 text-white font-black flex items-center justify-center shrink-0 shadow-xs">
                    <KeyRound class="w-5 h-5" />
                  </div>
                  <div>
                    <h3 class="font-extrabold text-navy-900 dark:text-white text-base">
                      {{ t('Change User Password') }}
                    </h3>
                    <p class="text-xs text-slate-500 dark:text-slate-400">
                      {{ passwordTargetUser.full_name }} ({{ passwordTargetUser.email }})
                    </p>
                  </div>
                </div>

                <button
                  type="button"
                  class="rounded-xl p-2 text-slate-400 hover:text-slate-700 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition cursor-pointer"
                  @click="passwordTargetUser = null"
                  :aria-label="t('Close')"
                >
                  <X class="w-5 h-5" />
                </button>
              </div>

              <form @submit.prevent="saveUserPassword" class="p-5 space-y-4">
                <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                  {{ t('The user will use this new password to sign into their account.') }}
                </p>

                <p v-if="passwordError" role="alert" class="rounded-xl bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900/40 p-3 text-xs text-red-700 dark:text-red-300">
                  {{ passwordError }}
                </p>

                <div>
                  <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                    {{ t('New Password') }}
                  </label>
                  <div class="relative">
                    <input
                      v-model="passwordForm.newPassword"
                      :type="showNewPassword ? 'text' : 'password'"
                      required
                      minlength="8"
                      class="admin-input pr-10"
                      :placeholder="t('Enter new password (min. 8 characters)')"
                    />
                    <button
                      type="button"
                      class="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
                      @click="showNewPassword = !showNewPassword"
                    >
                      <component :is="showNewPassword ? EyeOff : Eye" class="w-4 h-4" />
                    </button>
                  </div>
                </div>

                <div>
                  <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                    {{ t('Confirm New Password') }}
                  </label>
                  <input
                    v-model="passwordForm.confirmPassword"
                    :type="showNewPassword ? 'text' : 'password'"
                    required
                    minlength="8"
                    class="admin-input"
                    :placeholder="t('Confirm new password')"
                  />
                </div>

                <div class="flex items-center justify-end gap-2.5 pt-3 border-t border-slate-100 dark:border-slate-800">
                  <button
                    type="button"
                    class="rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2 text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 transition"
                    @click="passwordTargetUser = null"
                  >
                    {{ t('Cancel') }}
                  </button>
                  <button
                    type="submit"
                    :disabled="passwordBusy"
                    class="rounded-xl bg-amber-600 hover:bg-amber-700 text-white px-4 py-2 text-xs font-bold transition shadow-xs disabled:opacity-50 cursor-pointer"
                  >
                    {{ passwordBusy ? t('Saving...') : t('Save Password') }}
                  </button>
                </div>
              </form>
            </div>
          </div>

          <!-- Interactive Modal: Delete User Confirmation -->
          <div
            v-if="deleteTargetUser"
            class="fixed inset-0 z-[70] flex items-center justify-center p-3 sm:p-5 bg-slate-950/60 backdrop-blur-xs transition-opacity"
            @click.self="deleteTargetUser = null"
          >
            <div
              role="dialog"
              aria-modal="true"
              class="w-full max-w-md flex flex-col rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150 my-auto"
            >
              <div class="p-5 text-center space-y-3">
                <div class="w-12 h-12 rounded-2xl bg-red-100 dark:bg-red-950/60 text-red-600 dark:text-red-400 flex items-center justify-center mx-auto shadow-xs">
                  <Trash2 class="w-6 h-6" />
                </div>
                <h3 class="text-base font-extrabold text-navy-900 dark:text-white">
                  {{ t('Delete User Account') }}
                </h3>
                <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">
                  {{ t('This action will permanently delete all profile data, login credentials, and sessions for') }}
                  <strong class="text-slate-800 dark:text-slate-200 block mt-1 font-bold">{{ deleteTargetUser.full_name }} ({{ deleteTargetUser.email }})</strong>
                </p>
                <p class="text-[11px] font-semibold text-red-600 dark:text-red-400">
                  {{ t('This action cannot be undone.') }}
                </p>

                <p v-if="deleteError" role="alert" class="rounded-xl bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900/40 p-2.5 text-xs text-red-700 dark:text-red-300">
                  {{ deleteError }}
                </p>
              </div>

              <div class="flex items-center justify-center gap-3 p-4 bg-slate-50 dark:bg-slate-800/50 border-t border-slate-100 dark:border-slate-800">
                <button
                  type="button"
                  class="flex-1 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2.5 text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 transition cursor-pointer"
                  @click="deleteTargetUser = null"
                >
                  {{ t('Cancel') }}
                </button>
                <button
                  type="button"
                  :disabled="deleteBusy"
                  class="flex-1 rounded-xl bg-red-600 hover:bg-red-700 text-white px-4 py-2.5 text-xs font-bold transition shadow-xs disabled:opacity-50 cursor-pointer"
                  @click="confirmDeleteUser"
                >
                  {{ deleteBusy ? t('Deleting...') : t('Delete User') }}
                </button>
              </div>
            </div>
          </div>
        </section>

        <section v-else-if="activeSection === 'settings'" class="w-full pb-8">
          <form class="space-y-6 rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-card sm:p-7" @submit.prevent="saveSettings">
            <div><h2 class="text-lg font-extrabold text-navy-900 dark:text-white">{{ t('Site Settings & CMS') }}</h2><p class="mt-1 text-sm text-slate-500 dark:text-slate-300">{{ t('Edit About page metrics, contact details, footer text, and payment setup.') }}</p></div>
            <section><h3 class="mb-3 font-bold text-slate-800 dark:text-slate-200">{{ t('About Page Stats') }}</h3><div class="grid gap-4 sm:grid-cols-2"><label v-for="(value, key) in aboutSettings" :key="key" class="block"><span class="admin-label dark:text-slate-100">{{ t(value.label) }}</span><input v-model.trim="settingsForm[key]" maxlength="30" class="admin-input" /></label></div></section>
            <section><h3 class="mb-3 font-bold text-slate-800 dark:text-slate-200">{{ t('CMS Sections') }}</h3><div class="grid gap-4 sm:grid-cols-2"><label class="block"><span class="admin-label dark:text-slate-100">{{ t('Contact email') }}</span><input v-model.trim="settingsForm.contact_email" type="email" maxlength="254" class="admin-input" /></label><label class="block"><span class="admin-label dark:text-slate-100">{{ t('Contact phone') }}</span><input v-model.trim="settingsForm.contact_phone" maxlength="80" class="admin-input" /></label><label class="block sm:col-span-2"><span class="admin-label dark:text-slate-100">{{ t('Footer description') }}</span><textarea v-model.trim="settingsForm.footer_description" maxlength="1000" rows="3" class="admin-input resize-y py-2.5"></textarea></label></div></section>
            <section><h3 class="mb-3 font-bold text-slate-800 dark:text-slate-200">{{ t('Payment Setup') }}</h3><div class="grid gap-4 sm:grid-cols-2">
              <div class="block"><span class="admin-label dark:text-slate-100">{{ t('Merchant QR image') }}</span><img v-if="settingsForm.merchant_qr_url" :src="resolveImageUrl(settingsForm.merchant_qr_url)" alt="" class="mb-3 h-36 w-36 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 object-contain" /><input ref="qrImageInput" type="file" accept=".png,.jpg,.jpeg,image/png,image/jpeg" class="sr-only" @change="handleQrImageSelection" /><button type="button" :disabled="qrImageUploading" class="rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2 text-sm font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-50" @click="qrImageInput?.click()">{{ qrImageUploading ? t('Uploading...') : t('Upload QR image') }}</button></div>
              <label class="block"><span class="admin-label dark:text-slate-100">{{ t('Merchant QR image URL') }}</span><input v-model.trim="settingsForm.merchant_qr_url" type="url" maxlength="2000" class="admin-input" /></label>
              <label class="block"><span class="admin-label dark:text-slate-100">{{ t('Bank info') }}</span><input v-model.trim="settingsForm.merchant_bank_info" maxlength="500" class="admin-input" /></label><label class="block"><span class="admin-label dark:text-slate-100">{{ t('Session timer (minutes)') }}</span><input v-model.number="settingsForm.payment_session_minutes" type="number" min="1" max="1440" class="admin-input" /></label></div></section>
            <section class="rounded-xl border border-amber-200 dark:border-amber-900/50 bg-amber-50 dark:bg-amber-950/30 p-4"><h3 class="font-bold text-amber-900 dark:text-amber-300">{{ t('Security') }}</h3><p class="mt-2 text-sm leading-6 text-amber-900 dark:text-amber-200/90">{{ t('Admin credentials and session secrets are configured on the backend server, not in website settings. Update the server environment and restart the API to rotate them.') }}</p></section>
            <p v-if="settingsError" role="alert" class="rounded-lg bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900/40 p-3 text-sm text-red-700 dark:text-red-300">{{ settingsError }}</p>
            <p v-if="settingsSaved" role="status" class="rounded-lg bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 p-3 text-sm text-emerald-800 dark:text-emerald-300">{{ t('Settings saved.') }}</p>
            <button type="submit" :disabled="busy" class="admin-primary-button max-w-xs">{{ busy ? t('Saving...') : t('Save site settings') }}</button>
          </form>
        </section>

        <!-- Traffic & Login Logs Section -->
        <section v-else-if="activeSection === 'logs'" class="w-full pb-8 space-y-6">
          <!-- Top Stat Cards -->
          <div class="grid grid-cols-2 gap-3 sm:gap-5 lg:grid-cols-4">
            <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 sm:p-5 shadow-xs flex items-center gap-3.5">
              <div class="flex h-11 w-11 sm:h-12 sm:w-12 shrink-0 items-center justify-center rounded-xl bg-indigo-50 dark:bg-indigo-950/60 text-indigo-600 dark:text-indigo-400">
                <Eye class="h-5 w-5 sm:h-6 sm:w-6" />
              </div>
              <div class="min-w-0">
                <p class="text-[11px] sm:text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">{{ t('Total Page Visits') }}</p>
                <p class="text-xl sm:text-2xl font-black text-navy-900 dark:text-white mt-0.5">{{ (logsAnalytics?.total_visits ?? 0).toLocaleString() }}</p>
              </div>
            </div>

            <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 sm:p-5 shadow-xs flex items-center gap-3.5">
              <div class="flex h-11 w-11 sm:h-12 sm:w-12 shrink-0 items-center justify-center rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400">
                <Users class="h-5 w-5 sm:h-6 sm:w-6" />
              </div>
              <div class="min-w-0">
                <p class="text-[11px] sm:text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">{{ t('Unique Visitors') }}</p>
                <p class="text-xl sm:text-2xl font-black text-navy-900 dark:text-white mt-0.5">{{ (logsAnalytics?.unique_visitors ?? 0).toLocaleString() }}</p>
              </div>
            </div>

            <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 sm:p-5 shadow-xs flex items-center gap-3.5">
              <div class="flex h-11 w-11 sm:h-12 sm:w-12 shrink-0 items-center justify-center rounded-xl bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400">
                <ShieldCheck class="h-5 w-5 sm:h-6 sm:w-6" />
              </div>
              <div class="min-w-0">
                <p class="text-[11px] sm:text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">{{ t('Total User Logins') }}</p>
                <p class="text-xl sm:text-2xl font-black text-navy-900 dark:text-white mt-0.5">{{ (logsAnalytics?.total_logins ?? 0).toLocaleString() }}</p>
              </div>
            </div>

            <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 sm:p-5 shadow-xs flex items-center gap-3.5">
              <div class="flex h-11 w-11 sm:h-12 sm:w-12 shrink-0 items-center justify-center rounded-xl bg-amber-50 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400">
                <Activity class="h-5 w-5 sm:h-6 sm:w-6" />
              </div>
              <div class="min-w-0">
                <p class="text-[11px] sm:text-xs font-semibold uppercase tracking-wider text-slate-500 dark:text-slate-400">{{ t('Visits Today') }}</p>
                <p class="text-xl sm:text-2xl font-black text-navy-900 dark:text-white mt-0.5">
                  {{ (logsAnalytics?.today_visits ?? 0).toLocaleString() }}
                  <span class="text-xs font-normal text-slate-400">({{ logsAnalytics?.today_logins ?? 0 }} logins)</span>
                </p>
              </div>
            </div>
          </div>

          <!-- Main Card with Tabs -->
          <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-card overflow-hidden">
            <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 p-5 sm:p-6 border-b border-slate-100 dark:border-slate-800">
              <div>
                <h2 class="text-lg font-extrabold text-navy-900 dark:text-white">{{ t('Traffic & Login Logs') }}</h2>
                <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-400">{{ t('Monitor real-time user authentication and website visitor traffic.') }}</p>
              </div>
              <div class="flex items-center gap-2">
                <div class="flex rounded-xl bg-slate-100 dark:bg-slate-800 p-1">
                  <button
                    type="button"
                    class="px-3 py-1.5 rounded-lg text-xs font-bold transition"
                    :class="logsActiveTab === 'logins' ? 'bg-white dark:bg-slate-700 text-navy-900 dark:text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-navy-900 dark:hover:text-white'"
                    @click="logsActiveTab = 'logins'"
                  >
                    {{ t('Sign-in History') }} ({{ loginLogs.length }})
                  </button>
                  <button
                    type="button"
                    class="px-3 py-1.5 rounded-lg text-xs font-bold transition"
                    :class="logsActiveTab === 'visits' ? 'bg-white dark:bg-slate-700 text-navy-900 dark:text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-navy-900 dark:hover:text-white'"
                    @click="logsActiveTab = 'visits'"
                  >
                    {{ t('Website Traffic') }} ({{ visitLogs.length }})
                  </button>
                  <button
                    type="button"
                    class="px-3 py-1.5 rounded-lg text-xs font-bold transition"
                    :class="logsActiveTab === 'pages' ? 'bg-white dark:bg-slate-700 text-navy-900 dark:text-white shadow-xs' : 'text-slate-600 dark:text-slate-400 hover:text-navy-900 dark:hover:text-white'"
                    @click="logsActiveTab = 'pages'"
                  >
                    {{ t('Top Pages') }}
                  </button>
                </div>

                <button
                  type="button"
                  :disabled="logsLoading"
                  class="flex h-9 items-center gap-1.5 px-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-xs font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700/60 disabled:opacity-50 transition"
                  @click="loadLogsData"
                >
                  <RefreshCw class="w-3.5 h-3.5" :class="{ 'animate-spin': logsLoading }" />
                  <span class="hidden sm:inline">{{ t('Refresh') }}</span>
                </button>
              </div>
            </div>

            <!-- Tab 1: Login Logs -->
            <div v-if="logsActiveTab === 'logins'">
              <div class="flex flex-col sm:flex-row items-center justify-between gap-3 p-4 bg-slate-50/60 dark:bg-slate-800/30 border-b border-slate-100 dark:border-slate-800">
                <div class="relative w-full sm:w-72">
                  <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-slate-400" />
                  <input
                    v-model="loginSearch"
                    type="text"
                    :placeholder="t('Search user, email, or IP...')"
                    class="w-full pl-9 pr-3 py-1.5 text-xs rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500"
                  />
                </div>
                <div class="flex items-center gap-2 self-end sm:self-auto">
                  <span class="text-xs font-semibold text-slate-500 dark:text-slate-400">{{ t('Role') }}:</span>
                  <select
                    v-model="loginRoleFilter"
                    class="px-2.5 py-1.5 text-xs rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white font-medium focus:outline-none"
                  >
                    <option value="all">{{ t('All Roles') }}</option>
                    <option value="user">{{ t('Users Only') }}</option>
                    <option value="admin">{{ t('Admins Only') }}</option>
                  </select>
                </div>
              </div>

              <div class="overflow-x-auto">
                <table class="w-full text-left text-xs">
                  <thead class="bg-slate-50/80 dark:bg-slate-800/60 text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-100 dark:border-slate-800">
                    <tr>
                      <th class="py-3 px-4">{{ t('User') }}</th>
                      <th class="py-3 px-4">{{ t('Role') }}</th>
                      <th class="py-3 px-4">{{ t('Method') }}</th>
                      <th class="py-3 px-4">{{ t('IP Address') }}</th>
                      <th class="py-3 px-4">{{ t('Device / Browser') }}</th>
                      <th class="py-3 px-4 text-right">{{ t('Date & Time') }}</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60">
                    <tr v-for="log in paginatedLoginLogs" :key="log.id" class="hover:bg-slate-50/50 dark:hover:bg-slate-800/40 transition">
                      <td class="py-3 px-4">
                        <div class="flex items-center gap-2.5">
                          <span class="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300 font-bold text-xs uppercase">
                            {{ (log.user_name || log.user_email || 'U')[0] }}
                          </span>
                          <div class="min-w-0">
                            <p class="font-bold text-slate-900 dark:text-white truncate">{{ log.user_name || t('User') }}</p>
                            <p class="text-[11px] text-slate-500 dark:text-slate-400 truncate">{{ log.user_email }}</p>
                          </div>
                        </div>
                      </td>
                      <td class="py-3 px-4">
                        <span
                          class="inline-flex items-center px-2 py-0.5 rounded-full text-[10px] font-bold"
                          :class="log.role === 'Admin' ? 'bg-indigo-50 dark:bg-indigo-950/60 text-indigo-700 dark:text-indigo-300 border border-indigo-200 dark:border-indigo-800/60' : 'bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/60'"
                        >
                          {{ log.role }}
                        </span>
                      </td>
                      <td class="py-3 px-4">
                        <span class="inline-flex items-center gap-1 px-2 py-0.5 rounded-md text-[11px] font-semibold bg-slate-100 dark:bg-slate-800 text-slate-700 dark:text-slate-300">
                          {{ log.login_method }}
                        </span>
                      </td>
                      <td class="py-3 px-4 font-mono text-[11px] text-slate-600 dark:text-slate-400">
                        {{ log.ip_address || '—' }}
                      </td>
                      <td class="py-3 px-4 text-slate-600 dark:text-slate-400">
                        {{ parseDevice(log.user_agent).type }} &bull; {{ parseDevice(log.user_agent).browser }}
                      </td>
                      <td class="py-3 px-4 text-right text-slate-500 dark:text-slate-400 whitespace-nowrap">
                        {{ log.created_at }}
                      </td>
                    </tr>
                    <tr v-if="!paginatedLoginLogs.length">
                      <td colspan="6" class="py-8 text-center text-slate-400 dark:text-slate-500">
                        {{ t('No login records found.') }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div v-if="filteredLoginLogs.length > loginLimit" class="p-3 sm:p-4 border-t border-slate-100 dark:border-slate-800">
                <AdminPagination
                  v-model:current-page="loginPage"
                  :total-pages="totalLoginPages"
                  :total-items="filteredLoginLogs.length"
                  :page-size="loginLimit"
                />
              </div>
            </div>

            <!-- Tab 2: Traffic / Visit Logs -->
            <div v-else-if="logsActiveTab === 'visits'">
              <div class="p-4 bg-slate-50/60 dark:bg-slate-800/30 border-b border-slate-100 dark:border-slate-800">
                <div class="relative w-full sm:w-72">
                  <Search class="absolute left-3 top-1/2 -translate-y-1/2 h-3.5 w-3.5 text-slate-400" />
                  <input
                    v-model="visitSearch"
                    type="text"
                    :placeholder="t('Search path, IP, or referrer...')"
                    class="w-full pl-9 pr-3 py-1.5 text-xs rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500"
                  />
                </div>
              </div>

              <div class="overflow-x-auto">
                <table class="w-full text-left text-xs">
                  <thead class="bg-slate-50/80 dark:bg-slate-800/60 text-slate-500 dark:text-slate-400 uppercase tracking-wider font-semibold border-b border-slate-100 dark:border-slate-800">
                    <tr>
                      <th class="py-3 px-4">{{ t('Page Path') }}</th>
                      <th class="py-3 px-4">{{ t('User / Visitor') }}</th>
                      <th class="py-3 px-4">{{ t('Device / Browser') }}</th>
                      <th class="py-3 px-4">{{ t('IP Address') }}</th>
                      <th class="py-3 px-4">{{ t('Referrer') }}</th>
                      <th class="py-3 px-4 text-right">{{ t('Date & Time') }}</th>
                    </tr>
                  </thead>
                  <tbody class="divide-y divide-slate-100 dark:divide-slate-800/60">
                    <tr v-for="visit in paginatedVisitLogs" :key="visit.id" class="hover:bg-slate-50/50 dark:hover:bg-slate-800/40 transition">
                      <td class="py-3 px-4">
                        <span class="inline-flex items-center px-2 py-0.5 rounded-md text-[11px] font-mono font-bold bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-indigo-300">
                          {{ visit.path }}
                        </span>
                      </td>
                      <td class="py-3 px-4 min-w-[160px]">
                        <div v-if="visit.user_email || visit.user_name" class="flex items-center gap-2">
                          <div class="h-6 w-6 rounded-full bg-emerald-100 dark:bg-emerald-950/80 text-emerald-700 dark:text-emerald-300 flex items-center justify-center text-[10px] font-black shrink-0 border border-emerald-200 dark:border-emerald-800">
                            {{ (visit.user_name || visit.user_email || 'U')[0].toUpperCase() }}
                          </div>
                          <div class="min-w-0">
                            <p class="font-bold text-slate-900 dark:text-white truncate text-[11px] leading-tight">
                              {{ visit.user_name || visit.user_email }}
                            </p>
                            <p v-if="visit.user_name && visit.user_email" class="text-[10px] text-slate-400 truncate leading-tight">
                              {{ visit.user_email }}
                            </p>
                            <span class="font-mono text-[9px] text-slate-400 truncate block">
                              {{ visit.visitor_id }}
                            </span>
                          </div>
                        </div>
                        <div v-else class="flex items-center gap-1.5">
                          <span class="inline-flex items-center px-1.5 py-0.5 rounded text-[10px] font-medium bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400">
                            {{ t('Guest') }}
                          </span>
                          <span class="font-mono text-[10px] text-slate-400 truncate max-w-28" :title="visit.visitor_id">
                            {{ visit.visitor_id }}
                          </span>
                        </div>
                      </td>
                      <td class="py-3 px-4 text-slate-600 dark:text-slate-400">
                        {{ parseDevice(visit.user_agent).type }} &bull; {{ parseDevice(visit.user_agent).browser }}
                      </td>
                      <td class="py-3 px-4 font-mono text-[11px] text-slate-600 dark:text-slate-400">
                        {{ visit.ip_address || '—' }}
                      </td>
                      <td class="py-3 px-4 text-slate-500 dark:text-slate-400 truncate max-w-36">
                        {{ visit.referrer || t('Direct') }}
                      </td>
                      <td class="py-3 px-4 text-right text-slate-500 dark:text-slate-400 whitespace-nowrap">
                        {{ visit.created_at }}
                      </td>
                    </tr>
                    <tr v-if="!paginatedVisitLogs.length">
                      <td colspan="6" class="py-8 text-center text-slate-400 dark:text-slate-500">
                        {{ t('No visitor traffic recorded yet.') }}
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>

              <div v-if="filteredVisitLogs.length > visitLimit" class="p-3 sm:p-4 border-t border-slate-100 dark:border-slate-800">
                <AdminPagination
                  v-model:current-page="visitPage"
                  :total-pages="totalVisitPages"
                  :total-items="filteredVisitLogs.length"
                  :page-size="visitLimit"
                />
              </div>
            </div>

            <!-- Tab 3: Top Pages Breakdown -->
            <div v-else-if="logsActiveTab === 'pages'" class="p-5 sm:p-6 space-y-4">
              <h3 class="text-sm font-bold text-slate-900 dark:text-white">{{ t('Most Visited Pages') }}</h3>
              <div v-if="logsAnalytics?.top_pages && logsAnalytics.top_pages.length" class="space-y-3">
                <div
                  v-for="item in logsAnalytics.top_pages"
                  :key="item.path"
                  class="flex flex-col gap-1.5 p-3 rounded-xl border border-slate-100 dark:border-slate-800 bg-slate-50/50 dark:bg-slate-800/40"
                >
                  <div class="flex items-center justify-between text-xs font-bold">
                    <span class="font-mono text-navy-900 dark:text-white">{{ item.path }}</span>
                    <span class="text-slate-500 dark:text-slate-400">{{ item.count.toLocaleString() }} {{ t('views') }}</span>
                  </div>
                  <div class="h-2 w-full rounded-full bg-slate-200 dark:bg-slate-700 overflow-hidden">
                    <div
                      class="h-full bg-navy-800 dark:bg-indigo-500 rounded-full transition-all duration-300"
                      :style="{ width: `${Math.min(100, Math.round(((item.count || 0) / (logsAnalytics?.total_visits || 1)) * 100))}%` }"
                    ></div>
                  </div>
                </div>
              </div>
              <p v-else class="text-xs text-slate-400 dark:text-slate-500">{{ t('No page visit statistics yet.') }}</p>
            </div>
          </div>
        </section>

        <div v-else class="w-full grid gap-6 items-start lg:grid-cols-[30%_minmax(0,1fr)]">
          <!-- 30% Column: Courses List -->
          <section class="h-fit rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-4 sm:p-5 shadow-card flex flex-col">
            <div>
              <div class="mb-4 flex items-center justify-between gap-2 border-b border-slate-100 dark:border-slate-800 pb-3">
                <div>
                  <h2 class="text-base font-extrabold text-navy-900 dark:text-white leading-tight">{{ t('Courses') }}</h2>
                  <p class="text-[11px] text-slate-500 dark:text-slate-400">
                    {{ filteredCourses.length }} {{ t('courses total') }}
                    <span v-if="!reorderAllMode && totalCoursePages > 1" class="text-slate-400 dark:text-slate-500">
                      &bull; {{ t('Page') }} {{ coursePage }} / {{ totalCoursePages }}
                    </span>
                    <span v-else-if="reorderAllMode" class="text-indigo-600 dark:text-indigo-400 font-semibold">
                      &bull; {{ t('Reorder all') }}
                    </span>
                  </p>
                </div>
                <div class="flex items-center gap-1.5">
                  <button
                    type="button"
                    @click="reorderAllMode = !reorderAllMode"
                    class="inline-flex items-center gap-1 px-2.5 py-1 rounded-lg text-[11px] font-semibold transition cursor-pointer select-none"
                    :class="reorderAllMode
                      ? 'bg-navy-900 text-white dark:bg-indigo-600 shadow-2xs'
                      : 'border border-slate-200 dark:border-slate-700 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800'"
                    :title="reorderAllMode ? t('Paging view') : t('Reorder all')"
                  >
                    <GripVertical class="w-3.5 h-3.5" />
                    <span>{{ reorderAllMode ? t('Paging view') : t('Reorder all') }}</span>
                  </button>
                </div>
              </div>

              <p v-if="errorMessage" class="mb-3 rounded-lg bg-red-50 p-2.5 text-xs text-red-700" role="alert">{{ errorMessage }}</p>
              <p v-if="successMessage" class="mb-3 rounded-lg bg-emerald-50 p-2.5 text-xs text-emerald-800" role="status">{{ successMessage }}</p>
              <div v-if="loadingCourses" class="py-10 text-center text-xs text-slate-500">{{ t('Loading courses...') }}</div>
              <div v-else class="space-y-2.5">
                <article
                  v-for="(course, index) in displayedCourses"
                  :key="course.id"
                  :draggable="!courseSearch.trim()"
                  @dragstart="handleCourseDragStart($event, course, index)"
                  @dragover.prevent="handleCourseDragOver($event, index)"
                  @dragleave="handleCourseDragLeave($event, index)"
                  @drop="handleCourseDrop($event, index)"
                  @dragend="handleCourseDragEnd"
                  class="group flex items-center gap-2 rounded-xl border p-2.5 transition select-none cursor-pointer"
                  :class="[
                    editingId === course.id
                      ? 'border-navy-900 dark:border-indigo-500 bg-navy-50/60 dark:bg-slate-800 ring-1 ring-navy-900/10'
                      : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-white dark:bg-slate-900',
                    dragOverCourseIndex === index ? 'ring-2 ring-indigo-500 border-indigo-500 bg-indigo-50/40 dark:bg-indigo-950/40' : '',
                    draggedCourseIndex === index ? 'opacity-40 scale-[0.98] border-dashed border-indigo-400' : ''
                  ]"
                  @click="editCourse(course)"
                >
                  <!-- Drag Grip Handle & Rank Badge -->
                  <div
                    class="flex items-center gap-1 shrink-0 text-slate-400 hover:text-navy-900 dark:hover:text-slate-200 cursor-grab active:cursor-grabbing p-1 -ml-1 rounded touch-none"
                    :title="t('Drag to change position')"
                    @click.stop
                  >
                    <GripVertical class="w-4 h-4 shrink-0 text-slate-400 group-hover:text-slate-600 dark:group-hover:text-slate-300 transition-colors" />
                    <span
                      class="inline-flex items-center justify-center min-w-5 h-5 px-1 rounded text-[10px] font-bold border transition"
                      :class="getCourseGlobalIndex(index) === 0
                        ? 'bg-amber-100 text-amber-800 border-amber-300 dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-800/80 font-black'
                        : 'bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-400 border-slate-200/80 dark:border-slate-700'"
                      :title="t('Current display position')"
                    >
                      #{{ getCourseGlobalIndex(index) + 1 }}
                    </span>
                  </div>

                  <img v-if="course.image_url" :src="resolveImageUrl(course.image_url)" alt="" class="h-12 w-12 shrink-0 rounded-lg bg-slate-100 dark:bg-slate-800 object-cover" />
                  <div v-else class="flex h-12 w-12 shrink-0 items-center justify-center rounded-lg bg-slate-100 dark:bg-slate-800 text-[10px] text-slate-400">{{ t('No image') }}</div>
                  <div class="min-w-0 flex-1">
                    <h3 class="truncate text-xs font-bold text-slate-900 dark:text-white" :title="course.title">{{ course.title }}</h3>
                    <p class="mt-0.5 truncate text-[11px] text-slate-500 dark:text-slate-400">
                      ${{ course.price }} · {{ t(course.status) }}
                    </p>
                  </div>
                  <div class="flex shrink-0 items-center gap-1" @click.stop>
                    <!-- Quick Move Up/Down/Top buttons -->
                    <button
                      type="button"
                      class="p-1 rounded text-slate-400 hover:text-navy-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition disabled:opacity-20 disabled:pointer-events-none cursor-pointer"
                      :disabled="getCourseGlobalIndex(index) === 0"
                      @click="moveCourseUp(course)"
                      :title="t('Move up')"
                    >
                      <ArrowUp class="w-3.5 h-3.5" />
                    </button>
                    <button
                      type="button"
                      class="p-1 rounded text-slate-400 hover:text-navy-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition disabled:opacity-20 disabled:pointer-events-none cursor-pointer"
                      :disabled="getCourseGlobalIndex(index) === courses.length - 1"
                      @click="moveCourseDown(course)"
                      :title="t('Move down')"
                    >
                      <ArrowDown class="w-3.5 h-3.5" />
                    </button>
                    <button
                      v-if="getCourseGlobalIndex(index) > 0"
                      type="button"
                      class="p-1 rounded text-indigo-600 dark:text-indigo-400 hover:bg-indigo-50 dark:hover:bg-slate-800 transition cursor-pointer"
                      @click="moveCourseToTop(course)"
                      :title="t('Make this course #1 (first seen by website visitors)')"
                    >
                      <ArrowUpToLine class="w-3.5 h-3.5" />
                    </button>

                    <button
                      type="button"
                      class="rounded-md border border-slate-300 dark:border-slate-700 px-2 py-1 text-[11px] font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-800 cursor-pointer"
                      @click="editCourse(course)"
                    >
                      {{ t('Edit') }}
                    </button>
                    <button
                      type="button"
                      class="rounded-md border border-red-200 dark:border-red-900/50 px-2 py-1 text-[11px] font-semibold text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/40 cursor-pointer"
                      @click="removeCourse(course)"
                    >
                      {{ t('Delete') }}
                    </button>
                  </div>
                </article>
                <p v-if="!filteredCourses.length && courseSearch.trim()" class="rounded-lg bg-slate-50 dark:bg-slate-800 px-3 py-6 text-center text-xs text-slate-500">{{ t('No matching courses.') }}</p>
                <p v-else-if="!courses.length" class="rounded-lg bg-slate-50 dark:bg-slate-800 px-3 py-6 text-center text-xs text-slate-500">{{ t('No courses yet. Add your first course.') }}</p>
              </div>
            </div>

            <!-- Pagination Bar matching wireframe (hidden in Reorder All mode) -->
            <div v-if="!reorderAllMode" class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-800">
              <AdminPagination
                v-model:current-page="coursePage"
                :total-pages="totalCoursePages"
                :total-items="filteredCourses.length"
                :page-size="coursePerPage"
                :center="true"
              />
            </div>
          </section>

          <!-- 70% Column: Add / Edit Course Form -->
          <section class="h-fit rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-card sm:p-6">
            <div class="mb-5 flex items-center justify-between gap-3 border-b border-slate-100 dark:border-slate-800 pb-4">
              <div>
                <h2 class="text-lg font-extrabold text-navy-900 dark:text-white">{{ editingId ? t('Edit course') : t('Add course') }}</h2>
                <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-300">{{ t('Published course details appear in the public catalog and detail page.') }}</p>
              </div>
              <button
                type="button"
                class="rounded-lg bg-navy-900 dark:bg-indigo-600 px-3.5 py-2 text-xs font-bold text-white transition hover:bg-navy-800 shadow-2xs cursor-pointer flex items-center gap-1.5"
                @click="startNewCourse"
              >
                <Plus class="w-3.5 h-3.5" />
                <span>{{ t('Add course') }}</span>
              </button>
            </div>
            <form class="space-y-4" @submit.prevent="saveCourse">
              <!-- Language Switcher Tabs for Course Content -->
              <div class="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-3 pb-3.5 mb-2 border-b border-slate-200 dark:border-slate-800">
                <div class="flex items-center gap-2.5">
                  <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-sky-400">
                    <Globe class="h-4 w-4" />
                  </div>
                  <div>
                    <p class="text-xs font-bold uppercase tracking-wider text-navy-900 dark:text-white">{{ t('Course Language') }}</p>
                    <p class="text-[11px] text-slate-500 dark:text-slate-400">
                      {{ courseFormLang === 'en' ? t('Editing English content') : t('Editing Khmer content (ភាសាខ្មែរ)') }}
                    </p>
                  </div>
                </div>
                <div class="inline-flex items-center rounded-xl bg-slate-100 p-1 dark:bg-slate-800/80 border border-slate-200/80 dark:border-slate-700/80 shadow-2xs">
                  <button
                    type="button"
                    @click="courseFormLang = 'en'"
                    class="inline-flex items-center gap-2 rounded-lg px-3.5 py-1.5 text-xs font-bold transition-all cursor-pointer"
                    :class="courseFormLang === 'en'
                      ? 'bg-navy-900 text-white shadow-xs dark:bg-indigo-600'
                      : 'text-slate-600 dark:text-slate-400 hover:text-navy-900 dark:hover:text-white hover:bg-slate-200/60 dark:hover:bg-slate-700/60'"
                  >
                    <span
                      class="px-1.5 py-0.5 rounded text-[9px] font-black uppercase tracking-wide"
                      :class="courseFormLang === 'en' ? 'bg-white/20 text-white' : 'bg-slate-200 text-slate-700 dark:bg-slate-700 dark:text-slate-300'"
                    >
                      EN
                    </span>
                    <span>English</span>
                    <span v-if="courseForm.title" class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  </button>
                  <button
                    type="button"
                    @click="courseFormLang = 'kh'"
                    class="inline-flex items-center gap-2 rounded-lg px-3.5 py-1.5 text-xs font-bold transition-all cursor-pointer"
                    :class="courseFormLang === 'kh'
                      ? 'bg-navy-900 text-white shadow-xs dark:bg-indigo-600'
                      : 'text-slate-600 dark:text-slate-400 hover:text-navy-900 dark:hover:text-white hover:bg-slate-200/60 dark:hover:bg-slate-700/60'"
                  >
                    <span
                      class="px-1.5 py-0.5 rounded text-[9px] font-black uppercase tracking-wide"
                      :class="courseFormLang === 'kh' ? 'bg-white/20 text-white' : 'bg-slate-200 text-slate-700 dark:bg-slate-700 dark:text-slate-300'"
                    >
                      KH
                    </span>
                    <span>ភាសាខ្មែរ</span>
                    <span v-if="courseForm.title_kh" class="w-1.5 h-1.5 rounded-full bg-emerald-400"></span>
                  </button>
                </div>
              </div>

              <!-- English Fields (Visible when English tab active) -->
              <div v-show="courseFormLang === 'en'" class="space-y-4">
                <label class="block">
                  <div class="flex items-center justify-between mb-1">
                    <span class="admin-label dark:text-slate-100 mb-0">{{ t('Course title') }}</span>
                  </div>
                  <input v-model.trim="courseForm.title" required maxlength="160" class="admin-input" placeholder="e.g. MicroBit Robotics & Embedded Systems Kit" />
                </label>
                <label class="block">
                  <span class="admin-label dark:text-slate-100">{{ t('URL slug (optional)') }}</span>
                  <input v-model.trim="courseForm.slug" maxlength="180" :placeholder="t('Generated from course title if blank')" class="admin-input" />
                </label>
                <label class="block">
                  <span class="admin-label dark:text-slate-100">{{ t('Short description') }}</span>
                  <textarea v-model.trim="courseForm.short_description" maxlength="2000" rows="3" class="admin-input resize-y py-2.5" placeholder="Brief summary of the course in English..."></textarea>
                </label>
                <div class="grid gap-4 sm:grid-cols-2">
                  <label class="block">
                    <span class="admin-label dark:text-slate-100">{{ t('Category') }}</span>
                    <input v-model.trim="courseForm.category" required maxlength="80" class="admin-input" placeholder="e.g. Robotics, IoT, Mechanical" />
                  </label>
                  <label class="block">
                    <span class="admin-label dark:text-slate-100">{{ t('Level') }}</span>
                    <input v-model.trim="courseForm.level" maxlength="80" class="admin-input" placeholder="e.g. Beginner, Intermediate, Advanced" />
                  </label>
                  <label class="block sm:col-span-2">
                    <span class="admin-label dark:text-slate-100">{{ t('Duration') }}</span>
                    <input v-model.trim="courseForm.duration" maxlength="120" class="admin-input" placeholder="e.g. 45 Hours, 6 Weeks" />
                  </label>
                </div>
                <label class="block">
                  <span class="admin-label dark:text-slate-100">{{ t('Badges') }}</span>
                  <input v-model="courseBadgesText" maxlength="300" class="admin-input" :placeholder="t('Bestseller, New, Starter (comma separated)')" />
                </label>
              </div>

              <!-- Khmer Fields (Visible when Khmer tab active) -->
              <div v-show="courseFormLang === 'kh'" class="space-y-4">
                <label class="block">
                  <div class="flex items-center justify-between mb-1">
                    <span class="admin-label dark:text-slate-100 mb-0">{{ t('Course title in Khmer') }} (ចំណងជើងវគ្គសិក្សា)</span>
                    <span v-if="courseForm.title" class="text-[11px] text-slate-400 dark:text-slate-500 italic max-w-xs truncate">EN: {{ courseForm.title }}</span>
                  </div>
                  <input v-model.trim="courseForm.title_kh" maxlength="200" class="admin-input" placeholder="ឧ. កញ្ចប់ឧបករណ៍ MicroBit Robotics & ប្រព័ន្ធបង្កប់" />
                </label>
                <label class="block">
                  <div class="flex items-center justify-between mb-1">
                    <span class="admin-label dark:text-slate-100 mb-0">{{ t('Short description in Khmer') }} (ការពិពណ៌នាសង្ខេប)</span>
                    <span v-if="courseForm.short_description" class="text-[11px] text-slate-400 dark:text-slate-500 italic max-w-xs truncate">EN: {{ courseForm.short_description }}</span>
                  </div>
                  <textarea v-model.trim="courseForm.short_description_kh" maxlength="3000" rows="3" class="admin-input resize-y py-2.5" placeholder="ការពិពណ៌នាសង្ខេបជាភាសាខ្មែរ..."></textarea>
                </label>
                <div class="grid gap-4 sm:grid-cols-2">
                  <label class="block">
                    <span class="admin-label dark:text-slate-100">{{ t('Category in Khmer') }} (ប្រភេទវគ្គសិក្សា)</span>
                    <input v-model.trim="courseForm.category_kh" maxlength="100" class="admin-input" :placeholder="courseForm.category ? `ឧ. ${t(courseForm.category)}` : 'ឧ. មនុស្សយន្ត'" />
                  </label>
                  <label class="block">
                    <span class="admin-label dark:text-slate-100">{{ t('Level in Khmer') }} (កម្រិតសិក្សា)</span>
                    <input v-model.trim="courseForm.level_kh" maxlength="100" class="admin-input" placeholder="ឧ. កម្រិតដំបូង, មធ្យម" />
                  </label>
                  <label class="block sm:col-span-2">
                    <span class="admin-label dark:text-slate-100">{{ t('Duration in Khmer') }} (រយៈពេលសិក្សា)</span>
                    <input v-model.trim="courseForm.duration_kh" maxlength="150" class="admin-input" placeholder="ឧ. ៤៥ ម៉ោង, ៦ សប្តាហ៍" />
                  </label>
                </div>
                <label class="block">
                  <span class="admin-label dark:text-slate-100">{{ t('Badges in Khmer') }} (ស្លាកសម្គាល់ជាភាសាខ្មែរ)</span>
                  <input v-model="courseBadgesKhText" maxlength="300" class="admin-input" placeholder="ឧ. ពេញនិយម, ថ្មី, កម្រិតដំបូង (សញ្ញាក្បៀសដើម្បីបំបែក)" />
                </label>
              </div>

              <!-- Shared Pricing & Publishing Settings -->
              <div class="grid gap-4 sm:grid-cols-2 pt-2 border-t border-slate-100 dark:border-slate-800">
                <div class="block">
                  <span class="admin-label dark:text-slate-100">{{ t('Language') }}</span>
                  <CustomSelect
                    v-model="courseForm.language"
                    :options="['English', 'Khmer']"
                  />
                </div>
                <div class="block">
                  <span class="admin-label dark:text-slate-100">{{ t('Status') }}</span>
                  <CustomSelect
                    v-model="courseForm.status"
                    :options="[
                      { value: 'published', label: t('published') },
                      { value: 'draft', label: t('draft') },
                      { value: 'archived', label: t('archived') }
                    ]"
                  />
                </div>
                <label class="block">
                  <span class="admin-label dark:text-slate-100">{{ t('Discount price / current price') }}</span>
                  <input v-model.number="courseForm.price" type="number" min="0" max="1000000" step="0.01" required class="admin-input" />
                </label>
                <label class="block">
                  <span class="admin-label dark:text-slate-100">{{ t('List price before discount (optional)') }}</span>
                  <input v-model.number="courseForm.original_price" type="number" min="0" max="1000000" step="0.01" class="admin-input" />
                </label>
              </div>

              <!-- Course Cover Image -->
              <label class="block">
                <span class="admin-label dark:text-slate-100">{{ t('Course cover image') }}</span>
                <div
                  class="rounded-xl border-2 border-dashed p-4 text-center transition"
                  :class="draggingImage ? 'border-navy-700 dark:border-indigo-500 bg-navy-50 dark:bg-slate-800' : 'border-slate-300 dark:border-slate-700 bg-slate-50 dark:bg-slate-800/50'"
                  @dragover.prevent="draggingImage = true"
                  @dragleave.prevent="draggingImage = false"
                  @drop.prevent="handleImageDrop"
                >
                  <img v-if="courseForm.image_url" :src="resolveImageUrl(courseForm.image_url)" alt="" class="mx-auto mb-3 max-h-44 rounded-lg object-contain" @error="$event.target.style.display = 'none'" @load="$event.target.style.display = 'block'" />
                  <p class="text-sm font-semibold text-slate-700 dark:text-slate-200">{{ t('Drag and drop a PNG or JPG image here') }}</p>
                  <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">{{ t('PNG/JPG, 5 MB maximum') }}</p>
                  <input ref="imageInput" type="file" accept=".png,.jpg,.jpeg,image/png,image/jpeg" class="sr-only" @change="handleImageSelection" />
                  <div class="flex flex-wrap items-center justify-center gap-2 mt-3">
                    <button type="button" :disabled="imageUploading" class="rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2 text-sm font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-50 cursor-pointer" @click="imageInput?.click()">
                      {{ imageUploading ? t('Uploading...') : t('Choose image') }}
                    </button>
                    <button
                      v-if="courseForm.image_url"
                      type="button"
                      class="inline-flex items-center gap-1.5 rounded-lg border border-sky-300 dark:border-sky-800 bg-sky-50 dark:bg-sky-950/40 px-3.5 py-2 text-xs font-bold text-sky-700 dark:text-sky-300 hover:bg-sky-100 dark:hover:bg-sky-900/60 cursor-pointer"
                      @click="openCoverCropForExisting"
                    >
                      <Crop class="h-3.5 w-3.5" />
                      <span>{{ t('Crop image') }}</span>
                    </button>
                    <button
                      v-if="courseForm.image_url"
                      type="button"
                      class="rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-2 text-xs font-semibold text-red-600 dark:text-red-400 hover:bg-red-50 dark:hover:bg-red-950/30 cursor-pointer"
                      @click="courseForm.image_url = ''"
                    >
                      {{ t('Remove') }}
                    </button>
                  </div>
                </div>
                <input v-model.trim="courseForm.image_url" type="text" maxlength="2000" class="admin-input mt-3" :placeholder="t('Or paste an image URL')" />
                <p v-if="isLocalFilePath(courseForm.image_url)" class="mt-1.5 text-xs text-amber-600 dark:text-amber-400 font-medium">
                  {{ t('Local file paths (e.g. C:\\...) cannot be viewed on web browsers. Please click "Choose image" above to upload your file.') }}
                </p>
              </label>

              <!-- Batch Schedule -->
              <section class="rounded-xl border border-slate-200 dark:border-slate-800 p-4">
                <div class="flex items-center justify-between gap-3">
                  <div><h3 class="text-sm font-bold text-slate-800 dark:text-white">{{ t('Batch Schedule') }}</h3><p class="mt-1 text-xs text-slate-500 dark:text-slate-300">{{ t('Schedules shown to students and seat limits are stored with this course.') }}</p></div>
                  <button type="button" class="text-xs font-bold text-navy-800 dark:text-indigo-400 underline underline-offset-2 hover:text-navy-900 dark:hover:text-indigo-300" @click="addBatchSchedule">+ {{ t('Add batch') }}</button>
                </div>
                <div v-for="(batch, index) in courseForm.batch_schedules" :key="index" class="mt-3 grid gap-2 rounded-lg bg-slate-50 dark:bg-slate-800/70 p-3 sm:grid-cols-2">
                  <div class="flex items-center justify-between sm:col-span-2"><span class="text-xs font-semibold text-slate-500 dark:text-slate-400">{{ t('Batch') }} {{ index + 1 }}</span><button type="button" class="text-xs font-semibold text-red-700 dark:text-red-400 hover:underline" @click="courseForm.batch_schedules.splice(index, 1)">{{ t('Remove') }}</button></div>
                  <label><span class="admin-label dark:text-slate-100">{{ t('Day type') }}</span><input v-model.trim="batch.day_type" class="admin-input" :placeholder="t('Weekday (Mon-Fri)')" /></label>
                  <label><span class="admin-label dark:text-slate-100">{{ t('Time slot') }}</span><input v-model.trim="batch.time_slot" class="admin-input" :placeholder="t('Morning / Afternoon')" /></label>
                  <label><span class="admin-label dark:text-slate-100">{{ t('Start time') }}</span><input v-model.trim="batch.start_time" class="admin-input" :placeholder="t('8:00 AM')" /></label>
                  <label><span class="admin-label dark:text-slate-100">{{ t('End time') }}</span><input v-model.trim="batch.end_time" class="admin-input" :placeholder="t('1:00 PM')" /></label>
                  <label><span class="admin-label dark:text-slate-100">{{ t('Max seat capacity') }}</span><input v-model.number="batch.max_seats" type="number" min="1" max="1000" class="admin-input" /></label>
                  <label class="flex items-center gap-2 pt-7 text-sm font-semibold text-slate-700 dark:text-slate-200"><input v-model="batch.active" type="checkbox" />{{ t('Active') }}</label>
                </div>
              </section>

              <!-- Course Modules -->
              <section class="rounded-xl border border-slate-200 dark:border-slate-800 p-4">
                <div class="flex items-center justify-between gap-3">
                  <div>
                    <h3 class="text-sm font-bold text-slate-800 dark:text-white">{{ t('Course modules') }}</h3>
                    <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                      {{ courseFormLang === 'en' ? t('Add and edit modules in English.') : t('Add and edit modules in Khmer (ភាសាខ្មែរ).') }}
                    </p>
                  </div>
                  <button type="button" class="text-xs font-bold text-navy-800 dark:text-indigo-400 underline underline-offset-2 hover:text-navy-900 dark:hover:text-indigo-300" @click="addModule">
                    + {{ t('Add module') }}
                  </button>
                </div>
                <div v-for="(module, index) in courseForm.modules" :key="index" class="mt-3 space-y-3 rounded-lg bg-slate-50 dark:bg-slate-800/70 p-3">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-semibold text-slate-500 dark:text-slate-400">{{ t('Module') }} {{ index + 1 }}</span>
                    <button type="button" class="text-xs font-semibold text-red-700 dark:text-red-400 hover:underline" @click="courseForm.modules.splice(index, 1)">{{ t('Remove') }}</button>
                  </div>

                  <!-- English Module Fields -->
                  <div v-if="courseFormLang === 'en'" class="space-y-3">
                    <label class="block">
                      <span class="admin-label dark:text-slate-100">{{ t('Module title') }}</span>
                      <input v-model.trim="module.title" :aria-label="`${t('Module')} ${index + 1} ${t('title')}`" :placeholder="t('Module title')" class="admin-input" />
                    </label>
                    <label class="block">
                      <span class="admin-label dark:text-slate-100">{{ t('Module description') }}</span>
                      <textarea v-model.trim="module.description" :aria-label="`${t('Module')} ${index + 1} ${t('description')}`" :placeholder="t('Module description')" maxlength="1000" rows="2" class="admin-input resize-y py-2.5"></textarea>
                    </label>
                  </div>

                  <!-- Khmer Module Fields -->
                  <div v-else class="space-y-3">
                    <label class="block">
                      <div class="flex items-center justify-between mb-1">
                        <span class="admin-label dark:text-slate-100 mb-0">{{ t('Module title in Khmer') }} (ចំណងជើងម៉ូឌុល)</span>
                        <span v-if="module.title" class="text-[11px] text-slate-400 dark:text-slate-500 italic max-w-xs truncate">EN: {{ module.title }}</span>
                      </div>
                      <input v-model.trim="module.title_kh" :aria-label="`${t('Module')} ${index + 1} ${t('Module title in Khmer')}`" placeholder="ចំណងជើងម៉ូឌុលជាភាសាខ្មែរ" class="admin-input" />
                    </label>
                    <label class="block">
                      <div class="flex items-center justify-between mb-1">
                        <span class="admin-label dark:text-slate-100 mb-0">{{ t('Module description in Khmer') }} (ការពិពណ៌នាម៉ូឌុល)</span>
                        <span v-if="module.description" class="text-[11px] text-slate-400 dark:text-slate-500 italic max-w-xs truncate">EN: {{ module.description }}</span>
                      </div>
                      <textarea v-model.trim="module.description_kh" :aria-label="`${t('Module')} ${index + 1} ${t('Module description in Khmer')}`" placeholder="ការពិពណ៌នាម៉ូឌុលជាភាសាខ្មែរ..." maxlength="1000" rows="2" class="admin-input resize-y py-2.5"></textarea>
                    </label>
                  </div>

                  <div class="rounded-lg border border-dashed border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 p-3">
                    <img
                      v-if="module.image_url"
                      :src="resolveImageUrl(module.image_url)"
                      alt=""
                      class="mb-3 h-32 w-full rounded-md object-cover"
                      @error="$event.target.style.display = 'none'"
                      @load="$event.target.style.display = 'block'"
                    />
                    <div class="flex flex-wrap items-center gap-2">
                      <input
                        :ref="(element) => setModuleImageInput(element, index)"
                        type="file"
                        accept=".png,.jpg,.jpeg,image/png,image/jpeg"
                        class="sr-only"
                        @change="handleModuleImageSelection($event, module)"
                      />
                      <button
                        type="button"
                        :disabled="moduleImageUploading"
                        class="rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-2 text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-50 cursor-pointer"
                        @click="moduleImageInputs[index]?.click()"
                      >
                        {{ moduleImageUploading ? t('Uploading...') : t('Upload module photo') }}
                      </button>
                      <button
                        v-if="module.image_url"
                        type="button"
                        class="inline-flex items-center gap-1 rounded-lg border border-sky-300 dark:border-sky-800 bg-sky-50 dark:bg-sky-950/40 px-2.5 py-1.5 text-xs font-bold text-sky-700 dark:text-sky-300 hover:bg-sky-100 dark:hover:bg-sky-900/60 cursor-pointer"
                        @click="openModuleCropForExisting(module)"
                      >
                        <Crop class="h-3 w-3" />
                        <span>{{ t('Crop photo') }}</span>
                      </button>
                      <button
                        v-if="module.image_url"
                        type="button"
                        class="text-xs font-semibold text-red-700 dark:text-red-400 hover:underline cursor-pointer"
                        @click="module.image_url = ''"
                      >
                        {{ t('Remove image') }}
                      </button>
                    </div>
                    <input
                      v-model.trim="module.image_url"
                      type="url"
                      maxlength="2000"
                      class="admin-input mt-3"
                      :placeholder="t('Or paste a module image URL')"
                    />
                  </div>
                  <label class="block">
                    <span class="admin-label dark:text-slate-100">{{ t('Module icon and label') }}</span>
                    <input
                      v-model.trim="module.icon_type"
                      type="text"
                      maxlength="100"
                      class="admin-input"
                      :placeholder="t('e.g. Core PCB, Microcontroller, Sensors')"
                    />
                  </label>
                </div>
              </section>

              <!-- Hardware Specifications -->
              <section class="rounded-xl border border-slate-200 dark:border-slate-800 p-4">
                <div class="flex items-center justify-between gap-3">
                  <div>
                    <h3 class="text-sm font-bold text-slate-800 dark:text-white">{{ t('Hardware specifications') }}</h3>
                    <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                      {{ courseFormLang === 'en' ? t('Provide topic titles and bullet items in English.') : t('Provide topic titles and bullet items in Khmer (ភាសាខ្មែរ).') }}
                    </p>
                  </div>
                  <button type="button" class="text-xs font-bold text-navy-800 dark:text-indigo-400 underline underline-offset-2 hover:text-navy-900 dark:hover:text-indigo-300" @click="addHardwareSpec">
                    + {{ t('Add specification') }}
                  </button>
                </div>
                <div v-for="(spec, index) in courseForm.hardware_specs" :key="index" class="mt-3 space-y-3 rounded-lg bg-slate-50 dark:bg-slate-800/70 p-3">
                  <div class="flex items-center justify-between">
                    <span class="text-xs font-semibold text-slate-500 dark:text-slate-400">{{ t('Specification') }} {{ index + 1 }}</span>
                    <button type="button" class="text-xs font-semibold text-red-700 dark:text-red-400 hover:underline" @click="courseForm.hardware_specs.splice(index, 1)">{{ t('Remove') }}</button>
                  </div>

                  <!-- English Spec Fields -->
                  <div v-if="courseFormLang === 'en'" class="space-y-3">
                    <label class="block">
                      <span class="admin-label dark:text-slate-100">{{ t('Specification title') }}</span>
                      <input v-model.trim="spec.title" :placeholder="t('Specification title')" class="admin-input" />
                    </label>
                    <label class="block">
                      <span class="admin-label dark:text-slate-100">{{ t('Items') }} ({{ t('Add one item per line') }})</span>
                      <textarea
                        :value="spec.items.join('\n')"
                        :placeholder="t('Add one item per line')"
                        rows="3"
                        class="admin-input resize-y py-2.5"
                        @input="updateSpecItems(index, $event.target.value)"
                      ></textarea>
                    </label>
                  </div>

                  <!-- Khmer Spec Fields -->
                  <div v-else class="space-y-3">
                    <label class="block">
                      <div class="flex items-center justify-between mb-1">
                        <span class="admin-label dark:text-slate-100 mb-0">{{ t('Specification title in Khmer') }} (ចំណងជើងលក្ខណៈបច្ចេកទេស)</span>
                        <span v-if="spec.title" class="text-[11px] text-slate-400 dark:text-slate-500 italic max-w-xs truncate">EN: {{ spec.title }}</span>
                      </div>
                      <input v-model.trim="spec.title_kh" placeholder="ចំណងជើងលក្ខណៈបច្ចេកទេសជាភាសាខ្មែរ" class="admin-input" />
                    </label>
                    <label class="block">
                      <span class="admin-label dark:text-slate-100">{{ t('Items in Khmer') }} ({{ t('Add one item per line in Khmer') }})</span>
                      <textarea
                        :value="(spec.items_kh || []).join('\n')"
                        :placeholder="t('Add one item per line in Khmer')"
                        rows="3"
                        class="admin-input resize-y py-2.5"
                        @input="updateSpecKhItems(index, $event.target.value)"
                      ></textarea>
                    </label>
                  </div>
                </div>
              </section>
              <p v-if="formError" class="rounded-lg bg-red-50 dark:bg-red-950/40 border border-red-200 dark:border-red-900/40 px-3 py-2 text-sm text-red-700 dark:text-red-300" role="alert">{{ formError }}</p>
              <div class="flex gap-3 pt-1">
                <button type="submit" :disabled="busy" class="admin-primary-button">
                  {{ busy ? t('Saving...') : t('Publish changes') }}
                </button>
                <button v-if="editingId" type="button" class="rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2.5 text-sm font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700" @click="startNewCourse">
                  {{ t('Cancel') }}
                </button>
              </div>
            </form>
          </section>
        </div>
      </main>
    </div>
  </template>

  <!-- Image Cropper Modal for Course Cover & Modules -->
  <ImageCropperModal
    v-model="cropperOpen"
    :image-src="cropperImageSrc"
    :title="cropperTitle"
    :default-ratio="cropperDefaultRatio"
    :original-file="cropperOriginalFile"
    @crop="onCropperApply"
    @use-original="onCropperUseOriginal"
  />
</div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import {
  ArrowDown,
  ArrowUp,
  ArrowUpRight,
  ArrowUpToLine,
  BookOpen,
  Check,
  ChevronLeft,
  ChevronRight,
  Copy,
  CreditCard,
  ExternalLink,
  FileSpreadsheet,
  Globe,
  GripVertical,
  Activity,
  Eye,
  LayoutDashboard,
  RefreshCw,
  ShieldCheck,
  LogOut,
  Menu,
  Moon,
  PieChart,
  Plus,
  Printer,
  Search,
  Settings,
  Sun,
  Tag,
  TrendingUp,
  Users,
  UserCog,
  KeyRound,
  Trash2,
  Pencil,
  EyeOff,
  Mail,
  X,
  Crop,
} from 'lucide-vue-next'
import { useLanguage } from '../i18n'
import { useTheme } from '../composables/useTheme'
import { adminService } from '../services/api'
import { formatCambodiaTime } from '../utils/date'
import CatThemeSwitch from '../components/common/CatThemeSwitch.vue'
import CustomSelect from '../components/common/CustomSelect.vue'
import DatePicker from '../components/common/DatePicker.vue'
import AdminPagination from '../components/common/AdminPagination.vue'
import ImageCropperModal from '../components/common/ImageCropperModal.vue'
import { resolveImageUrl, isLocalFilePath } from '../utils/image'

const moduleIconOptions = computed(() => [
  { value: 'Core PCB', label: t('Core PCB') },
  { value: 'Telemetry', label: t('Telemetry') },
  { value: 'Motors', label: t('Motors') },
  { value: 'Frame', label: t('Frame') },
  { value: 'cpu', label: 'cpu' },
  { value: 'activity', label: 'activity' },
  { value: 'settings', label: 'settings' },
  { value: 'compass', label: 'compass' },
  { value: 'package', label: 'package' },
  { value: 'book', label: 'book' },
])

const router = useRouter()
const { locale, setLocale, t } = useLanguage()
const { isDark, toggleTheme } = useTheme()
const authenticated = ref(false)
const sidebarOpen = ref(false)
const sidebarCollapsed = ref(localStorage.getItem('admin_sidebar_collapsed') === 'true')
const navItemRefs = ref([])
const highlightStyle = ref({})
const isTitleSwapping = ref(false)

function updateHighlight() {
  nextTick(() => {
    const idx = adminSections.findIndex(s => s.id === activeSection.value)
    if (idx !== -1 && navItemRefs.value[idx]) {
      const el = navItemRefs.value[idx]
      highlightStyle.value = {
        top: `${el.offsetTop}px`,
        height: `${el.offsetHeight}px`,
        transitionTimingFunction: 'cubic-bezier(0.34, 1.45, 0.64, 1)',
      }
    }
  })
}

function toggleSidebarCollapse() {
  sidebarCollapsed.value = !sidebarCollapsed.value
  localStorage.setItem('admin_sidebar_collapsed', String(sidebarCollapsed.value))
  setTimeout(updateHighlight, 320)
}
const loadingCourses = ref(false)
const busy = ref(false)
const courses = ref([])
const overview = ref({})
const enrollments = ref([])
const payments = ref([])
const coupons = ref([])
const editingId = ref('')
const errorMessage = ref('')
const formError = ref('')
const successMessage = ref('')
const activeSection = ref('dashboard')

const chartMetric = ref('revenue')
const hoveredPoint = ref(null)

const monthlyChartData = computed(() => {
  const months = [
    { key: '2026-05', label: 'May', fullLabel: 'May 2026', revenue: 420, students: 4 },
    { key: '2026-06', label: 'Jun', fullLabel: 'Jun 2026', revenue: 890, students: 8 },
    { key: '2026-07', label: 'Jul', fullLabel: 'Jul 2026', revenue: 1450, students: 13 },
    { key: '2026-08', label: 'Aug', fullLabel: 'Aug 2026', revenue: 1980, students: 17 },
    { key: '2026-09', label: 'Sep', fullLabel: 'Sep 2026', revenue: 2650, students: 24 },
    { key: '2026-10', label: 'Oct', fullLabel: 'Oct 2026', revenue: 3120, students: 28 },
  ]

  if (payments.value && payments.value.length > 0) {
    const revenueByMonth = {}
    for (const p of payments.value) {
      if (p.created_at && p.status === 'paid') {
        const ym = p.created_at.slice(0, 7)
        revenueByMonth[ym] = (revenueByMonth[ym] || 0) + (Number(p.amount_due) || 0)
      }
    }
    const studentsByMonth = {}
    for (const e of enrollments.value) {
      if (e.created_at) {
        const ym = e.created_at.slice(0, 7)
        studentsByMonth[ym] = (studentsByMonth[ym] || 0) + 1
      }
    }

    const currentYm = '2026-10'
    if (revenueByMonth[currentYm] !== undefined) {
      months[5].revenue = Number(revenueByMonth[currentYm].toFixed(2))
    } else if (overview.value?.total_revenue) {
      months[5].revenue = Number(overview.value.total_revenue)
    }
    if (studentsByMonth[currentYm] !== undefined) {
      months[5].students = studentsByMonth[currentYm]
    } else if (overview.value?.active_enrollments) {
      months[5].students = Number(overview.value.active_enrollments)
    }
  } else {
    if (overview.value?.total_revenue) {
      months[5].revenue = Number(overview.value.total_revenue)
    }
    if (overview.value?.active_enrollments) {
      months[5].students = Number(overview.value.active_enrollments)
    }
  }

  return months
})

const maxChartRevenue = computed(() => {
  const max = Math.max(...monthlyChartData.value.map((d) => d.revenue), 1000)
  return Math.ceil(max / 500) * 500
})

const maxChartStudents = computed(() => {
  const max = Math.max(...monthlyChartData.value.map((d) => d.students), 10)
  return Math.ceil(max / 5) * 5
})

const chartPoints = computed(() => {
  const data = monthlyChartData.value
  const left = 50
  const width = 580
  const top = 20
  const height = 150
  const bottom = top + height
  const xStep = width / (data.length - 1)

  return data.map((d, i) => {
    const x = left + i * xStep
    const revRatio = Math.min(1, Math.max(0, d.revenue / maxChartRevenue.value))
    const yRev = bottom - revRatio * height

    const stuRatio = Math.min(1, Math.max(0, d.students / maxChartStudents.value))
    const yStu = bottom - stuRatio * height

    return {
      index: i,
      label: d.label,
      fullLabel: d.fullLabel,
      revenue: d.revenue,
      students: d.students,
      x: Number(x.toFixed(1)),
      yRevenue: Number(yRev.toFixed(1)),
      yStudents: Number(yStu.toFixed(1)),
    }
  })
})

const revenueAreaPath = computed(() => {
  const pts = chartPoints.value
  if (!pts.length) return ''
  const bottom = 170
  let d = `M ${pts[0].x} ${pts[0].yRevenue}`
  for (let i = 1; i < pts.length; i++) {
    const prev = pts[i - 1]
    const curr = pts[i]
    const cp1x = prev.x + (curr.x - prev.x) / 2
    const cp2x = prev.x + (curr.x - prev.x) / 2
    d += ` C ${cp1x} ${prev.yRevenue}, ${cp2x} ${curr.yRevenue}, ${curr.x} ${curr.yRevenue}`
  }
  const last = pts[pts.length - 1]
  d += ` L ${last.x} ${bottom} L ${pts[0].x} ${bottom} Z`
  return d
})

const revenueLinePath = computed(() => {
  const pts = chartPoints.value
  if (!pts.length) return ''
  let d = `M ${pts[0].x} ${pts[0].yRevenue}`
  for (let i = 1; i < pts.length; i++) {
    const prev = pts[i - 1]
    const curr = pts[i]
    const cp1x = prev.x + (curr.x - prev.x) / 2
    const cp2x = prev.x + (curr.x - prev.x) / 2
    d += ` C ${cp1x} ${prev.yRevenue}, ${cp2x} ${curr.yRevenue}, ${curr.x} ${curr.yRevenue}`
  }
  return d
})

const studentsAreaPath = computed(() => {
  const pts = chartPoints.value
  if (!pts.length) return ''
  const bottom = 170
  let d = `M ${pts[0].x} ${pts[0].yStudents}`
  for (let i = 1; i < pts.length; i++) {
    const prev = pts[i - 1]
    const curr = pts[i]
    const cp1x = prev.x + (curr.x - prev.x) / 2
    const cp2x = prev.x + (curr.x - prev.x) / 2
    d += ` C ${cp1x} ${prev.yStudents}, ${cp2x} ${curr.yStudents}, ${curr.x} ${curr.yStudents}`
  }
  const last = pts[pts.length - 1]
  d += ` L ${last.x} ${bottom} L ${pts[0].x} ${bottom} Z`
  return d
})

const studentsLinePath = computed(() => {
  const pts = chartPoints.value
  if (!pts.length) return ''
  let d = `M ${pts[0].x} ${pts[0].yStudents}`
  for (let i = 1; i < pts.length; i++) {
    const prev = pts[i - 1]
    const curr = pts[i]
    const cp1x = prev.x + (curr.x - prev.x) / 2
    const cp2x = prev.x + (curr.x - prev.x) / 2
    d += ` C ${cp1x} ${prev.yStudents}, ${cp2x} ${curr.yStudents}, ${curr.x} ${curr.yStudents}`
  }
  return d
})

const categoryDistribution = computed(() => {
  const counts = { Robotics: 0, IoT: 0, Mechanical: 0, Electronics: 0, ROS: 0 }
  const courseList = courses.value || []
  for (const c of courseList) {
    const cat = c.category || 'Robotics'
    counts[cat] = (counts[cat] || 0) + 1
  }

  const colors = {
    Robotics: '#0284c7', // Sky Blue
    IoT: '#10b981',      // Emerald
    Mechanical: '#f59e0b',// Amber
    Electronics: '#6366f1', // Indigo
    ROS: '#8b5cf6',       // Violet
  }

  const total = Object.values(counts).reduce((a, b) => a + b, 0) || 1
  const categories = Object.keys(counts).map((name) => {
    const count = counts[name]
    const percent = Math.round((count / total) * 100)
    return {
      name,
      count,
      percent,
      color: colors[name] || '#64748b',
    }
  })

  // Circumference for r=46
  const circumference = 2 * Math.PI * 46
  let currentOffset = 0
  const slices = categories.map((cat) => {
    const dashLength = (cat.percent / 100) * circumference
    const slice = {
      ...cat,
      dashArray: `${dashLength} ${circumference}`,
      dashOffset: -currentOffset,
    }
    currentOffset += dashLength
    return slice
  })

  return {
    total: courseList.length,
    slices,
    categories,
  }
})
const studentSearch = ref('')
const courseSearch = ref('')
const selectedStudent = ref(null)
const imageInput = ref(null)
const moduleImageInputs = ref([])
const qrImageInput = ref(null)
const imageUploading = ref(false)
const moduleImageUploading = ref(false)
const qrImageUploading = ref(false)
const draggingImage = ref(false)
const couponError = ref('')
const settingsError = ref('')
const settingsSaved = ref(false)
const editingCoupon = ref('')
const couponForm = reactive(emptyCoupon())
const settingsForm = reactive(emptySettings())

const adminSections = [
  {
    id: 'dashboard',
    title: 'Dashboard Overview',
    icon: LayoutDashboard,
    description: 'KPI cards, recent enrollment activity, and top courses.',
    summary: 'Revenue, enrollment, QR payment, and course metrics.',
    features: ['KPI Cards', 'Recent enrollments table', 'Top selling courses', 'Quick search and activity feed'],
  },
  {
    id: 'courses',
    title: 'Courses & Schedules',
    icon: BookOpen,
    description: 'Manage course fields, cover images, schedule batches, badges, and publishing status.',
    summary: 'Edit course details, upload images, and set batch seat limits.',
    features: ['Course & batch manager', 'PNG/JPG cover upload', 'Batch schedule & capacity', 'Badges and publish status'],
  },
  {
    id: 'students',
    title: 'Student Enrollments',
    icon: Users,
    description: 'Review and update student enrollment records.',
    summary: 'Search student records, preferences, and enrollment status.',
    features: ['Personal and education information', 'Schedule preferences', 'Pending / confirmed / cancelled', 'Export roster Excel'],
  },
  {
    id: 'payments',
    title: 'Payments & QR Checkout',
    icon: CreditCard,
    description: 'Review transaction details and manually update verified payment statuses.',
    summary: 'Monitor checkout records and payment status history.',
    features: ['Transaction log', 'Paid / pending / expired / refunded', 'Manual status override', 'Payment timeline fields'],
  },
  {
    id: 'promos',
    title: 'Promo & Coupons',
    icon: Tag,
    description: 'Create and manage discount codes.',
    summary: 'Set coupon type, value, usage limits, expiry, and active state.',
    features: ['Percent or fixed discount', 'Usage count and maximum', 'Expiry date', 'Activate or deactivate'],
  },
  {
    id: 'users',
    title: 'User Accounts',
    icon: UserCog,
    description: 'Manage registered user accounts, profiles, passwords, and access.',
    summary: 'View registered users, edit profile information, change passwords, and delete accounts.',
    features: ['User directory', 'Profile data editor', 'Password change', 'Account deletion'],
  },
  {
    id: 'logs',
    title: 'Traffic & Login Logs',
    icon: Activity,
    description: 'Track visitor traffic and student/admin sign-in history.',
    summary: 'Monitor total page visits, unique visitors, and authenticated user logins with device, method, and timestamp information.',
    features: ['User and Admin login logs', 'Website traffic & visit counter', 'IP & Device breakdown', 'Real-time timeline'],
  },
  {
    id: 'settings',
    title: 'Site Settings & CMS',
    icon: Settings,
    description: 'Edit public About metrics, contact/footer details, and payment setup.',
    summary: 'Manage the site statistics, contact information, QR setup, and checkout timer.',
    features: ['About page stats', 'Merchant QR and bank details', 'Contact / footer information', 'Checkout session duration'],
  },
]
const currentSection = computed(() => adminSections.find((section) => section.id === activeSection.value) || adminSections[0])

function emptyCoupon() {
  return { code: '', discount_type: 'percent', value: 10, max_usage: null, expires_at: '', active: true }
}

function emptySettings() {
  return {
    about_courses: '15+',
    about_learning: '100%',
    about_mentors: '12+',
    about_projects: '500+',
    contact_email: '',
    contact_phone: '',
    footer_description: '',
    merchant_qr_url: '',
    merchant_bank_info: '',
    payment_session_minutes: 15,
  }
}

const aboutSettings = {
  about_courses: { label: 'Hands-On Tech Courses' },
  about_learning: { label: 'Project-Based Learning' },
  about_mentors: { label: 'Industry Mentors' },
  about_projects: { label: 'Student Projects Built' },
}

const courseFormLang = ref('en')

const emptyCourse = () => ({
  title: '',
  title_kh: '',
  slug: '',
  short_description: '',
  short_description_kh: '',
  category: 'Robotics',
  category_kh: '',
  section_group: 'Courses',
  level: '',
  level_kh: '',
  price: 0,
  original_price: null,
  language: 'English',
  duration: '',
  duration_kh: '',
  image_url: '',
  status: 'published',
  badges: [],
  badges_kh: [],
  batch_schedules: [],
  modules: [],
  hardware_specs: [],
})
const courseForm = reactive(emptyCourse())
const courseBadgesText = computed({
  get: () => courseForm.badges.join(', '),
  set: (value) => { courseForm.badges = value.split(',').map((badge) => badge.trim()).filter(Boolean) },
})
const courseBadgesKhText = computed({
  get: () => (courseForm.badges_kh || []).join(', '),
  set: (value) => { courseForm.badges_kh = value.split(',').map((badge) => badge.trim()).filter(Boolean) },
})
const coursePage = ref(1)
const coursePerPage = ref(6)

const filteredCourses = computed(() => {
  const query = courseSearch.value.trim().toLowerCase()
  if (!query) return courses.value
  return courses.value.filter((course) =>
    [course.title, course.category, course.slug, course.short_description, course.status]
      .some((value) => String(value || '').toLowerCase().includes(query)),
  )
})

const totalCoursePages = computed(() =>
  Math.max(1, Math.ceil(filteredCourses.value.length / coursePerPage.value))
)

const paginatedCourses = computed(() => {
  const start = (coursePage.value - 1) * coursePerPage.value
  return filteredCourses.value.slice(start, start + coursePerPage.value)
})

const courseDisplayPages = computed(() => {
  const pages = []
  const maxButtons = 5
  let start = Math.max(1, coursePage.value - Math.floor(maxButtons / 2))
  let end = start + maxButtons - 1

  if (end > totalCoursePages.value) {
    end = totalCoursePages.value
    start = Math.max(1, end - maxButtons + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})

const reorderAllMode = ref(false)
const draggedCourseIndex = ref(null)
const dragOverCourseIndex = ref(null)
const isReordering = ref(false)

const displayedCourses = computed(() => {
  if (reorderAllMode.value || courseSearch.value.trim()) {
    return filteredCourses.value
  }
  return paginatedCourses.value
})

function getCourseGlobalIndex(localIndex) {
  if (reorderAllMode.value || courseSearch.value.trim()) {
    return localIndex
  }
  return (coursePage.value - 1) * coursePerPage.value + localIndex
}

function handleCourseDragStart(event, course, index) {
  draggedCourseIndex.value = index
  event.dataTransfer.effectAllowed = 'move'
  event.dataTransfer.setData('text/plain', course.id)
}

function handleCourseDragOver(event, index) {
  event.preventDefault()
  if (draggedCourseIndex.value === null || draggedCourseIndex.value === index) return
  dragOverCourseIndex.value = index
}

function handleCourseDragLeave(event, index) {
  if (dragOverCourseIndex.value === index) {
    dragOverCourseIndex.value = null
  }
}

async function handleCourseDrop(event, dropIndex) {
  event.preventDefault()
  const fromIndex = draggedCourseIndex.value
  draggedCourseIndex.value = null
  dragOverCourseIndex.value = null

  if (fromIndex === null || fromIndex === dropIndex) return

  const fromGlobal = getCourseGlobalIndex(fromIndex)
  const toGlobal = getCourseGlobalIndex(dropIndex)

  const reordered = [...courses.value]
  const [moved] = reordered.splice(fromGlobal, 1)
  reordered.splice(toGlobal, 0, moved)
  courses.value = reordered

  await persistCourseOrder()
}

function handleCourseDragEnd() {
  draggedCourseIndex.value = null
  dragOverCourseIndex.value = null
}

async function moveCourseToTop(course) {
  const currentIndex = courses.value.findIndex((c) => c.id === course.id)
  if (currentIndex <= 0) return
  const reordered = [...courses.value]
  const [moved] = reordered.splice(currentIndex, 1)
  reordered.unshift(moved)
  courses.value = reordered
  await persistCourseOrder()
}

async function moveCourseUp(course) {
  const currentIndex = courses.value.findIndex((c) => c.id === course.id)
  if (currentIndex <= 0) return
  const reordered = [...courses.value]
  const [moved] = reordered.splice(currentIndex, 1)
  reordered.splice(currentIndex - 1, 0, moved)
  courses.value = reordered
  await persistCourseOrder()
}

async function moveCourseDown(course) {
  const currentIndex = courses.value.findIndex((c) => c.id === course.id)
  if (currentIndex === -1 || currentIndex >= courses.value.length - 1) return
  const reordered = [...courses.value]
  const [moved] = reordered.splice(currentIndex, 1)
  reordered.splice(currentIndex + 1, 0, moved)
  courses.value = reordered
  await persistCourseOrder()
}

async function persistCourseOrder() {
  try {
    isReordering.value = true
    const courseIds = courses.value.map((c) => c.id)
    await adminService.reorderCourses(courseIds)
    successMessage.value = t('Courses reordered successfully! Changes are live on the website.')
    setTimeout(() => {
      if (successMessage.value === t('Courses reordered successfully! Changes are live on the website.')) {
        successMessage.value = ''
      }
    }, 4000)
  } catch (error) {
    console.error('Failed to save course order:', error)
    errorMessage.value = t('Failed to save course order. Please try again.')
  } finally {
    isReordering.value = false
  }
}

watch(courseSearch, () => {
  coursePage.value = 1
})

watch(totalCoursePages, (newTotal) => {
  if (coursePage.value > newTotal) {
    coursePage.value = newTotal
  }
})
const filteredEnrollments = computed(() => {
  const query = studentSearch.value.toLowerCase()
  if (!query) return enrollments.value
  return enrollments.value.filter((record) =>
    [record.student_name, record.email, record.course_title, record.phone_number]
      .some((value) => String(value || '').toLowerCase().includes(query)),
  )
})

const studentPage = ref(1)
const studentPerPage = ref(8)
const totalStudentPages = computed(() =>
  Math.max(1, Math.ceil(filteredEnrollments.value.length / studentPerPage.value))
)
const paginatedEnrollments = computed(() => {
  const start = (studentPage.value - 1) * studentPerPage.value
  return filteredEnrollments.value.slice(start, start + studentPerPage.value)
})
watch(studentSearch, () => {
  studentPage.value = 1
})
watch(totalStudentPages, (newTotal) => {
  if (studentPage.value > newTotal) {
    studentPage.value = newTotal
  }
})

const paymentPage = ref(1)
const paymentPerPage = ref(8)
const totalPaymentPages = computed(() =>
  Math.max(1, Math.ceil(payments.value.length / paymentPerPage.value))
)
const paginatedPayments = computed(() => {
  const start = (paymentPage.value - 1) * paymentPerPage.value
  return payments.value.slice(start, start + paymentPerPage.value)
})
watch(totalPaymentPages, (newTotal) => {
  if (paymentPage.value > newTotal) {
    paymentPage.value = newTotal
  }
})

const couponPage = ref(1)
const couponPerPage = ref(6)
const totalCouponPages = computed(() =>
  Math.max(1, Math.ceil(coupons.value.length / couponPerPage.value))
)
const paginatedCoupons = computed(() => {
  const start = (couponPage.value - 1) * couponPerPage.value
  return coupons.value.slice(start, start + couponPerPage.value)
})
watch(totalCouponPages, (newTotal) => {
  if (couponPage.value > newTotal) {
    couponPage.value = newTotal
  }
})

// --- User Accounts State ---
const users = ref([])
const usersLoading = ref(false)
const userSearch = ref('')
const userMethodFilter = ref('all') // 'all' | 'email' | 'google'
const userVerifiedFilter = ref('all') // 'all' | 'verified' | 'unverified'
const userPage = ref(1)
const userPerPage = ref(10)

// User Modals
const editingUser = ref(null)
const userEditForm = reactive({
  id: '',
  full_name: '',
  email: '',
  phone: '',
  telegram: '',
  date_of_birth: '',
  location: '',
  qualification: '',
  qualification_other: '',
  occupation: '',
  experience: '',
  is_verified: true,
})
const userEditBusy = ref(false)
const userEditError = ref('')

const passwordTargetUser = ref(null)
const passwordForm = reactive({
  newPassword: '',
  confirmPassword: '',
})
const showNewPassword = ref(false)
const passwordBusy = ref(false)
const passwordError = ref('')

const deleteTargetUser = ref(null)
const deleteBusy = ref(false)
const deleteError = ref('')

const totalUsersCount = computed(() => users.value.length)
const emailUsersCount = computed(() => users.value.filter((u) => !u.google_sub).length)
const googleUsersCount = computed(() => users.value.filter((u) => !!u.google_sub).length)
const verifiedUsersCount = computed(() => users.value.filter((u) => u.is_verified === 1).length)

const filteredUsers = computed(() => {
  const q = (userSearch.value || '').trim().toLowerCase()
  return users.value.filter((user) => {
    if (q) {
      const matchName = (user.full_name || '').toLowerCase().includes(q)
      const matchEmail = (user.email || '').toLowerCase().includes(q)
      const matchPhone = (user.phone || '').toLowerCase().includes(q)
      const matchTg = (user.telegram || '').toLowerCase().includes(q)
      const matchId = (user.id || '').toLowerCase().includes(q)
      if (!matchName && !matchEmail && !matchPhone && !matchTg && !matchId) {
        return false
      }
    }
    if (userMethodFilter.value === 'email' && user.google_sub) return false
    if (userMethodFilter.value === 'google' && !user.google_sub) return false
    if (userVerifiedFilter.value === 'verified' && user.is_verified !== 1) return false
    if (userVerifiedFilter.value === 'unverified' && user.is_verified === 1) return false
    return true
  })
})

const totalUserPages = computed(() =>
  Math.max(1, Math.ceil(filteredUsers.value.length / userPerPage.value))
)

const paginatedUsers = computed(() => {
  const start = (userPage.value - 1) * userPerPage.value
  return filteredUsers.value.slice(start, start + userPerPage.value)
})

watch(totalUserPages, (newTotal) => {
  if (userPage.value > newTotal) {
    userPage.value = newTotal
  }
})

watch([userSearch, userMethodFilter, userVerifiedFilter], () => {
  userPage.value = 1
})

function selectSection(sectionId) {
  if (activeSection.value !== sectionId) {
    isTitleSwapping.value = true
    setTimeout(() => {
      isTitleSwapping.value = false
    }, 180)
  }
  activeSection.value = sectionId
  updateHighlight()
  sidebarOpen.value = false
  errorMessage.value = ''
  successMessage.value = ''
  if (sectionId === 'logs') {
    loadLogsData()
  } else if (sectionId === 'users') {
    loadUsersData()
  }
}

function setCourseForm(course = emptyCourse()) {
  Object.assign(courseForm, emptyCourse(), course, {
    title_kh: course.title_kh ?? '',
    short_description_kh: course.short_description_kh ?? '',
    category_kh: course.category_kh ?? '',
    level_kh: course.level_kh ?? '',
    duration_kh: course.duration_kh ?? '',
    badges_kh: [...(course.badges_kh ?? [])],
    original_price: course.original_price ?? null,
    level: course.level ?? '',
    duration: course.duration ?? '',
    image_url: course.image_url ?? '',
    status: course.status ?? 'published',
    badges: [...(course.badges ?? [])],
    batch_schedules: (course.batch_schedules ?? []).map((batch) => ({ ...batch })),
    modules: (course.modules ?? []).map((module) => ({
      ...module,
      title_kh: module.title_kh ?? '',
      description_kh: module.description_kh ?? '',
    })),
    hardware_specs: (course.hardware_specs ?? []).map((spec) => ({
      ...spec,
      title_kh: spec.title_kh ?? '',
      items: [...(spec.items ?? [])],
      items_kh: [...(spec.items_kh ?? [])],
    })),
  })
}

function errorDetail(error, fallback) {
  return error.response?.data?.detail || error.message || fallback
}

async function loadAdminData() {
  loadingCourses.value = true
  try {
    const [courseResult, overviewResult, enrollmentResult, paymentResult, couponResult, settingsResult, usersResult] = await Promise.all([
      adminService.getCourses(),
      adminService.getOverview(),
      adminService.getEnrollments(),
      adminService.getPayments(),
      adminService.getCoupons(),
      adminService.getSettings(),
      adminService.getUsers().catch(() => ({ data: [] })),
    ])
    courses.value = courseResult.data
    overview.value = overviewResult.data
    enrollments.value = enrollmentResult.data
    payments.value = paymentResult.data
    coupons.value = couponResult.data
    users.value = Array.isArray(usersResult?.data) ? usersResult.data : []
    Object.assign(settingsForm, emptySettings(), settingsResult.data)
  } catch (error) {
    errorMessage.value = errorDetail(error, t('Unable to load admin data.'))
    if (error.response?.status === 401) authenticated.value = false
  } finally {
    loadingCourses.value = false
  }
}

async function checkSession() {
  try {
    await adminService.getSession()
    authenticated.value = true
    await loadAdminData()
  } catch (error) {
    if (error.response?.status === 401) {
      await router.replace('/account?mode=signin')
      return
    }
    errorMessage.value = errorDetail(error, t('Unable to verify admin session.'))
  }
}

async function signOut() {
  busy.value = true
  errorMessage.value = ''
  authenticated.value = false
  courses.value = []
  editingId.value = ''
  setCourseForm()
  let logoutFailed = false

  try {
    await adminService.logout()
  } catch (error) {
    logoutFailed = true
    console.error('Admin logout request failed:', error)
  } finally {
    busy.value = false
    await router.replace({
      path: '/account',
      query: {
        mode: 'signin',
        ...(logoutFailed ? { adminLogout: 'failed' } : {}),
      },
    })
  }
}

function startNewCourse() {
  editingId.value = ''
  formError.value = ''
  setCourseForm()
}

function editCourse(course) {
  editingId.value = course.id
  formError.value = ''
  successMessage.value = ''
  setCourseForm(course)
}

function addModule() {
  const nextNumber = Math.max(
    0,
    ...courseForm.modules.map((module) => Number.parseInt(module.module_number, 10) || 0),
  ) + 1
  courseForm.modules.push({
    module_number: String(nextNumber),
    title: '',
    title_kh: '',
    description: '',
    description_kh: '',
    icon_type: 'Core PCB',
    image_url: '',
  })
}

function addHardwareSpec() {
  courseForm.hardware_specs.push({ title: '', title_kh: '', items: [], items_kh: [] })
}

function addBatchSchedule() {
  courseForm.batch_schedules.push({
    day_type: 'Weekday (Mon-Fri)',
    time_slot: 'Morning',
    start_time: '8:00 AM',
    end_time: '1:00 PM',
    max_seats: 20,
    active: true,
  })
}

function updateSpecItems(index, text) {
  courseForm.hardware_specs[index].items = text.split(/\r?\n/).map((item) => item.trim()).filter(Boolean)
}

function updateSpecKhItems(index, text) {
  if (!courseForm.hardware_specs[index].items_kh) {
    courseForm.hardware_specs[index].items_kh = []
  }
  courseForm.hardware_specs[index].items_kh = text.split(/\r?\n/).map((item) => item.trim()).filter(Boolean)
}

function validateImageFile(file) {
  if (!file) return false
  if (!['image/png', 'image/jpeg'].includes(file.type)) {
    formError.value = t('Choose a PNG or JPG image.')
    return false
  }
  if (file.size > 5 * 1024 * 1024) {
    formError.value = t('Image must be 5 MB or smaller.')
    return false
  }
  return true
}

async function uploadCourseImage(file) {
  formError.value = ''
  if (!validateImageFile(file)) return
  imageUploading.value = true
  try {
    const { data } = await adminService.uploadImage(file)
    courseForm.image_url = data.image_url
    successMessage.value = t('Image uploaded! Click "Publish changes" below to save the course.')
  } catch (error) {
    formError.value = errorDetail(error, t('Unable to upload course image.'))
  } finally {
    imageUploading.value = false
    if (imageInput.value) imageInput.value.value = ''
  }
}

function setModuleImageInput(element, index) {
  if (element) {
    moduleImageInputs.value[index] = element
  }
}

const cropperOpen = ref(false)
const cropperImageSrc = ref('')
const cropperTitle = ref('')
const cropperDefaultRatio = ref(16 / 9)
const cropperOriginalFile = ref(null)
let cropperTargetType = 'course'
let cropperTargetModule = null

function promptCropCourseImage(file) {
  if (!validateImageFile(file)) return
  cropperTargetType = 'course'
  cropperTargetModule = null
  cropperTitle.value = t('Crop Course Cover Image')
  cropperDefaultRatio.value = 16 / 9
  cropperOriginalFile.value = file
  cropperImageSrc.value = URL.createObjectURL(file)
  cropperOpen.value = true
}

function promptCropModuleImage(file, module) {
  if (!validateImageFile(file)) return
  cropperTargetType = 'module'
  cropperTargetModule = module
  cropperTitle.value = t('Crop Module Photo')
  cropperDefaultRatio.value = 4 / 3
  cropperOriginalFile.value = file
  cropperImageSrc.value = URL.createObjectURL(file)
  cropperOpen.value = true
}

function openCoverCropForExisting() {
  if (!courseForm.image_url) return
  cropperTargetType = 'course'
  cropperTargetModule = null
  cropperTitle.value = t('Crop Course Cover Image')
  cropperDefaultRatio.value = 16 / 9
  cropperOriginalFile.value = null
  cropperImageSrc.value = resolveImageUrl(courseForm.image_url)
  cropperOpen.value = true
}

function openModuleCropForExisting(module) {
  if (!module.image_url) return
  cropperTargetType = 'module'
  cropperTargetModule = module
  cropperTitle.value = t('Crop Module Photo')
  cropperDefaultRatio.value = 4 / 3
  cropperOriginalFile.value = null
  cropperImageSrc.value = resolveImageUrl(module.image_url)
  cropperOpen.value = true
}

async function onCropperApply(file) {
  if (cropperTargetType === 'course') {
    await uploadCourseImage(file)
  } else if (cropperTargetType === 'module' && cropperTargetModule) {
    await uploadModuleImageFile(file, cropperTargetModule)
  }
}

async function onCropperUseOriginal(file) {
  if (cropperTargetType === 'course') {
    await uploadCourseImage(file)
  } else if (cropperTargetType === 'module' && cropperTargetModule) {
    await uploadModuleImageFile(file, cropperTargetModule)
  }
}

async function uploadModuleImageFile(file, targetModule) {
  formError.value = ''
  moduleImageUploading.value = true
  try {
    const { data } = await adminService.uploadImage(file)
    targetModule.image_url = data.image_url
  } catch (error) {
    formError.value = errorDetail(error, t('Unable to upload course image.'))
  } finally {
    moduleImageUploading.value = false
  }
}

function handleModuleImageSelection(event, module) {
  const file = event.target.files?.[0]
  if (file) {
    promptCropModuleImage(file, module)
  }
  event.target.value = ''
}

function handleImageSelection(event) {
  const file = event.target.files?.[0]
  if (file) {
    promptCropCourseImage(file)
  }
  event.target.value = ''
}

function handleImageDrop(event) {
  draggingImage.value = false
  const file = event.dataTransfer?.files?.[0]
  if (file) {
    promptCropCourseImage(file)
  }
}

async function saveCourse() {
  busy.value = true
  formError.value = ''
  errorMessage.value = ''
  successMessage.value = ''

  if (isLocalFilePath(courseForm.image_url)) {
    formError.value = t('Local file paths (e.g. C:\\...) cannot be viewed on web browsers. Please click "Choose image" to upload the image file to the server.')
    busy.value = false
    return
  }

  const payload = {
    ...courseForm,
    title_kh: courseForm.title_kh ? courseForm.title_kh.trim() : null,
    short_description_kh: courseForm.short_description_kh ? courseForm.short_description_kh.trim() : null,
    category_kh: courseForm.category_kh ? courseForm.category_kh.trim() : null,
    level_kh: courseForm.level_kh ? courseForm.level_kh.trim() : null,
    duration_kh: courseForm.duration_kh ? courseForm.duration_kh.trim() : null,
    badges_kh: courseForm.badges_kh || [],
    original_price: courseForm.original_price || null,
    level: courseForm.level || null,
    duration: courseForm.duration || null,
  }
  try {
    let publishedMessage
    if (editingId.value) {
      await adminService.updateCourse(editingId.value, payload)
      publishedMessage = payload.status === 'published' ? t('Course changes published.') : t('Course saved.')
    } else {
      await adminService.createCourse(payload)
      publishedMessage = payload.status === 'published' ? t('Course added and published.') : t('Course saved.')
    }
    await loadAdminData()
    startNewCourse()
    successMessage.value = publishedMessage
  } catch (error) {
    formError.value = errorDetail(error, t('Unable to save course.'))
  } finally {
    busy.value = false
  }
}

async function removeCourse(course) {
  if (!window.confirm(`${t('Delete')} "${course.title}"?`)) return
  errorMessage.value = ''
  successMessage.value = ''
  try {
    await adminService.deleteCourse(course.id)
    if (editingId.value === course.id) startNewCourse()
    await loadAdminData()
    successMessage.value = t('Course deleted.')
  } catch (error) {
    errorMessage.value = errorDetail(error, t('Unable to delete course.'))
  }
}

async function changeEnrollmentStatus(record, status) {
  try {
    const { data } = await adminService.updateEnrollmentStatus(record.enrollment_id, status)
    const index = enrollments.value.findIndex((item) => item.enrollment_id === data.enrollment_id)
    if (index >= 0) enrollments.value[index] = data
    const paymentIndex = payments.value.findIndex((item) => item.enrollment_id === data.enrollment_id)
    if (paymentIndex >= 0) payments.value[paymentIndex] = data
    if (selectedStudent.value && selectedStudent.value.enrollment_id === data.enrollment_id) {
      selectedStudent.value = data
    }
    await refreshOverview()
    if (status === 'confirmed') {
      successMessage.value = t('Enrollment confirmed and payment verified successfully!')
    } else {
      successMessage.value = t('Enrollment status updated.')
    }
    setTimeout(() => { successMessage.value = '' }, 4000)
  } catch (error) {
    errorMessage.value = errorDetail(error, t('Unable to update enrollment status.'))
  }
}

async function changePaymentStatus(record, status) {
  try {
    const { data } = await adminService.updatePaymentStatus(record.enrollment_id, status)
    const index = payments.value.findIndex((item) => item.enrollment_id === data.enrollment_id)
    if (index >= 0) payments.value[index] = data
    const studentIndex = enrollments.value.findIndex((item) => item.enrollment_id === data.enrollment_id)
    if (studentIndex >= 0) enrollments.value[studentIndex] = data
    if (selectedStudent.value && selectedStudent.value.enrollment_id === data.enrollment_id) {
      selectedStudent.value = data
    }
    await refreshOverview()
    if (status === 'paid') {
      successMessage.value = t('Payment verified and student enrollment confirmed!')
    } else {
      successMessage.value = t('Payment status updated.')
    }
    setTimeout(() => { successMessage.value = '' }, 4000)
  } catch (error) {
    errorMessage.value = errorDetail(error, t('Unable to update payment status.'))
  }
}

async function refreshOverview() {
  try {
    const { data } = await adminService.getOverview()
    overview.value = data
  } catch (error) {
    errorMessage.value = errorDetail(error, t('Unable to refresh dashboard data.'))
  }
}

const copiedStudentInfo = ref(false)

function showStudentDetails(record) {
  selectedStudent.value = record
}

async function copyStudentContact(student) {
  if (!student) return
  const lines = [
    `Student: ${student.student_name}`,
    `Email: ${student.email || '—'}`,
    `Phone: ${student.phone_number || student.phone_telegram || '—'}`,
    `Address: ${student.address || '—'}`,
    `Course: ${student.course_title || '—'}`,
    `Schedule: ${student.preferred_schedule || '—'}`,
    `Status: ${student.enrollment_status || '—'}`
  ]
  try {
    await navigator.clipboard.writeText(lines.join('\n'))
    copiedStudentInfo.value = true
    setTimeout(() => {
      copiedStudentInfo.value = false
    }, 2000)
  } catch (err) {
    console.warn('Could not copy student contact info:', err)
  }
}

function handleEscapeKey(e) {
  if (e.key === 'Escape' && selectedStudent.value) {
    selectedStudent.value = null
  }
}

function studentDetails(record) {
  return {
    'Date of birth': record.date_of_birth,
    'Gender': record.gender,
    'Email': record.email,
    'Phone Number': record.phone_number,
    'Telegram username': record.phone_telegram,
    'Address': record.address,
    'Age Range': record.age_range,
    'Highest Qualification': record.highest_qualification,
    'Current Occupation / School': record.current_occupation,
    'Previous Robotics / Coding Experience': record.coding_experience,
    'Special Requirements or Notes': record.special_requirements,
  }
}

async function exportRoster() {
  try {
    const { data } = await adminService.exportEnrollments()
    const url = URL.createObjectURL(data)
    const link = document.createElement('a')
    link.href = url
    link.download = 'aerobyte-enrollments.xlsx'
    link.click()
    URL.revokeObjectURL(url)
  } catch (error) {
    errorMessage.value = errorDetail(error, t('Unable to export enrollment roster.'))
  }
}

function editCoupon(coupon) {
  editingCoupon.value = coupon.code
  couponError.value = ''
  Object.assign(couponForm, emptyCoupon(), coupon)
}

function resetCoupon() {
  editingCoupon.value = ''
  couponError.value = ''
  Object.assign(couponForm, emptyCoupon())
}

async function saveCoupon() {
  busy.value = true
  couponError.value = ''
  const payload = {
    ...couponForm,
    code: couponForm.code.trim().toUpperCase(),
    max_usage: couponForm.max_usage || null,
    expires_at: couponForm.expires_at || null,
  }
  try {
    if (editingCoupon.value) await adminService.updateCoupon(editingCoupon.value, payload)
    else await adminService.createCoupon(payload)
    const { data } = await adminService.getCoupons()
    coupons.value = data
    resetCoupon()
  } catch (error) {
    couponError.value = errorDetail(error, t('Unable to save coupon.'))
  } finally {
    busy.value = false
  }
}

async function toggleCoupon(coupon) {
  try {
    await adminService.updateCoupon(coupon.code, { ...coupon, active: !coupon.active })
    coupon.active = !coupon.active
  } catch (error) {
    errorMessage.value = errorDetail(error, t('Unable to update coupon.'))
  }
}

async function removeCoupon(coupon) {
  if (!window.confirm(`${t('Delete')} "${coupon.code}"?`)) return
  try {
    await adminService.deleteCoupon(coupon.code)
    coupons.value = coupons.value.filter((item) => item.code !== coupon.code)
    if (editingCoupon.value === coupon.code) resetCoupon()
  } catch (error) {
    errorMessage.value = errorDetail(error, t('Unable to delete coupon.'))
  }
}

async function saveSettings() {
  busy.value = true
  settingsError.value = ''
  settingsSaved.value = false
  try {
    const { data } = await adminService.updateSettings(settingsForm)
    Object.assign(settingsForm, data)
    settingsSaved.value = true
  } catch (error) {
    settingsError.value = errorDetail(error, t('Unable to save site settings.'))
  } finally {
    busy.value = false
  }
}

// --- Traffic & Login Logs State & Logic ---
const logsAnalytics = ref({
  total_visits: 0,
  unique_visitors: 0,
  total_logins: 0,
  today_visits: 0,
  today_logins: 0,
  top_pages: [],
})
const logsActiveTab = ref('logins')
const logsLoading = ref(false)
const loginLogs = ref([])
const visitLogs = ref([])

const loginSearch = ref('')
const loginRoleFilter = ref('all')
const loginPage = ref(1)
const loginLimit = 15

const visitSearch = ref('')
const visitPage = ref(1)
const visitLimit = 15

function parseDevice(ua) {
  if (!ua) return { type: 'Desktop', browser: 'Unknown' }
  const lower = ua.toLowerCase()
  let type = 'Desktop'
  if (/mobile|iphone|ipod|android.*mobile/.test(lower)) {
    type = 'Mobile'
  } else if (/ipad|tablet|android/.test(lower)) {
    type = 'Tablet'
  }

  let browser = 'Browser'
  if (lower.includes('chrome') && !lower.includes('edg') && !lower.includes('opr')) {
    browser = 'Chrome'
  } else if (lower.includes('safari') && !lower.includes('chrome')) {
    browser = 'Safari'
  } else if (lower.includes('firefox')) {
    browser = 'Firefox'
  } else if (lower.includes('edg')) {
    browser = 'Edge'
  } else if (lower.includes('opera') || lower.includes('opr')) {
    browser = 'Opera'
  }

  return { type, browser }
}

async function loadLogsData() {
  logsLoading.value = true
  try {
    const [analyticsRes, loginsRes, visitsRes] = await Promise.all([
      adminService.getLogsAnalytics().catch(() => ({ data: { total_visits: 0, unique_visitors: 0, total_logins: 0, today_visits: 0, today_logins: 0, top_pages: [] } })),
      adminService.getLoginLogs({ limit: 200 }).catch(() => ({ data: [] })),
      adminService.getVisitLogs({ limit: 200 }).catch(() => ({ data: [] })),
    ])

    if (analyticsRes && analyticsRes.data) {
      logsAnalytics.value = {
        total_visits: analyticsRes.data.total_visits || 0,
        unique_visitors: analyticsRes.data.unique_visitors || 0,
        total_logins: analyticsRes.data.total_logins || 0,
        today_visits: analyticsRes.data.today_visits || 0,
        today_logins: analyticsRes.data.today_logins || 0,
        top_pages: analyticsRes.data.top_pages || [],
      }
    }

    loginLogs.value = Array.isArray(loginsRes?.data) ? loginsRes.data : []
    visitLogs.value = Array.isArray(visitsRes?.data) ? visitsRes.data : []
  } catch (err) {
    console.error('Failed to load logs:', err)
  } finally {
    logsLoading.value = false
  }
}

const filteredLoginLogs = computed(() => {
  let list = loginLogs.value || []
  if (loginRoleFilter.value === 'admin') {
    list = list.filter((l) => (l.role || '').toLowerCase() === 'admin')
  } else if (loginRoleFilter.value === 'user') {
    list = list.filter((l) => (l.role || '').toLowerCase() !== 'admin')
  }
  const q = (loginSearch.value || '').trim().toLowerCase()
  if (q) {
    list = list.filter(
      (l) =>
        (l.user_email || '').toLowerCase().includes(q) ||
        (l.user_name || '').toLowerCase().includes(q) ||
        (l.ip_address || '').toLowerCase().includes(q)
    )
  }
  return list
})

const totalLoginPages = computed(() => Math.max(1, Math.ceil(filteredLoginLogs.value.length / loginLimit)))

const paginatedLoginLogs = computed(() => {
  const start = (loginPage.value - 1) * loginLimit
  return filteredLoginLogs.value.slice(start, start + loginLimit)
})

watch([loginSearch, loginRoleFilter], () => {
  loginPage.value = 1
})

const filteredVisitLogs = computed(() => {
  let list = visitLogs.value || []
  const q = (visitSearch.value || '').trim().toLowerCase()
  if (q) {
    list = list.filter(
      (v) =>
        (v.path || '').toLowerCase().includes(q) ||
        (v.visitor_id || '').toLowerCase().includes(q) ||
        (v.user_email || '').toLowerCase().includes(q) ||
        (v.user_name || '').toLowerCase().includes(q) ||
        (v.ip_address || '').toLowerCase().includes(q) ||
        (v.referrer || '').toLowerCase().includes(q)
    )
  }
  return list
})

const totalVisitPages = computed(() => Math.max(1, Math.ceil(filteredVisitLogs.value.length / visitLimit)))

const paginatedVisitLogs = computed(() => {
  const start = (visitPage.value - 1) * visitLimit
  return filteredVisitLogs.value.slice(start, start + visitLimit)
})

watch(visitSearch, () => {
  visitPage.value = 1
})

async function loadUsersData() {
  usersLoading.value = true
  try {
    const res = await adminService.getUsers()
    users.value = Array.isArray(res?.data) ? res.data : []
  } catch (err) {
    console.error('Failed to load users:', err)
  } finally {
    usersLoading.value = false
  }
}

function openEditUserModal(user) {
  editingUser.value = user
  userEditError.value = ''
  Object.assign(userEditForm, {
    id: user.id,
    full_name: user.full_name || '',
    email: user.email || '',
    phone: user.phone || '',
    telegram: user.telegram || '',
    date_of_birth: user.date_of_birth || '',
    location: user.location || '',
    qualification: user.qualification || '',
    qualification_other: user.qualification_other || '',
    occupation: user.occupation || '',
    experience: user.experience || '',
    is_verified: user.is_verified === 1,
  })
}

async function saveUserEdit() {
  if (!userEditForm.full_name.trim() || !userEditForm.email.trim()) {
    userEditError.value = t('Please enter both name and email.')
    return
  }
  userEditBusy.value = true
  userEditError.value = ''
  try {
    const res = await adminService.updateUser(userEditForm.id, userEditForm)
    const updated = res.data
    const index = users.value.findIndex((u) => u.id === userEditForm.id)
    if (index !== -1) {
      users.value[index] = { ...users.value[index], ...updated }
    }
    editingUser.value = null
    successMessage.value = t('User profile updated successfully.')
  } catch (err) {
    userEditError.value = errorDetail(err, t('Unable to update user profile.'))
  } finally {
    userEditBusy.value = false
  }
}

function openChangePasswordModal(user) {
  passwordTargetUser.value = user
  passwordError.value = ''
  passwordForm.newPassword = ''
  passwordForm.confirmPassword = ''
  showNewPassword.value = false
}

async function saveUserPassword() {
  if (passwordForm.newPassword.length < 8) {
    passwordError.value = t('Password must be at least 8 characters.')
    return
  }
  if (passwordForm.newPassword !== passwordForm.confirmPassword) {
    passwordError.value = t('Passwords do not match.')
    return
  }
  passwordBusy.value = true
  passwordError.value = ''
  try {
    await adminService.setUserPassword(passwordTargetUser.value.id, passwordForm.newPassword)
    passwordTargetUser.value = null
    successMessage.value = t('User password updated successfully.')
  } catch (err) {
    passwordError.value = errorDetail(err, t('Unable to update user password.'))
  } finally {
    passwordBusy.value = false
  }
}

function openDeleteUserModal(user) {
  deleteTargetUser.value = user
  deleteError.value = ''
}

async function confirmDeleteUser() {
  if (!deleteTargetUser.value) return
  deleteBusy.value = true
  deleteError.value = ''
  try {
    await adminService.deleteUser(deleteTargetUser.value.id)
    users.value = users.value.filter((u) => u.id !== deleteTargetUser.value.id)
    deleteTargetUser.value = null
    successMessage.value = t('User account deleted successfully.')
  } catch (err) {
    deleteError.value = errorDetail(err, t('Unable to delete user.'))
  } finally {
    deleteBusy.value = false
  }
}

watch(activeSection, (sec) => {
  if (sec === 'logs') {
    loadLogsData()
  } else if (sec === 'users') {
    loadUsersData()
  }
})

onMounted(() => {
  document.documentElement.classList.add('admin-locked-viewport')
  document.body.classList.add('admin-locked-viewport')
  window.addEventListener('keydown', handleEscapeKey)
  checkSession()
  if (activeSection.value === 'logs') {
    loadLogsData()
  } else if (activeSection.value === 'users') {
    loadUsersData()
  }
})

onUnmounted(() => {
  document.documentElement.classList.remove('admin-locked-viewport')
  document.body.classList.remove('admin-locked-viewport')
  window.removeEventListener('keydown', handleEscapeKey)
})
</script>

<style>
.admin-input {
  display: block;
  width: 100%;
  min-height: 42px;
  border: 1px solid rgb(148 163 184 / 0.7);
  border-radius: 0.625rem;
  background: white;
  padding: 0.55rem 0.75rem;
  color: #1e293b;
  font-size: 0.875rem;
  outline: none;
  transition: background-color 150ms ease, border-color 150ms ease, color 150ms ease;
}

.admin-input:focus {
  border-color: #27466d;
  box-shadow: 0 0 0 3px rgb(39 70 109 / 0.12);
}

html.dark .admin-input {
  border-color: #334155 !important;
  background-color: #1e293b !important;
  color: #f8fafc !important;
}

html.dark .admin-input::placeholder {
  color: #94a3b8 !important;
}

html.dark .admin-input:focus {
  border-color: #6366f1 !important;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.25) !important;
}

html.dark .admin-input option {
  background-color: #1e293b !important;
  color: #f8fafc !important;
}

.admin-label {
  display: block;
  margin-bottom: 0.375rem;
  color: #334155;
  font-size: 0.875rem;
  font-weight: 600;
  transition: color 150ms ease;
}

html.dark .admin-label {
  color: #f1f5f9 !important;
}

.admin-primary-button {
  display: inline-flex;
  min-height: 42px;
  flex: 1;
  align-items: center;
  justify-content: center;
  border-radius: 0.625rem;
  background: #17313d;
  padding: 0.625rem 1rem;
  color: white;
  font-size: 0.875rem;
  font-weight: 700;
  transition: background-color 150ms ease;
}

.admin-primary-button:hover {
  background: #27466d;
}

html.dark .admin-primary-button {
  background: #4f46e5;
}

html.dark .admin-primary-button:hover {
  background: #4338ca;
}

.admin-primary-button:disabled {
  cursor: wait;
  opacity: 0.65;
}

html.dark .courses-hero header h1,
html.dark .courses-hero h1,
html.dark .courses-hero h2,
html.dark .courses-hero h3 {
  color: #f8fafc !important;
}

html.dark .courses-hero article,
html.dark .courses-hero section.rounded-2xl,
html.dark .courses-hero section.rounded-xl,
html.dark .courses-hero nav.rounded-xl,
html.dark .courses-hero div.rounded-2xl.border,
html.dark .courses-hero div.rounded-xl.border,
html.dark .courses-hero form.rounded-2xl {
  background-color: #0f172a !important;
  border-color: #1e293b !important;
}

html.dark .courses-hero table thead {
  background-color: #1e293b !important;
  color: #94a3b8 !important;
}

html.dark .courses-hero table tbody tr:hover {
  background-color: rgba(30, 41, 59, 0.4) !important;
}

html.dark .courses-hero table td,
html.dark .courses-hero table th {
  border-color: #1e293b !important;
}

html.dark .courses-hero td p.font-bold,
html.dark .courses-hero .font-extrabold {
  color: #f8fafc !important;
}

html.dark .courses-hero .bg-slate-50 {
  background-color: #1e293b !important;
  color: #cbd5e1 !important;
}

html.dark .courses-hero .border-slate-200,
html.dark .courses-hero .border-slate-100 {
  border-color: #334155 !important;
}

html.dark .courses-hero .text-slate-800,
html.dark .courses-hero .text-slate-700,
html.dark .courses-hero .text-slate-900,
html.dark .courses-hero .text-navy-900 {
  color: #f1f5f9 !important;
}

html.dark .courses-hero .text-slate-600,
html.dark .courses-hero .text-slate-500 {
  color: #94a3b8 !important;
}

/* Custom scrollbar for admin dashboard columns */
.admin-scroll-box {
  scrollbar-width: thin;
  scrollbar-color: #cbd5e1 transparent;
}

html.dark .admin-scroll-box {
  scrollbar-color: #334155 transparent;
}

.admin-scroll-box::-webkit-scrollbar {
  width: 5px;
}

.admin-scroll-box::-webkit-scrollbar-track {
  background: transparent;
}

.admin-scroll-box::-webkit-scrollbar-thumb {
  background-color: #cbd5e1;
  border-radius: 9999px;
}

html.dark .admin-scroll-box::-webkit-scrollbar-thumb {
  background-color: #334155;
}

.admin-scroll-box::-webkit-scrollbar-thumb:hover {
  background-color: #94a3b8;
}

html.dark .admin-scroll-box::-webkit-scrollbar-thumb:hover {
  background-color: #475569;
}

/* Lucian UX/UI Prompt #040 Title Swap Motion */
.u040-main-title {
  white-space: nowrap;
  transition: opacity 0.2s, transform 0.4s cubic-bezier(0.34, 1.45, 0.64, 1);
}
.u040-main-title.swap {
  opacity: 0;
  transform: translateY(8px);
}
@media (prefers-reduced-motion: reduce) {
  .u040-main-title {
    animation-duration: 0.001ms !important;
    transition-duration: 0.001ms !important;
  }
}
</style>
