<template>
  <div class="account-access relative isolate flex min-h-screen items-center justify-center overflow-x-hidden overflow-y-auto bg-slate-100 dark:bg-slate-950 px-3 py-4 sm:px-8 sm:py-6">
    <!-- Top-Right Actions: Language Switcher & Dark/Light Mode -->
    <div class="fixed top-3 right-3 sm:top-5 sm:right-6 z-30 flex items-center gap-2">
      <!-- Language Toggle Pill -->
      <div
        class="inline-flex items-center rounded-full border border-slate-200/90 dark:border-slate-700/80 bg-white/90 dark:bg-slate-800/90 p-0.5 shadow-2xs backdrop-blur transition"
        role="group"
        :aria-label="t('Language')"
      >
        <button
          type="button"
          @click="setLocale('en')"
          class="px-2.5 py-1 text-xs font-bold rounded-full transition cursor-pointer"
          :class="locale === 'en'
            ? 'bg-navy-900 text-white dark:bg-blue-600 shadow-xs'
            : 'text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white'"
          :aria-pressed="locale === 'en'"
        >
          EN
        </button>
        <button
          type="button"
          @click="setLocale('kh')"
          class="px-2.5 py-1 text-xs font-bold rounded-full transition cursor-pointer font-khmer"
          :class="locale === 'kh'
            ? 'bg-navy-900 text-white dark:bg-blue-600 shadow-xs'
            : 'text-slate-600 dark:text-slate-300 hover:text-navy-900 dark:hover:text-white'"
          :aria-pressed="locale === 'kh'"
        >
          ខ្មែរ
        </button>
      </div>

      <!-- Dark / Light Mode Toggle Button -->
      <button
        type="button"
        @click="toggleTheme"
        class="inline-flex h-8 w-8 items-center justify-center rounded-full border border-slate-200/90 dark:border-slate-700/80 bg-white/90 dark:bg-slate-800/90 text-slate-700 dark:text-slate-200 shadow-2xs backdrop-blur transition hover:bg-white dark:hover:bg-slate-700 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-navy-800/40 cursor-pointer"
        :aria-label="isDark ? t('Switch to light mode') : t('Switch to dark mode')"
        :title="isDark ? t('Switch to light mode') : t('Switch to dark mode')"
      >
        <Sun v-if="isDark" class="h-4 w-4 text-amber-400" aria-hidden="true" />
        <Moon v-else class="h-4 w-4 text-slate-700 dark:text-slate-200" aria-hidden="true" />
      </button>
    </div>

    <img
      src="/account-access-bg.png"
      alt=""
      class="absolute inset-y-0 right-0 -z-20 h-full w-auto max-w-none object-contain object-right opacity-90 dark:opacity-20 pointer-events-none"
      aria-hidden="true"
    />
    <div
      class="absolute inset-0 -z-10 bg-[linear-gradient(90deg,rgba(255,255,255,0.98)_0%,rgba(255,255,255,0.96)_30%,rgba(255,255,255,0.82)_48%,rgba(255,255,255,0.35)_72%,rgba(255,255,255,0.04)_100%)] dark:bg-[linear-gradient(90deg,rgba(15,23,42,0.98)_0%,rgba(15,23,42,0.95)_35%,rgba(15,23,42,0.8)_55%,rgba(15,23,42,0.35)_75%,rgba(15,23,42,0.05)_100%)] pointer-events-none"
      aria-hidden="true"
    ></div>

    <section class="mx-auto w-full max-w-7xl">
      <div class="w-full max-w-[400px] mx-auto sm:mx-0 px-1 sm:px-2">
        <RouterLink
          to="/courses"
          class="-ml-1 mb-2 sm:mb-2.5 inline-flex items-center gap-1.5 rounded-full border border-white/80 bg-white/75 px-3 py-1 text-xs font-semibold text-navy-900 shadow-2xs backdrop-blur transition hover:bg-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-navy-800/40 dark:border-slate-700/80 dark:bg-slate-800/80 dark:text-slate-200 dark:hover:bg-slate-800"
        >
          <ArrowLeft class="h-3.5 w-3.5" aria-hidden="true" />
          {{ t('Back to courses') }}
        </RouterLink>

        <h1 class="text-2xl font-bold leading-tight tracking-tight text-slate-950 dark:text-white sm:text-[1.65rem]">
          {{ isForgot ? t('Forgot your password?') : isReset ? t('Choose a new password') : isVerify ? t('Verify your email') : isRegister ? t('Create your account') : t('Welcome back') }}
        </h1>
        <p class="mt-0.5 text-xs sm:text-[13px] leading-snug text-slate-700 dark:text-slate-300">
          {{ isForgot ? t('Enter your email and we will send you a password reset link.') : isReset ? t('Choose a new password for your account.') : isVerify ? t('Enter the 6-digit verification code sent to your email.') : isRegister ? t('Register to keep your course information together.') : t('Nice to see you again! Please sign in to continue.') }}
        </p>

        <!-- Informative notice when redirected from course enrollment -->
        <div
          v-if="route.query.redirect"
          class="mt-1.5 rounded-lg border border-sky-200 dark:border-sky-800 bg-sky-50 dark:bg-sky-950/40 px-2.5 py-1 text-xs font-semibold text-sky-900 dark:text-sky-300 flex items-center gap-1.5"
        >
          <span>💡 {{ isRegister ? t('Please register to proceed with your course enrollment.') : t('Please sign in to proceed with your course enrollment.') }}</span>
        </div>

        <div
          v-if="message"
          class="mt-2 rounded-lg border px-3 py-1.5 text-xs sm:text-sm leading-snug"
          :class="(isError || route.query.adminLogout === 'failed')
            ? 'border-red-200 bg-red-50 text-red-800 dark:border-red-900/60 dark:bg-red-950/40 dark:text-red-300'
            : 'border-emerald-200 bg-emerald-50 text-emerald-900 dark:border-emerald-900/60 dark:bg-emerald-950/40 dark:text-emerald-300'"
          :role="(isError || route.query.adminLogout === 'failed') ? 'alert' : 'status'"
        >
          <p>{{ message }}</p>
          <div v-if="devResetUrl" class="mt-1.5 pt-1.5 border-t border-emerald-200 dark:border-emerald-800">
            <p class="text-xs font-bold text-navy-900 dark:text-white">Dev mode reset link generated:</p>
            <a
              :href="devResetUrl"
              class="inline-block mt-0.5 font-semibold text-xs text-blue-700 dark:text-sky-400 underline hover:text-navy-900 dark:hover:text-sky-300 break-all"
            >
              Click here to test resetting your password &rarr;
            </a>
          </div>

        </div>

        <form v-if="isForgot" class="mt-2.5 sm:mt-3 space-y-2 sm:space-y-2.5" @submit.prevent="submitResetRequest">
          <label class="block">
            <span class="mb-1 block text-xs sm:text-sm font-semibold text-slate-800 dark:text-slate-200">{{ t('Email') }}</span>
            <input
              v-model.trim="form.email"
              type="email"
              autocomplete="email"
              required
              maxlength="254"
              placeholder="you@example.com"
              class="account-input dark:!bg-slate-800 dark:!border-slate-700 dark:!text-white dark:placeholder:!text-slate-400"
            />
          </label>
          <button
            type="submit"
            :disabled="submitting"
            class="mt-1 inline-flex h-10 w-full items-center justify-center rounded-full bg-[#17313d] px-5 text-sm font-semibold text-white transition hover:bg-navy-900 disabled:opacity-60 dark:bg-blue-600 dark:hover:bg-blue-500"
          >
            {{ submitting ? t('Please wait...') : t('Send reset link') }}
          </button>
          <button type="button" class="w-full text-xs sm:text-sm font-semibold text-slate-700 dark:text-slate-300 underline underline-offset-2 hover:text-navy-900 dark:hover:text-white" @click="goToSignIn">
            {{ t('Back to sign in') }}
          </button>
        </form>

        <form v-else-if="isReset" class="mt-2.5 sm:mt-3 space-y-2 sm:space-y-2.5" @submit.prevent="submitPasswordReset">
          <!-- New Password -->
          <div>
            <div class="mb-1 flex items-center justify-between">
              <label class="block text-xs sm:text-sm font-semibold text-slate-800 dark:text-slate-200">{{ t('New password') }}</label>
              <span v-if="capsLockOn" class="inline-flex items-center gap-1.5 text-[11px] font-medium text-[#1570ef] dark:text-sky-400">
                <svg class="h-3.5 w-3.5 shrink-0" viewBox="0 0 20 20" fill="none" aria-hidden="true">
                  <circle cx="10" cy="10" r="9" fill="#1570EF" />
                  <circle cx="10" cy="6.25" r="1.1" fill="#FFFFFF" />
                  <rect x="8.9" y="8.8" width="2.2" height="5.5" rx="1.1" fill="#FFFFFF" />
                </svg>
                {{ t('Caps lock is on') }}
              </span>
            </div>
            <div class="relative">
              <input
                v-model="form.password"
                :type="passwordVisible ? 'text' : 'password'"
                autocomplete="new-password"
                required
                minlength="8"
                maxlength="256"
                class="pw-input dark:!bg-slate-800 dark:!border-slate-700 dark:!text-white dark:placeholder:!text-slate-400"
                @keydown="checkCapsLock"
                @keyup="checkCapsLock"
                @click="checkCapsLock"
                @focus="checkCapsLock"
                @blur="onPasswordBlur"
              />
              <button
                type="button"
                class="absolute right-3 top-1/2 -translate-y-1/2 rounded p-1 text-slate-500 dark:text-slate-400 transition hover:text-navy-900 dark:hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-navy-800/40"
                :aria-label="passwordVisible ? t('Hide password') : t('Show password')"
                @click="passwordVisible = !passwordVisible"
              >
                <EyeOff v-if="passwordVisible" class="h-4 w-4" aria-hidden="true" />
                <Eye v-else class="h-4 w-4" aria-hidden="true" />
              </button>
            </div>

            <!-- Password strength bars -->
            <div class="mt-1.5">
              <div class="grid grid-cols-4 gap-1.5">
                <div
                  v-for="index in 4"
                  :key="index"
                  class="h-1 rounded-full transition-all duration-300"
                  :class="getStrengthBarClass(index)"
                ></div>
              </div>
              <div class="mt-0.5 flex justify-end">
                <span class="text-[11px] text-slate-500 dark:text-slate-400 font-normal">
                  {{ t(strengthLabel) }}
                </span>
              </div>
            </div>
          </div>

          <!-- Confirm Password -->
          <div>
            <div class="mb-1 flex items-center justify-between">
              <label class="block text-xs sm:text-sm font-semibold text-slate-800 dark:text-slate-200">{{ t('Confirm password') }}</label>
            </div>
            <div class="relative">
              <input
                v-model="form.confirmPassword"
                :type="confirmPasswordVisible ? 'text' : 'password'"
                autocomplete="new-password"
                required
                minlength="8"
                maxlength="256"
                class="pw-input dark:!bg-slate-800 dark:!border-slate-700 dark:!text-white dark:placeholder:!text-slate-400"
                :class="{ 'pw-input-error': passwordMismatch }"
                @keydown="checkCapsLock"
                @keyup="checkCapsLock"
                @click="checkCapsLock"
                @focus="checkCapsLock"
                @blur="onPasswordBlur"
              />
              <button
                type="button"
                class="absolute right-3 top-1/2 -translate-y-1/2 rounded p-1 text-slate-500 dark:text-slate-400 transition hover:text-navy-900 dark:hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-navy-800/40"
                :aria-label="confirmPasswordVisible ? t('Hide password') : t('Show password')"
                @click="confirmPasswordVisible = !confirmPasswordVisible"
              >
                <EyeOff v-if="confirmPasswordVisible" class="h-4 w-4" aria-hidden="true" />
                <Eye v-else class="h-4 w-4" aria-hidden="true" />
              </button>
            </div>
            <p v-if="passwordMismatch" class="mt-1 px-2 text-[11px] font-semibold text-red-500 dark:text-red-400">
              {{ t('Passwords do not match.') }}
            </p>
          </div>
          <button
            type="submit"
            :disabled="submitting || !resetToken"
            class="mt-1 inline-flex h-10 w-full items-center justify-center rounded-full bg-[#17313d] px-5 text-sm font-semibold text-white transition hover:bg-navy-900 disabled:opacity-60 dark:bg-blue-600 dark:hover:bg-blue-500"
          >
            {{ submitting ? t('Please wait...') : t('Update password') }}
          </button>
          <button type="button" class="w-full text-xs sm:text-sm font-semibold text-slate-700 dark:text-slate-300 underline underline-offset-2 hover:text-navy-900 dark:hover:text-white" @click="goToSignIn">
            {{ t('Back to sign in') }}
          </button>
        </form>

        <form v-else-if="isVerify" class="mt-2.5 sm:mt-3 space-y-3.5" @submit.prevent="submitVerifyCode">
          <div class="rounded-xl border border-sky-200 dark:border-sky-800 bg-sky-50 dark:bg-sky-950/40 p-3 text-xs text-sky-900 dark:text-sky-200">
            <div class="flex items-center gap-2">
              <Mail class="h-4 w-4 shrink-0 text-navy-800 dark:text-sky-300" />
              <span class="font-medium">{{ t('We sent a verification code to:') }}</span>
            </div>
            <p class="mt-1 font-bold text-navy-950 dark:text-white break-all text-sm">{{ verifyEmail }}</p>
          </div>


          <div>
            <label class="block text-xs sm:text-sm font-semibold text-slate-800 dark:text-slate-200 mb-2">
              {{ t('Enter 6-digit verification code') }}
            </label>
            <div class="flex justify-between gap-1.5 sm:gap-2">
              <input
                v-for="(digit, index) in otpDigits"
                :key="index"
                :ref="el => { if (el) otpInputs[index] = el }"
                v-model="otpDigits[index]"
                type="text"
                inputmode="numeric"
                pattern="[0-9]*"
                maxlength="1"
                class="w-10 sm:w-12 h-12 text-center text-lg sm:text-xl font-black rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-navy-950 dark:text-white focus:border-navy-900 dark:focus:border-blue-500 focus:ring-2 focus:ring-navy-900/20 dark:focus:ring-blue-500/20 outline-none transition"
                @input="onOtpInput(index, $event)"
                @keydown="onOtpKeydown(index, $event)"
                @paste="onOtpPaste($event)"
              />
            </div>
          </div>

          <button
            type="submit"
            :disabled="submitting || otpDigits.join('').length !== 6"
            class="inline-flex h-10 w-full items-center justify-center rounded-full bg-[#17313d] px-5 text-sm font-semibold text-white transition hover:bg-navy-900 disabled:opacity-50 dark:bg-blue-600 dark:hover:bg-blue-500 cursor-pointer"
          >
            {{ submitting ? t('Verifying...') : t('Verify & Activate Account') }}
          </button>

          <div class="flex flex-col items-center gap-2 pt-1 text-center text-xs text-slate-600 dark:text-slate-400">
            <button
              type="button"
              :disabled="resendCooldown > 0 || resending"
              class="font-semibold underline underline-offset-2 hover:text-navy-900 dark:hover:text-white disabled:opacity-50 disabled:no-underline cursor-pointer"
              @click="resendVerificationCode"
            >
              {{ resendCooldown > 0 ? `${t('Resend code in')} ${resendCooldown}s` : (resending ? t('Sending...') : t('Resend code')) }}
            </button>

            <button
              type="button"
              class="text-slate-500 dark:text-slate-400 hover:text-slate-800 dark:hover:text-slate-200 cursor-pointer"
              @click="goToRegister"
            >
              {{ t('Change email address') }}
            </button>
          </div>
        </form>

        <form v-else class="mt-2.5 sm:mt-3 space-y-2 sm:space-y-2.5" @submit.prevent="submitAccountForm">
          <label v-if="isRegister" class="block">
            <span class="mb-1 block text-xs sm:text-sm font-semibold text-slate-800 dark:text-slate-200">{{ t('Full name') }}</span>
            <input
              v-model.trim="form.name"
              type="text"
              autocomplete="name"
              required
              maxlength="120"
              @keypress="onNameKeypress"
              @input="onNameInput"
              :placeholder="t('Enter full name')"
              class="account-input dark:!bg-slate-800 dark:!border-slate-700 dark:!text-white dark:placeholder:!text-slate-400"
            />
          </label>

          <label class="block">
            <span class="mb-1 block text-xs sm:text-sm font-semibold text-slate-800 dark:text-slate-200">{{ t('Email') }}</span>
            <input
              v-model.trim="form.email"
              type="email"
              autocomplete="email"
              required
              maxlength="254"
              placeholder="you@example.com"
              class="account-input dark:!bg-slate-800 dark:!border-slate-700 dark:!text-white dark:placeholder:!text-slate-400"
            />
          </label>

          <div>
            <div class="mb-1 flex items-center justify-between">
              <label class="block text-xs sm:text-sm font-semibold text-slate-800 dark:text-slate-200">{{ t('Password') }}</label>
              <span v-if="capsLockOn" class="inline-flex items-center gap-1.5 text-[11px] font-medium text-[#1570ef] dark:text-sky-400">
                <svg class="h-3.5 w-3.5 shrink-0" viewBox="0 0 20 20" fill="none" aria-hidden="true">
                  <circle cx="10" cy="10" r="9" fill="#1570EF" />
                  <circle cx="10" cy="6.25" r="1.1" fill="#FFFFFF" />
                  <rect x="8.9" y="8.8" width="2.2" height="5.5" rx="1.1" fill="#FFFFFF" />
                </svg>
                {{ t('Caps lock is on') }}
              </span>
            </div>
            <div class="relative">
              <input
                v-model="form.password"
                :type="passwordVisible ? 'text' : 'password'"
                :autocomplete="isRegister ? 'new-password' : 'current-password'"
                required
                minlength="8"
                :placeholder="t('At least 8 characters')"
                class="account-input pr-10 dark:!bg-slate-800 dark:!border-slate-700 dark:!text-white dark:placeholder:!text-slate-400"
                @keydown="checkCapsLock"
                @keyup="checkCapsLock"
                @click="checkCapsLock"
                @focus="checkCapsLock"
                @blur="onPasswordBlur"
              />
              <button
                type="button"
                class="absolute right-3 top-1/2 -translate-y-1/2 rounded p-1 text-slate-500 dark:text-slate-400 transition hover:text-navy-900 dark:hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-navy-800/40"
                :aria-label="passwordVisible ? t('Hide password') : t('Show password')"
                @click="passwordVisible = !passwordVisible"
              >
                <EyeOff v-if="passwordVisible" class="h-4 w-4" aria-hidden="true" />
                <Eye v-else class="h-4 w-4" aria-hidden="true" />
              </button>
            </div>

            <!-- Password strength for registration -->
            <div v-if="isRegister" class="mt-1.5">
              <div class="grid grid-cols-4 gap-1.5">
                <div
                  v-for="index in 4"
                  :key="index"
                  class="h-1 rounded-full transition-all duration-300"
                  :class="getStrengthBarClass(index)"
                ></div>
              </div>
              <div class="mt-0.5 flex justify-end">
                <span class="text-[11px] text-slate-500 dark:text-slate-400 font-normal">
                  {{ t(strengthLabel) }}
                </span>
              </div>
            </div>
          </div>

          <div v-if="isRegister">
            <div class="mb-1 flex items-center justify-between">
              <label class="block text-xs sm:text-sm font-semibold text-slate-800 dark:text-slate-200">{{ t('Confirm password') }}</label>
            </div>
            <div class="relative">
              <input
                v-model="form.confirmPassword"
                :type="confirmPasswordVisible ? 'text' : 'password'"
                autocomplete="new-password"
                required
                minlength="8"
                :placeholder="t('Confirm password')"
                class="account-input pr-10 dark:!bg-slate-800 dark:!border-slate-700 dark:!text-white dark:placeholder:!text-slate-400"
                :class="{ 'account-input-error': passwordMismatch }"
                @keydown="checkCapsLock"
                @keyup="checkCapsLock"
                @click="checkCapsLock"
                @focus="checkCapsLock"
                @blur="onPasswordBlur"
              />
              <button
                type="button"
                class="absolute right-3 top-1/2 -translate-y-1/2 rounded p-1 text-slate-500 dark:text-slate-400 transition hover:text-navy-900 dark:hover:text-white focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-navy-800/40"
                :aria-label="confirmPasswordVisible ? t('Hide password') : t('Show password')"
                @click="confirmPasswordVisible = !confirmPasswordVisible"
              >
                <EyeOff v-if="confirmPasswordVisible" class="h-4 w-4" aria-hidden="true" />
                <Eye v-else class="h-4 w-4" aria-hidden="true" />
              </button>
            </div>
            <p v-if="passwordMismatch" class="mt-1 px-2 text-[11px] font-semibold text-red-500 dark:text-red-400">
              {{ t('Passwords do not match.') }}
            </p>
          </div>

          <div v-if="!isRegister" class="flex justify-end">
            <button
              type="button"
              class="text-xs sm:text-sm font-medium text-slate-800 dark:text-sky-400 underline underline-offset-2 hover:text-navy-700 dark:hover:text-sky-300"
              @click="goToForgotPassword"
            >
              {{ t('Forgot Password?') }}
            </button>
          </div>

          <button
            type="submit"
            :disabled="submitting"
            class="mt-1 inline-flex h-10 w-full items-center justify-center rounded-full bg-[#17313d] px-5 text-sm font-semibold text-white transition hover:bg-navy-900 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-navy-800 focus-visible:ring-offset-2 dark:bg-blue-600 dark:hover:bg-blue-500"
          >
            {{ submitting ? t('Please wait...') : isRegister ? t('Register') : t('Sign in') }}
          </button>
        </form>

        <div v-if="!isForgot && !isReset && !isVerify" class="my-2.5 flex items-center gap-3 text-xs text-slate-500 dark:text-slate-400" aria-hidden="true">
          <span class="h-px flex-1 bg-white/90 dark:bg-slate-700"></span>
          <span>{{ t('Or') }}</span>
          <span class="h-px flex-1 bg-white/90 dark:bg-slate-700"></span>
        </div>

        <button
          v-if="!isForgot && !isReset && !isVerify"
          type="button"
          class="flex h-10 w-full items-center justify-center gap-2.5 rounded-full border border-slate-300 bg-white px-4 text-sm font-semibold text-slate-700 shadow-2xs transition hover:bg-slate-50 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-navy-800/40 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
          @click="startGoogleSignIn"
        >
          <img src="/google-icon.png" alt="" class="h-4 w-4 shrink-0 object-contain" aria-hidden="true" />
          <span class="whitespace-nowrap">{{ isRegister ? t('Continue with Google') : t('Sign in with Google') }}</span>
        </button>

        <p v-if="!isForgot && !isReset && !isVerify" class="mt-2.5 sm:mt-3 text-center text-xs sm:text-sm leading-5 text-slate-700 dark:text-slate-400">
          {{ isRegister ? t('Already have an account?') : t("Don't you have an account?") }}
          <RouterLink
            :to="{ path: '/account', query: { mode: isRegister ? 'signin' : 'register', ...(route.query.redirect ? { redirect: route.query.redirect } : {}) } }"
            class="ml-1 font-bold text-slate-900 dark:text-sky-400 underline underline-offset-2 hover:text-navy-700 dark:hover:text-sky-300"
          >
            {{ isRegister ? t('Sign in') : t('Sign up') }}
          </RouterLink>
        </p>

      </div>
    </section>
  </div>
