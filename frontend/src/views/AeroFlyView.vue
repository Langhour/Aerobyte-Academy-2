<template>
  <div class="aero-fly-root relative isolate min-h-screen transition-colors duration-300 bg-[#f8fafc] dark:bg-[#04060f] text-slate-800 dark:text-[#f3f6ff] overflow-x-hidden selection:bg-orange-500/20 selection:text-orange-600 dark:selection:bg-[#5df0a8]/20 dark:selection:text-[#5df0a8]">
    <!-- Fixed WebGL 3D Real Drone Canvas Behind Everything -->
    <canvas ref="canvasRef" class="fixed inset-0 w-full h-full block z-0 pointer-events-none"></canvas>

    <!-- Loading Indicator overlay while real 3D drone GLB loads -->
    <div
      v-if="loadingProgress < 100"
      class="fixed bottom-6 right-6 z-50 flex items-center gap-3 bg-white/95 dark:bg-[rgba(12,18,38,0.9)] border border-slate-300 dark:border-[rgba(150,175,230,0.2)] px-4 py-2.5 rounded-full backdrop-blur-md shadow-xl text-xs font-bold text-slate-800 dark:text-white transition-opacity duration-500"
      :class="loadingProgress >= 100 ? 'opacity-0 pointer-events-none' : 'opacity-100'"
    >
      <div class="w-4 h-4 border-2 border-orange-500 dark:border-[#5df0a8] border-t-transparent rounded-full animate-spin"></div>
      <span>Loading 3D DJI FPV Drone... {{ loadingProgress }}%</span>
    </div>

    <!-- Page Content Floating Over Fixed 3D Drone -->
    <div class="relative z-10">
      <!-- Aero Fly Top Sub-Navigation Bar -->
      <header class="sticky top-0 z-40 bg-white/85 dark:bg-[#04060f]/85 backdrop-blur-xl border-b border-slate-200 dark:border-[rgba(150,175,230,0.12)] transition-colors duration-300 shadow-2xs">
        <div class="mx-auto max-w-[1180px] px-4 sm:px-6 lg:px-8">
          <div class="flex items-center justify-between py-3.5 gap-4">
            <!-- Brand Mark -->
            <div class="flex items-center gap-2.5">
              <span class="text-orange-500 dark:text-[#5df0a8] text-base font-extrabold select-none">▲</span>
              <span class="text-lg font-black tracking-widest uppercase text-[#0c1e5b] dark:text-white">Aero Fly</span>
              <span class="hidden sm:inline-block text-[10px] font-bold uppercase tracking-wider bg-sky-100 text-sky-700 dark:bg-[#5df0a8]/10 dark:text-[#5df0a8] border border-sky-200 dark:border-[#5df0a8]/20 px-2.5 py-0.5 rounded-full ml-1">
                Real FPV Flight Collective
              </span>
            </div>

            <!-- Page Nav Links -->
            <nav class="hidden md:flex items-center gap-6 text-xs sm:text-sm font-semibold text-slate-600 dark:text-[#9aa6c4]">
              <a href="#features" class="hover:text-[#0c1e5b] dark:hover:text-white transition">Features</a>
              <a href="#telemetry" class="hover:text-[#0c1e5b] dark:hover:text-white transition">Telemetry</a>
              <a href="#events" class="hover:text-[#0c1e5b] dark:hover:text-white transition">Events & Schedule</a>
              <a href="#store" class="hover:text-[#0c1e5b] dark:hover:text-white transition">Aero Store</a>
            </nav>

            <!-- Action Buttons: Theme Toggle & Telegram -->
            <div class="flex items-center gap-3">
              <!-- Quick Theme Toggle Pill Button -->
              <button
                type="button"
                @click="toggleTheme"
                class="inline-flex items-center justify-center p-2 rounded-full border border-slate-300 dark:border-[rgba(150,175,230,0.2)] bg-white/90 dark:bg-white/5 text-slate-800 dark:text-slate-200 hover:scale-105 active:scale-95 transition cursor-pointer shadow-xs"
                :title="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
                aria-label="Toggle Theme"
              >
                <span v-if="isDark" class="text-sm">☀️</span>
                <span v-else class="text-sm">🌙</span>
              </button>

              <a
                href="https://t.me/aerobyteacademy"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center gap-2 rounded-full bg-[#ff6b00] hover:bg-[#e05e00] text-white px-4 py-2 text-xs sm:text-sm font-bold transition shadow-sm active:scale-95 cursor-pointer"
              >
                <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24">
                  <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.121l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.458c.538-.196 1.006.128.832.943z"/>
                </svg>
                <span>Join Telegram</span>
              </a>
            </div>
          </div>
        </div>
      </header>

      <!-- SECTION 1: HERO (The 3D Drone is centered right below the content) -->
      <section class="min-h-[92vh] flex flex-col justify-between items-center text-center px-4 sm:px-6 pt-12 pb-16 relative">
        <div class="max-w-3xl mx-auto space-y-5">
          <div class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-sky-50 dark:bg-[#5df0a8]/10 border border-sky-200 dark:border-[#5df0a8]/20 text-sky-700 dark:text-[#5df0a8] text-xs font-bold tracking-widest uppercase transition-colors">
            <span class="w-2 h-2 rounded-full bg-sky-500 dark:bg-[#5df0a8] animate-pulse"></span>
            Cambodia's Open Drone Flight Community
          </div>

          <h1 class="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] text-[#0c1e5b] dark:text-white transition-colors">
            Fly Smarter,<br>
            Not <span class="bg-gradient-to-b from-sky-600 to-teal-500 dark:from-[#5df0a8] dark:to-[#2fd38a] bg-clip-text text-transparent">Harder</span>
          </h1>

          <p class="text-base sm:text-xl text-slate-600 dark:text-[#9aa6c4] leading-relaxed max-w-2xl mx-auto transition-colors">
            Experience real FPV racing dynamics, connect with solo pilots across Cambodia, and configure custom quads with hands-on bench consulting.
          </p>

          <div class="pt-3 flex flex-col sm:flex-row items-center justify-center gap-4">
            <a
              href="https://t.me/aerobyteacademy"
              target="_blank"
              rel="noopener noreferrer"
              class="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 rounded-full bg-[#ff6b00] hover:bg-[#e05e00] text-white px-8 py-3.5 text-base font-bold shadow-lg shadow-orange-500/25 hover:shadow-orange-500/40 hover:-translate-y-0.5 transition active:scale-95 cursor-pointer"
            >
              <span>Start Flying Right Now</span>
              <svg class="w-4 h-4 stroke-current fill-none stroke-[2.5]" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>

            <a
              href="#events"
              class="w-full sm:w-auto inline-flex items-center justify-center gap-2 rounded-full bg-white dark:bg-white/5 hover:bg-slate-50 dark:hover:bg-white/10 border border-slate-300 dark:border-[rgba(150,175,230,0.22)] px-7 py-3.5 text-base font-bold text-[#0c1e5b] dark:text-white transition hover:-translate-y-0.5 shadow-xs"
            >
              <span>Weekend Flight Schedule</span>
            </a>
          </div>
        </div>

        <!-- Spacer area allowing the 3D drone to hover in full view -->
        <div class="h-32 sm:h-44 pointer-events-none"></div>

        <!-- Trusted Logos Row -->
        <div class="pt-8 border-t border-slate-200/80 dark:border-[rgba(150,175,230,0.08)] w-full max-w-4xl mx-auto transition-colors">
          <p class="text-[11px] font-bold uppercase tracking-widest text-slate-500 dark:text-[#6b7796] mb-4">
            Supported hardware & open-source flight stacks
          </p>
          <div class="flex flex-wrap items-center justify-center gap-6 sm:gap-12 text-sm sm:text-base font-bold text-slate-600 dark:text-[#6b7796]">
            <span class="hover:text-[#0c1e5b] dark:hover:text-white transition">DJI FPV</span>
            <span class="hover:text-[#0c1e5b] dark:hover:text-white transition">Betaflight</span>
            <span class="hover:text-[#0c1e5b] dark:hover:text-white transition">ExpressLRS</span>
            <span class="hover:text-[#0c1e5b] dark:hover:text-white transition">RadioMaster</span>
            <span class="hover:text-[#0c1e5b] dark:hover:text-white transition">Walksnail</span>
            <span class="hover:text-[#0c1e5b] dark:hover:text-white transition">ArduPilot</span>
          </div>
        </div>
      </section>

      <!-- SECTION 2: FEATURES (6 Glassmorphism Cards) -->
      <section id="features" class="py-24 sm:py-32 px-4 sm:px-6 lg:px-8 max-w-[1180px] mx-auto">
        <div class="text-center max-w-2xl mx-auto mb-16">
          <span class="text-xs font-bold uppercase tracking-widest text-sky-600 dark:text-[#5df0a8]">Everything in Orbit</span>
          <h2 class="text-3xl sm:text-5xl font-extrabold text-[#0c1e5b] dark:text-white mt-2 leading-tight transition-colors">
            One collective to power the entire flight journey
          </h2>
          <p class="mt-4 text-base sm:text-lg text-slate-600 dark:text-[#9aa6c4] leading-relaxed transition-colors">
            Stop struggling with mismatched voltages and broken solder joints alone. Aero Fly unifies flight training, telemetry diagnostics, and physical maker spaces.
          </p>
        </div>

        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <!-- Card 1 -->
          <div class="p-7 rounded-[18px] bg-white/80 dark:bg-[rgba(12,18,38,0.55)] border border-slate-200 dark:border-[rgba(150,175,230,0.12)] backdrop-blur-md shadow-sm dark:shadow-none hover:border-sky-400 dark:hover:border-[rgba(150,175,230,0.25)] hover:bg-white dark:hover:bg-[rgba(16,24,48,0.7)] hover:-translate-y-1 transition duration-200">
            <div class="w-11 h-11 rounded-xl bg-sky-50 dark:bg-[#5df0a8]/10 text-sky-600 dark:text-[#5df0a8] border border-sky-100 dark:border-[#5df0a8]/20 flex items-center justify-center text-xl mb-4">
              ⚡
            </div>
            <h3 class="text-lg font-bold text-[#0c1e5b] dark:text-white mb-2 transition-colors">Clever Workflows</h3>
            <p class="text-sm text-slate-600 dark:text-[#9aa6c4] leading-relaxed transition-colors">
              Automate radio bindings, failsafes, and PID profiles with step-by-step verified flight templates that protect your motors.
            </p>
          </div>

          <!-- Card 2 -->
          <div class="p-7 rounded-[18px] bg-white/80 dark:bg-[rgba(12,18,38,0.55)] border border-slate-200 dark:border-[rgba(150,175,230,0.12)] backdrop-blur-md shadow-sm dark:shadow-none hover:border-sky-400 dark:hover:border-[rgba(150,175,230,0.25)] hover:bg-white dark:hover:bg-[rgba(16,24,48,0.7)] hover:-translate-y-1 transition duration-200">
            <div class="w-11 h-11 rounded-xl bg-sky-50 dark:bg-[#5df0a8]/10 text-sky-600 dark:text-[#5df0a8] border border-sky-100 dark:border-[#5df0a8]/20 flex items-center justify-center text-xl mb-4">
              📊
            </div>
            <h3 class="text-lg font-bold text-[#0c1e5b] dark:text-white mb-2 transition-colors">Live Telemetry</h3>
            <p class="text-sm text-slate-600 dark:text-[#9aa6c4] leading-relaxed transition-colors">
              Real-time OSD blackbox logs and gyro frequency graphs pinpoint vibration noise and motor desyncs in milliseconds.
            </p>
          </div>

          <!-- Card 3 -->
          <div class="p-7 rounded-[18px] bg-white/80 dark:bg-[rgba(12,18,38,0.55)] border border-slate-200 dark:border-[rgba(150,175,230,0.12)] backdrop-blur-md shadow-sm dark:shadow-none hover:border-sky-400 dark:hover:border-[rgba(150,175,230,0.25)] hover:bg-white dark:hover:bg-[rgba(16,24,48,0.7)] hover:-translate-y-1 transition duration-200">
            <div class="w-11 h-11 rounded-xl bg-sky-50 dark:bg-[#5df0a8]/10 text-sky-600 dark:text-[#5df0a8] border border-sky-100 dark:border-[#5df0a8]/20 flex items-center justify-center text-xl mb-4">
              👥
            </div>
            <h3 class="text-lg font-bold text-[#0c1e5b] dark:text-white mb-2 transition-colors">Seamless Pilot Wings</h3>
            <p class="text-sm text-slate-600 dark:text-[#9aa6c4] leading-relaxed transition-colors">
              Never fly solo again. Connect with local spotters, co-pilots, and freestyle racers across Phnom Penh and Ta Khmau.
            </p>
          </div>

          <!-- Card 4 -->
          <div class="p-7 rounded-[18px] bg-white/80 dark:bg-[rgba(12,18,38,0.55)] border border-slate-200 dark:border-[rgba(150,175,230,0.12)] backdrop-blur-md shadow-sm dark:shadow-none hover:border-sky-400 dark:hover:border-[rgba(150,175,230,0.25)] hover:bg-white dark:hover:bg-[rgba(16,24,48,0.7)] hover:-translate-y-1 transition duration-200">
            <div class="w-11 h-11 rounded-xl bg-sky-50 dark:bg-[#5df0a8]/10 text-sky-600 dark:text-[#5df0a8] border border-sky-100 dark:border-[#5df0a8]/20 flex items-center justify-center text-xl mb-4">
              📡
            </div>
            <h3 class="text-lg font-bold text-[#0c1e5b] dark:text-white mb-2 transition-colors">Instant ELRS Triggers</h3>
            <p class="text-sm text-slate-600 dark:text-[#9aa6c4] leading-relaxed transition-colors">
              Sub-millisecond packet rates at 1000Hz. Ultra-low latency transmission that translates thumb twitches straight to motor RPM.
            </p>
          </div>

          <!-- Card 5 -->
          <div class="p-7 rounded-[18px] bg-white/80 dark:bg-[rgba(12,18,38,0.55)] border border-slate-200 dark:border-[rgba(150,175,230,0.12)] backdrop-blur-md shadow-sm dark:shadow-none hover:border-sky-400 dark:hover:border-[rgba(150,175,230,0.25)] hover:bg-white dark:hover:bg-[rgba(16,24,48,0.7)] hover:-translate-y-1 transition duration-200">
            <div class="w-11 h-11 rounded-xl bg-sky-50 dark:bg-[#5df0a8]/10 text-sky-600 dark:text-[#5df0a8] border border-sky-100 dark:border-[#5df0a8]/20 flex items-center justify-center text-xl mb-4">
              🛠️
            </div>
            <h3 class="text-lg font-bold text-[#0c1e5b] dark:text-white mb-2 transition-colors">Ta Khmau Maker Hub</h3>
            <p class="text-sm text-slate-600 dark:text-[#9aa6c4] leading-relaxed transition-colors">
              100% free physical workshop with soldering irons, smoke stoppers, and multimeters open daily for tuning and repairs.
            </p>
          </div>

          <!-- Card 6 -->
          <div class="p-7 rounded-[18px] bg-white/80 dark:bg-[rgba(12,18,38,0.55)] border border-slate-200 dark:border-[rgba(150,175,230,0.12)] backdrop-blur-md shadow-sm dark:shadow-none hover:border-sky-400 dark:hover:border-[rgba(150,175,230,0.25)] hover:bg-white dark:hover:bg-[rgba(16,24,48,0.7)] hover:-translate-y-1 transition duration-200">
            <div class="w-11 h-11 rounded-xl bg-sky-50 dark:bg-[#5df0a8]/10 text-sky-600 dark:text-[#5df0a8] border border-sky-100 dark:border-[#5df0a8]/20 flex items-center justify-center text-xl mb-4">
              🛸
            </div>
            <h3 class="text-lg font-bold text-[#0c1e5b] dark:text-white mb-2 transition-colors">Custom Drone Sourcing</h3>
            <p class="text-sm text-slate-600 dark:text-[#9aa6c4] leading-relaxed transition-colors">
              We don't just sell parts; we consult. Get genuine frames, stacks, and motors specifically matched to your flight goals.
            </p>
          </div>
        </div>
      </section>

      <!-- SECTION 3: SHOWCASE & TELEMETRY MOCK -->
      <section id="telemetry" class="py-20 px-4 sm:px-6 lg:px-8 max-w-[1180px] mx-auto">
        <div class="grid lg:grid-cols-12 gap-12 items-center">
          <!-- Left Text -->
          <div class="lg:col-span-5 space-y-5 text-left">
            <span class="text-xs font-bold uppercase tracking-widest text-sky-600 dark:text-[#5df0a8]">Built for Momentum</span>
            <h2 class="text-3xl sm:text-5xl font-extrabold text-[#0c1e5b] dark:text-white leading-tight transition-colors">
              See the whole flight envelope move in real time
            </h2>
            <p class="text-base text-slate-600 dark:text-[#9aa6c4] leading-relaxed transition-colors">
              Every cell voltage, RSSI dBm level, motor temperature, and throttle response — rendered live. Aero Fly gives operators the altitude to fly with total confidence.
            </p>
            <div class="pt-2">
              <a
                href="https://t.me/aerobyteacademy"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center gap-2 rounded-full bg-[#ff6b00] hover:bg-[#e05e00] text-white px-7 py-3 text-sm font-bold shadow-md hover:shadow-lg transition cursor-pointer"
              >
                <span>Explore Live Telemetry</span>
                <span class="text-xs font-black">→</span>
              </a>
            </div>
          </div>

          <!-- Right Dashboard Mockup -->
          <div class="lg:col-span-7">
            <div class="p-6 sm:p-7 rounded-[26px] bg-white/90 dark:bg-[rgba(16,24,48,0.75)] border border-slate-200 dark:border-[rgba(150,175,230,0.22)] shadow-xl dark:shadow-2xl backdrop-blur-xl space-y-6 transition-colors">
              <div class="flex items-center justify-between border-b border-slate-200 dark:border-[rgba(150,175,230,0.12)] pb-4">
                <span class="text-sm font-bold text-[#0c1e5b] dark:text-white">Flight Telemetry · Quads 6S</span>
                <span class="inline-flex items-center gap-1.5 text-xs font-bold text-emerald-600 dark:text-[#5df0a8] uppercase tracking-wider">
                  <span class="w-2 h-2 rounded-full bg-emerald-500 dark:bg-[#5df0a8] animate-ping"></span>
                  Live Link
                </span>
              </div>

              <!-- Animated Bars -->
              <div class="flex items-end gap-2.5 h-36 p-4 rounded-xl bg-slate-100/90 dark:bg-black/30 border border-slate-200 dark:border-[rgba(150,175,230,0.12)] transition-colors">
                <div class="flex-1 bg-gradient-to-t from-sky-400 to-sky-600 dark:from-[rgba(47,211,138,0.2)] dark:to-[#5df0a8] rounded-t-md transition-all duration-700" style="height: 62%"></div>
                <div class="flex-1 bg-gradient-to-t from-sky-400 to-sky-600 dark:from-[rgba(47,211,138,0.2)] dark:to-[#5df0a8] rounded-t-md transition-all duration-700" style="height: 88%"></div>
                <div class="flex-1 bg-gradient-to-t from-sky-400 to-sky-600 dark:from-[rgba(47,211,138,0.2)] dark:to-[#5df0a8] rounded-t-md transition-all duration-700" style="height: 47%"></div>
                <div class="flex-1 bg-gradient-to-t from-sky-400 to-sky-600 dark:from-[rgba(47,211,138,0.2)] dark:to-[#5df0a8] rounded-t-md transition-all duration-700" style="height: 95%"></div>
                <div class="flex-1 bg-gradient-to-t from-sky-400 to-sky-600 dark:from-[rgba(47,211,138,0.2)] dark:to-[#5df0a8] rounded-t-md transition-all duration-700" style="height: 71%"></div>
                <div class="flex-1 bg-gradient-to-t from-sky-400 to-sky-600 dark:from-[rgba(47,211,138,0.2)] dark:to-[#5df0a8] rounded-t-md transition-all duration-700" style="height: 80%"></div>
                <div class="flex-1 bg-gradient-to-t from-sky-400 to-sky-600 dark:from-[rgba(47,211,138,0.2)] dark:to-[#5df0a8] rounded-t-md transition-all duration-700" style="height: 58%"></div>
              </div>

              <!-- Telemetry Metrics Rows -->
              <div class="space-y-3 text-xs font-semibold text-slate-600 dark:text-[#9aa6c4]">
                <div class="flex items-center gap-4">
                  <span class="w-32 text-left">ELRS Signal Link</span>
                  <div class="flex-1 h-2 rounded-full bg-slate-200 dark:bg-white/5 overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-teal-500 to-emerald-500 dark:from-[#2fd38a] dark:to-[#5df0a8] rounded-full" style="width: 90%"></div>
                  </div>
                  <span class="text-slate-800 dark:text-white w-10 text-right">90%</span>
                </div>

                <div class="flex items-center gap-4">
                  <span class="w-32 text-left">Battery 6S Pack</span>
                  <div class="flex-1 h-2 rounded-full bg-slate-200 dark:bg-white/5 overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-teal-500 to-emerald-500 dark:from-[#2fd38a] dark:to-[#5df0a8] rounded-full" style="width: 72%"></div>
                  </div>
                  <span class="text-slate-800 dark:text-white w-10 text-right">72%</span>
                </div>

                <div class="flex items-center gap-4">
                  <span class="w-32 text-left">VTX Transmission</span>
                  <div class="flex-1 h-2 rounded-full bg-slate-200 dark:bg-white/5 overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-teal-500 to-emerald-500 dark:from-[#2fd38a] dark:to-[#5df0a8] rounded-full" style="width: 48%"></div>
                  </div>
                  <span class="text-slate-800 dark:text-white w-10 text-right">48%</span>
                </div>

                <div class="flex items-center gap-4">
                  <span class="w-32 text-left">GPS Satellites</span>
                  <div class="flex-1 h-2 rounded-full bg-slate-200 dark:bg-white/5 overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-teal-500 to-emerald-500 dark:from-[#2fd38a] dark:to-[#5df0a8] rounded-full" style="width: 34%"></div>
                  </div>
                  <span class="text-slate-800 dark:text-white w-10 text-right">18 Sats</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 4 Stats Cards -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-16">
          <div class="p-6 rounded-[18px] bg-white/80 dark:bg-[rgba(12,18,38,0.55)] border border-slate-200 dark:border-[rgba(150,175,230,0.12)] text-center backdrop-blur-md shadow-xs dark:shadow-none transition-colors">
            <div class="text-3xl sm:text-4xl font-extrabold bg-gradient-to-b from-[#0c1e5b] to-sky-600 dark:from-white dark:to-[#5df0a8] bg-clip-text text-transparent">3.4×</div>
            <p class="text-xs sm:text-sm text-slate-600 dark:text-[#9aa6c4] mt-2">Faster pilot skill progression</p>
          </div>
          <div class="p-6 rounded-[18px] bg-white/80 dark:bg-[rgba(12,18,38,0.55)] border border-slate-200 dark:border-[rgba(150,175,230,0.12)] text-center backdrop-blur-md shadow-xs dark:shadow-none transition-colors">
            <div class="text-3xl sm:text-4xl font-extrabold bg-gradient-to-b from-[#0c1e5b] to-sky-600 dark:from-white dark:to-[#5df0a8] bg-clip-text text-transparent">99.8%</div>
            <p class="text-xs sm:text-sm text-slate-600 dark:text-[#9aa6c4] mt-2">Radio link reliability on ELRS</p>
          </div>
          <div class="p-6 rounded-[18px] bg-white/80 dark:bg-[rgba(12,18,38,0.55)] border border-slate-200 dark:border-[rgba(150,175,230,0.12)] text-center backdrop-blur-md shadow-xs dark:shadow-none transition-colors">
            <div class="text-3xl sm:text-4xl font-extrabold bg-gradient-to-b from-[#0c1e5b] to-sky-600 dark:from-white dark:to-[#5df0a8] bg-clip-text text-transparent">1,200+</div>
            <p class="text-xs sm:text-sm text-slate-600 dark:text-[#9aa6c4] mt-2">Flights logged in Cambodia</p>
          </div>
          <div class="p-6 rounded-[18px] bg-white/80 dark:bg-[rgba(12,18,38,0.55)] border border-slate-200 dark:border-[rgba(150,175,230,0.12)] text-center backdrop-blur-md shadow-xs dark:shadow-none transition-colors">
            <div class="text-3xl sm:text-4xl font-extrabold bg-gradient-to-b from-[#0c1e5b] to-sky-600 dark:from-white dark:to-[#5df0a8] bg-clip-text text-transparent">100%</div>
            <p class="text-xs sm:text-sm text-slate-600 dark:text-[#9aa6c4] mt-2">Free Ta Khmau Hub access</p>
          </div>
        </div>
      </section>

      <!-- SECTION 4: EVENTS & TA KHMAU LOCATION -->
      <section id="events" class="py-20 px-4 sm:px-6 lg:px-8 max-w-[1180px] mx-auto">
        <div class="p-8 sm:p-12 rounded-[26px] bg-gradient-to-b from-white/95 to-slate-50/90 dark:from-[rgba(16,24,48,0.85)] dark:to-[rgba(12,18,38,0.9)] border border-slate-200 dark:border-[rgba(150,175,230,0.22)] shadow-xl dark:shadow-2xl backdrop-blur-xl transition-colors">
          <div class="max-w-2xl text-left space-y-4">
            <span class="text-xs font-bold uppercase tracking-widest text-[#ff6b00]">Events & Weekend Schedule</span>
            <h2 class="text-3xl sm:text-5xl font-extrabold text-[#0c1e5b] dark:text-white transition-colors">
              Weekend Flying Gatherings & Ta Khmau Location
            </h2>
            <p class="text-sm sm:text-base text-slate-600 dark:text-[#9aa6c4] leading-relaxed transition-colors">
              Outdoor flying sessions take place on <strong>Saturdays or Sundays</strong>, but please note that <strong>they do NOT happen every week</strong> due to weather conditions. Timetables are confirmed via Thursday polls on Telegram.
            </p>
          </div>

          <div class="grid md:grid-cols-2 gap-6 mt-8">
            <!-- Event Rules -->
            <div class="p-6 rounded-2xl bg-white/80 dark:bg-white/5 border border-slate-200 dark:border-[rgba(150,175,230,0.12)] text-left space-y-3 shadow-xs dark:shadow-none transition-colors">
              <h4 class="text-base font-bold text-sky-700 dark:text-[#5df0a8]">Weekend Flight Notice</h4>
              <p class="text-xs sm:text-sm text-slate-600 dark:text-[#9aa6c4] leading-relaxed transition-colors">
                Weather (wind under 20km/h, zero rain) dictates when we fly. Join the group to reserve your VTX Raceband frequency and get the GPS coordinates for this weekend.
              </p>
              <a
                href="https://t.me/aerobyteacademy"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center gap-2 text-xs font-bold text-[#ff6b00] hover:underline pt-2 cursor-pointer"
              >
                <span>View This Week's Poll on Telegram</span>
                <span>→</span>
              </a>
            </div>

            <!-- Ta Khmau Hub Details -->
            <div class="p-6 rounded-2xl bg-white/80 dark:bg-white/5 border border-slate-200 dark:border-[rgba(150,175,230,0.12)] text-left space-y-3 shadow-xs dark:shadow-none transition-colors">
              <h4 class="text-base font-bold text-[#0c1e5b] dark:text-white">📍 Free Physical Ta Khmau Space</h4>
              <p class="text-xs sm:text-sm text-slate-600 dark:text-[#9aa6c4] leading-relaxed transition-colors">
                Open Tuesday – Sunday (9 AM – 6 PM). Drop in anytime to solder parts, test ESC stacks, configure Betaflight, or talk with fellow drone makers.
              </p>
              <a
                href="https://maps.google.com/?q=Ta+Khmau+Cambodia"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center gap-2 text-xs font-bold text-sky-600 dark:text-[#5df0a8] hover:underline pt-2 cursor-pointer"
              >
                <span>Open Google Maps Directions</span>
                <span>→</span>
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- SECTION 5: AERO STORE & FINAL CTA -->
      <section id="store" class="py-20 px-4 sm:px-6 lg:px-8 max-w-[1180px] mx-auto text-center">
        <div class="p-10 sm:p-16 rounded-[26px] bg-gradient-to-b from-sky-50 via-white to-slate-50 dark:from-[#5df0a8]/10 dark:via-[rgba(16,24,48,0.7)] dark:to-[rgba(12,18,38,0.85)] border border-slate-200 dark:border-[rgba(150,175,230,0.22)] shadow-xl dark:shadow-2xl backdrop-blur-2xl max-w-3xl mx-auto space-y-6 transition-colors">
          <span class="text-xs font-bold uppercase tracking-widest text-sky-600 dark:text-[#5df0a8]">Ready When You Are</span>
          <h2 class="text-3xl sm:text-5xl font-extrabold text-[#0c1e5b] dark:text-white leading-tight transition-colors">
            Put your flight journey on a new trajectory
          </h2>
          <p class="text-base text-slate-600 dark:text-[#9aa6c4] leading-relaxed transition-colors">
            Need custom drone parts, a complete hand-soldered BNF quad, or pre-purchase hardware advice? We consult before you buy.
          </p>

          <div class="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3.5">
            <a
              href="https://t.me/aerobyteacademy"
              target="_blank"
              rel="noopener noreferrer"
              class="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 rounded-full bg-[#ff6b00] hover:bg-[#e05e00] text-white px-8 py-3.5 text-base font-bold shadow-lg shadow-orange-500/25 hover:shadow-orange-500/40 transition active:scale-95 cursor-pointer"
            >
              <span>Join Aero Fly Telegram</span>
              <svg class="w-4 h-4 stroke-current fill-none stroke-[2.5]" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>

            <a
              href="https://t.me/aerobyteacademy"
              target="_blank"
              rel="noopener noreferrer"
              class="w-full sm:w-auto inline-flex items-center justify-center gap-2 rounded-full bg-white dark:bg-white/5 hover:bg-slate-50 dark:hover:bg-white/10 border border-slate-300 dark:border-[rgba(150,175,230,0.22)] px-7 py-3.5 text-base font-bold text-[#0c1e5b] dark:text-white transition cursor-pointer shadow-xs"
            >
              <span>Request Custom Build Quote</span>
            </a>
          </div>
        </div>

        <p class="mt-16 text-xs text-slate-500 dark:text-[#6b7796] transition-colors">
          © {{ currentYear }} Aero Fly — Built among the skies.
        </p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js'
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js'
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js'
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass.js'
import { GammaCorrectionShader } from 'three/examples/jsm/shaders/GammaCorrectionShader.js'
import { useTheme } from '../composables/useTheme'

const { isDark, toggleTheme } = useTheme()

const canvasRef = ref(null)
const loadingProgress = ref(0)
const currentYear = new Date().getFullYear()

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
    // Disable bloom pass completely in light mode to prevent white wash out
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
  scene.background = null // Transparent background handled by CSS

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

      // 1. Remove rogue meshes defense
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

      // 2. Drone natural flight orientation:
      // The model is already correctly oriented with +Y as UP and +Z as FRONT (camera facing viewer).
      // We keep rotation at (0, 0, 0) so the 4 arms lie flat in the horizontal flight plane!
      droneModel.rotation.set(0, 0, 0)
      droneModel.updateMatrixWorld(true)

      // 3. Compute clean bounding box of the real drone
      const box = new THREE.Box3().setFromObject(droneModel)
      const size = box.getSize(new THREE.Vector3())
      const maxDim = Math.max(size.x, size.y, size.z)

      // Prominent scale: 3.5 units wide
      const targetScale = 3.5 / (maxDim || 1)
      droneModel.scale.setScalar(targetScale)
      droneModel.updateMatrixWorld(true)

      // 4. Center the scaled drone precisely at (0, 0, 0)
      const scaledBox = new THREE.Box3().setFromObject(droneModel)
      const center = scaledBox.getCenter(new THREE.Vector3())
      droneModel.position.x = -center.x
      droneModel.position.y = -center.y
      droneModel.position.z = -center.z

      // 5. Enhance materials for crisp, high-contrast visibility in BOTH light and dark modes
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

      // 6. Extract the 4 authentic real propellers from SpineB (the rotor assembly containing the carbon tri-blades, purple tips, and center nuts)
      // IMPORTANT: Drone arms and frame (Cube.178, Cube.183, Object_16..20, Object_44..47) remain 100% STATIC and untouched!
      let spineNode = null
      droneModel.traverse((c) => {
        if (c.name && c.name.includes('SpineB')) spineNode = c
      })

      propellers.length = 0

      if (spineNode && spineNode.parent) {
        // True 4 Propeller coordinates & motor normal spin axis in SpineB local space
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
        spineNode.traverse((c) => {
          if (c.isMesh && c.geometry) origMeshes.push(c)
        })

        origMeshes.forEach((c) => {
          const geom = c.geometry
          const pos = geom.attributes.position
          const idx = geom.index
          if (idx && pos) {
            const kept = [[], [], [], []]
            for (let i = 0; i < idx.count; i += 3) {
              const a = idx.getX(i)
              const b = idx.getX(i + 1)
              const c_idx = idx.getX(i + 2)

              const avgX = (pos.getX(a) + pos.getX(b) + pos.getX(c_idx)) / 3
              const avgY = (pos.getY(a) + pos.getY(b) + pos.getY(c_idx)) / 3
              const avgZ = (pos.getZ(a) + pos.getZ(b) + pos.getZ(c_idx)) / 3

              let bestK = 0
              let bestD = Infinity
              for (let k = 0; k < 4; k++) {
                const cfg = propConfigs[k]
                const dx = avgX - cfg.center.x
                const dy = avgY - cfg.center.y
                const dz = avgZ - cfg.center.z
                const d = dx * dx + dy * dy + dz * dz
                if (d < bestD) {
                  bestD = d
                  bestK = k
                }
              }
              kept[bestK].push(a, b, c_idx)
            }

            for (let k = 0; k < 4; k++) {
              if (kept[k].length > 0) {
                const subGeom = extractSubGeometry(geom, kept[k], propConfigs[k].center)
                const newMesh = new THREE.Mesh(subGeom, c.material)
                newMesh.castShadow = true
                newMesh.receiveShadow = true
                propGroups[k].add(newMesh)
              }
            }
          }
        })

        // Hide the original un-split meshes inside spineNode
        origMeshes.forEach((m) => {
          m.visible = false
        })

        // Add the 4 isolated rotating propeller groups directly inside spineNode
        // so they inherit spineNode's exact position, scale, and orientation on the drone arms
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

  // Scroll Choreography - drone in horizontal flight with natural forward flight pitch
  const STOPS_X = [{ p: 0, v: 0 }, { p: 0.32, v: -2.4 }, { p: 0.64, v: 2.5 }, { p: 1, v: 0 }]
  const STOPS_Y = [{ p: 0, v: -0.4 }, { p: 0.32, v: 0.2 }, { p: 0.64, v: 0.1 }, { p: 1, v: 0.2 }]
  const STOPS_S = [{ p: 0, v: 1.35 }, { p: 0.32, v: 1.05 }, { p: 0.64, v: 0.95 }, { p: 1, v: 1.15 }]
  const STOPS_ROLL = [{ p: 0, v: -0.06 }, { p: 0.32, v: 0.16 }, { p: 0.64, v: -0.18 }, { p: 1, v: 0.04 }]
  const STOPS_PITCH = [{ p: 0, v: 0.22 }, { p: 0.32, v: 0.16 }, { p: 0.64, v: 0.18 }, { p: 1, v: 0.24 }]

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

  // Apply initial theme state
  applySceneTheme(isDark.value)

  // Track scroll velocity: faster scroll = faster propeller spin, slow scroll = slow, no scroll = 0 spin
  lastScrollPos = window.pageYOffset || document.documentElement.scrollTop
  scrollSpeed = 0

  function onScroll() {
    const curScroll = window.pageYOffset || document.documentElement.scrollTop
    const delta = Math.abs(curScroll - lastScrollPos)
    lastScrollPos = curScroll
    // Velocity directly proportional to scroll distance
    scrollSpeed = Math.max(scrollSpeed, Math.min(delta * 0.95, 55.0))
  }

  window.addEventListener('scroll', onScroll, { passive: true })

  function animate() {
    animationFrameId = requestAnimationFrame(animate)
    const now = performance.now()
    const dt = Math.min((now - lastTime) / 1000, 0.05)
    lastTime = now

    // Scroll progress
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

    // Smooth decay of scroll speed towards 0
    scrollSpeed *= Math.pow(0.04, dt)
    if (scrollSpeed < 0.04) scrollSpeed = 0

    // Spin propellers strictly according to scroll speed:
    // If not scrolling, scrollSpeed is 0 -> propellers do NOT move!
    if (scrollSpeed > 0) {
      propellers.forEach((p) => {
        p.group.rotateOnAxis(p.axis, scrollSpeed * dt * p.dir * 2.5)
      })
    }

    // Drone orientation: locked strictly to scroll position, NO continuous auto-rotation around!
    droneGroup.rotation.x = curPitch
    droneGroup.rotation.z = curRoll
    droneGroup.rotation.y = curP * Math.PI * 1.5

    // If bloom is disabled in light mode, direct renderer.render produces pristine output without buffer artifacts
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
