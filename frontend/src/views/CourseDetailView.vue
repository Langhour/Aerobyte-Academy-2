<template>
  <div class="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8 pt-4 sm:pt-6 pb-10">
    <!-- Loading State -->
    <div v-if="loading" class="space-y-8 animate-pulse">
      <div class="grid grid-cols-1 sm:grid-cols-12 gap-5">
        <div class="sm:col-span-8 h-64 bg-slate-100 dark:bg-slate-800 rounded-2xl"></div>
        <div class="sm:col-span-4 h-64 bg-slate-100 dark:bg-slate-800 rounded-2xl"></div>
      </div>
      <div class="h-40 bg-slate-100 dark:bg-slate-800 rounded-2xl"></div>
    </div>

    <!-- Error / Not Found State -->
    <div v-else-if="loadError" role="alert" class="text-center py-16">
      <h2 class="text-xl font-bold text-navy-900 dark:text-white">{{ t('Unable to Load Course') }}</h2>
      <p class="text-xs text-slate-500 dark:text-slate-400 mt-2">{{ t(loadError) }}</p>
      <button
        type="button"
        @click="fetchCourseDetail"
        class="mt-4 inline-block rounded-lg bg-navy-800 px-5 py-2.5 text-xs font-semibold text-white"
      >
        {{ t('Retry') }}
      </button>
    </div>
    <div v-else-if="!course" class="text-center py-16">
      <h2 class="text-xl font-bold text-navy-900 dark:text-white">{{ t('Course Not Found') }}</h2>
      <p class="text-xs text-slate-500 dark:text-slate-400 mt-2">{{ t('The course you are looking for does not exist or has been moved.') }}</p>
      <router-link
        to="/courses"
        class="mt-4 inline-block px-5 py-2.5 rounded-lg bg-navy-800 text-white text-xs font-semibold"
      >
        {{ t('Back to Courses') }}
      </router-link>
    </div>

    <!-- Main Course Detail Content -->
    <div v-else class="space-y-8">
      <section class="grid grid-cols-1 sm:grid-cols-12 gap-5 items-start">
        <!-- Left Course Hero Image -->
        <div class="relative sm:col-span-8 aspect-[16/9] rounded-xl overflow-hidden bg-slate-100 dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700 shadow-card">
          <img
            v-if="course.image_url"
            :src="resolveImageUrl(course.image_url)"
            :alt="getCourseLocalized(course, 'title')"
            class="w-full h-full object-cover"
          />
          <div
            v-else
            class="flex h-full w-full items-center justify-center bg-gradient-to-br from-blue-50 via-slate-50 to-navy-50 dark:from-slate-800 dark:via-slate-700 dark:to-slate-800 text-navy-800 dark:text-slate-200"
            aria-hidden="true"
          >
            <component :is="getCourseIcon(course.category)" class="h-28 w-28 opacity-80" />
          </div>
          <span
            v-if="course.duration"
            class="absolute left-3 top-3 rounded-full bg-navy-900/80 dark:bg-slate-900/80 px-3 py-1 text-[10px] font-semibold text-white backdrop-blur-sm"
          >
            {{ getCourseLocalized(course, 'duration') }}
          </span>
        </div>

        <!-- Right Course Info & Pricing Card -->
        <div class="sm:col-span-4 bg-white dark:bg-slate-800 rounded-xl border border-slate-200/80 dark:border-slate-700 p-4 sm:p-5 shadow-card flex flex-col justify-between">
          <div>
            <div class="flex flex-wrap items-center gap-2 mb-2">
              <span class="px-2 py-0.5 rounded-sm bg-navy-800 dark:bg-slate-900 text-white text-[9px] font-bold uppercase tracking-wider">
                {{ getCourseLocalized(course, 'category') }}
              </span>
              <span v-if="course.level" class="px-2 py-0.5 rounded-sm bg-slate-100 dark:bg-slate-700 text-slate-600 dark:text-slate-300 text-[10px] font-semibold">
                {{ getCourseLocalized(course, 'level') }}
              </span>
            </div>

            <!-- Course Title -->
            <h1 class="text-sm font-extrabold text-navy-900 dark:text-white leading-snug">
              {{ getCourseLocalized(course, 'title') }}
            </h1>

            <!-- Course Description Box -->
            <div class="mt-3">
              <div class="mb-2 flex items-center gap-1.5 text-[9px] font-bold uppercase tracking-wide text-slate-500 dark:text-slate-400">
                <Globe2 class="h-3 w-3 text-sky-600" />
                <span>{{ t('Description') }}</span>
                <span v-if="course.language">({{ course.language === 'Khmer' ? t('Khmer script') : t(course.language) }})</span>
              </div>
              <p v-if="getCourseLocalized(course, 'short_description')" class="rounded-lg bg-slate-50 dark:bg-slate-900/60 p-3 text-[11px] text-slate-600 dark:text-slate-300 leading-relaxed">
                {{ getCourseLocalized(course, 'short_description') }}
              </p>
              <p v-else class="rounded-lg bg-slate-50 dark:bg-slate-900/60 p-3 text-[11px] text-slate-600 dark:text-slate-300 leading-relaxed">
                {{ t('Course description coming soon. Contact us for the current syllabus and schedule.') }}
              </p>
            </div>
          </div>

          <!-- Price & Enroll Button Footer -->
          <div class="mt-3 pt-3 border-t border-slate-100 dark:border-slate-700">
            <div class="flex items-center justify-between gap-2 mb-3">
              <span class="shrink-0 text-[11px] font-semibold text-slate-500 dark:text-slate-400">{{ t('Price') }}</span>
              <div class="flex min-w-0 items-baseline justify-end gap-1 whitespace-nowrap">
                <span
                  v-if="course.original_price"
                  class="text-[9px] text-slate-400 dark:text-slate-500 line-through"
                >
                  ${{ course.original_price.toFixed(2) }}
                </span>
                <span class="text-lg font-extrabold text-navy-900 dark:text-white">
                  ${{ course.price.toFixed(2) }}
                </span>
                <span class="text-[8px] text-slate-400 font-medium">USD</span>
              </div>
            </div>

            <button
              type="button"
              @click="goToEnrollment"
              class="w-full py-3 px-5 rounded-lg bg-navy-800 hover:bg-navy-900 dark:bg-indigo-600 dark:hover:bg-indigo-700 text-white text-[11px] font-bold tracking-wide transition shadow-sm flex items-center justify-center gap-2 cursor-pointer"
            >
              <span>{{ t('Enroll Now') }}</span>
              <ArrowRight class="w-4 h-4" />
            </button>
          </div>
        </div>
      </section>

      <section>
        <div class="flex items-center justify-between mb-3">
          <h2 class="text-[10px] font-bold uppercase tracking-wider text-slate-500 dark:text-slate-400">
            {{ t('Course Contents') }}
          </h2>
          <span v-if="course.modules.length" class="text-[10px] font-semibold text-sky-700 dark:text-sky-300 bg-sky-50 dark:bg-sky-950/60 px-2.5 py-1 rounded-full">
            {{ course.modules.length }} {{ t('Learning Modules Included') }}
          </span>
        </div>

        <div v-if="course.modules.length" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
          <div
            v-for="(mod, index) in course.modules"
            :key="mod.module_number"
            class="group rounded-xl border border-slate-200/90 dark:border-slate-700/80 bg-white dark:bg-slate-800 p-3.5 sm:p-4 transition-all duration-300 hover:border-slate-300 dark:hover:border-slate-600 hover:shadow-card flex flex-col justify-between"
          >
            <div>
              <div
                class="mb-3 flex h-36 sm:h-44 w-full items-center justify-center overflow-hidden rounded-lg bg-slate-100 dark:bg-slate-900/60"
                :class="!mod.image_url && moduleCardStyles[index % moduleCardStyles.length].background"
              >
                <img
                  v-if="mod.image_url"
                  :src="resolveImageUrl(mod.image_url)"
                  :alt="getModuleLocalized(mod, 'title')"
                  loading="lazy"
                  decoding="async"
                  class="h-full w-full object-cover transition-transform duration-500 group-hover:scale-105"
                />
                <component
                  v-else
                  :is="getModuleIcon(mod.icon_type)"
                  class="h-8 w-8 transition-transform duration-300 group-hover:scale-110"
                  :class="moduleCardStyles[index % moduleCardStyles.length].icon"
                />
                <span class="sr-only">{{ mod.module_number }}</span>
              </div>
              <div class="flex min-h-5 items-center justify-between gap-1.5">
                <span class="text-[9px] sm:text-[10px] font-extrabold uppercase tracking-wider text-sky-700 dark:text-sky-400">
                  {{ t('Module') }} {{ mod.module_number || index + 1 }}
                </span>
                <span
                  v-if="mod.icon_type"
                  class="max-w-28 truncate rounded-full bg-slate-100 dark:bg-slate-700/80 px-2 py-0.5 text-[8px] sm:text-[9px] font-semibold text-slate-600 dark:text-slate-300 border border-slate-200/60 dark:border-slate-600/60"
                >
                  {{ t(getModuleLabel(mod.icon_type)) }}
                </span>
              </div>
              <h3 class="mt-2 text-xs sm:text-sm font-bold leading-snug text-navy-900 dark:text-white">
                {{ getModuleLocalized(mod, 'title') }}
              </h3>
            </div>
            <p class="mt-2 text-[11px] sm:text-xs leading-relaxed text-slate-500 dark:text-slate-400 line-clamp-4">
              {{ getModuleLocalized(mod, 'description') }}
            </p>
          </div>
        </div>
        <div v-else class="flex flex-col gap-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-4 sm:flex-row sm:items-center sm:justify-between">
          <p class="text-xs leading-relaxed text-slate-600 dark:text-slate-300">
            {{ t('Course outline coming soon. Contact us for the current syllabus and upcoming schedules.') }}
          </p>
          <router-link
            to="/contact"
            class="inline-flex shrink-0 items-center justify-center rounded-lg border border-navy-800 dark:border-slate-600 px-4 py-2 text-[11px] font-semibold text-navy-800 dark:text-white transition hover:bg-navy-50 dark:hover:bg-slate-700"
          >
            {{ t('Contact Us') }}
          </router-link>
        </div>
      </section>

      <section>
        <h2 class="text-sm font-extrabold text-navy-900 dark:text-white mb-3">
          {{ t('Course Topics & Skills') }}
        </h2>

        <div v-if="course.hardware_specs.length" class="max-w-3xl space-y-2">
          <div
            v-for="(spec, idx) in course.hardware_specs"
            :key="spec.title"
            class="rounded-lg border transition overflow-hidden"
            :class="
              openSpecIndex === idx
                ? 'border-navy-800 dark:border-indigo-500 bg-white dark:bg-slate-800 shadow-sm'
                : 'border-slate-200/80 dark:border-slate-700 bg-white dark:bg-slate-800'
            "
          >
            <!-- Accordion Header -->
            <button
              type="button"
              @click="toggleSpec(idx)"
              class="w-full px-2.5 py-2.5 flex items-center justify-between text-left cursor-pointer"
              :aria-expanded="openSpecIndex === idx"
              :aria-controls="`hardware-spec-${idx}`"
            >
              <div class="flex items-center gap-3">
                <span class="grid h-5 w-5 shrink-0 place-items-center rounded bg-sky-50 dark:bg-slate-700 text-[9px] font-bold text-navy-800 dark:text-sky-300">
                  {{ String(idx + 1).padStart(2, '0') }}
                </span>
                <span class="text-[11px] sm:text-xs font-bold text-navy-900 dark:text-white">
                  {{ getSpecLocalized(spec, 'title') }}
                </span>
              </div>
              <ChevronDown
                class="w-3.5 h-3.5 text-slate-500 dark:text-slate-400 transition-transform duration-200"
                :class="{ 'rotate-180 text-navy-800 dark:text-indigo-400': openSpecIndex === idx }"
              />
            </button>

            <!-- Accordion Content -->
            <div
              :id="`hardware-spec-${idx}`"
              v-show="openSpecIndex === idx"
              class="px-4 pb-3 pt-2 border-t border-slate-100/80 dark:border-slate-700"
            >
              <ul class="space-y-1.5 pl-4 list-disc text-[10px] text-slate-600 dark:text-slate-300">
                <li v-for="item in getSpecItemsLocalized(spec)" :key="item" class="leading-relaxed">
                  {{ item }}
                </li>
              </ul>
            </div>
          </div>
        </div>
        <div v-else class="max-w-3xl rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-4">
          <p class="text-xs leading-relaxed text-slate-600 dark:text-slate-300">
            {{ t('Course topic details are being prepared. Contact us for the current syllabus.') }}
          </p>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import {
  Activity,
  ArrowRight,
  Bot,
  ChevronDown,
  Compass,
  Cpu,
  Globe2,
  Network,
  Package,
  Settings,
  Wifi,
  Wrench,
  Zap,
} from 'lucide-vue-next'
import { accountService, courseService } from '../services/api'
import {
  useLanguage,
  getCourseLocalized,
  getModuleLocalized,
  getSpecLocalized,
  getSpecItemsLocalized,
} from '../i18n'
import { resolveImageUrl } from '../utils/image'

