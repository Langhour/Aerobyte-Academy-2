<template>
  <div class="min-h-screen bg-[#F8F9FA] dark:bg-[#090A0F] text-[#111112] dark:text-white transition-colors pb-20">

    <!-- SECTION 1: Minimal Hero — Masked Kinetic Reveal + Architectural Daylight Portal -->
    <section class="relative overflow-hidden bg-[#F8F9FA] dark:bg-[#090A0F]">
      <div class="relative z-10 mx-auto max-w-4xl px-6 pt-12 sm:pt-16 pb-6 text-center">
        <div class="overflow-hidden py-2 -my-2">
          <h1
            v-reveal="{ variant: 'mask', immediate: true, delay: 40 }"
            class="text-4xl sm:text-5xl lg:text-[62px] font-bold tracking-[-0.03em] leading-[1.08] text-[#111112] dark:text-white"
          >
            {{ t('Precision Printing in Every Layer') }}
          </h1>
        </div>

        <div class="overflow-hidden py-1.5 -my-1.5 mt-3.5">
          <p
            v-reveal="{ variant: 'mask', immediate: true, delay: 160 }"
            class="text-base sm:text-lg font-medium text-[#575757] dark:text-white/70"
          >
            {{ t('Aero Print • High-Speed CoreXY, SLA & Multi-Color Lab') }}
          </p>
        </div>

        <div
          v-reveal="{ variant: 'up', immediate: true, delay: 260 }"
          class="mt-7"
        >
          <router-link
            to="/print/upload"
            class="group inline-flex items-center gap-2 rounded-full bg-navy-900 hover:bg-navy-800 dark:bg-navy-600 dark:hover:bg-navy-800 px-8 py-3.5 text-sm font-bold text-white shadow-[0_10px_25px_rgba(16,42,73,0.3)] active:scale-[0.99] transition"
          >
            <span>{{ t('Drop Your 3D File') }}</span>
            <svg class="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
            </svg>
          </router-link>
        </div>
      </div>

      <!-- Unobstructed Architectural Studio Stage -->
      <div
        v-reveal="{ variant: 'scale', immediate: true, delay: 200 }"
        class="relative mx-auto w-full max-w-[1600px] h-[300px] sm:h-[440px] lg:h-[560px] -mt-2"
      >
        <img
          src="/assets/print/k2-plus-portal-hero.jpg"
          alt="Aero Print 3D Printing Lab inside Architectural Studio"
          class="w-full h-full object-cover object-center opacity-95 dark:opacity-85"
        />
        <div aria-hidden="true" class="pointer-events-none absolute inset-x-0 top-0 h-16 sm:h-24 bg-gradient-to-b from-[#F8F9FA] via-[#F8F9FA]/60 to-transparent dark:from-[#090A0F] dark:via-[#090A0F]/60"></div>
        <div aria-hidden="true" class="pointer-events-none absolute inset-x-0 bottom-0 h-24 sm:h-32 bg-gradient-to-t from-[#F8F9FA] via-[#F8F9FA]/70 to-transparent dark:from-[#090A0F] dark:via-[#090A0F]/75"></div>
        <div aria-hidden="true" class="pointer-events-none hidden xl:block absolute inset-y-0 left-0 w-32 bg-gradient-to-r from-[#F8F9FA] to-transparent dark:from-[#090A0F]"></div>
        <div aria-hidden="true" class="pointer-events-none hidden xl:block absolute inset-y-0 right-0 w-32 bg-gradient-to-l from-[#F8F9FA] to-transparent dark:from-[#090A0F]"></div>
      </div>
    </section>

    <!-- KINETIC BRAND LOGO MARQUEE -->
    <div
      v-reveal="{ variant: 'fade', delay: 100 }"
      class="border-y border-black/[0.06] dark:border-white/10 bg-white/80 dark:bg-[#111217]/80 backdrop-blur-sm py-3.5 sm:py-4 overflow-hidden select-none"
    >
      <div class="marquee-track flex w-max items-center">
        <div
          v-for="half in 2"
          :key="half"
          class="flex shrink-0 items-center"
          :aria-hidden="half === 2"
        >
          <div
            v-for="repeat in 3"
            :key="`${half}-${repeat}`"
            class="flex shrink-0 items-center gap-10 sm:gap-16 pr-10 sm:pr-16"
          >
            <RouterLink
              v-for="brand in marqueeLogos"
              :key="`${half}-${repeat}-${brand.name}`"
              :to="brand.to"
              :aria-label="brand.name"
              :tabindex="half === 2 ? -1 : 0"
              class="inline-flex shrink-0 items-center justify-center opacity-85 hover:opacity-100 transition duration-200 hover:scale-[1.04]"
            >
              <img
                :src="brand.src"
                :alt="brand.name"
                loading="lazy"
                :class="[
                  'w-auto object-contain select-none pointer-events-none',
                  brand.heightClass,
                  brand.darkClass
                ]"
              />
            </RouterLink>
          </div>
        </div>
      </div>
    </div>

    <!-- SECTION 2: Produck-Style 2-Tier Bento Highlights (1 Wide Visual Card + 2 Clean Cards) -->
    <section ref="bentoStatsRef" class="mx-auto max-w-[1160px] px-6 py-16 sm:py-24">
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Full-Width Top Bento Card -->
        <div
          v-reveal="{ variant: 'up', delay: 40 }"
          class="md:col-span-2 rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-8 sm:p-12 shadow-[0_10px_30px_rgba(0,0,0,0.03)] grid grid-cols-1 lg:grid-cols-12 gap-8 items-center overflow-hidden group"
        >
          <div class="lg:col-span-5 space-y-3">
            <span
              v-reveal="{ variant: 'fade', delay: 100 }"
              class="inline-flex items-center rounded-full border border-black/[0.08] dark:border-white/15 bg-[#F8F9FA] dark:bg-white/5 px-3.5 py-1 text-xs font-medium text-[#575757] dark:text-white/75"
            >
              {{ t('Hyper-Speed CoreXY') }}
            </span>
            <div class="overflow-hidden py-1 -my-1">
              <h2
                v-reveal="{ variant: 'mask', delay: 160 }"
                class="text-3xl sm:text-4xl font-bold tracking-[-0.02em] text-[#111112] dark:text-white tabular-nums"
              >
                {{ displaySpeed }} mm/s Precision
              </h2>
            </div>
            <p
              v-reveal="{ variant: 'up', delay: 230 }"
              class="text-sm sm:text-base text-[#575757] dark:text-white/65 leading-relaxed"
            >
              {{ t('Step-servo motion prints strong engineering prototypes up to 5× faster.') }}
            </p>
          </div>
          <div class="lg:col-span-7 w-full overflow-hidden rounded-[24px] bg-[#0B0D14] aspect-[16/9]">
            <img
              src="/assets/print/k2-plus-extruder.jpg"
              alt="High-Speed Direct Drive Extruder"
              class="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-[1.03]"
            />
          </div>
        </div>

        <!-- Half-Width Card Left -->
        <div
          v-reveal="{ variant: 'up', delay: 100 }"
          class="rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-8 sm:p-10 shadow-[0_10px_30px_rgba(0,0,0,0.03)] flex flex-col justify-between transition-transform duration-300 hover:-translate-y-1"
        >
          <div>
            <div class="flex h-11 w-11 items-center justify-center rounded-full bg-[#F3F4F6] dark:bg-white/10 text-[#1F2937] dark:text-white">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
              </svg>
            </div>
            <div class="overflow-hidden py-1 -my-1 mt-6">
              <h3
                v-reveal="{ variant: 'mask', delay: 180 }"
                class="text-2xl sm:text-3xl font-bold tracking-tight text-[#111112] dark:text-white tabular-nums"
              >
                {{ displayVolume }}³ mm Volume
              </h3>
            </div>
            <p
              v-reveal="{ variant: 'up', delay: 250 }"
              class="mt-2.5 text-sm sm:text-base text-[#575757] dark:text-white/65"
            >
              {{ t('Print full drone frames and robotics parts in one seamless piece.') }}
            </p>
          </div>
        </div>

        <!-- Half-Width Card Right -->
        <div
          v-reveal="{ variant: 'up', delay: 180 }"
          class="rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-8 sm:p-10 shadow-[0_10px_30px_rgba(0,0,0,0.03)] flex flex-col justify-between transition-transform duration-300 hover:-translate-y-1"
        >
          <div>
            <div class="flex h-11 w-11 items-center justify-center rounded-full bg-[#F3F4F6] dark:bg-white/10 text-[#1F2937] dark:text-white">
              <svg class="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.6">
                <path stroke-linecap="round" stroke-linejoin="round" d="M6.429 9.75L2.25 12l4.179 2.25m0-4.5l5.571 3 5.571-3m-11.142 0L2.25 7.5 12 2.25l9.75 5.25-4.179 2.25m0 0L21.75 12l-4.179 2.25m0 0l4.179 2.25L12 21.75 2.25 16.5l4.179-2.25m11.142 0l-5.571 3-5.571-3" />
              </svg>
            </div>
            <div class="overflow-hidden py-1 -my-1 mt-6">
              <h3
                v-reveal="{ variant: 'mask', delay: 260 }"
                class="text-2xl sm:text-3xl font-bold tracking-tight text-[#111112] dark:text-white tabular-nums"
              >
                {{ displayColors }}-Color Filament Hub
              </h3>
            </div>
            <p
              v-reveal="{ variant: 'up', delay: 330 }"
              class="mt-2.5 text-sm sm:text-base text-[#575757] dark:text-white/65"
            >
              {{ t('Automated RFID spool switching inside a sealed dry enclosure.') }}
            </p>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 3: Calm Monochrome Hardware Showcase Banner (Animated Text & Media Switcher) -->
    <section class="mx-auto max-w-[1160px] px-6 pb-16 sm:pb-24">
      <div
        v-reveal="{ variant: 'up', delay: 60 }"
        class="rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-6 sm:p-10 shadow-[0_10px_30px_rgba(0,0,0,0.03)]"
      >
        <div class="mx-auto max-w-2xl text-center">
          <div class="overflow-hidden py-1.5 -my-1.5">
            <Transition name="mode-text" mode="out-in">
              <h2
                :key="activeMode.id"
                class="text-3xl sm:text-4xl font-bold tracking-[-0.02em] text-[#111112] dark:text-white"
              >
                {{ activeMode.title }}
              </h2>
            </Transition>
          </div>
          <div class="overflow-hidden py-1 -my-1 mt-2.5">
            <Transition name="mode-subtext" mode="out-in">
              <p
                :key="activeMode.id"
                class="text-sm sm:text-base text-[#575757] dark:text-white/65"
              >
                {{ activeMode.description }}
              </p>
            </Transition>
          </div>
        </div>

        <div class="mt-8 w-full h-[240px] sm:h-[400px] lg:h-[500px] overflow-hidden rounded-[24px] bg-[#F3F4F6] dark:bg-black/40">
          <Transition name="mode-image" mode="out-in">
            <img
              :key="activeMode.id"
              :src="activeMode.image"
              :alt="activeMode.title"
              class="w-full h-full object-cover"
            />
          </Transition>
        </div>

        <!-- Clean Monochrome Switcher Pills -->
        <div class="mt-6 flex flex-wrap items-center justify-center gap-2.5">
          <button
            v-for="(mode, idx) in showcaseModes"
            :key="mode.id"
            type="button"
            @click="selectedModeIndex = idx"
            class="inline-flex items-center gap-2 rounded-full px-4 py-2 text-xs font-semibold border transition-all duration-200 cursor-pointer"
            :class="selectedModeIndex === idx
              ? 'border-[#111112] dark:border-white bg-[#111112] dark:bg-white text-white dark:text-[#111112] scale-[1.03]'
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
        <div
          v-reveal="{ variant: 'up', delay: 60 }"
          class="rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-8 sm:p-10 shadow-[0_10px_30px_rgba(0,0,0,0.03)] flex flex-col justify-between group"
        >
          <div>
            <div class="overflow-hidden py-1 -my-1">
              <h3
                v-reveal="{ variant: 'mask', delay: 140 }"
                class="text-2xl font-bold tracking-tight text-[#111112] dark:text-white"
              >
                {{ t('16-Color Smart Filament Hub') }}
              </h3>
            </div>
            <p
              v-reveal="{ variant: 'up', delay: 210 }"
              class="mt-2 text-sm text-[#575757] dark:text-white/65"
            >
              {{ t('Zero manual spool swaps with automatic moisture protection.') }}
            </p>
          </div>
          <div class="mt-7 w-full overflow-hidden rounded-[22px] aspect-[16/10] bg-[#F8F9FA] dark:bg-black/30">
            <img
              src="/assets/print/k2-plus-cfs.jpg"
              alt="Automated Multi-Color Filament Hub"
              class="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-[1.03]"
            />
          </div>
        </div>

        <div
          v-reveal="{ variant: 'up', delay: 140 }"
          class="rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-8 sm:p-10 shadow-[0_10px_30px_rgba(0,0,0,0.03)] flex flex-col justify-between group"
        >
          <div>
            <div class="overflow-hidden py-1 -my-1">
              <h3
                v-reveal="{ variant: 'mask', delay: 220 }"
                class="text-2xl font-bold tracking-tight text-[#111112] dark:text-white"
              >
                {{ t('350°C Nozzle & 60°C Chamber') }}
              </h3>
            </div>
            <p
              v-reveal="{ variant: 'up', delay: 290 }"
              class="mt-2 text-sm text-[#575757] dark:text-white/65"
            >
              {{ t('Warp-free ABS, ASA, and carbon-fiber PA-CF structural prints.') }}
            </p>
          </div>
          <div class="mt-7 w-full overflow-hidden rounded-[22px] aspect-[16/10] bg-[#0B0D14]">
            <img
              src="/assets/print/k2-plus-extruder.jpg"
              alt="High-Temperature 350C Nozzle"
              class="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-[1.03]"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 5: Produck Sticky 2-Column Specs Layout (Uniform Monochrome White Cards + Sticky Right Summary) -->
    <section class="mx-auto max-w-[1160px] px-6 pb-16 sm:pb-24">
      <div class="mb-10 max-w-xl">
        <div class="overflow-hidden py-1.5 -my-1.5">
          <h2
            v-reveal="{ variant: 'mask', delay: 40 }"
            class="text-3xl sm:text-4xl font-bold tracking-[-0.02em] text-[#111112] dark:text-white"
          >
            {{ t('Engineered for Industrial Precision') }}
          </h2>
        </div>
        <p
          v-reveal="{ variant: 'up', delay: 140 }"
          class="mt-2.5 text-sm sm:text-base text-[#575757] dark:text-white/65"
        >
          {{ t('Every printer in our Aero Print lab is calibrated for repeatable accuracy.') }}
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        <!-- Left Stacked Uniform White Feature Cards -->
        <div class="lg:col-span-7 space-y-4">
          <div
            v-for="(spec, idx) in uniformSpecs"
            :key="spec.title"
            v-reveal="{ variant: 'up', delay: idx * 70 }"
            class="rounded-[24px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-6 sm:p-7 shadow-[0_4px_16px_rgba(0,0,0,0.02)] flex items-start gap-5 transition-all duration-300 hover:border-black/15 dark:hover:border-white/20 hover:-translate-y-0.5"
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
        <div
          v-reveal="{ variant: 'up', delay: 140 }"
          class="lg:col-span-5 lg:sticky lg:top-24 rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-8 shadow-[0_10px_30px_rgba(0,0,0,0.03)] group"
        >
          <div class="w-full overflow-hidden rounded-[22px] bg-[#F8F9FA] dark:bg-black/30 aspect-[4/3]">
            <img
              src="/assets/print/k2-plus-hero.jpg"
              alt="Aero Print Industrial 3D Printer"
              class="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-[1.03]"
            />
          </div>
          <div class="mt-6 flex items-baseline justify-between">
            <h3 class="text-2xl font-bold text-[#111112] dark:text-white">{{ t('Aero Print Service') }}</h3>
            <span class="text-base font-bold text-navy-900 dark:text-blue-300">$0.08 / cm³</span>
          </div>
          <p class="mt-2 text-sm text-[#575757] dark:text-white/65">
            {{ t('Upload your CAD files for instant pricing and local Phnom Penh printing.') }}
          </p>
          <router-link
            to="/print/upload"
            class="group/btn mt-6 w-full inline-flex items-center justify-center gap-2 rounded-full bg-navy-900 hover:bg-navy-800 dark:bg-navy-600 dark:hover:bg-navy-800 px-6 py-3.5 text-sm font-bold text-white shadow-[0_10px_25px_rgba(16,42,73,0.3)] transition"
          >
            <span>{{ t('Drop Your 3D File') }}</span>
            <svg class="w-4 h-4 transition-transform duration-300 group-hover/btn:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
            </svg>
          </router-link>
        </div>
      </div>
    </section>

    <!-- SECTION 6: Clean Full-Bleed Workshop Photo Banner (Zero Floating Boxes) -->
    <section class="mx-auto max-w-[1160px] px-6 pb-16 sm:pb-24">
      <div
        v-reveal="{ variant: 'scale', delay: 60 }"
        class="relative rounded-[32px] overflow-hidden min-h-[380px] sm:min-h-[440px] flex items-end p-8 sm:p-12 text-white group"
      >
        <img
          src="/assets/print/k2-plus-workshop.jpg"
          alt="AeroByte Robotics & Drone 3D Printing Lab"
          class="absolute inset-0 w-full h-full object-cover transition-transform duration-1000 ease-out group-hover:scale-[1.04]"
        />
        <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent"></div>

        <div class="relative z-10 max-w-lg">
          <div class="overflow-hidden py-1 -my-1">
            <h2
              v-reveal="{ variant: 'mask', delay: 140 }"
              class="text-3xl sm:text-4xl font-bold tracking-tight text-white"
            >
              {{ t('Built for Drones, Robotics & Real Prototypes') }}
            </h2>
          </div>
          <p
            v-reveal="{ variant: 'up', delay: 230 }"
            class="mt-2.5 text-sm sm:text-base text-white/80"
          >
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
            <span
              v-reveal="{ variant: 'fade', delay: 40 }"
              class="inline-flex items-center rounded-full border border-black/[0.08] dark:border-white/15 bg-white dark:bg-white/5 px-3.5 py-1 text-xs font-medium text-[#575757] dark:text-white/80"
            >
              {{ t('Available Now') }}
            </span>

            <div class="mt-4 flex items-baseline justify-between gap-2 overflow-hidden py-1 -my-1">
              <h2
                v-reveal="{ variant: 'mask', delay: 100 }"
                class="text-3xl sm:text-4xl font-bold tracking-tight text-[#111112] dark:text-white"
              >
                {{ t('Aero Print Lab') }}
              </h2>
              <span
                v-reveal="{ variant: 'up', delay: 140 }"
                class="text-xl font-bold text-navy-900 dark:text-blue-300"
              >
                From $0.08 / cm³
              </span>
            </div>

            <div
              v-reveal="{ variant: 'up', delay: 180 }"
              class="mt-2.5 flex items-center gap-2"
            >
              <span class="text-navy-900 dark:text-blue-300 text-sm">★★★★★</span>
              <span class="text-xs font-medium text-[#575757] dark:text-white/65">4.9 / 5 • {{ t('Cambodia Maker Lab') }}</span>
            </div>

            <p
              v-reveal="{ variant: 'up', delay: 220 }"
              class="mt-4 text-sm sm:text-base text-[#575757] dark:text-white/70 leading-relaxed"
            >
              {{ t('Skip weeks of international shipping with instant Phnom Penh CAD printing.') }}
            </p>

            <!-- 2 Clean Monochrome Metric Pills (Zero Emojis) -->
            <div
              v-reveal="{ variant: 'up', delay: 260 }"
              class="mt-6 grid grid-cols-2 gap-3.5"
            >
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
                <span class="text-xs font-bold text-[#111112] dark:text-white">16-Color Hub</span>
              </div>
            </div>
          </div>

          <!-- Clean Review Card with Directional Text Slide -->
          <div
            v-reveal="{ variant: 'up', delay: 300 }"
            class="rounded-[24px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-6 shadow-[0_4px_16px_rgba(0,0,0,0.02)] overflow-hidden"
          >
            <div class="flex items-center justify-between mb-3">
              <div class="overflow-hidden">
                <Transition :name="reviewTransitionName" mode="out-in">
                  <div :key="reviewIndex">
                    <p class="text-sm font-bold text-[#111112] dark:text-white">{{ currentReview.author }}</p>
                    <p class="text-xs text-[#696969] dark:text-white/55">{{ currentReview.role }}</p>
                  </div>
                </Transition>
              </div>
              <div class="flex items-center gap-1.5">
                <button
                  type="button"
                  @click="prevReview"
                  aria-label="Previous review"
                  class="h-8 w-8 rounded-full border border-black/10 dark:border-white/15 flex items-center justify-center text-xs text-[#111112] dark:text-white hover:border-black/30 dark:hover:border-white/35 active:scale-95 transition cursor-pointer"
                >
                  ←
                </button>
                <button
                  type="button"
                  @click="nextReview"
                  aria-label="Next review"
                  class="h-8 w-8 rounded-full border border-black/10 dark:border-white/15 flex items-center justify-center text-xs text-[#111112] dark:text-white hover:border-black/30 dark:hover:border-white/35 active:scale-95 transition cursor-pointer"
                >
                  →
                </button>
              </div>
            </div>
            <div class="overflow-hidden">
              <Transition :name="reviewTransitionName" mode="out-in">
                <p
                  :key="reviewIndex"
                  class="text-sm text-[#575757] dark:text-white/75 leading-relaxed"
                >
                  "{{ currentReview.quote }}"
                </p>
              </Transition>
            </div>
          </div>
        </div>

        <!-- Right Tall Studio Render Card -->
        <div
          v-reveal="{ variant: 'scale', delay: 140 }"
          class="rounded-[32px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111217] p-6 sm:p-8 flex items-center justify-center shadow-[0_10px_30px_rgba(0,0,0,0.03)] group"
        >
          <div class="overflow-hidden rounded-[24px] w-full aspect-[4/3] bg-[#0B0D14]">
            <img
              src="/assets/print/k2-plus-extruder.jpg"
              alt="High-Flow Tri-Metal Extruder Cutaway"
              class="w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-[1.03]"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 8: 6-Feature Clean Photographic Bento Grid -->
    <section class="mx-auto max-w-[1160px] px-6 pb-16 sm:pb-24">
      <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
        <div
          v-for="(item, idx) in photoGridFeatures"
          :key="item.title"
          v-reveal="{ variant: 'up', delay: idx * 70 }"
          class="relative rounded-[28px] overflow-hidden min-h-[260px] flex items-end p-7 text-white group"
        >
          <img
            :src="item.image"
            :alt="item.title"
            class="absolute inset-0 w-full h-full object-cover transition-transform duration-700 ease-out group-hover:scale-105"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/85 via-black/35 to-black/15"></div>
          <div class="relative z-10 transition-transform duration-300 ease-out group-hover:-translate-y-1">
            <h3 class="text-lg font-bold text-white">{{ item.title }}</h3>
            <p class="mt-1 text-xs sm:text-sm text-white/80">{{ item.desc }}</p>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 9: Minimal 2-Column Produck FAQ Accordion (Smooth Grid Collapse Animation) -->
    <section id="faq" class="mx-auto max-w-[1160px] px-6 pb-16 sm:pb-24">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-10 lg:gap-12 items-start">
        <div class="lg:col-span-5 lg:sticky lg:top-24">
          <div
            v-reveal="{ variant: 'fade', delay: 40 }"
            class="inline-flex items-center gap-2 rounded-full border border-black/[0.06] dark:border-white/15 bg-white dark:bg-white/5 px-3.5 py-1.5 text-xs font-medium text-[#575757] dark:text-white/80"
          >
            <svg class="w-3.5 h-3.5 text-[#575757] dark:text-white/75" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
              <path stroke-linecap="round" stroke-linejoin="round" d="M9.879 7.519c1.171-1.025 3.071-1.025 4.242 0 1.172 1.025 1.172 2.687 0 3.712-.203.179-.43.326-.67.442-.745.361-1.45.999-1.45 1.827v.75M21 12a9 9 0 11-18 0 9 9 0 0118 0zm-9 5.25h.008v.008H12v-.008z" />
            </svg>
            <span>F.A.Q</span>
          </div>
          <div class="overflow-hidden py-1.5 -my-1.5 mt-4">
            <h2
              v-reveal="{ variant: 'mask', delay: 110 }"
              class="text-3xl sm:text-4xl font-bold tracking-[-0.02em] text-[#111112] dark:text-white leading-tight"
            >
              {{ t('Everything You Need to Know') }}
            </h2>
          </div>
          <p
            v-reveal="{ variant: 'up', delay: 190 }"
            class="mt-3 text-sm sm:text-base text-[#575757] dark:text-white/65"
          >
            {{ t('Drop your STL or STEP files for an instant online quote.') }}
          </p>
          <div
            v-reveal="{ variant: 'up', delay: 260 }"
            class="mt-6"
          >
            <router-link
              to="/print/upload"
              class="group inline-flex items-center gap-2 rounded-full bg-navy-900 hover:bg-navy-800 dark:bg-navy-600 dark:hover:bg-navy-800 px-6 py-3 text-xs font-bold text-white shadow-[0_8px_20px_rgba(16,42,73,0.28)] transition"
            >
              <span>{{ t('Drop Your 3D File') }}</span>
              <svg class="w-3.5 h-3.5 transition-transform duration-300 group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
              </svg>
            </router-link>
          </div>
        </div>

        <div class="lg:col-span-7 space-y-3.5">
          <div
            v-for="(faq, idx) in faqs"
            :key="faq.q"
            v-reveal="{ variant: 'up', delay: idx * 60 }"
            class="rounded-[20px] border bg-white dark:bg-[#111217] transition-all overflow-hidden"
            :class="openFaqIndex === idx
              ? 'border-navy-900/50 dark:border-blue-400/50 shadow-[0_6px_20px_rgba(0,0,0,0.03)]'
              : 'border-black/[0.06] dark:border-white/10 hover:border-black/15 dark:hover:border-white/20'"
          >
            <button
              type="button"
              @click="toggleFaq(idx)"
              class="w-full px-6 py-5 flex items-center justify-between gap-4 text-left cursor-pointer"
            >
              <span
                class="text-sm sm:text-base font-semibold transition-colors"
                :class="openFaqIndex === idx ? 'text-navy-900 dark:text-blue-300' : 'text-[#111112] dark:text-white'"
              >
                {{ faq.q }}
              </span>
              <svg
                class="w-4 h-4 shrink-0 transition-transform duration-300"
                :class="openFaqIndex === idx ? 'rotate-180 text-navy-900 dark:text-blue-300' : 'text-[#575757] dark:text-white/60'"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
                stroke-width="2"
              >
                <path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" />
              </svg>
            </button>
            <div
              class="grid transition-[grid-template-rows,opacity] duration-300 ease-[cubic-bezier(0.16,1,0.3,1)]"
              :class="openFaqIndex === idx ? 'grid-rows-[1fr] opacity-100' : 'grid-rows-[0fr] opacity-0'"
            >
              <div class="overflow-hidden">
                <div class="px-6 pb-5 pt-0 text-sm text-[#575757] dark:text-white/70 leading-relaxed">
                  {{ faq.a }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- SECTION 10: Centered Grounded Obsidian Final CTA Card -->
    <section class="mx-auto max-w-[1160px] px-6">
      <div
        v-reveal="{ variant: 'up', delay: 60 }"
        class="rounded-[32px] bg-[#0A0A0A] text-white px-6 sm:px-12 py-14 sm:py-20 text-center border border-white/10 shadow-2xl"
      >
        <div class="overflow-hidden py-1.5 -my-1.5">
          <h2
            v-reveal="{ variant: 'mask', delay: 140 }"
            class="text-3xl sm:text-4xl lg:text-5xl font-bold tracking-tight"
          >
            {{ t('Ready to Print Your 3D Project?') }}
          </h2>
        </div>
        <p
          v-reveal="{ variant: 'up', delay: 220 }"
          class="mt-3.5 mx-auto max-w-xl text-sm sm:text-base text-white/70"
        >
          {{ t('Drop your STL or STEP files for an instant online quote.') }}
        </p>
        <div
          v-reveal="{ variant: 'up', delay: 300 }"
          class="mt-8"
        >
          <router-link
            to="/print/upload"
            class="group inline-flex items-center gap-2 rounded-full bg-navy-800 hover:bg-navy-600 border border-white/15 px-8 py-4 text-sm font-bold text-white shadow-[0_10px_25px_rgba(16,42,73,0.45)] transition"
          >
            <span>{{ t('Go to 3D File Upload') }}</span>
            <svg class="w-4 h-4 transition-transform duration-300 group-hover:translate-x-1" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2">
              <path stroke-linecap="round" stroke-linejoin="round" d="M13.5 4.5L21 12m0 0l-7.5 7.5M21 12H3" />
            </svg>
          </router-link>
        </div>
      </div>
    </section>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useI18n } from '../i18n'

