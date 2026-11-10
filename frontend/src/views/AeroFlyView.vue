<template>
  <div class="aero-fly-root relative isolate min-h-screen transition-colors duration-300 bg-[#f8fafc] dark:bg-[#04060f] text-slate-800 dark:text-[#f3f6ff] overflow-x-hidden selection:bg-orange-500/20 selection:text-orange-600 dark:selection:bg-[#5df0a8]/20 dark:selection:text-[#5df0a8]">
    <!-- Fixed WebGL 3D Real Drone Canvas (Kept identical as requested) -->
    <canvas ref="canvasRef" class="fixed inset-0 w-full h-full block z-0 pointer-events-none"></canvas>

    <!-- Loading Indicator overlay while real 3D drone GLB loads -->
    <div
      v-if="loadingProgress < 100"
      class="fixed bottom-6 right-6 z-50 flex items-center gap-3 bg-white/95 dark:bg-[rgba(12,18,38,0.9)] border border-slate-300 dark:border-[rgba(150,175,230,0.2)] px-4 py-2 rounded-full backdrop-blur-md shadow-xl text-xs font-mono font-bold text-slate-800 dark:text-white transition-opacity duration-500"
      :class="loadingProgress >= 100 ? 'opacity-0 pointer-events-none' : 'opacity-100'"
    >
      <div class="w-3.5 h-3.5 border-2 border-orange-500 dark:border-[#5df0a8] border-t-transparent rounded-full animate-spin"></div>
      <span>{{ t('SYS // LOADING DRONE 3D') }} · {{ loadingProgress }}%</span>
    </div>

    <!-- Notification Toast -->
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
        class="fixed top-24 right-6 z-50 flex items-center gap-3 px-5 py-2.5 rounded-full bg-slate-900/95 dark:bg-[#070e24]/95 text-white border border-emerald-500/40 shadow-2xl backdrop-blur-xl text-xs font-mono font-semibold"
      >
        <span class="text-emerald-400">✓</span>
        <span>{{ toastMessage }}</span>
      </div>
    </transition>

    <!-- Page Content Floating Over Fixed 3D Drone -->
    <div class="relative z-10">

      <!-- SECTION 1: HERO (Pure 2-Line Cinematic Layout placed on top of the drone) -->
      <section class="h-[calc(100vh-64px)] min-h-[520px] sm:min-h-[580px] flex flex-col items-center justify-between text-center px-4 sm:px-6 pt-6 sm:pt-12 pb-6 sm:pb-8 relative select-none">
        <!-- TOP AREA: TWO TEXT LINES DIRECTLY ABOVE THE DRONE -->
        <div class="max-w-4xl mx-auto space-y-2 sm:space-y-3.5 pt-1 sm:pt-4">
          <!-- LINE 1: BOLD GEOMETRIC TITLE -->
          <h1 class="text-4xl sm:text-6xl md:text-8xl lg:text-9xl font-black tracking-[0.10em] sm:tracking-[0.18em] uppercase text-[#0c1e5b] dark:text-white drop-shadow-sm font-sans transition-colors">
            AERO FLY
          </h1>

          <!-- LINE 2: UPPERCASE SUBTITLE WITH SUBTLE RED DOT ACCENTS -->
          <div class="relative inline-block max-w-sm sm:max-w-none px-2">
            <p class="text-[10px] sm:text-sm md:text-base font-bold tracking-[0.16em] sm:tracking-[0.32em] uppercase text-slate-700 dark:text-white/90">
              {{ t('THE OPEN DRONE FLIGHT COMMUNITY FOR CAMBODIA.') }}
            </p>
            <!-- Minimal Red Dot Accents from reference image -->
            <div class="mt-2 sm:mt-2.5 flex items-center justify-center gap-1.5 opacity-80">
              <span class="w-1 h-1 rounded-full bg-red-500"></span>
              <span class="w-1 h-1 rounded-full bg-red-500"></span>
              <span class="w-1 h-1 rounded-full bg-red-500"></span>
              <span class="w-1 h-1 rounded-full bg-red-500"></span>
              <span class="w-1 h-1 rounded-full bg-red-500"></span>
              <span class="w-1 h-1 rounded-full bg-red-500"></span>
              <span class="w-1 h-1 rounded-full bg-red-500"></span>
              <span class="w-1 h-1 rounded-full bg-red-500"></span>
            </div>
          </div>
        </div>

        <!-- Middle spacer keeping drone clear and unobstructed in view -->
        <div class="flex-1 pointer-events-none"></div>

        <!-- Scroll Indicator at bottom -->
        <a
          href="#sessions"
          class="flex flex-col items-center gap-1.5 opacity-50 hover:opacity-100 active:scale-95 transition text-[10px] font-mono tracking-widest uppercase text-slate-400 dark:text-slate-500 cursor-pointer py-2"
        >
          <span>{{ t('SCROLL') }}</span>
          <span class="animate-bounce">↓</span>
        </a>
      </section>

      <!-- SECTION 2: GATHERINGS (Drone flies to LEFT on desktop, centered aloft on mobile) -->
      <section id="sessions" class="pt-4 sm:pt-10 pb-12 sm:pb-16 px-4 sm:px-6 lg:px-8 max-w-[1240px] mx-auto">
        <div class="w-full grid lg:grid-cols-12 gap-6 lg:gap-12 items-center">
          <!-- Left 5 cols: Completely clear open air for 3D drone flying on the left -->
          <div class="hidden lg:block lg:col-span-5 pointer-events-none"></div>

          <!-- Right 7 cols: Content & Text on the right -->
          <div class="lg:col-span-7 space-y-4 sm:space-y-5">
            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-1.5 pb-3 border-b border-slate-200 dark:border-white/10">
              <div>
                <div class="text-[10px] font-mono tracking-widest uppercase text-slate-400 dark:text-slate-500">{{ t('01 // SESSIONS') }}</div>
                <h2 class="text-xl sm:text-3xl font-black text-[#0c1e5b] dark:text-white">{{ t('Weekend Flights') }}</h2>
              </div>
              <span class="text-[10px] sm:text-[11px] font-mono text-emerald-600 dark:text-[#5df0a8] font-bold self-start sm:self-auto">
                {{ t('● SKY CLEAR · 8 KM/H') }}
              </span>
            </div>

            <!-- Minimal Stats Line -->
            <div class="flex flex-wrap items-center gap-3 sm:gap-6 text-[11px] sm:text-xs font-mono text-slate-500 dark:text-slate-400 py-0.5">
              <span><strong>140+</strong> {{ t('Pilots') }}</span>
              <span>•</span>
              <span><strong>5.8 GHz</strong> {{ t('Band') }}</span>
              <span>•</span>
              <span><strong>{{ t('Weekly') }}</strong> {{ t('Gatherings') }}</span>
            </div>

            <!-- Ultra-Short Sessions List -->
            <div class="space-y-2.5 sm:space-y-3">
              <div
                v-for="session in flightSessions"
                :key="session.id"
                class="p-3.5 sm:p-4 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex flex-col sm:flex-row sm:items-center justify-between gap-3 sm:gap-4 hover:border-slate-400 dark:hover:border-white/20 transition shadow-xs"
              >
                <div class="space-y-0.5">
                  <div class="flex items-center gap-2 text-[10px] font-mono text-slate-400">
                    <span class="uppercase font-bold text-slate-600 dark:text-slate-300">{{ session.category }}</span>
                    <span>·</span>
                    <span>{{ session.time }}</span>
                  </div>
                  <h3 class="text-sm sm:text-base font-bold text-[#0c1e5b] dark:text-white">
                    {{ session.title }}
                  </h3>
                  <p class="text-xs text-slate-500 dark:text-slate-400">
                    📍 {{ session.location }}
                  </p>
                </div>

                <div class="flex items-center justify-between sm:justify-end gap-3 shrink-0 pt-1 sm:pt-0 border-t sm:border-t-0 border-slate-100 dark:border-white/5">
                  <span class="text-[10px] sm:text-[11px] font-mono text-slate-400">
                    {{ session.attendees.length }} {{ t('attending') }}
                  </span>
                  <button
                    type="button"
                    @click="toggleRSVP(session)"
                    class="px-4 py-1.5 min-h-[34px] rounded-full text-xs font-bold active:scale-95 transition cursor-pointer"
                    :class="session.isJoined
                      ? 'bg-emerald-500 text-white'
                      : 'bg-slate-100 dark:bg-white/10 hover:bg-slate-200 dark:hover:bg-white/20 text-[#0c1e5b] dark:text-white'"
                  >
                    {{ session.isJoined ? t('✓ Joined') : t('RSVP') }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- SECTION: THE MIDDLE STOP (Drone in Middle, Text Cleanly Under Drone with Masked Sliding Reveal) -->
      <section id="middle" class="h-[120vh] relative">
        <div class="sticky top-0 h-screen w-full flex flex-col items-center justify-start px-4 pt-[45vh] sm:pt-[52vh] overflow-hidden pointer-events-none select-none">
          <!-- TWO TEXT LINES CLEANLY UNDER THE DRONE (Elevated into upper UX/UI frame, NOT sunken down below!) -->
          <div class="max-w-4xl mx-auto text-center space-y-2 sm:space-y-3 relative z-10 pointer-events-auto">
            <!-- LINE 1: BOLD GEOMETRIC TITLE (Masked Sliding Reveal) -->
            <div class="overflow-hidden py-1 inline-block">
              <h2
                class="text-3xl sm:text-5xl md:text-7xl lg:text-8xl font-black tracking-[0.08em] sm:tracking-[0.18em] uppercase text-[#0c1e5b] dark:text-white drop-shadow-sm font-sans transition-all duration-700 ease-[cubic-bezier(0.16,1,0.3,1)] transform"
                :class="{
                  'translate-y-0 opacity-100': middleTextState === 'active',
                  'translate-y-[120%] opacity-0': middleTextState === 'before',
                  '-translate-y-[120%] opacity-0': middleTextState === 'after'
                }"
              >
                {{ t('FLY AS ONE') }}
              </h2>
            </div>

            <!-- LINE 2: UPPERCASE SUBTITLE (Masked Sliding Reveal with Stagger) -->
            <div class="block max-w-sm sm:max-w-none px-2">
              <div class="overflow-hidden py-1 inline-block">
                <p
                  class="text-[11px] sm:text-sm md:text-base font-bold tracking-[0.14em] sm:tracking-[0.32em] uppercase text-slate-700 dark:text-white/90 transition-all duration-700 delay-100 ease-[cubic-bezier(0.16,1,0.3,1)] transform"
                  :class="{
                    'translate-y-0 opacity-100': middleTextState === 'active',
                    'translate-y-[120%] opacity-0': middleTextState === 'before',
                    '-translate-y-[120%] opacity-0': middleTextState === 'after'
                  }"
                >
                  {{ t('FROM FIRST HOVER TO PRO FREESTYLE & CINEMATIC MISSIONS.') }}
                </p>
              </div>

              <!-- Minimal Red Dot Accents -->
              <div
                class="mt-2 sm:mt-2.5 flex items-center justify-center gap-1.5 transition-all duration-500 delay-200 ease-out transform"
                :class="{
                  'opacity-80 scale-100 translate-y-0': middleTextState === 'active',
                  'opacity-0 scale-75 translate-y-2': middleTextState !== 'active'
                }"
              >
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section id="benefits" class="pt-4 sm:pt-10 pb-12 sm:pb-16 px-4 sm:px-6 lg:px-8 max-w-[1240px] mx-auto">
        <div class="w-full grid lg:grid-cols-12 gap-6 lg:gap-12 items-center">
          <!-- Left 7 cols: Content & Text on the left -->
          <div class="lg:col-span-7 space-y-4 sm:space-y-5">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-1.5 pb-3 border-b border-slate-200 dark:border-white/10">
              <div>
                <div class="text-[10px] font-mono tracking-widest uppercase text-slate-400 dark:text-slate-500">{{ t('02 // MEMBERSHIP BENEFITS') }}</div>
                <h2 class="text-xl sm:text-3xl font-black text-[#0c1e5b] dark:text-white">{{ t('What You Get When You Join') }}</h2>
              </div>
              <span class="text-[10px] sm:text-[11px] font-mono text-emerald-600 dark:text-[#5df0a8] font-bold self-start sm:self-auto">
                {{ t('● 100% FREE COMMUNITY') }}
              </span>
            </div>

            <p class="text-xs text-slate-600 dark:text-[#9aa6c4]">
              {{ t("Join Cambodia's open FPV collective. Everything you need to build, tune, and fly safely with active pilots.") }}
            </p>

            <!-- 6 Key Member Benefits Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-2.5 sm:gap-3">
              <!-- Benefit 1: Aero Print Discounts -->
              <div class="p-3.5 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex items-start gap-3 hover:border-slate-400 dark:hover:border-white/20 transition shadow-xs">
                <div class="w-8 h-8 rounded-xl bg-purple-500/10 text-purple-600 dark:text-purple-400 flex items-center justify-center shrink-0 text-sm">
                  🖨️
                </div>
                <div class="space-y-0.5">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">{{ t('Aero Print 3D Discounts') }}</h4>
                  <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-snug">
                    {{ t('Exclusive member discounts when you order 3D prints — custom TPU GoPro mounts, arm skids, antenna tubes, and drone armor.') }}
                  </p>
                </div>
              </div>

              <!-- Benefit 2: Free Ta Khmau Lab Access -->
              <div class="p-3.5 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex items-start gap-3 hover:border-slate-400 dark:hover:border-white/20 transition shadow-xs">
                <div class="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0 text-sm">
                  📍
                </div>
                <div class="space-y-0.5">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">{{ t('Free Ta Khmau Lab Access') }}</h4>
                  <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-snug">
                    {{ t('Our workshop in Ta Khmau is 100% free. Come and join anytime in your free time — use open soldering benches and tools at no cost.') }}
                  </p>
                </div>
              </div>

              <!-- Benefit 3: Meet Pro Pilots & Mechanics -->
              <div class="p-3.5 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex items-start gap-3 hover:border-slate-400 dark:hover:border-white/20 transition shadow-xs">
                <div class="w-8 h-8 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 text-sm">
                  🛠️
                </div>
                <div class="space-y-0.5">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">{{ t('Pro Config & Mechanic Team') }}</h4>
                  <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-snug">
                    {{ t('Bring your drone to configure Betaflight, tune rates, and discuss electronics directly with our professional pilots and mechanics.') }}
                  </p>
                </div>
              </div>

              <!-- Benefit 4: Find Flight Partners (Never Fly Alone) -->
              <div class="p-3.5 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex items-start gap-3 hover:border-slate-400 dark:hover:border-white/20 transition shadow-xs">
                <div class="w-8 h-8 rounded-xl bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 flex items-center justify-center shrink-0 text-sm">
                  🤝
                </div>
                <div class="space-y-0.5">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">{{ t('Have a Drone? Find Flight Buddies') }}</h4>
                  <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-snug">
                    {{ t('Have a drone but no partner to fly with? Come and join our group flights, meet local pilots, find spotters, and fly together safely.') }}
                  </p>
                </div>
              </div>

              <!-- Benefit 5: Beginners & Hobbyists Welcome (No Drone Needed) -->
              <div class="p-3.5 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex items-start gap-3 hover:border-slate-400 dark:hover:border-white/20 transition shadow-xs">
                <div class="w-8 h-8 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400 flex items-center justify-center shrink-0 text-sm">
                  🐣
                </div>
                <div class="space-y-0.5">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">{{ t('No Drone Yet? You Can Still Join!') }}</h4>
                  <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-snug">
                    {{ t('New to drones or have a hobby curiosity without gear? You are 100% welcome! Hang out, spectate in goggles, try sims, and learn for free.') }}
                  </p>
                </div>
              </div>

              <!-- Benefit 6: Coordinated Airspace & Field Spares -->
              <div class="p-3.5 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex items-start gap-3 hover:border-slate-400 dark:hover:border-white/20 transition shadow-xs">
                <div class="w-8 h-8 rounded-xl bg-rose-500/10 text-rose-600 dark:text-rose-400 flex items-center justify-center shrink-0 text-sm">
                  ⚡
                </div>
                <div class="space-y-0.5">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">{{ t('Coordinated Airspace & Field Spares') }}</h4>
                  <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-snug">
                    {{ t('Zero video stomping with coordinated 5.8 GHz & HD channels, plus shared field toolkits and spare hardware so you never get grounded.') }}
                  </p>
                </div>
              </div>
            </div>
            <!-- Bottom action banner -->
            <div class="pt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <span class="text-[11px] text-slate-400 dark:text-slate-500 font-mono">
                {{ t('Open to Tiny Whoop, 3.5" cinewhoop, 5" freestyle & long-range.') }}
              </span>
              <a
                href="https://t.me/aerobyteacademy"
                target="_blank"
                rel="noopener noreferrer"
                class="w-full sm:w-auto inline-flex items-center justify-center gap-1.5 px-5 py-2.5 rounded-full text-xs font-bold bg-[#0c1e5b] dark:bg-white text-white dark:text-[#0c1e5b] hover:opacity-90 active:scale-95 transition cursor-pointer shrink-0 shadow-sm"
              >
                <span>{{ t('Join Telegram Hub') }}</span>
                <span>↗</span>
              </a>
            </div>
          </div>

          <!-- Right 5 cols: Completely clear open air for 3D drone flying on the right -->
          <div class="hidden lg:block lg:col-span-5 pointer-events-none"></div>
        </div>
      </section>

      <!-- SECTION: THE SECOND MIDDLE STOP (Drone Rotates to Center, Big Line Text Cleanly Under Drone) -->
      <section id="middle-two" class="h-[120vh] relative">
        <div class="sticky top-0 h-screen w-full flex flex-col items-center justify-start px-4 pt-[45vh] sm:pt-[52vh] overflow-hidden pointer-events-none select-none">
          <!-- TWO TEXT LINES CLEANLY UNDER THE DRONE -->
          <div class="max-w-4xl mx-auto text-center space-y-2 sm:space-y-3 relative z-10 pointer-events-auto">
            <!-- LINE 1: BOLD GEOMETRIC TITLE (Masked Sliding Reveal) -->
            <div class="overflow-hidden py-1 inline-block">
              <h2
                class="text-3xl sm:text-5xl md:text-7xl lg:text-8xl font-black tracking-[0.08em] sm:tracking-[0.18em] uppercase text-[#0c1e5b] dark:text-white drop-shadow-sm font-sans transition-all duration-700 ease-[cubic-bezier(0.16,1,0.3,1)] transform"
                :class="{
                  'translate-y-0 opacity-100': middleTextTwoState === 'active',
                  'translate-y-[120%] opacity-0': middleTextTwoState === 'before',
                  '-translate-y-[120%] opacity-0': middleTextTwoState === 'after'
                }"
              >
                {{ t('BUILT TO SOAR') }}
              </h2>
            </div>

            <!-- LINE 2: UPPERCASE SUBTITLE (Masked Sliding Reveal with Stagger) -->
            <div class="block max-w-sm sm:max-w-none px-2">
              <div class="overflow-hidden py-1 inline-block">
                <p
                  class="text-[11px] sm:text-sm md:text-base font-bold tracking-[0.14em] sm:tracking-[0.32em] uppercase text-slate-700 dark:text-white/90 transition-all duration-700 delay-100 ease-[cubic-bezier(0.16,1,0.3,1)] transform"
                  :class="{
                    'translate-y-0 opacity-100': middleTextTwoState === 'active',
                    'translate-y-[120%] opacity-0': middleTextTwoState === 'before',
                    '-translate-y-[120%] opacity-0': middleTextTwoState === 'after'
                  }"
                >
                  {{ t('FROM CAD BENCH TO FULL THROTTLE FREEDOM.') }}
                </p>
              </div>

              <!-- Minimal Red Dot Accents -->
              <div
                class="mt-2 sm:mt-2.5 flex items-center justify-center gap-1.5 transition-all duration-500 delay-200 ease-out transform"
                :class="{
                  'opacity-80 scale-100 translate-y-0': middleTextTwoState === 'active',
                  'opacity-0 scale-75 translate-y-2': middleTextTwoState !== 'active'
                }"
              >
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
                <span class="w-1.5 h-1.5 rounded-full bg-red-500"></span>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- SECTION 5: AERO STORE & LAB SUPPLY (Drone Ended in Middle, Clean Store Display Without Overlap) -->
      <section id="store" class="pt-10 sm:pt-16 pb-12 sm:pb-16 px-4 sm:px-6 lg:px-8 max-w-[1240px] mx-auto">

        <div class="w-full space-y-8 sm:space-y-10 relative z-10">
          <!-- Section Header: What Aero Store Is & Does -->
          <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-3 sm:gap-4 pb-4 border-b border-slate-200 dark:border-white/10">
            <div>
              <div class="text-[10px] font-mono tracking-widest uppercase text-slate-400 dark:text-slate-500">
                {{ t('03 // HARDWARE & LAB SUPPLY') }}
              </div>
              <h2 class="text-xl sm:text-3xl lg:text-4xl font-black text-[#0c1e5b] dark:text-white">
                {{ t('Aero Store & Hardware Lab') }}
              </h2>
              <p class="text-xs sm:text-sm text-slate-600 dark:text-slate-400 mt-1 max-w-2xl">
                {{ t("Cambodia's dedicated hardware hub for BNF FPV quads, robotics lab kits, custom 3D TPU parts, and hands-on bench tuning.") }}
              </p>
            </div>

            <div class="flex items-center gap-2.5 shrink-0 pt-1 sm:pt-0">
              <router-link
                to="/store"
                class="w-full sm:w-auto justify-center px-5 py-2.5 rounded-full text-xs font-bold bg-[#0c1e5b] dark:bg-white text-white dark:text-[#0c1e5b] hover:opacity-90 active:scale-95 transition shadow-sm inline-flex items-center gap-1.5 cursor-pointer"
              >
                <span>{{ t('Browse Store Catalog') }}</span>
                <span>→</span>
              </router-link>
            </div>
          </div>

          <!-- BLOCK 1: WHAT WE DO IN AERO STORE (3 Core Specialties) -->
          <div class="space-y-4">
            <div class="flex items-center justify-between">
              <h3 class="text-xs font-mono font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                {{ t('What We Do in Aero Store') }}
              </h3>
              <span class="text-[11px] font-mono text-emerald-600 dark:text-[#5df0a8] font-bold">
                {{ t('● 100% BENCH-TESTED') }}
              </span>
            </div>

            <div class="grid grid-cols-1 md:grid-cols-3 gap-3 sm:gap-4">
              <!-- Specialty 1: FPV Drone Hardware -->
              <div class="p-4 sm:p-5 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex flex-col justify-between gap-3 sm:gap-4 hover:border-slate-400 dark:hover:border-white/20 transition shadow-xs">
                <div class="space-y-2 sm:space-y-2.5">
                  <div class="flex items-center justify-between">
                    <span class="text-2xl">🚁</span>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-sky-500/10 text-sky-600 dark:text-sky-400">
                      {{ t('FPV DRONES') }}
                    </span>
                  </div>
                  <h4 class="text-sm sm:text-base font-bold text-[#0c1e5b] dark:text-white">
                    {{ t('Flight-Tested FPV Quads & Parts') }}
                  </h4>
                  <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                    {{ t('From beginner Tiny Whoops to 5-inch freestyle beasts, ESC stacks, brushless motors, ELRS radios, and digital HD video transmitters.') }}
                  </p>
                </div>

                <div class="pt-2.5 sm:pt-3 border-t border-slate-100 dark:border-white/5 space-y-2">
                  <div class="flex flex-wrap gap-1.5 text-[10px] font-mono text-slate-500 dark:text-slate-400">
                    <span class="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-white/5">{{ t('BNF Quads') }}</span>
                    <span class="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-white/5">{{ t('55A Stacks') }}</span>
                    <span class="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-white/5">{{ t('ELRS 2.4G') }}</span>
                  </div>
                  <router-link
                    to="/store"
                    class="inline-flex items-center gap-1 text-xs font-bold text-[#0c1e5b] dark:text-white hover:underline pt-0.5"
                  >
                    <span>{{ t('View Drone Gear') }}</span>
                    <span>→</span>
                  </router-link>
                </div>
              </div>

              <!-- Specialty 2: Robotics & STEM Maker Kits -->
              <div class="p-4 sm:p-5 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex flex-col justify-between gap-3 sm:gap-4 hover:border-slate-400 dark:hover:border-white/20 transition shadow-xs">
                <div class="space-y-2 sm:space-y-2.5">
                  <div class="flex items-center justify-between">
                    <span class="text-2xl">🤖</span>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-emerald-500/10 text-emerald-600 dark:text-emerald-400">
                      {{ t('STEM & MAKER') }}
                    </span>
                  </div>
                  <h4 class="text-sm sm:text-base font-bold text-[#0c1e5b] dark:text-white">
                    {{ t('Robotics & IoT Learning Kits') }}
                  </h4>
                  <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                    {{ t('ESP32 dual-core learning kits, Arduino Uno compatible sets, sensor arrays, and motor driver shields designed for students and university labs.') }}
                  </p>
                </div>

                <div class="pt-2.5 sm:pt-3 border-t border-slate-100 dark:border-white/5 space-y-2">
                  <div class="flex flex-wrap gap-1.5 text-[10px] font-mono text-slate-500 dark:text-slate-400">
                    <span class="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-white/5">{{ t('ESP32 Lab Kit') }}</span>
                    <span class="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-white/5">{{ t('IoT Sensors') }}</span>
                    <span class="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-white/5">{{ t('Motor Shields') }}</span>
                  </div>
                  <router-link
                    to="/store"
                    class="inline-flex items-center gap-1 text-xs font-bold text-[#0c1e5b] dark:text-white hover:underline pt-0.5"
                  >
                    <span>{{ t('View Maker Kits') }}</span>
                    <span>→</span>
                  </router-link>
                </div>
              </div>

              <!-- Specialty 3: Custom 3D TPU Armor -->
              <div class="p-4 sm:p-5 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex flex-col justify-between gap-3 sm:gap-4 hover:border-slate-400 dark:hover:border-white/20 transition shadow-xs">
                <div class="space-y-2 sm:space-y-2.5">
                  <div class="flex items-center justify-between">
                    <span class="text-2xl">🖨️</span>
                    <span class="px-2 py-0.5 rounded-full text-[10px] font-mono font-bold bg-purple-500/10 text-purple-600 dark:text-purple-400">
                      {{ t('3D TPU LAB') }}
                    </span>
                  </div>
                  <h4 class="text-sm sm:text-base font-bold text-[#0c1e5b] dark:text-white">
                    {{ t('Crash-Proof 3D TPU Armor') }}
                  </h4>
                  <p class="text-xs text-slate-600 dark:text-slate-300 leading-relaxed">
                    {{ t('Custom vibration-damped GoPro mounts, motor arm skids, antenna holders, and frame bumpers precision-printed for your exact drone frame.') }}
                  </p>
                </div>

                <div class="pt-2.5 sm:pt-3 border-t border-slate-100 dark:border-white/5 space-y-2">
                  <div class="flex flex-wrap gap-1.5 text-[10px] font-mono text-slate-500 dark:text-slate-400">
                    <span class="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-white/5">{{ t('GoPro Mounts') }}</span>
                    <span class="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-white/5">{{ t('Arm Guards') }}</span>
                    <span class="px-2 py-0.5 rounded-md bg-slate-100 dark:bg-white/5">{{ t('Antenna Tubes') }}</span>
                  </div>
                  <router-link
                    to="/print"
                    class="inline-flex items-center gap-1 text-xs font-bold text-[#0c1e5b] dark:text-white hover:underline pt-0.5"
                  >
                    <span>{{ t('Custom 3D Printing') }}</span>
                    <span>→</span>
                  </router-link>
                </div>
              </div>
            </div>
          </div>

          <!-- BLOCK 2: WHAT CUSTOMERS NEED & WHY THEY NEED AERO STORE -->
          <div class="space-y-4 pt-4 border-t border-slate-200 dark:border-white/10">
            <div>
              <h3 class="text-xs font-mono font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
                {{ t('Why You Need Aero Store & How We Help You') }}
              </h3>
              <p class="text-xs sm:text-sm font-bold text-[#0c1e5b] dark:text-white mt-0.5">
                {{ t('Solving the most expensive mistakes pilots and builders face in Cambodia.') }}
              </p>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-3.5">
              <!-- Reason 1: No Burnt Boards -->
              <div class="p-3.5 sm:p-4 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex items-start gap-3 sm:gap-3.5 shadow-xs">
                <div class="w-8 sm:w-9 h-8 sm:h-9 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400 flex items-center justify-center shrink-0 text-sm sm:text-base">
                  ⚡
                </div>
                <div class="space-y-1">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">
                    {{ t('Zero Burnt Electronics (Pre-Checked Smoke Stop)') }}
                  </h4>
                  <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed">
                    {{ t('The #1 beginner heartbreak is plugging in a battery and frying a $60 flight controller or ESC. Every stack and motor we deliver is pre-checked on multimeter bench diagnostics with verified wiring guides.') }}
                  </p>
                </div>
              </div>

              <!-- Reason 2: Fast Local Cambodia Stock -->
              <div class="p-3.5 sm:p-4 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex items-start gap-3 sm:gap-3.5 shadow-xs">
                <div class="w-8 sm:w-9 h-8 sm:h-9 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 text-sm sm:text-base">
                  🚚
                </div>
                <div class="space-y-1">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">
                    {{ t('Local Cambodia Stock (No 4-Week Customs Wait)') }}
                  </h4>
                  <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed">
                    {{ t('When you crash on Saturday, you cannot wait 3 to 4 weeks for AliExpress or risk import customs. We keep genuine inventory in Phnom Penh and dispatch nationwide in 24–48 hours.') }}
                  </p>
                </div>
              </div>

              <!-- Reason 3: Hands-on Lab Bench Support -->
              <div class="p-3.5 sm:p-4 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex items-start gap-3.5 shadow-xs">
                <div class="w-8 sm:w-9 h-8 sm:h-9 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0 text-sm sm:text-base">
                  🛠️
                </div>
                <div class="space-y-1">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">
                    {{ t('Free Ta Khmau Bench Lab & Tuning Guidance') }}
                  </h4>
                  <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed">
                    {{ t('Need help soldering tiny motor pads, flashing Betaflight 4.5, or binding ELRS? Bring your parts to our Ta Khmau Lab for free smoke-stopper maiden checks and rate tuning.') }}
                  </p>
                </div>
              </div>

              <!-- Reason 4: Correct Hardware Matching -->
              <div class="p-3.5 sm:p-4 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex items-start gap-3.5 shadow-xs">
                <div class="w-8 sm:w-9 h-8 sm:h-9 rounded-xl bg-rose-500/10 text-rose-600 dark:text-rose-400 flex items-center justify-center shrink-0 text-sm sm:text-base">
                  🎯
                </div>
                <div class="space-y-1">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">
                    {{ t('Engineered Compatibility (Zero Guesswork)') }}
                  </h4>
                  <p class="text-[11px] text-slate-600 dark:text-slate-400 leading-relaxed">
                    {{ t('Never accidentally buy 4S motors for a 6S build or mismatched antenna polarizations. Our engineers review your setup before purchase to ensure 100% plug-and-fly synergy.') }}
                  </p>
                </div>
              </div>
            </div>
          </div>

          <!-- BLOCK 3: QUICK CONSULT & TA KHMAU LAB CONTACT -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 sm:gap-4 pt-4 border-t border-slate-200 dark:border-white/10">
            <!-- Telegram Hub -->
            <div class="p-4 sm:p-5 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex flex-col justify-between gap-3 shadow-xs">
              <div class="space-y-1.5">
                <div class="text-xl">💬</div>
                <h3 class="text-sm font-bold text-[#0c1e5b] dark:text-white">
                  {{ t('Chat with an Aero Store Engineer') }}
                </h3>
                <p class="text-xs text-slate-500 dark:text-slate-400">
                  {{ t('Send your build questions, part requirements, or custom order inquiries directly to our lab pilots.') }}
                </p>
              </div>
              <div class="pt-2">
                <a
                  href="https://t.me/aerobyteacademy"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="inline-flex items-center gap-1.5 text-xs font-bold text-sky-600 dark:text-cyan-400 hover:underline active:scale-95 transition"
                >
                  <span>{{ t('Open Telegram Chat') }}</span>
                  <span>↗</span>
                </a>
              </div>
            </div>

            <!-- Ta Khmau Flight & Maker Lab -->
            <div class="p-4 sm:p-5 rounded-2xl bg-white/92 dark:bg-[#070e24]/90 border border-slate-200/90 dark:border-white/10 backdrop-blur-xl flex flex-col justify-between gap-3 shadow-xs">
              <div class="space-y-1.5">
                <div class="text-xl">📍</div>
                <h3 class="text-sm font-bold text-[#0c1e5b] dark:text-white">
                  {{ t('Ta Khmau Flight & Maker Lab') }}
                </h3>
                <p class="text-xs text-slate-500 dark:text-slate-400">
                  {{ t('Free open soldering benches, smoke stoppers, Betaflight diagnostics, and in-person hardware pickup.') }}
                </p>
              </div>
              <div class="pt-2">
                <a
                  href="https://maps.google.com/?q=Ta+Khmau+Cambodia"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="inline-flex items-center gap-1.5 text-xs font-bold text-[#0c1e5b] dark:text-white hover:underline active:scale-95 transition"
                >
                  <span>{{ t('Get Directions') }}</span>
                  <span>↗</span>
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- MINIMALIST FOOTER -->
      <footer ref="footerRef" class="py-8 sm:py-12 px-4 sm:px-6 text-center border-t border-slate-200 dark:border-white/10 max-w-[1240px] mx-auto flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 dark:text-slate-500 font-mono gap-4 relative z-20 bg-slate-50 dark:bg-slate-950">
        <div>© {{ currentYear }} {{ t('AERO FLY // CAMBODIA DRONE & HARDWARE COLLECTIVE') }}</div>
        <div class="flex flex-wrap items-center justify-center gap-4 sm:gap-6">
          <a href="https://t.me/aerobyteacademy" target="_blank" rel="noopener noreferrer" class="hover:text-slate-800 dark:hover:text-white py-1 transition">Telegram</a>
          <a href="#sessions" class="hover:text-slate-800 dark:hover:text-white py-1 transition">{{ t('Sessions') }}</a>
          <a href="#benefits" class="hover:text-slate-800 dark:hover:text-white py-1 transition">{{ t('Benefits') }}</a>
          <a href="#store" class="hover:text-slate-800 dark:hover:text-white py-1 transition">{{ t('Aero Store') }}</a>
        </div>
      </footer>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { DRACOLoader } from 'three/examples/jsm/loaders/DRACOLoader.js'
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js'
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js'
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js'
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass.js'
import { GammaCorrectionShader } from 'three/examples/jsm/shaders/GammaCorrectionShader.js'
import { useTheme } from '../composables/useTheme'
import { useI18n } from '../i18n'

