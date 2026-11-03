<!-- Lucian UX/UI Prompt #040 · MIT License (c) 2026 Seokwoooo · https://lucianlabs.dev/uxui-prompt/#040 -->
<template>
  <div class="ux u040" :class="{ 'is-wide': isWide }">
    <nav class="u040-rail" :aria-label="t('Main admin menu')">
      <!-- Top Branding & Collapse/Expand Toggle -->
      <div class="u040-top">
        <RouterLink to="/courses" class="u040-logo" :title="t('Back to courses')">
          <img src="/aerobyte-logo.png" alt="AeroByte Logo" class="w-6 h-6 object-contain brightness-0 invert" />
        </RouterLink>
        <span class="u040-name">AeroByte Admin</span>
      </div>

      <!-- Rail Toggle Button (Chevron Arrow that rotates 180° with spring curve) -->
      <button
        class="u040-tog"
        type="button"
        :aria-expanded="isWide"
        :aria-label="isWide ? t('Collapse sidebar') : t('Expand sidebar')"
        @click="toggleWide"
      >
        <svg viewBox="0 0 16 16" aria-hidden="true">
          <path d="M6 3.5L10.5 8 6 12.5" />
        </svg>
      </button>

      <!-- Navigation List with Spring Highlight -->
      <ul ref="navListRef" class="u040-nav" role="tablist">
        <!-- Floating Highlight Indicator that slides up and down -->
        <li
          class="u040-hl"
          role="presentation"
          aria-hidden="true"
          :style="{ '--y': highlightTop + 'px' }"
        ></li>

        <!-- Section Navigation Items -->
        <li
          v-for="(section, index) in sections"
          :key="section.id"
          :ref="el => { if (el) itemRefs[index] = el }"
          role="presentation"
        >
          <button
            class="u040-it"
            type="button"
            role="tab"
            :style="{ '--i': index }"
            :aria-selected="activeSection === section.id"
            :aria-current="activeSection === section.id ? 'page' : undefined"
            :title="!isWide ? t(section.title) : undefined"
            @click="onSelect(section.id, index)"
            @keydown="onKeyDown($event, index)"
          >
            <!-- Tab Icon -->
            <component :is="section.icon" aria-hidden="true" class="shrink-0" />

            <!-- Tab Name with staggered slide-in -->
            <span>{{ t(section.title) }}</span>

            <!-- Optional dynamic notification / pending badge -->
            <em
              v-if="getBadgeCount(section.id)"
              class="u040-bd"
              :aria-label="`${getBadgeCount(section.id)} ${t('items')}`"
            >
              {{ getBadgeCount(section.id) }}
            </em>
          </button>
        </li>
      </ul>

      <!-- Bottom Utilities: Language & Theme Switches -->
      <div class="u040-utils" :class="{ 'is-wide': isWide }">
        <div class="u040-util-row">
          <!-- Language Toggle -->
          <div class="u040-lang-pill" role="group" :aria-label="t('Language')">
            <button
              type="button"
              class="u040-lang-btn"
              :class="{ 'is-active': locale === 'en' }"
              @click="$emit('update:locale', 'en')"
            >
              EN
            </button>
            <button
              type="button"
              class="u040-lang-btn font-khmer"
              :class="{ 'is-active': locale === 'kh' }"
              @click="$emit('update:locale', 'kh')"
            >
              KH
            </button>
          </div>

          <!-- Cat Theme Switch -->
          <div class="u040-theme-wrap">
            <CatThemeSwitch :compact="isWide" :head-only="!isWide" />
          </div>
        </div>

        <!-- Explore Public Site Link -->
        <RouterLink
          to="/courses"
          class="u040-link-btn"
          :title="!isWide ? t('Explore Courses') : undefined"
        >
          <ExternalLink class="w-4 h-4 shrink-0" aria-hidden="true" />
          <span v-if="isWide">{{ t('Explore Courses') }}</span>
        </RouterLink>
      </div>

      <!-- Admin Identity & Sign Out Card -->
      <div class="u040-me" :title="adminEmail || 'Administrator'">
        <i aria-hidden="true">{{ (adminEmail || 'Admin').charAt(0).toUpperCase() }}</i>
        <div class="u040-me-info">
          <span>{{ adminEmail ? adminEmail.split('@')[0] : 'Administrator' }}</span>
          <small>{{ t('Admin Session') }}</small>
        </div>
        <button
          type="button"
          class="u040-logout-btn"
          :title="t('Sign out')"
          :aria-label="t('Sign out')"
          :disabled="busy"
          @click="$emit('signout')"
        >
          <LogOut class="w-4 h-4" aria-hidden="true" />
        </button>
      </div>
    </nav>
  </div>
</template>

