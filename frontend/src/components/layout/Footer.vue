<template>
  <footer class="mt-12 border-t border-slate-200 dark:border-slate-800 bg-slate-50 dark:bg-slate-900 transition-colors">
    <div
      class="mx-auto grid max-w-[1408px] grid-cols-1 gap-8 px-4 py-8 sm:px-8 sm:py-12 md:grid-cols-2 lg:grid-cols-[1.2fr_1fr_1fr_1fr] lg:gap-12 lg:px-10 lg:py-14"
    >
      <section>
        <RouterLink
          to="/courses"
          class="flex w-fit items-center gap-2.5 text-xl font-extrabold leading-tight tracking-tight text-slate-900 dark:text-white sm:text-3xl"
        >
          <img src="/aerobyte-logo.png" alt="" width="48" height="40" loading="lazy" class="h-9 w-11 sm:h-10 sm:w-12 shrink-0 object-contain transition duration-200 dark:brightness-0 dark:invert" />
          <span>AeroByte Academy</span>
        </RouterLink>
        <p class="mt-4 sm:mt-5 max-w-sm text-sm sm:text-base leading-relaxed text-slate-600 dark:text-slate-400">
          {{ t(siteSettings.footer_description || 'Start learning today, build something amazing tomorrow, and grow with AeroByte Academy.') }}
        </p>
      </section>

      <section>
        <h2 class="text-sm font-extrabold text-navy-900 dark:text-white">{{ t('Navigation') }}</h2>
        <nav class="mt-5 flex flex-col items-start gap-3 text-sm text-slate-600 dark:text-slate-400" :aria-label="t('Footer navigation')">
          <RouterLink to="/courses" class="transition hover:text-navy-900 dark:hover:text-white">{{ t('Courses') }}</RouterLink>
          <RouterLink to="/store" class="transition hover:text-navy-900 dark:hover:text-white flex items-center gap-1.5 font-semibold text-navy-900 dark:text-white">
            <span>{{ t('Aero Store') }}</span>
            <span class="px-1.5 py-0.2 rounded text-[10px] bg-indigo-100 dark:bg-indigo-900 text-indigo-700 dark:text-indigo-300 font-bold">New</span>
          </RouterLink>
          <RouterLink to="/print" class="transition hover:text-navy-900 dark:hover:text-white">{{ t('Aero Print') }}</RouterLink>
          <RouterLink to="/fly" class="transition hover:text-navy-900 dark:hover:text-white">{{ t('Aero Fly') }}</RouterLink>
          <RouterLink to="/questions" class="transition hover:text-navy-900 dark:hover:text-white">{{ t('Questions') }}</RouterLink>
          <RouterLink to="/about" class="transition hover:text-navy-900 dark:hover:text-white">{{ t('About') }}</RouterLink>
          <RouterLink to="/contact" class="transition hover:text-navy-900 dark:hover:text-white">{{ t('Contact Us') }}</RouterLink>
        </nav>
      </section>

      <section>
        <h2 class="text-sm font-extrabold text-navy-900 dark:text-white">{{ t('Categories') }}</h2>
        <nav class="mt-5 flex flex-col items-start gap-3 text-sm text-slate-600 dark:text-slate-400" :aria-label="t('Course categories')">
          <RouterLink
            v-for="category in categories"
            :key="category"
            :to="{ path: '/courses', query: { category } }"
            class="transition hover:text-navy-900 dark:hover:text-white"
          >
            {{ t(category) }}
          </RouterLink>
        </nav>
      </section>

      <section>
        <h2 class="text-sm font-extrabold text-navy-900 dark:text-white">{{ t('Legal & Support') }}</h2>
        <div class="mt-5 flex flex-col items-start gap-3 text-sm text-slate-600 dark:text-slate-400">
          <a v-if="siteSettings.contact_email" :href="`mailto:${siteSettings.contact_email}`" class="transition hover:text-navy-900 dark:hover:text-white">{{ siteSettings.contact_email }}</a>
          <a v-if="siteSettings.contact_phone" :href="`tel:${siteSettings.contact_phone}`" class="transition hover:text-navy-900 dark:hover:text-white">{{ siteSettings.contact_phone }}</a>
          <RouterLink to="/terms" class="transition hover:text-navy-900 dark:hover:text-white">{{ t('Terms of use') }}</RouterLink>
          <RouterLink to="/privacy" class="transition hover:text-navy-900 dark:hover:text-white">{{ t('Privacy Policy') }}</RouterLink>
          <a
            href="https://maps.app.goo.gl/Pj7oV9NrPmbc5mnFA"
            target="_blank"
            rel="noopener noreferrer"
            class="text-sm leading-relaxed text-slate-600 dark:text-slate-400 transition hover:text-navy-900 dark:hover:text-white"
            :title="t('View on Google Maps')"
          >
            <span class="block font-extrabold text-navy-900 dark:text-white">{{ t('Location') }}</span>
            <span class="block">{{ t('Phum Lekh Muoy, Sangkat Svay Rolum Ta Khmau, Kandal 08110701') }}</span>
          </a>
        </div>
      </section>
    </div>

    <div class="border-t border-slate-200 dark:border-slate-800">
      <p class="mx-auto max-w-7xl px-4 py-5 text-center text-xs text-slate-500 dark:text-slate-400 sm:px-6 lg:px-8">
        &copy; {{ new Date().getFullYear() }} AeroByte Academy &middot; {{ t('All rights reserved.') }}
      </p>
    </div>
  </footer>
</template>

<script setup>
import { onMounted, reactive } from 'vue'
import { useLanguage } from '../../i18n'
import { siteSettingsService } from '../../services/api'

const categories = ['Robotics', 'Mechanical', 'IoT', 'Electronics', 'ROS']
const { t } = useLanguage()
const siteSettings = reactive({ footer_description: '', contact_email: '', contact_phone: '' })

onMounted(async () => {
  try {
    const { data } = await siteSettingsService.getPublicSettings()
    Object.assign(siteSettings, data)
  } catch (error) {
    console.error('Unable to load public footer settings:', error)
  }
})
</script>
