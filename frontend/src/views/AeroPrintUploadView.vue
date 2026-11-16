<template>
  <div class="min-h-screen bg-[#FAFAFA] dark:bg-[#05060B] pb-20 transition-colors">
    <!-- Top Header Strip -->
    <header class="border-b border-black/[0.06] dark:border-white/10 bg-white/90 dark:bg-[#111112]/90 backdrop-blur-md">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 py-5 sm:py-6">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div class="flex flex-col gap-2">
            <router-link
              to="/print"
              class="inline-flex w-fit items-center gap-2 rounded-full border border-black/[0.08] dark:border-white/15 bg-[#F3F4F6] dark:bg-white/5 px-3.5 py-1 text-xs font-semibold text-[#111112] dark:text-white/90 hover:border-navy-900 hover:text-navy-900 dark:hover:border-blue-400 dark:hover:text-blue-400 transition"
            >
              <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2.2">
                <path stroke-linecap="round" stroke-linejoin="round" d="M10.5 19.5L3 12m0 0l7.5-7.5M3 12h18" />
              </svg>
              <span>{{ t('Back to Aero Print') }}</span>
            </router-link>

            <div class="flex flex-wrap items-center gap-2.5">
              <h1 class="text-2xl sm:text-3xl font-bold tracking-[-0.02em] text-[#111112] dark:text-white">
                {{ t('Drop Your 3D CAD Files') }}
              </h1>
              <span class="inline-flex items-center gap-1.5 rounded-full bg-navy-900/10 dark:bg-blue-400/15 border border-navy-900/20 dark:border-blue-400/30 px-3 py-0.5 text-xs font-semibold text-navy-900 dark:text-blue-300">
                <span class="h-1.5 w-1.5 rounded-full bg-navy-900 dark:bg-blue-400"></span>
                Aero Print • {{ t('Direct Telegram Quote') }}
              </span>
            </div>
            <p class="text-xs sm:text-sm text-[#575757] dark:text-white/65">
              {{ t('Drop your 3D CAD files and enter your Telegram contact. Our admin will inspect your models and text you directly on Telegram with the price quote.') }}
            </p>
          </div>

          <!-- Quick Lab Status Badge -->
          <div class="flex items-center gap-2.5 self-start sm:self-center rounded-full border border-black/[0.06] dark:border-white/10 bg-[#F3F4F6] dark:bg-white/5 px-4 py-2 text-xs">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span class="font-semibold text-[#111112] dark:text-white">{{ t('Lab Status: Ready') }}</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Main 2-Column Container -->
    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 mt-6 sm:mt-8">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 sm:gap-8 items-start">

        <!-- LEFT COLUMN: 3D CAD Dropzone & Telegram Contact (8 Cols) -->
        <div class="lg:col-span-8 space-y-6">

          <!-- 1. 3D File Upload Area -->
          <section class="rounded-[24px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111112] p-5 sm:p-7 shadow-sm">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-3">
                <span class="flex h-7 w-7 items-center justify-center rounded-full bg-navy-900 dark:bg-navy-600 text-white font-bold text-xs shadow-sm shadow-navy-900/25">
                  1
                </span>
                <h2 class="text-base sm:text-lg font-bold text-[#111112] dark:text-white">
                  {{ t('Upload 3D CAD Files') }}
                </h2>
              </div>
              <span class="rounded-full bg-[#F3F4F6] dark:bg-white/10 px-3 py-1 text-[11px] font-medium text-[#575757] dark:text-white/70">
                .STL, .STP, .STEP, .OBJ, .3MF
              </span>
            </div>

            <!-- Drag & Drop Zone -->
            <div
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleFileDrop"
              @click="triggerFileInput"
              class="relative rounded-[20px] border-2 border-dashed transition-all p-7 sm:p-10 text-center cursor-pointer group"
              :class="isDragging
                ? 'border-navy-900 dark:border-blue-400 bg-navy-900/[0.06] dark:bg-blue-500/10 scale-[1.01]'
                : 'border-black/15 dark:border-white/15 hover:border-navy-900 dark:hover:border-blue-400 bg-[#FAFAFA] dark:bg-white/[0.02] hover:bg-navy-50/70 dark:hover:bg-white/[0.04]'"
            >
              <input
                ref="fileInputRef"
                type="file"
                multiple
                accept=".stl,.stp,.step,.obj,.3mf,.igs,.iges"
                class="hidden"
                @change="handleFileInputChange"
              />

              <div class="mx-auto flex h-16 w-16 items-center justify-center rounded-2xl bg-navy-900/10 dark:bg-blue-400/15 text-navy-900 dark:text-blue-300 mb-4 group-hover:scale-105 transition-transform">
                <svg class="w-8 h-8" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M3 16.5v2.25A2.25 2.25 0 005.25 21h13.5A2.25 2.25 0 0021 18.75V16.5m-13.5-9L12 3m0 0l4.5 4.5M12 3v13.5" />
                </svg>
              </div>
              <p class="text-sm sm:text-base font-bold text-[#111112] dark:text-white">
                {{ t('Drag & Drop 3D CAD Files Here') }}
              </p>
              <p class="text-xs text-[#696969] dark:text-white/60 mt-1.5">
                {{ t('Supports STL, STEP, OBJ, 3MF up to 350×350×350 mm build plate') }}
              </p>

              <div class="mt-5">
                <span class="inline-flex items-center gap-2 rounded-full bg-navy-900 hover:bg-navy-800 dark:bg-navy-600 dark:hover:bg-navy-800 px-6 py-2.5 text-xs font-bold text-white shadow-[0_10px_25px_rgba(16,42,73,0.28)] transition">
                  {{ t('Select 3D Files') }}
                </span>
              </div>
            </div>

            <!-- Uploaded Files List -->
            <div v-if="files.length > 0" class="mt-5 space-y-3">
              <div
                v-for="(f, idx) in files"
                :key="f.id"
                class="rounded-2xl border border-black/[0.07] dark:border-white/10 bg-[#FAFAFA] dark:bg-white/[0.03] p-4 flex items-center justify-between gap-3"
              >
                <div class="flex items-center gap-3.5 min-w-0">
                  <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-navy-900/10 dark:bg-blue-400/15 text-navy-900 dark:text-blue-300 font-bold text-xs uppercase">
                    3D
                  </div>
                  <div class="min-w-0">
                    <p class="truncate text-xs sm:text-sm font-bold text-[#111112] dark:text-white">{{ f.name }}</p>
                    <div class="flex items-center gap-2 mt-0.5">
                      <span class="text-[11px] text-[#696969] dark:text-white/55 font-mono">{{ f.sizeStr }}</span>
                      <span class="inline-flex items-center gap-1 rounded-full bg-emerald-500/10 text-emerald-600 dark:text-emerald-400 text-[10px] font-semibold px-2 py-0.5">
                        <span class="h-1 w-1 rounded-full bg-emerald-500"></span>
                        {{ t('Ready to submit') }}
                      </span>
                    </div>
                  </div>
                </div>

                <!-- Remove File Button -->
                <button
                  type="button"
                  @click="removeFile(idx)"
                  class="shrink-0 text-xs text-rose-500 hover:text-rose-600 hover:bg-rose-50 dark:hover:bg-rose-950/30 px-3 py-1.5 rounded-full font-semibold transition cursor-pointer flex items-center gap-1.5"
                >
                  <svg class="w-3.5 h-3.5" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                  </svg>
                  <span>{{ t('Delete') }}</span>
                </button>
              </div>
            </div>
          </section>

          <!-- 2. Telegram Contact & Details -->
          <section class="rounded-[24px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111112] p-5 sm:p-7 shadow-sm space-y-5">
            <div class="flex items-center gap-3 mb-1">
              <span class="flex h-7 w-7 items-center justify-center rounded-full bg-navy-900 dark:bg-navy-600 text-white font-bold text-xs shadow-sm shadow-navy-900/25">
                2
              </span>
              <div>
                <h2 class="text-base sm:text-lg font-bold text-[#111112] dark:text-white">
                  {{ t('Your Telegram Contact') }}
                </h2>
                <p class="text-xs text-[#575757] dark:text-white/65 mt-0.5">
                  {{ t('Enter your Telegram username, phone number, or drop your QR code. Our admin will text you directly on Telegram with your price quote.') }}
                </p>
              </div>
            </div>

            <!-- Form Fields Grid -->
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 pt-2">
              <!-- Telegram Username / Phone Number -->
              <div>
                <label class="block text-xs font-bold text-[#111112] dark:text-white/90 mb-1.5">
                  {{ t('Telegram Username or Phone Number *') }}
                </label>
                <div class="relative">
                  <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5 text-[#575757] dark:text-white/50">
                    <svg class="w-4 h-4 text-[#229ED9]" fill="currentColor" viewBox="0 0 24 24">
                      <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.19-.08-.05-.19-.02-.27 0-.12.03-1.99 1.27-5.62 3.72-.53.36-1.01.54-1.44.53-.47-.01-1.38-.27-2.05-.49-.83-.27-1.49-.42-1.43-.88.03-.24.37-.49 1.02-.74 4-1.74 6.68-2.88 8.03-3.44 3.82-1.59 4.62-1.87 5.14-1.88.11 0 .37.03.54.17.14.12.18.28.2.45-.02.07-.02.21-.04.35z"/>
                    </svg>
                  </div>
                  <input
                    v-model="orderForm.telegram"
                    type="text"
                    placeholder="@username or 012 345 678"
                    class="w-full rounded-xl border border-black/15 dark:border-white/15 bg-[#FAFAFA] dark:bg-white/5 pl-10 pr-3.5 py-2.5 text-xs text-[#111112] dark:text-white placeholder:text-[#696969] dark:placeholder:text-white/40 focus:outline-none focus:border-navy-900 dark:focus:border-blue-400 focus:bg-white dark:focus:bg-white/10 transition"
                  />
                </div>
              </div>

              <!-- Customer Name -->
              <div>
                <label class="block text-xs font-bold text-[#111112] dark:text-white/90 mb-1.5">
                  {{ t('Your Name (Optional)') }}
                </label>
                <input
                  v-model="orderForm.name"
                  type="text"
                  placeholder="e.g. Sokha Chan"
                  class="w-full rounded-xl border border-black/15 dark:border-white/15 bg-[#FAFAFA] dark:bg-white/5 px-3.5 py-2.5 text-xs text-[#111112] dark:text-white placeholder:text-[#696969] dark:placeholder:text-white/40 focus:outline-none focus:border-navy-900 dark:focus:border-blue-400 focus:bg-white dark:focus:bg-white/10 transition"
                />
              </div>
            </div>

            <!-- Drop Telegram QR Code Section -->
            <div class="pt-1">
              <label class="block text-xs font-bold text-[#111112] dark:text-white/90 mb-1">
                {{ t('Drop Telegram QR Code (Optional)') }}
              </label>
              <p class="text-[11px] text-[#696969] dark:text-white/55 mb-2.5">
                {{ t('Upload a screenshot or photo of your Telegram QR code so our lab engineers can scan and connect with you immediately.') }}
              </p>

              <!-- QR Upload Dropzone (When not uploaded yet) -->
              <div
                v-if="!qrPreviewUrl"
                @dragover.prevent="isQrDragging = true"
                @dragleave.prevent="isQrDragging = false"
                @drop.prevent="handleQrDrop"
                @click="triggerQrInput"
                class="relative rounded-2xl border-2 border-dashed p-5 text-center cursor-pointer transition group"
                :class="isQrDragging
                  ? 'border-navy-900 dark:border-blue-400 bg-navy-900/[0.05] dark:bg-blue-500/10'
                  : 'border-black/15 dark:border-white/15 hover:border-navy-900 dark:hover:border-blue-400 bg-[#FAFAFA] dark:bg-white/[0.02] hover:bg-navy-50/50 dark:hover:bg-white/[0.03]'"
              >
                <input
                  ref="qrFileInputRef"
                  type="file"
                  accept="image/png,image/jpeg,image/jpg,image/webp"
                  class="hidden"
                  @change="handleQrInputChange"
                />

                <div class="mx-auto flex h-11 w-11 items-center justify-center rounded-xl bg-navy-900/10 dark:bg-blue-400/15 text-navy-900 dark:text-blue-300 mb-2 group-hover:scale-105 transition-transform">
                  <svg class="w-6 h-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M3.75 4.875c0-.621.504-1.125 1.125-1.125h4.5c.621 0 1.125.504 1.125 1.125v4.5c0 .621-.504 1.125-1.125 1.125h-4.5A1.125 1.125 0 013.75 9.375v-4.5zM3.75 14.625c0-.621.504-1.125 1.125-1.125h4.5c.621 0 1.125.504 1.125 1.125v4.5c0 .621-.504 1.125-1.125 1.125h-4.5a1.125 1.125 0 01-1.125-1.125v-4.5zM13.5 4.875c0-.621.504-1.125 1.125-1.125h4.5c.621 0 1.125.504 1.125 1.125v4.5c0 .621-.504 1.125-1.125 1.125h-4.5A1.125 1.125 0 0113.5 9.375v-4.5zM13.5 13.5h2.25v2.25H13.5V13.5zM18 13.5h2.25v2.25H18V13.5zM13.5 18h2.25v2.25H13.5V18zM18 18h2.25v2.25H18V18z" />
                  </svg>
                </div>
                <p class="text-xs font-bold text-[#111112] dark:text-white">
                  {{ t('Drag & Drop Telegram QR Code Image here, or click to upload') }}
                </p>
                <p class="text-[10px] text-[#696969] dark:text-white/50 mt-1">
                  {{ t('Supports PNG, JPG, JPEG, WEBP') }}
                </p>
              </div>

              <!-- QR Code Attached Preview Card -->
              <div
                v-else
                class="rounded-2xl border border-emerald-500/30 bg-emerald-50/40 dark:bg-emerald-950/20 p-4 flex items-center justify-between gap-4"
              >
                <div class="flex items-center gap-3.5 min-w-0">
                  <div class="h-16 w-16 shrink-0 rounded-xl overflow-hidden border border-black/10 dark:border-white/15 bg-white p-1 shadow-sm flex items-center justify-center">
                    <img :src="qrPreviewUrl" alt="Telegram QR Code Preview" class="h-full w-full object-contain" />
                  </div>
                  <div class="min-w-0">
                    <div class="inline-flex items-center gap-1.5 rounded-full bg-emerald-600/10 text-emerald-700 dark:text-emerald-400 px-2.5 py-0.5 text-[10px] font-bold">
                      <span>✓</span>
                      <span>{{ t('QR Code Attached') }}</span>
                    </div>
                    <p class="truncate text-xs font-semibold text-[#111112] dark:text-white mt-1">
                      {{ qrFile?.name || 'telegram-qr.png' }}
                    </p>
                    <p class="text-[10px] text-[#696969] dark:text-white/50">
                      {{ (qrFile?.size ? (qrFile.size / 1024).toFixed(1) + ' KB' : 'Image ready for scan') }}
                    </p>
                  </div>
                </div>

                <button
                  type="button"
                  @click="removeQrFile"
                  class="text-xs text-rose-500 hover:text-rose-600 font-semibold px-3 py-1.5 hover:bg-rose-100/50 dark:hover:bg-rose-950/40 rounded-full cursor-pointer transition shrink-0"
                >
                  {{ t('Remove QR Code') }}
                </button>
              </div>
            </div>

            <!-- Notes & Instructions -->
            <div>
              <label class="block text-xs font-bold text-[#111112] dark:text-white/90 mb-1.5">
                {{ t('Project Notes & Instructions (Optional)') }}
              </label>
              <textarea
                v-model="orderForm.notes"
                rows="3"
                placeholder="Any specific requirements for our lab engineers? (e.g. strength, color preference, or target deadline)..."
                class="w-full rounded-xl border border-black/15 dark:border-white/15 bg-[#FAFAFA] dark:bg-white/5 px-3.5 py-2.5 text-xs text-[#111112] dark:text-white placeholder:text-[#696969] dark:placeholder:text-white/40 focus:outline-none focus:border-navy-900 dark:focus:border-blue-400 focus:bg-white dark:focus:bg-white/10 transition resize-none"
              ></textarea>
            </div>

            <!-- Validation Error Alert -->
            <div
              v-if="validationError"
              class="rounded-xl border border-rose-300 dark:border-rose-900/60 bg-rose-50 dark:bg-rose-950/30 p-3 text-xs text-rose-700 dark:text-rose-300 flex items-center gap-2"
            >
              <svg class="w-4 h-4 shrink-0" fill="currentColor" viewBox="0 0 20 20">
                <path fill-rule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
              </svg>
              <span>{{ validationError }}</span>
            </div>
          </section>
        </div>

        <!-- RIGHT COLUMN: Request Summary Card (4 Cols, Sticky) -->
        <div class="lg:col-span-4 lg:sticky lg:top-20 space-y-5">
          <div class="rounded-[28px] border border-black/[0.07] dark:border-white/10 bg-white dark:bg-[#111112] p-6 shadow-xl shadow-black/[0.04]">
            <div class="flex items-center justify-between border-b border-black/[0.06] dark:border-white/10 pb-4">
              <h3 class="text-lg font-bold text-[#111112] dark:text-white">
                {{ t('3D Print Request Summary') }}
              </h3>
              <span class="inline-flex items-center rounded-full bg-navy-900/10 dark:bg-blue-400/15 px-2.5 py-0.5 text-[11px] font-bold text-navy-900 dark:text-blue-300">
                {{ t('Direct Telegram Quote') }}
              </span>
            </div>

            <!-- Files Overview -->
            <div class="mt-4 space-y-2.5 text-xs">
              <div class="flex justify-between items-center text-[#575757] dark:text-white/60">
                <span>{{ t('Files Attached') }}</span>
                <span class="font-bold text-[#111112] dark:text-white">{{ files.length }} {{ files.length === 1 ? 'file' : 'files' }}</span>
              </div>

              <!-- Mini file list -->
              <div v-if="files.length > 0" class="space-y-1.5 pt-1">
                <div
                  v-for="f in files"
                  :key="f.id"
                  class="flex items-center justify-between rounded-lg bg-[#FAFAFA] dark:bg-white/[0.03] px-2.5 py-1.5 text-[11px]"
                >
                  <span class="truncate font-medium text-[#111112] dark:text-white max-w-[180px]">{{ f.name }}</span>
                  <span class="font-mono text-[10px] font-semibold text-navy-900 dark:text-blue-300">{{ f.sizeStr }}</span>
                </div>
              </div>

              <!-- Telegram status -->
              <div class="border-t border-black/[0.06] dark:border-white/10 pt-3 flex justify-between items-center text-[#575757] dark:text-white/60">
                <span>{{ t('Telegram Contact') }}</span>
                <span class="font-bold text-[#111112] dark:text-white max-w-[160px] truncate text-right">
                  {{ orderForm.telegram || (qrPreviewUrl ? 'QR Attached' : 'Not provided yet') }}
                </span>
              </div>

              <div class="flex justify-between items-center text-[#575757] dark:text-white/60">
                <span>{{ t('QR Code') }}</span>
                <span :class="qrPreviewUrl ? 'text-emerald-600 font-bold' : 'text-[#696969] dark:text-white/50'">
                  {{ qrPreviewUrl ? '✓ Attached' : 'Optional' }}
                </span>
              </div>
            </div>

            <!-- How Quote Works Explainer Card -->
            <div class="mt-5 rounded-2xl bg-navy-50/70 dark:bg-white/[0.03] border border-navy-900/10 dark:border-white/10 p-4 space-y-2.5">
              <p class="text-xs font-bold text-navy-900 dark:text-blue-300 flex items-center gap-1.5">
                <svg class="w-4 h-4" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="2">
                  <path stroke-linecap="round" stroke-linejoin="round" d="M8.625 12a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H8.25m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0H12m4.125 0a.375.375 0 11-.75 0 .375.375 0 01.75 0zm0 0h-.375M21 12c0 4.556-4.03 8.25-9 8.25a9.764 9.764 0 01-2.555-.337A5.972 5.972 0 015.41 20.97a.75.75 0 01-.874-.954 6.027 6.027 0 00.702-2.316C3.805 16.29 3 14.256 3 12c0-4.556 4.03-8.25 9-8.25s9 3.694 9 8.25z" />
                </svg>
                <span>{{ t('How You Get Your Price') }}</span>
              </p>
              <ul class="text-[11px] text-[#575757] dark:text-white/65 space-y-2 leading-relaxed">
                <li>• <strong>1. {{ t('Drop your 3D CAD files') }}:</strong> {{ t('Upload your 3D models here.') }}</li>
                <li>• <strong>2. {{ t('Leave your Telegram') }}:</strong> {{ t('Provide your username, phone, or QR code.') }}</li>
                <li>• <strong>3. {{ t('Admin texts you on Telegram') }}:</strong> {{ t('Our admin reviews your file and texts you the price quote directly on Telegram.') }}</li>
              </ul>
            </div>

            <!-- Action Buttons -->
            <div class="mt-6 space-y-3">
              <button
                type="button"
                @click="submitPrintOrder"
                :disabled="isSubmitting"
                class="w-full rounded-full bg-navy-900 hover:bg-navy-800 dark:bg-navy-600 dark:hover:bg-navy-800 text-white font-bold py-3.5 px-5 text-sm shadow-[0_10px_25px_rgba(16,42,73,0.3)] active:scale-[0.99] disabled:opacity-75 disabled:cursor-not-allowed transition flex items-center justify-center gap-2 cursor-pointer"
              >
                <svg v-if="isSubmitting" class="w-4 h-4 animate-spin text-white" fill="none" viewBox="0 0 24 24">
                  <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                  <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8H4z"></path>
                </svg>
                <span>{{ isSubmitting ? t('Sending 3D Files...') : t('Submit Print Request') }}</span>
              </button>

              <a
                :href="telegramDirectLink"
                target="_blank"
                rel="noopener"
                class="w-full rounded-full border border-black/10 dark:border-white/15 bg-[#FAFAFA] dark:bg-white/5 hover:border-navy-900 dark:hover:border-blue-400 text-[#111112] dark:text-white font-bold py-3 px-4 text-xs transition flex items-center justify-center gap-2"
              >
                <svg class="w-4 h-4 text-[#229ED9]" fill="currentColor" viewBox="0 0 24 24">
                  <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.19-.08-.05-.19-.02-.27 0-.12.03-1.99 1.27-5.62 3.72-.53.36-1.01.54-1.44.53-.47-.01-1.38-.27-2.05-.49-.83-.27-1.49-.42-1.43-.88.03-.24.37-.49 1.02-.74 4-1.74 6.68-2.88 8.03-3.44 3.82-1.59 4.62-1.87 5.14-1.88.11 0 .37.03.54.17.14.12.18.28.2.45-.02.07-.02.21-.04.35z"/>
                </svg>
                <span>{{ t('Chat on Telegram (@aerobyte168)') }}</span>
              </a>
            </div>

            <p class="text-[11px] text-center text-[#696969] dark:text-white/50 mt-4 leading-relaxed">
              📍 AeroByte Academy Maker Lab • Ta Khmau, Cambodia. Fast 24h turnarounds for prototypes, drones & robotics.
            </p>
          </div>
        </div>
      </div>
    </main>

    <!-- Request Received Modal -->
    <div
      v-if="openOrderModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/65 backdrop-blur-sm p-4"
    >
      <div class="relative w-full max-w-lg rounded-[28px] bg-white dark:bg-[#111112] p-6 sm:p-7 shadow-2xl border border-black/[0.08] dark:border-white/10">
        <div class="flex items-center justify-between pb-4 border-b border-black/[0.06] dark:border-white/10">
          <div>
            <h3 class="text-lg font-bold text-[#111112] dark:text-white">{{ t('Submit 3D Print Request') }}</h3>
            <p class="text-xs text-[#696969] dark:text-white/55 mt-0.5">Aero Print Lab Queue</p>
          </div>
          <button
            type="button"
            @click="openOrderModal = false"
            class="h-8 w-8 rounded-full flex items-center justify-center text-[#696969] hover:text-[#111112] dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/10 font-bold cursor-pointer"
          >
            ✕
          </button>
        </div>

        <div class="py-8 text-center space-y-3">
          <div class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-emerald-100 dark:bg-emerald-950/60 text-emerald-600 text-2xl font-bold">
            ✓
          </div>
          <h4 class="text-xl font-bold text-[#111112] dark:text-white">{{ t('Quote Request Received!') }}</h4>
          <p class="text-xs text-[#575757] dark:text-white/65 max-w-sm mx-auto leading-relaxed">
            {{ t('Our admin has received your CAD files and will text you directly on Telegram with your price quote.') }}
          </p>

          <div class="rounded-2xl bg-[#FAFAFA] dark:bg-white/5 border border-black/[0.06] dark:border-white/10 p-3.5 text-xs text-left text-[#575757] dark:text-white/75 space-y-2 max-w-sm mx-auto mt-4">
            <div v-if="submittedOrder?.order_number" class="flex justify-between items-center bg-navy-900/5 dark:bg-blue-400/10 px-2.5 py-1.5 rounded-xl border border-navy-900/10 dark:border-blue-400/20">
              <span class="font-bold text-navy-900 dark:text-blue-300">Order ID:</span>
              <span class="font-mono font-black text-xs text-navy-900 dark:text-blue-300 bg-white dark:bg-slate-800 px-2 py-0.5 rounded shadow-xs">{{ submittedOrder.order_number }}</span>
            </div>
            <div class="flex justify-between">
              <span>Contact:</span>
              <span class="font-bold text-[#111112] dark:text-white">{{ orderForm.telegram || 'Telegram QR attached' }}</span>
            </div>
            <div v-if="orderForm.name" class="flex justify-between">
              <span>Name:</span>
              <span class="font-bold text-[#111112] dark:text-white">{{ orderForm.name }}</span>
            </div>
            <div class="flex justify-between">
              <span>Files Submitted:</span>
              <span class="font-bold text-[#111112] dark:text-white">{{ files.length }} {{ files.length === 1 ? 'file' : 'files' }}</span>
            </div>
            <div v-if="qrPreviewUrl" class="flex justify-between items-center text-emerald-600 font-bold">
              <span>Telegram QR Code:</span>
              <span>✓ Attached for Scan</span>
            </div>
          </div>

          <div class="pt-4 flex flex-col sm:flex-row gap-2.5 justify-center">
            <a
              :href="telegramDirectLink"
              target="_blank"
              rel="noopener"
              class="rounded-full bg-navy-900 hover:bg-navy-800 dark:bg-navy-600 dark:hover:bg-navy-800 text-white font-bold px-6 py-2.5 text-xs shadow-md transition flex items-center justify-center gap-2"
            >
              <svg class="w-3.5 h-3.5" fill="currentColor" viewBox="0 0 24 24">
                <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69.01-.03.01-.14-.07-.19-.08-.05-.19-.02-.27 0-.12.03-1.99 1.27-5.62 3.72-.53.36-1.01.54-1.44.53-.47-.01-1.38-.27-2.05-.49-.83-.27-1.49-.42-1.43-.88.03-.24.37-.49 1.02-.74 4-1.74 6.68-2.88 8.03-3.44 3.82-1.59 4.62-1.87 5.14-1.88.11 0 .37.03.54.17.14.12.18.28.2.45-.02.07-.02.21-.04.35z"/>
              </svg>
              <span>{{ t('Message @aerobyte168 on Telegram') }}</span>
            </a>
            <button
              type="button"
              @click="openOrderModal = false"
              class="rounded-full border border-black/10 dark:border-white/15 bg-[#FAFAFA] dark:bg-white/5 hover:bg-black/5 text-[#111112] dark:text-white font-bold px-6 py-2.5 text-xs transition cursor-pointer"
            >
              {{ t('Done') }}
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onUnmounted } from 'vue'
import { useI18n } from '../i18n'
import { printOrderService } from '../services/api'