const { isDark } = useTheme()
const { t } = useI18n()

const canvasRef = ref(null)
const footerRef = ref(null)
const loadingProgress = ref(0)
const currentYear = new Date().getFullYear()
const toastMessage = ref('')
const middleTextState = ref('before') // 'before' | 'active' | 'after'
const middleTextTwoState = ref('before') // 'before' | 'active' | 'after'

function showToast(msg) {
  toastMessage.value = msg
  setTimeout(() => {
    toastMessage.value = ''
  }, 3500)
}

// ----------------------------------------------------
// COMMUNITY SESSIONS DATA (Clear & Concise)
// ----------------------------------------------------
const joinedSessionIds = ref([2])

const rawFlightSessions = [
  {
    id: 1,
    titleKey: 'Sunrise Freestyle & Proximity Run',
    categoryKey: 'WEEKEND FLY-IN',
    timeKey: 'Sun · 6:30 AM',
    locationKey: 'AeroByte Flight Zone, Ta Khmau',
    descriptionKey: 'Open grass runway with low morning wind. Freestyle gaps, proximity practice, and active spotters.',
    attendees: ['Vuthy', 'Dara', 'Alex', 'Samnang', 'Chhay', 'Sreypov']
  },
  {
    id: 2,
    titleKey: 'Bench Tuning & Maiden Diagnostics',
    categoryKey: 'TECH WORKSHOP',
    timeKey: 'Sat · 2:00 PM',
    locationKey: 'AeroByte Maker Lab, Ta Khmau',
    descriptionKey: 'Free open soldering bench, Betaflight 4.5 tuning, smoke-stopper tests, and motor telemetry checks.',
    attendees: ['Rithy', 'Bona', 'Sophea', 'Sovann', 'Alex']
  },
  {
    id: 3,
    titleKey: 'Beginner Clinic & Simulator Coaching',
    categoryKey: 'COMMUNITY CLINIC',
    timeKey: 'Sat & Sun · 4:30 PM',
    locationKey: 'Ta Khmau Lab & Testing Field',
    descriptionKey: 'Zero gear required. First-timer goggles spectating, simulator practice, and flight buddy pairing.',
    attendees: ['Samnang', 'Dara', 'Alex', 'Kosal']
  }
]

