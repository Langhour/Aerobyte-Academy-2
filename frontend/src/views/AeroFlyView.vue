<template>
  <div class="min-h-screen bg-white text-slate-800 font-sans selection:bg-orange-100 selection:text-orange-900 pb-24">
    <!-- Top Aero Fly Sub-Navigation Header (Split Across 3 Distinct Pages) -->
    <header class="sticky top-14 z-40 bg-white/95 backdrop-blur-md border-b border-slate-200 shadow-2xs">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col sm:flex-row items-center justify-between py-3 gap-3">
          <!-- Brand Badge -->
          <div class="flex items-center gap-3">
            <div class="h-9 w-9 rounded-xl bg-[#0c1e5b] flex items-center justify-center text-white font-black text-sm shadow-xs">
              AF
            </div>
            <div>
              <div class="flex items-center gap-2">
                <span class="text-base font-extrabold tracking-tight text-[#0c1e5b]">Aero Fly</span>
                <span class="text-[10px] font-bold uppercase tracking-wider bg-sky-100 text-sky-700 px-2 py-0.5 rounded-full">Community & Maker Hub</span>
              </div>
              <p class="text-xs text-slate-500 hidden sm:block">Fly, build, and configure drones together in Cambodia</p>
            </div>
          </div>

          <!-- 3-Page Segmented Tab Navigation: Community | Events | Aero Store -->
          <nav class="flex items-center p-1 rounded-xl bg-slate-100 border border-slate-200/80 w-full sm:w-auto" aria-label="Aero Fly Pages">
            <button
              type="button"
              @click="setTab('community')"
              class="flex-1 sm:flex-none flex items-center justify-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-bold transition-all duration-150 cursor-pointer"
              :class="activeTab === 'community'
                ? 'bg-[#0c1e5b] text-white shadow-xs'
                : 'text-slate-600 hover:text-[#0c1e5b] hover:bg-white/60'"
            >
              <span>✈️ Community</span>
            </button>

            <button
              type="button"
              @click="setTab('events')"
              class="flex-1 sm:flex-none flex items-center justify-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-bold transition-all duration-150 cursor-pointer"
              :class="activeTab === 'events'
                ? 'bg-[#0c1e5b] text-white shadow-xs'
                : 'text-slate-600 hover:text-[#0c1e5b] hover:bg-white/60'"
            >
              <span>📅 Events</span>
            </button>

            <button
              type="button"
              @click="setTab('store')"
              class="flex-1 sm:flex-none flex items-center justify-center gap-1.5 px-3.5 py-1.5 rounded-lg text-xs sm:text-sm font-bold transition-all duration-150 cursor-pointer"
              :class="activeTab === 'store'
                ? 'bg-[#0c1e5b] text-white shadow-xs'
                : 'text-slate-600 hover:text-[#0c1e5b] hover:bg-white/60'"
            >
              <span>🛠️ Aero Store</span>
            </button>
          </nav>
        </div>
      </div>
    </header>

    <!-- ============================================================== -->
    <!-- PAGE 1: AERO FLY COMMUNITY (HOME)                             -->
    <!-- ============================================================== -->
    <main v-if="activeTab === 'community'" class="transition-opacity duration-200">
      <!-- 1. Hero Section -->
      <section class="relative overflow-hidden pt-10 pb-16 sm:pt-16 sm:pb-24 border-b border-slate-100">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="grid lg:grid-cols-12 gap-10 items-center">
            <!-- Left Hero Content -->
            <div class="lg:col-span-7 space-y-6 text-left">
              <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-50 border border-sky-200 text-sky-700 text-xs font-bold">
                <span class="inline-block w-2 h-2 rounded-full bg-sky-500 animate-pulse"></span>
                Cambodia's Open Drone Community
              </div>

              <h1 class="text-3xl sm:text-5xl lg:text-[52px] font-extrabold tracking-tight text-[#0c1e5b] leading-[1.12]">
                Whether You Fly, Build, or Just Want to Learn.
              </h1>

              <p class="text-base sm:text-lg text-slate-600 leading-relaxed max-w-2xl">
                Aero Fly is a welcoming home for every drone enthusiast in Cambodia. Whether you own a multi-thousand dollar camera drone, build high-speed FPV racing quads from parts, or have never held a controller before—we're here to fly together.
              </p>

              <!-- Hero CTA Buttons -->
              <div class="flex flex-col sm:flex-row items-stretch sm:items-center gap-3.5 pt-2">
                <!-- Primary Orange CTA -->
                <a
                  href="https://t.me/aerobyteacademy"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="inline-flex items-center justify-center gap-2.5 rounded-xl bg-[#ff6b00] hover:bg-[#e05e00] px-7 py-3.5 text-base font-bold text-white shadow-md shadow-orange-500/20 active:scale-95 transition cursor-pointer"
                >
                  <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24">
                    <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.121l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.458c.538-.196 1.006.128.832.943z"/>
                  </svg>
                  <span>Join Telegram Group</span>
                </a>

                <!-- Secondary Link to Events -->
                <button
                  type="button"
                  @click="setTab('events')"
                  class="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-300 bg-white hover:bg-slate-50 px-6 py-3.5 text-sm font-bold text-[#0c1e5b] transition cursor-pointer"
                >
                  <span>Explore Flying Events</span>
                  <span class="text-xs">→</span>
                </button>
              </div>

              <!-- Quick Stats / Social Proof -->
              <div class="pt-4 flex items-center gap-6 text-xs text-slate-500 font-medium border-t border-slate-100">
                <div class="flex items-center gap-1.5">
                  <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                  <span>Free & Open to All</span>
                </div>
                <div>• Weekly Live Discussions</div>
                <div>• Zero Experience Needed</div>
              </div>
            </div>

            <!-- Right Hero Imagery -->
            <div class="lg:col-span-5">
              <div class="relative mx-auto max-w-md lg:max-w-none">
                <div class="relative overflow-hidden rounded-3xl border border-slate-200 shadow-xl bg-slate-50">
                  <img
                    src="/assets/about/drone_pilot.jpg"
                    alt="Aero Fly Drone Community Pilot Flying"
                    class="w-full h-80 sm:h-96 object-cover object-center transition duration-500 hover:scale-105"
                  />
                  <!-- Floating Badge -->
                  <div class="absolute bottom-4 left-4 right-4 bg-white/95 backdrop-blur-md p-4 rounded-2xl border border-slate-200/80 shadow-md">
                    <div class="flex items-center justify-between">
                      <div class="flex items-center gap-3">
                        <div class="w-10 h-10 rounded-xl bg-sky-100 text-sky-700 flex items-center justify-center font-bold text-lg">
                          🚁
                        </div>
                        <div>
                          <p class="text-xs font-extrabold text-[#0c1e5b]">Solo Pilots Welcome</p>
                          <p class="text-[11px] text-slate-500">Find wingmates & practice buddies</p>
                        </div>
                      </div>
                      <span class="text-[11px] font-bold text-orange-600 bg-orange-50 px-2 py-1 rounded-md">Live Chat</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 2. Mission & Purpose ("Why Aero Fly Exists") -->
      <section class="py-16 sm:py-20 bg-slate-50/50 border-b border-slate-200/60">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="text-center max-w-3xl mx-auto mb-12">
            <span class="text-xs font-bold uppercase tracking-wider text-sky-600">Our Community Mission</span>
            <h2 class="mt-2 text-2xl sm:text-4xl font-extrabold text-[#0c1e5b]">
              Why Fly Alone When We Can Grow Together?
            </h2>
            <p class="mt-3 text-sm sm:text-base text-slate-600 leading-relaxed">
              Drones can feel intimidating: complex radio binds, confusing frequencies, and sudden crashes. Aero Fly was founded to eliminate that barrier.
            </p>
          </div>

          <div class="grid sm:grid-cols-2 lg:grid-cols-3 gap-6">
            <!-- Card 1 -->
            <div class="rounded-2xl border border-slate-200 bg-white p-7 shadow-xs hover:shadow-md transition">
              <div class="w-12 h-12 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center text-2xl mb-4 border border-sky-100">
                🤝
              </div>
              <h3 class="text-lg font-bold text-[#0c1e5b]">Connect Solo Drone Pilots</h3>
              <p class="mt-2 text-xs sm:text-sm text-slate-600 leading-relaxed">
                Flying in a park alone gets boring fast. We unite hobbyists across Phnom Penh, Kandal, and provinces so you can share spotter duties, race gates, and video feeds.
              </p>
            </div>

            <!-- Card 2 -->
            <div class="rounded-2xl border border-slate-200 bg-white p-7 shadow-xs hover:shadow-md transition">
              <div class="w-12 h-12 rounded-xl bg-amber-50 text-amber-600 flex items-center justify-center text-2xl mb-4 border border-amber-100">
                🔰
              </div>
              <h3 class="text-lg font-bold text-[#0c1e5b]">Zero-Jargon Beginner Guidance</h3>
              <p class="mt-2 text-xs sm:text-sm text-slate-600 leading-relaxed">
                Don't know what ESC, ELRS, or LiPo 4S means? That's completely okay. Our members break everything down simply and guide your very first flight on a simulator.
              </p>
            </div>

            <!-- Card 3 -->
            <div class="rounded-2xl border border-slate-200 bg-white p-7 shadow-xs hover:shadow-md transition sm:col-span-2 lg:col-span-1">
              <div class="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center text-2xl mb-4 border border-emerald-100">
                🔧
              </div>
              <h3 class="text-lg font-bold text-[#0c1e5b]">Crash Repair & Hardware Exchange</h3>
              <p class="mt-2 text-xs sm:text-sm text-slate-600 leading-relaxed">
                Crashing is part of learning. Learn how to solder loose wires, swap broken arms, tune PIDs in Betaflight, and borrow spare props from friends on the field.
              </p>
            </div>
          </div>
        </div>
      </section>

      <!-- 3. Primary CTA Banner (Telegram Group) -->
      <section class="py-14 sm:py-18">
        <div class="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8">
          <div class="relative overflow-hidden rounded-3xl bg-[#0c1e5b] text-white p-8 sm:p-12 shadow-xl border border-navy-800">
            <div class="relative z-10 max-w-2xl space-y-4">
              <span class="inline-block text-xs font-bold uppercase tracking-wider bg-orange-500/20 text-orange-300 border border-orange-400/30 px-3 py-1 rounded-full">
                Real-Time Updates & Flight Schedules
              </span>
              <h3 class="text-2xl sm:text-4xl font-extrabold tracking-tight">
                Join the Aero Fly Telegram Group Today
              </h3>
              <p class="text-sm sm:text-base text-slate-200 leading-relaxed">
                Get notified of spontaneous weekend flying sessions, weather forecasts, technical Q&A, and community buy/swap deals. It's 100% free.
              </p>
              <div class="pt-3 flex flex-wrap gap-3">
                <a
                  href="https://t.me/aerobyteacademy"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="inline-flex items-center gap-2.5 rounded-xl bg-[#ff6b00] hover:bg-[#e05e00] px-7 py-3.5 text-sm sm:text-base font-bold text-white shadow-lg shadow-orange-950/30 transition cursor-pointer"
                >
                  <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24">
                    <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.121l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.458c.538-.196 1.006.128.832.943z"/>
                  </svg>
                  <span>Open Telegram Group (@aerobyteacademy)</span>
                </a>
              </div>
            </div>

            <!-- Background Aesthetic Watermark -->
            <div class="pointer-events-none absolute right-4 -bottom-10 opacity-10 text-[180px] font-black select-none">
              ✈️
            </div>
          </div>
        </div>
      </section>
    </main>

    <!-- ============================================================== -->
    <!-- PAGE 2: EVENTS (WEEKEND FLIGHTS & TA KHMAU LOCATION)          -->
    <!-- ============================================================== -->
    <main v-else-if="activeTab === 'events'" class="transition-opacity duration-200">
      <!-- 1. Events Hero Header -->
      <section class="pt-10 pb-12 sm:pt-14 sm:pb-16 border-b border-slate-100">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="max-w-3xl text-left space-y-4">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-50 border border-sky-200 text-sky-800 text-xs font-bold">
              <span class="w-2 h-2 rounded-full bg-sky-500 animate-pulse"></span>
              Outdoor Flying Sessions & Maker Gatherings
            </div>

            <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight text-[#0c1e5b] leading-[1.12]">
              Aero Fly Events & Flying Schedule
            </h1>

            <p class="text-base sm:text-lg text-slate-600 leading-relaxed">
              We organize outdoor flying gatherings, FPV race days, and free physical tech meetups at our Ta Khmau location. Connect with fellow pilots, test your hardware safely, and explore new flying fields together.
            </p>

            <!-- Hero Action Buttons -->
            <div class="pt-2 flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
              <a
                href="https://t.me/aerobyteacademy"
                target="_blank"
                rel="noopener noreferrer"
                class="inline-flex items-center justify-center gap-2.5 rounded-xl bg-[#ff6b00] hover:bg-[#e05e00] px-7 py-3.5 text-sm sm:text-base font-bold text-white shadow-md shadow-orange-500/20 active:scale-95 transition cursor-pointer"
              >
                <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24">
                  <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.121l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.458c.538-.196 1.006.128.832.943z"/>
                </svg>
                <span>Get Exact Schedule on Telegram</span>
              </a>

              <a
                href="#takhmaulocation"
                class="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-300 bg-white hover:bg-slate-50 px-6 py-3.5 text-sm font-bold text-[#0c1e5b] transition"
              >
                <span>📍 View Ta Khmau Location</span>
              </a>
            </div>
          </div>
        </div>
      </section>

      <!-- 2. Weekend Flying Schedule Notice Box -->
      <section class="py-10 bg-slate-50/70 border-b border-slate-200">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="rounded-2xl border-2 border-amber-300 bg-amber-50/90 p-6 sm:p-8 shadow-xs max-w-4xl mx-auto">
            <div class="flex items-start gap-4">
              <span class="text-3xl shrink-0">⚠️</span>
              <div class="space-y-2 text-left">
                <div class="flex items-center gap-2 flex-wrap">
                  <h3 class="text-base sm:text-lg font-extrabold text-amber-950">
                    Important Schedule Notice: Weekend Flight Sessions
                  </h3>
                  <span class="text-[11px] font-bold uppercase bg-amber-200/80 text-amber-900 px-2 py-0.5 rounded-md">
                    Saturdays or Sundays
                  </span>
                </div>
                <p class="text-xs sm:text-sm text-amber-900/90 leading-relaxed">
                  Our outdoor flying sessions take place on <strong>Saturdays or Sundays</strong>, but please note that <strong>they do NOT happen every single week</strong>. Drone flights require safe weather conditions (low winds, clear visibility, and zero rain).
                </p>
                <p class="text-xs sm:text-sm text-amber-950 font-bold leading-relaxed pt-1">
                  👉 To know the exact weekly timetable, flight field GPS coordinates, and weather confirmations, you must join our official Telegram group where polls are held every Thursday.
                </p>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 3. What Happens at Our Events (4 Event Types) -->
      <section class="py-16 sm:py-20 border-b border-slate-100">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="text-center max-w-3xl mx-auto mb-12">
            <span class="text-xs font-bold uppercase tracking-wider text-sky-600">Event Formats</span>
            <h2 class="mt-2 text-2xl sm:text-4xl font-extrabold text-[#0c1e5b]">
              What We Do at Aero Fly Events
            </h2>
            <p class="mt-3 text-sm sm:text-base text-slate-600 leading-relaxed">
              Every gathering is designed to be beginner-friendly while giving advanced drone builders an open playground to test high-performance hardware.
            </p>
          </div>

          <div class="grid sm:grid-cols-2 lg:grid-cols-4 gap-6">
            <!-- Event 1: FPV Freestyle & Racing -->
            <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs hover:shadow-md transition text-left flex flex-col justify-between">
              <div>
                <div class="w-12 h-12 rounded-xl bg-orange-50 text-orange-600 flex items-center justify-center text-2xl mb-4 border border-orange-100">
                  🏁
                </div>
                <span class="text-[10px] font-bold uppercase tracking-wider text-orange-600 bg-orange-50 px-2 py-0.5 rounded">High Speed</span>
                <h3 class="text-base font-bold text-[#0c1e5b] mt-2">FPV Freestyle & Racing</h3>
                <p class="mt-2 text-xs text-slate-600 leading-relaxed">
                  Fly through racing gates, perform acro tricks, and test high-speed 4S/6S drone setups with multi-pilot video frequency coordination.
                </p>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-500 font-medium">
                📍 Open grasslands & fields
              </div>
            </div>

            <!-- Event 2: Cinematic & Photography -->
            <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs hover:shadow-md transition text-left flex flex-col justify-between">
              <div>
                <div class="w-12 h-12 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center text-2xl mb-4 border border-sky-100">
                  📸
                </div>
                <span class="text-[10px] font-bold uppercase tracking-wider text-sky-600 bg-sky-50 px-2 py-0.5 rounded">Scenic</span>
                <h3 class="text-base font-bold text-[#0c1e5b] mt-2">Aerial Cinematography</h3>
                <p class="mt-2 text-xs text-slate-600 leading-relaxed">
                  Bring DJI, camera drones, or cinewhoops. Practice smooth camera motions, ND filter settings, and golden-hour sunset landscape shoots.
                </p>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-500 font-medium">
                📍 Scenic outdoor locations
              </div>
            </div>

            <!-- Event 3: Beginner Flight Clinic -->
            <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs hover:shadow-md transition text-left flex flex-col justify-between">
              <div>
                <div class="w-12 h-12 rounded-xl bg-emerald-50 text-emerald-600 flex items-center justify-center text-2xl mb-4 border border-emerald-100">
                  🔰
                </div>
                <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded">Beginner Friendly</span>
                <h3 class="text-base font-bold text-[#0c1e5b] mt-2">Beginner Flight Clinic</h3>
                <p class="mt-2 text-xs text-slate-600 leading-relaxed">
                  Never flown before? Borrow our trainer radios, practice on high-resolution simulators, and make your very first assisted real-life takeoff.
                </p>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-500 font-medium">
                📍 100% Free Coaching
              </div>
            </div>

            <!-- Event 4: Ta Khmau Tech Meetups -->
            <div class="rounded-2xl border border-slate-200 bg-white p-6 shadow-xs hover:shadow-md transition text-left flex flex-col justify-between">
              <div>
                <div class="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center text-2xl mb-4 border border-indigo-100">
                  🔧
                </div>
                <span class="text-[10px] font-bold uppercase tracking-wider text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">Hardware & Tuning</span>
                <h3 class="text-base font-bold text-[#0c1e5b] mt-2">Tech & Config Meetup</h3>
                <p class="mt-2 text-xs text-slate-600 leading-relaxed">
                  In-person gatherings at our Ta Khmau workshop to solder broken motors, flash Betaflight firmware, bind ELRS transmitters, and exchange build tips.
                </p>
              </div>
              <div class="mt-4 pt-3 border-t border-slate-100 text-[11px] text-slate-500 font-medium">
                📍 Ta Khmau Physical Space
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 4. The Ta Khmau Physical Meetup Location -->
      <section id="takhmaulocation" class="py-16 sm:py-20 bg-slate-50/60 border-b border-slate-200 scroll-mt-24">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="grid lg:grid-cols-12 gap-10 items-center">
            <!-- Left Info -->
            <div class="lg:col-span-7 space-y-5 text-left">
              <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs font-bold">
                <span class="w-2 h-2 rounded-full bg-emerald-500"></span>
                Free Physical Location in Ta Khmau • Open Daily
              </div>

              <h2 class="text-2xl sm:text-4xl font-extrabold text-[#0c1e5b] leading-[1.18]">
                Come Anytime to Our Ta Khmau Location
              </h2>

              <p class="text-sm sm:text-base text-slate-600 leading-relaxed">
                You don't have to wait for weekend flights to connect. Our physical space in <strong>Ta Khmau, Kandal</strong> is completely free and open for anyone to drop by anytime. Configure your drones, solder parts, talk tech, and exchange experiences with our resident builders.
              </p>

              <!-- Features Grid -->
              <div class="grid grid-cols-2 sm:grid-cols-3 gap-3 pt-2">
                <div class="p-3.5 rounded-xl bg-white border border-slate-200 text-left shadow-2xs">
                  <span class="text-xl">🛠️</span>
                  <p class="text-xs font-bold text-[#0c1e5b] mt-1.5">Free Workbenches</p>
                  <p class="text-[11px] text-slate-500">Soldering irons, multimeters & smoke stoppers</p>
                </div>
                <div class="p-3.5 rounded-xl bg-white border border-slate-200 text-left shadow-2xs">
                  <span class="text-xl">💻</span>
                  <p class="text-xs font-bold text-[#0c1e5b] mt-1.5">Betaflight Station</p>
                  <p class="text-[11px] text-slate-500">Fast PID tuning, gyro calibration & ELRS bind</p>
                </div>
                <div class="p-3.5 rounded-xl bg-white border border-slate-200 text-left shadow-2xs col-span-2 sm:col-span-1">
                  <span class="text-xl">☕</span>
                  <p class="text-xs font-bold text-[#0c1e5b] mt-1.5">Pilot Lounge</p>
                  <p class="text-[11px] text-slate-500">Hang out, have coffee, talk drones & specs</p>
                </div>
              </div>

              <!-- Location Action -->
              <div class="pt-3 flex flex-wrap items-center gap-3">
                <a
                  href="https://maps.google.com/?q=Ta+Khmau+Cambodia"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="inline-flex items-center gap-2 rounded-xl bg-[#0c1e5b] hover:bg-[#16365c] text-white px-6 py-3 text-sm font-bold shadow-xs transition"
                >
                  <span>📍 Open Directions on Google Maps</span>
                </a>
                <span class="text-xs text-slate-500 font-medium">Free Access • Everyone Welcome</span>
              </div>
            </div>

            <!-- Right Location Card -->
            <div class="lg:col-span-5">
              <div class="rounded-3xl border border-slate-200 bg-white shadow-lg overflow-hidden">
                <img
                  src="/assets/about/aerobyte_lab.jpg"
                  alt="Aero Fly Ta Khmau Location Workbench"
                  class="w-full h-64 object-cover object-center"
                />
                <div class="p-6 space-y-4">
                  <div class="flex items-center justify-between border-b border-slate-100 pb-3">
                    <span class="text-xs font-bold uppercase tracking-wider text-slate-500">Location Address</span>
                    <span class="text-xs font-bold text-emerald-600 bg-emerald-50 px-2 py-0.5 rounded-md">Open to Anyone</span>
                  </div>
                  <p class="text-sm font-bold text-[#0c1e5b]">
                    Aero Fly Location @ Ta Khmau, Kandal Province, Cambodia
                  </p>
                  <div class="text-xs text-slate-600 space-y-2">
                    <div class="flex items-center justify-between">
                      <span class="text-slate-500">Operating Hours:</span>
                      <span class="font-bold text-slate-800">Tuesday – Sunday, 9:00 AM – 6:00 PM</span>
                    </div>
                    <div class="flex items-center justify-between">
                      <span class="text-slate-500">Admission Fee:</span>
                      <span class="font-bold text-emerald-600">Free ($0.00)</span>
                    </div>
                    <div class="flex items-center justify-between">
                      <span class="text-slate-500">What to Bring:</span>
                      <span class="font-medium text-slate-700">Your drone or just your curiosity</span>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <!-- 5. How to Join a Weekend Event (3 Step Flow) -->
      <section class="py-16 sm:py-20 border-b border-slate-100">
        <div class="mx-auto max-w-5xl px-4 sm:px-6 lg:px-8 text-center">
          <span class="text-xs font-bold uppercase tracking-wider text-sky-600">Participation Guide</span>
          <h2 class="text-2xl sm:text-3xl font-extrabold text-[#0c1e5b] mt-1">
            How to Join an Aero Fly Weekend Event
          </h2>
          <p class="text-xs sm:text-sm text-slate-600 mt-2 max-w-xl mx-auto">
            Joining our flight sessions is easy, safe, and completely open to both experienced pilots and spectators.
          </p>

          <div class="grid sm:grid-cols-3 gap-6 mt-10">
            <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs text-left">
              <div class="w-10 h-10 rounded-xl bg-sky-100 text-sky-700 flex items-center justify-center font-extrabold text-base mb-3">
                1
              </div>
              <h4 class="text-sm font-bold text-[#0c1e5b]">Check Weekly Poll</h4>
              <p class="mt-1.5 text-xs text-slate-600 leading-relaxed">
                Join our Telegram group where our team posts the weekend weather poll every Thursday to confirm either Saturday or Sunday.
              </p>
            </div>

            <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs text-left">
              <div class="w-10 h-10 rounded-xl bg-sky-100 text-sky-700 flex items-center justify-center font-extrabold text-base mb-3">
                2
              </div>
              <h4 class="text-sm font-bold text-[#0c1e5b]">Coordinate Frequency</h4>
              <p class="mt-1.5 text-xs text-slate-600 leading-relaxed">
                If flying FPV video goggles, coordinate your band/channel (Raceband 1–8) in the chat to prevent video interference with others.
              </p>
            </div>

            <div class="bg-white rounded-2xl border border-slate-200 p-6 shadow-xs text-left">
              <div class="w-10 h-10 rounded-xl bg-sky-100 text-sky-700 flex items-center justify-center font-extrabold text-base mb-3">
                3
              </div>
              <h4 class="text-sm font-bold text-[#0c1e5b]">Arrive & Fly</h4>
              <p class="mt-1.5 text-xs text-slate-600 leading-relaxed">
                Show up at the field GPS pin. Bring charged LiPo batteries, spare props, or just watch and ask questions.
              </p>
            </div>
          </div>

          <!-- Bottom Schedule Callout -->
          <div class="mt-12">
            <a
              href="https://t.me/aerobyteacademy"
              target="_blank"
              rel="noopener noreferrer"
              class="inline-flex items-center gap-2.5 rounded-xl bg-[#ff6b00] hover:bg-[#e05e00] px-8 py-4 text-base font-bold text-white shadow-lg shadow-orange-500/20 active:scale-95 transition cursor-pointer"
            >
              <svg class="w-5 h-5 fill-current" viewBox="0 0 24 24">
                <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.121l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.458c.538-.196 1.006.128.832.943z"/>
              </svg>
              <span>Join Telegram for Real-Time Event Schedules</span>
            </a>
          </div>
        </div>
      </section>
    </main>

    <!-- ============================================================== -->
    <!-- PAGE 3: AERO STORE (CUSTOM ORDERS & HARDWARE CONSULTING)       -->
    <!-- ============================================================== -->
    <main v-else-if="activeTab === 'store'" class="transition-opacity duration-200">
      <!-- 1. Store Services Overview -->
      <section class="pt-10 pb-12 sm:pt-14 sm:pb-16 border-b border-slate-100">
        <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div class="max-w-3xl text-left">
            <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-orange-50 border border-orange-200 text-orange-800 text-xs font-bold">
              🛠️ Hardware Consulting & Custom Sourcing
            </div>
            <h1 class="mt-3 text-3xl sm:text-5xl font-extrabold tracking-tight text-[#0c1e5b] leading-[1.15]">
              We Don't Just Sell. We Consult.
            </h1>
            <p class="mt-4 text-base sm:text-lg text-slate-600 leading-relaxed">
              Buying random parts online often leads to incompatible voltage stacks, wrong motor KV ratings, or burned electronics. Aero Store operates differently: tell us what you want to achieve, and we consult, specify, source, or custom-assemble the perfect drone setup for you.
            </p>
          </div>

          <!-- 3 Service Offerings Grid -->
          <div class="grid md:grid-cols-3 gap-6 mt-10">
            <!-- Pillar 1: Order Drone Parts -->
            <div class="rounded-2xl border-2 border-slate-200 bg-white p-7 shadow-xs hover:border-[#0c1e5b] transition">
              <div class="w-12 h-12 rounded-xl bg-sky-50 text-sky-600 flex items-center justify-center text-2xl mb-4 border border-sky-100">
                📦
              </div>
              <h3 class="text-lg font-bold text-[#0c1e5b]">Order Drone Parts</h3>
              <p class="mt-2 text-xs sm:text-sm text-slate-600 leading-relaxed">
                Source genuine carbon frames, brushless motors, flight controllers (F4/F7/H7), ESC stacks, video transmitters (VTX), antennas, and camera modules.
              </p>
              <ul class="mt-4 space-y-1.5 text-xs text-slate-500 font-medium">
                <li>✓ Compatibility checks guaranteed</li>
                <li>✓ High-quality tested components</li>
                <li>✓ Fast delivery in Cambodia</li>
              </ul>
              <button
                type="button"
                @click="openOrderModal('parts')"
                class="mt-6 w-full py-2.5 px-4 rounded-xl border border-[#0c1e5b] text-[#0c1e5b] hover:bg-[#0c1e5b] hover:text-white font-bold text-xs transition cursor-pointer"
              >
                Request Parts Sourcing
              </button>
            </div>

            <!-- Pillar 2: Fully Built Drones -->
            <div class="rounded-2xl border-2 border-[#0c1e5b] bg-slate-50/50 p-7 shadow-sm relative">
              <div class="absolute -top-3 right-6 bg-[#ff6b00] text-white text-[10px] font-extrabold uppercase px-2.5 py-0.5 rounded-full tracking-wide">
                Most Popular
              </div>
              <div class="w-12 h-12 rounded-xl bg-orange-100 text-orange-700 flex items-center justify-center text-2xl mb-4 border border-orange-200">
                🛸
              </div>
              <h3 class="text-lg font-bold text-[#0c1e5b]">Order Fully Built Drones</h3>
              <p class="mt-2 text-xs sm:text-sm text-slate-600 leading-relaxed">
                Hand-built, soldered, tuned, and test-flown by veteran Aero Fly engineers. Bind-and-Fly (BNF) or Ready-to-Fly (RTF) packages including transmitter and goggles.
              </p>
              <ul class="mt-4 space-y-1.5 text-xs text-slate-500 font-medium">
                <li>✓ Complete solder inspection & smoke test</li>
                <li>✓ Custom Betaflight/ArduPilot tuning</li>
                <li>✓ Ready to take flight on day one</li>
              </ul>
              <button
                type="button"
                @click="openOrderModal('built')"
                class="mt-6 w-full py-2.5 px-4 rounded-xl bg-[#0c1e5b] text-white hover:bg-[#16365c] font-bold text-xs transition cursor-pointer shadow-xs"
              >
                Order Custom Build
              </button>
            </div>

            <!-- Pillar 3: Expert Recommendations -->
            <div class="rounded-2xl border-2 border-slate-200 bg-white p-7 shadow-xs hover:border-[#0c1e5b] transition">
              <div class="w-12 h-12 rounded-xl bg-indigo-50 text-indigo-600 flex items-center justify-center text-2xl mb-4 border border-indigo-100">
                💡
              </div>
              <h3 class="text-lg font-bold text-[#0c1e5b]">Expert Recommendations</h3>
              <p class="mt-2 text-xs sm:text-sm text-slate-600 leading-relaxed">
                Unsure whether analog or digital HD video fits your budget? Confused about LiPo cell counts? Schedule a quick chat to get an honest gear recommendation.
              </p>
              <ul class="mt-4 space-y-1.5 text-xs text-slate-500 font-medium">
                <li>✓ Tailored to your exact budget ($)</li>
                <li>✓ For beginners, videographers & racers</li>
                <li>✓ 100% free consultation advice</li>
              </ul>
              <button
                type="button"
                @click="openOrderModal('advice')"
                class="mt-6 w-full py-2.5 px-4 rounded-xl border border-[#0c1e5b] text-[#0c1e5b] hover:bg-[#0c1e5b] hover:text-white font-bold text-xs transition cursor-pointer"
              >
                Get Free Gear Advice
              </button>
            </div>
          </div>
        </div>
      </section>

      <!-- 2. Interactive Custom Order & Consultation Intake Form -->
      <section class="py-14 sm:py-18 bg-slate-50/70 border-b border-slate-200">
        <div class="mx-auto max-w-4xl px-4 sm:px-6 lg:px-8">
          <div class="rounded-3xl border border-slate-200 bg-white p-8 sm:p-12 shadow-sm">
            <div class="text-left mb-8">
              <span class="text-xs font-bold uppercase tracking-wider text-sky-600">Start Your Custom Order</span>
              <h2 class="text-2xl sm:text-3xl font-extrabold text-[#0c1e5b] mt-1">
                Tell Us What You're Looking For
              </h2>
              <p class="text-xs sm:text-sm text-slate-600 mt-2">
                Fill out this quick form or reach out directly on Telegram. Our team will review your specifications and contact you with quotes and advice.
              </p>
            </div>

            <!-- Order Intake Form -->
            <form @submit.prevent="submitOrderForm" class="space-y-6 text-left">
              <!-- Service Category -->
              <div>
                <label class="block text-xs font-bold text-[#0c1e5b] uppercase tracking-wider mb-2">
                  What kind of service do you need?
                </label>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <label
                    class="flex items-center gap-2.5 p-3 rounded-xl border cursor-pointer text-xs font-bold transition"
                    :class="orderForm.service === 'parts' ? 'border-[#0c1e5b] bg-sky-50 text-[#0c1e5b]' : 'border-slate-200 text-slate-700 hover:bg-slate-50'"
                  >
                    <input type="radio" value="parts" v-model="orderForm.service" class="accent-[#0c1e5b]" />
                    <span>Order Drone Parts</span>
                  </label>
                  <label
                    class="flex items-center gap-2.5 p-3 rounded-xl border cursor-pointer text-xs font-bold transition"
                    :class="orderForm.service === 'built' ? 'border-[#0c1e5b] bg-sky-50 text-[#0c1e5b]' : 'border-slate-200 text-slate-700 hover:bg-slate-50'"
                  >
                    <input type="radio" value="built" v-model="orderForm.service" class="accent-[#0c1e5b]" />
                    <span>Order Fully Built Drone</span>
                  </label>
                  <label
                    class="flex items-center gap-2.5 p-3 rounded-xl border cursor-pointer text-xs font-bold transition"
                    :class="orderForm.service === 'advice' ? 'border-[#0c1e5b] bg-sky-50 text-[#0c1e5b]' : 'border-slate-200 text-slate-700 hover:bg-slate-50'"
                  >
                    <input type="radio" value="advice" v-model="orderForm.service" class="accent-[#0c1e5b]" />
                    <span>Expert Advice / Consult</span>
                  </label>
                </div>
              </div>

              <!-- Experience Level -->
              <div>
                <label class="block text-xs font-bold text-[#0c1e5b] uppercase tracking-wider mb-2">
                  Your Current Experience Level
                </label>
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
                  <label
                    class="flex items-center gap-2 p-3 rounded-xl border cursor-pointer text-xs font-medium transition"
                    :class="orderForm.experience === 'beginner' ? 'border-sky-400 bg-sky-50 text-sky-900 font-bold' : 'border-slate-200 text-slate-600'"
                  >
                    <input type="radio" value="beginner" v-model="orderForm.experience" class="accent-sky-600" />
                    <span>🔰 Complete Beginner</span>
                  </label>
                  <label
                    class="flex items-center gap-2 p-3 rounded-xl border cursor-pointer text-xs font-medium transition"
                    :class="orderForm.experience === 'intermediate' ? 'border-sky-400 bg-sky-50 text-sky-900 font-bold' : 'border-slate-200 text-slate-600'"
                  >
                    <input type="radio" value="intermediate" v-model="orderForm.experience" class="accent-sky-600" />
                    <span>🚁 Some Simulator / Flying</span>
                  </label>
                  <label
                    class="flex items-center gap-2 p-3 rounded-xl border cursor-pointer text-xs font-medium transition"
                    :class="orderForm.experience === 'maker' ? 'border-sky-400 bg-sky-50 text-sky-900 font-bold' : 'border-slate-200 text-slate-600'"
                  >
                    <input type="radio" value="maker" v-model="orderForm.experience" class="accent-sky-600" />
                    <span>🔧 Experienced Maker / Pilot</span>
                  </label>
                </div>
              </div>

              <!-- Contact & Details Grid -->
              <div class="grid sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs font-bold text-slate-700 mb-1.5">
                    Your Name or Nickname *
                  </label>
                  <input
                    type="text"
                    required
                    v-model="orderForm.name"
                    placeholder="e.g. Chan Dara"
                    class="w-full rounded-xl border border-slate-300 px-3.5 py-2.5 text-sm focus:border-[#0c1e5b] focus:outline-none focus:ring-1 focus:ring-[#0c1e5b]"
                  />
                </div>

                <div>
                  <label class="block text-xs font-bold text-slate-700 mb-1.5">
                    Telegram Handle or Phone Number *
                  </label>
                  <input
                    type="text"
                    required
                    v-model="orderForm.contact"
                    placeholder="e.g. @dara_fpv or 012 345 678"
                    class="w-full rounded-xl border border-slate-300 px-3.5 py-2.5 text-sm focus:border-[#0c1e5b] focus:outline-none focus:ring-1 focus:ring-[#0c1e5b]"
                  />
                </div>
              </div>

              <!-- Estimated Budget & Details -->
              <div class="grid sm:grid-cols-2 gap-4">
                <div>
                  <label class="block text-xs font-bold text-slate-700 mb-1.5">
                    Estimated Budget Range (Optional)
                  </label>
                  <select
                    v-model="orderForm.budget"
                    class="w-full rounded-xl border border-slate-300 px-3.5 py-2.5 text-sm focus:border-[#0c1e5b] focus:outline-none focus:ring-1 focus:ring-[#0c1e5b] bg-white text-slate-700"
                  >
                    <option value="">Under $150 (Starter / Parts)</option>
                    <option value="150-300">$150 – $300 (Analog BNF / Kit)</option>
                    <option value="300-600">$300 – $600 (High-End Freestyle / HD)</option>
                    <option value="600+">$600+ (Professional Cinema / Autonomous)</option>
                  </select>
                </div>

                <div>
                  <label class="block text-xs font-bold text-slate-700 mb-1.5">
                    Drone Type or Usage
                  </label>
                  <input
                    type="text"
                    v-model="orderForm.droneType"
                    placeholder="e.g. 5-inch Freestyle, Cinematic, TinyWhoop..."
                    class="w-full rounded-xl border border-slate-300 px-3.5 py-2.5 text-sm focus:border-[#0c1e5b] focus:outline-none focus:ring-1 focus:ring-[#0c1e5b]"
                  />
                </div>
              </div>

              <!-- Notes / Description -->
              <div>
                <label class="block text-xs font-bold text-slate-700 mb-1.5">
                  Specific Parts Needed or Project Description
                </label>
                <textarea
                  rows="3"
                  v-model="orderForm.notes"
                  placeholder="Tell us what parts you want, or explain what you want your drone to do..."
                  class="w-full rounded-xl border border-slate-300 px-3.5 py-2.5 text-sm focus:border-[#0c1e5b] focus:outline-none focus:ring-1 focus:ring-[#0c1e5b]"
                ></textarea>
              </div>

              <!-- Submit Buttons -->
              <div class="pt-2 flex flex-col sm:flex-row items-stretch sm:items-center gap-3">
                <button
                  type="submit"
                  class="inline-flex items-center justify-center gap-2 rounded-xl bg-[#ff6b00] hover:bg-[#e05e00] px-7 py-3.5 text-sm font-bold text-white shadow-md shadow-orange-500/20 active:scale-95 transition cursor-pointer"
                >
                  <span>🚀 Submit Consultation Request</span>
                </button>

                <a
                  href="https://t.me/aerobyteacademy"
                  target="_blank"
                  rel="noopener noreferrer"
                  class="inline-flex items-center justify-center gap-2 rounded-xl border border-slate-300 bg-white hover:bg-slate-50 px-5 py-3.5 text-sm font-bold text-slate-700 transition"
                >
                  <span>Or Message Builder Directly on Telegram</span>
                </a>
              </div>

              <!-- Success Alert Message -->
              <div v-if="orderSubmitted" class="p-4 rounded-xl bg-emerald-50 border border-emerald-200 text-emerald-800 text-xs sm:text-sm font-medium flex items-center gap-2">
                <span>✓</span>
                <span>Thank you! Your request has been received. Our builder will connect with you via Telegram within 24 hours.</span>
              </div>
            </form>
          </div>
        </div>
      </section>
    </main>

    <!-- Bottom Sticky Telegram Floating Shortcut for Mobile -->
    <aside class="sm:hidden fixed bottom-4 right-4 z-50">
      <a
        href="https://t.me/aerobyteacademy"
        target="_blank"
        rel="noopener noreferrer"
        class="flex items-center gap-2 bg-[#ff6b00] text-white px-4 py-2.5 rounded-full shadow-lg font-bold text-xs active:scale-95 transition"
      >
        <svg class="w-4 h-4 fill-current" viewBox="0 0 24 24">
          <path d="M12 0C5.373 0 0 5.373 0 12s5.373 12 12 12 12-5.373 12-12S18.627 0 12 0zm5.894 8.221l-1.97 9.28c-.145.658-.537.818-1.084.508l-3-2.21-1.446 1.394c-.16.16-.295.295-.605.295l.213-3.053 5.56-5.023c.242-.213-.054-.333-.373-.121l-6.871 4.326-2.962-.924c-.643-.204-.657-.643.136-.953l11.57-4.458c.538-.196 1.006.128.832.943z"/>
        </svg>
        <span>Telegram</span>
      </a>
    </aside>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'

const route = useRoute()
const router = useRouter()

// 3 distinct pages: 'community' | 'events' | 'store'
const activeTab = ref('community')

// Order Consultation Intake Form State
const orderForm = reactive({
  service: 'parts',
  experience: 'beginner',
  name: '',
  contact: '',
  budget: '',
  droneType: '',
  notes: ''
})

const orderSubmitted = ref(false)

function setTab(tab) {
  // Normalize 'hub' alias to 'events'
  const normalized = tab === 'hub' ? 'events' : tab
  activeTab.value = normalized
  router.replace({ query: { ...route.query, tab: normalized } })
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

function openOrderModal(serviceType) {
  activeTab.value = 'store'
  orderForm.service = serviceType
  router.replace({ query: { ...route.query, tab: 'store' } })
}

function submitOrderForm() {
  orderSubmitted.value = true
  setTimeout(() => {
    orderSubmitted.value = false
  }, 6000)
}

function parseInitialTab(tabParam) {
  if (!tabParam) return 'community'
  if (tabParam === 'hub' || tabParam === 'events') return 'events'
  if (tabParam === 'store') return 'store'
  return 'community'
}

// Sync tab with route query on load
onMounted(() => {
  const target = parseInitialTab(route.query.tab || route.query.page)
  activeTab.value = target
})

watch(() => route.query.tab, (newTab) => {
  if (newTab) {
    activeTab.value = parseInitialTab(newTab)
  }
})
</script>