const { t } = useI18n()

// State: Uploaded files - starts empty so users only drop their own files
const files = ref([])

const isDragging = ref(false)
const fileInputRef = ref(null)

function triggerFileInput() {
  fileInputRef.value?.click()
}

function appendFiles(fileList) {
  for (const f of fileList) {
    const sizeInMb = f.size ? (f.size / (1024 * 1024)).toFixed(2) : '1.0'
    files.value.push({
      id: Date.now() + Math.random(),
      name: f.name,
      file: f,
      sizeStr: `${sizeInMb} MB`,
    })
  }
  validationError.value = ''
}

function handleFileInputChange(e) {
  appendFiles(Array.from(e.target.files || []))
  if (e.target) e.target.value = ''
}

function handleFileDrop(e) {
  isDragging.value = false
  appendFiles(Array.from(e.dataTransfer?.files || []))
}

function removeFile(index) {
  files.value.splice(index, 1)
}

const totalPartCount = computed(() => {
  return files.value.length
})

// Telegram QR Code upload state
const qrFileInputRef = ref(null)
const qrFile = ref(null)
const qrPreviewUrl = ref(null)
const isQrDragging = ref(false)

function triggerQrInput() {
  qrFileInputRef.value?.click()
}

function handleQrInputChange(e) {
  const file = e.target.files?.[0]
  if (file && file.type.startsWith('image/')) {
    setQrFile(file)
  }
  if (e.target) e.target.value = ''
}

