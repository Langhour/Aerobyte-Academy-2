<template>
  <div ref="containerRef" class="relative w-full">
    <!-- Hidden input for native form validation -->
    <input
      type="text"
      :value="modelValue"
      :required="required"
      class="sr-only pointer-events-none"
      tabindex="-1"
      aria-hidden="true"
    />

    <!-- Trigger Button / Field -->
    <button
      type="button"
      :disabled="disabled"
      class="w-full px-3.5 py-2.5 min-h-[42px] rounded-xl border text-xs sm:text-sm bg-white dark:bg-slate-800 flex items-center justify-between text-left transition-all duration-200 focus:outline-none cursor-pointer disabled:opacity-60 disabled:cursor-not-allowed group shadow-2xs"
      :class="[
        isOpen
          ? 'border-navy-800 dark:border-indigo-500 ring-2 ring-navy-800/20 dark:ring-indigo-500/20 shadow-md'
          : 'border-slate-300 dark:border-slate-700 hover:border-slate-400 dark:hover:border-slate-600',
        hasError ? 'border-red-400 ring-2 ring-red-400/20' : ''
      ]"
      @click="toggleCalendar"
    >
      <span :class="modelValue ? 'text-slate-900 dark:text-white font-medium' : 'text-slate-400 dark:text-slate-500'">
        {{ formattedDisplayValue || placeholder || t('Select date') }}
      </span>

      <div class="flex items-center gap-1.5 shrink-0">
        <button
          v-if="modelValue && !disabled"
          type="button"
          class="rounded-full p-0.5 text-slate-300 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-950/50 transition-colors duration-150"
          :title="t('Clear date')"
          @click.stop="clearDate"
        >
          <X class="w-3.5 h-3.5" />
        </button>
        <CalendarIcon
          class="w-4 h-4 transition-colors duration-200"
          :class="isOpen ? 'text-navy-800 dark:text-indigo-400' : 'text-slate-400 dark:text-slate-500 group-hover:text-slate-500 dark:group-hover:text-slate-300'"
        />
      </div>
    </button>

    <!-- Floating Calendar Card -->
    <Transition
      enter-active-class="transition duration-200 ease-out"
      enter-from-class="opacity-0 translate-y-1 scale-[0.98]"
      enter-to-class="opacity-100 translate-y-0 scale-100"
      leave-active-class="transition duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0 scale-100"
      leave-to-class="opacity-0 translate-y-1 scale-[0.98]"
    >
      <div
        v-if="isOpen"
        class="absolute top-full z-50 mt-2 w-[300px] max-w-[calc(100vw-2rem)] rounded-2xl border border-slate-200/80 dark:border-slate-700 bg-white dark:bg-slate-800 p-5 shadow-[0_20px_60px_-12px_rgba(0,0,0,0.15)] dark:shadow-slate-900/50"
        :class="align === 'right' ? 'right-0' : 'left-0'"
        @click.stop
      >
        <!-- Header: Navigation -->
        <div class="flex items-center justify-between mb-4">
          <!-- Prev Month Arrow -->
          <button
            type="button"
            class="w-8 h-8 flex items-center justify-center rounded-xl text-slate-400 dark:text-slate-400 hover:text-navy-800 dark:hover:text-white hover:bg-navy-50 dark:hover:bg-slate-700 transition-all duration-150 cursor-pointer"
            :title="t('Previous month')"
            @click="prevMonth"
          >
            <ChevronLeft class="w-4 h-4" />
          </button>

          <!-- Month & Year Center Display -->
          <div class="flex items-center gap-1">
            <button
              type="button"
              class="text-sm font-bold text-navy-900 dark:text-white hover:text-navy-800 dark:hover:text-indigo-300 hover:bg-navy-50 dark:hover:bg-slate-700 px-2 py-1 rounded-lg transition-all duration-150 cursor-pointer"
              @click="toggleView('month')"
            >
              {{ t(monthNames[currentMonth]) }}
            </button>
            <button
              type="button"
              class="text-sm font-bold text-navy-900 dark:text-white hover:text-navy-800 dark:hover:text-indigo-300 hover:bg-navy-50 dark:hover:bg-slate-700 px-2 py-1 rounded-lg transition-all duration-150 cursor-pointer"
              @click="toggleView('year')"
            >
              {{ currentYear }}
            </button>
          </div>

          <!-- Next Month Arrow -->
          <button
            type="button"
            class="w-8 h-8 flex items-center justify-center rounded-xl text-slate-400 dark:text-slate-400 hover:text-navy-800 dark:hover:text-white hover:bg-navy-50 dark:hover:bg-slate-700 transition-all duration-150 cursor-pointer"
            :title="t('Next month')"
            @click="nextMonth"
          >
            <ChevronRight class="w-4 h-4" />
          </button>
        </div>

        <!-- ====== MONTH SELECTOR VIEW ====== -->
        <Transition
          enter-active-class="transition duration-150 ease-out"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition duration-100 ease-in"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div v-if="activeView === 'month'" class="grid grid-cols-3 gap-2 mb-2">
            <button
              v-for="(mName, mIdx) in monthNames"
              :key="mIdx"
              type="button"
              class="py-2 px-1 rounded-xl text-xs font-semibold transition-all duration-150 cursor-pointer"
              :class="[
                mIdx === currentMonth
                  ? 'bg-navy-900 dark:bg-indigo-600 text-white shadow-sm'
                  : mIdx === today.getMonth() && currentYear === today.getFullYear()
                    ? 'text-navy-800 dark:text-indigo-400 bg-navy-50 dark:bg-slate-700 hover:bg-navy-100 dark:hover:bg-slate-600'
                    : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 hover:text-slate-900 dark:hover:text-white'
              ]"
              @click="selectMonth(mIdx)"
            >
              {{ t(mName).slice(0, 3) }}
            </button>
          </div>
        </Transition>

        <!-- ====== YEAR SELECTOR VIEW ====== -->
        <Transition
          enter-active-class="transition duration-150 ease-out"
          enter-from-class="opacity-0 scale-95"
          enter-to-class="opacity-100 scale-100"
          leave-active-class="transition duration-100 ease-in"
          leave-from-class="opacity-100 scale-100"
          leave-to-class="opacity-0 scale-95"
        >
          <div v-if="activeView === 'year'" class="mb-2">
            <div class="grid grid-cols-4 gap-1.5 max-h-[200px] overflow-y-auto pr-1 custom-scrollbar">
              <button
                v-for="y in availableYears"
                :key="y"
                :ref="el => { if (y === currentYear) yearActiveRef = el }"
                type="button"
                class="py-1.5 px-1 rounded-xl text-xs font-semibold transition-all duration-150 cursor-pointer"
                :class="[
                  y === currentYear
                    ? 'bg-navy-900 dark:bg-indigo-600 text-white shadow-sm'
                    : y === today.getFullYear()
                      ? 'text-navy-800 dark:text-indigo-400 bg-navy-50 dark:bg-slate-700 hover:bg-navy-100 dark:hover:bg-slate-600'
                      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 hover:text-slate-900 dark:hover:text-white'
                ]"
                @click="selectYear(y)"
              >
                {{ y }}
              </button>
            </div>
          </div>
        </Transition>

        <!-- ====== CALENDAR DAYS VIEW ====== -->
        <template v-if="activeView === 'days'">
          <!-- Days of Week Header -->
          <div class="grid grid-cols-7 mb-1">
            <span
              v-for="(day, idx) in weekDays"
              :key="idx"
              class="text-[11px] font-semibold text-slate-400 dark:text-slate-500 text-center py-1.5 select-none"
            >
              {{ t(day) }}
            </span>
          </div>

          <!-- Calendar Days Grid -->
          <div class="grid grid-cols-7">
            <div
              v-for="(cell, index) in calendarCells"
              :key="index"
              class="flex items-center justify-center py-[3px]"
            >
              <button
                type="button"
                :disabled="cell.disabled"
                class="relative w-9 h-9 flex items-center justify-center rounded-full text-[13px] transition-all duration-150 cursor-pointer disabled:opacity-20 disabled:cursor-not-allowed"
                :class="getDayCellClasses(cell)"
                @click="selectDate(cell)"
                @mouseenter="hoveredDate = cell.dateString"
                @mouseleave="hoveredDate = ''"
              >
                <span class="relative z-10">{{ cell.day }}</span>
                <!-- Today dot indicator -->
                <span
                  v-if="cell.isToday && !cell.isSelected"
                  class="absolute bottom-1 left-1/2 -translate-x-1/2 w-1 h-1 rounded-full bg-navy-800 dark:bg-indigo-400"
                ></span>
              </button>
            </div>
          </div>

          <!-- Footer: Clear & Today -->
          <div class="flex items-center justify-between mt-3 pt-3 border-t border-slate-100 dark:border-slate-700">
            <button
              type="button"
              class="text-xs text-slate-400 hover:text-red-500 dark:hover:text-red-400 font-medium px-3 py-1.5 rounded-lg hover:bg-red-50 dark:hover:bg-red-950/40 transition-all duration-150 cursor-pointer"
              @click="clearDate"
            >
              {{ t('Clear') }}
            </button>
            <button
              type="button"
              class="text-xs text-white bg-navy-900 dark:bg-indigo-600 hover:bg-navy-800 dark:hover:bg-indigo-700 font-semibold px-4 py-1.5 rounded-lg transition-all duration-150 cursor-pointer shadow-sm hover:shadow"
              @click="selectToday"
            >
              {{ t('Today') }}
            </button>
          </div>
        </template>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import {
  Calendar as CalendarIcon,
  ChevronLeft,
  ChevronRight,
  X,
} from 'lucide-vue-next'
import { useLanguage } from '../../i18n'

