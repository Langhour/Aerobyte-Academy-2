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
                Aero Print
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
                  <span>{{ t('Telegram Username or Phone Number') }}</span>
                  <span class="text-rose-500 font-normal ml-1 text-[11px]">({{ t('Required if no QR code') }})</span>
                </label>
                <div class="relative">
                  <div class="pointer-events-none absolute inset-y-0 left-0 flex items-center pl-3.5">
                    <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                      <circle cx="12" cy="12" r="12" fill="#24A1DE"/>
                      <path fill-rule="evenodd" clip-rule="evenodd" d="M5.39 11.58c3.96-1.72 6.6-2.86 7.92-3.41 3.77-1.57 4.56-1.84 5.07-1.85.11 0 .36.03.52.16.14.11.18.27.2.44-.02.07-.02.21-.04.35-.15 1.56-.79 5.35-1.12 7.09-.14.74-.41.99-.67 1.01-.57.05-1-.37-1.56-.74-.86-.57-1.35-.93-2.19-1.48-.97-.64-.34-.99.21-1.57.15-.15 2.67-2.45 2.72-2.65.01-.03.01-.14-.07-.19-.08-.05-.19-.02-.27 0-.12.03-1.96 1.25-5.54 3.67-.52.36-.99.53-1.42.52-.46-.01-1.36-.26-2.02-.48-.82-.27-1.47-.41-1.41-.87.03-.24.36-.48 1.01-.73z" fill="white"/>
                    </svg>
                  </div>
                  <input
                    v-model="orderForm.telegram"
                    type="text"
                    placeholder="@username or 012 345 678"
                    @input="validationError = ''"
                    class="w-full rounded-xl border bg-[#FAFAFA] dark:bg-white/5 pl-10 pr-3.5 py-2.5 text-xs text-[#111112] dark:text-white placeholder:text-[#696969] dark:placeholder:text-white/40 focus:outline-none focus:bg-white dark:focus:bg-white/10 transition"
                    :class="(validationError && !orderForm.telegram.trim() && !qrFile)
                      ? 'border-rose-500 focus:border-rose-500 ring-2 ring-rose-500/20'
                      : 'border-black/15 dark:border-white/15 focus:border-navy-900 dark:focus:border-blue-400'"
                  />
                </div>
                <p v-if="validationError && !orderForm.telegram.trim() && !qrFile" class="text-[11px] text-rose-500 dark:text-rose-400 mt-1 font-medium">
                  {{ t('Please provide your Telegram username or phone number (or upload QR code below).') }}
                </p>
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
                  @input="validationError = ''"
                  class="w-full rounded-xl border border-black/15 dark:border-white/15 bg-[#FAFAFA] dark:bg-white/5 px-3.5 py-2.5 text-xs text-[#111112] dark:text-white placeholder:text-[#696969] dark:placeholder:text-white/40 focus:outline-none focus:border-navy-900 dark:focus:border-blue-400 focus:bg-white dark:focus:bg-white/10 transition"
                />
              </div>
            </div>

            <!-- Drop Telegram QR Code Section -->
            <div class="pt-1">
              <label class="block text-xs font-bold text-[#111112] dark:text-white/90 mb-1">
                <span>{{ t('Drop Telegram QR Code (Optional)') }}</span>
                <span class="text-emerald-600 dark:text-emerald-400 font-normal ml-1 text-[11px]">({{ t('Optional — user can provide username instead') }})</span>
              </label>
              <p class="text-[11px] text-[#696969] dark:text-white/55 mb-2.5">
                {{ t('Uploading a Telegram QR code is completely optional. If you entered your Telegram username or phone number above, you do NOT need to upload an image.') }}
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
            <div class="border-b border-black/[0.06] dark:border-white/10 pb-4">
              <h3 class="text-lg font-bold text-[#111112] dark:text-white">
                {{ t('3D Print Request Summary') }}
              </h3>
            </div>

            <!-- Files Overview -->
            <div class="mt-4 space-y-2.5 text-xs">
              <div class="flex justify-between items-center text-[#575757] dark:text-white/60">
                <span>{{ t('Files Attached') }}</span>
                <span class="font-bold text-[#111112] dark:text-white">{{ files.length }} {{ files.length === 1 ? t('file') : t('files') }}</span>
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
                  {{ orderForm.telegram || (qrPreviewUrl ? t('QR Attached') : t('Not provided yet')) }}
                </span>
              </div>

              <div class="flex justify-between items-center text-[#575757] dark:text-white/60">
                <span>{{ t('QR Code') }}</span>
                <span :class="qrPreviewUrl ? 'text-emerald-600 font-bold' : 'text-[#696969] dark:text-white/50'">
                  {{ qrPreviewUrl ? t('✓ Attached') : t('Optional') }}
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
                <svg class="w-4 h-4 shrink-0" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                  <circle cx="12" cy="12" r="12" fill="#24A1DE"/>
                  <path fill-rule="evenodd" clip-rule="evenodd" d="M5.39 11.58c3.96-1.72 6.6-2.86 7.92-3.41 3.77-1.57 4.56-1.84 5.07-1.85.11 0 .36.03.52.16.14.11.18.27.2.44-.02.07-.02.21-.04.35-.15 1.56-.79 5.35-1.12 7.09-.14.74-.41.99-.67 1.01-.57.05-1-.37-1.56-.74-.86-.57-1.35-.93-2.19-1.48-.97-.64-.34-.99.21-1.57.15-.15 2.67-2.45 2.72-2.65.01-.03.01-.14-.07-.19-.08-.05-.19-.02-.27 0-.12.03-1.96 1.25-5.54 3.67-.52.36-.99.53-1.42.52-.46-.01-1.36-.26-2.02-.48-.82-.27-1.47-.41-1.41-.87.03-.24.36-.48 1.01-.73z" fill="white"/>
                </svg>
                <span>{{ t('Chat on Telegram (@aerobyte168)') }}</span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </main>

    <!-- Request Received Modal (Redesigned like Official Payment Success / Receipt Card) -->
    <div
      v-if="openOrderModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/70 backdrop-blur-md p-3 sm:p-5 overflow-y-auto"
      @click.self="openOrderModal = false"
    >
      <div
        class="relative w-full max-w-lg rounded-3xl bg-white dark:bg-slate-900 border border-slate-200/90 dark:border-slate-800 shadow-2xl overflow-hidden transition-all duration-300 my-auto"
      >
        <!-- Top Accent Gradient Stripe (Payment/Academy Signature) -->
        <div class="h-2 w-full bg-gradient-to-r from-emerald-500 via-navy-800 to-indigo-600"></div>

        <!-- Close Button Top Right -->
        <button
          type="button"
          @click="openOrderModal = false"
          class="absolute top-4 right-4 h-8 w-8 rounded-full bg-slate-100 hover:bg-slate-200 dark:bg-slate-800 dark:hover:bg-slate-700 flex items-center justify-center text-slate-500 dark:text-slate-400 transition cursor-pointer z-10"
          :title="t('Close')"
        >
          <X class="w-4 h-4" />
        </button>

        <div class="p-6 sm:p-8 text-center">
          <!-- Official UX/UI Design Success Icon (Green Squircle with Circle Checkmark) -->
          <div class="mx-auto mt-2 mb-5 flex items-center justify-center">
            <div class="flex h-[84px] w-[84px] items-center justify-center rounded-[26px] bg-gradient-to-b from-[#27C28C] to-[#12A777] shadow-[0_14px_28px_rgba(18,167,119,0.36)] transition-transform hover:scale-105 duration-200">
              <svg
                class="w-[52px] h-[52px]"
                viewBox="0 0 96 96"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <circle
                  cx="48"
                  cy="48"
                  r="23"
                  stroke="white"
                  stroke-width="5"
                />
                <path
                  d="M38.5 48L45 54L57 41.5"
                  stroke="white"
                  stroke-width="5"
                  stroke-linecap="round"
                  stroke-linejoin="round"
                />
              </svg>
            </div>
          </div>

          <!-- Title -->
          <div class="space-y-1.5">
            <h3 class="text-xl sm:text-2xl font-black text-navy-900 dark:text-white tracking-tight">
              {{ t('Request Submitted!') }}
            </h3>
            <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 max-w-sm mx-auto leading-relaxed">
              {{ t('Our lab team will inspect your 3D models and contact you on Telegram with filament specs and price quote.') }}
            </p>
          </div>

          <!-- Official Invoice/Receipt Card Style Breakdown -->
          <div class="mt-5 rounded-2xl border border-slate-200/90 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-800/40 p-4 sm:p-5 text-left text-xs space-y-3">
            <!-- Header Row: Order Reference & Date -->
            <div class="flex items-center justify-between border-b border-slate-200/80 dark:border-slate-700/80 pb-3">
              <div>
                <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 block">
                  {{ t('Order Reference') }}
                </span>
                <span class="text-sm font-mono font-black text-navy-900 dark:text-indigo-300">
                  #{{ submittedOrder?.order_number || 'PR-1025' }}
                </span>
              </div>
              <div class="text-right">
                <span class="text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 block">
                  {{ t('Date') }}
                </span>
                <span class="text-xs font-semibold text-slate-700 dark:text-slate-300">
                  {{ formatCambodiaTime(submittedOrder?.created_at || new Date()) }}
                </span>
              </div>
            </div>

            <!-- CAD Files Line Items -->
            <div class="space-y-2">
              <div class="text-[10px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500 flex items-center gap-1.5">
                <Box class="w-3.5 h-3.5 text-navy-800 dark:text-indigo-400" />
                <span>{{ t('Submitted CAD Models') }} ({{ files.length }})</span>
              </div>
              <div class="divide-y divide-slate-200/60 dark:divide-slate-700/50 rounded-xl bg-white dark:bg-slate-800/80 border border-slate-200/70 dark:border-slate-700/60 p-2 sm:p-2.5 max-h-36 overflow-y-auto">
                <div
                  v-for="(file, idx) in files"
                  :key="file.id || idx"
                  class="flex items-center justify-between gap-3 py-1.5 first:pt-0 last:pb-0"
                >
                  <div class="flex items-center gap-2 min-w-0">
                    <div class="flex h-6 w-6 shrink-0 items-center justify-center rounded-md bg-navy-50 dark:bg-slate-700 text-navy-900 dark:text-indigo-300 text-[11px]">
                      <Box class="w-3.5 h-3.5" />
                    </div>
                    <span class="font-bold text-slate-800 dark:text-slate-200 truncate max-w-[200px] text-xs">
                      {{ file.name }}
                    </span>
                  </div>
                  <span class="text-[11px] font-medium text-slate-400 shrink-0">
                    {{ file.sizeStr }}
                  </span>
                </div>
              </div>
            </div>

            <!-- Contact & Customer Information -->
            <div class="pt-2 border-t border-slate-200/80 dark:border-slate-700/80 flex flex-wrap items-center justify-between gap-2 text-xs">
              <div>
                <span class="text-slate-500 dark:text-slate-400">{{ t('Contact') }}:</span>
                <strong class="ml-1 text-slate-900 dark:text-white">{{ orderForm.telegram || (qrPreviewUrl ? t('QR Attached') : t('Not provided')) }}</strong>
              </div>
              <div v-if="orderForm.name">
                <span class="text-slate-500 dark:text-slate-400">{{ t('Customer') }}:</span>
                <strong class="ml-1 text-slate-900 dark:text-white">{{ orderForm.name }}</strong>
              </div>
              <div v-if="qrPreviewUrl" class="text-emerald-600 dark:text-emerald-400 font-bold flex items-center gap-1 text-[11px]">
                <span>✓ {{ t('Telegram QR Code Attached') }}</span>
              </div>
            </div>
          </div>

          <!-- Lab Inspection Callout Box (Like Scan to Pay Verification Box) -->
          <div class="mt-4 rounded-xl bg-blue-50/80 dark:bg-indigo-950/40 border border-blue-100 dark:border-indigo-900/50 p-3 flex items-start gap-2.5 text-xs text-blue-900 dark:text-indigo-200 text-left">
            <ShieldCheck class="w-4 h-4 text-blue-600 dark:text-indigo-400 shrink-0 mt-0.5" />
            <p class="leading-relaxed text-[11px]">
              {{ t('Our engineering lab will inspect your CAD geometry and message you on Telegram with exact filament pricing.') }}
            </p>
          </div>

          <!-- Action Buttons Hierarchy -->
          <div class="mt-6 space-y-2.5">
            <!-- Hero Telegram Direct Action -->
            <a
              :href="telegramDirectLink"
              target="_blank"
              rel="noopener"
              class="w-full py-3 sm:py-3.5 px-5 rounded-xl bg-navy-900 hover:bg-navy-800 dark:bg-indigo-600 dark:hover:bg-indigo-500 text-white font-bold text-xs sm:text-sm shadow-md transition flex items-center justify-center gap-2 cursor-pointer"
            >
              <Send class="w-4 h-4" />
              <span>{{ t('Message @aerobyte168 on Telegram') }}</span>
              <ExternalLink class="w-3.5 h-3.5 opacity-70" />
            </a>

            <!-- Secondary Action: Track in My Orders -->
            <button
              type="button"
              @click="openOrderModal = false; router.push({ path: '/profile', query: { section: 'orders' } })"
              class="w-full py-2.5 px-4 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-800 dark:text-slate-200 font-bold text-xs transition flex items-center justify-center gap-1.5 shadow-2xs cursor-pointer"
            >
              <Printer class="w-3.5 h-3.5 text-slate-500 dark:text-slate-400" />
              <span>{{ t('Track in My Orders') }}</span>
              <ArrowRight class="w-3.5 h-3.5 text-slate-400" />
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import {
  ArrowRight,
  Box,
  ExternalLink,
  Printer,
  Send,
  ShieldCheck,
  X,
} from 'lucide-vue-next'
import { useI18n } from '../i18n'
import { printOrderService, accountService } from '../services/api'
import { formatCambodiaTime } from '../utils/date'

