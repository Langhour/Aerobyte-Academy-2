<template>
  <div class="courses-hero dark:bg-slate-900 transition-colors">
    <div class="mx-auto max-w-7xl space-y-12 sm:space-y-16 px-4 sm:px-6 lg:px-8 pb-16 pt-8 sm:pt-12">
      <!-- 1. Top Header Banner (Slide 1 & 2) -->
      <section class="text-center max-w-3xl mx-auto space-y-3">
        <h1 class="text-2xl sm:text-4xl font-black tracking-tight text-navy-900 dark:text-white">
          {{ t('About AeroByte Academy') }}
        </h1>
        <p class="text-xs sm:text-sm leading-relaxed text-slate-600 dark:text-slate-300 max-w-2xl mx-auto">
          {{ t('Where students learn to blend software, coding, and data with physical engineering like robotics, automation, and design.') }}
        </p>
      </section>

      <!-- 2. Overview Hybrid Model Card with Real Lab Photo (Slide 2 & 6) -->
      <section class="rounded-3xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-800/90 overflow-hidden shadow-card grid grid-cols-1 lg:grid-cols-12 items-center">
        <div class="p-6 sm:p-10 lg:col-span-7 space-y-4">
          <span class="inline-flex items-center gap-1.5 text-xs font-bold uppercase tracking-wider text-accent-orange">
            <Layers class="w-4 h-4" />
            {{ t('AeroByte Overview') }}
          </span>
          <h2 class="text-lg sm:text-2xl font-black text-navy-900 dark:text-white leading-snug">
            {{ t('Transitioning to Cambodia\'s Premier STEM & Maker Ecosystem') }}
          </h2>
          <p class="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            {{ t('AeroByte Academy is transitioning from a traditional technical school to a comprehensive STEM Ecosystem. Our hybrid model seamlessly integrates specialized education (Software/Hardware), physical maker kits retail, and community-driven innovation. This ensures multiple pathways for learners while positioning our brand as a leader in Cambodia\'s Industry 4.0 evolution.') }}
          </p>
          <div class="pt-2 flex flex-wrap items-center gap-2.5">
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-bold bg-slate-100 dark:bg-slate-700/80 text-navy-900 dark:text-white">
              <CheckCircle2 class="w-3.5 h-3.5 text-emerald-500" />
              {{ t('Software & Hardware Education') }}
            </span>
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-bold bg-slate-100 dark:bg-slate-700/80 text-navy-900 dark:text-white">
              <CheckCircle2 class="w-3.5 h-3.5 text-emerald-500" />
              {{ t('In-House Maker Kits') }}
            </span>
            <span class="inline-flex items-center gap-1.5 px-3 py-1 rounded-xl text-xs font-bold bg-slate-100 dark:bg-slate-700/80 text-navy-900 dark:text-white">
              <CheckCircle2 class="w-3.5 h-3.5 text-emerald-500" />
              {{ t('Community-Driven Innovation') }}
            </span>
          </div>
        </div>

        <div class="lg:col-span-5 h-64 lg:h-full relative overflow-hidden bg-slate-100 dark:bg-slate-900">
          <img
            src="/assets/about/aerobyte_lab.jpg"
            alt="AeroByte Maker Lab"
            class="w-full h-full object-cover"
            loading="lazy"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/60 via-black/20 to-transparent flex items-end p-5">
            <span class="text-xs font-bold text-white tracking-wide flex items-center gap-1.5">
              <MapPin class="w-3.5 h-3.5 text-accent-orange" />
              {{ t('AeroByte Maker Lab & Robotics Center') }}
            </span>
          </div>
        </div>
      </section>

      <!-- 3. Official Mission & Vision Statements (Slide 3) -->
      <section class="grid grid-cols-1 gap-5 md:grid-cols-2">
        <!-- Official Mission Card -->
        <div class="bg-gradient-to-br from-white to-orange-50/40 dark:from-slate-800 dark:to-slate-800/80 rounded-2xl border border-orange-200/70 dark:border-orange-500/30 p-6 sm:p-8 shadow-card flex flex-col justify-between">
          <div class="space-y-3">
            <div class="w-11 h-11 rounded-2xl bg-orange-100 dark:bg-orange-950/60 text-accent-orange flex items-center justify-center">
              <Target class="w-6 h-6" />
            </div>
            <span class="text-[11px] font-extrabold uppercase tracking-widest text-accent-orange block">
              {{ t('Our Mission') }}
            </span>
            <blockquote class="text-sm sm:text-base font-extrabold text-navy-900 dark:text-white leading-relaxed italic">
              "{{ t('To provide a comprehensive technical ecosystem that equips learners with the expertise to engineer, program, and deploy robotic systems that solve critical real-world challenges.') }}"
            </blockquote>
          </div>
          <div class="mt-6 pt-4 border-t border-orange-100 dark:border-slate-700 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
            <span>AeroByte Core Mission</span>
            <CheckCircle2 class="w-4 h-4 text-accent-orange" />
          </div>
        </div>

        <!-- Official Vision Card -->
        <div class="bg-gradient-to-br from-white to-indigo-50/40 dark:from-slate-800 dark:to-slate-800/80 rounded-2xl border border-indigo-200/70 dark:border-indigo-500/30 p-6 sm:p-8 shadow-card flex flex-col justify-between">
          <div class="space-y-3">
            <div class="w-11 h-11 rounded-2xl bg-indigo-100 dark:bg-indigo-950/60 text-navy-800 dark:text-indigo-400 flex items-center justify-center">
              <Compass class="w-6 h-6" />
            </div>
            <span class="text-[11px] font-extrabold uppercase tracking-widest text-navy-700 dark:text-indigo-400 block">
              {{ t('Our Vision') }}
            </span>
            <blockquote class="text-sm sm:text-base font-extrabold text-navy-900 dark:text-white leading-relaxed italic">
              "{{ t('To cultivate a future-ready workforce through advanced robotics education and industry-aligned innovation initiatives.') }}"
            </blockquote>
          </div>
          <div class="mt-6 pt-4 border-t border-indigo-100 dark:border-slate-700 flex items-center justify-between text-xs text-slate-500 dark:text-slate-400">
            <span>Industry 4.0 Vision</span>
            <CheckCircle2 class="w-4 h-4 text-navy-800 dark:text-indigo-400" />
          </div>
        </div>
      </section>

      <!-- 4. What We Offer: The Unified Ecosystem (Slide 4) -->
      <section class="space-y-6">
        <div class="text-center max-w-2xl mx-auto space-y-2">
          <span class="text-xs font-bold uppercase tracking-wider text-accent-orange">{{ t('What We Offer') }}</span>
          <h2 class="text-xl sm:text-2xl font-black text-navy-900 dark:text-white">
            {{ t('The Unified Ecosystem') }}
          </h2>
          <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
            {{ t('We are the only provider in Cambodia seamlessly combining hardware production, technical instruction, and maintenance under one roof.') }}
          </p>
        </div>

        <div class="grid grid-cols-1 md:grid-cols-3 gap-5">
          <!-- Column 1: Retail & Maker Kits -->
          <div class="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200/80 dark:border-slate-700 p-6 shadow-card hover:shadow-card-hover transition">
            <div class="w-12 h-12 rounded-xl bg-orange-50 dark:bg-orange-950/60 text-accent-orange flex items-center justify-center mb-4">
              <ShoppingBag class="w-6 h-6" />
            </div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-accent-orange">Retail</span>
            <h3 class="text-base font-bold text-navy-900 dark:text-white mt-1 mb-2">{{ t('Retail & Maker Kits') }}</h3>
            <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              {{ t('In-house hardware production, robotics starter kits, microcontrollers, and DIY maker components designed to remove all barriers to hands-on learning.') }}
            </p>
          </div>

          <!-- Column 2: Technical Education -->
          <div class="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200/80 dark:border-slate-700 p-6 shadow-card hover:shadow-card-hover transition">
            <div class="w-12 h-12 rounded-xl bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 flex items-center justify-center mb-4">
              <GraduationCap class="w-6 h-6" />
            </div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-blue-600 dark:text-blue-400">Education</span>
            <h3 class="text-base font-bold text-navy-900 dark:text-white mt-1 mb-2">{{ t('Technical Education') }}</h3>
            <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              {{ t('Structured courses from beginner to advanced levels, spanning robotics engineering, ROS2 middleware, embedded firmware, PCB layout, and 3D prototyping.') }}
            </p>
          </div>

          <!-- Column 3: Engineering Services -->
          <div class="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200/80 dark:border-slate-700 p-6 shadow-card hover:shadow-card-hover transition">
            <div class="w-12 h-12 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center mb-4">
              <Wrench class="w-6 h-6" />
            </div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-emerald-600 dark:text-emerald-400">Services</span>
            <h3 class="text-base font-bold text-navy-900 dark:text-white mt-1 mb-2">{{ t('Engineering Services') }}</h3>
            <p class="text-xs text-slate-600 dark:text-slate-400 leading-relaxed">
              {{ t('Hardware maintenance, specialized prototyping, rapid 3D printing, and continuous engineering support for students, makers, and corporate clients.') }}
            </p>
          </div>
        </div>
      </section>

      <!-- 5. Why Choose Us? (Slide 5) -->
      <section class="space-y-6">
        <div class="text-center max-w-2xl mx-auto space-y-2">
          <span class="text-xs font-bold uppercase tracking-wider text-navy-700 dark:text-indigo-400">{{ t('Competitive Advantage') }}</span>
          <h2 class="text-xl sm:text-2xl font-black text-navy-900 dark:text-white">
            {{ t('Why Choose AeroByte?') }}
          </h2>
          <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400">
            {{ t('What sets AeroByte Academy apart is our complete, self-sustained engineering ecosystem built to empower every student.') }}
          </p>
        </div>

        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-5">
          <div
            v-for="pillar in whyChooseUs"
            :key="pillar.title"
            class="rounded-2xl border border-slate-200/90 dark:border-slate-700 bg-white dark:bg-slate-800 p-5 shadow-card hover:shadow-card-hover transition flex flex-col justify-between"
          >
            <div>
              <div class="w-10 h-10 rounded-xl flex items-center justify-center mb-3.5" :class="pillar.bgClass">
                <component :is="pillar.icon" class="w-5 h-5" :class="pillar.iconClass" />
              </div>
              <span class="text-[10px] font-extrabold uppercase tracking-wider text-accent-orange">{{ pillar.badge }}</span>
              <h3 class="text-sm font-bold text-navy-900 dark:text-white mt-1 mb-1.5">{{ t(pillar.title) }}</h3>
              <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed">{{ t(pillar.description) }}</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 6. Key Metrics Bar (Dynamic from Admin Settings) -->
      <section class="bg-navy-50/70 dark:bg-slate-800/70 rounded-2xl border border-navy-100/80 dark:border-slate-700 py-8 px-6">
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-6 text-center divide-y sm:divide-y-0 sm:divide-x divide-slate-200/70 dark:divide-slate-700">
          <div v-for="stat in stats" :key="stat.label" class="pt-4 sm:pt-0 px-2">
            <div class="text-2xl sm:text-3xl font-extrabold text-navy-900 dark:text-white">
              {{ stat.value }}
            </div>
            <div class="mt-1 text-[11px] font-medium text-slate-500 dark:text-slate-400">
              {{ t(stat.label) }}
            </div>
          </div>
        </div>
      </section>


      <!-- 8. Ecosystem Partnerships & The Racing Drone Warrior Championship (Slide 11-14) -->
      <section class="rounded-3xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-800 overflow-hidden shadow-card grid grid-cols-1 lg:grid-cols-12 items-center">
        <div class="h-64 lg:h-full lg:col-span-5 relative overflow-hidden bg-slate-900">
          <img
            src="/assets/about/drone_championship.jpg"
            alt="The Racing Drone Warrior Championship"
            class="w-full h-full object-cover"
            loading="lazy"
          />
          <div class="absolute inset-0 bg-gradient-to-t from-black/80 via-black/30 to-transparent flex flex-col justify-end p-6">
            <span class="inline-flex items-center gap-1.5 px-2.5 py-1 rounded-md text-[10px] font-black uppercase tracking-wider bg-orange-600 text-white w-fit mb-2">
              Cambodia Premier Tech-Sport
            </span>
            <p class="text-sm font-black text-white">The Racing Drone Warrior Championship</p>
          </div>
        </div>

        <div class="p-6 sm:p-8 lg:col-span-7 space-y-4">
          <span class="text-xs font-bold uppercase tracking-wider text-accent-orange">
            {{ t('Our Ecosystem & Partnerships') }}
          </span>
          <h2 class="text-lg sm:text-xl font-black text-navy-900 dark:text-white">
            {{ t('Anchoring Cambodia\'s Drone & Maker Tech Ecosystem') }}
          </h2>
          <p class="text-xs sm:text-sm text-slate-600 dark:text-slate-300 leading-relaxed">
            {{ t('AeroByte Academy anchors Cambodia\'s tech ecosystem as the proud home of the Cambodia Drone Technology Association (CDTA) with over 2,000 members, alongside our active MakerGuy and HACK THE BEST tech communities. Through national media partnerships with TNOAT and Technology Cambodia, our hands-on events and STEM initiatives reach innovators across the country.') }}
          </p>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-3 pt-2">
            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-100 dark:border-slate-700">
              <p class="text-xs font-bold text-navy-900 dark:text-white flex items-center gap-1.5">
                <Users class="w-3.5 h-3.5 text-blue-500" />
                {{ t('CDTA Association') }}
              </p>
              <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">2,000+ aerial robotics & FPV pilot community members</p>
            </div>
            <div class="p-3 rounded-xl bg-slate-50 dark:bg-slate-900/60 border border-slate-100 dark:border-slate-700">
              <p class="text-xs font-bold text-navy-900 dark:text-white flex items-center gap-1.5">
                <Trophy class="w-3.5 h-3.5 text-accent-orange" />
                {{ t('National Drone Championship') }}
              </p>
              <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-0.5">Merging competitive FPV piloting with advanced STEM</p>
            </div>
          </div>
        </div>
      </section>

      <!-- 9. Contact & Hub Information Bar (Slide 1 & 15) -->
      <section class="rounded-2xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-800 p-6 sm:p-8 shadow-card">
        <div class="grid grid-cols-1 md:grid-cols-3 gap-6 divide-y md:divide-y-0 md:divide-x divide-slate-100 dark:divide-slate-700">
          <div class="flex items-center gap-3.5 pt-4 md:pt-0">
            <div class="w-10 h-10 rounded-xl bg-blue-50 dark:bg-blue-950/60 text-blue-600 dark:text-blue-400 flex items-center justify-center shrink-0">
              <MapPin class="w-5 h-5" />
            </div>
            <div>
              <p class="text-[11px] font-bold uppercase tracking-wider text-slate-400">{{ t('Campus Location') }}</p>
              <p class="text-xs font-bold text-navy-900 dark:text-white mt-0.5">Ta Kmau Krong, Kandal Province, Cambodia</p>
            </div>
          </div>

          <div class="flex items-center gap-3.5 pt-4 md:pt-0 md:pl-6">
            <div class="w-10 h-10 rounded-xl bg-emerald-50 dark:bg-emerald-950/60 text-emerald-600 dark:text-emerald-400 flex items-center justify-center shrink-0">
              <Phone class="w-5 h-5" />
            </div>
            <div>
              <p class="text-[11px] font-bold uppercase tracking-wider text-slate-400">{{ t('Direct Hotline') }}</p>
              <a href="tel:015341002" class="text-xs font-bold text-navy-900 dark:text-white hover:text-navy-800 dark:hover:text-indigo-400 mt-0.5 block">015 341 002</a>
            </div>
          </div>

          <div class="flex items-center gap-3.5 pt-4 md:pt-0 md:pl-6">
            <div class="w-10 h-10 rounded-xl bg-purple-50 dark:bg-purple-950/60 text-purple-600 dark:text-purple-400 flex items-center justify-center shrink-0">
              <Mail class="w-5 h-5" />
            </div>
            <div>
              <p class="text-[11px] font-bold uppercase tracking-wider text-slate-400">{{ t('Email Inquiries') }}</p>
              <a href="mailto:aerobyte.academy@gmail.com" class="text-xs font-bold text-navy-900 dark:text-white hover:text-navy-800 dark:hover:text-indigo-400 mt-0.5 block">aerobyte.academy@gmail.com</a>
            </div>
          </div>
        </div>
      </section>

      <!-- 10. Bottom Dark Navy CTA Banner -->
      <section class="bg-navy-800 dark:bg-slate-800/95 border dark:border-slate-700 rounded-3xl px-6 py-12 text-center text-white shadow-card">
        <h2 class="text-xl sm:text-2xl font-extrabold tracking-tight">
          {{ t('Ready to Build Your First Robot?') }}
        </h2>
        <p class="mt-2.5 text-xs sm:text-sm text-slate-300 dark:text-slate-400 max-w-lg mx-auto leading-relaxed">
          {{ t('Explore our hands-on robotics, IoT, and embedded systems courses and start building real hardware today.') }}
        </p>
        <div class="mt-6">
          <router-link
            to="/courses"
            class="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-white dark:bg-slate-900 text-navy-900 dark:text-white hover:bg-slate-100 dark:hover:bg-slate-800 text-xs font-extrabold tracking-wide transition shadow-xs"
          >
            <span>{{ t('Explore Courses') }}</span>
            <ArrowRight class="w-4 h-4" />
          </router-link>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import {
  Layers,
  CheckCircle2,
  MapPin,
  Target,
  Compass,
  ShoppingBag,
  GraduationCap,
  Wrench,
  Package,
  Cpu,
  TrendingUp,
  Users,
  Trophy,
  Phone,
  Mail,
  ArrowRight
} from 'lucide-vue-next'
import { useLanguage } from '../i18n'
import { siteSettingsService } from '../services/api'

