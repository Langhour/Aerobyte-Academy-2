<template>
  <div class="aero-fly-root relative isolate min-h-screen text-[#f3f6ff] bg-[#04060f] overflow-x-hidden selection:bg-[#5df0a8]/20 selection:text-[#5df0a8]">
    <!-- Fixed WebGL 3D Real Drone Canvas Behind Everything -->
    <canvas ref="canvasRef" class="fixed inset-0 w-full h-full block z-0 pointer-events-none"></canvas>

    <!-- Loading Indicator overlay while real 3D drone GLB loads -->
    <div
      v-if="loadingProgress < 100"
      class="fixed bottom-6 right-6 z-50 flex items-center gap-3 bg-[rgba(12,18,38,0.85)] border border-[rgba(150,175,230,0.2)] px-4 py-2.5 rounded-full backdrop-blur-md shadow-xl text-xs font-bold text-white transition-opacity duration-500"
      :class="loadingProgress >= 100 ? 'opacity-0 pointer-events-none' : 'opacity-100'"
    >
      <div class="w-4 h-4 border-2 border-[#5df0a8] border-t-transparent rounded-full animate-spin"></div>
      <span>Loading Real DJI FPV 3D Drone... {{ loadingProgress }}%</span>
    </div>

    <!-- Page Content Floating Over Fixed 3D Drone -->
    <div class="relative z-10">
      <!-- Aero Fly Top Sub-Navigation Bar -->
      <header class="sticky top-0 z-40 bg-[#04060f]/80 backdrop-blur-xl border-b border-[rgba(150,175,230,0.12)]">
        <div class="mx-auto max-w-[1180px] px-4 sm:px-6 lg:px-8">
          <div class="flex items-center justify-between py-3.5 gap-4">
            <!-- Brand Mark -->
            <div class="flex items-center gap-2.5">
              <span class="text-[#5df0a8] text-base font-extrabold select-none">▲</span>
              <span class="text-lg font-black tracking-widest uppercase text-white">Aero Fly</span>
              <span class="hidden sm:inline-block text-[10px] font-bold uppercase tracking-wider bg-[#5df0a8]/10 text-[#5df0a8] border border-[#5df0a8]/20 px-2 py-0.5 rounded-full ml-1">
                Real FPV Quad Flight Lab
              </span>
            </div>

            <!-- Page Nav Links -->
            <nav class="hidden md:flex items-center gap-6 text-xs sm:text-sm font-semibold text-[#9aa6c4]">
              <a href="#features" class="hover:text-white transition">Features</a>
              <a href="#telemetry" class="hover:text-white transition">Telemetry</a>
              <a href="#events" class="hover:text-white transition">Events & Schedule</a>
              <a href="#store" class="hover:text-white transition">Aero Store</a>
            </nav>

            <!-- Telegram CTA -->
            <a
              href="https://t.me/aerobyteacademy"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex items-center gap-2 rounded-full bg-white/5 hover:bg-white/10 border border-[rgba(150,175,230,0.22)] px-4 py-2 text-xs sm:text-sm font-bold text-white transition active:scale-95"
            >
              <svg class="w-4 h-4 fill-[#5df0a8]" viewBox="0 0 24 24">
                <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.121l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.458c.538-.196 1.006.128.832.943z"/>
              </svg>
              <span>Join Telegram</span>
            </a>
          </div>
        </div>
      </header>

      <!-- SECTION 1: HERO (Floating over the Real 3D Drone) -->
      <section class="min-h-[92vh] flex flex-col justify-center items-center text-center px-4 sm:px-6 pt-12 pb-20 relative">
        <div class="max-w-3xl mx-auto space-y-6">
          <div class="inline-flex items-center gap-2 px-3.5 py-1 rounded-full bg-[#5df0a8]/10 border border-[#5df0a8]/20 text-[#5df0a8] text-xs font-bold tracking-widest uppercase">
            <span class="w-2 h-2 rounded-full bg-[#5df0a8] animate-pulse"></span>
            Cambodia's Real Drone Flight Community
          </div>

          <h1 class="text-4xl sm:text-6xl lg:text-7xl font-extrabold tracking-tight leading-[1.05] text-white">
            Fly Smarter,<br>
            Not <span class="bg-gradient-to-b from-[#5df0a8] to-[#2fd38a] bg-clip-text text-transparent">Harder</span>
          </h1>

          <p class="text-base sm:text-xl text-[#9aa6c4] leading-relaxed max-w-2xl mx-auto">
            Experience real FPV racing dynamics, connect with solo pilots across Cambodia, and configure custom quads with hands-on bench consulting.
          </p>

          <div class="pt-4 flex flex-col sm:flex-row items-center justify-center gap-4">
            <a
              href="https://t.me/aerobyteacademy"
              target="_blank"
              rel="noopener noreferrer"
              class="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 rounded-full bg-gradient-to-b from-[#5df0a8] to-[#2fd38a] text-[#032018] px-8 py-3.5 text-base font-bold shadow-lg shadow-[#5df0a8]/25 hover:shadow-[#5df0a8]/40 hover:-translate-y-0.5 transition active:scale-95"
            >
              <span>Start Flying Right Now</span>
              <svg class="w-4 h-4 stroke-current fill-none stroke-[2.5]" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>

            <a
              href="#events"
              class="w-full sm:w-auto inline-flex items-center justify-center gap-2 rounded-full bg-white/5 hover:bg-white/10 border border-[rgba(150,175,230,0.22)] px-7 py-3.5 text-base font-bold text-white transition hover:-translate-y-0.5"
            >
              <span>Weekend Flight Schedule</span>
            </a>
          </div>
        </div>

        <!-- Trusted Logos Row -->
        <div class="mt-20 pt-10 border-t border-[rgba(150,175,230,0.08)] w-full max-w-4xl mx-auto">
          <p class="text-[11px] font-bold uppercase tracking-widest text-[#6b7796] mb-5">
            Supported hardware & open-source flight stacks
          </p>
          <div class="flex flex-wrap items-center justify-center gap-6 sm:gap-12 text-sm sm:text-base font-bold text-[#6b7796]">
            <span class="hover:text-white transition">DJI FPV</span>
            <span class="hover:text-white transition">Betaflight</span>
            <span class="hover:text-white transition">ExpressLRS</span>
            <span class="hover:text-white transition">RadioMaster</span>
            <span class="hover:text-white transition">Walksnail</span>
            <span class="hover:text-white transition">ArduPilot</span>
          </div>
        </div>
      </section>

      <!-- SECTION 2: FEATURES (6 Glassmorphism Cards) -->
      <section id="features" class="py-24 sm:py-32 px-4 sm:px-6 lg:px-8 max-w-[1180px] mx-auto">
        <div class="text-center max-w-2xl mx-auto mb-16">
          <span class="text-xs font-bold uppercase tracking-widest text-[#5df0a8]">Everything in Orbit</span>
          <h2 class="text-3xl sm:text-5xl font-extrabold text-white mt-2 leading-tight">
            One collective to power the entire flight journey
          </h2>
          <p class="mt-4 text-base sm:text-lg text-[#9aa6c4] leading-relaxed">
            Stop struggling with mismatched voltages and broken solder joints alone. Aero Fly unifies flight training, telemetry diagnostics, and physical maker spaces.
          </p>
        </div>

        <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
          <!-- Card 1 -->
          <div class="p-7 rounded-[18px] bg-[rgba(12,18,38,0.55)] border border-[rgba(150,175,230,0.12)] backdrop-blur-md hover:border-[rgba(150,175,230,0.25)] hover:bg-[rgba(16,24,48,0.7)] hover:-translate-y-1 transition duration-200">
            <div class="w-11 h-11 rounded-xl bg-[#5df0a8]/10 text-[#5df0a8] border border-[#5df0a8]/20 flex items-center justify-center text-xl mb-4">
              ⚡
            </div>
            <h3 class="text-lg font-bold text-white mb-2">Clever Workflows</h3>
            <p class="text-sm text-[#9aa6c4] leading-relaxed">
              Automate radio bindings, failsafes, and PID profiles with step-by-step verified flight templates that protect your motors.
            </p>
          </div>

          <!-- Card 2 -->
          <div class="p-7 rounded-[18px] bg-[rgba(12,18,38,0.55)] border border-[rgba(150,175,230,0.12)] backdrop-blur-md hover:border-[rgba(150,175,230,0.25)] hover:bg-[rgba(16,24,48,0.7)] hover:-translate-y-1 transition duration-200">
            <div class="w-11 h-11 rounded-xl bg-[#5df0a8]/10 text-[#5df0a8] border border-[#5df0a8]/20 flex items-center justify-center text-xl mb-4">
              📊
            </div>
            <h3 class="text-lg font-bold text-white mb-2">Live Telemetry</h3>
            <p class="text-sm text-[#9aa6c4] leading-relaxed">
              Real-time OSD blackbox logs and gyro frequency graphs pinpoint vibration noise and motor desyncs in milliseconds.
            </p>
          </div>

          <!-- Card 3 -->
          <div class="p-7 rounded-[18px] bg-[rgba(12,18,38,0.55)] border border-[rgba(150,175,230,0.12)] backdrop-blur-md hover:border-[rgba(150,175,230,0.25)] hover:bg-[rgba(16,24,48,0.7)] hover:-translate-y-1 transition duration-200">
            <div class="w-11 h-11 rounded-xl bg-[#5df0a8]/10 text-[#5df0a8] border border-[#5df0a8]/20 flex items-center justify-center text-xl mb-4">
              👥
            </div>
            <h3 class="text-lg font-bold text-white mb-2">Seamless Pilot Wings</h3>
            <p class="text-sm text-[#9aa6c4] leading-relaxed">
              Never fly solo again. Connect with local spotters, co-pilots, and freestyle racers across Phnom Penh and Ta Khmau.
            </p>
          </div>

          <!-- Card 4 -->
          <div class="p-7 rounded-[18px] bg-[rgba(12,18,38,0.55)] border border-[rgba(150,175,230,0.12)] backdrop-blur-md hover:border-[rgba(150,175,230,0.25)] hover:bg-[rgba(16,24,48,0.7)] hover:-translate-y-1 transition duration-200">
            <div class="w-11 h-11 rounded-xl bg-[#5df0a8]/10 text-[#5df0a8] border border-[#5df0a8]/20 flex items-center justify-center text-xl mb-4">
              📡
            </div>
            <h3 class="text-lg font-bold text-white mb-2">Instant ELRS Triggers</h3>
            <p class="text-sm text-[#9aa6c4] leading-relaxed">
              Sub-millisecond packet rates at 1000Hz. Ultra-low latency transmission that translates thumb twitches straight to motor RPM.
            </p>
          </div>

          <!-- Card 5 -->
          <div class="p-7 rounded-[18px] bg-[rgba(12,18,38,0.55)] border border-[rgba(150,175,230,0.12)] backdrop-blur-md hover:border-[rgba(150,175,230,0.25)] hover:bg-[rgba(16,24,48,0.7)] hover:-translate-y-1 transition duration-200">
            <div class="w-11 h-11 rounded-xl bg-[#5df0a8]/10 text-[#5df0a8] border border-[#5df0a8]/20 flex items-center justify-center text-xl mb-4">
              🛠️
            </div>
            <h3 class="text-lg font-bold text-white mb-2">Ta Khmau Maker Hub</h3>
            <p class="text-sm text-[#9aa6c4] leading-relaxed">
              100% free physical workshop with soldering irons, smoke stoppers, and multimeters open daily for tuning and repairs.
            </p>
          </div>

          <!-- Card 6 -->
          <div class="p-7 rounded-[18px] bg-[rgba(12,18,38,0.55)] border border-[rgba(150,175,230,0.12)] backdrop-blur-md hover:border-[rgba(150,175,230,0.25)] hover:bg-[rgba(16,24,48,0.7)] hover:-translate-y-1 transition duration-200">
            <div class="w-11 h-11 rounded-xl bg-[#5df0a8]/10 text-[#5df0a8] border border-[#5df0a8]/20 flex items-center justify-center text-xl mb-4">
              🛸
            </div>
            <h3 class="text-lg font-bold text-white mb-2">Custom Drone Sourcing</h3>
            <p class="text-sm text-[#9aa6c4] leading-relaxed">
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
            <span class="text-xs font-bold uppercase tracking-widest text-[#5df0a8]">Built for Momentum</span>
            <h2 class="text-3xl sm:text-5xl font-extrabold text-white leading-tight">
              See the whole flight envelope move in real time
            </h2>
            <p class="text-base text-[#9aa6c4] leading-relaxed">
              Every cell voltage, RSSI dBm level, motor temperature, and throttle response — rendered live. Aero Fly gives operators the altitude to fly with total confidence.
            </p>
            <div class="pt-2">
              <a
                href="https://t.me/aerobyteacademy"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center gap-2 rounded-full bg-gradient-to-b from-[#5df0a8] to-[#2fd38a] text-[#032018] px-7 py-3 text-sm font-bold shadow-md hover:shadow-lg transition"
              >
                <span>Explore Live Telemetry</span>
                <span class="text-xs font-black">→</span>
              </a>
            </div>
          </div>

          <!-- Right Dashboard Mockup -->
          <div class="lg:col-span-7">
            <div class="p-6 sm:p-7 rounded-[26px] bg-[rgba(16,24,48,0.75)] border border-[rgba(150,175,230,0.22)] shadow-2xl backdrop-blur-xl space-y-6">
              <div class="flex items-center justify-between border-b border-[rgba(150,175,230,0.12)] pb-4">
                <span class="text-sm font-bold text-white">Flight Telemetry · Quads 6S</span>
                <span class="inline-flex items-center gap-1.5 text-xs font-bold text-[#5df0a8] uppercase tracking-wider">
                  <span class="w-2 h-2 rounded-full bg-[#5df0a8] animate-ping"></span>
                  Live Link
                </span>
              </div>

              <!-- Animated Bars -->
              <div class="flex items-end gap-2.5 h-36 p-4 rounded-xl bg-black/30 border border-[rgba(150,175,230,0.12)]">
                <div class="flex-1 bg-gradient-to-t from-[rgba(47,211,138,0.2)] to-[#5df0a8] rounded-t-md transition-all duration-700" style="height: 62%"></div>
                <div class="flex-1 bg-gradient-to-t from-[rgba(47,211,138,0.2)] to-[#5df0a8] rounded-t-md transition-all duration-700" style="height: 88%"></div>
                <div class="flex-1 bg-gradient-to-t from-[rgba(47,211,138,0.2)] to-[#5df0a8] rounded-t-md transition-all duration-700" style="height: 47%"></div>
                <div class="flex-1 bg-gradient-to-t from-[rgba(47,211,138,0.2)] to-[#5df0a8] rounded-t-md transition-all duration-700" style="height: 95%"></div>
                <div class="flex-1 bg-gradient-to-t from-[rgba(47,211,138,0.2)] to-[#5df0a8] rounded-t-md transition-all duration-700" style="height: 71%"></div>
                <div class="flex-1 bg-gradient-to-t from-[rgba(47,211,138,0.2)] to-[#5df0a8] rounded-t-md transition-all duration-700" style="height: 80%"></div>
                <div class="flex-1 bg-gradient-to-t from-[rgba(47,211,138,0.2)] to-[#5df0a8] rounded-t-md transition-all duration-700" style="height: 58%"></div>
              </div>

              <!-- Telemetry Metrics Rows -->
              <div class="space-y-3 text-xs font-semibold text-[#9aa6c4]">
                <div class="flex items-center gap-4">
                  <span class="w-32 text-left">ELRS Signal Link</span>
                  <div class="flex-1 h-2 rounded-full bg-white/5 overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-[#2fd38a] to-[#5df0a8] rounded-full" style="width: 90%"></div>
                  </div>
                  <span class="text-white w-10 text-right">90%</span>
                </div>

                <div class="flex items-center gap-4">
                  <span class="w-32 text-left">Battery 6S Pack</span>
                  <div class="flex-1 h-2 rounded-full bg-white/5 overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-[#2fd38a] to-[#5df0a8] rounded-full" style="width: 72%"></div>
                  </div>
                  <span class="text-white w-10 text-right">72%</span>
                </div>

                <div class="flex items-center gap-4">
                  <span class="w-32 text-left">VTX Transmission</span>
                  <div class="flex-1 h-2 rounded-full bg-white/5 overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-[#2fd38a] to-[#5df0a8] rounded-full" style="width: 48%"></div>
                  </div>
                  <span class="text-white w-10 text-right">48%</span>
                </div>

                <div class="flex items-center gap-4">
                  <span class="w-32 text-left">GPS Satellites</span>
                  <div class="flex-1 h-2 rounded-full bg-white/5 overflow-hidden">
                    <div class="h-full bg-gradient-to-r from-[#2fd38a] to-[#5df0a8] rounded-full" style="width: 34%"></div>
                  </div>
                  <span class="text-white w-10 text-right">18 Sats</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- 4 Stats Cards -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4 mt-16">
          <div class="p-6 rounded-[18px] bg-[rgba(12,18,38,0.55)] border border-[rgba(150,175,230,0.12)] text-center backdrop-blur-md">
            <div class="text-3xl sm:text-4xl font-extrabold bg-gradient-to-b from-white to-[#5df0a8] bg-clip-text text-transparent">3.4×</div>
            <p class="text-xs sm:text-sm text-[#9aa6c4] mt-2">Faster pilot skill progression</p>
          </div>
          <div class="p-6 rounded-[18px] bg-[rgba(12,18,38,0.55)] border border-[rgba(150,175,230,0.12)] text-center backdrop-blur-md">
            <div class="text-3xl sm:text-4xl font-extrabold bg-gradient-to-b from-white to-[#5df0a8] bg-clip-text text-transparent">99.8%</div>
            <p class="text-xs sm:text-sm text-[#9aa6c4] mt-2">Radio link reliability on ELRS</p>
          </div>
          <div class="p-6 rounded-[18px] bg-[rgba(12,18,38,0.55)] border border-[rgba(150,175,230,0.12)] text-center backdrop-blur-md">
            <div class="text-3xl sm:text-4xl font-extrabold bg-gradient-to-b from-white to-[#5df0a8] bg-clip-text text-transparent">1,200+</div>
            <p class="text-xs sm:text-sm text-[#9aa6c4] mt-2">Flights logged in Cambodia</p>
          </div>
          <div class="p-6 rounded-[18px] bg-[rgba(12,18,38,0.55)] border border-[rgba(150,175,230,0.12)] text-center backdrop-blur-md">
            <div class="text-3xl sm:text-4xl font-extrabold bg-gradient-to-b from-white to-[#5df0a8] bg-clip-text text-transparent">100%</div>
            <p class="text-xs sm:text-sm text-[#9aa6c4] mt-2">Free Ta Khmau Hub access</p>
          </div>
        </div>
      </section>

      <!-- SECTION 4: EVENTS & TA KHMAU LOCATION -->
      <section id="events" class="py-20 px-4 sm:px-6 lg:px-8 max-w-[1180px] mx-auto">
        <div class="p-8 sm:p-12 rounded-[26px] bg-gradient-to-b from-[rgba(16,24,48,0.85)] to-[rgba(12,18,38,0.9)] border border-[rgba(150,175,230,0.22)] shadow-2xl backdrop-blur-xl">
          <div class="max-w-2xl text-left space-y-4">
            <span class="text-xs font-bold uppercase tracking-widest text-[#ff6b00]">Events & Weekend Schedule</span>
            <h2 class="text-3xl sm:text-5xl font-extrabold text-white">
              Weekend Flying Gatherings & Ta Khmau Location
            </h2>
            <p class="text-sm sm:text-base text-[#9aa6c4] leading-relaxed">
              Outdoor flying sessions take place on <strong>Saturdays or Sundays</strong>, but please note that <strong>they do NOT happen every week</strong> due to weather conditions. Timetables are confirmed via Thursday polls on Telegram.
            </p>
          </div>

          <div class="grid md:grid-cols-2 gap-6 mt-8">
            <!-- Event Rules -->
            <div class="p-6 rounded-2xl bg-white/5 border border-[rgba(150,175,230,0.12)] text-left space-y-3">
              <h4 class="text-base font-bold text-[#5df0a8]">Weekend Flight Notice</h4>
              <p class="text-xs sm:text-sm text-[#9aa6c4] leading-relaxed">
                Weather (wind under 20km/h, zero rain) dictates when we fly. Join the group to reserve your VTX Raceband frequency and get the GPS coordinates for this weekend.
              </p>
              <a
                href="https://t.me/aerobyteacademy"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center gap-2 text-xs font-bold text-[#ff6b00] hover:underline pt-2"
              >
                <span>View This Week's Poll on Telegram</span>
                <span>→</span>
              </a>
            </div>

            <!-- Ta Khmau Hub Details -->
            <div class="p-6 rounded-2xl bg-white/5 border border-[rgba(150,175,230,0.12)] text-left space-y-3">
              <h4 class="text-base font-bold text-white">📍 Free Physical Ta Khmau Space</h4>
              <p class="text-xs sm:text-sm text-[#9aa6c4] leading-relaxed">
                Open Tuesday – Sunday (9 AM – 6 PM). Drop in anytime to solder parts, test ESC stacks, configure Betaflight, or talk with fellow drone makers.
              </p>
              <a
                href="https://maps.google.com/?q=Ta+Khmau+Cambodia"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center gap-2 text-xs font-bold text-[#5df0a8] hover:underline pt-2"
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
        <div class="p-10 sm:p-16 rounded-[26px] bg-gradient-to-b from-[#5df0a8]/10 via-[rgba(16,24,48,0.7)] to-[rgba(12,18,38,0.85)] border border-[rgba(150,175,230,0.22)] shadow-2xl backdrop-blur-2xl max-w-3xl mx-auto space-y-6">
          <span class="text-xs font-bold uppercase tracking-widest text-[#5df0a8]">Ready When You Are</span>
          <h2 class="text-3xl sm:text-5xl font-extrabold text-white leading-tight">
            Put your flight journey on a new trajectory
          </h2>
          <p class="text-base text-[#9aa6c4] leading-relaxed">
            Need custom drone parts, a complete hand-soldered BNF quad, or pre-purchase hardware advice? We consult before you buy.
          </p>

          <div class="pt-2 flex flex-col sm:flex-row items-center justify-center gap-3.5">
            <a
              href="https://t.me/aerobyteacademy"
              target="_blank"
              rel="noopener noreferrer"
              class="w-full sm:w-auto inline-flex items-center justify-center gap-2.5 rounded-full bg-gradient-to-b from-[#5df0a8] to-[#2fd38a] text-[#032018] px-8 py-3.5 text-base font-bold shadow-lg shadow-[#5df0a8]/25 hover:shadow-[#5df0a8]/40 transition active:scale-95"
            >
              <span>Join Aero Fly Telegram</span>
              <svg class="w-4 h-4 stroke-current fill-none stroke-[2.5]" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </a>

            <a
              href="https://t.me/aerobyteacademy"
              target="_blank"
              rel="noopener noreferrer"
              class="w-full sm:w-auto inline-flex items-center justify-center gap-2 rounded-full bg-white/5 hover:bg-white/10 border border-[rgba(150,175,230,0.22)] px-7 py-3.5 text-base font-bold text-white transition"
            >
              <span>Request Custom Build Quote</span>
            </a>
          </div>
        </div>

        <p class="mt-16 text-xs text-[#6b7796]">
          © {{ currentYear }} Aero Fly — Built among the skies.
        </p>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as THREE from 'three'
import { GLTFLoader } from 'three/examples/jsm/loaders/GLTFLoader.js'
import { EffectComposer } from 'three/examples/jsm/postprocessing/EffectComposer.js'
import { RenderPass } from 'three/examples/jsm/postprocessing/RenderPass.js'
import { UnrealBloomPass } from 'three/examples/jsm/postprocessing/UnrealBloomPass.js'
import { ShaderPass } from 'three/examples/jsm/postprocessing/ShaderPass.js'
import { GammaCorrectionShader } from 'three/examples/jsm/shaders/GammaCorrectionShader.js'

const canvasRef = ref(null)
const loadingProgress = ref(0)
const currentYear = new Date().getFullYear()

let animationFrameId = null
let renderer = null
let composer = null

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

  const scene = new THREE.Scene()
  scene.background = new THREE.Color(0x04060f)

  const camera = new THREE.PerspectiveCamera(40, width / height, 0.1, 200)
  camera.position.set(0, 0, 8)
  scene.add(camera)

  // Lighting tuned for realistic carbon fiber and anodized metals
  const ambientLight = new THREE.AmbientLight(0xffffff, 2.5)
  scene.add(ambientLight)

  const keyLight = new THREE.DirectionalLight(0xffffff, 3.2)
  keyLight.position.set(4, 9, 6)
  keyLight.castShadow = true
  scene.add(keyLight)

  const fillLight = new THREE.DirectionalLight(0x7da4ff, 1.8)
  fillLight.position.set(-5, -2, 4)
  scene.add(fillLight)

  const cyanRim = new THREE.PointLight(0x5df0a8, 4.0, 15)
  cyanRim.position.set(-3, 2, 3)
  scene.add(cyanRim)

  const orangeRim = new THREE.PointLight(0xff6b00, 3.0, 12)
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
      const model = gltf.scene

      // Compute bounding box and center precisely
      const box = new THREE.Box3().setFromObject(model)
      const size = box.getSize(new THREE.Vector3())
      const center = box.getCenter(new THREE.Vector3())

      model.position.x = -center.x
      model.position.y = -center.y
      model.position.z = -center.z

      // Normalize scale (max dimension ~ 3.6 units)
      const maxDim = Math.max(size.x, size.y, size.z)
      const scale = 3.6 / maxDim
      model.scale.setScalar(scale)

      model.traverse((child) => {
        if (child.isMesh) {
          child.castShadow = true
          child.receiveShadow = true
          if (child.material) {
            child.material.envMapIntensity = 1.3
            child.material.roughness = Math.min(child.material.roughness, 0.4)
          }
        }
      })

      droneGroup.add(model)
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

  // Holographic HUD Telemetry Rings
  const ringGeo = new THREE.RingGeometry(2.3, 2.35, 64)
  const ringMat = new THREE.MeshBasicMaterial({ color: 0x5df0a8, transparent: true, opacity: 0.35, side: THREE.DoubleSide })
  const hudRing = new THREE.Mesh(ringGeo, ringMat)
  hudRing.rotation.x = Math.PI / 2
  droneGroup.add(hudRing)

  const ring2Geo = new THREE.RingGeometry(2.65, 2.69, 48)
  const ring2Mat = new THREE.MeshBasicMaterial({ color: 0x3a6cff, transparent: true, opacity: 0.22, side: THREE.DoubleSide })
  const hudRing2 = new THREE.Mesh(ring2Geo, ring2Mat)
  hudRing2.rotation.x = Math.PI / 2
  droneGroup.add(hudRing2)

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
  const stars = new THREE.Points(starGeo, starMat)
  scene.add(stars)

  // Composers (Bloom & Gamma)
  composer = new EffectComposer(renderer)
  composer.addPass(new RenderPass(scene, camera))
  composer.addPass(new UnrealBloomPass(new THREE.Vector2(width, height), 0.35, 0.4, 0.1))
  composer.addPass(new ShaderPass(GammaCorrectionShader))

  // Scroll Choreography
  const STOPS_X = [{ p: 0, v: 0 }, { p: 0.32, v: -2.7 }, { p: 0.64, v: 2.8 }, { p: 1, v: 0 }]
  const STOPS_Y = [{ p: 0, v: -3.6 }, { p: 0.32, v: 0.4 }, { p: 0.64, v: 0.3 }, { p: 1, v: 0.15 }]
  const STOPS_S = [{ p: 0, v: 2.05 }, { p: 0.32, v: 1.05 }, { p: 0.64, v: 0.95 }, { p: 1, v: 1.15 }]
  const STOPS_ROLL = [{ p: 0, v: -0.15 }, { p: 0.32, v: 0.28 }, { p: 0.64, v: -0.32 }, { p: 1, v: 0.05 }]
  const STOPS_PITCH = [{ p: 0, v: 0.65 }, { p: 0.32, v: 0.35 }, { p: 0.64, v: 0.42 }, { p: 1, v: 0.55 }]

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

    const hoverWobble = Math.sin(now * 0.003) * 0.06
    const hoverTilt = Math.cos(now * 0.0025) * 0.04

    droneGroup.rotation.x = curPitch + hoverWobble
    droneGroup.rotation.z = curRoll + hoverTilt
    droneGroup.rotation.y = (curP * Math.PI * 1.8) + (now * 0.0003)

    hudRing.rotation.z += dt * 0.25
    hudRing2.rotation.z -= dt * 0.18

    composer.render()
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
})

onUnmounted(() => {
  if (animationFrameId) cancelAnimationFrame(animationFrameId)
  if (renderer) renderer.dispose()
})
</script>