const props = defineProps({
  modelValue: {
    type: String,
    default: '',
  },
  placeholder: {
    type: String,
    default: '',
  },
  required: {
    type: Boolean,
    default: false,
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  hasError: {
    type: Boolean,
    default: false,
  },
  minYear: {
    type: Number,
    default: 1940,
  },
  maxYear: {
    type: Number,
    default: new Date().getFullYear() + 5,
  },
  align: {
    type: String,
    default: 'left',
  },
})

const emit = defineEmits(['update:modelValue', 'change'])
const { t } = useLanguage()

const containerRef = ref(null)
const yearActiveRef = ref(null)
const isOpen = ref(false)
const activeView = ref('days') // 'days' | 'month' | 'year'
const hoveredDate = ref('')

const monthNames = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
]

const weekDays = ['Su', 'Mo', 'Tu', 'We', 'Th', 'Fr', 'Sa']

const today = new Date()
const currentMonth = ref(today.getMonth())
const currentYear = ref(today.getFullYear())

// Sync current view with incoming modelValue
function syncWithModelValue() {
  if (props.modelValue && typeof props.modelValue === 'string') {
    const parts = props.modelValue.split('-')
    if (parts.length === 3) {
      const y = parseInt(parts[0], 10)
      const m = parseInt(parts[1], 10) - 1
      if (!isNaN(y) && !isNaN(m)) {
        currentYear.value = y
        currentMonth.value = m
      }
    }
  }
}

