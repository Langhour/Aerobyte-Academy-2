<template>
  <div class="pb-16 dark:bg-slate-900 transition-colors">
    <!-- Hero Section -->
    <section class="courses-hero px-4 pb-12 pt-8 sm:px-6 sm:pb-16 sm:pt-14 lg:px-8 text-center">
      <div class="mx-auto max-w-4xl">
        <div class="inline-flex items-center gap-2 rounded-full border border-sky-200 dark:border-sky-900/60 bg-sky-50 dark:bg-sky-950/40 px-3.5 py-1 text-xs font-bold text-sky-700 dark:text-sky-300 mb-4">
          <span>AeroByte Ecosystem</span>
          <span class="text-slate-300 dark:text-slate-600">/</span>
          <span>Robotics Hardware & Gear</span>
        </div>

        <div class="flex justify-center mb-6">
          <div class="p-6 rounded-2xl bg-white dark:bg-slate-800 shadow-md border border-slate-100 dark:border-slate-700 inline-block">
            <img
              src="/assets/brand/aero-store.png"
              alt="Aero Store"
              class="h-24 sm:h-32 object-contain mx-auto dark:invert"
            />
          </div>
        </div>

        <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight text-navy-900 dark:text-white">
          Aero Store
        </h1>
        <p class="mx-auto mt-4 max-w-2xl text-sm sm:text-base leading-relaxed text-slate-600 dark:text-slate-300">
          {{ t('Official hardware store for authentic robotics learning kits, drone parts, microcontrollers, brushless motors, and lab tools.') }}
        </p>

        <div class="mt-8 flex flex-wrap justify-center gap-3">
          <RouterLink
            to="/contact"
            class="inline-flex items-center gap-2 rounded-xl bg-sky-600 hover:bg-sky-500 dark:bg-sky-600 dark:hover:bg-sky-500 px-6 py-3 text-sm font-bold text-white shadow-sm shadow-sky-600/20 transition"
          >
            <span>{{ t('Order Equipment') }}</span>
          </RouterLink>
          <RouterLink
            to="/courses"
            class="inline-flex items-center gap-2 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-6 py-3 text-sm font-bold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 transition"
          >
            <span>{{ t('Courses with Kit Included') }}</span>
          </RouterLink>
        </div>
      </div>
    </section>

    <!-- Products & Kits Categories -->
    <section class="mx-auto max-w-6xl px-4 sm:px-6 lg:px-8 mt-4">
      <div class="grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
        <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/80 p-6 shadow-xs">
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-sky-100 dark:bg-sky-950/50 text-sky-600 dark:text-sky-400 mb-4 text-xl">
            🤖
          </div>
          <h3 class="text-lg font-bold text-navy-900 dark:text-white">{{ t('Student Lab Kits') }}</h3>
          <p class="mt-2 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            {{ t('All-in-one robotics kits including microcontrollers, sensor modules, breadboards, jumper wires, and motors.') }}
          </p>
        </div>

        <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/80 p-6 shadow-xs">
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-sky-100 dark:bg-sky-950/50 text-sky-600 dark:text-sky-400 mb-4 text-xl">
            🚁
          </div>
          <h3 class="text-lg font-bold text-navy-900 dark:text-white">{{ t('FPV Drone Hardware') }}</h3>
          <p class="mt-2 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            {{ t('Carbon fiber frames, flight controllers, ESC stacks, brushless motors, propellers, and video transmitters.') }}
          </p>
        </div>

        <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-800/80 p-6 shadow-xs sm:col-span-2 lg:col-span-1">
          <div class="flex h-12 w-12 items-center justify-center rounded-xl bg-sky-100 dark:bg-sky-950/50 text-sky-600 dark:text-sky-400 mb-4 text-xl">
            🧰
          </div>
          <h3 class="text-lg font-bold text-navy-900 dark:text-white">{{ t('Tools & Accessories') }}</h3>
          <p class="mt-2 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            {{ t('Precision soldering stations, multimeter sets, hex screwdrivers, LiPo balance chargers, and safety gear.') }}
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
