<template>
  <div class="pb-16 dark:bg-slate-900 transition-colors">
    <!-- Hero Section -->
    <section class="courses-hero px-4 pb-12 pt-8 sm:px-6 sm:pb-16 sm:pt-14 lg:px-8 text-center">
      <div class="mx-auto max-w-4xl">
        <div class="flex justify-center mb-6 sm:mb-8">
          <img
            src="/assets/brand/aero-fly.png"
            alt="Aero Fly"
            class="h-28 sm:h-36 md:h-44 w-auto object-contain mx-auto transition-transform duration-300 hover:scale-105 dark:invert"
          />
        </div>

        <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight text-navy-900 dark:text-white">
          Aero Fly
        </h1>
        <p class="mx-auto mt-4 max-w-2xl text-sm sm:text-base leading-relaxed text-slate-600 dark:text-slate-300">
          {{ t('Hands-on drone pilot training, FPV racing simulations, aerodynamics workshops, and autonomous flight engineering.') }}
        </p>

        <div class="mt-8 flex flex-wrap justify-center gap-3">
          <RouterLink
            to="/contact"
            class="inline-flex items-center gap-2 rounded-xl bg-navy-900 hover:bg-navy-800 dark:bg-indigo-600 dark:hover:bg-indigo-500 px-6 py-3 text-sm font-bold text-white shadow-sm shadow-navy-950/20 transition"
          >
            <span>{{ t('Join Flight Lab') }}</span>
          </RouterLink>
          <RouterLink
            to="/courses"
            class="inline-flex items-center gap-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-6 py-3 text-sm font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 transition"
          >
            <span>{{ t('Drone Courses') }}</span>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Capabilities Overview -->
    <section class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 mt-4">
      <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/80 p-6 shadow-xs">
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-indigo-300 mb-4 text-xl">
            ✈️
          </div>
          <h3 class="text-lg font-bold text-navy-900 dark:text-white">{{ t('FPV Pilot Training') }}</h3>
          <p class="mt-2 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            {{ t('From beginner drone flight simulator hours to high-speed FPV racing with professional mentor coaching.') }}
          </p>
        </div>

        <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/80 p-6 shadow-xs">
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-indigo-300 mb-4 text-xl">
            📡
          </div>
          <h3 class="text-lg font-bold text-navy-900 dark:text-white">{{ t('Autonomous Navigation') }}</h3>
          <p class="mt-2 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            {{ t('GPS waypoint navigation, obstacle detection, ArduPilot and Betaflight firmware tuning for modern UAVs.') }}
          </p>
        </div>

        <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/80 p-6 shadow-xs sm:col-span-2 lg:col-span-1">
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-indigo-300 mb-4 text-xl">
            🏆
          </div>
          <h3 class="text-lg font-bold text-navy-900 dark:text-white">{{ t('Competitions & Teams') }}</h3>
          <p class="mt-2 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            {{ t('Represent AeroByte Academy in national and regional robotics championships and drone sports leagues.') }}
          </p>
        </div>
      </div>
    </section>
  </div>
</template>

<script setup>
import { useI18n } from '../i18n'

const { t } = useI18n()
</script>
