<!-- Lucian UX/UI Prompt #267 · MIT License (c) 2026 Seokwoooo · https://lucianlabs.dev/uxui-prompt/#267 -->
<template>
  <div ref="wrapperRef" class="ux u267-wrapper" :class="{ 'is-open': isOpen }">
    <!-- Globe trigger button -->
    <button
      ref="triggerRef"
      type="button"
      class="u267-gb"
      :aria-label="locale === 'kh' ? 'KH - ជ្រើសរើសភាសា' : 'EN - Choose language'"
      aria-haspopup="listbox"
      :aria-expanded="isOpen"
      @click="toggleDropdown"
      @keydown.down.prevent="openDropdown"
      @keydown.esc.prevent="closeDropdown"
    >
      <Globe2 class="w-4 h-4 shrink-0 text-slate-500 dark:text-slate-400" aria-hidden="true" />
      <span class="u267-sw" :class="animClass" :style="animStyle">
        <span>{{ locale.toUpperCase() }}</span>
      </span>
    </button>

    <!-- Language options dropdown -->
    <div
      class="u267-dd"
      role="listbox"
      :aria-label="locale === 'kh' ? 'ជ្រើសរើសភាសា' : 'Choose language'"
      @keydown.esc.prevent="closeDropdown"
    >
      <button
        v-for="language in languages"
        :key="language.value"
        type="button"
        role="option"
        :aria-selected="locale === language.value"
        class="u267-op"
        :class="{ 'is-on': locale === language.value }"
        @click="selectLanguage(language.value)"
      >
        <span class="font-bold">{{ language.label }}</span>
        <em>{{ language.sublabel }}</em>
        <Check class="shrink-0" aria-hidden="true" />
      </button>
    </div>
  </div>
</template>

<script setup>
import { nextTick, onMounted, onUnmounted, ref } from 'vue'
import { Check, Globe2 } from 'lucide-vue-next'

