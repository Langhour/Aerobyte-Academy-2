<template>
  <!-- Head Only Mode (for collapsed navigation / mini sidebar) -->
  <button
    v-if="headOnly"
    type="button"
    role="button"
    :title="isDark ? 'Theme: Dark (Click to switch)' : 'Theme: Light (Click to switch)'"
    :aria-label="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
    class="cat-head-btn group relative inline-flex items-center justify-center p-1 bg-transparent border-0 cursor-pointer select-none transition-transform duration-200 hover:scale-110 active:scale-95 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 rounded-full"
    @click="toggleTheme"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <div class="w-9 h-9 relative flex items-center justify-center transition-transform duration-200">
      <!-- Light Mode Cat Head (Grey Tabby) -->
      <svg
        v-if="!isDark"
        viewBox="0 0 100 100"
        class="w-full h-full drop-shadow-sm transition-all duration-300 group-hover:rotate-3"
      >
        <!-- Ears -->
        <polygon points="18,36 10,8 38,20" fill="#9ca3af" />
        <polygon points="19,32 14,14 34,22" fill="#d1d5db" />
        <polygon points="82,36 90,8 62,20" fill="#9ca3af" />
        <polygon points="81,32 86,14 66,22" fill="#d1d5db" />

        <!-- Body / Head Circle -->
        <circle cx="50" cy="54" r="44" fill="#9ca3af" />

        <!-- Belly / Chest patch -->
        <path d="M 18,74 Q 50,48 82,74 A 44,44 0 0,1 18,74 Z" fill="#e5e7eb" />

        <!-- Forehead Stripes (Grey Tabby) -->
        <path d="M 47,12 L 47,34 A 3,3 0 0,0 53,34 L 53,12 Z" fill="#6b7280" />
        <path d="M 33,18 L 35,32 A 3,3 0 0,0 41,31 L 39,17 Z" fill="#6b7280" />
        <path d="M 67,18 L 65,32 A 3,3 0 0,1 59,31 L 61,17 Z" fill="#6b7280" />

        <!-- Face Group (shifts eyes/face slightly on hover) -->
        <g
          class="transition-transform duration-200 ease-out"
          :transform="isHovered ? 'translate(5, -2)' : 'translate(0, 0)'"
        >
          <!-- Left Eye -->
          <circle cx="34" cy="52" r="7" fill="#1f2937" />
          <circle cx="32" cy="49" r="2.5" fill="#ffffff" />

          <!-- Right Eye -->
          <circle cx="66" cy="52" r="7" fill="#1f2937" />
          <circle cx="64" cy="49" r="2.5" fill="#ffffff" />

          <!-- Cute Cat Nose -->
          <polygon points="50,60 47,56 53,56" fill="#4b5563" />

          <!-- Cat Mouth Curves -->
          <path
            d="M 45,63 Q 50,67 50,61 Q 50,67 55,63"
            fill="none"
            stroke="#4b5563"
            stroke-width="2"
            stroke-linecap="round"
          />
        </g>
      </svg>

      <!-- Dark Mode Cat Head (Sleek Black Cat with Pink Nose) -->
      <svg
        v-else
        viewBox="0 0 100 100"
        class="w-full h-full drop-shadow-sm transition-all duration-300 group-hover:-rotate-3"
      >
        <!-- Ears -->
        <polygon points="18,36 10,8 38,20" fill="#18181b" />
        <polygon points="19,32 14,14 34,22" fill="#f43f5e" opacity="0.8" />
        <polygon points="82,36 90,8 62,20" fill="#18181b" />
        <polygon points="81,32 86,14 66,22" fill="#f43f5e" opacity="0.8" />

        <!-- Body / Head Circle -->
        <circle cx="50" cy="54" r="44" fill="#18181b" stroke="#27272a" stroke-width="1.5" />

        <!-- White Belly / Chest Patch -->
        <path d="M 22,76 Q 50,54 78,76 A 44,44 0 0,1 22,76 Z" fill="#f4f4f5" />

        <!-- Face Group (shifts eyes/face slightly on hover) -->
        <g
          class="transition-transform duration-200 ease-out"
          :transform="isHovered ? 'translate(-5, -2)' : 'translate(0, 0)'"
        >
          <!-- Left Eye (Big Shiny Black Cat Eye) -->
          <circle cx="34" cy="52" r="7" fill="#f8fafc" />
          <circle cx="35" cy="52" r="4.5" fill="#0f172a" />
          <circle cx="33" cy="50" r="2" fill="#ffffff" />

          <!-- Right Eye -->
          <circle cx="66" cy="52" r="7" fill="#f8fafc" />
          <circle cx="67" cy="52" r="4.5" fill="#0f172a" />
          <circle cx="65" cy="50" r="2" fill="#ffffff" />

          <!-- Cute Bright Pink Nose -->
          <polygon points="50,60 47,56 53,56" fill="#f43f5e" />

          <!-- White Cat Mouth Curves -->
          <path
            d="M 45,63 Q 50,67 50,61 Q 50,67 55,63"
            fill="none"
            stroke="#f4f4f5"
            stroke-width="2"
            stroke-linecap="round"
          />
        </g>
      </svg>
    </div>
  </button>

  <!-- Full Pill Switch Mode (Standard & Compact) -->
  <button
    v-else
    type="button"
    role="switch"
    :aria-checked="isDark"
    :aria-label="isDark ? 'Switch to Light Mode' : 'Switch to Dark Mode'"
    class="cat-switch-container group relative inline-flex items-center cursor-pointer select-none focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-indigo-500 focus-visible:ring-offset-2 transition-all duration-300"
    :class="[
      compact ? 'w-[68px] h-[32px] p-[2px]' : 'w-[78px] h-[36px] p-[3px]',
      isDark ? 'bg-[#18181b] border border-slate-700 shadow-inner' : 'bg-[#d1d5db] border border-slate-300 shadow-inner'
    ]"
    style="border-radius: 9999px;"
    @click="toggleTheme"
    @mouseenter="isHovered = true"
    @mouseleave="isHovered = false"
  >
    <!-- Background Track Details -->
    <div class="absolute inset-0 pointer-events-none overflow-hidden rounded-full transition-opacity duration-300">
      <!-- Dark mode tiny stars/moon hint in track background -->
      <span
        v-if="isDark"
        class="absolute left-2.5 top-1/2 -translate-y-1/2 text-[10px] text-slate-500 font-bold opacity-60 tracking-wider uppercase"
      >
        ✦
      </span>
      <!-- Light mode subtle sun/day hint in track background -->
      <span
        v-else
        class="absolute right-2.5 top-1/2 -translate-y-1/2 text-[11px] text-slate-400 font-bold opacity-70"
      >
        ☼
      </span>
    </div>

    <!-- The Animated Cat Knob -->
    <div
      class="cat-knob relative z-10 rounded-full transition-transform duration-400 ease-[cubic-bezier(0.34,1.56,0.64,1)] shrink-0"
      :class="compact ? 'w-[28px] h-[28px]' : 'w-[30px] h-[30px]'"
      :style="{
        transform: isDark
          ? `translateX(${compact ? '36px' : '42px'})`
          : 'translateX(0px)'
      }"
    >
      <!-- Light Mode Cat (Grey Tabby) -->
      <svg
        v-if="!isDark"
        viewBox="0 0 100 100"
        class="w-full h-full drop-shadow-sm transition-all duration-300"
      >
        <!-- Ears -->
        <polygon points="18,36 10,8 38,20" fill="#9ca3af" />
        <polygon points="19,32 14,14 34,22" fill="#d1d5db" />
        <polygon points="82,36 90,8 62,20" fill="#9ca3af" />
        <polygon points="81,32 86,14 66,22" fill="#d1d5db" />

        <!-- Body / Head Circle -->
        <circle cx="50" cy="54" r="44" fill="#9ca3af" />

        <!-- Belly / Chest patch -->
        <path d="M 18,74 Q 50,48 82,74 A 44,44 0 0,1 18,74 Z" fill="#e5e7eb" />

        <!-- Forehead Stripes (Grey Tabby) -->
        <path d="M 47,12 L 47,34 A 3,3 0 0,0 53,34 L 53,12 Z" fill="#6b7280" />
        <path d="M 33,18 L 35,32 A 3,3 0 0,0 41,31 L 39,17 Z" fill="#6b7280" />
        <path d="M 67,18 L 65,32 A 3,3 0 0,1 59,31 L 61,17 Z" fill="#6b7280" />

        <!-- Face Group (shifts slightly to the right on hover, exactly like the video Frame 2) -->
        <g
          class="transition-transform duration-200 ease-out"
          :transform="isHovered ? 'translate(6, 0)' : 'translate(0, 0)'"
        >
          <!-- Left Eye -->
          <circle cx="34" cy="52" r="7" fill="#1f2937" />
          <circle cx="32" cy="49" r="2.5" fill="#ffffff" />

          <!-- Right Eye -->
          <circle cx="66" cy="52" r="7" fill="#1f2937" />
          <circle cx="64" cy="49" r="2.5" fill="#ffffff" />

          <!-- Cute Cat Nose -->
          <polygon points="50,60 47,56 53,56" fill="#4b5563" />

          <!-- Cat Mouth Curves -->
          <path
            d="M 45,63 Q 50,67 50,61 Q 50,67 55,63"
            fill="none"
            stroke="#4b5563"
            stroke-width="2"
            stroke-linecap="round"
          />
        </g>
      </svg>

      <!-- Dark Mode Cat (Sleek Black Cat with Pink Nose) -->
      <svg
        v-else
        viewBox="0 0 100 100"
        class="w-full h-full drop-shadow-sm transition-all duration-300"
      >
        <!-- Ears -->
        <polygon points="18,36 10,8 38,20" fill="#18181b" />
        <polygon points="19,32 14,14 34,22" fill="#f43f5e" opacity="0.8" />
        <polygon points="82,36 90,8 62,20" fill="#18181b" />
        <polygon points="81,32 86,14 66,22" fill="#f43f5e" opacity="0.8" />

        <!-- Body / Head Circle -->
        <circle cx="50" cy="54" r="44" fill="#18181b" stroke="#27272a" stroke-width="1.5" />

        <!-- White Belly / Chest Patch -->
        <path d="M 22,76 Q 50,54 78,76 A 44,44 0 0,1 22,76 Z" fill="#f4f4f5" />

        <!-- Face Group (shifts slightly to the left on hover, looking toward light) -->
        <g
          class="transition-transform duration-200 ease-out"
          :transform="isHovered ? 'translate(-6, 0)' : 'translate(0, 0)'"
        >
          <!-- Left Eye (Big Shiny Black Cat Eye) -->
          <circle cx="34" cy="52" r="7" fill="#f8fafc" />
          <circle cx="35" cy="52" r="4.5" fill="#0f172a" />
          <circle cx="33" cy="50" r="2" fill="#ffffff" />

          <!-- Right Eye -->
          <circle cx="66" cy="52" r="7" fill="#f8fafc" />
          <circle cx="67" cy="52" r="4.5" fill="#0f172a" />
          <circle cx="65" cy="50" r="2" fill="#ffffff" />

          <!-- Cute Bright Pink Nose (from UXbyAnt video) -->
          <polygon points="50,60 47,56 53,56" fill="#f43f5e" />

          <!-- White Cat Mouth Curves -->
          <path
            d="M 45,63 Q 50,67 50,61 Q 50,67 55,63"
            fill="none"
            stroke="#f4f4f5"
            stroke-width="2"
            stroke-linecap="round"
          />
        </g>
      </svg>
    </div>
  </button>
</template>

<script setup>
import { ref } from 'vue'
import { isDark, toggleTheme } from '../../composables/useTheme'

defineProps({
  compact: {
    type: Boolean,
    default: false,
  },
  headOnly: {
    type: Boolean,
    default: false,
  },
})

const isHovered = ref(false)
</script>

<style scoped>
.cat-switch-container {
  box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.12);
}

.cat-knob {
  filter: drop-shadow(0 2px 3px rgba(0, 0, 0, 0.25));
}

.cat-switch-container:hover .cat-knob {
  filter: drop-shadow(0 3px 5px rgba(0, 0, 0, 0.35));
}
</style>