</template>

<script setup>
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ArrowLeft, Eye, EyeOff, Mail, Moon, Sun } from 'lucide-vue-next'
import { useLanguage } from '../i18n'
import { useTheme } from '../composables/useTheme'
import { accountService, adminService, getGoogleSignInUrl } from '../services/api'

const route = useRoute()
const router = useRouter()
const { locale, setLocale, t } = useLanguage()
const { isDark, toggleTheme } = useTheme()
const isRegister = computed(() => route.query.mode === 'register')
const isForgot = computed(() => route.query.mode === 'forgot')
const isReset = computed(() => route.query.mode === 'reset')
const isVerify = computed(() => route.query.mode === 'verify')
const verifyEmail = ref(route.query.email || '')
const otpDigits = ref(['', '', '', '', '', ''])
const otpInputs = ref([])
const resendCooldown = ref(0)
const resending = ref(false)
let resendTimer = null
const passwordMismatch = computed(() => {
  return Boolean(form.confirmPassword && form.password !== form.confirmPassword)
})

const capsLockOn = ref(false)

function checkCapsLock(event) {
  if (event && typeof event.getModifierState === 'function') {
    capsLockOn.value = event.getModifierState('CapsLock')
  }
}

function onPasswordBlur() {
  capsLockOn.value = false
}