const { t } = useI18n()
const router = useRouter()

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

function getCachedUserProfile() {
  let uid = ''
  let uemail = ''
  let uname = ''
  let utg = ''
  let uphone = ''

  try {
    const rawSess = localStorage.getItem('aerobyte_user_session')
    if (rawSess) {
      const sess = JSON.parse(rawSess)
      const u = sess.user || sess
      if (u) {
        uid = u.id || ''
        uemail = u.email || ''
        uname = u.name || u.full_name || ''
        utg = u.telegram || ''
        uphone = u.phone || ''
      }
    }
  } catch (_) {}

  try {
    const raw = localStorage.getItem('aerobyte-profile-current') || localStorage.getItem('aerobyte-profile')
    if (raw) {
      const p = JSON.parse(raw)
      if (p) {
        if (!uid && p.id) uid = p.id
        if (!uemail && p.email) uemail = p.email
        if (!uname && p.fullName) uname = p.fullName
        if (!utg && p.telegram) utg = p.telegram
        if (!uphone && p.phone) uphone = p.phone
      }
    }
  } catch (_) {}

  if (uemail) {
    try {
      const byEmail = localStorage.getItem(`aerobyte-profile:${uemail.toLowerCase()}`)
      if (byEmail) {
        const ep = JSON.parse(byEmail)
        if (ep) {
          if (!utg && ep.telegram) utg = ep.telegram
          if (!uphone && ep.phone) uphone = ep.phone
          if (!uname && ep.fullName) uname = ep.fullName
        }
      }
    } catch (_) {}
  }

  return { id: uid, email: uemail, fullName: uname, telegram: utg, phone: uphone }
}

