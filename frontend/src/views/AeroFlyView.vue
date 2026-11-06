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
      <span>SYS // LOADING DRONE 3D · {{ loadingProgress }}%</span>
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
      <section class="h-[calc(100vh-64px)] min-h-[580px] flex flex-col items-center justify-between text-center px-4 sm:px-6 pt-8 sm:pt-12 pb-8 relative select-none">
        <!-- TOP AREA: TWO TEXT LINES DIRECTLY ABOVE THE DRONE -->
        <div class="max-w-4xl mx-auto space-y-2.5 sm:space-y-3.5 pt-2 sm:pt-4">
          <!-- LINE 1: BOLD GEOMETRIC TITLE -->
          <h1 class="text-5xl sm:text-7xl md:text-8xl lg:text-9xl font-black tracking-[0.14em] sm:tracking-[0.18em] uppercase text-[#0c1e5b] dark:text-white drop-shadow-sm font-sans transition-colors">
            AERO FLY
          </h1>

          <!-- LINE 2: UPPERCASE SUBTITLE WITH SUBTLE RED DOT ACCENTS -->
          <div class="relative inline-block">
            <p class="text-xs sm:text-sm md:text-base font-bold tracking-[0.24em] sm:tracking-[0.32em] uppercase text-slate-700 dark:text-white/90">
              THE OPEN DRONE FLIGHT COMMUNITY FOR CAMBODIA.
            </p>
            <!-- Minimal Red Dot Accents from reference image -->
            <div class="mt-2.5 flex items-center justify-center gap-1.5 opacity-80">
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
          class="flex flex-col items-center gap-1.5 opacity-40 hover:opacity-100 transition-opacity text-[10px] font-mono tracking-widest uppercase text-slate-400 dark:text-slate-500 cursor-pointer"
        >
          <span>SCROLL</span>
          <span class="animate-bounce">↓</span>
        </a>
      </section>

      <!-- SECTION 2: GATHERINGS (Drone flies to LEFT, Text on RIGHT) -->
      <section id="sessions" class="pt-6 sm:pt-10 pb-16 px-4 sm:px-6 lg:px-8 max-w-[1240px] mx-auto">
        <div class="w-full grid lg:grid-cols-12 gap-8 lg:gap-12 items-center">
          <!-- Left 5 cols: Completely clear open air for 3D drone flying on the left -->
          <div class="hidden lg:block lg:col-span-5 pointer-events-none"></div>

          <!-- Right 7 cols: Content & Text on the right -->
          <div class="lg:col-span-7 space-y-5">
            <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-white/10">
              <div>
                <div class="text-[10px] font-mono tracking-widest uppercase text-slate-400 dark:text-slate-500">01 // SESSIONS</div>
                <h2 class="text-2xl sm:text-3xl font-black text-[#0c1e5b] dark:text-white">Weekend Flights</h2>
              </div>
              <span class="text-[11px] font-mono text-emerald-600 dark:text-[#5df0a8] font-bold">
                ● SKY CLEAR · 8 KM/H
              </span>
            </div>

            <!-- Minimal Stats Line -->
            <div class="flex items-center gap-6 text-xs font-mono text-slate-500 dark:text-slate-400 py-1">
              <span><strong>140+</strong> Pilots</span>
              <span><strong>5.8 GHz</strong> Band</span>
              <span><strong>Weekly</strong> Gatherings</span>
            </div>

            <!-- Ultra-Short Sessions List -->
            <div class="space-y-3">
              <div
                v-for="session in flightSessions"
                :key="session.id"
                class="p-4 rounded-2xl bg-white/80 dark:bg-white/[0.04] border border-slate-200 dark:border-white/10 backdrop-blur-xl flex items-center justify-between gap-4 hover:border-slate-400 dark:hover:border-white/20 transition duration-150"
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

                <div class="flex items-center gap-3 shrink-0">
                  <span class="text-[11px] font-mono text-slate-400 hidden sm:inline">
                    {{ session.attendees.length }} attending
                  </span>
                  <button
                    type="button"
                    @click="toggleRSVP(session)"
                    class="px-3.5 py-1.5 rounded-full text-xs font-bold transition cursor-pointer"
                    :class="session.isJoined
                      ? 'bg-emerald-500 text-white'
                      : 'bg-slate-100 dark:bg-white/10 hover:bg-slate-200 dark:hover:bg-white/20 text-[#0c1e5b] dark:text-white'"
                  >
                    {{ session.isJoined ? '✓ Joined' : 'RSVP' }}
                  </button>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- SECTION: THE MIDDLE STOP (Drone in Middle, Text Elevated Under Drone with Masked Sliding Reveal) -->
      <section id="middle" class="h-[120vh] relative">
        <div class="sticky top-0 h-screen w-full flex flex-col items-center justify-start px-4 pt-[46vh] sm:pt-[48vh] overflow-hidden pointer-events-none select-none">
          <!-- TWO TEXT LINES CLEANLY UNDER THE DRONE (Elevated into upper UX/UI frame, NOT sunken down below!) -->
          <div class="max-w-4xl mx-auto text-center space-y-2 sm:space-y-3 relative z-10 pointer-events-auto">
            <!-- LINE 1: BOLD GEOMETRIC TITLE (Masked Sliding Reveal) -->
            <div class="overflow-hidden py-1 inline-block">
              <h2
                class="text-4xl sm:text-6xl md:text-7xl lg:text-8xl font-black tracking-[0.14em] sm:tracking-[0.18em] uppercase text-[#0c1e5b] dark:text-white drop-shadow-sm font-sans transition-all duration-700 ease-[cubic-bezier(0.16,1,0.3,1)] transform"
                :class="{
                  'translate-y-0 opacity-100': middleTextState === 'active',
                  'translate-y-[120%] opacity-0': middleTextState === 'before',
                  '-translate-y-[120%] opacity-0': middleTextState === 'after'
                }"
              >
                FLY AS ONE
              </h2>
            </div>

            <!-- LINE 2: UPPERCASE SUBTITLE (Masked Sliding Reveal with Stagger) -->
            <div class="block">
              <div class="overflow-hidden py-1 inline-block">
                <p
                  class="text-xs sm:text-sm md:text-base font-bold tracking-[0.24em] sm:tracking-[0.32em] uppercase text-slate-700 dark:text-white/90 transition-all duration-700 delay-100 ease-[cubic-bezier(0.16,1,0.3,1)] transform"
                  :class="{
                    'translate-y-0 opacity-100': middleTextState === 'active',
                    'translate-y-[120%] opacity-0': middleTextState === 'before',
                    '-translate-y-[120%] opacity-0': middleTextState === 'after'
                  }"
                >
                  FROM FIRST HOVER TO PRO FREESTYLE &amp; CINEMATIC MISSIONS.
                </p>
              </div>

              <!-- Minimal Red Dot Accents -->
              <div
                class="mt-2.5 flex items-center justify-center gap-1.5 transition-all duration-500 delay-200 ease-out transform"
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

      <section id="benefits" class="pt-6 sm:pt-10 pb-16 px-4 sm:px-6 lg:px-8 max-w-[1240px] mx-auto">
        <div class="w-full grid lg:grid-cols-12 gap-8 lg:gap-12 items-center">
          <!-- Left 7 cols: Content & Text on the left -->
          <div class="lg:col-span-7 space-y-5">
            <div class="flex flex-col sm:flex-row sm:items-end justify-between gap-2 pb-3 border-b border-slate-200 dark:border-white/10">
              <div>
                <div class="text-[10px] font-mono tracking-widest uppercase text-slate-400 dark:text-slate-500">02 // MEMBERSHIP BENEFITS</div>
                <h2 class="text-2xl sm:text-3xl font-black text-[#0c1e5b] dark:text-white">What You Get When You Join</h2>
              </div>
              <span class="text-[11px] font-mono text-emerald-600 dark:text-[#5df0a8] font-bold">
                ● 100% FREE COMMUNITY
              </span>
            </div>

            <p class="text-xs text-slate-600 dark:text-[#9aa6c4]">
              Join Cambodia's open FPV collective. Everything you need to build, tune, and fly safely with active pilots.
            </p>

            <!-- 6 Key Member Benefits Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <!-- Benefit 1 -->
              <div class="p-3.5 rounded-2xl bg-white/80 dark:bg-white/[0.04] border border-slate-200 dark:border-white/10 backdrop-blur-xl flex items-start gap-3 hover:border-slate-400 dark:hover:border-white/20 transition">
                <div class="w-8 h-8 rounded-xl bg-blue-500/10 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0 text-sm">
                  🛠️
                </div>
                <div class="space-y-0.5">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">Free Ta Khmau Bench Lab</h4>
                  <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-snug">
                    Open soldering stations, smoke stoppers, Betaflight 4.5 tuning, and multimeter diagnostics.
                  </p>
                </div>
              </div>

              <!-- Benefit 2 -->
              <div class="p-3.5 rounded-2xl bg-white/80 dark:bg-white/[0.04] border border-slate-200 dark:border-white/10 backdrop-blur-xl flex items-start gap-3 hover:border-slate-400 dark:hover:border-white/20 transition">
                <div class="w-8 h-8 rounded-xl bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0 text-sm">
                  📍
                </div>
                <div class="space-y-0.5">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">Curated Flying Spots</h4>
                  <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-snug">
                    Tested legal locations across Phnom Penh (Koh Pich, OCIC, Chroy Changvar) with active spotters.
                  </p>
                </div>
              </div>

              <!-- Benefit 3 -->
              <div class="p-3.5 rounded-2xl bg-white/80 dark:bg-white/[0.04] border border-slate-200 dark:border-white/10 backdrop-blur-xl flex items-start gap-3 hover:border-slate-400 dark:hover:border-white/20 transition">
                <div class="w-8 h-8 rounded-xl bg-amber-500/10 text-amber-600 dark:text-amber-400 flex items-center justify-center shrink-0 text-sm">
                  📡
                </div>
                <div class="space-y-0.5">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">Coordinated VTX Spectrum</h4>
                  <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-snug">
                    Zero video stomping. Coordinated Raceband 5.8 GHz & HD channels so nobody crashes your feed.
                  </p>
                </div>
              </div>

              <!-- Benefit 4 -->
              <div class="p-3.5 rounded-2xl bg-white/80 dark:bg-white/[0.04] border border-slate-200 dark:border-white/10 backdrop-blur-xl flex items-start gap-3 hover:border-slate-400 dark:hover:border-white/20 transition">
                <div class="w-8 h-8 rounded-xl bg-purple-500/10 text-purple-600 dark:text-purple-400 flex items-center justify-center shrink-0 text-sm">
                  🖨️
                </div>
                <div class="space-y-0.5">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">TPU 3D Print Priority</h4>
                  <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-snug">
                    Member discounts on custom GoPro mounts, motor arm skids, antenna mounts, and bumpers.
                  </p>
                </div>
              </div>

              <!-- Benefit 5 -->
              <div class="p-3.5 rounded-2xl bg-white/80 dark:bg-white/[0.04] border border-slate-200 dark:border-white/10 backdrop-blur-xl flex items-start gap-3 hover:border-slate-400 dark:hover:border-white/20 transition">
                <div class="w-8 h-8 rounded-xl bg-cyan-500/10 text-cyan-600 dark:text-cyan-400 flex items-center justify-center shrink-0 text-sm">
                  🤝
                </div>
                <div class="space-y-0.5">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">Maiden Flight Mentorship</h4>
                  <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-snug">
                    Senior pilots personally guide your first flight, failsafe setup, and emergency safety disarms.
                  </p>
                </div>
              </div>

              <!-- Benefit 6 -->
              <div class="p-3.5 rounded-2xl bg-white/80 dark:bg-white/[0.04] border border-slate-200 dark:border-white/10 backdrop-blur-xl flex items-start gap-3 hover:border-slate-400 dark:hover:border-white/20 transition">
                <div class="w-8 h-8 rounded-xl bg-rose-500/10 text-rose-600 dark:text-rose-400 flex items-center justify-center shrink-0 text-sm">
                  ⚡
                </div>
                <div class="space-y-0.5">
                  <h4 class="text-xs font-bold text-[#0c1e5b] dark:text-white">Field Spares & Repairs</h4>
                  <p class="text-[11px] text-slate-500 dark:text-slate-400 leading-snug">
                    Shared field toolkit with spare props, M3 hardware, parallel LiPo charging, and quick solder fixes.
                  </p>
                </div>
              </div>
            </div>

            <!-- Bottom action banner -->
            <div class="pt-2 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
              <span class="text-[11px] text-slate-400 dark:text-slate-500 font-mono">
                Open to Tiny Whoop, 3.5" cinewhoop, 5" freestyle & long-range.
              </span>
              <a
                href="https://t.me/aerobyteacademy"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center justify-center gap-1.5 px-4 py-2 rounded-full text-xs font-bold bg-[#0c1e5b] dark:bg-white text-white dark:text-[#0c1e5b] hover:opacity-90 transition cursor-pointer shrink-0"
              >
                <span>Join Telegram Hub</span>
                <span>↗</span>
              </a>
            </div>
          </div>

          <!-- Right 5 cols: Completely clear open air for 3D drone flying on the right -->
          <div class="hidden lg:block lg:col-span-5 pointer-events-none"></div>
        </div>
      </section>

      <!-- SECTION 5: PILOT RADAR & WORKSHOP HUB (Drone stops in the MIDDLE, Text Below) -->
      <section id="buddy-board" class="pt-6 sm:pt-10 pb-16 px-4 sm:px-6 lg:px-8 max-w-[1240px] mx-auto">
        <!-- Generous space above so the 3D drone hovers freely in the center -->
        <div class="flex-1 min-h-[30vh] pointer-events-none"></div>

        <div class="w-full space-y-8 relative z-10">
          <!-- Active Pilot Callouts -->
          <div class="space-y-4">
            <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-white/10">
              <div>
                <div class="text-[10px] font-mono tracking-widest uppercase text-slate-400 dark:text-slate-500">03 // PILOT RADAR</div>
                <h2 class="text-2xl sm:text-3xl font-black text-[#0c1e5b] dark:text-white">Active Flight Callouts</h2>
              </div>
              <button
                type="button"
                @click="showCalloutModal = true"
                class="px-3.5 py-1.5 rounded-full text-xs font-bold bg-[#0c1e5b] dark:bg-white text-white dark:text-[#0c1e5b] hover:opacity-90 transition cursor-pointer"
              >
                + Post Callout
              </button>
            </div>

            <!-- Filter pills -->
            <div class="flex flex-wrap items-center gap-1.5">
              <button
                v-for="filter in ['All Callouts', 'Looking for Spotter', 'Beginners Welcome', 'Freestyle & Gaps', 'Ta Khmau Lab']"
                :key="filter"
                type="button"
                @click="activeFilter = filter"
                class="px-3 py-1 rounded-full text-[11px] font-medium transition cursor-pointer"
                :class="activeFilter === filter
                  ? 'bg-[#0c1e5b] dark:bg-white text-white dark:text-[#0c1e5b]'
                  : 'bg-slate-100 dark:bg-white/5 text-slate-600 dark:text-slate-400 hover:bg-slate-200 dark:hover:bg-white/10'"
              >
                {{ filter }}
              </button>
            </div>

            <!-- Short Callout Cards Grid -->
            <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-3">
              <div
                v-for="post in filteredPosts"
                :key="post.id"
                class="p-3.5 rounded-2xl bg-white/80 dark:bg-white/[0.04] border border-slate-200 dark:border-white/10 backdrop-blur-xl flex flex-col justify-between gap-3"
              >
                <div class="space-y-1">
                  <div class="flex items-center justify-between text-[10px] font-mono text-slate-400">
                    <span class="font-bold text-[#0c1e5b] dark:text-white">{{ post.author }}</span>
                    <span>{{ post.spot }}</span>
                  </div>
                  <p class="text-xs text-slate-600 dark:text-slate-300">
                    "{{ post.message }}"
                  </p>
                </div>

                <div class="flex items-center justify-between pt-1 text-[11px] font-mono border-t border-slate-100 dark:border-white/5">
                  <span class="text-slate-400">{{ post.droneSetup }}</span>
                  <a
                    :href="post.telegramLink || 'https://t.me/aerobyteacademy'"
                    target="_blank"
                    rel="noopener noreferrer"
                    class="font-bold text-sky-600 dark:text-cyan-400 hover:underline"
                  >
                    Reply →
                  </a>
                </div>
              </div>
            </div>
          </div>

          <!-- Bottom Row: Community & Workshop Hub -->
          <div class="grid sm:grid-cols-2 gap-3.5 pt-4 border-t border-slate-200 dark:border-white/10">
            <!-- Telegram -->
            <div class="p-5 rounded-2xl bg-white/80 dark:bg-white/[0.04] border border-slate-200 dark:border-white/10 backdrop-blur-xl flex flex-col justify-between">
              <div class="space-y-1.5">
                <div class="text-lg">💬</div>
                <h3 class="text-sm font-bold text-[#0c1e5b] dark:text-white">Telegram Pilot Hub</h3>
                <p class="text-xs text-slate-500 dark:text-slate-400">
                  Weekend weather polls, frequency reservations, and flight pins.
                </p>
              </div>
              <div class="pt-3">
                <a
                  href="https://t.me/aerobyteacademy"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="text-xs font-bold text-[#0c1e5b] dark:text-white hover:underline"
                >
                  t.me/aerobyteacademy ↗
                </a>
              </div>
            </div>

            <!-- Ta Khmau Lab -->
            <div class="p-5 rounded-2xl bg-white/80 dark:bg-white/[0.04] border border-slate-200 dark:border-white/10 backdrop-blur-xl flex flex-col justify-between">
              <div class="space-y-1.5">
                <div class="text-lg">📍</div>
                <h3 class="text-sm font-bold text-[#0c1e5b] dark:text-white">Ta Khmau Flight Lab</h3>
                <p class="text-xs text-slate-500 dark:text-slate-400">
                  Free open bench: Soldering, Betaflight 4.5 tuning, and Maiden tests.
                </p>
              </div>
              <div class="pt-3">
                <a
                  href="https://maps.google.com/?q=Ta+Khmau+Cambodia"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="text-xs font-bold text-[#0c1e5b] dark:text-white hover:underline"
                >
                  Directions ↗
                </a>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- MINIMALIST FOOTER -->
      <footer class="py-12 px-4 sm:px-6 text-center border-t border-slate-200 dark:border-white/10 max-w-[1240px] mx-auto flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500 dark:text-slate-500 font-mono gap-4">
        <div>© {{ currentYear }} AERO FLY // CAMBODIA DRONE COLLECTIVE</div>
        <div class="flex items-center gap-6">
          <a href="https://t.me/aerobyteacademy" target="_blank" rel="noopener noreferrer" class="hover:text-slate-800 dark:hover:text-white transition">Telegram</a>
          <a href="#sessions" class="hover:text-slate-800 dark:hover:text-white transition">Sessions</a>
          <a href="#buddy-board" class="hover:text-slate-800 dark:hover:text-white transition">Radar</a>
        </div>
      </footer>
    </div>

    <!-- MODAL 1: POST A FLIGHT CALLOUT -->
    <div
      v-if="showCalloutModal"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-md"
      @click.self="showCalloutModal = false"
    >
      <div class="w-full max-w-md p-6 rounded-2xl bg-white dark:bg-[#0c142c] border border-slate-200 dark:border-white/10 shadow-2xl text-left space-y-4 animate-in fade-in zoom-in-95 duration-200">
        <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-white/10">
          <div>
            <h3 class="text-base font-bold text-[#0c1e5b] dark:text-white font-mono">POST // FLIGHT NOTICE</h3>
            <p class="text-xs text-slate-500 dark:text-slate-400">Invite pilots or request a spotter.</p>
          </div>
          <button
            type="button"
            @click="showCalloutModal = false"
            class="w-7 h-7 rounded-full bg-slate-100 dark:bg-white/10 text-slate-500 dark:text-white flex items-center justify-center hover:bg-slate-200 dark:hover:bg-white/20 transition cursor-pointer text-xs"
          >
            ✕
          </button>
        </div>

        <form @submit.prevent="submitCallout" class="space-y-3 text-xs">
          <div>
            <label class="block font-medium text-slate-700 dark:text-slate-300 mb-1">Callsign / Name</label>
            <input
              v-model="newCallout.author"
              required
              placeholder="e.g. Dara_FPV"
              class="w-full px-3 py-2 rounded-xl bg-slate-50 dark:bg-black/30 border border-slate-300 dark:border-white/10 text-slate-800 dark:text-white outline-none"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-medium text-slate-700 dark:text-slate-300 mb-1">Category</label>
              <select
                v-model="newCallout.category"
                class="w-full px-3 py-2 rounded-xl bg-slate-50 dark:bg-[#121c3d] border border-slate-300 dark:border-white/10 text-slate-800 dark:text-white outline-none"
              >
                <option value="Looking for Spotter">Looking for Spotter</option>
                <option value="Weekend Fly-In">Weekend Fly-In</option>
                <option value="Beginners Welcome">Beginners Welcome</option>
                <option value="Freestyle & Gaps">Freestyle & Gaps</option>
                <option value="Ta Khmau Lab">Ta Khmau Lab</option>
              </select>
            </div>
            <div>
              <label class="block font-medium text-slate-700 dark:text-slate-300 mb-1">Drone Setup</label>
              <input
                v-model="newCallout.droneSetup"
                required
                placeholder="e.g. 5-inch 6S"
                class="w-full px-3 py-2 rounded-xl bg-slate-50 dark:bg-black/30 border border-slate-300 dark:border-white/10 text-slate-800 dark:text-white outline-none"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-medium text-slate-700 dark:text-slate-300 mb-1">Spot</label>
              <input
                v-model="newCallout.spot"
                required
                placeholder="e.g. Chroy Changvar"
                class="w-full px-3 py-2 rounded-xl bg-slate-50 dark:bg-black/30 border border-slate-300 dark:border-white/10 text-slate-800 dark:text-white outline-none"
              />
            </div>
            <div>
              <label class="block font-medium text-slate-700 dark:text-slate-300 mb-1">Date & Time</label>
              <input
                v-model="newCallout.dateTime"
                required
                placeholder="e.g. Sunday 6:30 AM"
                class="w-full px-3 py-2 rounded-xl bg-slate-50 dark:bg-black/30 border border-slate-300 dark:border-white/10 text-slate-800 dark:text-white outline-none"
              />
            </div>
          </div>

          <div>
            <label class="block font-medium text-slate-700 dark:text-slate-300 mb-1">Message</label>
            <textarea
              v-model="newCallout.message"
              required
              rows="2"
              placeholder="Short note about what you're flying or what you need..."
              class="w-full px-3 py-2 rounded-xl bg-slate-50 dark:bg-black/30 border border-slate-300 dark:border-white/10 text-slate-800 dark:text-white outline-none resize-none"
            ></textarea>
          </div>

          <div class="pt-2 flex items-center justify-end gap-2">
            <button
              type="button"
              @click="showCalloutModal = false"
              class="px-4 py-2 rounded-full text-slate-600 dark:text-slate-300 font-medium cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-5 py-2 rounded-full font-bold bg-[#0c1e5b] dark:bg-white text-white dark:text-[#0c1e5b] cursor-pointer"
            >
              Post Notice
            </button>
          </div>
        </form>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js'
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js'
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js'
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass.js'
import { GammaCorrectionShader } from 'three/examples/jsm/shaders/GammaCorrectionShader.js'
import { useTheme } from '../composables/useTheme'

const { isDark } = useTheme()

const canvasRef = ref(null)
const loadingProgress = ref(0)
const currentYear = new Date().getFullYear()
const toastMessage = ref('')
const middleTextState = ref('before') // 'before' | 'active' | 'after'

function showToast(msg) {
  toastMessage.value = msg
  setTimeout(() => {
    toastMessage.value = ''
  }, 3500)
}

// ----------------------------------------------------
// COMMUNITY SESSIONS DATA (Clear & Concise)
// ----------------------------------------------------
const flightSessions = ref([
  {
    id: 1,
    title: 'Sunrise Freestyle & Proximity',
    category: 'WEEKEND FLY-IN',
    time: 'Sun · 6:00 AM',
    location: 'Chroy Changvar Field, PP',
    description: 'Open grass runway with low wind. Freestyle gaps and co-pilot spotting.',
    attendees: ['Vuthy', 'Dara', 'Alex', 'Samnang', 'Chhay', 'Sreypov'],
    isJoined: false
  },
  {
    id: 2,
    title: 'Bench Tuning & Maiden Flights',
    category: 'MAKER LAB',
    time: 'Sat · 1:30 PM',
    location: 'AeroByte Lab, Ta Khmau',
    description: 'Soldering bench, Betaflight 4.5 tuning, and new quad hardware checks.',
    attendees: ['Rithy', 'Bona', 'Sophea', 'Sovann', 'Alex'],
    isJoined: true
  },
  {
    id: 3,
    title: 'Kirirom Mountain Expedition',
    category: 'EXPEDITION',
    time: 'Next Sun · 7:00 AM',
    location: 'Kirirom Ridge, Kampong Speu',
    description: 'Long-range cruising over pine forests with GPS rescue safety teams.',
    attendees: ['Samnang', 'Dara', 'Alex'],
    isJoined: false
  }
])

function toggleRSVP(session) {
  session.isJoined = !session.isJoined
  if (session.isJoined) {
    if (!session.attendees.includes('You')) session.attendees.push('You')
    showToast(`RSVP Confirmed: ${session.title}`)
  } else {
    session.attendees = session.attendees.filter((p) => p !== 'You')
    showToast(`RSVP Cancelled: ${session.title}`)
  }
}

// ----------------------------------------------------
// PILOT RADAR NOTICEBOARD
// ----------------------------------------------------
const activeFilter = ref('All Callouts')
const showCalloutModal = ref(false)

const newCallout = ref({
  author: '',
  category: 'Looking for Spotter',
  droneSetup: '',
  spot: '',
  dateTime: '',
  message: ''
})

const buddyPosts = ref([
  {
    id: 1,
    author: 'Rithy_Aero',
    droneSetup: '5" 6S Freestyle',
    category: 'Looking for Spotter',
    spot: 'Chroy Changvar',
    dateTime: 'Saturday 6:30 AM',
    message: 'Need a spotter for practicing power loops and inverted yaw spins.',
    telegramLink: 'https://t.me/aerobyteacademy'
  },
  {
    id: 2,
    author: 'Sreymom_Wings',
    droneSetup: 'Cetus X Tinywhoop',
    category: 'Beginners Welcome',
    spot: 'Ta Khmau Field',
    dateTime: 'Sunday 8:00 AM',
    message: 'First outdoor flight in acro mode. Looking for someone to guide rate settings.',
    telegramLink: 'https://t.me/aerobyteacademy'
  },
  {
    id: 3,
    author: 'Samnang_FPV',
    droneSetup: '3.5" Sub-250g',
    category: 'Freestyle & Gaps',
    spot: 'Koh Pich',
    dateTime: 'Friday 5:00 PM',
    message: 'Sunset proximity run. Looking for a chase cam buddy.',
    telegramLink: 'https://t.me/aerobyteacademy'
  },
  {
    id: 4,
    author: 'Alex_Tech',
    droneSetup: '7" Long Range',
    category: 'Ta Khmau Lab',
    spot: 'AeroByte Lab',
    dateTime: 'Saturday 2:00 PM',
    message: 'Testing ELRS 3.4 dynamic power & GPS rescue at the bench.',
    telegramLink: 'https://t.me/aerobyteacademy'
  }
])

const filteredPosts = computed(() => {
  if (activeFilter.value === 'All Callouts') return buddyPosts.value
  return buddyPosts.value.filter((p) => p.category === activeFilter.value)
})

function submitCallout() {
  if (!newCallout.value.author || !newCallout.value.message) return
  buddyPosts.value.unshift({
    id: Date.now(),
    author: newCallout.value.author,
    droneSetup: newCallout.value.droneSetup || 'FPV Quad',
    category: newCallout.value.category,
    spot: newCallout.value.spot || 'Phnom Penh',
    dateTime: newCallout.value.dateTime || 'This Weekend',
    message: newCallout.value.message,
    telegramLink: 'https://t.me/aerobyteacademy'
  })
  showCalloutModal.value = false
  showToast('Notice posted to board')
  newCallout.value = {
    author: '',
    category: 'Looking for Spotter',
    droneSetup: '',
    spot: '',
    dateTime: '',
    message: ''
  }
}

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

  const gltfLoader = new GLTFLoader()
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
  // Stage 3 (Middle Anthem): Drone sweeps promptly and smoothly into center (y = 0.75) ABOVE FLY AS ONE text
  // Stage 4 (Perks): Right hover facing elevated perks
  // Stage 5 (Radar): Center hover above noticeboard
  const STOPS_X = [
    { p: 0.00, v: 0.0 },   // Hero: Center
    { p: 0.12, v: -2.8 },  // Section 2: Drone glides to Left opposite cards
    { p: 0.18, v: -2.8 },  // Section 2 hold
    { p: 0.28, v: 0.0 },   // Rotates & sweeps smoothly and promptly into Center as cards end!
    { p: 0.48, v: 0.0 },   // Middle Stop: Center hold above text
    { p: 0.58, v: 2.8 },   // Section 4: Drone sweeps to Right opposite perks
    { p: 0.74, v: 2.8 },   // Section 4 hold
    { p: 0.86, v: 0.0 },   // Section 5: Drone sweeps to Center
    { p: 1.00, v: 0.0 }    // Bottom hold: Center
  ]

  const STOPS_Y = [
    { p: 0.00, v: -0.40 }, // Hero: comfortably below top text
    { p: 0.12, v: 0.15 },  // Section 2: level with upper cards
    { p: 0.18, v: 0.15 },
    { p: 0.28, v: 0.75 },  // Middle Stop: HIGH in upper center (37% from top), hovers ABOVE text!
    { p: 0.48, v: 0.75 },  // Middle Stop hold: text sits cleanly UNDER the drone!
    { p: 0.58, v: 0.15 },  // Section 4: level with upper perks cards
    { p: 0.74, v: 0.15 },
    { p: 0.86, v: 0.35 },  // Bottom: Upper center
    { p: 1.00, v: 0.35 }
  ]

  const STOPS_S = [
    { p: 0.00, v: 1.35 },
    { p: 0.12, v: 1.10 },
    { p: 0.18, v: 1.10 },
    { p: 0.28, v: 1.25 },  // Middle Stop: Prominent showcase
    { p: 0.48, v: 1.25 },
    { p: 0.58, v: 1.10 },
    { p: 0.74, v: 1.10 },
    { p: 0.86, v: 1.15 },
    { p: 1.00, v: 1.15 }
  ]

  const STOPS_ROLL = [
    { p: 0.00, v: 0.0 },
    { p: 0.12, v: 0.0 },
    { p: 0.18, v: 0.0 },
    { p: 0.28, v: 0.0 },
    { p: 0.48, v: 0.0 },
    { p: 0.58, v: 0.0 },
    { p: 0.74, v: 0.0 },
    { p: 0.86, v: 0.0 },
    { p: 1.00, v: 0.0 }
  ]

  const STOPS_PITCH = [
    { p: 0.00, v: 0.22 },  // Natural forward flight tilt facing user
    { p: 0.12, v: 0.08 },  // Slight hover tilt pointing at cards
    { p: 0.18, v: 0.08 },
    { p: 0.28, v: 0.22 },  // Forward flight tilt facing user above text
    { p: 0.48, v: 0.22 },
    { p: 0.58, v: 0.08 },  // Slight hover tilt pointing at perks
    { p: 0.74, v: 0.08 },
    { p: 0.86, v: 0.20 },
    { p: 1.00, v: 0.20 }
  ]

  const STOPS_YAW = [
    { p: 0.00, v: 0.0 },     // 1. Hero: Facing forward
    { p: 0.12, v: DEG90 },   // 2. Left: Rotates 90° right to point directly at cards
    { p: 0.18, v: DEG90 },   // Section 2 hold
    { p: 0.28, v: 0.0 },     // Rotates promptly to 0° facing forward as it glides to center!
    { p: 0.48, v: 0.0 },     // Middle Stop hold: Facing forward
    { p: 0.58, v: -DEG90 },  // Rotates 90° left to point at perks
    { p: 0.74, v: -DEG90 },  // Section 4 hold
    { p: 0.86, v: 0.0 },     // Rotates to 0° facing forward
    { p: 1.00, v: 0.0 }
  ]

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
  let curS = STOPS_S[0].v
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

    const sideScale = Math.max(0.5, Math.min(1, window.innerWidth / 1200))
    const targetX = sample(STOPS_X, curP) * sideScale
    const targetY = sample(STOPS_Y, curP)
    const targetS = sample(STOPS_S, curP)
    const targetRoll = sample(STOPS_ROLL, curP)
    const targetPitch = sample(STOPS_PITCH, curP)
    const targetYaw = sample(STOPS_YAW, curP)

    const k = Math.min(1, dt * 4.5)
    curX += (targetX - curX) * k
    curY += (targetY - curY) * k
    curS += (targetS - curS) * k
    curRoll += (targetRoll - curRoll) * k
    curPitch += (targetPitch - curPitch) * k
    curYaw += (targetYaw - curYaw) * k

    // Middle text sliding reveal: smoothly shows as drone arrives in the middle
    if (curP < 0.22) {
      middleTextState.value = 'before'
    } else if (curP > 0.50) {
      middleTextState.value = 'after'
    } else {
      middleTextState.value = 'active'
    }

    const hoverBob = Math.sin(now * 0.0018) * 0.05
    worldGroup.position.set(curX, curY + hoverBob, 0)
    worldGroup.scale.setScalar(curS)

    scrollSpeed *= Math.pow(0.04, dt)
    if (scrollSpeed < 0.04) scrollSpeed = 0

    // Smooth idle propeller spin, revving faster while actively scrolling
    const propSpinSpeed = 10.0 + scrollSpeed * 2.5
    propellers.forEach((p) => {
      p.group.rotateOnAxis(p.axis, propSpinSpeed * dt * p.dir)
    })

    droneGroup.rotation.y = curYaw
    droneGroup.rotation.x = curPitch
    droneGroup.rotation.z = curRoll

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
