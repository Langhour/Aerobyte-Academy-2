<template>
  <div class="max-w-6xl mx-auto px-3 sm:px-6 lg:px-8 pt-5 sm:pt-8 pb-12 sm:pb-16 dark:text-slate-100 transition-colors">
    <!-- Top Page Title -->
    <div class="text-center mb-8 sm:mb-10">
      <h1 class="text-xl sm:text-3xl font-extrabold text-navy-900 dark:text-white tracking-tight">
        {{ t('Course Enrollment Form') }}
      </h1>
      <p class="mt-1 sm:mt-1.5 text-xs sm:text-sm text-slate-500 dark:text-slate-400">
        {{ t('Complete your registration for') }} {{ course?.title || t('your selected course') }}
      </p>
    </div>

    <!-- Loading Skeleton -->
    <div v-if="loadingCourse" class="grid grid-cols-1 lg:grid-cols-12 gap-8 animate-pulse">
      <div class="lg:col-span-8 h-96 bg-slate-100 dark:bg-slate-800 rounded-2xl"></div>
      <div class="lg:col-span-4 h-72 bg-slate-100 dark:bg-slate-800 rounded-2xl"></div>
    </div>

    <div
      v-else-if="loadError"
      role="alert"
      class="mx-auto max-w-xl rounded-2xl border border-red-200 dark:border-red-900/50 bg-red-50 dark:bg-red-950/40 p-6 sm:p-8 text-center"
    >
      <p class="text-sm font-bold text-red-800 dark:text-red-300">      {{ t(loadError) }}</p>
      <RouterLink to="/courses" class="mt-4 inline-block text-sm font-semibold text-navy-800 dark:text-indigo-400">
        {{ t('Back to Courses') }}
      </RouterLink>
    </div>

    <form
      v-else-if="course"
      @submit.prevent="submitEnrollment"
      class="grid grid-cols-1 lg:grid-cols-12 gap-6 sm:gap-8 items-start"
    >
      <p
        v-if="submitError"
        role="alert"
        class="lg:col-span-12 rounded-xl border border-red-200 dark:border-red-900/50 bg-red-50 dark:bg-red-950/40 p-4 text-sm text-red-800 dark:text-red-300"
      >
        {{ t(submitError) }}
      </p>
      <!-- LEFT COLUMN: Multi-Section Form (8 Cols) -->
      <div class="lg:col-span-8 space-y-4 sm:space-y-6">
        <!-- Section 1: Personal Information -->
        <section class="bg-white dark:bg-slate-800 rounded-xl sm:rounded-2xl border border-slate-200/80 dark:border-slate-700 p-4 sm:p-6 shadow-card">
          <h2 class="text-sm font-extrabold text-navy-900 dark:text-white pb-3 mb-5 border-b border-slate-100 dark:border-slate-700">
            {{ t('Personal Information') }}
          </h2>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- Full Name -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                {{ t('Registerer Name') }} <span class="text-accent-red">*</span>
              </label>
              <input
                v-model="form.full_name"
                type="text"
                required
                @keypress="onNameKeypress"
                @input="onNameInput"
                :placeholder="t('Enter full name')"
                class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500"
              />
              <p class="mt-1 text-[10px] text-slate-400 dark:text-slate-500">
                {{ t('Please enter the exact name to appear on your certificate') }}
              </p>
            </div>

            <!-- Date of Birth -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                {{ t('Date of Birth') }} <span class="text-accent-red">*</span>
              </label>
              <DatePicker
                v-model="form.date_of_birth"
                required
                :placeholder="t('Select date of birth')"
                :min-year="1950"
                :max-year="new Date().getFullYear()"
              />
            </div>

            <!-- Gender Radio Group -->
            <div id="gender-field">
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-2">
                {{ t('Gender') }} <span class="text-accent-red">*</span>
              </label>
              <div
                class="flex items-center gap-5 pt-1 px-2.5 py-1.5 rounded-xl transition"
                :class="hasAttemptedSubmit && !form.gender ? 'bg-red-50/60 dark:bg-red-950/20 border border-red-300 dark:border-red-900/50' : ''"
              >
                <label class="flex items-center gap-2 text-xs text-slate-600 dark:text-slate-300 cursor-pointer">
                  <input type="radio" name="gender" value="Male" v-model="form.gender" required class="accent-[#102a49] dark:accent-indigo-500 cursor-pointer" />
                  <span>{{ t('Male') }}</span>
                </label>
                <label class="flex items-center gap-2 text-xs text-slate-600 dark:text-slate-300 cursor-pointer">
                  <input type="radio" name="gender" value="Female" v-model="form.gender" required class="accent-[#102a49] dark:accent-indigo-500 cursor-pointer" />
                  <span>{{ t('Female') }}</span>
                </label>
                <label class="flex items-center gap-2 text-xs text-slate-600 dark:text-slate-300 cursor-pointer">
                  <input type="radio" name="gender" value="Other" v-model="form.gender" required class="accent-[#102a49] dark:accent-indigo-500 cursor-pointer" />
                  <span>{{ t('Other') }}</span>
                </label>
              </div>
              <p v-if="hasAttemptedSubmit && !form.gender" class="mt-1 text-[11px] text-red-600 dark:text-red-400 font-medium">
                {{ t('Please select your gender to continue.') }}
              </p>
            </div>

            <!-- Telegram Contact -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                {{ t('Registerer Telegram') }} <span class="text-accent-red">*</span>
              </label>
              <input
                v-model="form.phone_telegram"
                type="text"
                required
                :placeholder="t('Enter Telegram username or number')"
                class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500"
              />
              <p class="mt-1 text-[10px] text-slate-400 dark:text-slate-500">
                {{ t('Used for course communication and updates') }}
              </p>
            </div>

            <!-- Email Address -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                {{ t('Email Address') }} <span class="text-accent-red">*</span>
              </label>
              <input
                v-model="form.email"
                type="email"
                required
                placeholder="student@example.com"
                class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500"
              />
            </div>

            <!-- Phone Number -->
            <div>
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                {{ t('Phone Number') }} <span class="text-accent-red">*</span>
              </label>
              <input
                v-model="form.phone_number"
                type="tel"
                inputmode="tel"
                required
                maxlength="20"
                @keypress="onPhoneKeypress"
                @input="onPhoneInput"
                :placeholder="t('Enter phone number')"
                class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500"
              />
              <p class="mt-1 text-[10px] text-slate-400 dark:text-slate-500">
                {{ t('Numbers and "+" sign only (e.g. +85512345678)') }}
              </p>
            </div>

            <!-- Current Address (Full Width) -->
            <div class="sm:col-span-2">
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                {{ t('Residential Address') }} <span class="text-accent-red">*</span>
              </label>
              <input
                v-model="form.address"
                type="text"
                required
                :placeholder="t('Street, Sangkat/District, City/Province')"
                class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500"
              />
            </div>
          </div>
        </section>

        <!-- Section 2: Education & Background -->
        <section class="bg-white dark:bg-slate-800 rounded-xl sm:rounded-2xl border border-slate-200/80 dark:border-slate-700 p-4 sm:p-6 shadow-card">
          <h2 class="text-sm font-extrabold text-navy-900 dark:text-white pb-3 mb-5 border-b border-slate-100 dark:border-slate-700">
            {{ t('Education & Background') }}
          </h2>

          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <!-- Age Range -->
            <div ref="ageDropdownRef" class="relative">
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                {{ t('Age Range') }} <span class="text-accent-red">*</span>
              </label>
              <button
                type="button"
                @click="ageDropdownOpen = !ageDropdownOpen; qualificationDropdownOpen = false"
                class="w-full px-3.5 py-2.5 rounded-xl border text-xs bg-white dark:bg-slate-900 flex items-center justify-between text-left focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500 transition cursor-pointer"
                :class="[
                  hasAttemptedSubmit && !form.age_range
                    ? 'border-red-500 dark:border-red-500 ring-1 ring-red-500/30'
                    : ageDropdownOpen
                      ? 'border-navy-800 dark:border-indigo-500 ring-2 ring-navy-800/20'
                      : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
                ]"
              >
                <span :class="form.age_range ? 'text-slate-800 dark:text-white font-medium' : 'text-slate-400 dark:text-slate-500'">
                  {{ form.age_range ? t(form.age_range) : t('Select age range') }}
                </span>
                <ChevronDown class="w-4 h-4 text-slate-400 transition-transform duration-200 shrink-0" :class="{ 'rotate-180 text-navy-800 dark:text-indigo-400': ageDropdownOpen }" />
              </button>
              <p v-if="hasAttemptedSubmit && !form.age_range" class="mt-1 text-[11px] text-red-600 dark:text-red-400">
                {{ t('Please select your age range.') }}
              </p>

              <div
                v-if="ageDropdownOpen"
                class="absolute left-0 right-0 top-full z-30 mt-1.5 overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-1.5 shadow-xl space-y-1"
              >
                <button
                  v-for="option in ageOptions"
                  :key="option"
                  type="button"
                  @click="selectAgeRange(option)"
                  class="flex w-full items-center justify-between rounded-xl px-3 py-2 text-xs transition cursor-pointer"
                  :class="form.age_range === option
                    ? 'bg-navy-50 dark:bg-slate-700 text-navy-900 dark:text-white font-bold'
                    : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/60 hover:text-navy-900 dark:hover:text-white font-medium'"
                >
                  <span>{{ t(option) }}</span>
                  <Check v-if="form.age_range === option" class="w-4 h-4 text-navy-900 dark:text-white shrink-0" />
                </button>
              </div>
            </div>

            <!-- Highest Qualification -->
            <div ref="qualificationDropdownRef" class="relative">
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                {{ t('Highest Qualification') }} <span class="text-accent-red">*</span>
              </label>
              <button
                type="button"
                @click="qualificationDropdownOpen = !qualificationDropdownOpen; ageDropdownOpen = false"
                class="w-full px-3.5 py-2.5 rounded-xl border text-xs bg-white dark:bg-slate-900 flex items-center justify-between text-left focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500 transition cursor-pointer"
                :class="[
                  hasAttemptedSubmit && !form.highest_qualification
                    ? 'border-red-500 dark:border-red-500 ring-1 ring-red-500/30'
                    : qualificationDropdownOpen
                      ? 'border-navy-800 dark:border-indigo-500 ring-2 ring-navy-800/20'
                      : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600'
                ]"
              >
                <span :class="form.highest_qualification ? 'text-slate-800 dark:text-white font-medium' : 'text-slate-400 dark:text-slate-500'">
                  {{ form.highest_qualification ? t(form.highest_qualification) : t('Select qualification') }}
                </span>
                <ChevronDown class="w-4 h-4 text-slate-400 transition-transform duration-200 shrink-0" :class="{ 'rotate-180 text-navy-800 dark:text-indigo-400': qualificationDropdownOpen }" />
              </button>
              <p v-if="hasAttemptedSubmit && !form.highest_qualification" class="mt-1 text-[11px] text-red-600 dark:text-red-400">
                {{ t('Please select your highest qualification.') }}
              </p>

              <div
                v-if="qualificationDropdownOpen"
                class="absolute left-0 right-0 top-full z-30 mt-1.5 overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-1.5 shadow-xl space-y-1"
              >
                <button
                  v-for="option in qualificationOptions"
                  :key="option"
                  type="button"
                  @click="selectQualification(option)"
                  class="flex w-full items-center justify-between rounded-xl px-3 py-2 text-xs transition cursor-pointer"
                  :class="form.highest_qualification === option
                    ? 'bg-navy-50 dark:bg-slate-700 text-navy-900 dark:text-white font-bold'
                    : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/60 hover:text-navy-900 dark:hover:text-white font-medium'"
                >
                  <span>{{ t(option) }}</span>
                  <Check v-if="form.highest_qualification === option" class="w-4 h-4 text-navy-900 dark:text-white shrink-0" />
                </button>
              </div>

              <input
                v-if="form.highest_qualification === 'Other'"
                v-model.trim="form.other_qualification"
                type="text"
                required
                maxlength="120"
                :aria-label="t('Please specify your qualification')"
                :placeholder="t('Please specify your qualification')"
                class="mt-3 w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 px-3.5 py-2.5 text-xs text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500"
              />
            </div>

            <!-- Current Occupation / Institution -->
            <div class="sm:col-span-2">
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                {{ t('Current Occupation / School') }} <span class="text-accent-red">*</span>
              </label>
              <input
                v-model="form.current_occupation"
                type="text"
                required
                :placeholder="t('e.g. ICT Student, Junior Developer, High School Student')"
                class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500"
                @keypress="(e) => { if (/[0-9\u17E0-\u17E9]/.test(e.key)) e.preventDefault() }"
                @input="form.current_occupation = form.current_occupation.replace(/[0-9\u17E0-\u17E9]/g, '')"
              />
            </div>

            <!-- Previous Experience -->
            <div class="sm:col-span-2">
              <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                {{ t('Previous Robotics / Coding Experience') }}
              </label>
              <textarea
                v-model="form.coding_experience"
                rows="2"
                :placeholder="t('Briefly describe any prior experience with Arduino, Python, C++, or electronics (Optional)...')"
                class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500"
              ></textarea>
            </div>
          </div>
        </section>

        <!-- Section 3: Schedule Preference -->
        <section class="bg-white dark:bg-slate-800 rounded-xl sm:rounded-2xl border border-slate-200/80 dark:border-slate-700 p-4 sm:p-6 shadow-card">
          <div class="flex flex-wrap items-center justify-between gap-2 pb-3 mb-5 border-b border-slate-100 dark:border-slate-700">
            <h2 class="text-sm font-extrabold text-navy-900 dark:text-white">
              {{ t('Schedule Preference') }}
            </h2>
            <span class="px-2.5 py-1 rounded-full bg-navy-50 dark:bg-slate-700 text-navy-800 dark:text-slate-200 text-[10px] font-bold">
              {{ getCourseLocalized(course, 'duration') || t('Schedule details provided after enrollment') }}
            </span>
          </div>

          <!-- Start & Completion Date Info Pill Cards -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-5">
            <div class="p-3.5 rounded-xl bg-navy-50/60 dark:bg-slate-700/60 border border-navy-100 dark:border-slate-700 flex items-center gap-3">
              <Calendar class="w-4 h-4 text-navy-800 dark:text-indigo-400 shrink-0" />
              <div>
                <p class="text-[10px] font-semibold uppercase text-slate-400 dark:text-slate-400">{{ t('Cohort Start Date') }}</p>
                <p class="text-xs font-bold text-navy-900 dark:text-white">{{ formatDate(cohortStart) }}</p>
              </div>
            </div>
            <div class="p-3.5 rounded-xl bg-navy-50/60 dark:bg-slate-700/60 border border-navy-100 dark:border-slate-700 flex items-center gap-3">
              <Clock class="w-4 h-4 text-navy-800 dark:text-indigo-400 shrink-0" />
              <div>
                <p class="text-[10px] font-semibold uppercase text-slate-400 dark:text-slate-400">{{ t('Estimated Completion') }}</p>
                <p class="text-xs font-bold text-navy-900 dark:text-white">
                  {{ cohortEnd ? formatDate(cohortEnd) : t('To be confirmed') }}
                </p>
              </div>
            </div>
          </div>

          <!-- Selectable Batch Cards (Matches Figma Highlighted Selection) -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 mb-4">
            <div
              v-for="batch in availableBatches"
              :key="`${batch.day_type}-${batch.time_slot}-${batch.start_time}`"
              @click="selectBatch(batch)"
              class="p-4 rounded-xl border-2 cursor-pointer transition flex items-start justify-between"
              :class="
                form.preferred_schedule === batch.day_type && form.time_slot === batchKey(batch)
                  ? 'border-navy-800 dark:border-indigo-500 bg-navy-50/70 dark:bg-slate-700/60'
                  : 'border-slate-200 dark:border-slate-700 hover:border-slate-300 dark:hover:border-slate-600 bg-white dark:bg-slate-800'
              "
            >
              <div>
                <p class="text-xs font-extrabold text-navy-900 dark:text-white">{{ t(batch.day_type) }}</p>
                <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1">{{ batchDescription(batch) }}</p>
                <p class="mt-1 text-[10px] text-slate-400 dark:text-slate-500">{{ t('Maximum seats') }}: {{ batch.max_seats }}</p>
              </div>
              <input
                type="radio"
                name="course-batch"
                :value="batch.day_type"
                required
                :checked="form.preferred_schedule === batch.day_type && form.time_slot === batchKey(batch)"
                @change="selectBatch(batch)"
                class="mt-0.5 accent-[#102a49] dark:accent-indigo-500 cursor-pointer"
              />
            </div>
          </div>
          <p v-if="!availableBatches.length" class="mb-4 rounded-lg bg-amber-50 dark:bg-amber-950/50 p-3 text-xs text-amber-800 dark:text-amber-300">{{ t('No active batch is available for enrollment. Please contact the academy.') }}</p>

          <!-- Additional Notes -->
          <div>
            <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
              {{ t('Special Requirements or Notes') }}
            </label>
            <textarea
              v-model="form.special_requirements"
              rows="2"
              :placeholder="t('Any specific hardware kit needs or schedule notes...')"
              class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs text-slate-900 dark:text-white focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500"
            ></textarea>
          </div>
        </section>

        <!-- Section 4: Coupon Code & Terms Agreement -->
        <section class="bg-white dark:bg-slate-800 rounded-xl sm:rounded-2xl border border-slate-200/80 dark:border-slate-700 p-4 sm:p-6 shadow-card space-y-4 sm:space-y-5">
          <div>
            <label class="block text-xs font-bold text-navy-900 dark:text-white mb-2">
              {{ t('Coupon Code') }}
            </label>
            <div class="flex gap-2 sm:gap-2.5 max-w-md">
              <input
                v-model="couponInput"
                type="text"
                :placeholder="t('Enter promo code')"
                class="flex-1 px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-900 text-xs text-slate-900 dark:text-white uppercase focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500 min-w-0"
              />
              <button
                type="button"
                @click="handleApplyCoupon"
                :disabled="validatingCoupon || !couponInput.trim()"
                class="px-4 sm:px-5 py-2.5 rounded-xl bg-slate-700 dark:bg-slate-700 hover:bg-navy-800 dark:hover:bg-indigo-600 text-white text-xs font-bold transition disabled:opacity-50 cursor-pointer shrink-0"
              >
                {{ validatingCoupon ? '...' : t('Apply') }}
              </button>
            </div>
            <p
              v-if="couponMessage"
              class="mt-2 text-xs font-medium"
              :class="couponValid ? 'text-accent-green dark:text-emerald-400' : 'text-accent-red dark:text-red-400'"
            >
              {{ t(couponMessage) }}
            </p>
          </div>

          <!-- Terms Checkboxes -->
          <div class="space-y-2.5 pt-3 border-t border-slate-100 dark:border-slate-700">
            <label class="flex items-start gap-2.5 cursor-pointer">
              <input
                type="checkbox"
                v-model="agreedInfoAccurate"
                required
                class="mt-0.5 w-4 h-4 rounded border-slate-300 dark:border-slate-600 accent-[#102a49] dark:accent-indigo-500 focus:ring-[#102a49] cursor-pointer"
              />
              <span class="text-xs text-slate-600 dark:text-slate-300">
                {{ t('I confirm that all personal and academic details provided above are accurate.') }}
              </span>
            </label>

            <label class="flex items-start gap-2.5 cursor-pointer">
              <input
                type="checkbox"
                v-model="agreedTerms"
                required
                class="mt-0.5 w-4 h-4 rounded border-slate-300 dark:border-slate-600 accent-[#102a49] dark:accent-indigo-500 focus:ring-[#102a49] cursor-pointer"
              />
              <span class="text-xs text-slate-600 dark:text-slate-300">
                {{ t("I agree to AeroByte Academy's Enrollment Terms, Lab Safety Guidelines, and Refund Policy.") }}
              </span>
            </label>
          </div>

          <!-- Submit CTA Button -->
          <button
            type="submit"
            :disabled="submitting || !availableBatches.length"
            class="w-full py-3.5 px-6 rounded-xl bg-navy-800 hover:bg-navy-900 dark:bg-indigo-600 dark:hover:bg-indigo-700 text-white text-xs font-extrabold tracking-wide transition shadow-sm flex items-center justify-center gap-2 disabled:opacity-50 cursor-pointer"
          >
            <span>{{ submitting ? t('Processing Enrollment...') : t('Proceed to Payment') }}</span>
            <ArrowRight class="w-4 h-4" />
          </button>
        </section>
      </div>

      <!-- RIGHT COLUMN: Sticky Order Summary Card (4 Cols) -->
      <aside class="lg:col-span-4 bg-white dark:bg-slate-800 rounded-xl sm:rounded-2xl border border-slate-200/80 dark:border-slate-700 p-4 sm:p-6 shadow-card sticky top-20 sm:top-24">
        <h3 class="text-sm font-extrabold text-navy-900 dark:text-white pb-3 mb-4 border-b border-slate-100 dark:border-slate-700">
          {{ t('Order Summary') }}
        </h3>

        <!-- Selected Course Mini Row -->
        <div class="flex items-center gap-3.5 pb-4 mb-4 border-b border-slate-100 dark:border-slate-700">
          <img
            v-if="course.image_url"
            :src="resolveImageUrl(course.image_url)"
            :alt="getCourseLocalized(course, 'title')"
            class="w-16 h-14 rounded-lg object-cover bg-slate-100 dark:bg-slate-700 shrink-0"
          />
          <div
            v-else
            class="flex h-14 w-16 shrink-0 items-center justify-center rounded-lg bg-navy-50 dark:bg-slate-700 text-lg font-extrabold text-navy-800 dark:text-slate-200"
            aria-hidden="true"
          >
            {{ (getCourseLocalized(course, 'category') || 'C').slice(0, 1) }}
          </div>
          <div>
            <span class="text-[10px] font-bold uppercase tracking-wider text-navy-600 dark:text-indigo-400">
              {{ getCourseLocalized(course, 'category') }}
            </span>
            <h4 class="text-xs font-extrabold text-navy-900 dark:text-white line-clamp-2">
              {{ getCourseLocalized(course, 'title') }}
            </h4>
            <p class="mt-1 text-[10px] text-slate-500 dark:text-slate-400">
              <template v-if="course.duration">{{ getCourseLocalized(course, 'duration') }} · </template>{{ formatDate(cohortStart) }}
            </p>
          </div>
        </div>

        <!-- Price Breakdown -->
        <div class="space-y-2.5 text-xs pb-4 mb-4 border-b border-slate-100 dark:border-slate-700">
          <div class="flex justify-between text-slate-500 dark:text-slate-400">
            <span>{{ t('Price per student') }}</span>
            <span class="font-semibold text-slate-800 dark:text-slate-200">${{ (course.original_price || course.price).toFixed(2) }}</span>
          </div>
          <div v-if="totalDiscount > 0" class="flex justify-between text-slate-500 dark:text-slate-400">
            <span>{{ t('Discount') }}</span>
            <span class="font-semibold text-accent-orange">
              -${{ totalDiscount.toFixed(2) }}
            </span>
          </div>
          <div v-if="totalDiscount > 0" class="flex justify-between text-slate-500 dark:text-slate-400">
            <span>{{ t('Base price') }}</span>
            <span class="font-semibold text-slate-800 dark:text-slate-200">${{ finalAmount.toFixed(2) }}</span>
          </div>
          <div v-for="fee in enrollmentFees" :key="fee.label" class="flex justify-between text-slate-500 dark:text-slate-400">
            <span>{{ t(fee.label) }}</span>
            <span class="font-semibold text-slate-800 dark:text-slate-200">${{ fee.amount.toFixed(2) }}</span>
          </div>
        </div>

        <!-- Total Amount Due -->
        <div class="flex items-baseline justify-between mb-5">
          <span class="text-xs font-bold text-navy-900 dark:text-white">{{ t('Total Price') }}</span>
          <span class="text-xl font-extrabold text-navy-900 dark:text-white">
            ${{ totalPrice.toFixed(2) }}
          </span>
        </div>

        <!-- Info Callout Box -->
        <div class="p-3.5 rounded-xl bg-indigo-50 dark:bg-indigo-950/40 border border-indigo-100 dark:border-indigo-900/50 flex items-start gap-2.5">
          <ShieldCheck class="w-4 h-4 text-navy-800 dark:text-indigo-400 shrink-0 mt-0.5" />
          <p class="text-[11px] text-slate-600 dark:text-slate-300 leading-relaxed">
            {{ t('Secure checkout. Your personal information is used to process your course registration.') }}
          </p>
        </div>
      </aside>
    </form>
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { Calendar, Clock, ArrowRight, ShieldCheck, ChevronDown, Check } from 'lucide-vue-next'
import DatePicker from '../components/common/DatePicker.vue'
import { accountService, courseService, enrollmentService } from '../services/api'
import { useLanguage, getCourseLocalized } from '../i18n'
import { resolveImageUrl } from '../utils/image'