const { t } = useI18n()

const marqueeLogos = [
  {
    name: 'AeroByte Academy',
    src: '/aerobyte-logo-tight.png',
    to: '/courses',
    heightClass: 'h-8 sm:h-10',
    darkClass: ''
  },
  {
    name: 'Aero Print',
    src: '/assets/brand/aero-print.png',
    to: '/print',
    heightClass: 'h-9 sm:h-11',
    darkClass: 'dark:invert dark:hue-rotate-180'
  },
  {
    name: 'Aero Store',
    src: '/assets/brand/aero-store.png',
    to: '/store',
    heightClass: 'h-9 sm:h-11',
    darkClass: 'dark:invert dark:hue-rotate-180'
  },
  {
    name: 'Aero Fly',
    src: '/assets/brand/aero-fly.png',
    to: '/fly',
    heightClass: 'h-9 sm:h-11',
    darkClass: 'dark:invert dark:hue-rotate-180'
  }
]

// ------------------------------------------------------------
// Bidirectional Scroll-Triggered Text Reveal Directive (v-reveal)
// Observes stationary mask wrappers & adds a viewport reconciliation guard
// so scrolling back UP never traps masked headings off-screen.
// ------------------------------------------------------------
const targetToTrigger = new WeakMap()
const triggerToTargets = new WeakMap()
const trackedTargets = new Set()
let enterObserver = null
let exitObserver = null
let scrollCheckRaf = 0

