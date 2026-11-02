<template>
  <header
    class="sticky top-0 z-50 w-full border-b border-slate-200 dark:border-slate-800 bg-white/95 dark:bg-slate-900/95 backdrop-blur transition-all duration-200"
    :class="isScrolled ? 'shadow-xs shadow-slate-900/5 dark:shadow-slate-950/40 bg-white/98 dark:bg-slate-900/98' : ''"
  >
    <nav
      class="mx-auto flex max-w-7xl items-center justify-between gap-2 px-3 py-2.5 sm:px-6 sm:py-3 lg:flex lg:gap-4 xl:gap-8 lg:px-8"
      :aria-label="t('Main navigation')"
    >
      <!-- Left side: Mobile Menu Hamburger Button & Brand Logo -->
      <div class="flex items-center gap-1.5 sm:gap-2.5 shrink-0">
        <!-- Mobile Left Sidebar Hamburger Button -->
        <button
          type="button"
          @click="mobileDrawerOpen = true"
          class="lg:hidden flex h-9 w-9 items-center justify-center -ml-1 text-slate-700 dark:text-slate-200 hover:text-navy-900 dark:hover:text-white rounded-lg hover:bg-slate-100 dark:hover:bg-slate-800 active:scale-95 transition cursor-pointer select-none"
          :aria-label="t('Open navigation menu')"
          :aria-expanded="mobileDrawerOpen"
        >
          <Menu class="w-5 h-5" />
        </button>

        <RouterLink
          to="/courses"
          class="flex w-fit items-center gap-2 text-sm sm:text-base font-extrabold tracking-tight text-navy-900 dark:text-white shrink-0"
          :aria-label="'AeroByte Academy'"
        >
          <img src="/aerobyte-logo.png" alt="" width="48" height="40" class="h-8 w-10 sm:h-10 sm:w-12 object-contain transition duration-200 dark:brightness-0 dark:invert" />
          <span><span class="inline sm:hidden">AeroByte</span><span class="hidden sm:inline">AeroByte Academy</span></span>
        </RouterLink>
      </div>

      <!-- Desktop Center Navigation Links (Courses, Print, Fly, Store, Question, About) -->
      <div class="hidden items-center justify-center gap-1 xl:gap-2.5 lg:flex">
        <RouterLink
          to="/courses"
          class="text-xs xl:text-[13px] font-bold tracking-tight transition-all duration-150 py-1.5 px-2.5 xl:px-3 rounded-lg"
          :class="route.path.startsWith('/courses') || route.path.startsWith('/course')
            ? 'text-navy-900 dark:text-white font-extrabold bg-slate-100 dark:bg-slate-800 shadow-xs'
            : 'text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white hover:bg-slate-100/70 dark:hover:bg-slate-800/60'"
        >
          {{ t('Courses') }}
        </RouterLink>

        <RouterLink
          to="/print"
          class="text-xs xl:text-[13px] font-bold tracking-tight transition-all duration-150 py-1.5 px-2.5 xl:px-3 rounded-lg flex items-center gap-1.5"
          :class="route.path === '/print'
            ? 'text-navy-900 dark:text-white font-extrabold bg-slate-100 dark:bg-slate-800 shadow-xs'
            : 'text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white hover:bg-slate-100/70 dark:hover:bg-slate-800/60'"
        >
          <span>{{ t('Print') }}</span>
        </RouterLink>

        <RouterLink
          to="/fly"
          class="text-xs xl:text-[13px] font-bold tracking-tight transition-all duration-150 py-1.5 px-2.5 xl:px-3 rounded-lg flex items-center gap-1.5"
          :class="route.path === '/fly'
            ? 'text-navy-900 dark:text-white font-extrabold bg-slate-100 dark:bg-slate-800 shadow-xs'
            : 'text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white hover:bg-slate-100/70 dark:hover:bg-slate-800/60'"
        >
          <span>{{ t('Fly') }}</span>
        </RouterLink>

        <RouterLink
          to="/store"
          class="text-xs xl:text-[13px] font-bold tracking-tight transition-all duration-150 py-1.5 px-2.5 xl:px-3 rounded-lg flex items-center gap-1.5"
          :class="route.path === '/store'
            ? 'text-navy-900 dark:text-white font-extrabold bg-slate-100 dark:bg-slate-800 shadow-xs'
            : 'text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white hover:bg-slate-100/70 dark:hover:bg-slate-800/60'"
        >
          <span>{{ t('Store') }}</span>
        </RouterLink>

        <RouterLink
          to="/questions"
          class="text-xs xl:text-[13px] font-bold tracking-tight transition-all duration-150 py-1.5 px-2.5 xl:px-3 rounded-lg"
          :class="route.path === '/questions'
            ? 'text-navy-900 dark:text-white font-extrabold bg-slate-100 dark:bg-slate-800 shadow-xs'
            : 'text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white hover:bg-slate-100/70 dark:hover:bg-slate-800/60'"
        >
          {{ t('Question') }}
        </RouterLink>

        <RouterLink
          to="/about"
          class="text-xs xl:text-[13px] font-bold tracking-tight transition-all duration-150 py-1.5 px-2.5 xl:px-3 rounded-lg"
          :class="route.path === '/about'
            ? 'text-navy-900 dark:text-white font-extrabold bg-slate-100 dark:bg-slate-800 shadow-xs'
            : 'text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white hover:bg-slate-100/70 dark:hover:bg-slate-800/60'"
        >
          {{ t('About') }}
        </RouterLink>
      </div>

      <!-- Right Action Items: Language, Account Profile, Contact Us -->
      <div class="flex items-center justify-self-end gap-1.5 sm:gap-2.5 shrink-0">
        <div ref="languageMenu" class="relative">
          <button
            ref="languageTrigger"
            type="button"
            class="inline-flex h-8 sm:h-9 cursor-pointer items-center gap-1 sm:gap-2 rounded-lg px-2 text-slate-600 dark:text-slate-300 transition hover:bg-slate-50 dark:hover:bg-slate-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-navy-800/30"
            :aria-label="locale === 'kh' ? 'KH - ជ្រើសរើសភាសា' : 'EN - Choose language'"
            aria-haspopup="listbox"
            :aria-expanded="languageMenuOpen"
            @click="toggleLanguageMenu"
            @keydown.down.prevent="openLanguageMenu"
          >
            <Globe2 class="h-4 w-4 sm:h-5 sm:w-5" aria-hidden="true" />
            <span class="text-xs sm:text-sm font-semibold text-navy-900 dark:text-white">{{ locale.toUpperCase() }}</span>
          </button>
          <div
            v-if="languageMenuOpen"
            class="absolute right-0 top-full z-50 mt-2 w-44 max-w-[calc(100vw-24px)] overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-1.5 shadow-xl"
            role="listbox"
            :aria-label="t('Choose language')"
            @keydown.esc.prevent="closeLanguageMenu"
          >
            <button
              v-for="language in languages"
              :key="language.value"
              :ref="language.value === locale ? 'selectedLanguageOption' : undefined"
              type="button"
              role="option"
              :aria-selected="locale === language.value"
              class="flex w-full items-center justify-between rounded-xl px-3 py-2 text-xs font-semibold transition"
              :class="locale === language.value
                ? 'bg-navy-50 dark:bg-slate-700 text-navy-900 dark:text-white font-bold'
                : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/60 hover:text-navy-900 dark:hover:text-white font-medium'"
              @click="selectLanguage(language.value)"
            >
              <div class="flex items-center gap-2">
                <span class="font-bold tracking-wide">{{ language.label }}</span>
                <span class="text-[11px] font-medium" :class="locale === language.value ? 'text-navy-700 dark:text-indigo-400' : 'text-slate-400 dark:text-slate-500'">
                  {{ language.sublabel }}
                </span>
              </div>
              <Check v-if="locale === language.value" class="h-4 w-4 text-navy-900 dark:text-white shrink-0" />
            </button>
          </div>
        </div>

        <!-- Account Profile Dropdown (Clean, User-Only) -->
        <div ref="accountMenu" class="relative">
          <button
            ref="accountTrigger"
            type="button"
            class="inline-flex h-8 sm:h-9 cursor-pointer items-center gap-1.5 sm:gap-2 rounded-lg px-2 text-slate-600 dark:text-slate-300 transition hover:bg-slate-50 dark:hover:bg-slate-800 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-navy-800/30"
            :aria-label="`${profileName || t('Name')} - ${t('Account menu')}`"
            aria-haspopup="menu"
            :aria-expanded="accountMenuOpen"
            @click="accountMenuOpen = !accountMenuOpen"
            @keydown.down.prevent="openAccountMenu"
          >
            <img
              v-if="profileAvatar && !avatarLoadFailed"
              :src="resolveImageUrl(profileAvatar)"
              alt=""
              class="h-5 w-5 sm:h-6 sm:w-6 rounded-full object-cover shrink-0 border border-slate-200 dark:border-slate-700"
              @error="avatarLoadFailed = true"
            />
            <UserRound v-else class="h-4 w-4 sm:h-5 sm:w-5 shrink-0" aria-hidden="true" />
            <span class="max-w-16 sm:max-w-24 truncate text-xs sm:text-sm font-medium text-navy-900 dark:text-white">{{ profileName || t('Name') }}</span>
          </button>
          <div
            v-if="accountMenuOpen"
            class="absolute right-0 top-full z-50 mt-2 w-72 max-w-[calc(100vw-24px)] overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 shadow-xl"
            role="menu"
            :aria-label="t('Account menu')"
            @keydown.esc.prevent="closeAccountMenu"
          >
            <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-700 px-4 sm:px-5 py-3.5 sm:py-4">
              <span class="flex h-10 w-10 sm:h-12 sm:w-12 shrink-0 items-center justify-center rounded-full bg-emerald-100 dark:bg-emerald-900/60 text-sm sm:text-base font-bold text-emerald-700 dark:text-emerald-300 overflow-hidden">
                <img
                  v-if="profileAvatar && !avatarLoadFailed"
                  :src="resolveImageUrl(profileAvatar)"
                  alt=""
                  class="h-full w-full object-cover"
                  @error="avatarLoadFailed = true"
                />
                <span v-else>{{ profileInitials }}</span>
              </span>
              <div class="min-w-0">
                <p class="truncate text-xs sm:text-sm font-bold text-slate-900 dark:text-white">{{ profileName || t('Welcome to AeroByte') }}</p>
                <p class="truncate text-[11px] sm:text-xs text-slate-500 dark:text-slate-400">
                  {{ profileName ? profileEmail || t('Your account') : t('Sign in or create an account') }}
                </p>
              </div>
            </div>
            <div class="space-y-1 p-2">
              <RouterLink
                v-if="profileName"
                to="/profile"
                role="menuitem"
                class="flex items-center gap-3 rounded-xl px-3 py-2.5 sm:py-3 text-xs sm:text-sm font-medium text-slate-700 dark:text-slate-200 transition hover:bg-slate-50 dark:hover:bg-slate-700 hover:text-navy-900 dark:hover:text-white"
                @click="closeAccountMenu"
              >
                <UserRound class="h-4 w-4 sm:h-5 sm:w-5 text-slate-400" aria-hidden="true" />
                <span>{{ t('Profile information') }}</span>
              </RouterLink>

              <!-- Dark / Light Mode Switch inside Account Dropdown -->
              <div class="flex items-center justify-between rounded-xl px-3 py-2 sm:py-2.5 transition hover:bg-slate-50 dark:hover:bg-slate-700/60">
                <div class="flex items-center gap-2.5 sm:gap-3 text-xs sm:text-sm font-medium text-slate-700 dark:text-slate-200">
                  <Sun v-if="!isDark" class="h-4 w-4 sm:h-5 sm:w-5 text-amber-500" />
                  <Moon v-else class="h-4 w-4 sm:h-5 sm:w-5 text-indigo-400" />
                  <span>{{ isDark ? t('Dark mode') : t('Light mode') }}</span>
                </div>
                <button
                  type="button"
                  role="switch"
                  :aria-checked="isDark"
                  :aria-label="isDark ? t('Switch to light mode') : t('Switch to dark mode')"
                  @click="toggleTheme"
                  class="relative inline-flex h-5 w-10 sm:h-6 sm:w-11 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none"
                  :class="isDark ? 'bg-indigo-600' : 'bg-slate-300'"
                >
                  <span
                    aria-hidden="true"
                    class="pointer-events-none inline-block h-4 w-4 sm:h-5 sm:w-5 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"
                    :class="isDark ? 'translate-x-5' : 'translate-x-0'"
                  />
                </button>
              </div>

              <RouterLink
                v-if="!profileName"
                :to="{ path: '/account', query: { mode: 'register' } }"
                role="menuitem"
                class="flex items-center gap-3 rounded-xl px-3 py-2.5 sm:py-3 text-xs sm:text-sm font-semibold text-navy-900 dark:text-white transition hover:bg-navy-50 dark:hover:bg-slate-700"
                @click="closeAccountMenu"
              >
                <UserPlus class="h-4 w-4 sm:h-5 sm:w-5" aria-hidden="true" />
                <span>{{ t('Register') }}</span>
              </RouterLink>
              <RouterLink
                v-if="!profileName"
                :to="{ path: '/account', query: { mode: 'signin' } }"
                role="menuitem"
                class="flex items-center gap-3 rounded-xl px-3 py-2.5 sm:py-3 text-xs sm:text-sm font-semibold text-navy-900 dark:text-white transition hover:bg-navy-50 dark:hover:bg-slate-700"
                @click="closeAccountMenu"
              >
                <LogIn class="h-4 w-4 sm:h-5 sm:w-5" aria-hidden="true" />
                <span>{{ t('Sign in') }}</span>
              </RouterLink>
            </div>
          </div>
        </div>

        <RouterLink
          to="/contact"
          class="inline-flex h-8 sm:h-9 items-center rounded-lg bg-navy-900 dark:bg-indigo-600 px-2.5 sm:px-4 text-[11px] sm:text-xs font-semibold text-white transition hover:bg-navy-800 dark:hover:bg-indigo-700 shrink-0"
        >
          {{ t('Contact Us') }}
        </RouterLink>
      </div>
    </nav>

    <!-- ======================================================== -->
    <!-- MOBILE LEFT-HAND SIDEBAR DRAWER (Courses, Questions, About) -->
    <!-- Teleported to body to avoid backdrop-blur containing block traps -->
    <!-- ======================================================== -->
    <Teleport to="body">
      <!-- Backdrop Overlay -->
      <Transition
        enter-active-class="transition-opacity duration-300 ease-out"
        enter-from-class="opacity-0"
        enter-to-class="opacity-100"
        leave-active-class="transition-opacity duration-200 ease-in"
        leave-from-class="opacity-100"
        leave-to-class="opacity-0"
      >
        <div
          v-if="mobileDrawerOpen"
          class="fixed inset-0 z-[100] bg-slate-950/60 backdrop-blur-xs lg:hidden"
          @click="mobileDrawerOpen = false"
          aria-hidden="true"
        />
      </Transition>

      <!-- Left-Hand Slide-out Sidebar Panel -->
      <Transition
        enter-active-class="transition-transform duration-300 ease-out"
        enter-from-class="-translate-x-full"
        enter-to-class="translate-x-0"
        leave-active-class="transition-transform duration-200 ease-in"
        leave-from-class="translate-x-0"
        leave-to-class="-translate-x-full"
      >
        <aside
          v-if="mobileDrawerOpen"
          class="fixed inset-y-0 left-0 z-[101] w-72 max-w-[85vw] h-full bg-white dark:bg-slate-900 border-r border-slate-200 dark:border-slate-800 shadow-2xl flex flex-col lg:hidden"
          :aria-label="t('Main navigation')"
        >
          <!-- Sidebar Drawer Header -->
          <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 px-4 py-3.5">
            <RouterLink
              to="/courses"
              class="flex items-center gap-2 text-sm font-extrabold tracking-tight text-navy-900 dark:text-white"
              @click="mobileDrawerOpen = false"
            >
              <img src="/aerobyte-logo.png" alt="" class="h-8 w-10 object-contain transition duration-200 dark:brightness-0 dark:invert" />
              <span>AeroByte Academy</span>
            </RouterLink>

            <button
              type="button"
              @click="mobileDrawerOpen = false"
              class="flex h-9 w-9 items-center justify-center rounded-lg text-slate-500 hover:text-navy-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 transition cursor-pointer"
              :aria-label="t('Close navigation menu')"
            >
              <X class="w-5 h-5" />
            </button>
          </div>

          <!-- User Card in Drawer (if signed in) -->
          <div v-if="profileName" class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 px-4 py-3 bg-slate-50/60 dark:bg-slate-800/40">
            <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-full bg-emerald-100 dark:bg-emerald-900/60 text-sm font-bold text-emerald-700 dark:text-emerald-300 overflow-hidden">
              <img
                v-if="profileAvatar && !avatarLoadFailed"
                :src="resolveImageUrl(profileAvatar)"
                alt=""
                class="h-full w-full object-cover"
                @error="avatarLoadFailed = true"
              />
              <span v-else>{{ profileInitials }}</span>
            </span>
            <div class="min-w-0 flex-1">
              <p class="truncate text-xs font-bold text-slate-900 dark:text-white">{{ profileName }}</p>
              <p class="truncate text-[11px] text-slate-500 dark:text-slate-400">{{ profileEmail || t('Your account') }}</p>
            </div>
          </div>

          <!-- Sidebar Navigation Links (Courses, Questions, About, Contact) -->
          <div class="flex-1 overflow-y-auto p-3 space-y-1">
            <p class="px-3 pt-2 pb-1.5 text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
              {{ t('Main navigation') }}
            </p>

            <!-- 1. Courses -->
            <RouterLink
              to="/courses"
              class="flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-bold transition hover:bg-slate-100 dark:hover:bg-slate-800"
              :class="route.path.startsWith('/courses') || route.path.startsWith('/course')
                ? 'bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-indigo-300 font-extrabold'
                : 'text-slate-700 dark:text-slate-200 hover:text-navy-900 dark:hover:text-white'"
              @click="mobileDrawerOpen = false"
            >
              <BookOpen class="h-5 w-5 text-navy-700 dark:text-indigo-400 shrink-0" />
              <span>{{ t('Courses') }}</span>
            </RouterLink>

            <!-- 2. Print -->
            <RouterLink
              to="/print"
              class="flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-bold transition hover:bg-slate-100 dark:hover:bg-slate-800"
              :class="route.path === '/print'
                ? 'bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-indigo-300 font-extrabold'
                : 'text-slate-700 dark:text-slate-200 hover:text-navy-900 dark:hover:text-white'"
              @click="mobileDrawerOpen = false"
            >
              <Printer class="h-5 w-5 text-slate-500 dark:text-slate-400 shrink-0" />
              <span>{{ t('Print') }}</span>
            </RouterLink>

            <!-- 3. Fly -->
            <RouterLink
              to="/fly"
              class="flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-bold transition hover:bg-slate-100 dark:hover:bg-slate-800"
              :class="route.path === '/fly'
                ? 'bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-indigo-300 font-extrabold'
                : 'text-slate-700 dark:text-slate-200 hover:text-navy-900 dark:hover:text-white'"
              @click="mobileDrawerOpen = false"
            >
              <Plane class="h-5 w-5 text-slate-500 dark:text-slate-400 shrink-0" />
              <span>{{ t('Fly') }}</span>
            </RouterLink>

            <!-- 4. Store -->
            <RouterLink
              to="/store"
              class="flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-bold transition hover:bg-slate-100 dark:hover:bg-slate-800"
              :class="route.path === '/store'
                ? 'bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-indigo-300 font-extrabold'
                : 'text-slate-700 dark:text-slate-200 hover:text-navy-900 dark:hover:text-white'"
              @click="mobileDrawerOpen = false"
            >
              <ShoppingBag class="h-5 w-5 text-slate-500 dark:text-slate-400 shrink-0" />
              <span>{{ t('Store') }}</span>
            </RouterLink>

            <!-- 5. Question -->
            <RouterLink
              to="/questions"
              class="flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-semibold transition hover:bg-slate-100 dark:hover:bg-slate-800"
              :class="route.path === '/questions'
                ? 'bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-indigo-300 font-extrabold'
                : 'text-slate-700 dark:text-slate-200 hover:text-navy-900 dark:hover:text-white'"
              @click="mobileDrawerOpen = false"
            >
              <HelpCircle class="h-5 w-5 text-slate-500 dark:text-slate-400 shrink-0" />
              <span>{{ t('Question') }}</span>
            </RouterLink>

            <!-- 6. About -->
            <RouterLink
              to="/about"
              class="flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-semibold transition hover:bg-slate-100 dark:hover:bg-slate-800"
              :class="route.path === '/about'
                ? 'bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-indigo-300 font-extrabold'
                : 'text-slate-700 dark:text-slate-200 hover:text-navy-900 dark:hover:text-white'"
              @click="mobileDrawerOpen = false"
            >
              <Info class="h-5 w-5 text-slate-500 dark:text-slate-400 shrink-0" />
              <span>{{ t('About') }}</span>
            </RouterLink>

            <!-- 7. Contact Us -->
            <RouterLink
              to="/contact"
              class="flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-semibold transition hover:bg-slate-100 dark:hover:bg-slate-800"
              :class="route.path === '/contact'
                ? 'bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-indigo-300 font-extrabold'
                : 'text-slate-700 dark:text-slate-200 hover:text-navy-900 dark:hover:text-white'"
              @click="mobileDrawerOpen = false"
            >
              <PhoneCall class="h-5 w-5 text-slate-500 dark:text-slate-400 shrink-0" />
              <span>{{ t('Contact Us') }}</span>
            </RouterLink>

            <!-- Account Section in Drawer -->
            <template v-if="profileName">
              <div class="my-2 border-t border-slate-100 dark:border-slate-800" />
              <p class="px-3 pt-1 pb-1.5 text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                {{ t('Account') }}
              </p>
              <RouterLink
                to="/profile"
                class="flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-slate-700 dark:text-slate-200 transition hover:bg-slate-100 dark:hover:bg-slate-800 hover:text-navy-900 dark:hover:text-white"
                @click="mobileDrawerOpen = false"
              >
                <UserRound class="h-5 w-5 text-slate-500 dark:text-slate-400 shrink-0" />
                <span>{{ t('Profile information') }}</span>
              </RouterLink>
            </template>
            <template v-else>
              <div class="my-2 border-t border-slate-100 dark:border-slate-800" />
              <p class="px-3 pt-1 pb-1.5 text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                {{ t('Account') }}
              </p>
              <RouterLink
                :to="{ path: '/account', query: { mode: 'signin' } }"
                class="flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-navy-900 dark:text-white transition hover:bg-navy-50 dark:hover:bg-slate-800"
                @click="mobileDrawerOpen = false"
              >
                <LogIn class="h-5 w-5 text-slate-500 dark:text-slate-400 shrink-0" />
                <span>{{ t('Sign in') }}</span>
              </RouterLink>
              <RouterLink
                :to="{ path: '/account', query: { mode: 'register' } }"
                class="flex items-center gap-3 rounded-xl px-3.5 py-2.5 text-sm font-semibold text-navy-900 dark:text-white transition hover:bg-navy-50 dark:hover:bg-slate-800"
                @click="mobileDrawerOpen = false"
              >
                <UserPlus class="h-5 w-5 text-slate-500 dark:text-slate-400 shrink-0" />
                <span>{{ t('Register') }}</span>
              </RouterLink>
            </template>
          </div>

          <!-- Sidebar Drawer Footer -->
          <div class="border-t border-slate-100 dark:border-slate-800 p-3 space-y-2 bg-slate-50/60 dark:bg-slate-900/60">
            <!-- Language Selector inside Drawer -->
            <div class="flex items-center justify-between rounded-xl px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700">
              <div class="flex items-center gap-2 text-xs font-semibold text-slate-700 dark:text-slate-200">
                <Globe2 class="h-4 w-4 text-slate-500 dark:text-slate-400" />
                <span>{{ t('Choose language') }}</span>
              </div>
              <div class="flex items-center gap-1">
                <button
                  v-for="lang in languages"
                  :key="lang.value"
                  type="button"
                  @click="selectLanguage(lang.value)"
                  class="px-2 py-1 text-xs font-bold rounded-md transition cursor-pointer"
                  :class="locale === lang.value
                    ? 'bg-navy-900 text-white dark:bg-indigo-600'
                    : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700'"
                >
                  {{ lang.label }}
                </button>
              </div>
            </div>

            <!-- Theme Toggle inside Drawer -->
            <div class="flex items-center justify-between rounded-xl px-3 py-2 bg-white dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700">
              <div class="flex items-center gap-2.5 text-xs font-semibold text-slate-700 dark:text-slate-200">
                <Sun v-if="!isDark" class="h-4 w-4 text-amber-500" />
                <Moon v-else class="h-4 w-4 text-indigo-400" />
                <span>{{ isDark ? t('Dark mode') : t('Light mode') }}</span>
              </div>
              <button
                type="button"
                role="switch"
                :aria-checked="isDark"
                :aria-label="isDark ? t('Switch to light mode') : t('Switch to dark mode')"
                @click="toggleTheme"
                class="relative inline-flex h-5 w-10 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-200 ease-in-out focus:outline-none"
                :class="isDark ? 'bg-indigo-600' : 'bg-slate-300'"
              >
                <span
                  aria-hidden="true"
                  class="pointer-events-none inline-block h-4 w-4 transform rounded-full bg-white shadow ring-0 transition duration-200 ease-in-out"
                  :class="isDark ? 'translate-x-5' : 'translate-x-0'"
                />
              </button>
            </div>
          </div>
        </aside>
      </Transition>
    </Teleport>
  </header>