const passwordScore = computed(() => {
  const pwd = form.password
  if (!pwd || pwd.length === 0) return 0
  if (pwd.length < 6) return 1

  let score = 1
  if (pwd.length >= 8) score += 1
  if (pwd.length >= 12) score += 1

  const hasUpper = /[A-Z]/.test(pwd)
  const hasLower = /[a-z]/.test(pwd)
  const hasNumber = /[0-9]/.test(pwd)
  const hasSpecial = /[^A-Za-z0-9]/.test(pwd)
  const variety = [hasUpper, hasLower, hasNumber, hasSpecial].filter(Boolean).length

  if (variety >= 3 && pwd.length >= 8) {
    score = Math.max(score, 3)
  }
  if (variety >= 3 && pwd.length >= 10) {
    score = 4
  }
  if (variety < 2 && pwd.length < 12) {
    score = Math.min(score, 2)
  }

  return Math.min(Math.max(score, 1), 4)
})

const strengthLabel = computed(() => {
  if (!form.password) return 'Password strength'
  switch (passwordScore.value) {
    case 1: return 'Very weak'
    case 2: return 'Weak'
    case 3: return 'Good'
    case 4: return 'Strong'
    default: return 'Password strength'
  }
})

function getStrengthBarClass(index) {
  if (!form.password) return 'bg-slate-200 dark:bg-slate-700'
  const score = passwordScore.value
  if (index > score) return 'bg-slate-200 dark:bg-slate-700'
  if (score === 1) return 'bg-[#dc2626]'
  if (score === 2) return 'bg-[#ea580c]'
  if (score === 3) return 'bg-[#0284c7]'
  return 'bg-[#0e7051]'
}
const message = ref('')
const devResetUrl = ref('')
const isError = ref(false)
const passwordVisible = ref(false)
const confirmPasswordVisible = ref(false)
const submitting = ref(false)
const resetToken = ref(typeof route.query.token === 'string' ? route.query.token : '')
const form = reactive({
  name: '',
  email: '',
  password: '',
  confirmPassword: '',
})

