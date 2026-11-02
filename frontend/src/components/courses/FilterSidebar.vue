<template>
  <aside class="bg-white rounded-xl sm:rounded-2xl border border-slate-200/80 p-4 sm:p-5 shadow-card lg:sticky lg:top-24 dark:bg-slate-800 dark:border-slate-700 dark:shadow-slate-900/20">
    <!-- Header: Static heading on desktop, Accordion toggle button on mobile -->
    <div class="flex items-center justify-between pb-3 sm:pb-4 border-b border-slate-100 dark:border-slate-700 mb-4">
      <!-- Desktop: Static Title (NOT clickable, cursor-default) -->
      <div class="hidden lg:flex items-center gap-2 select-none cursor-default">
        <h2 class="text-sm font-bold text-navy-900 dark:text-white">{{ t('Filters') }}</h2>
        <span
          v-if="activeFilterCount > 0"
          class="px-2 py-0.5 rounded-full bg-navy-100 dark:bg-indigo-900/60 text-[10px] font-bold text-navy-800 dark:text-indigo-300"
        >
          {{ activeFilterCount }}
        </span>
      </div>

      <!-- Mobile / Tablet (< lg): Clickable Toggle Button with Chevron -->
      <button
        type="button"
        @click="mobileOpen = !mobileOpen"
        class="lg:hidden flex items-center gap-2 text-sm font-bold text-navy-900 dark:text-white cursor-pointer select-none"
        :aria-expanded="mobileOpen"
        aria-controls="filters-content"
      >
        <span>{{ t('Filters') }}</span>
        <span
          v-if="activeFilterCount > 0"
          class="px-2 py-0.5 rounded-full bg-navy-100 dark:bg-indigo-900/60 text-[10px] font-bold text-navy-800 dark:text-indigo-300"
        >
          {{ activeFilterCount }}
        </span>
        <ChevronDown
          class="w-4 h-4 text-slate-400 transition-transform duration-200"
          :class="{ 'rotate-180 text-navy-800 dark:text-indigo-400': mobileOpen }"
        />
      </button>

      <!-- Clear All Button -->
      <button
        v-if="activeFilterCount > 0"
        type="button"
        @click="$emit('reset')"
        class="text-[11px] font-semibold text-slate-400 hover:text-accent-orange transition dark:text-slate-400 dark:hover:text-accent-orange cursor-pointer"
      >
        {{ t('Clear All') }}
      </button>
    </div>

    <!-- Filter Body (collapsible on mobile, always visible on desktop) -->
    <div id="filters-content" :class="mobileOpen ? 'block' : 'hidden lg:block'" class="pt-1 lg:pt-0">
      <!-- 1. Category Filter -->
      <div class="pb-5 mb-5 border-b border-slate-100 dark:border-slate-700">
        <h3 class="text-xs font-bold uppercase tracking-wider text-navy-900 mb-2 dark:text-slate-200 select-none">{{ t('Category') }}</h3>
        <div class="space-y-1">
          <label
            v-for="cat in categoryOptions"
            :key="cat"
            :for="`filter-cat-${cat}`"
            class="flex items-center gap-2.5 px-2 py-1.5 -mx-2 rounded-lg cursor-pointer select-none hover:bg-slate-50 dark:hover:bg-slate-700/60 transition group"
          >
            <input
              :id="`filter-cat-${cat}`"
              type="checkbox"
              :value="cat"
              v-model="localFilters.categories"
              @change="emitUpdate"
              class="w-4 h-4 rounded border-slate-300 dark:border-slate-600 text-navy-800 dark:text-indigo-500 focus:ring-navy-800 dark:bg-slate-700 cursor-pointer"
            />
            <span class="text-xs text-slate-600 dark:text-slate-300 group-hover:text-navy-900 dark:group-hover:text-white transition">
              {{ t(cat) }}
            </span>
          </label>
        </div>
      </div>

      <!-- 2. Price Range Filter -->
      <div class="pb-5 mb-5 border-b border-slate-100 dark:border-slate-700">
        <h3 class="text-xs font-bold uppercase tracking-wider text-navy-900 mb-2 dark:text-slate-200 select-none">{{ t('Price') }}</h3>
        <div class="space-y-1">
          <label
            v-for="price in priceOptions"
            :key="price.value"
            :for="`filter-price-${price.value}`"
            class="flex items-center gap-2.5 px-2 py-1.5 -mx-2 rounded-lg cursor-pointer select-none hover:bg-slate-50 dark:hover:bg-slate-700/60 transition group"
          >
            <input
              :id="`filter-price-${price.value}`"
              type="radio"
              name="price_range"
              :value="price.value"
              v-model="localFilters.price_range"
              @change="emitUpdate"
              class="w-4 h-4 border-slate-300 dark:border-slate-600 text-navy-800 dark:text-indigo-500 focus:ring-navy-800 dark:bg-slate-700 cursor-pointer"
            />
            <span class="text-xs text-slate-600 dark:text-slate-300 group-hover:text-navy-900 dark:group-hover:text-white transition">
              {{ t(price.label) }}
            </span>
          </label>
        </div>
      </div>

      <!-- 3. Language Filter -->
      <div>
        <h3 class="text-xs font-bold uppercase tracking-wider text-navy-900 mb-2 dark:text-slate-200 select-none">{{ t('Language') }}</h3>
        <div class="space-y-1">
          <label
            v-for="language in languageOptions"
            :key="language"
            :for="`filter-lang-${language}`"
            class="flex items-center gap-2.5 px-2 py-1.5 -mx-2 rounded-lg cursor-pointer select-none hover:bg-slate-50 dark:hover:bg-slate-700/60 transition group"
          >
            <input
              :id="`filter-lang-${language}`"
              type="checkbox"
              :value="language"
              v-model="localFilters.languages"
              @change="emitUpdate"
              class="w-4 h-4 rounded border-slate-300 dark:border-slate-600 text-navy-800 dark:text-indigo-500 focus:ring-navy-800 dark:bg-slate-700 cursor-pointer"
            />
            <span class="text-xs text-slate-600 dark:text-slate-300 group-hover:text-navy-900 dark:group-hover:text-white transition">
              {{ t(language) }}
            </span>
          </label>
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed, reactive, ref, watch } from 'vue'
import { ChevronDown } from 'lucide-vue-next'
import { useLanguage } from '../../i18n'