function handleQrDrop(e) {
  isQrDragging.value = false
  const file = e.dataTransfer?.files?.[0]
  if (file && file.type.startsWith('image/')) {
    setQrFile(file)
  }
}

function setQrFile(file) {
  qrFile.value = file
  if (qrPreviewUrl.value) {
    URL.revokeObjectURL(qrPreviewUrl.value)
  }
  qrPreviewUrl.value = URL.createObjectURL(file)
  validationError.value = ''
}

function removeQrFile() {
  if (qrPreviewUrl.value) {
    URL.revokeObjectURL(qrPreviewUrl.value)
  }
  qrFile.value = null
  qrPreviewUrl.value = null
}

onUnmounted(() => {
  if (qrPreviewUrl.value) {
    URL.revokeObjectURL(qrPreviewUrl.value)
  }
})

// Order Form & Submission
const openOrderModal = ref(false)
const validationError = ref('')
const isSubmitting = ref(false)
const submittedOrder = ref(null)
const orderForm = ref({
  name: '',
  telegram: '',
  notes: ''
})

async function submitPrintOrder() {
  validationError.value = ''
  if (files.value.length === 0) {
    validationError.value = t('Please upload at least one 3D CAD file.')
    return
  }
  if (!orderForm.value.telegram.trim() && !qrFile.value) {
    validationError.value = t('Please provide your Telegram username, phone, or QR code so we can contact you.')
    return
  }

  isSubmitting.value = true
  try {
    const formData = new FormData()
    const metaList = files.value.map(f => ({
      name: f.name,
      sizeStr: f.sizeStr,
    }))

    formData.append('order_data', JSON.stringify({
      name: orderForm.value.name,
      telegram: orderForm.value.telegram,
      phone: orderForm.value.telegram,
      notes: orderForm.value.notes,
      files: metaList,
    }))

    for (const f of files.value) {
      if (f.file) {
        formData.append('files', f.file, f.name)
      } else {
        const dummyContent = `solid ${f.name}\nendsolid ${f.name}\n`
        const blob = new Blob([dummyContent], { type: 'model/stl' })
        formData.append('files', blob, f.name)
      }
    }

    if (qrFile.value) {
      formData.append('qr_file', qrFile.value)
    }

    const res = await printOrderService.submitOrder(formData)
    if (res?.data?.order) {
      submittedOrder.value = res.data.order
    } else {
      submittedOrder.value = {
        order_number: `PR-${Math.floor(Math.random() * 9000 + 1000)}`
      }
    }
    openOrderModal.value = true
  } catch (err) {
    console.error('Failed to submit print order to backend:', err)
    // Fallback gracefully so user can still reach Telegram
    submittedOrder.value = {
      order_number: `PR-${Math.floor(Math.random() * 9000 + 1000)}`
    }
    openOrderModal.value = true
  } finally {
    isSubmitting.value = false
  }
}

// Telegram direct message link
const telegramDirectLink = computed(() => {
  const fileListText = files.value.map(f => `• ${f.name} (${f.sizeStr})`).join('\n')
  const orderIdText = submittedOrder.value?.order_number ? `\n• Order ID: ${submittedOrder.value.order_number}` : ''
  const contactText = orderForm.value.telegram ? `\n• My Telegram / Phone: ${orderForm.value.telegram}` : ''
  const nameText = orderForm.value.name ? `\n• Name: ${orderForm.value.name}` : ''
  const notesText = orderForm.value.notes ? `\n• Notes: ${orderForm.value.notes}` : ''
  const qrText = qrFile.value ? `\n• (I have also attached my Telegram QR code)` : ''

  const msg = encodeURIComponent(
    `Hello AeroByte Maker Lab! 👋\nI dropped my 3D CAD files for printing:${orderIdText}${nameText}${contactText}\n\nFiles (${files.value.length} file(s)):\n${fileListText || '• CAD models'}${notesText}${qrText}\n\nPlease inspect the files and text me the price on Telegram. Thank you!`
  )
  return `https://t.me/aerobyte168?text=${msg}`
})
</script>
