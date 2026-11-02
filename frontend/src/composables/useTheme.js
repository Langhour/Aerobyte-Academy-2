import { ref } from 'vue'

const THEME_KEY = 'aerobyte-theme'
export const isDark = ref(false)

function applyTheme(dark) {
  isDark.value = dark
  if (typeof document !== 'undefined') {
    if (dark) {
      document.documentElement.classList.add('dark')
      document.documentElement.setAttribute('data-theme', 'dark')
    } else {
      document.documentElement.classList.remove('dark')
      document.documentElement.setAttribute('data-theme', 'light')
    }
  }
  try {
    localStorage.setItem(THEME_KEY, dark ? 'dark' : 'light')
  } catch (error) {
    console.error('Could not save theme preference:', error)
  }
}

export function initTheme() {
  let saved = null
  try {
    saved = typeof localStorage !== 'undefined' ? localStorage.getItem(THEME_KEY) : null
  } catch (error) {
    console.error('Could not read theme preference:', error)
  }

  if (saved === 'dark') {
    applyTheme(true)
  } else if (saved === 'light') {
    applyTheme(false)
  } else if (typeof window !== 'undefined' && window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    applyTheme(true)
  } else {
    applyTheme(false)
  }
}

export function toggleTheme() {
  applyTheme(!isDark.value)
}

export function setTheme(dark) {
  applyTheme(Boolean(dark))
}

export function useTheme() {
  return {
    isDark,
    toggleTheme,
    setTheme,
    initTheme,
  }
}