const flightSessions = computed(() =>
  rawFlightSessions.map((session) => {
    const isJoined = joinedSessionIds.value.includes(session.id)
    const attendees = [...session.attendees]
    if (isJoined && !attendees.includes('You')) {
      attendees.push('You')
    }
    return {
      id: session.id,
      title: t(session.titleKey),
      category: t(session.categoryKey),
      time: t(session.timeKey),
      location: t(session.locationKey),
      description: t(session.descriptionKey),
      attendees,
      isJoined
    }
  })
)

function toggleRSVP(session) {
  if (joinedSessionIds.value.includes(session.id)) {
    joinedSessionIds.value = joinedSessionIds.value.filter((id) => id !== session.id)
    showToast(`${t('RSVP Cancelled:')} ${session.title}`)
  } else {
    joinedSessionIds.value.push(session.id)
    showToast(`${t('RSVP Confirmed:')} ${session.title}`)
  }
}

// ----------------------------------------------------
// AERO STORE & HARDWARE LAB SUPPLY
// ----------------------------------------------------
// Replaced pilot radar with Aero Store hardware & lab supply guidance

// ----------------------------------------------------
// THREE.JS 3D DRONE BACKGROUND CANVAS LOGIC (PRESERVED INTACT)
// ----------------------------------------------------
let animationFrameId = null
let renderer = null
let composer = null
let scene = null
let camera = null
let bloomPass = null
let ambientLight = null
let hemiLight = null
let keyLight = null
let fillLight = null
let cyanRim = null
let orangeRim = null
let stars = null
let droneModel = null
const propellers = []
let lastScrollPos = 0
let scrollSpeed = 0