watch([() => route.query.mode, () => route.query.email, () => route.query.adminLogout, () => route.query.google_error, () => route.query.token, () => route.query.reset_success], () => {
  const googleError = route.query.google_error
  devResetUrl.value = ''
  isError.value = false
  if (route.query.email) {
    verifyEmail.value = String(route.query.email)
  }
  if (route.query.adminLogout === 'failed') {
    isError.value = true
    message.value = t('Sign-in page opened, but the server could not confirm admin sign-out. Please retry sign-out before leaving this device unattended.')
  } else if (route.query.reset_success === '1') {
    message.value = t('Your password has been reset. You can now sign in.')
  } else if (googleError === 'not_configured') {
    isError.value = true
    message.value = t('Google sign-in is not configured yet. Please configure GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET.')
  } else if (googleError) {
    isError.value = true
    message.value = t('Google sign-in could not be completed. Please try again or use your email and password.')
  } else if (route.query.mode !== 'verify') {
    message.value = ''
  }
  passwordVisible.value = false
  confirmPasswordVisible.value = false
  resetToken.value = typeof route.query.token === 'string' ? route.query.token : ''
  form.password = ''
  form.confirmPassword = ''

  if (route.query.mode === 'verify' && route.query.token) {
    verifyViaToken(route.query.token)
  }
}, { immediate: true })

