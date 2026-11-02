<template>
  <div class="max-w-xl mx-auto px-3 sm:px-4 py-6 sm:py-14 transition-colors">
    <div class="bg-white dark:bg-slate-800 rounded-2xl sm:rounded-3xl border border-slate-200/90 dark:border-slate-700 shadow-card overflow-hidden">
      <!-- Top Navy Accent Bar -->
      <div class="h-1.5 w-full bg-navy-800 dark:bg-indigo-600"></div>

      <div class="p-5 sm:p-9 text-center">
        <h1 class="text-lg sm:text-xl font-extrabold text-navy-900 dark:text-white">{{ t('Scan to Pay') }}</h1>
        <p class="text-xs text-slate-400 dark:text-slate-400 mt-1">
          {{ t('Scan the QR code below with your mobile banking app') }}
        </p>

        <!-- Centered Amount Due (No Expiration / Time Left) -->
        <div class="mt-4 sm:mt-6 py-4 sm:py-5 px-4 sm:px-6 rounded-2xl bg-navy-50/70 dark:bg-slate-700/60 border border-navy-100/80 dark:border-slate-600 text-center flex flex-col items-center justify-center">
          <span class="block text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-400 mb-1">
            {{ t('Amount Due') }}
          </span>
          <span class="text-3xl sm:text-4xl font-extrabold text-navy-900 dark:text-white tracking-tight">
            {{ enrollment ? `$${enrollment.amount_due.toFixed(2)}` : '--' }}
          </span>
        </div>

        <!-- Fee Details Breakdown -->
        <div v-if="enrollment" class="mt-3.5 rounded-xl bg-slate-50/80 dark:bg-slate-900/60 border border-slate-200/70 dark:border-slate-700 p-3.5 text-left text-xs space-y-1.5">
          <div class="flex justify-between text-slate-500 dark:text-slate-400">
            <span>{{ t('Base price') }}</span>
            <span class="font-semibold text-slate-700 dark:text-slate-200">${{ (enrollment.base_price ?? Math.max(0, enrollment.amount_due - 15)).toFixed(2) }}</span>
          </div>
          <div class="flex justify-between text-slate-500 dark:text-slate-400">
            <span>{{ t('Administration fee') }}</span>
            <span class="font-semibold text-slate-700 dark:text-slate-200">${{ (enrollment.administration_fee ?? 7.5).toFixed(2) }}</span>
          </div>
          <div class="flex justify-between text-slate-500 dark:text-slate-400">
            <span>{{ t('Certification fee') }}</span>
            <span class="font-semibold text-slate-700 dark:text-slate-200">${{ (enrollment.certification_fee ?? 5.0).toFixed(2) }}</span>
          </div>
          <div class="flex justify-between text-slate-500 dark:text-slate-400">
            <span>{{ t('Card fee') }}</span>
            <span class="font-semibold text-slate-700 dark:text-slate-200">${{ (enrollment.card_fee ?? 2.5).toFixed(2) }}</span>
          </div>
        </div>

        <!-- Clean Real ABA QR Code (No Outer Frame) -->
        <div class="my-5 sm:my-6 mx-auto flex flex-col items-center justify-center">
          <div class="p-2.5 sm:p-3 bg-white rounded-2xl shadow-sm border border-slate-200/80 dark:border-slate-700 inline-flex items-center justify-center">
            <img
              :src="siteSettings.merchant_qr_url || '/aba-qr.png'"
              alt="ABA KHQR Payment"
              class="w-48 h-48 sm:w-56 sm:h-56 rounded-xl object-contain"
            />
          </div>
          <div class="mt-2.5 flex flex-col items-center gap-0.5">
            <span class="text-xs font-bold text-slate-800 dark:text-slate-200 tracking-wide">
              {{ siteSettings.merchant_bank_info || 'ABA Bank: VIDHCHETRA KHEMARAK' }}
            </span>
            <span class="text-[11px] font-medium text-slate-400 dark:text-slate-500">
              {{ enrollment?.transaction_id || 'ABA KHQR' }}
            </span>
          </div>
          <!-- Mobile Friendly: Save QR to photo library -->
          <div class="mt-2.5">
            <a
              :href="siteSettings.merchant_qr_url || '/aba-qr.png'"
              download="aerobyte-aba-qr.png"
              class="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-700 hover:bg-slate-100 dark:hover:bg-slate-600 text-[11px] font-semibold text-slate-700 dark:text-slate-200 transition shadow-2xs"
            >
              <Download class="w-3.5 h-3.5" />
              <span>{{ t('Save QR Image') }}</span>
            </a>
          </div>
        </div>

        <p v-if="loadError" role="alert" class="text-sm text-red-700 dark:text-red-400">
          {{ t(loadError) }}
        </p>
        <p v-if="actionError" role="alert" class="text-sm text-red-700 dark:text-red-400">
          {{ t(actionError) }}
        </p>

        <!-- Instructions -->
        <p class="text-xs text-slate-500 dark:text-slate-400 max-w-sm mx-auto leading-relaxed">
          {{ t('Scan this QR code with your mobile banking app to complete your payment.') }}
        </p>

        <!-- Admin Verification Notice (24h Confirmation) -->
        <div class="mt-7 pt-5 border-t border-slate-100 dark:border-slate-700 space-y-2.5">
          <div class="inline-flex items-center gap-2 px-3.5 py-2 rounded-xl bg-blue-50/80 dark:bg-indigo-950/40 border border-blue-100 dark:border-indigo-900/50 text-blue-900 dark:text-indigo-200 text-xs font-medium">
            <ShieldCheck class="w-4 h-4 text-blue-600 dark:text-indigo-400 shrink-0" />
            <span>{{ t('Transfer pending verification. Confirmation will arrive within 24 hours.') }}</span>
          </div>
          <p class="text-[11px] text-slate-400 dark:text-slate-500 max-w-sm mx-auto leading-normal">
            {{ t('You will receive confirmation on your registered Telegram and courses history once approved.') }}
          </p>
          <div class="pt-2">
            <RouterLink
              to="/courses"
              class="inline-flex items-center gap-1.5 text-xs font-semibold text-slate-500 hover:text-navy-900 dark:text-slate-400 dark:hover:text-white transition"
            >
              ← {{ t('Back to Courses') }}
            </RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Download, QrCode, ShieldCheck } from 'lucide-vue-next'