const route = useRoute()
const router = useRouter()
const { t } = useLanguage()

const course = ref(null)
const loading = ref(true)
const loadError = ref('')
// Keep the first Hardware Specification accordion open by default (matches Figma)
const openSpecIndex = ref(0)
const moduleCardStyles = [
  { background: 'bg-slate-200/80 dark:bg-slate-700/80', icon: 'text-sky-600 dark:text-sky-400' },
  { background: 'bg-emerald-50 dark:bg-emerald-950/50', icon: 'text-emerald-600 dark:text-emerald-400' },
  { background: 'bg-indigo-50 dark:bg-indigo-950/50', icon: 'text-indigo-600 dark:text-indigo-400' },
  { background: 'bg-violet-50 dark:bg-violet-950/50', icon: 'text-violet-600 dark:text-violet-400' },
]

function toggleSpec(idx) {
  openSpecIndex.value = openSpecIndex.value === idx ? -1 : idx
}

function getModuleIcon(iconType) {
  const map = {
    cpu: Cpu,
    activity: Activity,
    settings: Settings,
    compass: Compass,
    zap: Zap,
    package: Package,
    'core pcb': Cpu,
    telemetry: Activity,
    motors: Settings,
    frame: Package,
  }
  return map[String(iconType || '').toLowerCase()] || Cpu
}