function onOtpInput(index, event) {
  const val = event.target.value.replace(/[^0-9]/g, '')
  otpDigits.value[index] = val ? val[val.length - 1] : ''
  if (val && index < 5) {
    otpInputs.value[index + 1]?.focus()
  }
}

function onOtpKeydown(index, event) {
  if (event.key === 'Backspace' && !otpDigits.value[index] && index > 0) {
    otpInputs.value[index - 1]?.focus()
  }
}

function onOtpPaste(event) {
  event.preventDefault()
  const pasted = (event.clipboardData || window.clipboardData).getData('text').replace(/[^0-9]/g, '').slice(0, 6)
  if (!pasted) return
  for (let i = 0; i < 6; i++) {
    otpDigits.value[i] = pasted[i] || ''
  }
  const nextIdx = Math.min(pasted.length, 5)
  otpInputs.value[nextIdx]?.focus()
}


function startResendCooldown(seconds = 30) {
  resendCooldown.value = seconds
  clearInterval(resendTimer)
  resendTimer = setInterval(() => {
    resendCooldown.value--
    if (resendCooldown.value <= 0) {
      clearInterval(resendTimer)
    }
  }, 1000)
}

async function verifyViaToken(token) {
  submitting.value = true
  message.value = ''
  isError.value = false
  try {
    await accountService.verifyEmailToken(token)
    window.dispatchEvent(new Event('aerobyte-auth-updated'))
    const redirectUrl = (typeof route.query.redirect === 'string' && route.query.redirect.startsWith('/'))
      ? route.query.redirect
      : '/profile'
    sessionStorage.removeItem('aerobyte_enroll_redirect')
    await router.push(redirectUrl)
  } catch (error) {
    isError.value = true
    message.value = error.response?.data?.detail || t('The verification link is invalid or has expired.')
  } finally {
    submitting.value = false
  }
}

