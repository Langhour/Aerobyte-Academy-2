<template>
  <div class="aero-fly-root relative isolate min-h-screen transition-colors duration-300 bg-[#f8fafc] dark:bg-[#04060f] text-slate-800 dark:text-[#f3f6ff] overflow-x-hidden selection:bg-orange-500/20 selection:text-orange-600 dark:selection:bg-[#5df0a8]/20 dark:selection:text-[#5df0a8]">
    <!-- Fixed WebGL 3D Real Drone Canvas Behind Everything -->
    <canvas ref="canvasRef" class="fixed inset-0 w-full h-full block z-0 pointer-events-none"></canvas>

    <!-- FPV HUD OSD Telemetry Background Overlay (Cyber Drone Aesthetics) -->
    <div class="fixed inset-0 pointer-events-none z-1 overflow-hidden select-none opacity-40 dark:opacity-60 transition-opacity">
      <!-- Top HUD Banner -->
      <div class="absolute top-20 left-4 sm:left-8 flex items-center gap-3 text-[10px] sm:text-xs font-mono font-bold tracking-wider text-slate-500 dark:text-cyan-400/80">
        <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded bg-slate-200/60 dark:bg-cyan-950/40 border border-slate-300/80 dark:border-cyan-500/30">
          <span class="w-1.5 h-1.5 rounded-full bg-red-500 animate-pulse"></span>
          REC 00:14:32
        </span>
        <span class="hidden md:inline-block">CAM 1 · 4K 120FPS</span>
        <span class="hidden sm:inline-block">VTX: RACEBAND 5.8GHz</span>
      </div>

      <div class="absolute top-20 right-4 sm:right-8 flex items-center gap-3 text-[10px] sm:text-xs font-mono font-bold tracking-wider text-slate-500 dark:text-cyan-400/80">
        <span class="hidden sm:inline-block">BAT: 22.8V 6S (84%)</span>
        <span class="inline-flex items-center gap-1.5 px-2 py-0.5 rounded bg-slate-200/60 dark:bg-cyan-950/40 border border-slate-300/80 dark:border-cyan-500/30">
          <span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>
          ELRS 1000Hz · 99dBm
        </span>
      </div>

      <!-- Corner HUD Reticles -->
      <div class="hidden lg:block absolute top-28 left-6 w-8 h-8 border-t-2 border-l-2 border-sky-400/40 dark:border-cyan-400/40"></div>
      <div class="hidden lg:block absolute top-28 right-6 w-8 h-8 border-t-2 border-r-2 border-sky-400/40 dark:border-cyan-400/40"></div>
      <div class="hidden lg:block absolute bottom-12 left-6 w-8 h-8 border-b-2 border-l-2 border-sky-400/40 dark:border-cyan-400/40"></div>
      <div class="hidden lg:block absolute bottom-12 right-6 w-8 h-8 border-b-2 border-r-2 border-sky-400/40 dark:border-cyan-400/40"></div>

      <!-- Center Subtle Horizon Crosshair Guide -->
      <div class="hidden md:flex absolute inset-0 items-center justify-center opacity-20 dark:opacity-30">
        <div class="w-20 h-0.5 bg-sky-500 dark:bg-cyan-400"></div>
        <div class="w-6 h-6 border border-sky-500 dark:border-cyan-400 rounded-full mx-2 flex items-center justify-center">
          <div class="w-1 h-1 bg-sky-500 dark:bg-cyan-400 rounded-full"></div>
        </div>
        <div class="w-20 h-0.5 bg-sky-500 dark:bg-cyan-400"></div>
      </div>
    </div>

    <!-- Loading Indicator overlay while real 3D drone GLB loads -->
    <div
      v-if="loadingProgress < 100"
      class="fixed bottom-6 right-6 z-50 flex items-center gap-3 bg-white/95 dark:bg-[rgba(12,18,38,0.9)] border border-slate-300 dark:border-[rgba(150,175,230,0.2)] px-4 py-2.5 rounded-full backdrop-blur-md shadow-xl text-xs font-bold text-slate-800 dark:text-white transition-opacity duration-500"
      :class="loadingProgress >= 100 ? 'opacity-0 pointer-events-none' : 'opacity-100'"
    >
      <div class="w-4 h-4 border-2 border-orange-500 dark:border-[#5df0a8] border-t-transparent rounded-full animate-spin"></div>
      <span>Loading 3D FPV Drone Canvas... {{ loadingProgress }}%</span>
    </div>

    <!-- Toast Notification for Community Actions -->
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
        class="fixed top-24 right-6 z-50 flex items-center gap-3 px-5 py-3 rounded-2xl bg-slate-900/95 dark:bg-[#070e24]/95 text-white border border-emerald-500/40 shadow-2xl backdrop-blur-xl text-sm font-semibold"
      >
        <span class="text-emerald-400 text-lg">✓</span>
        <span>{{ toastMessage }}</span>
      </div>
    </transition>

    <!-- Page Content Floating Over Fixed 3D Drone -->
    <div class="relative z-10">

      <!-- SECTION 1: HERO - COMMUNITY FLIGHT COLLECTIVE -->
      <section class="min-h-[92vh] flex flex-col justify-between items-center text-center px-4 sm:px-6 pt-10 pb-16 relative">
        <div class="max-w-4xl mx-auto space-y-6">
          <!-- Live Collective Status Badge -->
          <div class="inline-flex items-center gap-2.5 px-4 py-1.5 rounded-full bg-white/90 dark:bg-[rgba(12,18,38,0.8)] border border-slate-300 dark:border-cyan-500/30 text-slate-700 dark:text-cyan-300 text-xs font-bold tracking-wider uppercase backdrop-blur-md shadow-xs">
            <span class="relative flex h-2.5 w-2.5">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
            </span>
            <span>142 Active Pilots · Cambodia Drone Flight Collective</span>
          </div>

          <!-- Main Community Headline -->
          <h1 class="text-4xl sm:text-6xl lg:text-7xl font-black tracking-tight leading-[1.08] text-[#0c1e5b] dark:text-white transition-colors">
            Fly Together.<br>
            <span class="bg-gradient-to-r from-sky-600 via-teal-500 to-emerald-500 dark:from-cyan-400 dark:via-[#5df0a8] dark:to-emerald-400 bg-clip-text text-transparent">
              Never Fly Solo.
            </span>
          </h1>

          <!-- Clear Communication & Meetup Mission -->
          <p class="text-base sm:text-xl text-slate-600 dark:text-[#a6b4d4] leading-relaxed max-w-2xl mx-auto transition-colors font-medium">
            Connect with local FPV & camera drone pilots across Cambodia. Find flight spotters, coordinate weekend group sessions, synchronize VTX race frequencies, and share open fields.
          </p>

          <!-- Action Buttons -->
          <div class="pt-2 flex flex-wrap items-center justify-center gap-3.5">
            <a
              href="https://t.me/aerobyteacademy"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex items-center justify-center gap-2.5 rounded-full bg-[#ff6b00] hover:bg-[#e05e00] text-white px-7 py-3.5 text-sm sm:text-base font-bold shadow-lg shadow-orange-500/25 hover:shadow-orange-500/40 hover:-translate-y-0.5 transition active:scale-95 cursor-pointer"
            >
              <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24">
                <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.121l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.458c.538-.196 1.006.128.832.943z"/>
              </svg>
              <span>Join Pilot Telegram Group</span>
            </a>

            <a
              href="#sessions"
              class="inline-flex items-center justify-center gap-2 rounded-full bg-white/90 dark:bg-[rgba(16,24,48,0.7)] hover:bg-slate-50 dark:hover:bg-white/10 border border-slate-300 dark:border-[rgba(150,175,230,0.22)] px-6 py-3.5 text-sm sm:text-base font-bold text-[#0c1e5b] dark:text-white transition hover:-translate-y-0.5 shadow-xs backdrop-blur-md"
            >
              <span>📅 Upcoming Weekend Flights</span>
            </a>

            <a
              href="#buddy-board"
              class="inline-flex items-center justify-center gap-2 rounded-full bg-sky-50 dark:bg-cyan-500/10 hover:bg-sky-100 dark:hover:bg-cyan-500/20 border border-sky-200 dark:border-cyan-500/30 px-6 py-3.5 text-sm sm:text-base font-bold text-sky-700 dark:text-cyan-300 transition hover:-translate-y-0.5 shadow-xs backdrop-blur-md"
            >
              <span>🛸 Find a Flight Buddy</span>
            </a>
          </div>
        </div>

        <!-- Spacer area allowing the 3D drone to hover in full view -->
        <div class="h-28 sm:h-40 pointer-events-none"></div>

        <!-- Real Flight Collective Key Metrics -->
        <div class="pt-6 border-t border-slate-200/80 dark:border-[rgba(150,175,230,0.12)] w-full max-w-4xl mx-auto transition-colors">
          <div class="grid grid-cols-2 md:grid-cols-4 gap-4 text-center">
            <div class="p-3">
              <div class="text-2xl sm:text-3xl font-black text-[#0c1e5b] dark:text-cyan-400">140+</div>
              <div class="text-xs font-semibold text-slate-500 dark:text-[#9aa6c4] mt-0.5">Active Pilots</div>
            </div>
            <div class="p-3">
              <div class="text-2xl sm:text-3xl font-black text-[#0c1e5b] dark:text-[#5df0a8]">38+</div>
              <div class="text-xs font-semibold text-slate-500 dark:text-[#9aa6c4] mt-0.5">Group Meetups Hosted</div>
            </div>
            <div class="p-3">
              <div class="text-2xl sm:text-3xl font-black text-[#0c1e5b] dark:text-orange-400">6 Spots</div>
              <div class="text-xs font-semibold text-slate-500 dark:text-[#9aa6c4] mt-0.5">Mapped Flying Fields</div>
            </div>
            <div class="p-3">
              <div class="text-2xl sm:text-3xl font-black text-[#0c1e5b] dark:text-emerald-400">100% Free</div>
              <div class="text-xs font-semibold text-slate-500 dark:text-[#9aa6c4] mt-0.5">Open Spotter Network</div>
            </div>
          </div>
        </div>
      </section>

      <!-- SECTION 2: UPCOMING GROUP FLIGHTS & WEATHER RADAR -->
      <section id="sessions" class="py-20 sm:py-28 px-4 sm:px-6 lg:px-8 max-w-[1180px] mx-auto">
        <!-- Section Header with Flight Radar Pill -->
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-12">
          <div class="space-y-2">
            <div class="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-[#ff6b00]">
              <span>Group Flying Calendar</span>
            </div>
            <h2 class="text-3xl sm:text-4xl lg:text-5xl font-black text-[#0c1e5b] dark:text-white transition-colors">
              Upcoming Flight Gatherings
            </h2>
            <p class="text-sm sm:text-base text-slate-600 dark:text-[#9aa6c4] max-w-xl">
              Never fly alone without a spotter. Join scheduled outdoor sessions, test props, and learn high-speed lines together.
            </p>
          </div>

          <!-- Live Weather Condition Card -->
          <div class="p-4 rounded-2xl bg-white/80 dark:bg-[rgba(16,24,48,0.7)] border border-slate-200 dark:border-[rgba(150,175,230,0.18)] backdrop-blur-md shadow-xs flex items-center gap-4">
            <div class="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-500/10 border border-emerald-200 dark:border-emerald-500/20 text-emerald-600 dark:text-emerald-400 flex items-center justify-center text-xl">
              ⛅
            </div>
            <div class="text-left text-xs">
              <div class="flex items-center gap-1.5 font-bold text-slate-800 dark:text-white">
                <span>Phnom Penh Sky Radar</span>
                <span class="w-2 h-2 rounded-full bg-emerald-500 animate-pulse"></span>
              </div>
              <div class="text-slate-500 dark:text-[#9aa6c4] mt-0.5">Wind 8 km/h · 0% Rain · Flight Go-Ahead: <span class="font-bold text-emerald-600 dark:text-emerald-400">OPTIMAL</span></div>
            </div>
          </div>
        </div>

        <!-- Flight Meetup Cards Grid -->
        <div class="grid md:grid-cols-3 gap-6">
          <div
            v-for="session in flightSessions"
            :key="session.id"
            class="group relative rounded-3xl p-7 bg-white/80 dark:bg-[rgba(12,18,38,0.65)] border border-slate-200 dark:border-[rgba(150,175,230,0.15)] hover:border-sky-400 dark:hover:border-cyan-500/40 backdrop-blur-xl shadow-sm dark:shadow-none transition-all duration-300 hover:-translate-y-1.5 flex flex-col justify-between"
          >
            <!-- Top Tag & Time -->
            <div>
              <div class="flex items-center justify-between mb-4">
                <span class="text-[11px] font-bold uppercase tracking-wider px-3 py-1 rounded-full" :class="session.tagClass">
                  {{ session.category }}
                </span>
                <span class="text-xs font-semibold text-slate-500 dark:text-[#8d9ab9]">
                  {{ session.time }}
                </span>
              </div>

              <h3 class="text-xl font-bold text-[#0c1e5b] dark:text-white mb-2 group-hover:text-sky-600 dark:group-hover:text-cyan-400 transition-colors">
                {{ session.title }}
              </h3>

              <div class="flex items-center gap-1.5 text-xs font-semibold text-slate-500 dark:text-[#9aa6c4] mb-4">
                <svg class="w-4 h-4 text-orange-500 shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z" />
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z" />
                </svg>
                <span>{{ session.location }}</span>
              </div>

              <p class="text-xs sm:text-sm text-slate-600 dark:text-[#a0afcf] leading-relaxed mb-6">
                {{ session.description }}
              </p>

              <!-- Pilot Attendees Counter & Avatars -->
              <div class="flex items-center justify-between py-3 px-3.5 rounded-2xl bg-slate-50 dark:bg-black/25 border border-slate-200/80 dark:border-white/5 mb-6 text-xs font-semibold text-slate-600 dark:text-[#9aa6c4]">
                <div class="flex items-center gap-2">
                  <span class="text-base">👥</span>
                  <span>{{ session.attendees.length }} Pilots Confirmed</span>
                </div>
                <span class="text-[11px] font-bold text-emerald-600 dark:text-[#5df0a8]">
                  Open Slots
                </span>
              </div>
            </div>

            <!-- RSVP Button -->
            <button
              type="button"
              @click="toggleRSVP(session)"
              class="w-full py-3 px-4 rounded-full font-bold text-xs sm:text-sm transition-all duration-200 flex items-center justify-center gap-2 cursor-pointer shadow-xs"
              :class="session.isJoined
                ? 'bg-emerald-500 text-white shadow-emerald-500/20'
                : 'bg-[#0c1e5b] dark:bg-white text-white dark:text-[#0c1e5b] hover:bg-sky-700 dark:hover:bg-slate-200 active:scale-95'"
            >
              <span v-if="session.isJoined">✓ You're Flying (Confirmed)</span>
              <span v-else>+ RSVP to Fly Together</span>
            </button>
          </div>
        </div>
      </section>

      <!-- SECTION 3: VTX RACEBAND FREQUENCY COORDINATION (Authentic FPV Pilot Hub) -->
      <section class="py-20 px-4 sm:px-6 lg:px-8 max-w-[1180px] mx-auto">
        <div class="rounded-3xl p-8 sm:p-12 bg-white/80 dark:bg-[rgba(16,24,48,0.7)] border border-slate-200 dark:border-cyan-500/20 backdrop-blur-2xl shadow-xl dark:shadow-2xl transition-colors">
          <div class="max-w-2xl mb-8">
            <div class="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-sky-600 dark:text-cyan-400 mb-2">
              <span class="w-2 h-2 rounded-full bg-sky-500 dark:bg-cyan-400"></span>
              Frequency Safety Board
            </div>
            <h2 class="text-3xl sm:text-4xl font-black text-[#0c1e5b] dark:text-white leading-tight">
              5.8GHz VTX Frequency Matrix
            </h2>
            <p class="text-xs sm:text-sm text-slate-600 dark:text-[#9aa6c4] mt-2 leading-relaxed">
              When flying together, frequency management is life or death for our goggles. Check which Raceband channels are occupied or reserve an open slot before turning on your quad.
            </p>
          </div>

          <!-- 8 Raceband Channels Grid -->
          <div class="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-8 gap-3">
            <div
              v-for="ch in vtxChannels"
              :key="ch.channel"
              class="p-4 rounded-2xl border text-center transition-all duration-200 flex flex-col justify-between"
              :class="ch.pilot
                ? 'bg-orange-50/70 dark:bg-orange-500/10 border-orange-200 dark:border-orange-500/30'
                : 'bg-slate-50/80 dark:bg-white/5 border-slate-200 dark:border-white/10 hover:border-cyan-400/50 hover:bg-sky-50/50 dark:hover:bg-cyan-500/10 cursor-pointer'"
              @click="!ch.pilot && openClaimChannel(ch)"
            >
              <div>
                <div class="text-xs font-mono font-bold text-slate-500 dark:text-[#8d9ab9]">{{ ch.mhz }} MHz</div>
                <div class="text-lg font-black my-1" :class="ch.pilot ? 'text-orange-600 dark:text-orange-400' : 'text-[#0c1e5b] dark:text-white'">
                  {{ ch.channel }}
                </div>
              </div>

              <div class="mt-3 pt-3 border-t border-slate-200 dark:border-white/5">
                <template v-if="ch.pilot">
                  <span class="text-[11px] font-bold text-slate-800 dark:text-white truncate block">
                    {{ ch.pilot }}
                  </span>
                  <span class="text-[10px] text-slate-500 dark:text-slate-400 block truncate">
                    {{ ch.protocol }}
                  </span>
                </template>
                <template v-else>
                  <span class="text-[11px] font-bold text-emerald-600 dark:text-[#5df0a8] block">
                    + Claim Slot
                  </span>
                </template>
              </div>
            </div>
          </div>

          <!-- Safety Notice -->
          <div class="mt-8 flex flex-col sm:flex-row items-center justify-between gap-4 p-4 rounded-2xl bg-sky-50/80 dark:bg-cyan-950/20 border border-sky-100 dark:border-cyan-500/20 text-xs">
            <div class="flex items-center gap-3 text-sky-800 dark:text-cyan-200 font-medium">
              <span class="text-lg">⚠️</span>
              <span><strong>Pilot Safety Rule:</strong> Never power on your drone in the pits while other pilots are in the air without checking Raceband channels first!</span>
            </div>
            <a
              href="https://t.me/aerobyteacademy"
              target="_blank"
              rel="noopener noreferrer"
              class="font-bold text-[#ff6b00] hover:underline shrink-0"
            >
              Live Chat Channel on Telegram →
            </a>
          </div>
        </div>
      </section>

      <!-- SECTION 4: FLIGHT BUDDY & SPOTTER FINDER NOTICEBOARD -->
      <section id="buddy-board" class="py-20 sm:py-28 px-4 sm:px-6 lg:px-8 max-w-[1180px] mx-auto">
        <!-- Section Header with Post Button -->
        <div class="flex flex-col md:flex-row md:items-end justify-between gap-6 mb-10">
          <div class="space-y-2">
            <div class="inline-flex items-center gap-2 text-xs font-bold uppercase tracking-widest text-[#5df0a8]">
              <span>Pilot Communication Board</span>
            </div>
            <h2 class="text-3xl sm:text-4xl lg:text-5xl font-black text-[#0c1e5b] dark:text-white transition-colors">
              Flight Buddy & Spotter Finder
            </h2>
            <p class="text-sm sm:text-base text-slate-600 dark:text-[#9aa6c4] max-w-xl">
              Solo today? Post a callout for a safety spotter, invite pilots to your favorite grass field, or ask for beginner bench help.
            </p>
          </div>

          <button
            type="button"
            @click="showCalloutModal = true"
            class="inline-flex items-center justify-center gap-2 rounded-full bg-[#ff6b00] hover:bg-[#e05e00] text-white px-6 py-3.5 text-sm font-bold shadow-lg shadow-orange-500/25 hover:shadow-orange-500/40 transition active:scale-95 cursor-pointer shrink-0"
          >
            <span>+ Post a Flight Callout</span>
          </button>
        </div>

        <!-- Filter Tabs -->
        <div class="flex flex-wrap items-center gap-2 mb-8">
          <button
            v-for="filter in ['All Callouts', 'Looking for Spotter', 'Beginners Welcome', 'Freestyle & Gaps', 'Ta Khmau Lab']"
            :key="filter"
            type="button"
            @click="activeFilter = filter"
            class="px-4 py-2 rounded-full text-xs font-bold transition cursor-pointer"
            :class="activeFilter === filter
              ? 'bg-[#0c1e5b] dark:bg-white text-white dark:text-[#0c1e5b] shadow-xs'
              : 'bg-white/70 dark:bg-white/5 text-slate-600 dark:text-[#9aa6c4] hover:bg-slate-100 dark:hover:bg-white/10 border border-slate-200 dark:border-white/10'"
          >
            {{ filter }}
          </button>
        </div>

        <!-- Callouts Grid -->
        <div class="grid md:grid-cols-2 gap-5">
          <div
            v-for="post in filteredPosts"
            :key="post.id"
            class="p-6 rounded-3xl bg-white/80 dark:bg-[rgba(12,18,38,0.65)] border border-slate-200 dark:border-[rgba(150,175,230,0.15)] backdrop-blur-xl shadow-xs dark:shadow-none hover:border-sky-400 dark:hover:border-cyan-500/30 transition-all flex flex-col justify-between"
          >
            <div>
              <div class="flex items-center justify-between mb-3">
                <div class="flex items-center gap-3">
                  <div class="w-10 h-10 rounded-full bg-gradient-to-tr from-sky-500 to-indigo-600 text-white flex items-center justify-center font-bold text-sm">
                    {{ post.avatar }}
                  </div>
                  <div>
                    <h4 class="text-sm font-bold text-[#0c1e5b] dark:text-white">{{ post.author }}</h4>
                    <span class="text-[11px] text-slate-500 dark:text-[#8d9ab9] font-mono">{{ post.droneSetup }}</span>
                  </div>
                </div>

                <span class="text-[10px] font-bold uppercase tracking-wider px-2.5 py-1 rounded-full bg-sky-100 text-sky-700 dark:bg-cyan-500/10 dark:text-cyan-300 border border-sky-200 dark:border-cyan-500/20">
                  {{ post.category }}
                </span>
              </div>

              <div class="flex items-center gap-2 text-xs font-semibold text-slate-500 dark:text-[#8d9ab9] my-2">
                <span class="text-orange-500">📍 {{ post.spot }}</span>
                <span>·</span>
                <span>⏰ {{ post.dateTime }}</span>
              </div>

              <p class="text-xs sm:text-sm text-slate-600 dark:text-[#a0afcf] leading-relaxed mt-2 mb-4">
                "{{ post.message }}"
              </p>
            </div>

            <div class="pt-3 border-t border-slate-100 dark:border-white/5 flex items-center justify-between">
              <span class="text-[11px] text-slate-400 dark:text-slate-500">{{ post.postedAgo }}</span>
              <a
                :href="post.telegramLink || 'https://t.me/aerobyteacademy'"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center gap-1.5 text-xs font-bold text-[#ff6b00] hover:underline"
              >
                <span>Reply on Telegram</span>
                <span>→</span>
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- SECTION 5: PILOT HUBS & CHANNELS -->
      <section class="py-20 px-4 sm:px-6 lg:px-8 max-w-[1180px] mx-auto">
        <div class="grid md:grid-cols-2 gap-8 items-stretch">
          <!-- Card 1: Official Telegram Group -->
          <div class="p-8 sm:p-10 rounded-3xl bg-gradient-to-b from-white/90 to-slate-50/80 dark:from-[rgba(16,24,48,0.8)] dark:to-[rgba(12,18,38,0.8)] border border-slate-200 dark:border-cyan-500/20 backdrop-blur-xl shadow-lg flex flex-col justify-between">
            <div class="space-y-4">
              <div class="w-12 h-12 rounded-2xl bg-sky-500/10 text-sky-500 dark:text-cyan-400 border border-sky-500/20 flex items-center justify-center text-2xl">
                💬
              </div>
              <h3 class="text-2xl sm:text-3xl font-black text-[#0c1e5b] dark:text-white">
                Telegram Pilot Community
              </h3>
              <p class="text-sm text-slate-600 dark:text-[#9aa6c4] leading-relaxed">
                Our main live communication hub. Where weekend flight polls are posted every Thursday, lost drones get rescued by spotter teams, and flight logs are dissected.
              </p>

              <div class="space-y-2 pt-2 text-xs font-semibold text-slate-600 dark:text-[#9aa6c4]">
                <div class="flex items-center gap-2">
                  <span class="text-emerald-500">✓</span>
                  <span><strong>#flight-radar:</strong> Live weekend coordinates & weather checks</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-emerald-500">✓</span>
                  <span><strong>#vtx-coordination:</strong> Reserve your Raceband before spinning motors</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-emerald-500">✓</span>
                  <span><strong>#bench-troubleshooting:</strong> Betaflight PID & soldering help</span>
                </div>
              </div>
            </div>

            <div class="pt-8">
              <a
                href="https://t.me/aerobyteacademy"
                target="_blank"
                rel="noopener noreferrer"
                class="w-full inline-flex items-center justify-center gap-2.5 rounded-full bg-[#ff6b00] hover:bg-[#e05e00] text-white py-3.5 px-6 text-sm font-bold shadow-md hover:shadow-lg transition cursor-pointer"
              >
                <span>Join AeroByte Telegram Channel</span>
                <span>→</span>
              </a>
            </div>
          </div>

          <!-- Card 2: Free Ta Khmau Physical Lab -->
          <div class="p-8 sm:p-10 rounded-3xl bg-gradient-to-b from-white/90 to-slate-50/80 dark:from-[rgba(16,24,48,0.8)] dark:to-[rgba(12,18,38,0.8)] border border-slate-200 dark:border-cyan-500/20 backdrop-blur-xl shadow-lg flex flex-col justify-between">
            <div class="space-y-4">
              <div class="w-12 h-12 rounded-2xl bg-orange-500/10 text-orange-500 border border-orange-500/20 flex items-center justify-center text-2xl">
                📍
              </div>
              <h3 class="text-2xl sm:text-3xl font-black text-[#0c1e5b] dark:text-white">
                Ta Khmau Flight Lab & Bench
              </h3>
              <p class="text-sm text-slate-600 dark:text-[#9aa6c4] leading-relaxed">
                Need to solder an ESC, balance your carbon props, or test your 6S battery capacity? Our physical maker workshop in Ta Khmau is 100% free for all local pilots.
              </p>

              <div class="space-y-2 pt-2 text-xs font-semibold text-slate-600 dark:text-[#9aa6c4]">
                <div class="flex items-center gap-2">
                  <span class="text-orange-500">⚡</span>
                  <span><strong>Open:</strong> Tuesday – Sunday · 9:00 AM – 6:00 PM</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-orange-500">🛠️</span>
                  <span><strong>Tools:</strong> Soldering irons, smoke stoppers, Betaflight bench</span>
                </div>
                <div class="flex items-center gap-2">
                  <span class="text-orange-500">☕</span>
                  <span><strong>Vibe:</strong> Free coffee, flight simulators, and pilot hangar talk</span>
                </div>
              </div>
            </div>

            <div class="pt-8">
              <a
                href="https://maps.google.com/?q=Ta+Khmau+Cambodia"
                target="_blank"
                rel="noopener noreferrer"
                class="w-full inline-flex items-center justify-center gap-2 rounded-full bg-white dark:bg-white/10 hover:bg-slate-100 dark:hover:bg-white/15 border border-slate-300 dark:border-white/10 text-[#0c1e5b] dark:text-white py-3.5 px-6 text-sm font-bold transition shadow-xs cursor-pointer"
              >
                <span>Get Directions to Ta Khmau Lab</span>
                <span>↗</span>
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- SECTION 6: COMMUNITY SAFETY & PILOT MANIFESTO -->
      <section class="py-16 px-4 sm:px-6 lg:px-8 max-w-[1180px] mx-auto text-center">
        <div class="p-8 sm:p-14 rounded-3xl bg-gradient-to-b from-sky-50/70 via-white/80 to-slate-50/80 dark:from-cyan-950/20 dark:via-[rgba(16,24,48,0.7)] dark:to-[rgba(12,18,38,0.85)] border border-slate-200 dark:border-cyan-500/20 backdrop-blur-2xl max-w-3xl mx-auto space-y-6">
          <span class="text-xs font-bold uppercase tracking-widest text-[#ff6b00]">Pilot Code of Honor</span>
          <h2 class="text-3xl sm:text-5xl font-black text-[#0c1e5b] dark:text-white leading-tight">
            Ready to Take Flight With Us?
          </h2>
          <p class="text-sm sm:text-base text-slate-600 dark:text-[#a0afcf] leading-relaxed">
            Whether you just bought your first simulator radio controller or you're ripping 5-inch freestyle quads around abandoned concrete gaps, there is always an open chair and a spotter ready for you.
          </p>

          <div class="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3.5">
            <a
              href="https://t.me/aerobyteacademy"
              target="_blank"
              rel="noopener noreferrer"
              class="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 rounded-full bg-[#ff6b00] hover:bg-[#e05e00] text-white px-8 py-3.5 text-base font-bold shadow-lg shadow-orange-500/25 hover:shadow-orange-500/40 transition active:scale-95 cursor-pointer"
            >
              <span>Connect on Telegram Now</span>
              <svg class="w-4 h-4 stroke-current fill-none stroke-[2.5]" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>

            <button
              type="button"
              @click="showCalloutModal = true"
              class="w-full sm:w-auto inline-flex items-center justify-center gap-2 rounded-full bg-white dark:bg-white/10 hover:bg-slate-50 dark:hover:bg-white/15 border border-slate-300 dark:border-white/10 px-7 py-3.5 text-base font-bold text-[#0c1e5b] dark:text-white transition cursor-pointer shadow-xs"
            >
              <span>Post Your First Flight Notice</span>
            </button>
          </div>
        </div>

        <p class="mt-16 text-xs text-slate-500 dark:text-[#6b7796] transition-colors">
          © {{ currentYear }} Aero Fly — Cambodia's Open Drone Flight Community.
        </p>
      </section>
    </div>

    <!-- MODAL 1: POST A FLIGHT CALLOUT -->
    <div
      v-if="showCalloutModal"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-md"
      @click.self="showCalloutModal = false"
    >
      <div class="w-full max-w-lg p-6 sm:p-8 rounded-3xl bg-white dark:bg-[#0c142c] border border-slate-200 dark:border-cyan-500/30 shadow-2xl text-left space-y-5 animate-in fade-in zoom-in-95 duration-200">
        <div class="flex items-center justify-between pb-3 border-b border-slate-200 dark:border-white/10">
          <div>
            <h3 class="text-xl font-bold text-[#0c1e5b] dark:text-white">Post Flight Notice</h3>
            <p class="text-xs text-slate-500 dark:text-[#9aa6c4]">Invite other pilots to fly with you or request a spotter.</p>
          </div>
          <button
            type="button"
            @click="showCalloutModal = false"
            class="w-8 h-8 rounded-full bg-slate-100 dark:bg-white/10 text-slate-500 dark:text-white flex items-center justify-center hover:bg-slate-200 dark:hover:bg-white/20 transition cursor-pointer"
          >
            ✕
          </button>
        </div>

        <form @submit.prevent="submitCallout" class="space-y-4 text-xs">
          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-200 mb-1">Your Pilot Callsign / Name</label>
            <input
              v-model="newCallout.author"
              required
              placeholder="e.g. Dara_FPV"
              class="w-full px-4 py-2.5 rounded-xl bg-slate-50 dark:bg-black/30 border border-slate-300 dark:border-white/10 text-slate-800 dark:text-white outline-none focus:border-sky-500 dark:focus:border-cyan-400"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-200 mb-1">Flight Category</label>
              <select
                v-model="newCallout.category"
                class="w-full px-3 py-2.5 rounded-xl bg-slate-50 dark:bg-[#121c3d] border border-slate-300 dark:border-white/10 text-slate-800 dark:text-white outline-none"
              >
                <option value="Looking for Spotter">Looking for Spotter</option>
                <option value="Weekend Fly-In">Weekend Fly-In</option>
                <option value="Beginners Welcome">Beginners Welcome</option>
                <option value="Freestyle & Gaps">Freestyle & Gaps</option>
                <option value="Ta Khmau Lab">Ta Khmau Lab</option>
              </select>
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-200 mb-1">Drone Setup</label>
              <input
                v-model="newCallout.droneSetup"
                required
                placeholder="e.g. 5-inch 6S / DJI O3"
                class="w-full px-4 py-2.5 rounded-xl bg-slate-50 dark:bg-black/30 border border-slate-300 dark:border-white/10 text-slate-800 dark:text-white outline-none"
              />
            </div>
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-200 mb-1">Flying Field / Spot</label>
              <input
                v-model="newCallout.spot"
                required
                placeholder="e.g. Chroy Changvar"
                class="w-full px-4 py-2.5 rounded-xl bg-slate-50 dark:bg-black/30 border border-slate-300 dark:border-white/10 text-slate-800 dark:text-white outline-none"
              />
            </div>
            <div>
              <label class="block font-bold text-slate-700 dark:text-slate-200 mb-1">Date & Time</label>
              <input
                v-model="newCallout.dateTime"
                required
                placeholder="e.g. Saturday 6:30 AM"
                class="w-full px-4 py-2.5 rounded-xl bg-slate-50 dark:bg-black/30 border border-slate-300 dark:border-white/10 text-slate-800 dark:text-white outline-none"
              />
            </div>
          </div>

          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-200 mb-1">Notice / Message</label>
            <textarea
              v-model="newCallout.message"
              required
              rows="3"
              placeholder="Tell other pilots what you're practicing, what gear to bring, or ask for a spotter..."
              class="w-full px-4 py-2.5 rounded-xl bg-slate-50 dark:bg-black/30 border border-slate-300 dark:border-white/10 text-slate-800 dark:text-white outline-none resize-none"
            ></textarea>
          </div>

          <div class="pt-2 flex items-center justify-end gap-3">
            <button
              type="button"
              @click="showCalloutModal = false"
              class="px-5 py-2.5 rounded-full font-bold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-white/5 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-6 py-2.5 rounded-full font-bold bg-[#ff6b00] hover:bg-[#e05e00] text-white shadow-md cursor-pointer active:scale-95"
            >
              Post Notice to Board
            </button>
          </div>
        </form>
      </div>
    </div>

    <!-- MODAL 2: CLAIM VTX RACEBAND SLOT -->
    <div
      v-if="showClaimModal && targetChannel"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-md"
      @click.self="showClaimModal = false"
    >
      <div class="w-full max-w-sm p-6 rounded-3xl bg-white dark:bg-[#0c142c] border border-slate-200 dark:border-cyan-500/30 shadow-2xl text-left space-y-4 animate-in fade-in zoom-in-95 duration-200">
        <h3 class="text-lg font-bold text-[#0c1e5b] dark:text-white">
          Claim {{ targetChannel.channel }} ({{ targetChannel.mhz }} MHz)
        </h3>
        <p class="text-xs text-slate-500 dark:text-[#9aa6c4]">
          Reserve this frequency for the upcoming session so other pilots know not to power on this band.
        </p>

        <form @submit.prevent="confirmClaimChannel" class="space-y-3 text-xs">
          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-200 mb-1">Your Pilot Callsign</label>
            <input
              v-model="claimForm.pilot"
              required
              placeholder="e.g. Pilot_Vireak"
              class="w-full px-3 py-2 rounded-xl bg-slate-50 dark:bg-black/30 border border-slate-300 dark:border-white/10 text-slate-800 dark:text-white outline-none"
            />
          </div>
          <div>
            <label class="block font-bold text-slate-700 dark:text-slate-200 mb-1">Video System / Protocol</label>
            <select
              v-model="claimForm.protocol"
              class="w-full px-3 py-2 rounded-xl bg-slate-50 dark:bg-[#121c3d] border border-slate-300 dark:border-white/10 text-slate-800 dark:text-white outline-none"
            >
              <option value="DJI O3 / 25mW">DJI O3 (25mW)</option>
              <option value="Analog / 200mW">Analog (200mW)</option>
              <option value="Walksnail Avatar">Walksnail Avatar</option>
              <option value="HDZero / 200mW">HDZero (200mW)</option>
            </select>
          </div>

          <div class="pt-3 flex items-center justify-end gap-2">
            <button
              type="button"
              @click="showClaimModal = false"
              class="px-4 py-2 rounded-full font-bold text-slate-600 dark:text-slate-300 cursor-pointer"
            >
              Cancel
            </button>
            <button
              type="submit"
              class="px-5 py-2 rounded-full font-bold bg-emerald-500 hover:bg-emerald-600 text-white cursor-pointer"
            >
              Confirm Reservation
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

function showToast(msg) {
  toastMessage.value = msg
  setTimeout(() => {
    toastMessage.value = ''
  }, 3500)
}

// ----------------------------------------------------
// COMMUNITY STATE & DATA: FLIGHT SESSIONS
// ----------------------------------------------------
const flightSessions = ref([
  {
    id: 1,
    title: 'Sunrise Freestyle & Proximity Run',
    category: 'Weekend Meetup',
    tagClass: 'bg-orange-100 text-orange-700 dark:bg-orange-500/10 dark:text-orange-400 border border-orange-200 dark:border-orange-500/20',
    time: 'This Sunday · 6:00 AM – 9:30 AM',
    location: 'Chroy Changvar Riverside Fields, Phnom Penh',
    description: 'Wide grass field with zero tree interference. Practicing inverted yaw spins, low altitude throttle control, and gap diving with full spotters.',
    attendees: ['Vuthy', 'Dara', 'Alex', 'Samnang', 'Chhay', 'Sreypov'],
    isJoined: false
  },
  {
    id: 2,
    title: 'Ta Khmau Flight Lab & Bench Tuning Day',
    category: 'Bench & Workshop',
    tagClass: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-400 border border-emerald-200 dark:border-emerald-500/20',
    time: 'Saturday · 1:30 PM – 5:30 PM',
    location: 'AeroByte Physical Lab, Ta Khmau',
    description: 'Free open bench session. Bring soldering projects, calibrate Betaflight 4.5 filters, troubleshoot motor desyncs, and maiden brand new quads.',
    attendees: ['Rithy', 'Bona', 'Sophea', 'Sovann', 'Alex'],
    isJoined: true
  },
  {
    id: 3,
    title: 'Kirirom Pine Forest FPV Expedition',
    category: 'Mountain Flight',
    tagClass: 'bg-sky-100 text-sky-700 dark:bg-cyan-500/10 dark:text-cyan-400 border border-sky-200 dark:border-cyan-500/20',
    time: 'Next Sunday · 7:00 AM – 1:30 PM',
    location: 'Kirirom National Park Ridge, Kampong Speu',
    description: 'Long-range cinematic cruising over pine hills. High power digital VTX (Walksnail/DJI O3), GPS Rescue test verification, and dual spotter safety.',
    attendees: ['Samnang', 'Dara', 'Alex'],
    isJoined: false
  }
])

function toggleRSVP(session) {
  session.isJoined = !session.isJoined
  if (session.isJoined) {
    if (!session.attendees.includes('You')) session.attendees.push('You')
    showToast(`You joined "${session.title}"! See you at the field.`)
  } else {
    session.attendees = session.attendees.filter((p) => p !== 'You')
    showToast(`Removed from "${session.title}" attendance.`)
  }
}

// ----------------------------------------------------
// COMMUNITY STATE & DATA: VTX FREQUENCIES
// ----------------------------------------------------
const vtxChannels = ref([
  { channel: 'R1', mhz: 5658, pilot: 'Dara FPV', protocol: 'DJI O3 · 25mW' },
  { channel: 'R2', mhz: 5695, pilot: null, protocol: null },
  { channel: 'R3', mhz: 5732, pilot: 'Samnang', protocol: 'Analog · 200mW' },
  { channel: 'R4', mhz: 5769, pilot: null, protocol: null },
  { channel: 'R5', mhz: 5806, pilot: 'Alex_Cam', protocol: 'Walksnail' },
  { channel: 'R6', mhz: 5843, pilot: null, protocol: null },
  { channel: 'R7', mhz: 5880, pilot: 'Sophea', protocol: 'HDZero · 200mW' },
  { channel: 'R8', mhz: 5917, pilot: null, protocol: null }
])

const showClaimModal = ref(false)
const targetChannel = ref(null)
const claimForm = ref({ pilot: '', protocol: 'DJI O3 / 25mW' })

function openClaimChannel(ch) {
  targetChannel.value = ch
  claimForm.value.pilot = ''
  showClaimModal.value = true
}

function confirmClaimChannel() {
  if (!targetChannel.value || !claimForm.value.pilot.trim()) return
  targetChannel.value.pilot = claimForm.value.pilot.trim()
  targetChannel.value.protocol = claimForm.value.protocol
  showClaimModal.value = false
  showToast(`Reserved ${targetChannel.value.channel} (${targetChannel.value.mhz} MHz) for ${claimForm.value.pilot}!`)
  targetChannel.value = null
}

// ----------------------------------------------------
// COMMUNITY STATE & DATA: FLIGHT BUDDY NOTICEBOARD
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
    avatar: 'R',
    droneSetup: '5" Freestyle 6S · Betaflight 4.5',
    category: 'Looking for Spotter',
    spot: 'Chroy Changvar Grass Runway',
    dateTime: 'Saturday 6:30 AM',
    message: 'Looking for an experienced spotter while I practice high-speed inverted yaw spins and power loops over soccer posts. Bringing 4 spare LiPos to share!',
    postedAgo: '35 mins ago',
    telegramLink: 'https://t.me/aerobyteacademy'
  },
  {
    id: 2,
    author: 'Sreymom_Wings',
    avatar: 'S',
    droneSetup: 'BetaFPV Cetus X · ELRS 2.4G',
    category: 'Beginners Welcome',
    spot: 'AeroByte Ta Khmau Field',
    dateTime: 'Sunday 8:00 AM',
    message: 'Brand new pilot! I have 25 hours on Liftoff simulator and want a kind mentor to watch my maiden outdoor flight in Angle and Acro mode.',
    postedAgo: '2 hours ago',
    telegramLink: 'https://t.me/aerobyteacademy'
  },
  {
    id: 3,
    author: 'Samnang_FPV',
    avatar: 'S',
    droneSetup: '3.5" Sub-250g Freestyle Quad',
    category: 'Freestyle & Gaps',
    spot: 'Koh Pich Riverside',
    dateTime: 'Friday 5:00 PM (Sunset)',
    message: 'Sunset proximity cruising. Testing new Gemfan 3520 durable triblades. Anyone want to film follow-cam chases together?',
    postedAgo: '4 hours ago',
    telegramLink: 'https://t.me/aerobyteacademy'
  },
  {
    id: 4,
    author: 'Alex_Tech',
    avatar: 'A',
    droneSetup: '7" Long Range Mountain Quad',
    category: 'Ta Khmau Lab',
    spot: 'AeroByte Lab Bench',
    dateTime: 'Saturday 2:00 PM',
    message: 'Flashing ExpressLRS 3.4 dynamic power and testing GPS Rescue telemetry. Welcome anyone who wants to solder together or learn Betaflight blackbox tuning.',
    postedAgo: 'Yesterday',
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
    avatar: newCallout.value.author.charAt(0).toUpperCase(),
    droneSetup: newCallout.value.droneSetup || 'FPV Quad',
    category: newCallout.value.category,
    spot: newCallout.value.spot || 'Phnom Penh Area',
    dateTime: newCallout.value.dateTime || 'This Weekend',
    message: newCallout.value.message,
    postedAgo: 'Just now',
    telegramLink: 'https://t.me/aerobyteacademy'
  })
  showCalloutModal.value = false
  showToast('Flight notice posted to community board!')
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
// THREE.JS 3D DRONE BACKGROUND CANVAS LOGIC
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
    // DARK MODE: Space environment with neon HUD, starfield, and glowing bloom
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
    // LIGHT MODE: Crisp daylight studio lighting, clean alpha transparent background, sharp contrast
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

  // Lighting setup
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

  // World & Drone Hierarchy
  const worldGroup = new THREE.Group()
  scene.add(worldGroup)

  const droneGroup = new THREE.Group()
  worldGroup.add(droneGroup)

  // LOAD REAL DJI FPV 3D DRONE GLB MODEL
  const gltfLoader = new GLTFLoader()
  gltfLoader.load(
    '/models/dji_fpv.glb',
    (gltf) => {
      droneModel = gltf.scene

      // Clean rogue meshes
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

      // Compute bounding box
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

      // Material adjustments
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

      // Extract 4 propellers
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
      console.warn('Real drone model load notice:', err)
      loadingProgress.value = 100
    }
  )

  // Starfield
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

  // Postprocessing: RenderPass, BloomPass, GammaCorrection
  composer = new EffectComposer(renderer)
  composer.addPass(new RenderPass(scene, camera))
  bloomPass = new UnrealBloomPass(new THREE.Vector2(width, height), 0.35, 0.4, 0.1)
  bloomPass.enabled = isDark.value
  composer.addPass(bloomPass)
  composer.addPass(new ShaderPass(GammaCorrectionShader))

  // Scroll Choreography - horizontal flight across the sections
  const STOPS_X = [{ p: 0, v: 0 }, { p: 0.28, v: -2.2 }, { p: 0.58, v: 2.3 }, { p: 1, v: 0 }]
  const STOPS_Y = [{ p: 0, v: -0.4 }, { p: 0.28, v: 0.2 }, { p: 0.58, v: 0.1 }, { p: 1, v: 0.2 }]
  const STOPS_S = [{ p: 0, v: 1.35 }, { p: 0.28, v: 1.05 }, { p: 0.58, v: 0.95 }, { p: 1, v: 1.15 }]
  const STOPS_ROLL = [{ p: 0, v: -0.06 }, { p: 0.28, v: 0.16 }, { p: 0.58, v: -0.18 }, { p: 1, v: 0.04 }]
  const STOPS_PITCH = [{ p: 0, v: 0.22 }, { p: 0.28, v: 0.16 }, { p: 0.58, v: 0.18 }, { p: 1, v: 0.24 }]

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
    curP += (pTarget - curP) * Math.min(1, dt * 4.5)

    const sideScale = Math.max(0.5, Math.min(1, window.innerWidth / 1200))
    const targetX = sample(STOPS_X, curP) * sideScale
    const targetY = sample(STOPS_Y, curP)
    const targetS = sample(STOPS_S, curP)
    const targetRoll = sample(STOPS_ROLL, curP)
    const targetPitch = sample(STOPS_PITCH, curP)

    const k = Math.min(1, dt * 3.2)
    curX += (targetX - curX) * k
    curY += (targetY - curY) * k
    curS += (targetS - curS) * k
    curRoll += (targetRoll - curRoll) * k
    curPitch += (targetPitch - curPitch) * k

    worldGroup.position.set(curX, curY, 0)
    worldGroup.scale.setScalar(curS)

    scrollSpeed *= Math.pow(0.04, dt)
    if (scrollSpeed < 0.04) scrollSpeed = 0

    if (scrollSpeed > 0) {
      propellers.forEach((p) => {
        p.group.rotateOnAxis(p.axis, scrollSpeed * dt * p.dir * 2.5)
      })
    }

    droneGroup.rotation.x = curPitch
    droneGroup.rotation.z = curRoll
    droneGroup.rotation.y = curP * Math.PI * 1.5

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
