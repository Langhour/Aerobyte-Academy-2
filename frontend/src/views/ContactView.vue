<template>
  <div class="pb-16 dark:bg-slate-900 transition-colors">
    <section class="courses-hero px-4 pb-10 pt-8 text-center sm:px-6 sm:pb-16 sm:pt-14 lg:px-8">
      <div class="mx-auto max-w-7xl">
        <h1 class="mt-2 text-2xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-navy-900 dark:text-white">
          {{ t('Contact Us') }}
        </h1>
        <p class="mx-auto mt-2.5 sm:mt-4 max-w-5xl text-sm sm:text-base leading-relaxed text-slate-600 dark:text-slate-300 sm:text-lg">
          {{ t('Follow AeroByte Academy for course updates, project highlights, and support.') }}
        </p>
      </div>
    </section>

    <section class="mx-auto mt-6 sm:mt-8 max-w-5xl px-3 sm:px-6 lg:px-8">
      <div class="mb-5 sm:mb-6">
        <h2 class="text-lg sm:text-xl font-extrabold text-navy-900 dark:text-white">{{ t('Connect with us') }}</h2>
        <p class="mt-1 text-xs sm:text-sm text-slate-500 dark:text-slate-400">{{ t('Choose your preferred platform to reach and follow us.') }}</p>
      </div>

      <div class="grid gap-3.5 sm:gap-4 sm:grid-cols-2">
        <a
          v-for="social in socialLinks"
          :key="social.name"
          :href="social.url"
          target="_blank"
          rel="noopener noreferrer"
          class="group flex min-h-24 sm:min-h-32 items-center gap-3.5 sm:gap-4 rounded-xl sm:rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-4 sm:p-5 shadow-xs transition hover:-translate-y-0.5 hover:border-navy-200 dark:hover:border-slate-600 hover:shadow-card"
          :aria-label="`${t('Follow us on')} ${social.name} (${social.handle})`"
        >
          <!-- Social Brand Logo (Clean standalone icon, no background container frame) -->
          <div class="flex h-12 w-12 sm:h-14 sm:w-14 shrink-0 items-center justify-center transition group-hover:scale-105">
            <img v-if="social.image" :src="social.image" alt="" class="h-10 w-10 sm:h-12 sm:w-12 object-contain" />
            <component v-else :is="social.icon" class="h-7 w-7" :class="social.iconColor" aria-hidden="true" />
          </div>
          <span class="min-w-0 flex-1">
            <span class="block text-base font-extrabold text-navy-900 dark:text-white">{{ social.name }}</span>
            <span class="mt-1 block truncate text-sm text-slate-500 dark:text-slate-400">{{ social.handle }}</span>
            <span class="mt-2 inline-flex items-center gap-1 text-xs font-bold text-navy-800 dark:text-indigo-400">
              {{ t('Visit our page') }}
              <ArrowUpRight class="h-3.5 w-3.5 transition group-hover:translate-x-0.5 group-hover:-translate-y-0.5" aria-hidden="true" />
            </span>
          </span>
        </a>
      </div>

      <div class="mt-8 flex flex-col gap-4 rounded-2xl border border-navy-100 dark:border-slate-700 bg-navy-50/70 dark:bg-slate-800/80 p-5 sm:flex-row sm:items-center sm:justify-between sm:px-6">
        <div class="flex items-start gap-3">
          <span class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-white dark:bg-slate-700 text-navy-800 dark:text-slate-200">
            <BookOpenText class="h-5 w-5" aria-hidden="true" />
          </span>
          <div>
            <h2 class="text-sm font-extrabold text-navy-900 dark:text-white">{{ t('Looking for course information?') }}</h2>
            <p class="mt-1 text-sm leading-5 text-slate-600 dark:text-slate-300">{{ t('Browse our programs and find the right place to start.') }}</p>
          </div>
        </div>
        <RouterLink
          to="/courses"
          class="inline-flex shrink-0 items-center justify-center gap-2 rounded-xl bg-navy-900 dark:bg-indigo-600 px-5 py-3 text-sm font-bold text-white transition hover:bg-navy-800 dark:hover:bg-indigo-700"
        >
          {{ t('Explore Courses') }}
          <ArrowRight class="h-4 w-4" aria-hidden="true" />
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ArrowRight, ArrowUpRight, BookOpenText, Facebook, Music2, Send, Youtube } from 'lucide-vue-next'
import { useLanguage } from '../i18n'

const { t } = useLanguage()

const socialLinks = [
  {
    name: 'YouTube',
    handle: '@aerobyte168',
    url: 'https://www.youtube.com/@aerobyte168',
    image: '/youtube-icon.png',
    icon: Youtube,
    iconBackground: 'bg-red-50 dark:bg-red-950/60',
    iconColor: 'text-red-600 dark:text-red-400',
  },
  {
    name: 'Facebook',
    handle: 'AeroByte Academy',
    url: 'https://www.facebook.com/Robotxacademy168',
    image: '/facebook-icon.png',
    icon: Facebook,
    iconBackground: 'bg-blue-50 dark:bg-blue-950/60',
    iconColor: 'text-blue-600 dark:text-blue-400',
  },
  {
    name: 'Telegram',
    handle: 't.me/aerobyte168',
    url: 'https://t.me/aerobyte168',
    image: '/telegram-icon.png',
    icon: Send,
    iconBackground: 'bg-sky-50 dark:bg-sky-950/60',
    iconColor: 'text-sky-600 dark:text-sky-400',
  },
  {
    name: 'TikTok',
    handle: '@aero.byte.academy168',
    url: 'https://www.tiktok.com/@aero.byte.academy168',
    image: '/tiktok-icon.png',
    icon: Music2,
    iconBackground: 'bg-slate-100 dark:bg-slate-700',
    iconColor: 'text-slate-900 dark:text-white',
  },
]
</script>
