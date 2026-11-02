<template>
  <nav
    v-if="totalPages >= 1"
    class="mt-12 flex items-center justify-center gap-1.5"
    :aria-label="t('Pagination')"
  >
    <!-- Previous Button -->
    <button
      type="button"
      :disabled="currentPage <= 1"
      @click="$emit('page-change', currentPage - 1)"
      class="w-8 h-8 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 flex items-center justify-center text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-40 disabled:pointer-events-none transition"
    >
      <ChevronLeft class="w-4 h-4" :aria-label="t('Previous page')" />
    </button>

    <!-- Page Numbers -->
    <button
      v-for="page in displayPages"
      :key="page"
      type="button"
      @click="$emit('page-change', page)"
      class="w-8 h-8 rounded-lg text-xs font-bold transition flex items-center justify-center"
      :class="
        page === currentPage
          ? 'bg-navy-800 dark:bg-indigo-600 text-white shadow-xs'
          : 'border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700'
      "
    >
      {{ page }}
    </button>

    <!-- Next Button -->
    <button
      type="button"
      :disabled="currentPage >= totalPages"
      @click="$emit('page-change', currentPage + 1)"
      class="w-8 h-8 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 flex items-center justify-center text-slate-500 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-700 disabled:opacity-40 disabled:pointer-events-none transition"
    >
      <ChevronRight class="w-4 h-4" :aria-label="t('Next page')" />
    </button>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { useLanguage } from '../../i18n'

const { t } = useLanguage()

const props = defineProps({
  currentPage: {
    type: Number,
    default: 1
  },
  totalPages: {
    type: Number,
    default: 1
  }
})

defineEmits(['page-change'])

const displayPages = computed(() => {
  const pages = []
  const maxButtons = 5
  let start = Math.max(1, props.currentPage - Math.floor(maxButtons / 2))
  let end = start + maxButtons - 1

  if (end > props.totalPages) {
    end = props.totalPages
    start = Math.max(1, end - maxButtons + 1)
  }

  for (let i = start; i <= end; i++) {
    pages.push(i)
  }
  return pages
})
</script>
