<template>
  <div class="max-w-xl mx-auto px-3 sm:px-4 py-8 sm:py-14 transition-colors">
    <div class="bg-white dark:bg-slate-800 rounded-2xl sm:rounded-3xl border border-slate-200/90 dark:border-slate-700 shadow-card overflow-hidden">
      <!-- Top Red Accent Bar -->
      <div class="h-1.5 w-full bg-accent-red"></div>

      <div class="p-5 sm:p-9 text-center">
        <!-- Red Exclamation Circle -->
        <div class="w-12 h-12 rounded-full bg-red-50 dark:bg-red-950/60 text-accent-red dark:text-red-400 mx-auto flex items-center justify-center mb-4">
          <AlertTriangle class="w-7 h-7" />
        </div>

        <h1 class="text-xl font-extrabold text-navy-900 dark:text-white">
          {{ t('Payment Session Expired') }}
        </h1>
        <p class="mt-2 text-xs text-slate-500 dark:text-slate-400 max-w-sm mx-auto leading-relaxed">
          {{ t('The 15-minute checkout window has elapsed. Unpaid registrations are automatically cancelled.') }}
        </p>

        <!-- Expired Notice Details Box -->
        <div class="mt-6 bg-slate-50 dark:bg-slate-900/60 rounded-2xl border border-slate-200/80 dark:border-slate-700 p-5 text-left space-y-3 text-xs">
          <div class="flex items-center justify-between border-b border-slate-200/70 dark:border-slate-700 pb-2.5">
            <span class="text-slate-400 dark:text-slate-400 font-medium">{{ t('Enrollment ID') }}</span>
            <span class="font-bold text-navy-900 dark:text-white">{{ enrollment?.enrollment_id || route.params.enrollmentId || '--' }}</span>
          </div>
          <div class="flex items-center justify-between">
            <span class="text-slate-400 dark:text-slate-400 font-medium">{{ t('Status') }}</span>
            <span class="font-bold text-accent-red dark:text-red-400 uppercase tracking-wider text-[11px]">{{ t('Expired') }}</span>
          </div>
        </div>

        <div class="mt-8 flex flex-col sm:flex-row items-center justify-center gap-3">
          <button
            type="button"
            @click="retryEnrollment"
            class="w-full sm:w-auto px-6 py-2.5 rounded-xl bg-navy-800 dark:bg-indigo-600 hover:bg-navy-900 dark:hover:bg-indigo-700 text-xs font-bold text-white transition flex items-center justify-center gap-2 shadow-xs cursor-pointer"
          >
            <RotateCcw class="w-4 h-4" />
            <span>{{ t('Try Again') }}</span>
          </button>

          <router-link
            to="/courses"
            class="w-full sm:w-auto px-5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-600 bg-white dark:bg-slate-700 text-xs font-bold text-navy-900 dark:text-white hover:bg-slate-50 dark:hover:bg-slate-600 transition flex items-center justify-center gap-2 shadow-xs"
          >
            <span>{{ t('Browse Courses') }}</span>
            <ArrowRight class="w-4 h-4" />
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { AlertTriangle, RotateCcw, ArrowRight } from 'lucide-vue-next'
import { enrollmentService } from '../services/api'
import { useLanguage } from '../i18n'

const route = useRoute()
const router = useRouter()
const { t } = useLanguage()

const enrollment = ref(null)

async function fetchEnrollment() {
  try {
    const { data } = await enrollmentService.getEnrollment(route.params.enrollmentId)
    enrollment.value = data
  } catch (error) {
    console.error('Error fetching expired enrollment:', error)
  }
}

function retryEnrollment() {
  const target = enrollment.value?.course_slug || enrollment.value?.course_id
  if (target) {
    router.push(`/enroll/${encodeURIComponent(target)}`)
  } else {
    router.push('/courses')
  }
}

onMounted(() => {
  fetchEnrollment()
})
</script>