const route = useRoute()
const router = useRouter()
const { t, isKhmer } = useLanguage()

const course = ref(null)
const accountId = ref(null)
const loadingCourse = ref(true)
const submitting = ref(false)
const loadError = ref('')
const submitError = ref('')

const couponInput = ref('')
const validatingCoupon = ref(false)
const couponValid = ref(false)
const couponMessage = ref('')
const discountAmount = ref(0)

const agreedInfoAccurate = ref(false)
const agreedTerms = ref(false)
const ageOptions = ['Under 15', '15 - 18 Years', '18 - 24 Years', '25+ Years']
const qualificationOptions = ['High School', 'Undergraduate / University', "Bachelor's Degree", 'Other']
const ageDropdownOpen = ref(false)
const qualificationDropdownOpen = ref(false)
const ageDropdownRef = ref(null)
const qualificationDropdownRef = ref(null)

const hasAttemptedSubmit = ref(false)

function selectAgeRange(value) {
  form.age_range = value
  ageDropdownOpen.value = false
  if (submitError.value === t('Please select your age range.')) {
    submitError.value = ''
  }
}

function selectQualification(value) {
  form.highest_qualification = value
  qualificationDropdownOpen.value = false
  if (submitError.value === t('Please select your highest qualification.')) {
    submitError.value = ''
  }
}