import { enrollmentService, siteSettingsService } from '../services/api'
import { useLanguage } from '../i18n'

const route = useRoute()
const router = useRouter()
const { t } = useLanguage()

const enrollment = ref(null)
const loadError = ref('')
const actionError = ref('')
const siteSettings = ref({
  merchant_qr_url: '',
  merchant_bank_info: '',
})
let statusPollInterval = null

async function checkEnrollmentStatus() {
  try {
    const { data } = await enrollmentService.getEnrollment(route.params.enrollmentId)
    enrollment.value = data
    if (data.status === 'paid' || data.enrollment_status === 'confirmed') {
      clearInterval(statusPollInterval)
      router.push({
        name: 'PaymentSuccessful',
        params: { enrollmentId: route.params.enrollmentId }
      })
    }
  } catch (error) {
    console.error('Status check error:', error)
  }
}

async function fetchEnrollment() {
  try {
    const { data } = await enrollmentService.getEnrollment(route.params.enrollmentId)
    enrollment.value = data
    if (data.status === 'paid' || data.enrollment_status === 'confirmed') {
      router.push({
        name: 'PaymentSuccessful',
        params: { enrollmentId: route.params.enrollmentId }
      })
      return
    }

    startPolling()
  } catch (error) {
    loadError.value = 'Failed to load enrollment details. Please try again.'
  }
}

function startPolling() {
  statusPollInterval = setInterval(checkEnrollmentStatus, 3000)
}

onMounted(async () => {
  try {
    const { data } = await siteSettingsService.getPublicSettings()
    siteSettings.value = data
  } catch (error) {
    console.error('Unable to load merchant bank settings:', error)
  }
  fetchEnrollment()
})

onUnmounted(() => {
  if (statusPollInterval) {
    clearInterval(statusPollInterval)
  }
})
</script>
