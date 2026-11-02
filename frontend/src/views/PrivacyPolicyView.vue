<template>
  <div class="bg-slate-50 min-h-screen dark:bg-slate-950">
    <!-- Top Header / Hero -->
    <section class="border-b border-slate-200 bg-white dark:border-slate-800 dark:bg-slate-900">
      <div class="mx-auto max-w-5xl px-3 py-6 sm:px-6 sm:py-8 lg:px-8">
        <!-- Breadcrumb -->
        <nav aria-label="Breadcrumb" class="text-xs font-medium text-slate-500 dark:text-slate-400 mb-4">
          <RouterLink to="/courses" class="transition hover:text-navy-900 dark:hover:text-white">Home</RouterLink>
          <span class="mx-2 text-slate-300 dark:text-slate-600" aria-hidden="true">/</span>
          <span class="text-navy-900 dark:text-slate-200 font-semibold">{{ t('Privacy Policy') }}</span>
        </nav>

        <div class="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <div class="inline-flex items-center gap-1.5 rounded-full border border-emerald-100 bg-emerald-50 px-3 py-1 text-xs font-bold text-emerald-800 dark:border-emerald-900/60 dark:bg-emerald-950/40 dark:text-emerald-300 mb-2">
              <Lock class="h-3.5 w-3.5" aria-hidden="true" />
              <span>AeroByte Security</span>
            </div>
            <h1 class="text-3xl font-extrabold tracking-tight text-navy-900 dark:text-white sm:text-4xl">
              {{ t('Privacy Policy') }}
            </h1>
            <p class="mt-2 text-xs sm:text-sm text-slate-500 dark:text-slate-400">
              {{ t('Learn how AeroByte Academy collects, safeguards, and handles your personal and learning data.') }}
            </p>
          </div>

          <!-- Switcher to Terms of Use -->
          <div class="flex items-center gap-2 bg-slate-100 dark:bg-slate-800 p-1 rounded-xl self-start sm:self-auto shrink-0">
            <RouterLink
              to="/terms"
              class="px-3.5 py-1.5 rounded-lg text-xs font-semibold text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white transition"
            >
              {{ t('Terms of use') }}
            </RouterLink>
            <span class="px-3.5 py-1.5 rounded-lg text-xs font-bold bg-white text-navy-900 shadow-xs dark:bg-slate-700 dark:text-white">
              {{ t('Privacy Policy') }}
            </span>
          </div>
        </div>

        <div class="mt-6 flex flex-wrap items-center gap-4 border-t border-slate-100 dark:border-slate-800 pt-4 text-xs text-slate-500 dark:text-slate-400">
          <span class="inline-flex items-center gap-1.5">
            <Clock class="h-3.5 w-3.5 text-slate-400" />
            <span>{{ t('Last updated') }}: October 2026</span>
          </span>
          <span class="inline-flex items-center gap-1.5">
            <ShieldCheck class="h-3.5 w-3.5 text-emerald-600" />
            <span class="text-emerald-700 dark:text-emerald-400 font-medium">{{ t('We never sell your personal information') }}</span>
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
                <span>{{ t('Privacy questions?') }} &rarr;</span>
              </RouterLink>
            </div>
          </div>
        </aside>

        <!-- Document Body -->
        <div class="space-y-8">
          <!-- Section 1: Overview -->
          <section id="overview" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3 mb-4">
              <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
                <ShieldCheck class="h-5 w-5" />
              </span>
              <h2 class="text-lg font-bold text-navy-900 dark:text-white">1. {{ t('Overview & Commitment') }}</h2>
            </div>
            <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              <p>
                At AeroByte Academy, we take your trust and privacy seriously. This Privacy Policy details how we collect, use, and protect your information when you enroll in our courses, register an account, or interact with our learning platform.
              </p>
              <p>
                Our core principle is simple: we collect only the information necessary to provide an exceptional educational experience and issue authentic certifications.
              </p>
            </div>
          </section>

          <!-- Section 2: Information We Collect -->
          <section id="collection" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3 mb-4">
              <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                <FileText class="h-5 w-5" />
              </span>
              <h2 class="text-lg font-bold text-navy-900 dark:text-white">2. {{ t('Information We Collect') }}</h2>
            </div>
            <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              <p>We collect information you directly provide when registering and enrolling:</p>
              <ul class="list-disc pl-5 space-y-1.5 text-slate-600 dark:text-slate-300">
                <li><strong>Identity & Contact:</strong> Full name (used for official certificates), email address, phone number, and Telegram username (used for cohort announcements and lab coordination).</li>
                <li><strong>Academic & Experience Background:</strong> Age group, highest academic qualification, and coding experience (used by mentors to tailor lab exercises).</li>
                <li><strong>Payment Transaction Data:</strong> KHQR transaction references, payment timestamps, and receipt numbers. <em>We never store credit card numbers or banking account passwords.</em></li>
              </ul>
            </div>
          </section>

          <!-- Section 3: How We Use Data -->
          <section id="usage" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3 mb-4">
              <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                <CheckCircle2 class="h-5 w-5" />
              </span>
              <h2 class="text-lg font-bold text-navy-900 dark:text-white">3. {{ t('How We Use Your Information') }}</h2>
            </div>
            <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              <p>Your data is used strictly for academic and operational purposes:</p>
              <ul class="list-disc pl-5 space-y-1.5 text-slate-600 dark:text-slate-300">
                <li>Processing course registrations and assigning students to cohort lab batches.</li>
                <li>Sending essential transactional messages: payment receipts, lab kit pickup schedules, and password reset codes.</li>
                <li>Issuing digital and physical AeroByte Academy course completion certificates.</li>
                <li>Providing responsive technical and student support through email and Telegram.</li>
              </ul>
            </div>
          </section>

          <!-- Section 4: Data Security -->
          <section id="security" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3 mb-4">
              <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-300">
                <Lock class="h-5 w-5" />
              </span>
              <h2 class="text-lg font-bold text-navy-900 dark:text-white">4. {{ t('Data Protection & Storage') }}</h2>
            </div>
            <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              <p>
                We employ standard industry security protocols to protect your personal information against unauthorized disclosure, alteration, or destruction:
              </p>
              <div class="rounded-xl border border-emerald-200 bg-emerald-50/50 p-4 space-y-2 dark:border-emerald-900/60 dark:bg-emerald-950/30">
                <p class="font-bold text-emerald-950 dark:text-emerald-200 text-xs sm:text-sm flex items-center gap-2">
                  <ShieldCheck class="h-4 w-4 shrink-0 text-emerald-600 dark:text-emerald-400" />
                  {{ t('Our Security Standards') }}
                </p>
                <ul class="list-disc pl-5 space-y-1 text-xs text-emerald-950 dark:text-emerald-300">
                  <li>Encrypted HTTPS/TLS transmission for all web sessions and form submissions.</li>
                  <li>Hashed and salted password storage with industry-standard cryptographic algorithms.</li>
                  <li>Strict access controls limiting student record access to authorized instructors and academy administrators.</li>
                </ul>
              </div>
            </div>
          </section>

          <!-- Section 5: Third-Party Integrations -->
          <section id="third-party" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3 mb-4">
              <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                <Scale class="h-5 w-5" />
              </span>
              <h2 class="text-lg font-bold text-navy-900 dark:text-white">5. {{ t('Third-Party Service Providers') }}</h2>
            </div>
            <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              <p>
                To provide seamless modern services, we integrate with trusted infrastructure providers:
              </p>
              <ul class="list-disc pl-5 space-y-1.5 text-slate-600 dark:text-slate-300">
                <li><strong>Transactional Email (Resend):</strong> Used solely to dispatch verified password reset security emails and account verification codes.</li>
                <li><strong>Google Sign-In:</strong> For optional one-click single sign-on authentication.</li>
                <li><strong>Bakong / National Banking Rails:</strong> For standardized KHQR payment processing.</li>
              </ul>
              <p class="text-xs text-slate-500 dark:text-slate-400">
                We never share your information with third-party advertisers or telemarketing brokers.
              </p>
            </div>
          </section>

          <!-- Section 6: Your Rights & Profile Management -->
          <section id="rights" class="rounded-2xl border border-slate-200 bg-white p-6 sm:p-8 shadow-xs dark:border-slate-800 dark:bg-slate-900">
            <div class="flex items-center gap-3 mb-4">
              <span class="flex h-9 w-9 items-center justify-center rounded-xl bg-navy-50 text-navy-800 dark:bg-slate-800 dark:text-indigo-400">
                <UserCheck class="h-5 w-5" />
              </span>
              <h2 class="text-lg font-bold text-navy-900 dark:text-white">6. {{ t('Your Data Rights & Control') }}</h2>
            </div>
            <div class="space-y-3 text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
              <p>
                You have full control over your educational record and profile:
              </p>
              <ul class="list-disc pl-5 space-y-1.5 text-slate-600 dark:text-slate-300">
                <li><strong>Access & Update:</strong> Modify your contact details, education level, and phone number anytime from your <RouterLink to="/profile" class="text-navy-800 dark:text-indigo-400 font-bold underline">Profile Information</RouterLink> page.</li>
                <li><strong>Data Portability:</strong> Request an export of your enrollment records and certificate verifications.</li>
                <li><strong>Account Deletion:</strong> Request full erasure of your account data by contacting our administrative desk.</li>
              </ul>
            </div>
          </section>

          <!-- Contact box -->
          <section class="rounded-2xl border border-navy-100 bg-gradient-to-r from-navy-900 to-[#1e3a5f] p-6 sm:p-8 text-white shadow-card dark:border-slate-800 dark:from-slate-900 dark:to-indigo-950">
            <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h3 class="text-lg font-bold">{{ t('Questions about your data privacy?') }}</h3>
                <p class="mt-1 text-xs sm:text-sm text-slate-300">
                  Reach out to our privacy officer directly for data inquiries or account deletion requests.
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
  CheckCircle2,
  Clock,
  FileText,
  HelpCircle,
  Lock,
  Mail,
  Scale,
  ShieldCheck,
  UserCheck,
} from 'lucide-vue-next'
import { useLanguage } from '../i18n'

const { t } = useLanguage()

const navSections = [
  { id: 'overview', title: '1. Overview & Commitment' },
  { id: 'collection', title: '2. Information We Collect' },
  { id: 'usage', title: '3. How We Use Data' },
  { id: 'security', title: '4. Data Protection' },
  { id: 'third-party', title: '5. Third-Party Services' },
  { id: 'rights', title: '6. Your Rights & Control' },
]
</script>
