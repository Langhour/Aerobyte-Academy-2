<template>
  <div
    v-if="modelValue"
    class="fixed inset-0 z-50 flex items-center justify-center p-3 sm:p-5 bg-slate-900/80 backdrop-blur-xs transition-opacity animate-in fade-in duration-200"
    role="dialog"
    aria-modal="true"
    @click.self="cancel"
  >
    <div
      class="relative flex flex-col w-full max-w-2xl max-h-[92vh] rounded-2xl bg-white dark:bg-slate-900 shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden"
    >
      <!-- Modal Header -->
      <div class="flex items-center justify-between px-5 py-3.5 border-b border-slate-100 dark:border-slate-800 shrink-0">
        <div class="flex items-center gap-2">
          <div class="flex h-8 w-8 items-center justify-center rounded-lg bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-sky-400">
            <Crop class="h-4 w-4" />
          </div>
          <div>
            <h3 class="text-sm font-bold text-navy-900 dark:text-white">
              {{ title || t('Crop Image') }}
            </h3>
            <p class="text-[11px] text-slate-500 dark:text-slate-400">
              {{ t('Drag to reposition or resize the crop box. Use controls to zoom, rotate, or change aspect ratio.') }}
            </p>
          </div>
        </div>
        <button
          type="button"
          class="p-1.5 rounded-lg text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 transition cursor-pointer"
          @click="cancel"
          :title="t('Close')"
        >
          <X class="h-4 w-4" />
        </button>
      </div>

      <!-- Cropper Viewport -->
      <div class="relative flex-1 min-h-[300px] sm:min-h-[380px] bg-slate-950 flex items-center justify-center overflow-hidden">
        <img
          ref="imageRef"
          :src="imageSrc"
          alt="To crop"
          class="block max-w-full max-h-[55vh]"
          @load="initCropper"
        />
        <div v-if="loading" class="absolute inset-0 flex items-center justify-center bg-slate-950/60 backdrop-blur-xs text-white text-xs">
          {{ t('Loading image...') }}
        </div>
      </div>

      <!-- Controls Toolbar -->
      <div class="px-5 py-3 bg-slate-50 dark:bg-slate-900/90 border-t border-slate-200 dark:border-slate-800 flex flex-wrap items-center justify-between gap-2 shrink-0">
        <!-- Aspect Ratio Selector -->
        <div class="flex items-center gap-1 bg-white dark:bg-slate-800 p-1 rounded-xl border border-slate-200 dark:border-slate-700 shadow-2xs">
          <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400 px-2">{{ t('Ratio') }}:</span>
          <button
            v-for="preset in aspectPresets"
            :key="preset.label"
            type="button"
            class="px-2.5 py-1 text-xs font-semibold rounded-lg transition cursor-pointer"
            :class="selectedRatio === preset.value
              ? 'bg-navy-900 text-white dark:bg-indigo-600 shadow-xs'
              : 'text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700'"
            @click="setRatio(preset.value)"
          >
            {{ preset.label }}
          </button>
        </div>

        <!-- Rotate & Zoom Buttons -->
        <div class="flex items-center gap-1">
          <button
            type="button"
            class="p-2 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 transition cursor-pointer"
            :title="t('Rotate Left (-90°)')"
            @click="rotate(-90)"
          >
            <RotateCcw class="h-3.5 w-3.5" />
          </button>
          <button
            type="button"
            class="p-2 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 transition cursor-pointer"
            :title="t('Rotate Right (+90°)')"
            @click="rotate(90)"
          >
            <RotateCw class="h-3.5 w-3.5" />
          </button>
          <button
            type="button"
            class="p-2 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 transition cursor-pointer"
            :title="t('Zoom In')"
            @click="zoom(0.1)"
          >
            <ZoomIn class="h-3.5 w-3.5" />
          </button>
          <button
            type="button"
            class="p-2 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 transition cursor-pointer"
            :title="t('Zoom Out')"
            @click="zoom(-0.1)"
          >
            <ZoomOut class="h-3.5 w-3.5" />
          </button>
          <button
            type="button"
            class="px-2.5 py-1.5 rounded-lg bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 text-[11px] font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-700 transition cursor-pointer"
            :title="t('Reset')"
            @click="reset"
          >
            {{ t('Reset') }}
          </button>
        </div>
      </div>

      <!-- Modal Footer Action Buttons -->
      <div class="px-5 py-3.5 bg-white dark:bg-slate-900 border-t border-slate-100 dark:border-slate-800 flex items-center justify-between gap-3 shrink-0">
        <button
          type="button"
          class="rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2 text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 cursor-pointer"
          @click="cancel"
        >
          {{ t('Cancel') }}
        </button>

        <div class="flex items-center gap-2">
          <button
            v-if="allowOriginal"
            type="button"
            class="rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs font-semibold text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 cursor-pointer"
            @click="useOriginal"
          >
            {{ t('Use Original') }}
          </button>
          <button
            type="button"
            :disabled="applying"
            class="inline-flex items-center gap-1.5 rounded-lg bg-navy-900 dark:bg-indigo-600 px-4 py-2 text-xs font-bold text-white shadow-xs hover:bg-navy-800 dark:hover:bg-indigo-500 transition cursor-pointer disabled:opacity-50"
            @click="cropAndApply"
          >
            <Check class="h-3.5 w-3.5" />
            <span>{{ applying ? t('Cropping...') : t('Crop & Apply') }}</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, nextTick, onBeforeUnmount } from 'vue'