const { t } = useLanguage()

const whyChooseUs = [
  {
    badge: 'Vertical Supply',
    title: 'Vertical Supply',
    description: 'Zero-friction learning with in-house hardware supply and instant component access.',
    icon: Package,
    bgClass: 'bg-orange-50 dark:bg-orange-950/60',
    iconClass: 'text-accent-orange dark:text-orange-400'
  },
  {
    badge: 'Complete Ecosystem',
    title: 'Complete Ecosystem',
    description: 'The unified advantage combining Education, Retail Maker Kits, and Technical Service.',
    icon: Layers,
    bgClass: 'bg-blue-50 dark:bg-blue-950/60',
    iconClass: 'text-blue-600 dark:text-blue-400'
  },
  {
    badge: 'Industry-Ready',
    title: 'Industry-Ready',
    description: 'Industry-aligned technical specialization preparing students for Cambodia\'s Industry 4.0.',
    icon: Cpu,
    bgClass: 'bg-purple-50 dark:bg-purple-950/60',
    iconClass: 'text-purple-600 dark:text-purple-400'
  },
  {
    badge: 'Active Community',
    title: 'Active Community',
    description: 'A thriving maker community flywheel connecting creators, engineers, and innovators.',
    icon: Users,
    bgClass: 'bg-emerald-50 dark:bg-emerald-950/60',
    iconClass: 'text-emerald-600 dark:text-emerald-400'
  }
]


const stats = ref([
  { value: '15+', label: 'Hands-On Tech Courses', key: 'about_courses' },
  { value: '100%', label: 'Project-Based Learning', key: 'about_learning' },
  { value: '12+', label: 'Industry Mentors', key: 'about_mentors' },
  { value: '500+', label: 'Student Projects Built', key: 'about_projects' }
])

onMounted(async () => {
  try {
    const { data } = await siteSettingsService.getPublicSettings()
    stats.value = stats.value.map((stat) => ({ ...stat, value: data[stat.key] || stat.value }))
  } catch (error) {
    console.error('Unable to load public site settings:', error)
  }
})
</script>