const props = defineProps({
  locale: {
    type: String,
    required: true,
  },
  animClass: {
    type: String,
    default: '',
  },
  animStyle: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['select', 'close'])

const isOpen = ref(false)
const wrapperRef = ref(null)
const triggerRef = ref(null)

const languages = [
  { value: 'en', label: 'EN', sublabel: 'English' },
  { value: 'kh', label: 'KH', sublabel: 'ភាសាខ្មែរ' },
]

function toggleDropdown() {
  isOpen.value = !isOpen.value
}

async function openDropdown() {
  isOpen.value = true
  await nextTick()
  wrapperRef.value?.querySelector('[role="option"][aria-selected="true"]')?.focus()
}

function closeDropdown() {
  if (isOpen.value) {
    isOpen.value = false
    triggerRef.value?.focus()
    emit('close')
  }
}

function selectLanguage(val) {
  isOpen.value = false
  emit('select', val)
}

function handleOutsideClick(event) {
  if (isOpen.value && !wrapperRef.value?.contains(event.target)) {
    isOpen.value = false
    emit('close')
  }
}

function handleKeydown(event) {
  if (event.key === 'Escape' && isOpen.value) {
    closeDropdown()
  }
}

onMounted(() => {
  document.addEventListener('click', handleOutsideClick)
  document.addEventListener('keydown', handleKeydown)
})

onUnmounted(() => {
  document.removeEventListener('click', handleOutsideClick)
  document.removeEventListener('keydown', handleKeydown)
})

defineExpose({
  closeDropdown,
  openDropdown,
})
</script>

<style scoped>
/* Theme variable mapping for prompt #267 */
:root {
  color-scheme: light;
  --ux-page: #F4F2EE;
  --ux-surface: #FFFFFF;
  --ux-surface-2: #F8FAFC;
  --ux-surface-3: #F1F5F9;
  --ux-ink: #0F172A;
  --ux-ink-2: #475569;
  --ux-ink-3: #8E8A97;
  --ux-line: rgba(15, 23, 42, 0.08);
  --ux-line-2: rgba(15, 23, 42, 0.16);
  --ux-accent: #2563EB;
  --ux-accent-2: #2F8FE0;
  --ux-accent-soft: rgba(37, 99, 235, 0.12);
  --ux-accent-ink: #FFFFFF;
  --ux-mint: #119C72;
  --ux-warn: #D6731E;
  --ux-danger: #D93A55;
  --ux-shadow: rgba(15, 23, 42, 0.08);
  --ux-shadow-strong: rgba(15, 23, 42, 0.2);
  --ux-ease: cubic-bezier(.2, .8, .2, 1);
  --ux-spring: cubic-bezier(.34, 1.45, .64, 1);
}

:root[data-theme="dark"], :global(.dark) {
  color-scheme: dark;
  --ux-page: #0B0F19;
  --ux-surface: #1E293B;
  --ux-surface-2: #0F172A;
  --ux-surface-3: #334155;
  --ux-ink: #F8FAFC;
  --ux-ink-2: rgba(248, 250, 252, 0.7);
  --ux-ink-3: rgba(248, 250, 252, 0.45);
  --ux-line: rgba(255, 255, 255, 0.09);
  --ux-line-2: rgba(255, 255, 255, 0.18);
  --ux-accent: #60A5FA;
  --ux-accent-2: #7DB4FF;
  --ux-accent-soft: rgba(96, 165, 250, 0.15);
  --ux-accent-ink: #0B0C12;
  --ux-shadow: rgba(0, 0, 0, 0.45);
  --ux-shadow-strong: rgba(0, 0, 0, 0.72);
}

.ux {
  color: var(--ux-ink);
  -webkit-font-smoothing: antialiased;
  letter-spacing: -.01em;
  -webkit-tap-highlight-color: transparent;
  word-break: keep-all;
  overflow-wrap: break-word;
}

.u267-wrapper {
  position: relative;
  display: inline-flex;
  align-items: center;
}

.u267-gb {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  height: 34px;
  padding: 0 10px;
  border: 1px solid var(--ux-line);
  border-radius: 10px;
  background: var(--ux-surface-2);
  color: var(--ux-ink);
  font: inherit;
  font-size: 12px;
  font-weight: 750;
  cursor: pointer;
  transition: background .15s, border-color .15s, box-shadow .15s;
}

.u267-gb:hover {
  background: var(--ux-surface-3);
}

.u267-gb:focus-visible,
.u267-op:focus-visible {
  outline: 2px solid var(--ux-accent);
  outline-offset: 2px;
}

.u267-dd {
  position: absolute;
  right: 0;
  top: calc(100% + 8px);
  width: 156px;
  padding: 5px;
  border-radius: 14px;
  background: var(--ux-surface);
  box-shadow: 0 0 0 1px var(--ux-line), 0 16px 34px -14px var(--ux-shadow-strong);
  transform-origin: 90% 0;
  transform: scale(.9) translateY(-4px);
  opacity: 0;
  pointer-events: none;
  transition: transform .25s cubic-bezier(.3, 1.5, .5, 1), opacity .15s;
  z-index: 60;
}

.u267-wrapper.is-open .u267-dd {
  transform: none;
  opacity: 1;
  pointer-events: auto;
}

.u267-op {
  display: flex;
  align-items: center;
  gap: 8px;
  width: 100%;
  height: 36px;
  padding: 0 10px;
  border: 0;
  border-radius: 9px;
  background: none;
  color: var(--ux-ink);
  font: inherit;
  font-size: 12px;
  font-weight: 750;
  cursor: pointer;
  text-align: left;
  transition: background .15s;
}

.u267-op:hover {
  background: var(--ux-surface-2);
}

.u267-op em {
  font-style: normal;
  font-size: 11px;
  font-weight: 500;
  color: var(--ux-ink-2);
  margin-left: 2px;
}

.u267-op svg {
  margin-left: auto;
  width: 14px;
  height: 14px;
  color: #16A34A;
  opacity: 0;
  transition: opacity .15s;
}

.u267-op.is-on svg {
  opacity: 1;
}

/* Stagger text switcher */
.u267-sw {
  display: inline-block;
  vertical-align: middle;
  overflow: hidden;
}

.u267-sw > span {
  display: block;
}

.u267-sw.is-go > span {
  animation: u267-out .26s ease-in forwards;
}

.u267-sw.is-in > span {
  animation: u267-in .38s cubic-bezier(.2, .9, .3, 1.2);
}

@keyframes u267-out {
  to {
    transform: translateY(-100%);
    opacity: 0;
  }
}

@keyframes u267-in {
  from {
    transform: translateY(100%);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

/* Reduced motion support */
@media (prefers-reduced-motion: reduce) {
  .u267-sw > span {
    animation: none !important;
  }
  .u267-dd {
    transition: none !important;
  }
}
</style>