import Cropper from 'cropperjs'
import 'cropperjs/dist/cropper.css'
import {
  Crop,
  X,
  RotateCcw,
  RotateCw,
  ZoomIn,
  ZoomOut,
  Check,
} from 'lucide-vue-next'
import { useLanguage } from '../../i18n'

const props = defineProps({
  modelValue: {
    type: Boolean,
    default: false,
  },
  imageSrc: {
    type: String,
    required: true,
  },
  title: {
    type: String,
    default: '',
  },
  defaultRatio: {
    type: [Number, String],
    default: 16 / 9,
  },
  allowOriginal: {
    type: Boolean,
    default: true,
  },
  originalFile: {
    type: Object,
    default: null,
  },
})

const emit = defineEmits(['update:modelValue', 'crop', 'use-original', 'cancel'])

const { t } = useLanguage()

const imageRef = ref(null)
let cropper = null
const loading = ref(true)
const applying = ref(false)

const aspectPresets = [
  { label: '16:9', value: 16 / 9 },
  { label: '4:3', value: 4 / 3 },
  { label: '1:1', value: 1 },
  { label: 'Free', value: NaN },
]

const selectedRatio = ref(props.defaultRatio)

function initCropper() {
  if (!imageRef.value) return
  destroyCropper()

  loading.value = false
  cropper = new Cropper(imageRef.value, {
    aspectRatio: selectedRatio.value,
    viewMode: 1,
    dragMode: 'move',
    autoCropArea: 0.9,
    restore: false,
    guides: true,
    center: true,
    highlight: false,
    cropBoxMovable: true,
    cropBoxResizable: true,
    toggleDragModeOnDblclick: false,
  })
}

function destroyCropper() {
  if (cropper) {
    cropper.destroy()
    cropper = null
  }
}

function setRatio(ratio) {
  selectedRatio.value = ratio
  if (cropper) {
    cropper.setAspectRatio(ratio)
  }
}

function rotate(deg) {
  if (cropper) {
    cropper.rotate(deg)
  }
}

function zoom(ratio) {
  if (cropper) {
    cropper.zoom(ratio)
  }
}

function reset() {
  if (cropper) {
    cropper.reset()
    if (!Number.isNaN(selectedRatio.value)) {
      cropper.setAspectRatio(selectedRatio.value)
    }
  }
}

async function cropAndApply() {
  if (!cropper) return
  applying.value = true
  try {
    const canvas = cropper.getCroppedCanvas({
      maxWidth: 1920,
      maxHeight: 1080,
      imageSmoothingQuality: 'high',
    })

    if (!canvas) {
      throw new Error('Canvas rendering failed')
    }

    canvas.toBlob((blob) => {
      applying.value = false
      if (!blob) return
      const fileName = props.originalFile?.name ? `cropped-${props.originalFile.name.replace(/\.[^.]+$/, '')}.jpg` : 'cropped-image.jpg'
      const croppedFile = new File([blob], fileName, { type: 'image/jpeg' })
      emit('crop', croppedFile)
      emit('update:modelValue', false)
    }, 'image/jpeg', 0.92)
  } catch (err) {
    console.error('Failed to crop image:', err)
    applying.value = false
  }
}

function useOriginal() {
  if (props.originalFile) {
    emit('use-original', props.originalFile)
  }
  emit('update:modelValue', false)
}

function cancel() {
  emit('cancel')
  emit('update:modelValue', false)
}

watch(
  () => props.modelValue,
  (val) => {
    if (val) {
      selectedRatio.value = props.defaultRatio
      loading.value = true
      nextTick(() => {
        initCropper()
      })
    } else {
      destroyCropper()
    }
  },
)

watch(
  () => props.imageSrc,
  () => {
    if (props.modelValue) {
      loading.value = true
      nextTick(() => {
        initCropper()
      })
    }
  },
)

onBeforeUnmount(() => {
  destroyCropper()
})
</script>

<style>
/* Custom overrides for cropper to match sleek dark/light theme */
.cropper-view-box {
  outline: 2px solid #38bdf8;
  outline-color: rgba(56, 189, 248, 0.85);
  border-radius: 4px;
}
.cropper-line {
  background-color: #38bdf8;
}
.cropper-point {
  background-color: #0284c7;
  width: 8px;
  height: 8px;
  border-radius: 2px;
}
.cropper-point.point-se {
  width: 10px;
  height: 10px;
}
</style>