function prefersReducedMotion() {
  return typeof window !== 'undefined' && window.matchMedia?.('(prefers-reduced-motion: reduce)').matches
}

function revealElement(el) {
  if (!el || el.classList.contains('is-revealed')) return
  const delay = Number(el.dataset.revealDelay || 0)
  // If reset happened on this same frame, flush layout before animating in
  if (el.style.transitionDuration === '0ms') {
    void el.offsetHeight
    el.style.transitionDuration = ''
  }
  el.style.transitionDelay = delay ? `${delay}ms` : ''
  el.classList.add('is-revealed')
}

function reconcileVisibleReveals() {
  scrollCheckRaf = 0
  if (typeof window === 'undefined') return
  const vh = window.innerHeight || document.documentElement.clientHeight
  trackedTargets.forEach((el) => {
    if (el.classList.contains('is-revealed')) return
    const triggerEl = targetToTrigger.get(el) || el
    const rect = triggerEl.getBoundingClientRect()
    if (rect.height > 0 && rect.bottom > 12 && rect.top < vh - 12) {
      revealElement(el)
    }
  })
}

function scheduleRevealReconcile() {
  if (scrollCheckRaf || typeof window === 'undefined') return
  scrollCheckRaf = requestAnimationFrame(reconcileVisibleReveals)
}

