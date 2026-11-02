<template>
  <div class="pb-16 dark:bg-slate-900 transition-colors">
    <section class="courses-hero px-4 pb-10 pt-8 text-center sm:px-6 sm:pb-16 sm:pt-14 lg:px-8">
      <div class="mx-auto max-w-7xl">
        <h1 class="mt-2 text-2xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight text-navy-900 dark:text-white">
          {{ t('Questions') }}
        </h1>
        <p class="mx-auto mt-2.5 sm:mt-4 max-w-5xl text-sm sm:text-base leading-relaxed text-slate-600 dark:text-slate-300 sm:text-lg">
          {{ t('Answers about courses, enrollment, and learning at AeroByte Academy.') }}
        </p>
      </div>
    </section>

    <section class="mx-auto mt-6 sm:mt-10 max-w-3xl px-3 sm:px-6 lg:px-8">
      <div class="mb-5 sm:mb-6">
        <h2 class="text-lg sm:text-xl font-extrabold text-navy-900 dark:text-white">{{ t('Frequently asked questions') }}</h2>
        <p class="mt-1 text-xs sm:text-sm text-slate-500 dark:text-slate-400">{{ t('Quick answers to help you get started.') }}</p>
      </div>

      <div class="space-y-3">
        <article
          v-for="(item, index) in questions"
          :key="item.question"
          class="overflow-hidden rounded-xl sm:rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 shadow-xs transition hover:border-navy-100 dark:hover:border-slate-600"
        >
          <h3>
            <button
              :id="`question-${index}`"
              type="button"
              class="flex w-full items-center justify-between gap-4 px-5 py-4 text-left text-sm font-bold text-navy-900 dark:text-white sm:px-6 cursor-pointer"
              :aria-expanded="openQuestion === index"
              :aria-controls="`answer-${index}`"
              @click="toggleQuestion(index)"
            >
              <span>{{ t(item.question) }}</span>
              <ChevronDown
                class="h-5 w-5 shrink-0 text-navy-700 dark:text-slate-300 transition-transform"
                :class="{ 'rotate-180': openQuestion === index }"
                aria-hidden="true"
              />
            </button>
          </h3>
          <div
            v-if="openQuestion === index"
            :id="`answer-${index}`"
            role="region"
            :aria-labelledby="`question-${index}`"
            class="border-t border-slate-100 dark:border-slate-700 px-5 pb-5 pt-4 text-sm leading-6 text-slate-600 dark:text-slate-300 sm:px-6"
          >
            {{ t(item.answer) }}
          </div>
        </article>
      </div>

      <div class="mt-8 rounded-2xl border border-navy-100 dark:border-slate-700 bg-navy-50/70 dark:bg-slate-800/80 p-5 sm:flex sm:items-center sm:justify-between sm:gap-6 sm:px-6">
        <div>
          <h2 class="text-sm font-extrabold text-navy-900 dark:text-white">{{ t('Still have a question?') }}</h2>
          <p class="mt-1 text-sm leading-6 text-slate-600 dark:text-slate-300">
            {{ t('Contact our team and we will be happy to help.') }}
          </p>
        </div>
        <RouterLink
          to="/contact"
          class="mt-4 inline-flex shrink-0 items-center gap-2 rounded-lg border border-navy-200 dark:border-slate-600 bg-white dark:bg-slate-700 px-4 py-2.5 text-sm font-bold text-navy-900 dark:text-white transition hover:bg-navy-50 dark:hover:bg-slate-600 sm:mt-0"
        >
          {{ t('Contact Us') }}
          <ArrowRight class="h-4 w-4" aria-hidden="true" />
        </RouterLink>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { ArrowRight, ChevronDown } from 'lucide-vue-next'
import { useLanguage } from '../i18n'

const { t } = useLanguage()
const openQuestion = ref(0)

const questions = [
  {
    question: 'How do I enroll in a course?',
    answer:
      'Choose a course from the catalog, click Enroll Now, and complete the enrollment form. You can pay securely via QR code or mobile banking.',
  },
  {
    question: 'Can I take home the hardware components or circuit boards?',
    answer:
      'No. All hardware components, circuit boards, microcontrollers, and sensor modules used or assembled during class are dedicated lab equipment for practical training at AeroByte Academy. They remain at the academy and cannot be taken home as personal property.',
  },
  {
    question: 'Are the courses taught in Khmer or English?',
    answer:
      'We offer courses in both Khmer and English. Each course card and details page clearly displays the primary language of instruction.',
  },
  {
    question: 'Do I need prior coding or engineering experience?',
    answer:
      'We have beginner-friendly courses that start with visual programming and basic electronics, as well as intermediate and advanced courses in Python, C++, and ROS.',
  },
  {
    question: 'Will I receive a certificate upon completion?',
    answer:
      'Yes. Students who attend all scheduled sessions and successfully complete their final capstone project receive a verified AeroByte Academy certificate.',
  },
  {
    question: 'What equipment do I need to bring to class?',
    answer:
      'All robotics kits, electronic components, testing instruments, and lab tools are fully provided by AeroByte Academy. You only need to bring your own laptop (Windows, macOS, or Linux) with permissions to install course programming software.',
  },
]

function toggleQuestion(index) {
  openQuestion.value = openQuestion.value === index ? -1 : index
}
</script>
