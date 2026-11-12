<template>
  <div class="min-h-screen bg-[#FAFAFA] dark:bg-[#05060B] text-[#111112] dark:text-white transition-colors pb-16 relative">

    <!-- Subtle Ambient Top Backdrop for Lower Canvas -->
    <div
      aria-hidden="true"
      class="pointer-events-none fixed inset-0 opacity-0 dark:opacity-100 transition-opacity duration-300"
      style="background: radial-gradient(65% 40% at 50% 0%, rgba(16, 52, 166, 0.16) 0%, rgba(255, 94, 14, 0.06) 45%, transparent 80%);"
    ></div>

    <!-- SECTION 1: Minimal Hero — Only 2 Text Lines + 1 Button + Full Architectural Portal -->
    <section class="relative overflow-hidden bg-[#FAFAFA] dark:bg-[#05060B]">
      <!-- Top Clean Typography Stack (Strictly 2 Lines + 1 CTA Button) -->
      <div class="relative z-10 mx-auto max-w-4xl px-4 sm:px-6 pt-10 sm:pt-14 pb-6 text-center">
        <h1 class="text-3xl sm:text-5xl lg:text-[60px] font-bold tracking-[-0.03em] leading-[1.08] text-[#111112] dark:text-white">
          {{ t('Precision Printing in Every Layer') }}
        </h1>

        <p class="mt-3 text-base sm:text-lg font-medium text-[#575757] dark:text-white/75">
          {{ t('Creality K2 Plus • 600 mm/s CoreXY & 16-Color CFS') }}
        </p>

        <div class="mt-6">
          <router-link
            to="/print/upload"
            class="inline-flex items-center gap-2 rounded-full bg-[#FF5E0E] hover:bg-[#FF764D] px-8 py-3.5 text-sm font-bold text-white shadow-[0_10px_25px_rgba(255,94,14,0.45)] active:scale-[0.99] transition"
          >
            <span>{{ t('Drop Your 3D File') }}</span>
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.4">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
            </svg>
          </router-link>
        </div>
      </div>

      <!-- Full-Bleed Architectural Daylight Portal Stage (Creality K2 Plus Unobstructed) -->
      <div class="relative mx-auto w-full max-w-[1680px] h-[300px] sm:h-[440px] lg:h-[560px] -mt-2">
        <img
          src="/assets/print/k2-plus-portal-hero.jpg"
          alt="Creality K2 Plus 3D Printer inside Architectural Studio"
          class="w-full h-full object-cover object-center opacity-95 dark:opacity-85"
        />
        <!-- Smooth top, bottom, and side feathers melting portal into #FAFAFA / #05060B -->
        <div aria-hidden="true" class="pointer-events-none absolute inset-x-0 top-0 h-16 sm:h-24 bg-gradient-to-b from-[#FAFAFA] via-[#FAFAFA]/60 to-transparent dark:from-[#05060B] dark:via-[#05060B]/60"></div>
        <div aria-hidden="true" class="pointer-events-none absolute inset-x-0 bottom-0 h-20 sm:h-28 bg-gradient-to-t from-[#FAFAFA] via-[#FAFAFA]/65 to-transparent dark:from-[#05060B] dark:via-[#05060B]/70"></div>
        <div aria-hidden="true" class="pointer-events-none hidden xl:block absolute inset-y-0 left-0 w-32 bg-gradient-to-r from-[#FAFAFA] to-transparent dark:from-[#05060B]"></div>
        <div aria-hidden="true" class="pointer-events-none hidden xl:block absolute inset-y-0 right-0 w-32 bg-gradient-to-l from-[#FAFAFA] to-transparent dark:from-[#05060B]"></div>
      </div>
    </section>

    <!-- SECTION 2: 3-Feature Bento Grid (Hero Highlights) -->
    <section id="features" class="mx-auto max-w-6xl px-4 sm:px-6 pb-12 sm:pb-16">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
        <div class="rounded-[28px] border border-black/[0.05] dark:border-white/10 bg-white dark:bg-[#111112] p-7 sm:p-8 shadow-xs flex flex-col justify-between">
          <div>
            <span class="inline-flex items-center rounded-full bg-[#F3F4F6] dark:bg-white/10 px-3 py-1 text-xs font-semibold text-[#575757] dark:text-white/75">
              {{ t('Hyper-Speed CoreXY') }}
            </span>
            <div class="mt-4 text-3xl sm:text-4xl font-bold tracking-tight text-[#111112] dark:text-white">
              600 mm/s
            </div>
            <p class="mt-2.5 text-sm text-[#575757] dark:text-white/65 leading-relaxed">
              {{ t('Closed-loop FOC step-servo motors and 30,000 mm/s² acceleration print prototypes at 5× standard speed.') }}
            </p>
          </div>
          <div class="mt-6 pt-4 border-t border-black/[0.05] dark:border-white/10 text-xs font-semibold text-[#FF5E0E]">
            0.1mm Active Input Shaping
          </div>
        </div>

        <div class="rounded-[28px] border border-black/[0.05] dark:border-white/10 bg-white dark:bg-[#111112] p-7 sm:p-8 shadow-xs flex flex-col justify-between">
          <div>
            <span class="inline-flex items-center rounded-full bg-[#F3F4F6] dark:bg-white/10 px-3 py-1 text-xs font-semibold text-[#575757] dark:text-white/75">
              {{ t('Industrial Build Volume') }}
            </span>
            <div class="mt-4 text-3xl sm:text-4xl font-bold tracking-tight text-[#111112] dark:text-white">
              350³ mm
            </div>
            <p class="mt-2.5 text-sm text-[#575757] dark:text-white/65 leading-relaxed">
              {{ t('Build full FPV drone frames, robotic arms, and large enclosures in a single seamless print.') }}
            </p>
          </div>
          <div class="mt-6 pt-4 border-t border-black/[0.05] dark:border-white/10 text-xs font-semibold text-[#FF5E0E]">
            Matrix Die-Cast Frame
          </div>
        </div>

        <div class="rounded-[28px] border border-black/[0.05] dark:border-white/10 bg-white dark:bg-[#111112] p-7 sm:p-8 shadow-xs flex flex-col justify-between">
          <div>
            <span class="inline-flex items-center rounded-full bg-[#F3F4F6] dark:bg-white/10 px-3 py-1 text-xs font-semibold text-[#575757] dark:text-white/75">
              {{ t('Smart Multi-Color') }}
            </span>
            <div class="mt-4 text-3xl sm:text-4xl font-bold tracking-tight text-[#111112] dark:text-white">
              16 Colors
            </div>
            <p class="mt-2.5 text-sm text-[#575757] dark:text-white/65 leading-relaxed">
              {{ t('Creality Filament System handles automatic spool switching, RFID detection, and sealed dry storage.') }}
            </p>
          </div>
          <div class="mt-6 pt-4 border-t border-black/[0.05] dark:border-white/10 text-xs font-semibold text-[#FF5E0E]">
            Auto-Refill & Breakage Sensor
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 3: Royal Blue Interactive Use-Case Showcase Banner -->
    <section class="mx-auto max-w-6xl px-4 sm:px-6 pb-12 sm:pb-16">
      <div
        class="rounded-[32px] p-7 sm:p-12 text-white relative overflow-hidden shadow-xl"
        style="background: linear-gradient(135deg, #1034A6 0%, #051036 100%);"
      >
        <div class="mx-auto max-w-2xl text-center">
          <h2 class="text-3xl sm:text-4xl lg:text-[42px] font-bold tracking-[-0.02em] leading-tight">
            {{ t('Build Without Limits on Creality K2 Plus') }}
          </h2>
          <p class="mt-3 text-sm sm:text-base text-white/75">
            {{ t('From carbon-reinforced FPV frames to multi-color student robotics assemblies, Creality K2 Plus turns CAD into flight-ready parts.') }}
          </p>
        </div>

        <!-- Active Showcase Panel -->
        <div class="mt-8 grid grid-cols-1 lg:grid-cols-12 gap-6 items-center rounded-[24px] border border-white/15 bg-black/25 backdrop-blur-md p-4 sm:p-6">
          <div class="lg:col-span-7 overflow-hidden rounded-2xl aspect-[16/10] bg-black/40">
            <img
              :src="activeMode.image"
              :alt="activeMode.title"
              class="w-full h-full object-cover transition-all duration-500"
            />
          </div>
          <div class="lg:col-span-5 space-y-4 px-1">
            <span class="inline-flex items-center rounded-full bg-white/15 border border-white/20 px-3 py-1 text-xs font-semibold text-[#C5E0F2]">
              {{ activeMode.tag }}
            </span>
            <h3 class="text-2xl font-bold text-white">{{ activeMode.title }}</h3>
            <p class="text-sm text-white/75 leading-relaxed">{{ activeMode.description }}</p>
            <div class="pt-2 flex flex-wrap gap-2">
              <span
                v-for="pill in activeMode.specs"
                :key="pill"
                class="rounded-full bg-white/10 px-3 py-1 text-xs font-medium text-white/90"
              >
                {{ pill }}
              </span>
            </div>
          </div>
        </div>

        <!-- 3 Circular Switcher Controls (Produck Style) -->
        <div class="mt-7 flex items-center justify-center gap-3.5">
          <button
            v-for="(mode, idx) in showcaseModes"
            :key="mode.id"
            type="button"
            @click="selectedModeIndex = idx"
            class="group flex items-center gap-2.5 rounded-full p-1.5 pr-4 border transition cursor-pointer"
            :class="selectedModeIndex === idx
              ? 'border-[#FF5E0E] bg-white text-[#111112] shadow-lg'
              : 'border-white/25 bg-white/10 text-white hover:bg-white/20'"
          >
            <img
              :src="mode.image"
              :alt="mode.label"
              class="h-8 w-8 rounded-full object-cover border border-black/10"
            />
            <span class="text-xs font-bold">{{ mode.label }}</span>
          </button>
        </div>
      </div>
    </section>

    <!-- SECTION 4: Dual Hardware Tech Showcase (CFS & 350°C Heated Chamber) -->
    <section id="technology" class="mx-auto max-w-6xl px-4 sm:px-6 pb-12 sm:pb-16">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <!-- Left Card: Multi-Color CFS -->
        <div class="rounded-[28px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111112] p-7 sm:p-9 flex flex-col justify-between shadow-xs">
          <div>
            <span class="inline-flex items-center rounded-full bg-[#F3F4F6] dark:bg-white/10 px-3.5 py-1 text-xs font-semibold text-[#575757] dark:text-white/80">
              {{ t('Automated Filament Switching') }}
            </span>
            <h3 class="mt-4 text-2xl sm:text-3xl font-bold tracking-tight text-[#111112] dark:text-white">
              {{ t('16-Color Smart CFS Unit') }}
            </h3>
            <p class="mt-2.5 text-sm sm:text-base text-[#575757] dark:text-white/65 leading-relaxed">
              {{ t('Seal out Cambodia humidity while switching effortlessly between colors or dissolvable support materials with zero manual spool swapping.') }}
            </p>
          </div>

          <div class="my-6 overflow-hidden rounded-2xl border border-black/[0.05] dark:border-white/10 bg-[#FAFAFA] dark:bg-black/40 aspect-[16/10]">
            <img
              src="/assets/print/k2-plus-cfs.jpg"
              alt="Creality K2 Plus CFS 4-Spool Multi-Color System"
              class="w-full h-full object-cover"
            />
          </div>

          <div class="flex flex-wrap gap-2">
            <span class="rounded-full bg-[#F3F4F6] dark:bg-white/10 px-3 py-1 text-xs font-medium text-[#111112] dark:text-white/85">Up to 16 Colors</span>
            <span class="rounded-full bg-[#F3F4F6] dark:bg-white/10 px-3 py-1 text-xs font-medium text-[#111112] dark:text-white/85">RFID Spool Sync</span>
            <span class="rounded-full bg-[#F3F4F6] dark:bg-white/10 px-3 py-1 text-xs font-medium text-[#111112] dark:text-white/85">Active Moisture Seal</span>
          </div>
        </div>

        <!-- Right Card: 350°C Unicorn Nozzle + Heated Chamber -->
        <div class="rounded-[28px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111112] p-7 sm:p-9 flex flex-col justify-between shadow-xs">
          <div>
            <span class="inline-flex items-center rounded-full bg-[#F3F4F6] dark:bg-white/10 px-3.5 py-1 text-xs font-semibold text-[#575757] dark:text-white/80">
              {{ t('Aerospace Composite Ready') }}
            </span>
            <h3 class="mt-4 text-2xl sm:text-3xl font-bold tracking-tight text-[#111112] dark:text-white">
              {{ t('350°C Nozzle & 60°C Chamber') }}
            </h3>
            <p class="mt-2.5 text-sm sm:text-base text-[#575757] dark:text-white/65 leading-relaxed">
              {{ t('An actively heated build chamber and hardened tri-metal Unicorn nozzle unlock strong ABS, ASA, and PA-CF carbon-fiber nylon parts.') }}
            </p>
          </div>

          <div class="my-6 overflow-hidden rounded-2xl border border-black/[0.05] dark:border-white/10 bg-[#0B0D14] aspect-[16/10]">
            <img
              src="/assets/print/k2-plus-extruder.jpg"
              alt="Creality K2 Plus High-Temp Direct Drive Extruder"
              class="w-full h-full object-cover"
            />
          </div>

          <div class="flex flex-wrap gap-2">
            <span class="rounded-full bg-[#F3F4F6] dark:bg-white/10 px-3 py-1 text-xs font-medium text-[#111112] dark:text-white/85">350°C Unicorn Nozzle</span>
            <span class="rounded-full bg-[#F3F4F6] dark:bg-white/10 px-3 py-1 text-xs font-medium text-[#111112] dark:text-white/85">60°C Heated Box</span>
            <span class="rounded-full bg-[#F3F4F6] dark:bg-white/10 px-3 py-1 text-xs font-medium text-[#111112] dark:text-white/85">PA-CF Carbon Ready</span>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 5: High-Velocity Prototyping Spotlight -->
    <section class="mx-auto max-w-4xl px-4 sm:px-6 py-10 sm:py-14 text-center">
      <div class="inline-flex items-center gap-2 rounded-full border border-black/[0.06] dark:border-white/15 bg-white dark:bg-white/10 px-4 py-1.5 text-xs font-medium text-[#575757] dark:text-white/80">
        <span class="h-2 w-2 rounded-full bg-[#FF5E0E]"></span>
        <span>{{ t('Speed that keeps innovation moving') }}</span>
      </div>

      <h2 class="mt-4 text-3xl sm:text-4xl lg:text-[44px] font-bold tracking-[-0.02em] text-[#111112] dark:text-white">
        {{ t('From CAD Upload to Ready Parts in Hours') }}
      </h2>

      <p class="mt-3 mx-auto max-w-xl text-base text-[#575757] dark:text-white/70">
        {{ t('Upload your STL or STEP model and our Creality K2 Plus prints crisp structural parts up to 5× faster — without layer ringing.') }}
      </p>

      <div class="mt-7">
        <router-link
          to="/print/upload"
          class="inline-flex items-center gap-2 rounded-full bg-[#FF5E0E] hover:bg-[#FF764D] px-7 py-3.5 text-sm font-bold text-white shadow-[0_10px_25px_rgba(255,94,14,0.45)] transition"
        >
          <span>{{ t('Upload 3D File & Quote') }}</span>
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
          </svg>
        </router-link>
      </div>
    </section>

    <!-- SECTION 6: Asymmetric Specs Bento Grid ("More Than Just a 3D Printer") -->
    <section id="specs" class="mx-auto max-w-6xl px-4 sm:px-6 pb-12 sm:pb-16">
      <div class="text-center mb-8">
        <h2 class="text-3xl sm:text-4xl font-bold tracking-[-0.02em] text-[#111112] dark:text-white">
          {{ t('More Than Just a 3D Printer') }}
        </h2>
        <p class="mt-2 text-sm sm:text-base text-[#575757] dark:text-white/65">
          {{ t('Every subsystem of the Creality K2 Plus is built for repeatable accuracy.') }}
        </p>
      </div>

      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        <div class="lg:col-span-2 rounded-[24px] border border-black/[0.05] dark:border-white/10 bg-[#05060B] text-white p-6 sm:p-7 flex flex-col justify-between relative overflow-hidden">
          <div aria-hidden="true" class="pointer-events-none absolute -right-10 -top-12 h-48 w-48 rounded-full bg-[#FF5E0E]/20 blur-3xl"></div>
          <div aria-hidden="true" class="pointer-events-none absolute -left-8 -bottom-10 h-40 w-40 rounded-full bg-[#1034A6]/25 blur-3xl"></div>
          <span class="relative z-10 text-xs font-bold uppercase tracking-wider text-[#FF5E0E]">Dual AI Guard</span>
          <div class="relative z-10 mt-6">
            <h3 class="text-xl font-bold">Chamber & Nozzle AI Cameras</h3>
            <p class="mt-2 text-sm text-white/70">Automatic flow-rate calibration and real-time spaghetti failure protection keep long overnight prints worry-free.</p>
          </div>
        </div>

        <div class="rounded-[24px] border border-black/[0.05] dark:border-white/10 bg-white dark:bg-[#111112] p-6 flex flex-col justify-between">
          <span class="text-2xl">⚡</span>
          <div class="mt-5">
            <h3 class="text-lg font-bold text-[#111112] dark:text-white">40 mm³/s High Flow</h3>
            <p class="mt-1.5 text-xs text-[#575757] dark:text-white/65">Unicorn quick-swap nozzle with titanium alloy throat for clean fast extrusion.</p>
          </div>
        </div>

        <div class="rounded-[24px] border border-black/[0.05] dark:border-white/10 bg-white dark:bg-[#111112] p-6 flex flex-col justify-between">
          <span class="text-2xl">📐</span>
          <div class="mt-5">
            <h3 class="text-lg font-bold text-[#111112] dark:text-white">Auto Tilt & Mesh</h3>
            <p class="mt-1.5 text-xs text-[#575757] dark:text-white/65">Dual independent Z-motors level the 350mm PEI plate automatically every print.</p>
          </div>
        </div>

        <div class="rounded-[24px] border border-black/[0.05] dark:border-white/10 bg-white dark:bg-[#111112] p-6 flex flex-col justify-between">
          <span class="text-2xl">🛡️</span>
          <div class="mt-5">
            <h3 class="text-lg font-bold text-[#111112] dark:text-white">Matrix Alloy Frame</h3>
            <p class="mt-1.5 text-xs text-[#575757] dark:text-white/65">Aerospace die-cast chassis eliminates vibration at 30,000 mm/s² acceleration.</p>
          </div>
        </div>

        <div class="rounded-[24px] border border-black/[0.05] dark:border-white/10 bg-white dark:bg-[#111112] p-6 flex flex-col justify-between">
          <span class="text-2xl">🌡️</span>
          <div class="mt-5">
            <h3 class="text-lg font-bold text-[#111112] dark:text-white">120°C Bed + 60°C Box</h3>
            <p class="mt-1.5 text-xs text-[#575757] dark:text-white/65">Active enclosure heater eliminates warping on large ABS & ASA parts.</p>
          </div>
        </div>

        <div class="lg:col-span-2 rounded-[24px] border border-black/[0.05] dark:border-white/10 bg-white dark:bg-[#111112] p-6 sm:p-7 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <span class="text-xs font-bold uppercase tracking-wider text-[#FF5E0E]">Instant Quotation</span>
            <h3 class="mt-1.5 text-xl font-bold text-[#111112] dark:text-white">Start From $0.08 / cm³</h3>
            <p class="mt-1 text-xs text-[#575757] dark:text-white/65">PLA, PETG, TPU 95A, ABS, ASA & PA-CF Nylon ready in Phnom Penh.</p>
          </div>
          <router-link
            to="/print/upload"
            class="shrink-0 inline-flex items-center justify-center rounded-full bg-[#FF5E0E] hover:bg-[#FF764D] px-5 py-2.5 text-xs font-bold text-white shadow-[0_8px_20px_rgba(255,94,14,0.4)] transition"
          >
            {{ t('Drop Your File') }}
          </router-link>
        </div>
      </div>
    </section>

    <!-- SECTION 7: Dark Workshop Lifestyle Banner -->
    <section class="mx-auto max-w-6xl px-4 sm:px-6 pb-12 sm:pb-16">
      <div class="relative rounded-[30px] overflow-hidden min-h-[380px] sm:min-h-[430px] flex flex-col justify-between p-7 sm:p-12 text-white border border-white/10">
        <img
          src="/assets/print/k2-plus-workshop.jpg"
          alt="Creality K2 Plus in AeroByte Robotics & Drone Lab"
          class="absolute inset-0 w-full h-full object-cover"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-black/90 via-black/45 to-black/55"></div>

        <div class="relative z-10 flex flex-col items-start">
          <span class="inline-flex items-center gap-1.5 rounded-full bg-white/12 backdrop-blur-md border border-white/20 px-3.5 py-1 text-xs font-semibold text-white">
            ✓ {{ t('Flagship Lab Hardware') }}
          </span>
          <h2 class="mt-4 max-w-xl text-3xl sm:text-4xl font-bold tracking-tight">
            {{ t('Built for Drones, Robotics & Real Prototypes') }}
          </h2>
          <p class="mt-2 text-sm text-white/75 max-w-md">
            {{ t('Precision hardware tuned daily by AeroByte Academy lab engineers.') }}
          </p>
        </div>

        <div class="relative z-10 mt-8 max-w-md rounded-2xl border border-white/15 bg-black/55 backdrop-blur-md p-4 sm:p-5">
          <p class="text-sm font-bold text-white">✦ Matrix Frame • ±0.1mm Tolerance</p>
          <p class="mt-1 text-xs text-white/75">Closed-loop step-servo motion guarantees bolt-ready alignment for motor mounts and enclosures.</p>
        </div>
      </div>
    </section>

    <!-- SECTION 8: Pricing Overview, Key Specs & Testimonials Carousel + Extruder Detail Card -->
    <section class="mx-auto max-w-6xl px-4 sm:px-6 pb-12 sm:pb-16">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-stretch">
        <!-- Left Info + Carousel -->
        <div class="lg:col-span-6 flex flex-col justify-between space-y-6">
          <div>
            <span class="inline-flex items-center gap-1.5 rounded-full border border-black/[0.08] dark:border-white/15 bg-white dark:bg-white/10 px-3.5 py-1 text-xs font-semibold text-[#111112] dark:text-white">
              <span class="h-1.5 w-1.5 rounded-full bg-emerald-500"></span>
              {{ t('Available Now') }}
            </span>

            <div class="mt-4 flex flex-wrap items-baseline justify-between gap-2">
              <h2 class="text-3xl sm:text-4xl font-bold tracking-tight text-[#111112] dark:text-white">Creality K2 Plus</h2>
              <span class="text-xl sm:text-2xl font-bold text-[#FF5E0E]">$0.08 / cm³</span>
            </div>

            <div class="mt-2.5 flex items-center gap-2">
              <div class="flex items-center text-[#FF5E0E] text-sm tracking-tight">★★★★★</div>
              <span class="text-xs font-medium text-[#575757] dark:text-white/65">4.9 / 5 • {{ t('Cambodia Maker Lab') }}</span>
            </div>

            <p class="mt-4 text-sm sm:text-base text-[#575757] dark:text-white/70 leading-relaxed">
              {{ t('Skip weeks of international shipping. Drop your 3D CAD files directly to our K2 Plus queue for rapid delivery or Phnom Penh lab pickup.') }}
            </p>

            <div class="mt-6">
              <router-link
                to="/print/upload"
                class="block w-full sm:w-auto sm:inline-flex items-center justify-center gap-2 rounded-full bg-[#FF5E0E] hover:bg-[#FF764D] px-8 py-4 text-sm font-bold text-white shadow-[0_10px_25px_rgba(255,94,14,0.45)] transition text-center"
              >
                <span>{{ t('Upload Your File & Quote Now') }}</span>
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.4">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
                </svg>
              </router-link>
            </div>

            <!-- Two Quick Spec Pills -->
            <div class="mt-5 grid grid-cols-2 gap-3">
              <div class="rounded-2xl border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111112] px-4 py-3 flex items-center gap-3">
                <span class="text-lg">📦</span>
                <span class="text-xs font-bold text-[#111112] dark:text-white">350×350×350 mm</span>
              </div>
              <div class="rounded-2xl border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111112] px-4 py-3 flex items-center gap-3">
                <span class="text-lg">🎨</span>
                <span class="text-xs font-bold text-[#111112] dark:text-white">16-Color CFS</span>
              </div>
            </div>
          </div>

          <!-- Interactive Testimonials Carousel -->
          <div class="rounded-[24px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111112] p-6">
            <div class="flex items-center justify-between mb-3">
              <div class="flex items-center gap-3">
                <div class="flex h-10 w-10 items-center justify-center rounded-full bg-[#FF5E0E]/15 text-[#FF5E0E] font-bold text-sm">
                  {{ currentReview.initials }}
                </div>
                <div>
                  <p class="text-sm font-bold text-[#111112] dark:text-white">{{ currentReview.author }}</p>
                  <p class="text-[11px] text-[#696969] dark:text-white/55">{{ currentReview.role }} • ★ {{ currentReview.rating }}</p>
                </div>
              </div>
              <div class="flex items-center gap-1.5">
                <button
                  type="button"
                  @click="prevReview"
                  aria-label="Previous review"
                  class="h-8 w-8 rounded-full border border-black/10 dark:border-white/15 flex items-center justify-center text-xs font-bold text-[#111112] dark:text-white hover:border-[#FF5E0E] cursor-pointer"
                >
                  ←
                </button>
                <button
                  type="button"
                  @click="nextReview"
                  aria-label="Next review"
                  class="h-8 w-8 rounded-full border border-black/10 dark:border-white/15 flex items-center justify-center text-xs font-bold text-[#111112] dark:text-white hover:border-[#FF5E0E] cursor-pointer"
                >
                  →
                </button>
              </div>
            </div>
            <p class="text-sm text-[#575757] dark:text-white/75 leading-relaxed">
              "{{ currentReview.quote }}"
            </p>
          </div>
        </div>

        <!-- Right Exploded Extruder Showcase Card -->
        <div class="lg:col-span-6 rounded-[30px] border border-black/[0.06] dark:border-white/10 bg-[#0B0D14] text-white p-6 sm:p-8 flex flex-col justify-between overflow-hidden">
          <div class="overflow-hidden rounded-2xl aspect-[4/3]">
            <img
              src="/assets/print/k2-plus-extruder.jpg"
              alt="Creality K2 Plus Unicorn Direct-Drive Cutaway"
              class="w-full h-full object-cover"
            />
          </div>
          <div class="mt-6">
            <span class="text-xs font-bold uppercase tracking-wider text-[#FF5E0E]">Direct-Drive Precision</span>
            <h3 class="mt-1.5 text-2xl font-bold">Unicorn Quick-Swap Tri-Metal Nozzle</h3>
            <p class="mt-2 text-sm text-white/70 leading-relaxed">
              Hardened steel tip meets high-conductivity copper alloy up to 350°C — engineered for clean overhangs and industrial composites.
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 9: 6-Feature Dark Photo Bento Grid -->
    <section class="mx-auto max-w-6xl px-4 sm:px-6 pb-12 sm:pb-16">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <div
          v-for="item in photoGridFeatures"
          :key="item.title"
          class="rounded-[24px] bg-[#0B0D14] text-white p-7 border border-white/10 relative overflow-hidden"
        >
          <div class="absolute -right-6 -top-6 h-28 w-28 rounded-full bg-[#FF5E0E]/15 blur-2xl"></div>
          <span class="text-xs font-bold text-[#FF5E0E] uppercase tracking-wider">{{ item.badge }}</span>
          <h3 class="mt-3 text-xl font-bold">{{ item.title }}</h3>
          <p class="mt-2 text-sm text-white/70 leading-relaxed">{{ item.desc }}</p>
        </div>
      </div>
    </section>

    <!-- SECTION 10: FAQ Accordion (Produck Interactive Highlight Style) -->
    <section id="faq" class="mx-auto max-w-6xl px-4 sm:px-6 pb-12 sm:pb-16">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <div class="lg:col-span-5 lg:sticky lg:top-24">
          <div class="inline-flex items-center gap-2 rounded-full border border-black/[0.06] dark:border-white/15 bg-white dark:bg-white/10 px-3.5 py-1 text-xs font-semibold text-[#111112] dark:text-white">
            <span>💡</span>
            <span>F.A.Q</span>
          </div>
          <h2 class="mt-4 text-3xl sm:text-4xl font-bold tracking-tight text-[#111112] dark:text-white">
            {{ t('Everything You Need to Know About Creality K2 Plus') }}
          </h2>
          <p class="mt-3 text-sm sm:text-base text-[#575757] dark:text-white/65">
            {{ t('Supported CAD file formats, build dimensions, material strengths, and turnaround timings.') }}
          </p>
          <div class="mt-6">
            <router-link
              to="/print/upload"
              class="inline-flex items-center gap-2 rounded-full bg-[#FF5E0E] hover:bg-[#FF764D] px-6 py-3 text-xs font-bold text-white shadow-[0_8px_20px_rgba(255,94,14,0.4)] transition"
            >
              {{ t('Drop Your 3D File Now') }}
            </router-link>
          </div>
        </div>

        <div class="lg:col-span-7 space-y-3">
          <div
            v-for="(faq, idx) in faqs"
            :key="faq.q"
            class="rounded-[20px] border bg-white dark:bg-[#111112] transition-all overflow-hidden"
            :class="openFaqIndex === idx
              ? 'border-[#FF5E0E] shadow-sm'
              : 'border-black/[0.07] dark:border-white/10'"
          >
            <button
              type="button"
              @click="toggleFaq(idx)"
              class="w-full px-6 py-4.5 flex items-center justify-between gap-4 text-left cursor-pointer"
            >
              <span
                class="text-sm sm:text-base font-semibold transition-colors"
                :class="openFaqIndex === idx ? 'text-[#FF5E0E]' : 'text-[#111112] dark:text-white'"
              >
                {{ faq.q }}
              </span>
              <svg
                class="w-4 h-4 shrink-0 transition-transform duration-200"
                :class="openFaqIndex === idx ? 'rotate-180 text-[#FF5E0E]' : 'text-[#575757] dark:text-white/60'"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2.2"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
              </svg>
            </button>
            <div v-show="openFaqIndex === idx" class="px-6 pb-5 text-sm text-[#575757] dark:text-white/70 leading-relaxed">
              {{ faq.a }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 11: Dark Final CTA Card -->
    <section class="mx-auto max-w-6xl px-4 sm:px-6">
      <div
        class="rounded-[30px] p-8 sm:p-14 text-white flex flex-col lg:flex-row items-start lg:items-center justify-between gap-8 border border-white/10 shadow-2xl"
        style="background: linear-gradient(90deg, #000000 0%, #161618 100%);"
      >
        <div class="max-w-xl">
          <span class="inline-flex items-center rounded-full bg-white/12 border border-white/20 px-3.5 py-1 text-xs font-semibold text-white">
            ✓ {{ t('Instant Print Queue') }}
          </span>
          <h2 class="mt-4 text-3xl sm:text-4xl font-bold tracking-tight">
            {{ t('Ready to Print on Creality K2 Plus?') }}
          </h2>
          <p class="mt-3 text-sm sm:text-base text-white/75 leading-relaxed">
            {{ t('Drop your STL, STEP, OBJ, or 3MF files into our uploader to calculate price instantly and queue your prototype.') }}
          </p>
        </div>

        <router-link
          to="/print/upload"
          class="shrink-0 inline-flex items-center gap-2.5 rounded-full bg-[#FF5E0E] hover:bg-[#FF764D] px-8 py-4 text-sm font-bold text-white shadow-[0_10px_25px_rgba(255,94,14,0.45)] transition"
        >
          <span>{{ t('Go to 3D File Upload') }}</span>
          <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.4">
            <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
          </svg>
        </router-link>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from '../i18n'

const { t } = useI18n()

// Section 3 Interactive Use-Case Switcher
const selectedModeIndex = ref(0)
const showcaseModes = [
  {
    id: 'workshop',
    label: 'FPV & Drones',
    tag: 'Aerospace Carbon Composites',
    title: 'Crash-Proof Motor Mounts & Drone Frames',
    description: 'Print high-stiffness PA-CF carbon-fiber frames, TPU vibration dampers, and custom GoPro cages inside the heated 60°C chamber.',
    image: '/assets/print/k2-plus-workshop.jpg',
    specs: ['PA-CF Carbon Nylon', 'TPU 95A Shock Mounts', '350mm Bed Size']
  },
  {
    id: 'cfs',
    label: '16-Color CFS',
    tag: 'Automated Spool System',
    title: 'Multi-Color Enclosures & Robotics Parts',
    description: 'Combine brand logos, color-coded wiring channels, and dissolvable supports seamlessly using up to four chained CFS units.',
    image: '/assets/print/k2-plus-cfs.jpg',
    specs: ['Up to 16 Colors', 'RFID Auto-Detect', 'Humidity Controlled']
  },
  {
    id: 'extruder',
    label: 'Mechanical Precision',
    tag: '350°C Direct-Drive Core',
    title: 'Functional Gears, Brackets & Tooling',
    description: 'Closed-loop step-servo motors eliminate ringing at 600 mm/s so planetary gears and bolt patterns assemble straight off the build plate.',
    image: '/assets/print/k2-plus-extruder.jpg',
    specs: ['600 mm/s CoreXY', '±0.1mm Tolerance', 'Unicorn 350°C Nozzle']
  }
]

const activeMode = computed(() => showcaseModes[selectedModeIndex.value])

// Section 8 Testimonials Carousel
const reviewIndex = ref(0)
const reviews = [
  {
    initials: 'SD',
    author: 'Sokha D.',
    role: 'FPV Drone Builder • Phnom Penh',
    rating: '5.0/5',
    quote: 'Printed a custom 5-inch Cinewhoop guard and TPU GoPro mount on the K2 Plus. Bolt holes lined up dead-on and arrived the next day.'
  },
  {
    initials: 'DV',
    author: 'Dara V.',
    role: 'Robotics Engineering Student',
    rating: '4.9/5',
    quote: 'Uploading our STEP gears took 30 seconds and the 16-color CFS printed clear assembly labels right onto our robot chassis.'
  },
  {
    initials: 'MK',
    author: 'Maly K.',
    role: 'Product Prototyper',
    rating: '4.9/5',
    quote: 'Having a 350mm chamber locally saved our capstone project — no 3-week overseas wait and super clean matte finish.'
  }
]

const currentReview = computed(() => reviews[reviewIndex.value])
function prevReview() {
  reviewIndex.value = (reviewIndex.value - 1 + reviews.length) % reviews.length
}
function nextReview() {
  reviewIndex.value = (reviewIndex.value + 1) % reviews.length
}

// Section 9: 6-Feature Visual Grid
const photoGridFeatures = [
  {
    badge: '01 • File Upload',
    title: 'Instant CAD Dropzone',
    desc: 'Drag and drop .STL, .STP, .STEP, .OBJ, or .3MF assemblies straight from Fusion 360 or SolidWorks.'
  },
  {
    badge: '02 • Transparent Quote',
    title: 'Live KHR & USD Pricing',
    desc: 'See exact weight, base setup, material rates, and bulk discounts update dynamically in real time.'
  },
  {
    badge: '03 • Smart CFS',
    title: 'Multi-Color Sequencing',
    desc: 'Highlight safety zones, logos, or tactile labels with automated multi-filament purging.'
  },
  {
    badge: '04 • Fast Turnaround',
    title: 'Phnom Penh Lab Pickup',
    desc: 'Rapid local production in our Ta Khmau engineering lab with express courier delivery available.'
  },
  {
    badge: '05 • Composites',
    title: '350°C Carbon-Fiber Parts',
    desc: 'Heat-resistant PA-CF and ABS enclosures engineered for outdoor tropical sun and drone motors.'
  },
  {
    badge: '06 • AI Quality',
    title: 'Dual AI Flow Inspection',
    desc: 'Live optical monitoring and pre-slice engineer checks ensure every part arrives clean and strong.'
  }
]

// Section 10: Interactive FAQ Accordion
const openFaqIndex = ref(0)
const faqs = [
  {
    q: 'What 3D CAD file formats can I drop into the uploader?',
    a: 'We support .STL, .STP, .STEP, .OBJ, and .3MF files. STEP assemblies are great for smooth curved industrial components, while STL and 3MF are ready for instant slicing.'
  },
  {
    q: 'How large can a single 3D print be on the Creality K2 Plus?',
    a: 'The Creality K2 Plus offers a massive 350 × 350 × 350 mm single-piece build volume, allowing full multi-rotor frames, oversized robotics brackets, and full-scale enclosures without splitting parts.'
  },
  {
    q: 'Can I request multi-color printing on my model?',
    a: 'Yes! Using the Creality Filament System (CFS), we can print multi-color accents, logos, and dual-material breakaway supports on the file upload page by selecting CFS Multi-Color.'
  },
  {
    q: 'Which materials are best for FPV drones and outdoor robotics?',
    a: 'For rigid motor arms and electronics plates, we recommend PA-CF Carbon Fiber Nylon or ABS/ASA printed inside the 60°C heated chamber. For shock-absorbing mounts, choose TPU 95A.'
  },
  {
    q: 'How fast is the turnaround in Cambodia?',
    a: 'Most single-color PLA/PETG/TPU prototypes are ready for pickup or Phnom Penh delivery within 24 to 48 hours thanks to the K2 Plus 600 mm/s CoreXY speed.'
  },
  {
    q: 'How is the final price calculated?',
    a: 'On our upload page, you receive an instant baseline quote calculated from estimated volume, material tier, infill percentage, and post-processing, with volume discounts for 5+ parts.'
  }
]

function toggleFaq(index) {
  openFaqIndex.value = openFaqIndex.value === index ? -1 : index
}
</script>