async function submitVerifyCode() {
  const code = otpDigits.value.join('')
  if (code.length !== 6) return
  submitting.value = true
  message.value = ''
  isError.value = false
  try {
    await accountService.verifyEmail({
      email: verifyEmail.value,
      code,
    })
    window.dispatchEvent(new Event('aerobyte-auth-updated'))
    const redirectUrl = (typeof route.query.redirect === 'string' && route.query.redirect.startsWith('/'))
      ? route.query.redirect
      : '/profile'
    sessionStorage.removeItem('aerobyte_enroll_redirect')
    await router.push(redirectUrl)
  } catch (error) {
    isError.value = true
    message.value = error.response?.data?.detail || t('Invalid or expired verification code.')
  } finally {
    submitting.value = false
  }
}

async function resendVerificationCode() {
  if (resendCooldown.value > 0 || resending.value) return
  resending.value = true
  message.value = ''
  isError.value = false
  try {
    const res = await accountService.resendVerification(verifyEmail.value)
    message.value = res.data?.message || t('A new verification code has been sent.')
    startResendCooldown(30)
  } catch (error) {
    isError.value = true
    message.value = error.response?.data?.detail || t('Unable to resend code. Please try again.')
  } finally {
    resending.value = false
  }
}

function goToRegister() {
  message.value = ''
  isError.value = false
  router.push({
    path: '/account',
    query: {
      mode: 'register',
      ...(route.query.redirect ? { redirect: route.query.redirect } : {}),
    },
  })
}