function getEnterObserver() {
  if (enterObserver) return enterObserver
  enterObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return
        const targets = triggerToTargets.get(entry.target)
        targets?.forEach((el) => revealElement(el))
      })
    },
    { threshold: 0.01, rootMargin: '0px 0px -16px 0px' }
  )
  return enterObserver
}

function getExitObserver() {
  if (exitObserver) return exitObserver
  exitObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) return
        const targets = triggerToTargets.get(entry.target)
        const exitedAbove = entry.boundingClientRect.bottom <= 0
        targets?.forEach((el) => {
          const wasRevealed = el.classList.contains('is-revealed')
          el.style.transitionDuration = '0ms'
          el.style.transitionDelay = '0ms'
          if (wasRevealed) {
            el.classList.remove('is-revealed')
          }

          // If element is above the viewport, prepare it to glide down when scrolling UP
          if (exitedAbove) {
            el.classList.add('reveal-from-top')
          } else {
            el.classList.remove('reveal-from-top')
          }

          requestAnimationFrame(() => {
            if (!el.classList.contains('is-revealed')) {
              el.style.transitionDuration = ''
            }
          })
        })
      })
    },
    { threshold: 0, rootMargin: '40px 0px 40px 0px' }
  )
  return exitObserver
}

const vReveal = {
  mounted(el, binding) {
    const opts = typeof binding.value === 'object' && binding.value !== null ? binding.value : {}
    const delay = opts.delay ?? 0
    const variant = opts.variant ?? 'up'

    el.classList.add('reveal-base', `reveal-${variant}`)
    el.dataset.revealDelay = String(delay)
    if (delay) {
      el.style.transitionDelay = `${delay}ms`
    }

    if (prefersReducedMotion()) {
      el.classList.add('is-revealed')
      return
    }

    if (opts.immediate) {
      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          el.classList.add('is-revealed')
        })
      })
    }

    // Observe the stationary wrapper for masked elements so ±105% translation never clips IO rect to 0px
    const triggerEl = variant === 'mask' && el.parentElement ? el.parentElement : el
    let set = triggerToTargets.get(triggerEl)
    if (!set) {
      set = new Set()
      triggerToTargets.set(triggerEl, set)
      getEnterObserver().observe(triggerEl)
      getExitObserver().observe(triggerEl)
    }
    set.add(el)
    targetToTrigger.set(el, triggerEl)
    trackedTargets.add(el)
  },
  unmounted(el) {
    trackedTargets.delete(el)
    const triggerEl = targetToTrigger.get(el)
    if (!triggerEl) return
    targetToTrigger.delete(el)
    const set = triggerToTargets.get(triggerEl)
    if (!set) return
    set.delete(el)
    if (set.size === 0) {
      triggerToTargets.delete(triggerEl)
      enterObserver?.unobserve(triggerEl)
      exitObserver?.unobserve(triggerEl)
    }
  }
}