function getModuleLabel(iconType) {
  const labels = {
    cpu: 'Foundations',
    activity: 'Hands-on',
    settings: 'Core Skills',
    compass: 'Design',
    package: 'Project',
    zap: 'Power',
  }
  return labels[String(iconType || '').toLowerCase()] || iconType
}

function getCourseIcon(category) {
  const icons = {
    Robotics: Bot,
    Mechanical: Wrench,
    IoT: Wifi,
    Electronics: Cpu,
    ROS: Network,
  }
  return icons[category] || Bot
}

async function goToEnrollment() {
  if (!course.value) return
  const target = course.value.slug || course.value.id
  if (!target) return
  const enrollPath = `/enroll/${encodeURIComponent(target)}`

  try {
    const { data } = await accountService.getSession()
    if (data?.authenticated) {
      router.push(enrollPath)
      return
    }
  } catch (err) {
    console.error('Session check failed before enrollment:', err)
  }

  router.push({
    path: '/account',
    query: {
      mode: 'register',
      redirect: enrollPath,
    },
  })
}

async function fetchCourseDetail() {
  loading.value = true
  loadError.value = ''
  openSpecIndex.value = 0
  try {
    const { data } = await courseService.getCourseById(route.params.id)
    course.value = data
  } catch (err) {
    console.error('Failed to load course detail:', err)
    course.value = null
    loadError.value = 'Please check your connection and try again.'
  } finally {
    loading.value = false
  }
}

watch(() => route.params.id, fetchCourseDetail, { immediate: true })
</script>