function onNameKeypress(event) {
  if (event.ctrlKey || event.metaKey || event.altKey) {
    return
  }
  if (event.key >= '0' && event.key <= '9') {
    event.preventDefault()
  }
}

function onNameInput(event) {
  const filtered = event.target.value.replace(/[0-9]/g, '')
  form.name = filtered
  event.target.value = filtered
}

async function submitAccountForm() {
  if (isRegister.value && form.password !== form.confirmPassword) {
    isError.value = true
    message.value = t('Passwords do not match.')
    return
  }
  submitting.value = true
  message.value = ''
  try {
    if (isRegister.value) {
      const regResponse = await accountService.register({
        full_name: form.name,
        email: form.email,
        password: form.password,
      })
      const userEmail = form.email
      form.password = ''
      form.confirmPassword = ''
      if (regResponse.data?.verification_required) {
        verifyEmail.value = userEmail
        startResendCooldown(30)
        message.value = regResponse.data.message || t('A 6-digit verification code has been sent to your email.')
        await router.push({
          path: '/account',
          query: {
            mode: 'verify',
            email: userEmail,
            ...(route.query.redirect ? { redirect: route.query.redirect } : {}),
          },
        })
        return
      }
      window.dispatchEvent(new Event('aerobyte-auth-updated'))
      await router.push('/profile')
      return
    }

    try {
      await adminService.login({ email: form.email, password: form.password })
      form.password = ''
      await router.push('/admin')
      return
    } catch (error) {
      if (![401, 503].includes(error.response?.status)) throw error
    }

    await accountService.login({ email: form.email, password: form.password })
    window.dispatchEvent(new Event('aerobyte-auth-updated'))
    form.password = ''
    const redirectUrl = (typeof route.query.redirect === 'string' && route.query.redirect.startsWith('/'))
      ? route.query.redirect
      : '/profile'
    sessionStorage.removeItem('aerobyte_enroll_redirect')
    await router.push(redirectUrl)
  } catch (error) {
    const attemptedEmail = form.email
    form.password = ''
    form.confirmPassword = ''
    if (error.response?.status === 403) {
      isError.value = false
      verifyEmail.value = attemptedEmail
      startResendCooldown(30)
      message.value = error.response.data?.detail || t('Please verify your email address. A 6-digit code has been sent to your inbox.')
      await router.push({
        path: '/account',
        query: {
          mode: 'verify',
          email: attemptedEmail,
          ...(route.query.redirect ? { redirect: route.query.redirect } : {}),
        },
      })
      return
    } else if (error.response?.status === 409) {
      message.value = t('An account with this email already exists. Sign in instead.')
    } else if (error.response?.status === 401) {
      message.value = isRegister.value
        ? t('Unable to create the account. Please check your details and try again.')
        : t('Invalid email or password.')
    } else if (error.response) {
      message.value = error.response.data?.detail || t('Unable to continue right now. Please try again.')
    } else if (error.request) {
      message.value = t('Unable to reach the sign-in server. Please try again later.')
    } else {
      message.value = error.message || t('Unable to continue right now. Please try again.')
    }
  } finally {
    submitting.value = false
  }
}