<script setup>
import { nextTick, onMounted, ref, watch } from 'vue'
import { ExternalLink, LogOut } from 'lucide-vue-next'
import CatThemeSwitch from '../common/CatThemeSwitch.vue'
import { useLanguage } from '../../i18n'

const props = defineProps({
  sections: {
    type: Array,
    required: true,
  },
  activeSection: {
    type: String,
    required: true,
  },
  isWide: {
    type: Boolean,
    default: true,
  },
  locale: {
    type: String,
    default: 'en',
  },
  isDark: {
    type: Boolean,
    default: false,
  },
  adminEmail: {
    type: String,
    default: '',
  },
  busy: {
    type: Boolean,
    default: false,
  },
  badgeCounts: {
    type: Object,
    default: () => ({}),
  },
})

const emit = defineEmits(['update:isWide', 'select', 'update:locale', 'signout'])

const { t } = useLanguage()

const navListRef = ref(null)
const itemRefs = ref([])
const highlightTop = ref(0)

function getBadgeCount(sectionId) {
  return props.badgeCounts[sectionId] || null
}

function updateHighlight() {
  nextTick(() => {
    const idx = props.sections.findIndex(s => s.id === props.activeSection)
    if (idx !== -1 && itemRefs.value[idx]) {
      const el = itemRefs.value[idx]
      highlightTop.value = el.offsetTop
    }
  })
}

function toggleWide() {
  emit('update:isWide', !props.isWide)
  setTimeout(updateHighlight, 350)
}

function onSelect(sectionId, index) {
  emit('select', sectionId)
  if (itemRefs.value[index]) {
    highlightTop.value = itemRefs.value[index].offsetTop
  }
}

function onKeyDown(event, currentIndex) {
  const d = event.key === 'ArrowDown' ? 1 : event.key === 'ArrowUp' ? -1 : 0
  if (d) {
    event.preventDefault()
    const nextIndex = (currentIndex + d + props.sections.length) % props.sections.length
    const nextSection = props.sections[nextIndex]
    if (nextSection) {
      onSelect(nextSection.id, nextIndex)
      const nextBtn = itemRefs.value[nextIndex]?.querySelector('button') || itemRefs.value[nextIndex]
      nextBtn?.focus()
    }
  }
}

watch(() => props.activeSection, () => {
  updateHighlight()
})

watch(() => props.isWide, () => {
  setTimeout(updateHighlight, 300)
})

onMounted(() => {
  updateHighlight()
  window.addEventListener('resize', updateHighlight)
})
</script>

<style scoped>
/* lucianLabs UI 요소 — 공통 테마 토큰 (라이트 / 다크)
   라이트 기본값 → 시스템이 다크면 다크 → data-theme으로 명시하면 그 값을 우선합니다.
   요소 CSS는 --ux-* 토큰만 참조하므로, 프로젝트 테마 변수에 이 값을 매핑하면 됩니다. */