</template>

<script setup>
import { computed, nextTick, onMounted, onUnmounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { BookOpen, Check, Globe2, HelpCircle, Info, LogIn, Menu, Moon, PhoneCall, Plane, Printer, ShoppingBag, Sun, UserPlus, UserRound, X } from 'lucide-vue-next'
import { useLanguage } from '../../i18n'
import { useTheme } from '../../composables/useTheme'
import { accountService } from '../../services/api'
import { resolveImageUrl } from '../../utils/image'

const route = useRoute()
const { locale, t, setLocale } = useLanguage()
const { isDark, toggleTheme } = useTheme()

const mobileDrawerOpen = ref(false)
const profileName = ref('')
const profileEmail = ref('')
const profileAvatar = ref('')
const avatarLoadFailed = ref(false)
const languageMenu = ref(null)
const languageTrigger = ref(null)
const languageMenuOpen = ref(false)
const accountMenu = ref(null)
const accountTrigger = ref(null)
const accountMenuOpen = ref(false)
const isScrolled = ref(false)

function handleScroll() {
  isScrolled.value = window.scrollY > 4
}

// Auto close mobile drawer when route changes & lock body scroll
watch(
  () => route.path,
  () => {
    mobileDrawerOpen.value = false
  }
)

watch(mobileDrawerOpen, (open) => {
  if (typeof document !== 'undefined') {
    document.body.style.overflow = open ? 'hidden' : ''
  }
})

const profileInitials = computed(() => {
  const names = profileName.value.trim().split(/\s+/).filter(Boolean)
  return names.length ? names.slice(0, 2).map((name) => name[0].toUpperCase()).join('') : 'A'
})
const languages = [
  { value: 'en', label: 'EN', sublabel: 'English' },
  { value: 'kh', label: 'KH', sublabel: 'ភាសាខ្មែរ' },
]

function toggleLanguageMenu() {
  languageMenuOpen.value = !languageMenuOpen.value
}

async function openLanguageMenu() {
  languageMenuOpen.value = true
  await nextTick()
  languageMenu.value?.querySelector('[role="option"][aria-selected="true"]')?.focus()
}

function closeLanguageMenu() {
  languageMenuOpen.value = false
  languageTrigger.value?.focus()
}

function selectLanguage(value) {
  setLocale(value)
  closeLanguageMenu()
}

async function openAccountMenu() {
  accountMenuOpen.value = true
  await nextTick()
  accountMenu.value?.querySelector('[role="menuitem"]')?.focus()
}

function closeAccountMenu() {
  accountMenuOpen.value = false
  accountTrigger.value?.focus()
}

function handleOutsideClick(event) {
  if (languageMenuOpen.value && !languageMenu.value?.contains(event.target)) {
    languageMenuOpen.value = false
  }
  if (accountMenuOpen.value && !accountMenu.value?.contains(event.target)) {
    accountMenuOpen.value = false
  }
}

function handleKeydown(event) {
  if (event.key === 'Escape') {
    if (mobileDrawerOpen.value) mobileDrawerOpen.value = false
    if (languageMenuOpen.value) languageMenuOpen.value = false
    if (accountMenuOpen.value) accountMenuOpen.value = false
  }
}

async function updateProfileName() {
  try {
    const { data } = await accountService.getSession()
    profileName.value = data.authenticated ? data.user.name : ''
    profileEmail.value = data.authenticated ? data.user.email : ''
    let avatar = data.authenticated ? (data.user.avatar_url || '') : ''
    if (data.authenticated && !avatar) {
      try {
        const saved = JSON.parse(localStorage.getItem(`aerobyte-profile:${data.user.id}`) || '{}')
        if (saved.avatarUrl) avatar = saved.avatarUrl
      } catch (e) {
        // ignore
      }
    }
    profileAvatar.value = avatar
    avatarLoadFailed.value = false
  } catch (error) {
    console.error('Could not load the signed-in account for navigation:', error)
    profileName.value = ''
    profileEmail.value = ''
    profileAvatar.value = ''
  }
}

onMounted(() => {
  handleScroll()
  window.addEventListener('scroll', handleScroll, { passive: true })
  updateProfileName()
  window.addEventListener('storage', updateProfileName)
  window.addEventListener('aerobyte-profile-updated', updateProfileName)
  window.addEventListener('aerobyte-auth-updated', updateProfileName)
  document.addEventListener('click', handleOutsideClick)
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  if (typeof document !== 'undefined') {
    document.body.style.overflow = ''
  }
  window.removeEventListener('scroll', handleScroll)
  window.removeEventListener('storage', updateProfileName)
  window.removeEventListener('aerobyte-profile-updated', updateProfileName)
  window.removeEventListener('aerobyte-auth-updated', updateProfileName)
  document.removeEventListener('click', handleOutsideClick)
  document.removeEventListener('keydown', handleKeydown)
})
</script>