// ------------------------------------------------------------
// Section 2 Bidirectional Hardware Telemetry Counters
// ------------------------------------------------------------
const bentoStatsRef = ref(null)
const displaySpeed = ref(600)
const displayVolume = ref(350)
const displayColors = ref(16)
let statsEnterObserver = null
let statsExitObserver = null
let statsPlaying = false
const activeCountRafs = []

function cancelStatsRafs() {
  activeCountRafs.forEach((id) => cancelAnimationFrame(id))
  activeCountRafs.length = 0
}

function animateCount(targetRef, targetVal, duration = 1100) {
  const startTime = performance.now()
  targetRef.value = 0

  function step(now) {
    const t = Math.min(1, (now - startTime) / duration)
    // Smooth exponential ease-out matching physical CoreXY deceleration
    const eased = t === 1 ? 1 : 1 - Math.pow(2, -10 * t)
    targetRef.value = Math.round(eased * targetVal)
    if (t < 1) {
      const id = requestAnimationFrame(step)
      activeCountRafs.push(id)
    }
  }

  const id = requestAnimationFrame(step)
  activeCountRafs.push(id)
}

onMounted(() => {
  window.addEventListener('scroll', scheduleRevealReconcile, { passive: true })
  window.addEventListener('resize', scheduleRevealReconcile, { passive: true })

  if (prefersReducedMotion() || !bentoStatsRef.value) return
  displaySpeed.value = 0
  displayVolume.value = 0
  displayColors.value = 0

  statsEnterObserver = new IntersectionObserver(
    (entries) => {
      if (entries.some((e) => e.isIntersecting) && !statsPlaying) {
        statsPlaying = true
        cancelStatsRafs()
        animateCount(displaySpeed, 600, 1200)
        animateCount(displayVolume, 350, 1100)
        animateCount(displayColors, 16, 900)
      }
    },
    { threshold: 0.05 }
  )

  statsExitObserver = new IntersectionObserver(
    (entries) => {
      if (entries.some((e) => !e.isIntersecting) && statsPlaying) {
        statsPlaying = false
        cancelStatsRafs()
        displaySpeed.value = 0
        displayVolume.value = 0
        displayColors.value = 0
      }
    },
    { threshold: 0, rootMargin: '40px 0px 40px 0px' }
  )

  statsEnterObserver.observe(bentoStatsRef.value)
  statsExitObserver.observe(bentoStatsRef.value)
})