.ux {
  color-scheme: light;
  --ux-page: #f8fafc;
  --ux-surface: #ffffff;
  --ux-surface-2: #f1f5f9;
  --ux-surface-3: #e2e8f0;
  --ux-ink: #0f172a;
  --ux-ink-2: #475569;
  --ux-ink-3: #94a3b8;
  --ux-line: rgba(15, 23, 42, 0.08);
  --ux-line-2: rgba(15, 23, 42, 0.16);
  --ux-accent: #0284c7;
  --ux-accent-2: #2563eb;
  --ux-accent-soft: rgba(2, 132, 199, 0.12);
  --ux-accent-ink: #ffffff;
  --ux-mint: #10b981;
  --ux-warn: #f59e0b;
  --ux-danger: #ef4444;
  --ux-glass: rgba(255, 255, 255, 0.58);
  --ux-glass-line: rgba(255, 255, 255, 0.85);
  --ux-shadow: rgba(15, 23, 42, 0.12);
  --ux-shadow-strong: rgba(15, 23, 42, 0.28);
  --ux-grad: linear-gradient(120deg, #38bdf8, #2563eb 55%, #10b981);
  --ux-ease: cubic-bezier(0.2, 0.8, 0.2, 1);
  --ux-spring: cubic-bezier(0.34, 1.45, 0.64, 1);
}

:global(html.dark) .ux,
.ux[data-theme="dark"] {
  color-scheme: dark;
  --ux-page: #020617;
  --ux-surface: #0f172a;
  --ux-surface-2: #1e293b;
  --ux-surface-3: #334155;
  --ux-ink: #f8fafc;
  --ux-ink-2: rgba(248, 250, 252, 0.7);
  --ux-ink-3: rgba(248, 250, 252, 0.45);
  --ux-line: rgba(255, 255, 255, 0.08);
  --ux-line-2: rgba(255, 255, 255, 0.16);
  --ux-accent: #38bdf8;
  --ux-accent-2: #60a5fa;
  --ux-accent-soft: rgba(56, 189, 248, 0.15);
  --ux-accent-ink: #020617;
  --ux-mint: #34d399;
  --ux-warn: #fbbf24;
  --ux-danger: #f87171;
  --ux-glass: rgba(255, 255, 255, 0.06);
  --ux-glass-line: rgba(255, 255, 255, 0.16);
  --ux-shadow: rgba(0, 0, 0, 0.45);
  --ux-shadow-strong: rgba(0, 0, 0, 0.72);
  --ux-grad: linear-gradient(120deg, #38bdf8, #3b82f6 55%, #34d399);
}

/* 요소 공통 베이스 — 루트에 .ux 클래스를 붙입니다 */
.ux, .ux *, .ux *::before, .ux *::after {
  box-sizing: border-box;
}

.ux {
  font-family: inherit;
  color: var(--ux-ink);
  -webkit-font-smoothing: antialiased;
  letter-spacing: -0.01em;
  -webkit-tap-highlight-color: transparent;
  word-break: keep-all;
  overflow-wrap: break-word;
}

:where(.ux) button {
  font: inherit;
  color: inherit;
  cursor: pointer;
}

.ux :focus-visible {
  outline: 2px solid var(--ux-accent);
  outline-offset: 3px;
}

/* 모션 줄이기: 전환은 즉시 끝나고, 무한 반복은 한 번으로 줄여 최종 상태가 보이게 합니다 */
@media (prefers-reduced-motion: reduce) {
  .ux, .ux *, .ux *::before, .ux *::after {
    animation-duration: 0.001ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.001ms !important;
    scroll-behavior: auto !important;
  }
}

/* Lucian UX/UI Prompt #040 Styles */
.u040 {
  --rw: 76px;
  position: relative;
  display: flex;
  height: 100%;
  padding: 10px 0 10px 10px;
  box-sizing: border-box;
}

.u040.is-wide {
  --rw: 228px;
}

.u040-rail {
  position: relative;
  flex: none;
  width: var(--rw);
  padding: 12px 10px;
  border-radius: 24px;
  background: var(--ux-ink);
  color: var(--ux-page);
  overflow: hidden;
  transition: width 0.6s var(--ux-spring);
  display: flex;
  flex-direction: column;
  box-shadow: 0 10px 30px -10px var(--ux-shadow-strong);
}

.u040-top {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 44px;
  margin-bottom: 12px;
  flex-shrink: 0;
}

.u040-logo {
  width: 36px;
  height: 36px;
  flex: none;
  margin-left: 10px;
  border-radius: 12px;
  background: var(--ux-grad);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: transform 0.2s ease;
}

.u040-logo:hover {
  transform: scale(1.05);
}

.u040-name {
  font-size: 15px;
  font-weight: 780;
  letter-spacing: -0.03em;
  white-space: nowrap;
  opacity: 0;
  transition: opacity 0.25s;
}

.u040.is-wide .u040-name {
  opacity: 1;
  transition: opacity 0.3s 0.15s;
}

.u040-tog {
  position: absolute;
  right: -1px;
  top: 16px;
  width: 30px;
  height: 36px;
  border: 0;
  padding: 0;
  border-radius: 10px 0 0 10px;
  background: color-mix(in srgb, var(--ux-page) 14%, transparent);
  color: inherit;
  display: grid;
  place-items: center;
  opacity: 0;
  transition: opacity 0.2s;
  cursor: pointer;
  z-index: 20;
}

.u040-rail:hover .u040-tog,
.u040-tog:focus-visible,
.u040.is-wide .u040-tog {
  opacity: 1;
}

@media (hover: none) {
  .u040-tog {
    opacity: 1;
  }
}

.u040-tog:focus-visible {
  outline: 2px solid var(--ux-accent);
  outline-offset: -2px;
}

.u040-tog svg {
  width: 16px;
  height: 16px;
  fill: none;
  stroke: currentColor;
  stroke-width: 2.4;
  stroke-linecap: round;
  stroke-linejoin: round;
  transition: transform 0.5s var(--ux-spring);
}

.u040.is-wide .u040-tog svg {
  transform: rotate(180deg);
}

.u040-nav {
  position: relative;
  margin: 0;
  padding: 0;
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 4px;
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  scrollbar-width: none;
}

.u040-nav::-webkit-scrollbar {
  display: none;
}

.u040-hl {
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  height: 48px;
  border-radius: 15px;
  background: color-mix(in srgb, var(--ux-page) 15%, transparent);
  transform: translateY(var(--y, 0));
  transition: transform 0.5s var(--ux-spring);
  pointer-events: none;
  z-index: 0;
}

.u040-hl::before {
  content: "";
  position: absolute;
  left: -10px;
  top: 12px;
  bottom: 12px;
  width: 4px;
  border-radius: 0 4px 4px 0;
  background: var(--ux-grad);
}

.u040-it {
  position: relative;
  display: flex;
  align-items: center;
  gap: 14px;
  width: 100%;
  height: 48px;
  padding: 0 0 0 16px;
  border: 0;
  border-radius: 15px;
  background: none;
  color: inherit;
  opacity: 0.62;
  text-align: left;
  transition: opacity 0.25s;
  cursor: pointer;
  z-index: 1;
}

.u040-it:hover,
.u040-it[aria-current="page"] {
  opacity: 1;
}

.u040-it:focus-visible {
  outline: 2px solid var(--ux-accent);
  outline-offset: -2px;
}

.u040-it svg {
  width: 22px;
  height: 22px;
  flex: none;
  stroke: currentColor;
  stroke-width: 1.9;
  stroke-linecap: round;
  stroke-linejoin: round;
}

.u040-it span {
  font-size: 13.5px;
  font-weight: 650;
  white-space: nowrap;
  opacity: 0;
  transform: translateX(-8px);
  transition: opacity 0.2s, transform 0.35s var(--ux-ease);
}

.u040.is-wide .u040-it span {
  opacity: 1;
  transform: none;
  transition: opacity 0.3s var(--ux-ease), transform 0.5s var(--ux-spring);
  transition-delay: calc(0.12s + var(--i) * 35ms);
}

.u040-bd {
  position: absolute;
  left: 34px;
  top: 9px;
  min-width: 17px;
  height: 17px;
  padding: 0 4px;
  border-radius: 9px;
  background: #ff5a6e;
  color: #fff;
  font-size: 10.5px;
  font-weight: 800;
  display: grid;
  place-items: center;
  font-style: normal;
  box-shadow: 0 0 0 2.5px var(--ux-ink);
  transition: left 0.5s var(--ux-spring);
}

.u040.is-wide .u040-bd {
  left: 190px;
}

/* Utilities (Language, Theme, External Link) */
.u040-utils {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px solid color-mix(in srgb, var(--ux-page) 10%, transparent);
  flex-shrink: 0;
}

.u040-util-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.u040-lang-pill {
  display: inline-flex;
  align-items: center;
  padding: 2px;
  border-radius: 10px;
  background: color-mix(in srgb, var(--ux-page) 10%, transparent);
}

.u040-lang-btn {
  padding: 3px 7px;
  font-size: 10.5px;
  font-weight: 800;
  border-radius: 8px;
  border: none;
  background: transparent;
  color: color-mix(in srgb, var(--ux-page) 60%, transparent);
  transition: all 0.2s ease;
}

.u040-lang-btn.is-active {
  background: color-mix(in srgb, var(--ux-page) 20%, transparent);
  color: var(--ux-page);
}

.u040-theme-wrap {
  display: flex;
  align-items: center;
  justify-content: center;
}

.u040-link-btn {
  display: flex;
  align-items: center;
  gap: 10px;
  height: 36px;
  padding: 0 12px;
  border-radius: 12px;
  color: color-mix(in srgb, var(--ux-page) 70%, transparent);
  text-decoration: none;
  font-size: 12px;
  font-weight: 650;
  transition: all 0.2s ease;
}

.u040-link-btn:hover {
  background: color-mix(in srgb, var(--ux-page) 10%, transparent);
  color: var(--ux-page);
}

/* User Card at Bottom */
.u040-me {
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
  height: 52px;
  padding: 0 10px;
  border-radius: 16px;
  background: color-mix(in srgb, var(--ux-page) 8%, transparent);
  margin-top: 8px;
  flex-shrink: 0;
}

.u040-me i {
  width: 34px;
  height: 34px;
  flex: none;
  border-radius: 50%;
  background: radial-gradient(circle at 35% 30%, #ffd3a8, #ff7a93 60%, #8b6cff);
  display: grid;
  place-items: center;
  font-style: normal;
  font-weight: 800;
  font-size: 13px;
  color: #fff;
}

.u040-me-info {
  flex: 1;
  min-width: 0;
  overflow: hidden;
}

.u040-me-info span {
  display: block;
  font-size: 12.5px;
  font-weight: 700;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  opacity: 0;
  transition: opacity 0.25s;
}

.u040-me-info small {
  display: block;
  font-size: 10.5px;
  opacity: 0.6;
  white-space: nowrap;
}

.u040.is-wide .u040-me-info span {
  opacity: 1;
  transition-delay: 0.25s;
}

.u040-logout-btn {
  display: none;
  width: 28px;
  height: 28px;
  border-radius: 8px;
  border: none;
  background: color-mix(in srgb, var(--ux-page) 10%, transparent);
  color: inherit;
  place-items: center;
  transition: background 0.2s ease;
  flex-shrink: 0;
}

.u040.is-wide .u040-logout-btn {
  display: grid;
}

.u040-logout-btn:hover {
  background: #ff5a6e;
  color: #fff;
}
</style>