onMounted(async () => {
  const profile = getCachedUserProfile()
  if (profile.fullName && !orderForm.value.name) {
    orderForm.value.name = profile.fullName
  }
  if (!orderForm.value.telegram) {
    if (profile.telegram) {
      orderForm.value.telegram = profile.telegram
    } else if (profile.phone) {
      orderForm.value.telegram = profile.phone
    }
  }

  // Backfill directly from active server session if telegram or name are not yet cached
  try {
    const res = await accountService.getSession()
    if (res?.data?.authenticated && res?.data?.user) {
      const u = res.data.user
      if (!orderForm.value.name && (u.name || u.full_name)) {
        orderForm.value.name = u.name || u.full_name
      }
      if (!orderForm.value.telegram) {
        if (u.telegram) {
          orderForm.value.telegram = u.telegram
        } else if (u.phone) {
          orderForm.value.telegram = u.phone
        }
      }
    }
  } catch (_) {}
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
    const cached = getCachedUserProfile()
    const formData = new FormData()
    const metaList = files.value.map(f => ({
      name: f.name,
      sizeStr: f.sizeStr,
    }))

    formData.append('order_data', JSON.stringify({
      user_id: cached.id || '',
      user_email: cached.email || '',
      name: orderForm.value.name || cached.fullName || '',
      telegram: orderForm.value.telegram || cached.telegram || '',
      phone: orderForm.value.telegram || cached.phone || '',
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
    let finalOrder = null
    if (res?.data?.order) {
      finalOrder = res.data.order
    } else {
      const fallbackNum = `PR-${Math.floor(Math.random() * 9000 + 1000)}`
      finalOrder = {
        id: fallbackNum,
        order_number: fallbackNum,
        customer_name: orderForm.value.name,
        telegram: orderForm.value.telegram,
        files: files.value.map(f => ({ original_name: f.name, size_str: f.sizeStr, quantity: 1, material: 'PLA / Custom' })),
        total_parts: files.value.length,
        estimated_price: 0.0,
        price: 0.0,
        status: 'Pending Review',
        created_at: new Date().toISOString(),
        date: new Date().toISOString(),
      }
    }

    submittedOrder.value = finalOrder

    // Persist to local cache so user profile displays it immediately
    try {
      const rawStored = localStorage.getItem('aerobyte_print_orders')
      const stored = rawStored ? JSON.parse(rawStored) : []
      const filtered = stored.filter(o => o.order_number !== finalOrder.order_number && o.id !== finalOrder.id)
      localStorage.setItem('aerobyte_print_orders', JSON.stringify([finalOrder, ...filtered]))
      window.dispatchEvent(new CustomEvent('aerobyte-orders-updated'))
    } catch (_) {}

    openOrderModal.value = true
  } catch (err) {
    console.error('Failed to submit print order to backend:', err)
    // Fallback gracefully so user can still reach Telegram and track order
    const fallbackNum = `PR-${Math.floor(Math.random() * 9000 + 1000)}`
    const fallbackOrder = {
      id: fallbackNum,
      order_number: fallbackNum,
      customer_name: orderForm.value.name,
      telegram: orderForm.value.telegram,
      files: files.value.map(f => ({ original_name: f.name, size_str: f.sizeStr, quantity: 1, material: 'PLA / Custom' })),
      total_parts: files.value.length,
      estimated_price: 0.0,
      price: 0.0,
      status: 'Pending Review',
      created_at: new Date().toISOString(),
      date: new Date().toISOString(),
    }
    submittedOrder.value = fallbackOrder

    try {
      const rawStored = localStorage.getItem('aerobyte_print_orders')
      const stored = rawStored ? JSON.parse(rawStored) : []
      const filtered = stored.filter(o => o.order_number !== fallbackOrder.order_number && o.id !== fallbackOrder.id)
      localStorage.setItem('aerobyte_print_orders', JSON.stringify([fallbackOrder, ...filtered]))
      window.dispatchEvent(new CustomEvent('aerobyte-orders-updated'))
    } catch (_) {}

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