function applySceneTheme(dark) {
  if (!scene || !ambientLight) return

  if (dark) {
    renderer.setClearColor(0x04060f, 1)
    ambientLight.color.setHex(0xffffff)
    ambientLight.intensity = 2.4
    if (hemiLight) hemiLight.intensity = 0.8
    if (keyLight) {
      keyLight.intensity = 3.2
      keyLight.color.setHex(0xffffff)
    }
    if (fillLight) fillLight.intensity = 1.8
    if (cyanRim) cyanRim.intensity = 4.0
    if (orangeRim) orangeRim.intensity = 3.0
    if (stars) stars.visible = true
    if (bloomPass) {
      bloomPass.enabled = true
      bloomPass.strength = 0.35
    }
  } else {
    renderer.setClearColor(0x000000, 0)
    ambientLight.color.setHex(0xffffff)
    ambientLight.intensity = 2.2
    if (hemiLight) {
      hemiLight.color.setHex(0xffffff)
      hemiLight.groundColor.setHex(0xb0bec5)
      hemiLight.intensity = 2.0
    }
    if (keyLight) {
      keyLight.intensity = 3.2
      keyLight.color.setHex(0xffffff)
    }
    if (fillLight) {
      fillLight.intensity = 1.8
      fillLight.color.setHex(0xdbeafe)
    }
    if (cyanRim) cyanRim.intensity = 2.2
    if (orangeRim) orangeRim.intensity = 2.2
    if (stars) stars.visible = false
    if (bloomPass) {
      bloomPass.enabled = false
    }
  }
}