watch(() => props.modelValue, syncWithModelValue, { immediate: true })

const availableYears = computed(() => {
  const years = []
  const max = props.maxYear
  const min = props.minYear
  for (let y = max; y >= min; y--) {
    years.push(y)
  }
  return years
})

const formattedDisplayValue = computed(() => {
  if (!props.modelValue) return ''
  const parts = props.modelValue.split('-')
  if (parts.length !== 3) return props.modelValue
  const y = parseInt(parts[0], 10)
  const m = parseInt(parts[1], 10) - 1
  const d = parseInt(parts[2], 10)
  if (isNaN(y) || isNaN(m) || isNaN(d)) return props.modelValue
  return `${d < 10 ? '0' + d : d} ${t(monthNames[m]).slice(0, 3)} ${y}`
})

const calendarCells = computed(() => {
  const year = currentYear.value
  const month = currentMonth.value

  const firstDayIndex = new Date(year, month, 1).getDay()
  const daysInCurrentMonth = new Date(year, month + 1, 0).getDate()
  const daysInPrevMonth = new Date(year, month, 0).getDate()

  const cells = []

  // Fill in days from previous month
  for (let i = firstDayIndex - 1; i >= 0; i--) {
    const day = daysInPrevMonth - i
    const dateStr = formatDateString(month === 0 ? year - 1 : year, month === 0 ? 11 : month - 1, day)
    cells.push({
      day,
      dateString: dateStr,
      isCurrentMonth: false,
      isSelected: props.modelValue === dateStr,
      isToday: isTodayDate(dateStr),
      disabled: false,
    })
  }

  // Days in current month
  for (let d = 1; d <= daysInCurrentMonth; d++) {
    const dateStr = formatDateString(year, month, d)
    cells.push({
      day: d,
      dateString: dateStr,
      isCurrentMonth: true,
      isSelected: props.modelValue === dateStr,
      isToday: isTodayDate(dateStr),
      disabled: false,
    })
  }

  // Fill in trailing days from next month to complete grid (multiples of 7)
  const remaining = (7 - (cells.length % 7)) % 7
  for (let d = 1; d <= remaining; d++) {
    const dateStr = formatDateString(month === 11 ? year + 1 : year, month === 11 ? 0 : month + 1, d)
    cells.push({
      day: d,
      dateString: dateStr,
      isCurrentMonth: false,
      isSelected: props.modelValue === dateStr,
      isToday: isTodayDate(dateStr),
      disabled: false,
    })
  }

  return cells
})

