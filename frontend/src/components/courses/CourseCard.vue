<template>
  <article
    @click="goToDetail"
    class="group bg-white dark:bg-slate-800 rounded-2xl border border-slate-200/80 dark:border-slate-700/80 overflow-hidden shadow-card hover:shadow-card-hover dark:shadow-slate-900/30 transition-all duration-300 flex flex-col cursor-pointer hover:border-slate-300 dark:hover:border-slate-600"
  >
    <!-- Thumbnail Container with Badges -->
    <RouterLink
      :to="courseLink"
      class="relative block h-44 w-full overflow-hidden bg-slate-100 dark:bg-slate-700"
      tabindex="-1"
      aria-hidden="true"
    >
      <img
        v-if="course.image_url"
        :src="cardImageUrl"
        :alt="getCourseLocalized(course, 'title')"
        :loading="priority ? 'eager' : 'lazy'"
        :fetchpriority="priority ? 'high' : 'auto'"
        decoding="async"
        width="360"
        height="176"
        class="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
      />
      <div
        v-else
        class="flex h-full w-full items-center justify-center bg-gradient-to-br from-blue-50 via-slate-50 to-navy-50 dark:from-slate-800 dark:via-slate-700 dark:to-slate-800 text-navy-800 dark:text-slate-200"
        aria-hidden="true"
      >
        <component :is="getCourseIcon(course.category)" class="h-14 w-14 opacity-80" />
      </div>

      <!-- Top-Left Category Badge -->
      <span class="absolute top-3 left-3 px-2.5 py-1 rounded-md bg-navy-800/90 dark:bg-slate-900/90 backdrop-blur-sm text-white text-[10px] font-bold uppercase tracking-wider">
        {{ getCourseLocalized(course, 'category') }}
      </span>

      <!-- Top-Right Discount Badge -->
      <span
        v-if="course.discount_badge"
        class="absolute top-3 right-3 px-2.5 py-1 rounded-md bg-accent-orange text-white text-[10px] font-bold uppercase tracking-wider shadow-xs"
      >
        {{ course.discount_badge }}
      </span>

      <div
        v-if="getCourseBadges(course).length"
        class="absolute bottom-3 left-3 flex flex-wrap gap-1"
      >
        <span v-for="badge in getCourseBadges(course)" :key="badge" class="rounded-md bg-white/95 dark:bg-slate-800/95 px-2 py-1 text-[10px] font-bold text-navy-900 dark:text-slate-100 shadow-sm dark:shadow-slate-900/30">
          {{ badge }}
        </span>
      </div>

      <!-- Bottom-Right Level Pill -->
      <span v-if="course.level" class="absolute bottom-3 right-3 px-2.5 py-0.5 rounded-md bg-navy-900/80 dark:bg-slate-900/80 backdrop-blur-sm text-white text-[10px] font-medium">
        {{ getCourseLocalized(course, 'level') }}
      </span>
    </RouterLink>

    <!-- Card Body -->
    <div class="p-4 flex-1 flex flex-col justify-between">
      <div>
        <RouterLink
          :to="courseLink"
          class="min-h-10 text-sm font-bold text-navy-900 dark:text-white group-hover:text-navy-600 dark:group-hover:text-indigo-400 transition line-clamp-2 block hover:underline"
        >
          {{ getCourseLocalized(course, 'title') }}
        </RouterLink>
        <p v-if="course.short_description" class="mt-1.5 text-xs text-slate-500 dark:text-slate-400 leading-relaxed line-clamp-2">
          {{ getCourseLocalized(course, 'short_description') }}
        </p>
      </div>

      <!-- Price & Action Button Footer -->
      <div class="mt-4 pt-3 border-t border-slate-100 dark:border-slate-700/80 flex items-center justify-between">
        <div class="flex items-baseline gap-1.5">
          <span
            class="text-sm font-extrabold"
            :class="course.original_price ? 'text-accent-orange' : 'text-navy-900 dark:text-white'"
          >
            ${{ course.price.toFixed(2) }}
          </span>
          <span
            v-if="course.original_price"
            class="text-[11px] text-slate-500 dark:text-slate-400 line-through"
          >
            ${{ course.original_price.toFixed(2) }}
          </span>
        </div>

        <!-- Circular Arrow Button -->
        <RouterLink
          :to="courseLink"
          @click.stop
          class="w-7 h-7 rounded-full bg-navy-50 text-navy-800 dark:bg-slate-700 dark:text-slate-200 group-hover:bg-navy-800 dark:group-hover:bg-indigo-600 group-hover:text-white flex items-center justify-center transition"
          :aria-label="`${t('View course details')}: ${getCourseLocalized(course, 'title')}`"
        >
          <ChevronRight class="w-4 h-4" />
        </RouterLink>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'
import { RouterLink, useRouter } from 'vue-router'
import { Bot, ChevronRight, Cpu, Network, Wifi, Wrench } from 'lucide-vue-next'
import { useLanguage, getCourseLocalized, getCourseBadges } from '../../i18n'
import { resolveImageUrl } from '../../utils/image'

const props = defineProps({
  course: {
    type: Object,
    required: true
  },
  priority: {
    type: Boolean,
    default: false
  }
})

const router = useRouter()
const { t } = useLanguage()

const cardImageUrl = computed(() => {
  const base = resolveImageUrl(props.course?.image_url)
  if (!base) return ''
  if (base.includes('/uploads/')) {
    const sep = base.includes('?') ? '&' : '?'
    return `${base}${sep}w=640`
  }
  if (base.includes('images.unsplash.com')) {
    try {
      const url = new URL(base)
      url.searchParams.set('w', '600')
      url.searchParams.set('auto', 'format')
      url.searchParams.set('q', '75')
      return url.toString()
    } catch {
      return base
    }
  }
  return base
})

const courseLink = computed(() => {
  const target = props.course?.slug || props.course?.id
  return target ? `/courses/${encodeURIComponent(target)}` : '/courses'
})

function goToDetail(e) {
  // If clicked directly on an anchor or button inside the card, let the link proceed
  if (e?.target?.closest('a, button')) return
  if (courseLink.value) {
    router.push(courseLink.value)
  }
}

function getCourseIcon(category) {
  const map = {
    Robotics: Bot,
    Mechanical: Wrench,
    IoT: Wifi,
    Electronics: Cpu,
    ROS: Network
  }
  return map[category] || Bot
}
</script>