watch(() => form.gender, (val) => {
  if (val && submitError.value === t('Please select your gender to continue.')) {
    submitError.value = ''
  }
})

function handleDropdownClickOutside(event) {
  if (ageDropdownRef.value && !ageDropdownRef.value.contains(event.target)) {
    ageDropdownOpen.value = false
  }
  if (qualificationDropdownRef.value && !qualificationDropdownRef.value.contains(event.target)) {
    qualificationDropdownOpen.value = false
  }
}

const enrollmentFees = ref([
  { label: 'Administration fee', amount: 7.5 },
  { label: 'Certification fee', amount: 5 },
  { label: 'Card fee', amount: 2.5 },
])

const form = reactive({
  full_name: '',
  date_of_birth: '',
  gender: '',
  phone_telegram: '',
  phone_number: '',
  email: '',
  parent_phone: '',
  address: '',
  age_range: '',
  highest_qualification: '',
  other_qualification: '',
  current_occupation: '',
  coding_experience: '',
  preferred_start_date: '',
  preferred_schedule: '',
  time_slot: '',
  special_requirements: '',
  coupon_code: ''
})

const availableBatches = computed(() => {
  if (!course.value?.batch_schedules?.length) {
    return [
      { day_type: 'Weekend Batch', time_slot: '', start_time: '9:00 AM', end_time: '12:00 PM', max_seats: 20 },
      { day_type: 'Weekday Evening', time_slot: '', start_time: '5:30 PM', end_time: '7:30 PM', max_seats: 20 },
    ]
  }
  return course.value.batch_schedules.filter((batch) => batch.active)
})

