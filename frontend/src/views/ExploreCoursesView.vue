<template>
  <div class="pb-16 dark:bg-slate-900 transition-colors">
    <section class="courses-hero px-4 pb-10 pt-8 text-center sm:px-6 sm:pb-20 sm:pt-16 lg:px-8">
      <div class="mx-auto max-w-7xl">
        <h1 class="text-2xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-navy-900 dark:text-white">
          {{ t('Explore Our Courses') }}
        </h1>
        <p class="mx-auto mt-2.5 sm:mt-4 max-w-3xl text-sm sm:text-base leading-relaxed text-slate-600 dark:text-slate-300 sm:text-lg">
          {{ t('Learn practical technology skills through hands-on courses designed by industry engineers.') }}
        </p>

        <div class="relative mx-auto mt-6 sm:mt-9 max-w-[784px]">
          <Search class="pointer-events-none absolute left-4 sm:left-5 top-1/2 h-4 w-4 sm:h-5 sm:w-5 -translate-y-1/2 text-slate-400" />
          <input
            v-model="searchQuery"
            @input="handleSearchInput"
            type="text"
            :placeholder="t('Search courses...')"
            class="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 py-3 sm:py-[18px] pl-11 sm:pl-14 pr-10 sm:pr-12 text-sm sm:text-base text-slate-800 dark:text-white shadow-xs transition placeholder:text-slate-500 dark:placeholder:text-slate-400 focus:border-transparent focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500"
          />
          <button
            v-if="searchQuery"
            type="button"
            :aria-label="t('Clear search')"
            @click="clearSearch"
            class="absolute right-3.5 sm:right-4 top-1/2 -translate-y-1/2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200"
          >
            <X class="h-4 w-4 sm:h-5 sm:w-5" />
          </button>
        </div>
      </div>
    </section>

    <!-- Main Layout: Sidebar (3 cols) + Course Grid (9 cols) -->
    <div class="mx-auto grid max-w-7xl grid-cols-1 items-start gap-6 lg:gap-8 px-3 sm:px-6 lg:grid-cols-12 lg:px-8 pt-5 sm:pt-8">
      <!-- Left Filter Sidebar -->
      <div class="lg:col-span-3">
        <FilterSidebar
          v-model="filters"
          @change="onFilterChange"
          @reset="resetAllFilters"
        />
      </div>

      <!-- Right Course Catalog Content -->
      <div class="lg:col-span-9 min-h-[720px]">
        <!-- Loading Skeleton -->
        <div v-if="loading" class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-6">
          <div
            v-for="n in 9"
            :key="n"
            class="h-80 rounded-2xl bg-slate-100 dark:bg-slate-800 animate-pulse"
          ></div>
        </div>

        <div
          v-else-if="loadError"
          role="alert"
          class="rounded-2xl border border-red-200 dark:border-red-900/50 bg-red-50 dark:bg-red-950/40 p-8 text-center"
        >
          <p class="text-sm font-bold text-red-800 dark:text-red-300">{{ t(loadError) }}</p>
          <button
            type="button"
            @click="fetchCourses"
            class="mt-4 rounded-lg bg-navy-800 px-4 py-2 text-xs font-semibold text-white hover:bg-navy-900"
          >
            {{ t('Retry') }}
          </button>
        </div>

        <!-- Empty State -->
        <div
          v-else-if="courses.length === 0"
          class="bg-navy-50/50 dark:bg-slate-800/60 rounded-2xl border border-dashed border-slate-200 dark:border-slate-700 p-12 text-center"
        >
          <p class="text-sm font-bold text-navy-900 dark:text-white">{{ t('No courses match your selected filters') }}</p>
          <p class="text-xs text-slate-500 dark:text-slate-400 mt-1">
            {{ t('Try clearing some filters or searching for another robotics or IoT topic.') }}
          </p>
          <button
            @click="resetAllFilters"
            class="mt-4 px-4 py-2 rounded-lg bg-navy-800 text-white text-xs font-semibold hover:bg-navy-900 transition"
          >
            {{ t('Reset Filters') }}
          </button>
        </div>

        <!-- Default course catalog -->
        <div v-else-if="!hasActiveFilters" class="space-y-10">
          <section
            v-for="(group, gIdx) in groupedCourses"
            :key="group.title"
          >
            <div class="flex items-center justify-between mb-4">
              <h2 class="text-xs font-bold uppercase tracking-wider text-slate-400 dark:text-slate-300">
                {{ t(group.title) }}
              </h2>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
              <CourseCard
                v-for="(course, cIdx) in group.items"
                :key="course.id"
                :course="course"
                :priority="gIdx === 0 && cIdx === 0"
              />
            </div>
          </section>
        </div>

        <!-- Filtered / Search Results View -->
        <div v-else>
          <div class="flex items-center justify-between mb-4">
            <p class="text-xs font-semibold text-slate-500 dark:text-slate-400">
              {{ t('Showing') }} <span class="text-navy-900 dark:text-white font-bold">{{ totalCourses }}</span> {{ t('result(s)') }}
            </p>
            <button
              @click="resetAllFilters"
              class="text-xs font-semibold text-accent-orange hover:underline"
            >
              {{ t('Reset all filters') }}
            </button>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
            <CourseCard
              v-for="(course, idx) in courses"
              :key="course.id"
              :course="course"
              :priority="idx === 0"
            />
          </div>
        </div>

        <!-- Bottom Pagination Bar -->
        <Pagination
          :current-page="currentPage"
          :total-pages="totalPages"
          @page-change="handlePageChange"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Search, X } from 'lucide-vue-next'