watch(isDark, (val) => {
  applySceneTheme(val)
})

onMounted(() => {
  if (!canvasRef.value) return

  const canvas = canvasRef.value
  let width = window.innerWidth
  let height = window.innerHeight

  renderer = new THREE.WebGLRenderer({ canvas, antialias: true, alpha: true })
  renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2))
  renderer.setSize(width, height)
  if (THREE.SRGBColorSpace) {
    renderer.outputColorSpace = THREE.SRGBColorSpace
  }
  renderer.shadowMap.enabled = true
  renderer.shadowMap.type = THREE.PCFSoftShadowMap

  scene = new THREE.Scene()
  scene.background = null

  camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 200)
  camera.position.set(0, 0, 8)
  scene.add(camera)

  ambientLight = new THREE.AmbientLight(0xffffff, isDark.value ? 2.4 : 2.2)
  scene.add(ambientLight)

  hemiLight = new THREE.HemisphereLight(0xffffff, 0xb0bec5, isDark.value ? 0.8 : 2.0)
  scene.add(hemiLight)

  keyLight = new THREE.DirectionalLight(0xffffff, isDark.value ? 3.2 : 3.2)
  keyLight.position.set(4, 9, 6)
  keyLight.castShadow = true
  scene.add(keyLight)

  fillLight = new THREE.DirectionalLight(isDark.value ? 0x7da4ff : 0xdbeafe, isDark.value ? 1.8 : 1.8)
  fillLight.position.set(-5, -2, 4)
  scene.add(fillLight)

  cyanRim = new THREE.PointLight(isDark.value ? 0x5df0a8 : 0x0284c7, isDark.value ? 4.0 : 2.2, 18)
  cyanRim.position.set(-3, 2, 3)
  scene.add(cyanRim)

  orangeRim = new THREE.PointLight(0xff6b00, isDark.value ? 3.0 : 2.2, 15)
  orangeRim.position.set(3, -2, -2)
  scene.add(orangeRim)

  const worldGroup = new THREE.Group()
  scene.add(worldGroup)

  const droneGroup = new THREE.Group()
  droneGroup.rotation.order = 'YXZ'
  worldGroup.add(droneGroup)

  const dracoLoader = new DRACOLoader()
  dracoLoader.setDecoderPath('/draco/')
  const gltfLoader = new GLTFLoader()
  gltfLoader.setDRACOLoader(dracoLoader)
  gltfLoader.load(
    '/models/dji_fpv.glb',
    (gltf) => {
      droneModel = gltf.scene

      const toRemove = []
      droneModel.traverse((child) => {
        const name = (child.name || '').toLowerCase()
        if (
          name.includes('pneu') ||
          name.includes('text') ||
          name.includes('wheel') ||
          name.includes('tire')
        ) {
          toRemove.push(child)
        } else if (child.isMesh && child.geometry) {
          if (!child.geometry.boundingBox) child.geometry.computeBoundingBox()
          const b = child.geometry.boundingBox
          if (b && (Math.abs(b.min.x) > 30 || Math.abs(b.max.x) > 30 || Math.abs(b.min.y) > 30 || Math.abs(b.max.y) > 30)) {
            toRemove.push(child)
          }
        }
      })
      toRemove.forEach((node) => {
        if (node.parent) node.parent.remove(node)
      })

      droneModel.rotation.set(0, 0, 0)
      droneModel.updateMatrixWorld(true)

      const box = new THREE.Box3().setFromObject(droneModel)
      const size = box.getSize(new THREE.Vector3())
      const maxDim = Math.max(size.x, size.y, size.z)

      const targetScale = 3.5 / (maxDim || 1)
      droneModel.scale.setScalar(targetScale)
      droneModel.updateMatrixWorld(true)

      const scaledBox = new THREE.Box3().setFromObject(droneModel)
      const center = scaledBox.getCenter(new THREE.Vector3())
      droneModel.position.x = -center.x
      droneModel.position.y = -center.y
      droneModel.position.z = -center.z

      droneModel.traverse((child) => {
        if (child.isMesh) {
          child.castShadow = true
          child.receiveShadow = true
          if (child.material) {
            child.material.roughness = Math.min(Math.max(child.material.roughness ?? 0.5, 0.35), 0.75)
            child.material.metalness = Math.min(child.material.metalness ?? 0.5, 0.35)
            if (child.material.color) {
              if (child.material.color.r < 0.08 && child.material.color.g < 0.08 && child.material.color.b < 0.08) {
                child.material.color.setRGB(0.18, 0.20, 0.24)
              }
            }
            child.material.needsUpdate = true
          }
        }
      })

      let spineNode = null
      droneModel.traverse((c) => {
        if (c.name && c.name.includes('SpineB')) spineNode = c
      })

      propellers.length = 0

      if (spineNode && spineNode.parent) {
        const propConfigs = [
          {
            name: 'Rear-Left',
            center: new THREE.Vector3(-1.9057, -2.1202, 1.1972),
            axis: new THREE.Vector3(0, 0.94604, 0.32404).normalize(),
            dir: -1
          },
          {
            name: 'Front-Left',
            center: new THREE.Vector3(-1.6792, -0.6965, -0.8018),
            axis: new THREE.Vector3(0, 0.94604, 0.32404).normalize(),
            dir: 1
          },
          {
            name: 'Rear-Right',
            center: new THREE.Vector3(1.7483, -2.1202, 1.1972),
            axis: new THREE.Vector3(0, 0.94604, 0.32404).normalize(),
            dir: 1
          },
          {
            name: 'Front-Right',
            center: new THREE.Vector3(1.5432, -0.6965, -0.8018),
            axis: new THREE.Vector3(0, 0.94604, 0.32404).normalize(),
            dir: -1
          }
        ]

        function extractSubGeometry(geom, indices, center) {
          const pos = geom.attributes.position
          const norm = geom.attributes.normal
          const uv = geom.attributes.uv
          const oldToNew = new Map()
          const newPositions = []
          const newNormals = norm ? [] : null
          const newUvs = uv ? [] : null
          const newIndices = []

          for (let i = 0; i < indices.length; i++) {
            const oldIdx = indices[i]
            let newIdx = oldToNew.get(oldIdx)
            if (newIdx === undefined) {
              newIdx = newPositions.length / 3
              oldToNew.set(oldIdx, newIdx)
              newPositions.push(
                pos.getX(oldIdx) - center.x,
                pos.getY(oldIdx) - center.y,
                pos.getZ(oldIdx) - center.z
              )
              if (norm) {
                newNormals.push(norm.getX(oldIdx), norm.getY(oldIdx), norm.getZ(oldIdx))
              }
              if (uv) {
                newUvs.push(uv.getX(oldIdx), uv.getY(oldIdx))
              }
            }
            newIndices.push(newIdx)
          }

          const subGeom = new THREE.BufferGeometry()
          subGeom.setAttribute('position', new THREE.Float32BufferAttribute(newPositions, 3))
          if (norm) subGeom.setAttribute('normal', new THREE.Float32BufferAttribute(newNormals, 3))
          if (uv) subGeom.setAttribute('uv', new THREE.Float32BufferAttribute(newUvs, 2))
          subGeom.setIndex(newIndices)
          subGeom.computeBoundingBox()
          subGeom.computeBoundingSphere()
          return subGeom
        }

        const propGroups = propConfigs.map((cfg) => {
          const grp = new THREE.Group()
          grp.position.copy(cfg.center)
          return grp
        })

        const origMeshes = []
        spineNode.traverse((child) => {
          if (child.isMesh && child.geometry) {
            origMeshes.push(child)
            const geom = child.geometry
            const posAttr = geom.attributes.position
            const indexAttr = geom.index
            if (!posAttr || !indexAttr) return

            const triCount = indexAttr.count / 3
            const triAssignment = []

            for (let t = 0; t < triCount; t++) {
              const i0 = indexAttr.getX(t * 3)
              const i1 = indexAttr.getX(t * 3 + 1)
              const i2 = indexAttr.getX(t * 3 + 2)

              const cx = (posAttr.getX(i0) + posAttr.getX(i1) + posAttr.getX(i2)) / 3
              const cy = (posAttr.getY(i0) + posAttr.getY(i1) + posAttr.getY(i2)) / 3
              const cz = (posAttr.getZ(i0) + posAttr.getZ(i1) + posAttr.getZ(i2)) / 3

              let assigned = -1
              for (let k = 0; k < propConfigs.length; k++) {
                const pc = propConfigs[k].center
                const dx = cx - pc.x
                const dy = cy - pc.y
                const dz = cz - pc.z
                const distSq = dx * dx + dy * dy + dz * dz
                if (distSq < 1.0) {
                  assigned = k
                  break
                }
              }
              triAssignment.push(assigned)
            }

            for (let k = 0; k < propConfigs.length; k++) {
              const subIndices = []
              for (let t = 0; t < triCount; t++) {
                if (triAssignment[t] === k) {
                  subIndices.push(indexAttr.getX(t * 3), indexAttr.getX(t * 3 + 1), indexAttr.getX(t * 3 + 2))
                }
              }

              if (subIndices.length > 0) {
                const subGeom = extractSubGeometry(geom, subIndices, propConfigs[k].center)
                const newMesh = new THREE.Mesh(subGeom, child.material)
                newMesh.castShadow = true
                newMesh.receiveShadow = true
                propGroups[k].add(newMesh)
              }
            }
          }
        })

        origMeshes.forEach((m) => {
          m.visible = false
        })

        propConfigs.forEach((cfg, k) => {
          spineNode.add(propGroups[k])
          propellers.push({
            group: propGroups[k],
            axis: cfg.axis,
            dir: cfg.dir
          })
        })
      }

      droneGroup.add(droneModel)
      loadingProgress.value = 100
    },
    (xhr) => {
      if (xhr.total > 0) {
        loadingProgress.value = Math.min(99, Math.round((xhr.loaded / xhr.total) * 100))
      }
    },
    (err) => {
      console.warn('Drone model load notice:', err)
      loadingProgress.value = 100
    }
  )

  const starGeo = new THREE.BufferGeometry()
  const starPos = []
  for (let i = 0; i < 1400; i++) {
    const u = Math.random()
    const v = Math.random()
    const theta = u * 2.0 * Math.PI
    const phi = Math.acos(2.0 * v - 1.0)
    const r = 85.0
    starPos.push(r * Math.sin(phi) * Math.cos(theta), r * Math.sin(phi) * Math.sin(theta), r * Math.cos(phi))
  }
  starGeo.setAttribute('position', new THREE.Float32BufferAttribute(starPos, 3))
  const starMat = new THREE.PointsMaterial({ color: 0xcfe0ff, size: 1.6, transparent: true, opacity: 0.75 })
  stars = new THREE.Points(starGeo, starMat)
  stars.visible = isDark.value
  scene.add(stars)

  composer = new EffectComposer(renderer)
  composer.addPass(new RenderPass(scene, camera))
  bloomPass = new UnrealBloomPass(new THREE.Vector2(width, height), 0.35, 0.4, 0.1)
  bloomPass.enabled = isDark.value
  composer.addPass(bloomPass)
  composer.addPass(new ShaderPass(GammaCorrectionShader))

  const DEG90 = Math.PI * 0.5

  // HARMONIC FLUID FLIGHT PATH:
  // Stage 1 (Hero): Center hover under AERO FLY title
  // Stage 2 (Weekend Flights): Left hover facing elevated cards
  // Stage 3 (Middle Anthem): Drone promptly & smoothly sweeps up into upper center (y = 1.15) comfortably ABOVE FLY AS ONE text
  // Stage 4 (Perks): Right hover facing perks without cut-off
  // Stage 5 (Aero Store): Center hover above store supply
  const STOPS_X = [
    { p: 0.00, v: 0.0 },    // 1. Hero: Center
    { p: 0.09, v: -2.25 },  // 2. Section 2: Smooth glide to Left
    { p: 0.16, v: -2.25 },  // Section 2 hold
    { p: 0.23, v: 0.0 },    // Sweep into Center
    { p: 0.38, v: 0.0 },    // Middle Stop 1: Center hold cleanly ABOVE FLY AS ONE
    { p: 0.45, v: 2.25 },   // Section 4: Smooth sweep to Right opposite perks
    { p: 0.58, v: 2.25 },   // Section 4 hold
    { p: 0.65, v: 0.0 },    // Middle Stop 2: Rotate and sweep into Center!
    { p: 0.77, v: 0.0 },    // Middle Stop 2 hold: Center above BUILT TO SOAR
    { p: 0.83, v: 0.0 },    // Ascends into sky BEFORE Aero Store
    { p: 0.88, v: 0.0 },    // Fully exited above screen ceiling
    { p: 1.00, v: 0.0 }
  ]

  const STOPS_Y = [
    { p: 0.00, v: -0.35 },  // Hero: comfortably below top title
    { p: 0.09, v: 0.25 },   // Section 2: level with upper cards
    { p: 0.16, v: 0.25 },   // Section 2 hold
    { p: 0.23, v: 1.15 },   // Elevated HIGH in upper frame above FLY AS ONE
    { p: 0.38, v: 1.15 },   // Middle Stop 1 hold
    { p: 0.45, v: 0.20 },   // Section 4: level with upper perks cards
    { p: 0.58, v: 0.20 },   // Section 4 hold
    { p: 0.65, v: 1.15 },   // Middle Stop 2: Elevated in upper frame above BUILT TO SOAR
    { p: 0.77, v: 1.15 },   // Middle Stop 2 hold
    { p: 0.83, v: 3.50 },   // Smooth rapid ascent into sky BEFORE Aero Store (ceiling is 2.91)
    { p: 0.88, v: 7.00 },   // Completely exited above viewport ceiling!
    { p: 1.00, v: 7.00 }
  ]

  const STOPS_S = [
    { p: 0.00, v: 1.20 },
    { p: 0.09, v: 1.00 },
    { p: 0.16, v: 1.00 },
    { p: 0.23, v: 1.05 },   // Middle Stop 1
    { p: 0.38, v: 1.05 },
    { p: 0.45, v: 1.00 },
    { p: 0.58, v: 1.00 },
    { p: 0.65, v: 1.05 },   // Middle Stop 2: Prominent showcase
    { p: 0.77, v: 1.05 },
    { p: 0.83, v: 0.45 },   // Recedes into distance as it climbs
    { p: 0.88, v: 0.05 },   // Exits
    { p: 1.00, v: 0.05 }
  ]

  const STOPS_ROLL = [
    { p: 0.00, v: 0.0 },
    { p: 0.09, v: 0.0 },
    { p: 0.16, v: 0.0 },
    { p: 0.23, v: 0.0 },
    { p: 0.38, v: 0.0 },
    { p: 0.45, v: 0.0 },
    { p: 0.58, v: 0.0 },
    { p: 0.65, v: 0.0 },
    { p: 0.77, v: 0.0 },
    { p: 0.83, v: 0.0 },
    { p: 0.88, v: 0.0 },
    { p: 1.00, v: 0.0 }
  ]

  const STOPS_PITCH = [
    { p: 0.00, v: 0.22 },  // Natural forward flight tilt facing user
    { p: 0.09, v: 0.08 },  // Slight hover tilt pointing at cards
    { p: 0.16, v: 0.08 },
    { p: 0.23, v: 0.22 },  // Forward flight tilt facing user above text 1
    { p: 0.38, v: 0.22 },
    { p: 0.45, v: 0.08 },  // Slight hover tilt pointing at perks
    { p: 0.58, v: 0.08 },
    { p: 0.65, v: 0.22 },  // Forward flight tilt facing user above text 2
    { p: 0.77, v: 0.22 },
    { p: 0.83, v: -0.28 }, // Tilts up as it climbs into the sky!
    { p: 0.88, v: -0.38 }, // Climbing angle
    { p: 1.00, v: -0.38 }
  ]

  const STOPS_YAW = [
    { p: 0.00, v: 0.0 },     // 1. Hero: Facing forward
    { p: 0.09, v: DEG90 },   // 2. Left: Rotates 90° right to point directly at cards
    { p: 0.16, v: DEG90 },   // Section 2 hold
    { p: 0.23, v: 0.0 },     // Rotates to 0° facing forward into center
    { p: 0.38, v: 0.0 },     // Middle Stop 1 hold: Facing forward
    { p: 0.45, v: -DEG90 },  // Rotates 90° left to point at perks
    { p: 0.58, v: -DEG90 },  // Section 4 hold
    { p: 0.65, v: 0.0 },     // ROTATES TO 0° FACING FORWARD INTO CENTER!
    { p: 0.77, v: 0.0 },     // Middle Stop 2 hold: Facing forward
    { p: 0.83, v: 0.0 },     // Exits into sky
    { p: 0.88, v: 0.0 },
    { p: 1.00, v: 0.0 }
  ]

  // Responsive Drone Scaling: Big on large desktop/4K monitors, scaled down to fit on laptops, tablets, and phones
  function getResponsiveDroneScale() {
    const w = window.innerWidth
    const h = window.innerHeight

    let factor = 1.0
    if (w >= 2200) {
      // 2K / 4K / Ultrawide displays: prominent, big, grand drone
      factor = 1.25 + Math.min(0.20, (w - 2200) / 2000)
    } else if (w >= 1600) {
      // Large 1080p+ desktop monitors: bigger drone
      factor = 1.10 + ((w - 1600) / 600) * 0.15
    } else if (w >= 1200) {
      // Standard desktop displays
      factor = 1.00 + ((w - 1200) / 400) * 0.10
    } else if (w >= 992) {
      // Laptops & small desktops
      factor = 0.85 + ((w - 992) / 208) * 0.15
    } else if (w >= 640) {
      // Tablets: scaled down to fit neatly
      factor = 0.65 + ((w - 640) / 352) * 0.15
    } else {
      // Mobile screens (< 640px): sleek mobile app size that fits portrait viewports cleanly
      factor = Math.max(0.36, 0.38 + ((w - 320) / 320) * 0.12)
    }

    // Viewport height guard: slightly scale down on short laptop/landscape heights
    if (h < 750) {
      const hRatio = Math.max(0.70, h / 750)
      factor *= hRatio
    }

    return factor
  }

  function sample(stops, p) {
    if (p <= stops[0].p) return stops[0].v
    if (p >= stops[stops.length - 1].p) return stops[stops.length - 1].v
    for (let i = 0; i < stops.length - 1; i++) {
      if (p >= stops[i].p && p <= stops[i + 1].p) {
        const t = (p - stops[i].p) / (stops[i + 1].p - stops[i].p)
        const st = t * t * (3 - 2 * t)
        return stops[i].v + (stops[i + 1].v - stops[i].v) * st
      }
    }
    return stops[0].v
  }

  let curP = 0
  let curX = STOPS_X[0].v
  let curY = STOPS_Y[0].v
  let curS = STOPS_S[0].v * getResponsiveDroneScale()
  let curRoll = STOPS_ROLL[0].v
  let curPitch = STOPS_PITCH[0].v
  let curYaw = STOPS_YAW[0].v
  let lastTime = performance.now()

  applySceneTheme(isDark.value)

  lastScrollPos = window.pageYOffset || document.documentElement.scrollTop
  scrollSpeed = 0

  function onScroll() {
    const curScroll = window.pageYOffset || document.documentElement.scrollTop
    const delta = Math.abs(curScroll - lastScrollPos)
    lastScrollPos = curScroll
    scrollSpeed = Math.max(scrollSpeed, Math.min(delta * 0.95, 55.0))
  }

  window.addEventListener('scroll', onScroll, { passive: true })

  function animate() {
    animationFrameId = requestAnimationFrame(animate)
    const now = performance.now()
    const dt = Math.min((now - lastTime) / 1000, 0.05)
    lastTime = now

    const maxScroll = Math.max(document.documentElement.scrollHeight - window.innerHeight, 1)
    const scrollY = window.pageYOffset || document.documentElement.scrollTop
    const pTarget = Math.max(0, Math.min(1, scrollY / maxScroll))
    curP += (pTarget - curP) * Math.min(1, dt * 5.0)

    const isMobile = window.innerWidth < 1024

    // On desktop, the drone sweeps between the left and right 5-column airspaces.
    // On mobile portrait, the screen is single-column, so the drone hovers gracefully
    // in the central aerial channel with a gentle, natural aerodynamic sway (no screen-edge cut-off).
    const targetX = isMobile
      ? sample(STOPS_X, curP) * 0.10
      : sample(STOPS_X, curP) * Math.min(1.05, Math.max(0.85, window.innerWidth / 1600))

    // On mobile, elevate the drone slightly in content sections so it hovers in clear airspace above cards
    const mobileYOffset = isMobile && (curP < 0.20 || (curP > 0.42 && curP < 0.60)) ? 0.35 : 0.0
    const targetY = sample(STOPS_Y, curP) + mobileYOffset

    const baseS = sample(STOPS_S, curP)
    const targetS = baseS * getResponsiveDroneScale()
    const targetRoll = isMobile
      ? sample(STOPS_X, curP) * -0.04
      : sample(STOPS_ROLL, curP)
    const targetPitch = sample(STOPS_PITCH, curP)

    // On desktop, drone turns 90° to face side cards. On mobile, drone faces forward with subtle dynamic banking.
    const targetYaw = isMobile
      ? sample(STOPS_YAW, curP) * 0.25
      : sample(STOPS_YAW, curP)

    const k = Math.min(1, dt * 4.5)
    curX += (targetX - curX) * k
    curY += (targetY - curY) * k
    curS += (targetS - curS) * k
    curRoll += (targetRoll - curRoll) * k
    curPitch += (targetPitch - curPitch) * k
    curYaw += (targetYaw - curYaw) * k

    // Middle text sliding reveal for Middle Stop 1: FLY AS ONE
    if (curP < 0.19) {
      middleTextState.value = 'before'
    } else if (curP > 0.40) {
      middleTextState.value = 'after'
    } else {
      middleTextState.value = 'active'
    }

    // Middle text sliding reveal for Middle Stop 2: BUILT TO SOAR
    if (curP < 0.60) {
      middleTextTwoState.value = 'before'
    } else if (curP > 0.79) {
      middleTextTwoState.value = 'after'
    } else {
      middleTextTwoState.value = 'active'
    }

    // Dynamic Footer Clearance: Ensure drone NEVER flies into or touches footer navigation
    const targetFooter = footerRef.value || document.querySelector('footer')
    let footerExitProgress = 0
    if (targetFooter) {
      const footerRect = targetFooter.getBoundingClientRect()
      // When footer approaches within 350px of entering viewport:
      const approachDistance = 350
      const distFromBottom = footerRect.top - window.innerHeight
      if (distFromBottom < approachDistance) {
        footerExitProgress = Math.min(1, Math.max(0, (approachDistance - distFromBottom) / approachDistance))
      }
    }

    const dynExitY = footerExitProgress * 5.0
    const dynExitPitch = -footerExitProgress * 0.40
    const dynExitScale = Math.max(0.01, 1 - footerExitProgress * 0.6)

    const hoverBob = Math.sin(now * 0.0018) * 0.05
    worldGroup.position.set(curX, curY + hoverBob + dynExitY, 0)
    worldGroup.scale.setScalar(curS * dynExitScale)

    scrollSpeed *= Math.pow(0.04, dt)
    if (scrollSpeed < 0.04) scrollSpeed = 0

    // Smooth idle propeller spin, revving faster while actively scrolling
    const propSpinSpeed = 10.0 + scrollSpeed * 2.5
    propellers.forEach((p) => {
      p.group.rotateOnAxis(p.axis, propSpinSpeed * dt * p.dir)
    })

    droneGroup.rotation.y = curYaw
    droneGroup.rotation.x = curPitch + dynExitPitch
    droneGroup.rotation.z = curRoll

    // Drone CANNOT fly into footer navigation under any circumstance:
    // When the footer enters near the viewport or scroll reaches the footer zone, hide the drone completely!
    const isAtFooter = footerExitProgress >= 0.65 || curP >= 0.89
    worldGroup.visible = !isAtFooter

    if (!isDark.value) {
      renderer.render(scene, camera)
    } else {
      composer.render()
    }
  }

  animate()

  function handleResize() {
    width = window.innerWidth
    height = window.innerHeight
    camera.aspect = width / height
    camera.updateProjectionMatrix()
    renderer.setSize(width, height)
    composer.setSize(width, height)
  }

  window.addEventListener('resize', handleResize)

  onUnmounted(() => {
    window.removeEventListener('scroll', onScroll)
    window.removeEventListener('resize', handleResize)
    if (animationFrameId) cancelAnimationFrame(animationFrameId)
    if (renderer) renderer.dispose()
  })
})
</script>

<style scoped>
.aero-fly-root {
  min-height: 100vh;
}
</style>