function batchDescription(batch) {
  return `${batch.time_slot ? `${batch.time_slot} · ` : ''}${batch.start_time} - ${batch.end_time}`
}

function batchKey(batch) {
  return batch.time_slot || `${batch.start_time} - ${batch.end_time}`
}

function selectBatch(batch) {
  form.preferred_schedule = batch.day_type
  form.time_slot = batchKey(batch)
}

function onNameKeypress(event) {
  if (event.ctrlKey || event.metaKey || event.altKey) {
    return
  }
  // Block numbers
  if (event.key >= '0' && event.key <= '9') {
    event.preventDefault()
  }
}

function onNameInput(event) {
  const filtered = event.target.value.replace(/[0-9]/g, '')
  form.full_name = filtered
  event.target.value = filtered
}

function onPhoneKeypress(event) {
  if (event.ctrlKey || event.metaKey || event.altKey) {
    return
  }
  // Allow digits 0-9
  if (event.key >= '0' && event.key <= '9') {
    return
  }
  // Allow '+' only if it is the first character and no '+' exists yet
  if (event.key === '+') {
    const target = event.target
    if (target.selectionStart === 0 && !target.value.includes('+')) {
      return
    }
  }
  event.preventDefault()
}

function onPhoneInput(event) {
  const raw = event.target.value
  let filtered = raw.replace(/[^0-9+]/g, '')
  if (filtered.includes('+')) {
    filtered = (filtered.startsWith('+') ? '+' : '') + filtered.replace(/\+/g, '')
  }
  form.phone_number = filtered
  event.target.value = filtered
}