function getDayCellClasses(cell) {
  if (cell.isSelected) {
    return 'bg-navy-900 dark:bg-indigo-600 text-white font-bold shadow-md'
  }
  if (cell.isToday && cell.isCurrentMonth) {
    return 'text-navy-900 dark:text-indigo-400 font-bold bg-navy-50 dark:bg-slate-700 hover:bg-navy-100 dark:hover:bg-slate-600'
  }
  if (cell.isCurrentMonth) {
    return 'text-slate-700 dark:text-slate-200 font-medium hover:bg-slate-100 dark:hover:bg-slate-700'
  }
  return 'text-slate-300 dark:text-slate-600 font-normal hover:bg-slate-50 dark:hover:bg-slate-700/50 hover:text-slate-400 dark:hover:text-slate-400'
}

function formatDateString(year, month, day) {
  const m = month + 1
  const mm = m < 10 ? `0${m}` : `${m}`
  const dd = day < 10 ? `0${day}` : `${day}`
  return `${year}-${mm}-${dd}`
}

function isTodayDate(dateString) {
  const tYear = today.getFullYear()
  const tMonth = today.getMonth() + 1
  const tDay = today.getDate()
  const mm = tMonth < 10 ? `0${tMonth}` : `${tMonth}`
  const dd = tDay < 10 ? `0${tDay}` : `${tDay}`
  return dateString === `${tYear}-${mm}-${dd}`
}

function toggleCalendar() {
  if (props.disabled) return
  if (!isOpen.value) {
    syncWithModelValue()
    activeView.value = 'days'
  }
  isOpen.value = !isOpen.value
}

function toggleView(view) {
  if (activeView.value === view) {
    activeView.value = 'days'
  } else {
    activeView.value = view
    if (view === 'year') {
      nextTick(() => {
        if (yearActiveRef.value) {
          yearActiveRef.value.scrollIntoView({ block: 'center', behavior: 'smooth' })
        }
      })
    }
  }
}

function selectMonth(mIdx) {
  currentMonth.value = mIdx
  activeView.value = 'days'
}

function selectYear(y) {
  currentYear.value = y
  activeView.value = 'days'
}

function prevMonth() {
  if (currentMonth.value === 0) {
    currentMonth.value = 11
    currentYear.value -= 1
  } else {
    currentMonth.value -= 1
  }
}

function nextMonth() {
  if (currentMonth.value === 11) {
    currentMonth.value = 0
    currentYear.value += 1
  } else {
    currentMonth.value += 1
  }
}

function selectDate(cell) {
  emit('update:modelValue', cell.dateString)
  emit('change', cell.dateString)
  isOpen.value = false
}

function selectToday() {
  const dateStr = formatDateString(today.getFullYear(), today.getMonth(), today.getDate())
  currentYear.value = today.getFullYear()
  currentMonth.value = today.getMonth()
  emit('update:modelValue', dateStr)
  emit('change', dateStr)
  isOpen.value = false
}

function clearDate() {
  emit('update:modelValue', '')
  emit('change', '')
  isOpen.value = false
}

function handleClickOutside(event) {
  if (containerRef.value && !containerRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 4px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #cbd5e1;
  border-radius: 9999px;
}
.custom-scrollbar::-webkit-scrollbar-thumb:hover {
  background: #94a3b8;
}
</style>