onUnmounted(() => {
  window.removeEventListener('scroll', scheduleRevealReconcile)
  window.removeEventListener('resize', scheduleRevealReconcile)
  if (scrollCheckRaf) {
    cancelAnimationFrame(scrollCheckRaf)
    scrollCheckRaf = 0
  }
  trackedTargets.clear()
  enterObserver?.disconnect()
  enterObserver = null
  exitObserver?.disconnect()
  exitObserver = null
  statsEnterObserver?.disconnect()
  statsEnterObserver = null
  statsExitObserver?.disconnect()
  statsExitObserver = null
  cancelStatsRafs()
})

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
    label: '16-Color Hub',
    title: 'Effortless 16-Color Automation',
    description: 'Smart RFID spool detection and sealed dry storage handle complex multi-color parts.',
    image: '/assets/print/k2-plus-cfs.jpg'
  },
  {
    id: 'extruder',
    label: 'High-Temp Core',
    title: '350°C Direct-Drive Precision',
    description: 'Hardened tri-metal nozzle lays crisp gears and mounting holes accurate to ±0.1mm.',
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
    desc: 'Hardened high-flow tri-metal nozzle extrudes composites cleanly at high speed.',
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

// Section 7 Reviews Carousel with Directional Slide Motion
const reviewIndex = ref(0)
const reviewDirection = ref('next')
const reviewTransitionName = computed(() => (reviewDirection.value === 'next' ? 'review-next' : 'review-prev'))
const reviews = [
  {
    author: 'Sokha D.',
    role: 'FPV Drone Builder',
    quote: 'Printed a custom 5-inch Cinewhoop guard and TPU mount with Aero Print. Every bolt hole lined up cleanly.'
  },
  {
    author: 'Dara V.',
    role: 'Robotics Student',
    quote: 'Uploading our STEP gears took seconds and the multi-color system printed clean labels right on our robot chassis.'
  },
  {
    author: 'Maly K.',
    role: 'Product Prototyper',
    quote: 'Having a 350mm chamber locally saved our capstone project with super clean matte finish parts.'
  }
]
const currentReview = computed(() => reviews[reviewIndex.value])
function prevReview() {
  reviewDirection.value = 'prev'
  reviewIndex.value = (reviewIndex.value - 1 + reviews.length) % reviews.length
}
function nextReview() {
  reviewDirection.value = 'next'
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
    a: 'Yes. Select Multi-Color on the upload page to automate multi-color branding, labels, or supports.'
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

<style scoped>
/* Base Scroll & Mount Reveal Transitions */
.reveal-base {
  will-change: transform, opacity;
  transition-property: transform, opacity, filter;
  transition-duration: 800ms;
  transition-timing-function: cubic-bezier(0.16, 1, 0.3, 1);
}

.reveal-mask {
  opacity: 0;
  transform: translateY(105%);
}

.reveal-mask.reveal-from-top {
  transform: translateY(-105%);
}

.reveal-up {
  opacity: 0;
  transform: translateY(26px);
  filter: blur(4px);
}

.reveal-up.reveal-from-top {
  transform: translateY(-26px);
}

.reveal-scale {
  opacity: 0;
  transform: scale(0.96);
}

.reveal-fade {
  opacity: 0;
}

.reveal-base.is-revealed {
  opacity: 1;
  transform: translateY(0) scale(1);
  filter: blur(0);
}

/* Continuous Kinetic Brand Logo Ticker */
.marquee-track {
  animation: print-marquee 32s linear infinite;
}

.marquee-track:hover {
  animation-play-state: paused;
}

@keyframes print-marquee {
  0% {
    transform: translateX(0);
  }
  100% {
    transform: translateX(-50%);
  }
}

/* Mode Switcher Masked Text & Image Transitions */
.mode-text-enter-active,
.mode-text-leave-active,
.mode-subtext-enter-active,
.mode-subtext-leave-active {
  transition: transform 420ms cubic-bezier(0.16, 1, 0.3, 1), opacity 320ms ease;
}

.mode-subtext-enter-active {
  transition-delay: 50ms;
}

.mode-text-enter-from,
.mode-subtext-enter-from {
  opacity: 0;
  transform: translateY(90%);
}

.mode-text-leave-to,
.mode-subtext-leave-to {
  opacity: 0;
  transform: translateY(-90%);
}

.mode-image-enter-active,
.mode-image-leave-active {
  transition: opacity 420ms ease, transform 520ms cubic-bezier(0.16, 1, 0.3, 1);
}

.mode-image-enter-from {
  opacity: 0;
  transform: scale(1.03);
}

.mode-image-leave-to {
  opacity: 0;
  transform: scale(0.98);
}

/* Directional Review Carousel Slide Transitions */
.review-next-enter-active,
.review-next-leave-active,
.review-prev-enter-active,
.review-prev-leave-active {
  transition: transform 360ms cubic-bezier(0.16, 1, 0.3, 1), opacity 280ms ease;
}

.review-next-enter-from {
  opacity: 0;
  transform: translateX(24px);
}
.review-next-leave-to {
  opacity: 0;
  transform: translateX(-24px);
}

.review-prev-enter-from {
  opacity: 0;
  transform: translateX(-24px);
}
.review-prev-leave-to {
  opacity: 0;
  transform: translateX(24px);
}

/* Accessibility: Respect Reduced Motion */
@media (prefers-reduced-motion: reduce) {
  .reveal-base {
    transition: none !important;
    opacity: 1 !important;
    transform: none !important;
    filter: none !important;
  }
  .marquee-track {
    animation: none !important;
  }
  .mode-text-enter-active,
  .mode-text-leave-active,
  .mode-subtext-enter-active,
  .mode-subtext-leave-active,
  .mode-image-enter-active,
  .mode-image-leave-active,
  .review-next-enter-active,
  .review-next-leave-active,
  .review-prev-enter-active,
  .review-prev-leave-active {
    transition: none !important;
  }
}
</style>