import { courseService } from '../services/api'
import FilterSidebar from '../components/courses/FilterSidebar.vue'
import CourseCard from '../components/courses/CourseCard.vue'
import Pagination from '../components/courses/Pagination.vue'
import { useLanguage } from '../i18n'

const route = useRoute()
const router = useRouter()
const { t } = useLanguage()

const courses = ref([])
const loading = ref(false)
const searchQuery = ref('')
const currentPage = ref(1)
const totalPages = ref(1)
const totalCourses = ref(0)
const loadError = ref('')

const filters = ref({
  categories: [],
  levels: [],
  price_range: 'all',
  languages: []
})

// Check if any search or sidebar filter is currently active
const hasActiveFilters = computed(() => {
  return (
    searchQuery.value.trim() !== '' ||
    filters.value.categories.length > 0 ||
    filters.value.levels.length > 0 ||
    filters.value.price_range !== 'all' ||
    filters.value.languages.length > 0
  )
})

const groupedCourses = computed(() => {
  const sections = ['Courses']
  return sections
    .map((title) => ({
      title,
      items: courses.value.filter((c) => c.section_group === title)
    }))
    .filter((g) => g.items.length > 0)
})

let searchTimeout = null
function handleSearchInput() {
  clearTimeout(searchTimeout)
  searchTimeout = setTimeout(() => {
    currentPage.value = 1
    fetchCourses()
  }, 250)
}

function clearSearch() {
  searchQuery.value = ''
  currentPage.value = 1
  fetchCourses()
}

function onFilterChange() {
  currentPage.value = 1
  fetchCourses()
}

function resetAllFilters() {
  searchQuery.value = ''
  filters.value = {
    categories: [],
    levels: [],
    price_range: 'all',
    languages: []
  }
  currentPage.value = 1
  if (route.query.category) {
    router.replace({ path: '/courses' })
  }
  fetchCourses()
}

function handlePageChange(page) {
  currentPage.value = page
  fetchCourses()
  window.scrollTo({ top: 200, behavior: 'smooth' })
}

async function fetchCourses() {
  loadError.value = ''
  const params = {
    page: currentPage.value,
    limit: 12
  }
  if (searchQuery.value.trim()) {
    params.search = searchQuery.value.trim()
  }
  if (filters.value.categories.length > 0) {
    params.categories = filters.value.categories
  }
  if (filters.value.levels.length > 0) {
    params.levels = filters.value.levels
  }
  if (filters.value.price_range !== 'all') {
    params.price_range = filters.value.price_range
  }
  if (filters.value.languages.length > 0) {
    params.languages = filters.value.languages
  }

  // Instant Cache Recall (Stale-While-Revalidate) so cards pop up with zero delay
  const cacheKey = `courses_cache_${JSON.stringify(params)}`
  try {
    const cached = sessionStorage.getItem(cacheKey)
    if (cached) {
      const parsed = JSON.parse(cached)
      if (Array.isArray(parsed?.courses) && parsed.courses.length > 0) {
        courses.value = parsed.courses
        totalCourses.value = parsed.total || parsed.courses.length
        totalPages.value = parsed.total_pages || 1
        loading.value = false
      }
    }
  } catch {}

  if (courses.value.length === 0) {
    loading.value = true
  }

  try {
    const { data } = await courseService.getCourses(params)
    courses.value = data.courses
    totalCourses.value = data.total
    totalPages.value = data.total_pages
    try {
      sessionStorage.setItem(cacheKey, JSON.stringify(data))
    } catch {}
  } catch (error) {
    console.error('Failed to fetch courses:', error)
    if (courses.value.length === 0) {
      loadError.value = 'Could not load courses. Check that the API server is running and try again.'
    }
  } finally {
    loading.value = false
  }
}

// Watch for category query links clicked in the Footer (e.g. /courses?category=Robotics)
watch(
  () => route.query.category,
  (newCategory) => {
    if (newCategory) {
      filters.value.categories = [newCategory]
      currentPage.value = 1
      fetchCourses()
    }
  },
  { immediate: true }
)

onMounted(() => {
  if (!route.query.category) {
    fetchCourses()
  }
})
</script>
