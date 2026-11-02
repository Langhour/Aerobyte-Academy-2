<template>
  <div class="bg-slate-50 min-h-screen dark:bg-slate-950">
    <!-- Top Header / Hero -->
    <section class="border-b border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
      <div class="mx-auto max-w-5xl px-3 py-6 sm:px-6 sm:py-8 lg:px-8">
        <!-- Breadcrumb -->
        <nav aria-label="Breadcrumb" class="text-xs font-medium text-slate-500 dark:text-slate-400 mb-4">
          <RouterLink to="/courses" class="transition hover:text-navy-900 dark:hover:text-white">Home</RouterLink>
          <span class="mx-2 text-slate-300 dark:text-slate-600" aria-hidden="true">/</span>
          <span class="text-navy-900 dark:text-slate-200 font-semibold">{{ t('Terms of use') }}</span>
        </nav>

        <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <div class="inline-flex items-center gap-1.5 rounded-full border border-navy-100 bg-navy-50 px-3 py-1 text-xs font-bold text-navy-800 dark:border-indigo-900/60 dark:bg-indigo-950/40 dark:text-indigo-300 mb-2">
              <Scale class="h-3.5 w-3.5" aria-hidden="true" />
              <span>AeroByte Legal</span>
            </div>
            <h1 class="text-3xl font-extrabold tracking-tight text-navy-900 dark:text-white sm:text-4xl">
              {{ t('Terms of use') }}
            </h1>
            <p class="mt-2 text-xs sm:text-sm text-slate-500 dark:text-slate-400">
              {{ t('Please read these terms carefully before enrolling in our courses or using AeroByte Academy services.') }}
            </p>
          </div>

          <!-- Switcher to Privacy Policy -->
          <div class="flex items-center gap-2 bg-slate-100 dark:bg-slate-800 p-1 rounded-xl self-start sm:self-auto shrink-0">
            <span class="px-3.5 py-1.5 rounded-lg text-xs font-bold bg-white text-navy-900 shadow-xs dark:bg-slate-700 dark:text-white">
              {{ t('Terms of use') }}
            </span>
            <RouterLink
              to="/privacy"
              class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white transition"
            >
              {{ t('Privacy Policy') }}
            </RouterLink>
          </div>
        </div>

        <div class="mt-6 flex flex-wrap items-center gap-4 border-t border-slate-100 dark:border-slate-800 pt-4 text-xs text-slate-500 dark:text-slate-400">
          <span class="inline-flex items-center gap-1.5">
            <Clock class="h-3.5 w-3.5 text-slate-400" />
            <span>{{ t('Last updated') }}: October 2026</span>
          </span>
          <span class="inline-flex items-center gap-1.5">
            <ShieldCheck class="h-3.5 w-3.5 text-emerald-600" />
            <span class="text-emerald-700 dark:text-emerald-400 font-medium">{{ t('Official AeroByte Academy Agreement') }}</span>
          </span>
        </div>
      </div>
    </section>

    <!-- Main Content Container -->
    <main class="mx-auto max-w-5xl px-3 py-6 sm:px-6 sm:py-10 lg:px-8">
      <div class="grid gap-8 lg:grid-cols-[260px_minmax(0,1fr)]">
        <!-- Quick Nav Sidebar -->
        <aside class="hidden lg:block">
          <div class="sticky top-24 rounded-2xl border border-slate-200 bg-white p-4 shadow-xs dark:border-slate-800 dark:bg-slate-900">
            <p class="text-xs font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 mb-3 px-2">
              {{ t('Table of Contents') }}
            </p>
            <nav class="space-y-1 text-xs font-medium">
              <a
                v-for="item in navSections"
                :key="item.id"
                :href="`#${item.id}`"
                class="block rounded-lg px-2.5 py-2 text-slate-600 dark:text-slate-300 transition hover:bg-navy-50 hover:text-navy-900 dark:hover:bg-slate-800 dark:hover:text-white"
              >
                {{ item.title }}
              </a>
            </nav>
            <div class="mt-5 border-t border-slate-100 dark:border-slate-800 pt-4 px-2">
              <RouterLink
                to="/contact"
                class="inline-flex items-center gap-1.5 text-xs font-bold text-navy-800 dark:text-indigo-400 hover:text-navy-950 dark:hover:text-indigo-300 transition"
              >
                <HelpCircle class="h-3.5 w-3.5" />
                <span>{{ t('Questions? Contact us') }} &rarr;</span>
              </RouterLink>
            </div>
          </div>
        </aside>

        <!-- Document Body -->
        <div class="space-y-8">
          <!-- Section 1: Overview & Acceptance -->
          <section id="acceptance" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3 mb-4">
              <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                <FileText class="h-5 w-5" />
              </span>
              <h2 class="text-lg font-bold text-navy-900 dark:text-white">1. {{ t('Acceptance of Terms') }}</h2>
            </div>
            <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              <p>
                Welcome to AeroByte Academy. By creating an account, browsing our course catalog, registering for classes, or using our physical robotics maker labs in Phnom Penh, you agree to comply with and be bound by these Terms of Use.
              </p>
              <p>
                If you do not agree with any part of these terms, you must discontinue the use of our services and website immediately.
              </p>
            </div>
          </section>

          <!-- Section 2: Account Responsibilities -->
          <section id="accounts" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3 mb-4">
              <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                <ShieldCheck class="h-5 w-5" />
              </span>
              <h2 class="text-lg font-bold text-navy-900 dark:text-white">2. {{ t('Account Registration & Security') }}</h2>
            </div>
            <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              <p>
                When creating an account or enrolling in a course, you agree to:
              </p>
              <ul class="list-disc pl-5 space-y-1.5 text-slate-600 dark:text-slate-300">
                <li>Provide accurate, current, and complete personal and contact information.</li>
                <li>Maintain the confidentiality of your login credentials and password.</li>
                <li>Promptly notify AeroByte Academy of any unauthorized access or security breach.</li>
                <li>Ensure that course certificates and student credentials accurately represent the individual who completed the learning program.</li>
              </ul>
            </div>
          </section>

          <!-- Section 3: Course Enrollment & Lab Guidelines -->
          <section id="lab-safety" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3 mb-4">
              <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-amber-50 text-amber-700 dark:bg-amber-950/40 dark:text-amber-300">
                <AlertCircle class="h-5 w-5" />
              </span>
              <h2 class="text-lg font-bold text-navy-900 dark:text-white">3. {{ t('Lab Safety Guidelines & Equipment Use') }}</h2>
            </div>
            <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              <p>
                Hands-on engineering involves working directly with electrical circuits, microcontrollers, motors, actuators, and soldering stations. All enrolled students agree to:
              </p>
              <div class="rounded-xl border border-amber-200 bg-amber-50/50 p-4 space-y-2 dark:border-amber-900/60 dark:bg-amber-950/30">
                <p class="font-bold text-amber-900 dark:text-amber-200 text-xs sm:text-sm flex items-center gap-2">
                  <AlertCircle class="h-4 w-4 shrink-0 text-amber-600 dark:text-amber-400" />
                  {{ t('Maker Lab Protocol') }}
                </p>
                <ul class="list-disc pl-5 space-y-1 text-xs text-amber-950 dark:text-amber-300">
                  <li>Follow instructor safety briefings before operating soldering equipment or high-current power supplies.</li>
                  <li>Wear protective eyewear when soldering or using mechanical 3D fabrication tools.</li>
                  <li>Handle electronic hardware kits (ESP32, Arduino, sensors, and custom PCBs) with due care to prevent electrostatic discharge (ESD) damage.</li>
                </ul>
              </div>
              <p>
                AeroByte Academy reserves the right to suspend or remove any student from lab sessions if safety guidelines are willfully disregarded.
              </p>
            </div>
          </section>

          <!-- Section 4: Fees, Payments & QR Checkout -->
          <section id="payments" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3 mb-4">
              <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                <CheckCircle2 class="h-5 w-5" />
              </span>
              <h2 class="text-lg font-bold text-navy-900 dark:text-white">4. {{ t('Tuition, Fees & Payment') }}</h2>
            </div>
            <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              <p>
                Course registration is officially confirmed only upon receipt of verified payment:
              </p>
              <ul class="list-disc pl-5 space-y-1.5 text-slate-600 dark:text-slate-300">
                <li><strong>Transparent Pricing:</strong> Enrollment totals include the course tuition, itemized administration fee, physical certification fee, and student access card fee.</li>
                <li><strong>KHQR & Bakong:</strong> Real-time payments are verified via standard Cambodian banking QR codes. Payment sessions remain open for 15 minutes before expiration.</li>
                <li><strong>Promotional Coupons:</strong> Valid coupon codes must be applied before final payment checkout. Discounts cannot be retroactively claimed after payment completion.</li>
              </ul>
            </div>
          </section>

          <!-- Section 5: Refunds & Cancellations -->
          <section id="refunds" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3 mb-4">
              <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                <Scale class="h-5 w-5" />
              </span>
              <h2 class="text-lg font-bold text-navy-900 dark:text-white">5. {{ t('Refund & Transfer Policy') }}</h2>
            </div>
            <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              <p>
                We understand that schedules can shift. Our refund and transfer policy is structured as follows:
              </p>
              <div class="grid gap-3 sm:grid-cols-2">
                <div class="rounded-xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-800/60">
                  <p class="font-bold text-navy-900 dark:text-white text-xs sm:text-sm">7+ Days Before Cohort Start</p>
                  <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">100% full tuition refund or complimentary batch transfer upon written request.</p>
                </div>
                <div class="rounded-xl border border-slate-200 bg-slate-50 p-4 dark:border-slate-800 dark:bg-slate-800/60">
                  <p class="font-bold text-navy-900 dark:text-white text-xs sm:text-sm">Within 7 Days of Start</p>
                  <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">Tuition credit applied toward any future cohort within 12 calendar months.</p>
                </div>
              </div>
              <p class="text-xs text-slate-500 dark:text-slate-400">
                Once a cohort has commenced and kit hardware has been distributed, course fees become non-refundable.
              </p>
            </div>
          </section>

          <!-- Section 6: Intellectual Property -->
          <section id="ip" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3 mb-4">
              <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                <Sparkles class="h-5 w-5" />
              </span>
              <h2 class="text-lg font-bold text-navy-900 dark:text-white">6. {{ t('Intellectual Property') }}</h2>
            </div>
            <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              <p>
                All course slide decks, proprietary schematics, firmware modules, and instructional curricula provided by AeroByte Academy are copyrighted and intended solely for your personal educational use.
              </p>
              <p>
                <strong>Student Project Ownership:</strong> You retain 100% ownership of your original robot code, mechanical modifications, and unique prototypes developed during our project labs.
              </p>
            </div>
          </section>

          <!-- Contact box -->
          <section class="rounded-2xl border border-navy-100 bg-gradient-to-r from-navy-900 to-[#1e3a5f] p-6 sm:p-8 text-white shadow-card dark:border-slate-800 dark:from-slate-900 dark:to-indigo-950">
            <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h3 class="text-lg font-bold">{{ t('Have questions regarding our terms?') }}</h3>
                <p class="mt-1 text-xs sm:text-sm text-slate-300">
                  Our academic and admissions team is available to assist you.
                </p>
              </div>
              <RouterLink
                to="/contact"
                class="inline-flex items-center justify-center gap-2 rounded-xl bg-white px-5 py-2.5 text-xs font-bold text-navy-900 hover:bg-slate-100 dark:bg-indigo-600 dark:text-white dark:hover:bg-indigo-500 transition shrink-0"
              >
                <Mail class="h-4 w-4" />
                <span>{{ t('Contact Academy') }}</span>
              </RouterLink>
            </div>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { RouterLink } from 'vue-router'
import {
  AlertCircle,
  CheckCircle2,
  Clock,
  FileText,
  HelpCircle,
  Mail,
  Scale,
  ShieldCheck,
  Sparkles,
} from 'lucide-vue-next'
import { useLanguage } from '../i18n'

const { t } = useLanguage()

const navSections = [
  { id: 'acceptance', title: '1. Acceptance of Terms' },
  { id: 'accounts', title: '2. Account Security' },
  { id: 'lab-safety', title: '3. Lab Safety Rules' },
  { id: 'payments', title: '4. Tuition & Payments' },
  { id: 'refunds', title: '5. Refunds & Transfers' },
  { id: 'ip', title: '6. Intellectual Property' },
]
</script>