async function submitResetRequest() {
  submitting.value = true
  message.value = ''
  devResetUrl.value = ''
  isError.value = false
  try {
    const response = await accountService.requestPasswordReset(form.email)
    message.value = response.data?.message || t('If an account exists for that email, a reset link has been sent.')
    if (response.data?.dev_reset_url) {
      devResetUrl.value = response.data.dev_reset_url
    }
  } catch (error) {
    isError.value = true
    message.value = error.response?.data?.detail || t('Unable to send the reset email right now. Please try again later.')
  } finally {
    submitting.value = false
  }
}

async function submitPasswordReset() {
  if (form.password.length < 8) {
    isError.value = true
    message.value = t('Password must be at least 8 characters.')
    return
  }
  if (form.password !== form.confirmPassword) {
    isError.value = true
    message.value = t('Passwords do not match.')
    return
  }
  submitting.value = true
  message.value = ''
  try {
    await accountService.completePasswordReset({ token: resetToken.value, password: form.password })
    form.password = ''
    form.confirmPassword = ''
    message.value = t('Your password has been reset. You can now sign in.')
    await router.replace({ path: '/account', query: { mode: 'signin', reset_success: '1' } })
  } catch (error) {
    message.value = error.response?.data?.detail || t('This reset link is invalid or has expired. Request a new one.')
  } finally {
    submitting.value = false
  }
}

function goToForgotPassword() {
  message.value = ''
  router.push({ path: '/account', query: { mode: 'forgot' } })
}

function goToSignIn() {
  message.value = ''
  router.push({
    path: '/account',
    query: {
      mode: 'signin',
      ...(route.query.redirect ? { redirect: route.query.redirect } : {})
    }
  })
}

function startGoogleSignIn() {
  if (typeof route.query.redirect === 'string' && route.query.redirect.startsWith('/')) {
    sessionStorage.setItem('aerobyte_enroll_redirect', route.query.redirect)
  }
  window.location.assign(getGoogleSignInUrl())
}

onMounted(async () => {
  try {
    const { data } = await accountService.getSession()
    if (data?.authenticated) {
      const redirectUrl = (typeof route.query.redirect === 'string' && route.query.redirect.startsWith('/'))
        ? route.query.redirect
        : '/profile'
      await router.replace(redirectUrl)
    }
  } catch {
    // ignore
  }
})
</script>

<style scoped>
.pw-input {
  display: block;
  width: 100%;
  height: 40px;
  border: 1px solid #cbd5e1;
  border-radius: 8px;
  background: #ffffff;
  padding: 0 38px 0 13px;
  color: #0f172a;
  font-size: 13px;
  outline: none;
  transition: border-color 150ms ease, box-shadow 150ms ease, background-color 150ms ease;
}

.pw-input::placeholder {
  color: #94a3b8;
}

.pw-input:focus {
  border-color: #0284c7;
  box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.2);
}

.pw-input.pw-input-error {
  border-color: #ef4444;
  background: #fef2f2;
}

.pw-input.pw-input-error:focus {
  border-color: #dc2626;
  box-shadow: 0 0 0 1px #dc2626;
}

.account-input {
  display: block;
  width: 100%;
  height: 40px;
  border: 1px solid #cbd5e1;
  border-radius: 9999px;
  background: #ffffff;
  padding: 0 14px;
  color: #0f172a;
  font-size: 13px;
  outline: none;
  transition: border-color 150ms ease, box-shadow 150ms ease, background-color 150ms ease;
}

.account-input::placeholder {
  color: #94a3b8;
}

.account-input:focus {
  border-color: #0284c7;
  background: #ffffff;
  box-shadow: 0 0 0 3px rgba(2, 132, 199, 0.2);
}

.account-input.account-input-error {
  border-color: #ef4444;
  background: #fef2f2;
}

.account-input.account-input-error:focus {
  border-color: #dc2626;
  box-shadow: 0 0 0 3px rgba(239, 68, 68, 0.2);
}

:global(html.dark .pw-input),
:global(html.dark .account-input) {
  border-color: #334155 !important;
  background-color: #1e293b !important;
  color: #f8fafc !important;
}

:global(html.dark .pw-input::placeholder),
:global(html.dark .account-input::placeholder) {
  color: #94a3b8 !important;
}

:global(html.dark .pw-input:focus),
:global(html.dark .account-input:focus) {
  border-color: #38bdf8 !important;
  background-color: #1e293b !important;
  box-shadow: 0 0 0 3px rgba(56, 189, 248, 0.25) !important;
}

:global(html.dark .pw-input.pw-input-error),
:global(html.dark .account-input.account-input-error) {
  border-color: #ef4444 !important;
  background-color: rgba(127, 29, 29, 0.25) !important;
}

:global(input::-ms-reveal),
:global(input::-ms-clear) {
  display: none !important;
  width: 0 !important;
  height: 0 !important;
}
</style>