const cohortStart = computed(() => {
  const start = new Date()
  start.setDate(1)
  start.setMonth(start.getMonth() + 1)
  return start
})

const cohortEnd = computed(() => {
  if (!course.value?.duration) return null
  const end = new Date(cohortStart.value)
  const durationWeeks = Number.parseInt(course.value.duration, 10)
  if (!durationWeeks) return null
  end.setDate(end.getDate() + durationWeeks * 7)
  return end
})

function formatDate(date) {
  return date.toLocaleDateString(isKhmer.value ? 'km-KH' : 'en-US', {
    month: 'long',
    day: '2-digit',
    year: 'numeric'
  })
}

const finalAmount = computed(() => {
  if (!course.value) return 0
  return Math.max(0, Number((course.value.price - discountAmount.value).toFixed(2)))
})

const totalPrice = computed(() =>
  Number((finalAmount.value + enrollmentFees.value.reduce((total, fee) => total + fee.amount, 0)).toFixed(2)),
)

const totalDiscount = computed(() => {
  if (!course.value) return 0
  const listedDiscount = Math.max(0, (course.value.original_price || course.value.price) - course.value.price)
  return Number((listedDiscount + discountAmount.value).toFixed(2))
})

async function handleApplyCoupon() {
  if (!course.value || !couponInput.value.trim()) return
  validatingCoupon.value = true
  couponMessage.value = ''
  try {
    const { data } = await enrollmentService.validateCoupon(
      couponInput.value.trim(),
      course.value.price
    )
    couponValid.value = data.valid
    discountAmount.value = data.discount_amount
    couponMessage.value = data.message
    form.coupon_code = data.valid ? data.code : ''
  } catch (err) {
    couponValid.value = false
    discountAmount.value = 0
    couponMessage.value = 'Could not validate coupon code.'
  } finally {
    validatingCoupon.value = false
  }
}

