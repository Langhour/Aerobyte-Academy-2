<template>
  <div
    v-if="totalItems > 0 || totalPages > 1"
    :class="center ? 'flex justify-center py-2' : 'flex flex-col sm:flex-row items-center justify-between gap-3 px-1 py-2'"
  >
    <!-- Left: Quiet record count (omitted when center=true) -->
    <div
      v-if="!center && totalItems"
      class="text-xs text-slate-500 dark:text-slate-400 font-medium select-none"
    >
      {{ t('Showing') }}
      <span class="font-bold text-slate-800 dark:text-slate-200">{{ itemRangeStart }}-{{ itemRangeEnd }}</span>
      {{ t('of') }}
      <span class="font-bold text-slate-800 dark:text-slate-200">{{ totalItems }}</span>
      {{ t('records') }}
    </div>
    <div
      v-else-if="!center"
      class="text-xs text-slate-500 dark:text-slate-400 font-medium select-none"
    >
      {{ t('Page') }} {{ currentPage }} {{ t('of') }} {{ totalPages }}
    </div>

    <!-- Capsule Pill Bar matching reference design -->
    <nav
      class="inline-flex items-center gap-1 sm:gap-1.5 rounded-full border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs px-2.5 sm:px-3 py-1 text-xs select-none shrink-0"
      :aria-label="t('Pagination')"
    >
      <!-- Previous Button -->
      <button
        type="button"
        :disabled="currentPage <= 1"
        :title="t('Previous page')"
        :aria-label="t('Previous page')"
        @click="goToPage(currentPage - 1)"
        class="w-7 h-7 rounded-full flex items-center justify-center text-slate-500 hover:text-navy-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-20 disabled:pointer-events-none transition cursor-pointer shrink-0"
      >
        <ChevronLeft class="w-4 h-4" />
      </button>

      <!-- Page Numbers -->
      <div class="flex items-center gap-1 shrink-0">
        <template v-for="(item, idx) in visiblePages" :key="idx">
          <span
            v-if="item === '...'"
            class="w-5 h-7 flex items-center justify-center text-slate-400 dark:text-slate-500 font-bold select-none text-xs shrink-0"
          >
            &hellip;
          </span>
          <button
            v-else
            type="button"
            :aria-current="item === currentPage ? 'page' : undefined"
            @click="goToPage(item)"
            class="w-7 h-7 rounded-full flex items-center justify-center text-xs transition cursor-pointer shrink-0 select-none"
            :class="
              item === currentPage
                ? 'bg-navy-900 dark:bg-sky-500 text-white font-bold ring-2 ring-navy-900 dark:ring-sky-400 ring-offset-2 ring-offset-white dark:ring-offset-slate-900 shadow-xs'
                : 'font-semibold text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800'
            "
          >
            {{ item }}
          </button>
        </template>
      </div>

      <!-- Next Button -->
      <button
        type="button"
        :disabled="currentPage >= totalPages"
        :title="t('Next page')"
        :aria-label="t('Next page')"
        @click="goToPage(currentPage + 1)"
        class="w-7 h-7 rounded-full flex items-center justify-center text-slate-500 hover:text-navy-900 dark:text-slate-400 dark:hover:text-white hover:bg-slate-100 dark:hover:bg-slate-800 disabled:opacity-20 disabled:pointer-events-none transition cursor-pointer shrink-0"
      >
        <ChevronRight class="w-4 h-4" />
      </button>

      <!-- Vertical Divider -->
      <div class="h-4 w-px bg-slate-200 dark:bg-slate-700 mx-1 shrink-0"></div>

      <!-- Go to page input pill -->
      <div class="inline-flex items-center gap-1.5 pl-0.5 shrink-0">
        <span class="text-[11px] text-slate-500 dark:text-slate-400 font-medium whitespace-nowrap select-none">
          {{ t('Go to page') }}
        </span>
        <input
          v-model="jumpInput"
          type="number"
          min="1"
          :max="totalPages"
          placeholder=""
          class="w-10 h-6 px-1 text-center text-xs font-bold rounded-full border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 text-slate-800 dark:text-white focus:outline-none focus:border-navy-900 dark:focus:border-sky-400 focus:ring-1 focus:ring-navy-900 dark:focus:ring-sky-400 transition shrink-0 [appearance:textfield] [&::-webkit-outer-spin-button]:appearance-none [&::-webkit-inner-spin-button]:appearance-none"
          @keydown.enter.prevent="handleJump"
          @blur="handleJump"
        />
      </div>
    </nav>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { ChevronLeft, ChevronRight } from 'lucide-vue-next'
import { useLanguage } from '../../i18n'

const { t } = useLanguage()

const props = defineProps({
  currentPage: {
    type: Number,
    required: true,
    default: 1,
  },
  totalPages: {
    type: Number,
    required: true,
    default: 1,
  },
  totalItems: {
    type: Number,
    default: 0,
  },
  pageSize: {
    type: Number,
    default: 8,
  },
  center: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:currentPage', 'page-change'])

const jumpInput = ref('')

const itemRangeStart = computed(() => {
  if (!props.totalItems) return 0
  return (props.currentPage - 1) * props.pageSize + 1
})

const itemRangeEnd = computed(() => {
  return Math.min(props.currentPage * props.pageSize, props.totalItems)
})

const visiblePages = computed(() => {
  const total = props.totalPages
  const current = props.currentPage
  if (total <= 5) {
    return Array.from({ length: total }, (_, i) => i + 1)
  }

  const pages = []
  if (current <= 3) {
    pages.push(1, 2, 3, 4, '...', total)
  } else if (current >= total - 2) {
    pages.push(1, '...', total - 3, total - 2, total - 1, total)
  } else {
    pages.push(1, '...', current - 1, current, current + 1, '...', total)
  }
  return pages
})

function goToPage(page) {
  const target = Math.max(1, Math.min(page, props.totalPages))
  if (target !== props.currentPage) {
    emit('update:currentPage', target)
    emit('page-change', target)
  }
}

function handleJump() {
  if (!jumpInput.value) return
  const val = parseInt(jumpInput.value, 10)
  jumpInput.value = ''
  if (!isNaN(val) && val >= 1 && val <= props.totalPages) {
    goToPage(val)
  }
}
</script>
