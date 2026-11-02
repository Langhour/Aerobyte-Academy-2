<template>
  <div ref="rootRef" class="relative w-full text-left select-none">
    <button
      type="button"
      :disabled="disabled"
      @click="toggleDropdown"
      class="flex w-full items-center justify-between text-left transition cursor-pointer select-none"
      :class="[
        size === 'sm'
          ? 'px-3 py-1.5 rounded-lg text-xs min-h-[34px]'
          : 'px-3.5 py-2.5 rounded-xl text-xs sm:text-sm min-h-[42px]',
        'border bg-white dark:bg-slate-800 text-slate-900 dark:text-white shadow-2xs',
        isOpen
          ? 'border-navy-800 dark:border-indigo-500 ring-2 ring-navy-800/20 dark:ring-indigo-500/20'
          : 'border-slate-300 dark:border-slate-700 hover:border-slate-400 dark:hover:border-slate-600',
        disabled ? 'opacity-60 cursor-not-allowed' : '',
        triggerClass
      ]"
      :aria-expanded="isOpen"
      :aria-haspopup="true"
    >
      <span
        class="truncate"
        :class="selectedLabel ? 'font-medium' : 'text-slate-400 dark:text-slate-500'"
      >
        {{ selectedLabel || placeholder || 'Select...' }}
      </span>
      <ChevronDown
        class="w-4 h-4 text-slate-400 transition-transform duration-200 shrink-0 ml-2"
        :class="{ 'rotate-180 text-navy-800 dark:text-indigo-400': isOpen }"
      />
    </button>

    <div
      v-if="isOpen"
      class="absolute left-0 right-0 z-50 overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-1.5 shadow-xl space-y-1"
      :class="[
        shouldDropUp ? 'bottom-full mb-1.5' : 'top-full mt-1.5',
        menuClass
      ]"
      role="listbox"
    >
      <button
        v-for="option in normalizedOptions"
        :key="String(option.value)"
        type="button"
        @click="selectOption(option.value)"
        class="flex w-full items-center justify-between rounded-xl px-3 py-2 text-xs transition cursor-pointer text-left"
        :class="modelValue === option.value
          ? 'bg-navy-50 dark:bg-slate-700 text-navy-900 dark:text-white font-bold'
          : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/60 hover:text-navy-900 dark:hover:text-white font-medium'"
        role="option"
        :aria-selected="modelValue === option.value"
      >
        <span class="truncate">{{ option.label }}</span>
        <Check
          v-if="modelValue === option.value"
          class="w-4 h-4 text-navy-900 dark:text-white shrink-0 ml-2"
        />
      </button>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { Check, ChevronDown } from 'lucide-vue-next'

const props = defineProps({
  modelValue: {
    type: [String, Number, Boolean],
    default: '',
  },
  options: {
    type: Array,
    required: true,
  },
  placeholder: {
    type: String,
    default: '',
  },
  disabled: {
    type: Boolean,
    default: false,
  },
  size: {
    type: String,
    default: 'md',
  },
  triggerClass: {
    type: [String, Object, Array],
    default: '',
  },
  menuClass: {
    type: [String, Object, Array],
    default: '',
  },
  dropUp: {
    type: Boolean,
    default: false,
  },
})

const emit = defineEmits(['update:modelValue', 'change'])

const isOpen = ref(false)
const isAutoDropUp = ref(false)
const rootRef = ref(null)

const shouldDropUp = computed(() => {
  return props.dropUp || isAutoDropUp.value
})

const normalizedOptions = computed(() => {
  return props.options.map((opt) => {
    if (typeof opt === 'object' && opt !== null) {
      return {
        value: opt.value,
        label: opt.label !== undefined ? opt.label : String(opt.value),
      }
    }
    return {
      value: opt,
      label: String(opt),
    }
  })
})

const selectedOption = computed(() => {
  return normalizedOptions.value.find((opt) => opt.value === props.modelValue)
})

const selectedLabel = computed(() => {
  if (selectedOption.value) {
    return selectedOption.value.label
  }
  return props.modelValue !== null && props.modelValue !== undefined && props.modelValue !== ''
    ? String(props.modelValue)
    : ''
})

function toggleDropdown() {
  if (props.disabled) return
  if (!isOpen.value && rootRef.value) {
    const rect = rootRef.value.getBoundingClientRect()
    const spaceBelow = window.innerHeight - rect.bottom
    const spaceAbove = rect.top
    isAutoDropUp.value = spaceBelow < 200 && spaceAbove > spaceBelow
  }
  isOpen.value = !isOpen.value
}

function selectOption(val) {
  isOpen.value = false
  emit('update:modelValue', val)
  emit('change', val)
}

function handleClickOutside(event) {
  if (rootRef.value && !rootRef.value.contains(event.target)) {
    isOpen.value = false
  }
}

function handleKeydown(event) {
  if (event.key === 'Escape' && isOpen.value) {
    isOpen.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
  document.removeEventListener('keydown', handleKeydown)
})
</script>