async function submitEnrollment() {
  if (!course.value) return
  hasAttemptedSubmit.value = true

  if (!form.gender) {
    submitError.value = t('Please select your gender to continue.')
    const el = document.getElementById('gender-field')
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'center' })
    return
  }
  if (!form.date_of_birth) {
    submitError.value = t('Please select your date of birth.')
    return
  }
  if (!form.age_range) {
    submitError.value = t('Please select your age range.')
    if (ageDropdownRef.value) ageDropdownRef.value.scrollIntoView({ behavior: 'smooth', block: 'center' })
    return
  }
  if (!form.highest_qualification) {
    submitError.value = t('Please select your highest qualification.')
    if (qualificationDropdownRef.value) qualificationDropdownRef.value.scrollIntoView({ behavior: 'smooth', block: 'center' })
    return
  }
  if (form.highest_qualification === 'Other' && !form.other_qualification.trim()) {
    submitError.value = t('Please specify your qualification.')
    return
  }
  submitting.value = true
  submitError.value = ''
  try {
    const payload = {
      course_id: course.value.id,
      ...form,
      highest_qualification: form.highest_qualification === 'Other'
        ? form.other_qualification.trim()
        : form.highest_qualification,
    }
    const { data } = await enrollmentService.createEnrollment(payload)
    try {
      const enrollmentCache = {
        ...payload,
        ...data,
        student_name: payload.full_name,
        course_title: course.value?.title || data.course_title,
      }
      localStorage.setItem(`aerobyte-enrollment:${data.enrollment_id}`, JSON.stringify(enrollmentCache))
      localStorage.setItem('aerobyte-latest-enrollment', JSON.stringify(enrollmentCache))

      const historyKey = accountId.value
        ? `aerobyte-course-history:${accountId.value}`
        : 'aerobyte-course-history'
      const history = JSON.parse(localStorage.getItem(historyKey) || '[]')
      if (Array.isArray(history)) {
        localStorage.setItem(
          historyKey,
          JSON.stringify([...new Set([data.enrollment_id, ...history])]),
        )
      }
    } catch (storageError) {
      console.error('Could not save enrollment to local course history:', storageError)
    }
    router.push({
      name: 'ScanToPay',
      params: { enrollmentId: data.enrollment_id }
    })
  } catch (err) {
    console.error('Failed to submit enrollment:', err)
    submitError.value = 'Could not submit your enrollment. Please check the details and try again.'
  } finally {
    submitting.value = false
  }
}

