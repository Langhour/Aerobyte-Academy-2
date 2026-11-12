<template>
  <div class="min-h-screen bg-[#F8F9FA] dark:bg-[#090A0F] text-[#111112] dark:text-white transition-colors pb-20">

    <!-- SECTION 1: Minimal Hero — Only 2 Text Lines + 1 Button + Architectural Daylight Portal -->
    <section class="relative overflow-hidden bg-[#F8F9FA] dark:bg-[#090A0F]">
      <div class="relative z-10 mx-auto max-w-4xl px-6 pt-12 sm:pt-16 pb-6 text-center">
        <h1 class="text-4xl sm:text-5xl lg:text-[62px] font-bold tracking-[-0.03em] leading-[1.08] text-[#111112] dark:text-white">
          {{ t('Precision Printing in Every Layer') }}
        </h1>

        <p class="mt-3.5 text-base sm:text-lg font-medium text-[#575757] dark:text-white/70">
          {{ t('Creality K2 Plus • 600 mm/s CoreXY & 16-Color CFS') }}
        </p>

        <div class="mt-7">
          <router-link
            to="/print/upload"
            class="inline-flex items-center gap-2 rounded-full bg-[#FF5E0E] hover:bg-[#FF764D] px-8 py-3.5 text-sm font-bold text-white shadow-[0_10px_25px_rgba(255,94,14,0.38)] active:scale-[0.99] transition"
          >
            <span>{{ t('Drop Your 3D File') }}</span>
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
            </svg>
          </router-link>
        </div>
      </div>

      <!-- Unobstructed Architectural Studio Stage -->
      <div class="relative mx-auto w-full max-w-[1600px] h-[300px] sm:h-[440px] lg:h-[560px] -mt-2">
        <img
          src="/assets/print/k2-plus-portal-hero.jpg"
          alt="Creality K2 Plus 3D Printer inside Architectural Studio"
          class="w-full h-full object-cover object-center opacity-95 dark:opacity-85"
        />
        <div aria-hidden="true" class="pointer-events-none absolute inset-x-0 top-0 h-16 sm:h-24 bg-gradient-to-b from-[#F8F9FA] via-[#F8F9FA]/60 to-transparent dark:from-[#090A0F] dark:via-[#090A0F]/60"></div>
        <div aria-hidden="true" class="pointer-events-none absolute inset-x-0 bottom-0 h-24 sm:h-32 bg-gradient-to-t from-[#F8F9FA] via-[#F8F9FA]/70 to-transparent dark:from-[#090A0F] dark:via-[#090A0F]/75"></div>
        <div aria-hidden="true" class="pointer-events-none hidden xl:block absolute inset-y-0 left-0 w-32 bg-gradient-to-r from-[#F8F9FA] to-transparent dark:from-[#090A0F]"></div>
        <div aria-hidden="true" class="pointer-events-none hidden xl:block absolute inset-y-0 right-0 w-32 bg-gradient-to-l from-[#F8F9FA] to-transparent dark:from-[#090A0F]"></div>
      </div>
    </section>

    <!-- SECTION 2: Produck-Style 2-Tier Bento Highlights (1 Wide Visual Card + 2 Clean Cards) -->
    <section class="mx-auto max-w-[1160px] px-6 py-16 sm:py-24">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Full-Width Top Bento Card -->
        <div class="md:col-span-2 rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-8 sm:p-12 shadow-[0_10px_30px_rgba(0,0,0,0.03)] grid grid-cols-1 lg:grid-cols-12 gap-8 items-center overflow-hidden">
          <div class="lg:col-span-5 space-y-3">
            <span class="inline-flex items-center rounded-full border border-black/[0.08] dark:border-white/15 bg-[#F8F9FA] dark:bg-white/5 px-3.5 py-1 text-xs font-medium text-[#575757] dark:text-white/75">
              {{ t('Hyper-Speed CoreXY') }}
            </span>
            <h2 class="text-3xl sm:text-4xl font-bold tracking-[-0.02em] text-[#111112] dark:text-white">
              600 mm/s Precision
            </h2>
            <p class="text-sm sm:text-base text-[#575757] dark:text-white/65 leading-relaxed">
              {{ t('Step-servo motion prints strong engineering prototypes up to 5× faster.') }}
            </p>
          </div>
          <div class="lg:col-span-7 w-full overflow-hidden rounded-[24px] bg-[#0B0D14] aspect-[16/9]">
            <img
              src="/assets/print/k2-plus-extruder.jpg"
              alt="Creality K2 Plus High-Speed Direct Drive Extruder"
              class="w-full h-full object-cover"
            />
          </div>
        </div>

        <!-- Half-Width Card Left -->
        <div class="rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-8 sm:p-10 shadow-[0_10px_30px_rgba(0,0,0,0.03)] flex flex-col justify-between">
          <div>
            <div class="flex h-11 w-11 items-center justify-center rounded-full bg-[#F3F4F6] dark:bg-white/10 text-[#1F2937] dark:text-white">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
              </svg>
            </div>
            <h3 class="mt-6 text-2xl sm:text-3xl font-bold tracking-tight text-[#111112] dark:text-white">
              350³ mm Volume
            </h3>
            <p class="mt-2.5 text-sm sm:text-base text-[#575757] dark:text-white/65">
              {{ t('Print full drone frames and robotics parts in one seamless piece.') }}
            </p>
          </div>
        </div>

        <!-- Half-Width Card Right -->
        <div class="rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-8 sm:p-10 shadow-[0_10px_30px_rgba(0,0,0,0.03)] flex flex-col justify-between">
          <div>
            <div class="flex h-11 w-11 items-center justify-center rounded-full bg-[#F3F4F6] dark:bg-white/10 text-[#1F2937] dark:text-white">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6.429 9.75L2.25 12l4.179 2.25m0-4.5l5.571 3 5.571-3m-11.142 0L2.25 7.5 12 2.25l9.75 5.25-4.179 2.25m0 0L21.75 12l-4.179 2.25m0 0l4.179 2.25L12 21.75 2.25 16.5l4.179-2.25m11.142 0l-5.571 3-5.571-3" />
              </svg>
            </div>
            <h3 class="mt-6 text-2xl sm:text-3xl font-bold tracking-tight text-[#111112] dark:text-white">
              16-Color Smart CFS
            </h3>
            <p class="mt-2.5 text-sm sm:text-base text-[#575757] dark:text-white/65">
              {{ t('Automated RFID spool switching inside a sealed dry enclosure.') }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 3: Calm Monochrome Hardware Showcase Banner (Replaces Saturated Blue Block) -->
    <section class="mx-auto max-w-[1160px] px-6 pb-16 sm:pb-24">
      <div class="rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-6 sm:p-10 shadow-[0_10px_30px_rgba(0,0,0,0.03)]">
        <div class="mx-auto max-w-2xl text-center">
          <h2 class="text-3xl sm:text-4xl font-bold tracking-[-0.02em] text-[#111112] dark:text-white">
            {{ activeMode.title }}
          </h2>
          <p class="mt-2.5 text-sm sm:text-base text-[#575757] dark:text-white/65">
            {{ activeMode.description }}
          </p>
        </div>

        <div class="mt-8 w-full h-[240px] sm:h-[400px] lg:h-[500px] overflow-hidden rounded-[24px] bg-[#F3F4F6] dark:bg-black/40">
          <img
            :src="activeMode.image"
            :alt="activeMode.title"
            class="w-full h-full object-cover transition-all duration-500"
          />
        </div>

        <!-- Clean Monochrome Switcher Pills -->
        <div class="mt-6 flex flex-wrap items-center justify-center gap-2.5">
          <button
            v-for="(mode, idx) in showcaseModes"
            :key="mode.id"
            type="button"
            @click="selectedModeIndex = idx"
            class="inline-flex items-center gap-2 rounded-full px-4 py-2 text-xs font-semibold border transition cursor-pointer"
            :class="selectedModeIndex === idx
              ? 'border-[#111112] dark:border-white bg-[#111112] dark:bg-white text-white dark:text-[#111112]'
              : 'border-black/[0.08] dark:border-white/15 bg-[#F8F9FA] dark:bg-white/5 text-[#575757] dark:text-white/75 hover:border-black/25'"
          >
            {{ mode.label }}
          </button>
        </div>
      </div>
    </section>

    <!-- SECTION 4: Clean 2-Column Hardware Comparison (CFS vs Heated Chamber) -->
    <section class="mx-auto max-w-[1160px] px-6 pb-16 sm:pb-24">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div class="rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-8 sm:p-10 shadow-[0_10px_30px_rgba(0,0,0,0.03)] flex flex-col justify-between">
          <div>
            <h3 class="text-2xl font-bold tracking-tight text-[#111112] dark:text-white">
              {{ t('16-Color Smart CFS Unit') }}
            </h3>
            <p class="mt-2 text-sm text-[#575757] dark:text-white/65">
              {{ t('Zero manual spool swaps with automatic moisture protection.') }}
            </p>
          </div>
          <div class="mt-7 w-full overflow-hidden rounded-[22px] aspect-[16/10] bg-[#F8F9FA] dark:bg-black/30">
            <img
              src="/assets/print/k2-plus-cfs.jpg"
              alt="Creality K2 Plus CFS Multi-Color Unit"
              class="w-full h-full object-cover"
            />
          </div>
        </div>

        <div class="rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-8 sm:p-10 shadow-[0_10px_30px_rgba(0,0,0,0.03)] flex flex-col justify-between">
          <div>
            <h3 class="text-2xl font-bold tracking-tight text-[#111112] dark:text-white">
              {{ t('350°C Nozzle & 60°C Chamber') }}
            </h3>
            <p class="mt-2 text-sm text-[#575757] dark:text-white/65">
              {{ t('Warp-free ABS, ASA, and carbon-fiber PA-CF structural prints.') }}
            </p>
          </div>
          <div class="mt-7 w-full overflow-hidden rounded-[22px] aspect-[16/10] bg-[#0B0D14]">
            <img
              src="/assets/print/k2-plus-extruder.jpg"
              alt="Creality K2 Plus 350C Nozzle"
              class="w-full h-full object-cover"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 5: Produck Sticky 2-Column Specs Layout (Uniform Monochrome White Cards + Sticky Right Summary) -->
    <section class="mx-auto max-w-[1160px] px-6 pb-16 sm:pb-24">
      <div class="mb-10 max-w-xl">
        <h2 class="text-3xl sm:text-4xl font-bold tracking-[-0.02em] text-[#111112] dark:text-white">
          {{ t('More Than Just a 3D Printer') }}
        </h2>
        <p class="mt-2.5 text-sm sm:text-base text-[#575757] dark:text-white/65">
          {{ t('Every subsystem of the Creality K2 Plus is built for repeatable accuracy.') }}
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <!-- Left Stacked Uniform White Feature Cards -->
        <div class="lg:col-span-7 space-y-4">
          <div
            v-for="spec in uniformSpecs"
            :key="spec.title"
            class="rounded-[24px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-6 sm:p-7 shadow-[0_4px_16px_rgba(0,0,0,0.02)] flex items-start gap-5"
          >
            <div class="flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-[#F3F4F6] dark:bg-white/10 text-[#1F2937] dark:text-white">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6">
                <path stroke-linecap="round" stroke-linejoin="round" :d="spec.iconPath" />
              </svg>
            </div>
            <div>
              <h3 class="text-lg font-bold text-[#111112] dark:text-white">{{ spec.title }}</h3>
              <p class="mt-1 text-sm text-[#575757] dark:text-white/65">{{ spec.desc }}</p>
            </div>
          </div>
        </div>

        <!-- Right Sticky Hardware Summary Card (Produck Pattern) -->
        <div class="lg:col-span-5 lg:sticky lg:top-24 rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-8 shadow-[0_10px_30px_rgba(0,0,0,0.03)]">
          <div class="w-full overflow-hidden rounded-[22px] bg-[#F8F9FA] dark:bg-black/30 aspect-[4/3]">
            <img
              src="/assets/print/k2-plus-hero.jpg"
              alt="Creality K2 Plus"
              class="w-full h-full object-cover"
            />
          </div>
          <div class="mt-6 flex items-baseline justify-between">
            <h3 class="text-2xl font-bold text-[#111112] dark:text-white">Creality K2 Plus</h3>
            <span class="text-base font-bold text-[#FF5E0E]">$0.08 / cm³</span>
          </div>
          <p class="mt-2 text-sm text-[#575757] dark:text-white/65">
            {{ t('Upload your CAD files for instant pricing and local Phnom Penh printing.') }}
          </p>
          <router-link
            to="/print/upload"
            class="mt-6 w-full inline-flex items-center justify-center gap-2 rounded-full bg-[#FF5E0E] hover:bg-[#FF764D] px-6 py-3.5 text-sm font-bold text-white shadow-[0_10px_25px_rgba(255,94,14,0.38)] transition"
          >
            <span>{{ t('Drop Your 3D File') }}</span>
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
            </svg>
          </router-link>
        </div>
      </div>
    </section>

    <!-- SECTION 6: Clean Full-Bleed Workshop Photo Banner (Zero Floating Boxes) -->
    <section class="mx-auto max-w-[1160px] px-6 pb-16 sm:pb-24">
      <div class="relative rounded-[32px] overflow-hidden min-h-[380px] sm:min-h-[440px] flex items-end p-8 sm:p-12 text-white">
        <img
          src="/assets/print/k2-plus-workshop.jpg"
          alt="Creality K2 Plus in AeroByte Robotics & Drone Lab"
          class="absolute inset-0 w-full h-full object-cover"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent"></div>

        <div class="relative z-10 max-w-lg">
          <h2 class="text-3xl sm:text-4xl font-bold tracking-tight text-white">
            {{ t('Built for Drones, Robotics & Real Prototypes') }}
          </h2>
          <p class="mt-2.5 text-sm sm:text-base text-white/80">
            {{ t('Precision hardware tuned daily by AeroByte Academy lab engineers.') }}
          </p>
        </div>
      </div>
    </section>

    <!-- SECTION 7: Clean 50/50 Split — Pricing, Specs & Reviews + Tall Studio Render -->
    <section class="mx-auto max-w-[1160px] px-6 pb-16 sm:pb-24">
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-8 items-stretch">
        <!-- Left Info + Monochrome Specs + Customer Quote -->
        <div class="flex flex-col justify-between space-y-8 py-2">
          <div>
            <span class="inline-flex items-center rounded-full border border-black/[0.08] dark:border-white/15 bg-white dark:bg-white/5 px-3.5 py-1 text-xs font-medium text-[#575757] dark:text-white/80">
              {{ t('Available Now') }}
            </span>

            <div class="mt-4 flex items-baseline justify-between gap-2">
              <h2 class="text-3xl sm:text-4xl font-bold tracking-tight text-[#111112] dark:text-white">Creality K2 Plus</h2>
              <span class="text-xl font-bold text-[#FF5E0E]">From $0.08 / cm³</span>
            </div>

            <div class="mt-2.5 flex items-center gap-2">
              <span class="text-[#FF5E0E] text-sm">★★★★★</span>
              <span class="text-xs font-medium text-[#575757] dark:text-white/65">4.9 / 5 • {{ t('Cambodia Maker Lab') }}</span>
            </div>

            <p class="mt-4 text-sm sm:text-base text-[#575757] dark:text-white/70 leading-relaxed">
              {{ t('Skip weeks of international shipping with instant Phnom Penh CAD printing.') }}
            </p>

            <!-- 2 Clean Monochrome Metric Pills (Zero Emojis) -->
            <div class="mt-6 grid grid-cols-2 gap-3.5">
              <div class="rounded-2xl border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] px-4 py-3.5 flex items-center gap-3">
                <svg class="w-4 h-4 shrink-0 text-[#575757] dark:text-white/75" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
                </svg>
                <span class="text-xs font-bold text-[#111112] dark:text-white">350×350×350 mm</span>
              </div>
              <div class="rounded-2xl border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] px-4 py-3.5 flex items-center gap-3">
                <svg class="w-4 h-4 shrink-0 text-[#575757] dark:text-white/75" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M6.429 9.75L2.25 12l4.179 2.25m0-4.5l5.571 3 5.571-3m-11.142 0L2.25 7.5 12 2.25l9.75 5.25-4.179 2.25m0 0L21.75 12l-4.179 2.25m0 0l4.179 2.25L12 21.75 2.25 16.5l4.179-2.25m11.142 0l-5.571 3-5.571-3" />
                </svg>
                <span class="text-xs font-bold text-[#111112] dark:text-white">16-Color CFS</span>
              </div>
            </div>
          </div>

          <!-- Clean Review Card -->
          <div class="rounded-[24px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-6 shadow-[0_4px_16px_rgba(0,0,0,0.02)]">
            <div class="flex items-center justify-between mb-3">
              <div>
                <p class="text-sm font-bold text-[#111112] dark:text-white">{{ currentReview.author }}</p>
                <p class="text-xs text-[#696969] dark:text-white/55">{{ currentReview.role }}</p>
              </div>
              <div class="flex items-center gap-1.5">
                <button
                  type="button"
                  @click="prevReview"
                  aria-label="Previous review"
                  class="h-8 w-8 rounded-full border border-black/10 dark:border-white/15 flex items-center justify-center text-xs text-[#111112] dark:text-white hover:border-black/30 cursor-pointer"
                >
                  ←
                </button>
                <button
                  type="button"
                  @click="nextReview"
                  aria-label="Next review"
                  class="h-8 w-8 rounded-full border border-black/10 dark:border-white/15 flex items-center justify-center text-xs text-[#111112] dark:text-white hover:border-black/30 cursor-pointer"
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

        <!-- Right Tall Studio Render Card -->
        <div class="rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-6 sm:p-8 flex items-center justify-center shadow-[0_10px_30px_rgba(0,0,0,0.03)]">
          <div class="overflow-hidden rounded-[24px] w-full aspect-[4/3] bg-[#0B0D14]">
            <img
              src="/assets/print/k2-plus-extruder.jpg"
              alt="Creality K2 Plus Unicorn Extruder Cutaway"
              class="w-full h-full object-cover"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 8: 6-Feature Clean Photographic Bento Grid -->
    <section class="mx-auto max-w-[1160px] px-6 pb-16 sm:pb-24">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <div
          v-for="item in photoGridFeatures"
          :key="item.title"
          class="relative rounded-[28px] overflow-hidden min-h-[260px] flex items-end p-7 text-white"
        >
          <img
            :src="item.image"
            :alt="item.title"
            class="absolute inset-0 w-full h-full object-cover"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/35 to-black/15"></div>
          <div class="relative z-10">
            <h3 class="text-lg font-bold text-white">{{ item.title }}</h3>
            <p class="mt-1 text-xs sm:text-sm text-white/80">{{ item.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 9: Minimal 2-Column Produck FAQ Accordion -->
    <section id="faq" class="mx-auto max-w-[1160px] px-6 pb-16 sm:pb-24">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-12 items-start">
        <div class="lg:col-span-5 lg:sticky lg:top-24">
          <div class="inline-flex items-center gap-2 rounded-full border border-black/[0.06] dark:border-white/15 bg-white dark:bg-white/5 px-3.5 py-1.5 text-xs font-medium text-[#575757] dark:text-white/80">
            <svg class="w-3.5 h-3.5 text-[#575757] dark:text-white/75" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z" />
            </svg>
            <span>F.A.Q</span>
          </div>
          <h2 class="mt-4 text-3xl sm:text-4xl font-bold tracking-[-0.02em] text-[#111112] dark:text-white leading-tight">
            {{ t('Everything You Need to Know') }}
          </h2>
          <p class="mt-3 text-sm sm:text-base text-[#575757] dark:text-white/65">
            {{ t('Drop your STL or STEP files for an instant online quote.') }}
          </p>
          <div class="mt-6">
            <router-link
              to="/print/upload"
              class="inline-flex items-center gap-2 rounded-full bg-[#FF5E0E] hover:bg-[#FF764D] px-6 py-3 text-xs font-bold text-white shadow-[0_8px_20px_rgba(255,94,14,0.35)] transition"
            >
              <span>{{ t('Drop Your 3D File') }}</span>
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </router-link>
          </div>
        </div>

        <div class="lg:col-span-7 space-y-3.5">
          <div
            v-for="(faq, idx) in faqs"
            :key="faq.q"
            class="rounded-[20px] border bg-white dark:bg-[#111217] transition-all overflow-hidden"
            :class="openFaqIndex === idx
              ? 'border-[#FF5E0E]/60 shadow-[0_6px_20px_rgba(0,0,0,0.03)]'
              : 'border-black/[0.06] dark:border-white/10 hover:border-black/15 dark:hover:border-white/20'"
          >
            <button
              type="button"
              @click="toggleFaq(idx)"
              class="w-full px-6 py-5 flex items-center justify-between gap-4 text-left cursor-pointer"
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
                stroke-width="2"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
              </svg>
            </button>
            <div v-show="openFaqIndex === idx" class="px-6 pb-5 pt-0 text-sm text-[#575757] dark:text-white/70 leading-relaxed">
              {{ faq.a }}
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 10: Centered Grounded Obsidian Final CTA Card -->
    <section class="mx-auto max-w-[1160px] px-6">
      <div class="rounded-[32px] bg-[#0A0A0A] text-white px-6 sm:px-12 py-14 sm:py-20 text-center border border-white/10 shadow-2xl">
        <h2 class="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight">
          {{ t('Ready to Print on Creality K2 Plus?') }}
        </h2>
        <p class="mt-3.5 mx-auto max-w-xl text-sm sm:text-base text-white/70">
          {{ t('Drop your STL or STEP files for an instant online quote.') }}
        </p>
        <div class="mt-8">
          <router-link
            to="/print/upload"
            class="inline-flex items-center gap-2 rounded-full bg-[#FF5E0E] hover:bg-[#FF764D] px-8 py-4 text-sm font-bold text-white shadow-[0_10px_25px_rgba(255,94,14,0.4)] transition"
          >
            <span>{{ t('Go to 3D File Upload') }}</span>
            <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
            </svg>
          </router-link>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from '../i18n'

const { t } = useI18n()

// Section 3 Interactive Hardware Mode Switcher
const selectedModeIndex = ref(0)
const showcaseModes = [
  {
    id: 'workshop',
    label: 'FPV & Drones',
    title: 'Aerospace Lab Workflow',
    description: 'Carbon-fiber frames and shock-absorbing mounts printed locally inside a 60°C chamber.',
    image: '/assets/print/k2-plus-workshop.jpg'
  },
  {
    id: 'cfs',
    label: '16-Color CFS',
    title: 'Effortless 16-Color Automation',
    description: 'Smart RFID spool detection and sealed dry storage handle complex multi-color parts.',
    image: '/assets/print/k2-plus-cfs.jpg'
  },
  {
    id: 'extruder',
    label: 'High-Temp Core',
    title: '350°C Direct-Drive Precision',
    description: 'Unicorn tri-metal nozzle lays crisp gears and mounting holes accurate to ±0.1mm.',
    image: '/assets/print/k2-plus-extruder.jpg'
  }
]
const activeMode = computed(() => showcaseModes[selectedModeIndex.value])

// Section 5 Uniform Monochrome Specs Cards
const uniformSpecs = [
  {
    title: 'Dual AI Cameras',
    desc: 'Monitors flow calibration and prevents failed overnight prints automatically.',
    iconPath: 'M2.036 12.322a1.012 1.012 0 010-.639C3.423 7.51 7.36 4.5 12 4.5c4.638 0 8.573 3.007 9.963 7.178.07.207.07.431 0 .639C20.577 16.49 16.64 19.5 12 19.5c-4.638 0-8.573-3.007-9.963-7.178z'
  },
  {
    title: '40 mm³/s High Flow Nozzle',
    desc: 'Hardened tri-metal Unicorn nozzle extrudes composites cleanly at high speed.',
    iconPath: 'M3.75 13.5l10.5-11.25L12 10.5h8.25L9.75 21.75 12 13.5H3.75z'
  },
  {
    title: 'Auto Tilt & Mesh Leveling',
    desc: 'Dual Z-motors calibrate the 350mm spring-steel bed before every print.',
    iconPath: 'M3.75 6A2.25 2.25 0 016 3.75h2.25A2.25 2.25 0 0110.5 6v2.25a2.25 2.25 0 01-2.25 2.25H6a2.25 2.25 0 01-2.25-2.25V6zM3.75 15.75A2.25 2.25 0 016 13.5h2.25a2.25 2.25 0 012.25 2.25V18a2.25 2.25 0 01-2.25 2.25H6A2.25 2.25 0 013.75 18v-2.25zM13.5 6a2.25 2.25 0 012.25-2.25H18A2.25 2.25 0 0120.25 6v2.25A2.25 2.25 0 0118 10.5h-2.25a2.25 2.25 0 01-2.25-2.25V6zM13.5 15.75a2.25 2.25 0 012.25-2.25H18a2.25 2.25 0 012.25 2.25V18A2.25 2.25 0 0118 20.25h-2.25A2.25 2.25 0 0113.5 18v-2.25z'
  },
  {
    title: 'Matrix Die-Cast Frame',
    desc: 'Rigid aerospace aluminum alloy chassis eliminates vibration ringing.',
    iconPath: 'M9 12.75L11.25 15 15 9.75m-3-7.036A11.959 11.959 0 013.598 6 11.99 11.99 0 003 9.749c0 5.592 3.824 10.29 9 11.623 5.176-1.332 9-6.03 9-11.622 0-1.31-.21-2.571-.598-3.751h-.152c-3.196 0-6.1-1.248-8.25-3.285z'
  },
  {
    title: '60°C Actively Heated Chamber',
    desc: 'Keeps large ABS, ASA, and PA-CF prototypes completely flat and warp-free.',
    iconPath: 'M15.362 5.214A8.252 8.252 0 0112 21 8.25 8.25 0 016.038 7.048 8.287 8.287 0 009 9.6a8.983 8.983 0 013.361-6.867 8.21 8.21 0 003 2.48z'
  }
]

// Section 7 Reviews Carousel
const reviewIndex = ref(0)
const reviews = [
  {
    author: 'Sokha D.',
    role: 'FPV Drone Builder',
    quote: 'Printed a custom 5-inch Cinewhoop guard and TPU mount on the K2 Plus. Every bolt hole lined up cleanly.'
  },
  {
    author: 'Dara V.',
    role: 'Robotics Student',
    quote: 'Uploading our STEP gears took seconds and the 16-color CFS printed clean labels right on our robot chassis.'
  },
  {
    author: 'Maly K.',
    role: 'Product Prototyper',
    quote: 'Having a 350mm chamber locally saved our capstone project with super clean matte finish parts.'
  }
]
const currentReview = computed(() => reviews[reviewIndex.value])
function prevReview() {
  reviewIndex.value = (reviewIndex.value - 1 + reviews.length) % reviews.length
}
function nextReview() {
  reviewIndex.value = (reviewIndex.value + 1) % reviews.length
}

// Section 8 Photographic 6-Grid
const photoGridFeatures = [
  {
    title: 'Instant CAD Dropzone',
    desc: 'Drag and drop STL, STEP, OBJ, or 3MF files in seconds.',
    image: '/assets/print/k2-plus-portal-hero.jpg'
  },
  {
    title: '16-Color Sequencing',
    desc: 'Automated multi-spool colors and clean breakaway supports.',
    image: '/assets/print/k2-plus-cfs.jpg'
  },
  {
    title: 'Carbon-Fiber Strength',
    desc: '350°C hotend ready for PA-CF drone arms and structural mounts.',
    image: '/assets/print/k2-plus-extruder.jpg'
  },
  {
    title: 'Phnom Penh Lab Queue',
    desc: 'Same-day local slicing and quick pickup in Ta Khmau.',
    image: '/assets/print/k2-plus-workshop.jpg'
  },
  {
    title: '350³ mm Build Capacity',
    desc: 'Full-scale prototypes printed without splitting parts.',
    image: '/assets/print/k2-plus-hero.jpg'
  },
  {
    title: 'AI Quality Inspection',
    desc: 'Optical flow calibration verified before every print run.',
    image: '/assets/print/k2-plus-extruder.jpg'
  }
]

// Section 9 Minimal FAQ Accordion
const openFaqIndex = ref(0)
const faqs = [
  {
    q: 'What 3D CAD file formats can I upload?',
    a: 'We accept .STL, .STP, .STEP, .OBJ, and .3MF files up to the full 350 × 350 × 350 mm build size.'
  },
  {
    q: 'Can I request multi-color 3D printing?',
    a: 'Yes. Select CFS Multi-Color on the upload page to automate multi-color branding, labels, or supports.'
  },
  {
    q: 'Which material is best for drone frames and outdoor parts?',
    a: 'Use PA-CF Carbon Fiber Nylon or ABS/ASA for rigid arms, and TPU 95A for flexible vibration-damped mounts.'
  },
  {
    q: 'How fast can I receive my printed parts in Cambodia?',
    a: 'Most single-color PLA, PETG, and TPU prototypes ship or are ready for pickup within 24–48 hours.'
  },
  {
    q: 'How is the instant price calculated?',
    a: 'Our quote summary calculates part volume, material tier, infill percentage, and bulk discounts live.'
  }
]

function toggleFaq(index) {
  openFaqIndex.value = openFaqIndex.value === index ? -1 : index
}
</script>