const { t } = useLanguage()

const mobileOpen = ref(false)

const props = defineProps({
  modelValue: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:modelValue', 'change', 'reset'])

const categoryOptions = ['Robotics', 'Mechanical', 'IoT', 'Electronics', 'ROS']
const languageOptions = ['English', 'Khmer']
const priceOptions = [
  { label: 'All', value: 'all' },
  { label: 'Under $100', value: 'under_100' },
  { label: '$100 - $200', value: '100_200' },
  { label: '$200+', value: 'over_200' }
]
const localFilters = reactive({
  categories: [...(props.modelValue.categories || [])],
  levels: [...(props.modelValue.levels || [])],
  price_range: props.modelValue.price_range || 'all',
  languages: [...(props.modelValue.languages || [])]
})

const activeFilterCount = computed(() => {
  let count = (localFilters.categories?.length || 0) + (localFilters.languages?.length || 0)
  if (localFilters.price_range && localFilters.price_range !== 'all') count += 1
  return count
})

watch(
  () => props.modelValue,
  (newVal) => {
    localFilters.categories = [...(newVal.categories || [])]
    localFilters.levels = [...(newVal.levels || [])]
    localFilters.price_range = newVal.price_range || 'all'
    localFilters.languages = [...(newVal.languages || [])]
  },
  { deep: true }
)

function emitUpdate() {
  const payload = {
    categories: [...localFilters.categories],
    levels: [...localFilters.levels],
    price_range: localFilters.price_range,
    languages: [...localFilters.languages]
  }
  emit('update:modelValue', payload)
  emit('change', payload)
}
</script>