onMounted(async () => {
  document.addEventListener('click', handleDropdownClickOutside)
  loadingCourse.value = true
  try {
    const { data } = await accountService.getSession()
    if (!data?.authenticated) {
      router.replace({
        path: '/account',
        query: {
          mode: 'register',
          redirect: route.fullPath,
        },
      })
      return
    }
    accountId.value = data.user.id
    if (!form.full_name && data.user.full_name) {
      form.full_name = data.user.full_name
    }
    if (!form.email && data.user.email) {
      form.email = data.user.email
    }
  } catch (error) {
    console.error('Could not check the signed-in account for enrollment:', error)
    router.replace({
      path: '/account',
      query: {
        mode: 'register',
        redirect: route.fullPath,
      },
    })
    return
  }

  try {
    const { data: feeData } = await enrollmentService.getFees()
    if (Array.isArray(feeData?.breakdown) && feeData.breakdown.length) {
      enrollmentFees.value = feeData.breakdown
    }
  } catch (error) {
    console.error('Could not load current enrollment fee rates:', error)
  }

  try {
    const { data } = await courseService.getCourseById(route.params.id)
    course.value = data
    form.preferred_start_date = formatDate(cohortStart.value)
  } catch (err) {
    console.error('Failed to load course for enrollment:', err)
    loadError.value = 'Unable to load this course for enrollment. Please try again later.'
  } finally {
    loadingCourse.value = false
  }
})
onUnmounted(() => {
  document.removeEventListener('click', handleDropdownClickOutside)
})
</script>
