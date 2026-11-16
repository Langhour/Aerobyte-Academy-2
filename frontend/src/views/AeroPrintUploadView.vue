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
              {{ t('Drop your CAD files and your Telegram contact. Our lab engineers will inspect your models and message you the custom price quote.') }}
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

            <!-- Sample Presets Bar -->
            <div class="mt-5 flex flex-col sm:flex-row sm:items-center justify-between gap-2.5 rounded-2xl border border-black/[0.05] dark:border-white/10 bg-[#FAFAFA] dark:bg-white/[0.03] px-4 py-3">
              <span class="text-xs font-medium text-[#575757] dark:text-white/70">
                {{ t('No CAD file ready? Test instant quoting with a sample part:') }}
              </span>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="sample in sampleModels"
                  :key="sample.id"
                  type="button"
                  @click="loadSampleModel(sample)"
                  class="inline-flex items-center gap-1.5 rounded-full border border-black/[0.08] dark:border-white/15 bg-white dark:bg-white/5 px-3 py-1.5 text-xs font-semibold text-[#111112] dark:text-white hover:border-navy-900 hover:text-navy-900 dark:hover:border-blue-400 dark:hover:text-blue-300 transition cursor-pointer"
                >
                  <svg class="w-3.5 h-3.5 text-[#575757] dark:text-white/65" fill="none" viewBox="0 0 24 24" stroke="currentColor" stroke-width="1.8">
                    <path stroke-linecap="round" stroke-linejoin="round" d="M21 7.5l-9-5.25L3 7.5m18 0l-9 5.25m9-5.25v9l-9 5.25M3 7.5l9 5.25M3 7.5v9l9 5.25m0-9v9" />
                  </svg>
                  <span>{{ sample.name }}</span>
                </button>
              </div>
            </div>

            <!-- Uploaded Files List -->
            <div v-if="files.length > 0" class="mt-5 space-y-3">
              <div
                v-for="(f, idx) in files"
                :key="f.id"
                class="rounded-2xl border border-black/[0.07] dark:border-white/10 bg-[#FAFAFA] dark:bg-white/[0.03] p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3"
              >
                <div class="flex items-center gap-3.5 min-w-0">
                  <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-xl bg-navy-900/10 dark:bg-blue-400/15 text-navy-900 dark:text-blue-300 font-bold text-xs uppercase">
                    3D
                  </div>
                  <div class="min-w-0">
                    <p class="truncate text-xs sm:text-sm font-bold text-[#111112] dark:text-white">{{ f.name }}</p>
                    <p class="text-[11px] text-[#696969] dark:text-white/55">
                      {{ f.sizeStr }} • {{ f.dimensions.x }}×{{ f.dimensions.y }}×{{ f.dimensions.z }} mm • {{ t('Est. Vol') }}: {{ f.volumeCm3 }} cm³
                    </p>
                  </div>
                </div>

                <!-- Quantity Counter & Delete -->
                <div class="flex items-center gap-3 self-end sm:self-auto shrink-0">
                  <div class="flex items-center border border-black/[0.08] dark:border-white/15 bg-white dark:bg-[#18181B] rounded-full overflow-hidden">
                    <button
                      type="button"
                      @click="decreaseQty(idx)"
                      class="px-3 py-1 text-[#575757] dark:text-white/75 hover:bg-black/5 dark:hover:bg-white/10 text-sm font-bold cursor-pointer"
                    >
                      −
                    </button>
                    <span class="px-3 py-1 text-xs font-bold text-[#111112] dark:text-white min-w-[2rem] text-center">
                      {{ f.quantity }}
                    </span>
                    <button
                      type="button"
                      @click="increaseQty(idx)"
                      class="px-3 py-1 text-[#575757] dark:text-white/75 hover:bg-black/5 dark:hover:bg-white/10 text-sm font-bold cursor-pointer"
                    >
                      +
                    </button>
                  </div>

                  <button
                    type="button"
                    @click="removeFile(idx)"
                    class="text-xs text-rose-500 hover:text-rose-600 font-semibold px-2.5 py-1.5 hover:bg-rose-50 dark:hover:bg-rose-950/30 rounded-full cursor-pointer transition"
                  >
                    {{ t('Delete') }}
                  </button>
                </div>
              </div>
            </div>

            <!-- Empty file warning if any -->
            <div v-else class="mt-4 rounded-xl border border-dashed border-black/10 dark:border-white/10 p-4 text-center text-xs text-[#696969] dark:text-white/50">
              {{ t('No CAD files uploaded yet. Select files or click a sample part above.') }}
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
                  {{ t('Your Telegram Contact & Details') }}
                </h2>
                <p class="text-xs text-[#575757] dark:text-white/65 mt-0.5">
                  {{ t('Tell us how to reach you. We will inspect your 3D CAD files and message you our price quote directly on Telegram.') }}
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
                <span class="font-bold text-[#111112] dark:text-white">{{ files.length }} file(s) • {{ totalPartCount }} pcs</span>
              </div>

              <!-- Mini file list -->
              <div v-if="files.length > 0" class="space-y-1.5 pt-1">
                <div
                  v-for="f in files"
                  :key="f.id"
                  class="flex items-center justify-between rounded-lg bg-[#FAFAFA] dark:bg-white/[0.03] px-2.5 py-1.5 text-[11px]"
                >
                  <span class="truncate font-medium text-[#111112] dark:text-white max-w-[180px]">{{ f.name }}</span>
                  <span class="font-bold text-navy-900 dark:text-blue-300">×{{ f.quantity }}</span>
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
                  <path stroke-linecap="round" stroke-linejoin="round" d="M9.813 15.904L9 18.75l-.813-2.846a4.5 4.5 0 00-3.09-3.09L2.25 12l2.846-.813a4.5 4.5 0 003.09-3.09L9 5.25l.813 2.846a4.5 4.5 0 003.09 3.09L15.75 12l-2.846.813a4.5 4.5 0 00-3.09 3.09zM18.259 8.715L18 9.75l-.259-1.035a3.375 3.375 0 00-2.455-2.456L14.25 6l1.036-.259a3.375 3.375 0 002.455-2.456L18 2.25l.259 1.035a3.375 3.375 0 002.456 2.456L21.75 6l-1.035.259a3.375 3.375 0 00-2.456 2.456zM16.894 20.567L16.5 21.75l-.394-1.183a2.25 2.25 0 00-1.423-1.423L13.5 18.75l1.183-.394a2.25 2.25 0 001.423-1.423l.394-1.183.394 1.183a2.25 2.25 0 001.423 1.423l1.183.394-1.183.394a2.25 2.25 0 00-1.423 1.423z" />
                </svg>
                <span>How You Get Your Price</span>
              </p>
              <ul class="text-[11px] text-[#575757] dark:text-white/65 space-y-1.5 leading-relaxed">
                <li>• <strong>1. Drop 3D file & contact:</strong> Submit your CAD files and your Telegram info.</li>
                <li>• <strong>2. Lab inspection:</strong> Engineers slice the geometry & verify wall thickness.</li>
                <li>• <strong>3. Custom quote:</strong> We message your Telegram directly with exact price and delivery time.</li>
              </ul>
            </div>

            <!-- Action Buttons -->
            <div class="mt-6 space-y-3">
              <button
                type="button"
                @click="submitPrintOrder"
                class="w-full rounded-full bg-navy-900 hover:bg-navy-800 dark:bg-navy-600 dark:hover:bg-navy-800 text-white font-bold py-3.5 px-5 text-sm shadow-[0_10px_25px_rgba(16,42,73,0.3)] active:scale-[0.99] transition flex items-center justify-center gap-2 cursor-pointer"
              >
                <span>{{ t('Submit Print Request') }}</span>
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
                <span>{{ t('Chat Directly on Telegram') }}</span>
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
            {{ t('Our Aero Print lab engineers will inspect your 3D files and contact you on Telegram within 2 hours with your custom price and print timeline.') }}
          </p>

          <div class="rounded-2xl bg-[#FAFAFA] dark:bg-white/5 border border-black/[0.06] dark:border-white/10 p-3.5 text-xs text-left text-[#575757] dark:text-white/75 space-y-1.5 max-w-sm mx-auto mt-4">
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
              <span class="font-bold text-[#111112] dark:text-white">{{ files.length }} file(s) ({{ totalPartCount }} parts)</span>
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
              <span>{{ t('Message Lab on Telegram') }}</span>
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

const { t } = useI18n()

// Sample presets for instant testing
const sampleModels = [
  { id: 'drone-mount', name: 'FPV Motor Mount', sizeStr: '1.2 MB', dimensions: { x: 45, y: 45, z: 12 }, volumeCm3: 14.5, quantity: 4 },
  { id: 'sensor-case', name: 'ESP32 Sensor Case', sizeStr: '2.8 MB', dimensions: { x: 75, y: 50, z: 24 }, volumeCm3: 32.0, quantity: 1 },
  { id: 'arm-gear', name: 'Robotic Servo Gear', sizeStr: '980 KB', dimensions: { x: 35, y: 35, z: 8 }, volumeCm3: 8.2, quantity: 2 },
]

// State: Uploaded files
const files = ref([
  {
    id: 1,
    name: 'Drone_Arm_V2_Reinforced.stl',
    sizeStr: '3.4 MB',
    dimensions: { x: 120, y: 35, z: 18 },
    volumeCm3: 28.5,
    quantity: 2,
  }
])

const isDragging = ref(false)
const fileInputRef = ref(null)

function triggerFileInput() {
  fileInputRef.value?.click()
}

function appendFiles(fileList) {
  for (const f of fileList) {
    files.value.push({
      id: Date.now() + Math.random(),
      name: f.name,
      sizeStr: `${Math.max(0.1, f.size / (1024 * 1024)).toFixed(1)} MB`,
      dimensions: {
        x: Math.floor(Math.random() * 80 + 30),
        y: Math.floor(Math.random() * 60 + 20),
        z: Math.floor(Math.random() * 40 + 10)
      },
      volumeCm3: parseFloat((Math.random() * 25 + 10).toFixed(1)),
      quantity: 1,
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

function loadSampleModel(sample) {
  files.value.push({
    id: Date.now() + Math.random(),
    name: `${sample.name}.stl`,
    sizeStr: sample.sizeStr,
    dimensions: { ...sample.dimensions },
    volumeCm3: sample.volumeCm3,
    quantity: sample.quantity,
  })
  validationError.value = ''
}

function increaseQty(index) {
  files.value[index].quantity++
}

function decreaseQty(index) {
  if (files.value[index].quantity > 1) {
    files.value[index].quantity--
  }
}

function removeFile(index) {
  files.value.splice(index, 1)
}

const totalPartCount = computed(() => {
  return files.value.reduce((acc, f) => acc + (f.quantity || 1), 0)
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
const orderForm = ref({
  name: '',
  telegram: '',
  notes: ''
})

function submitPrintOrder() {
  validationError.value = ''
  if (files.value.length === 0) {
    validationError.value = t('Please upload at least one 3D CAD file.')
    return
  }
  if (!orderForm.value.telegram.trim() && !qrFile.value) {
    validationError.value = t('Please provide your Telegram username, phone, or QR code so we can contact you.')
    return
  }
  openOrderModal.value = true
}

// Telegram direct message link
const telegramDirectLink = computed(() => {
  const fileListText = files.value.map(f => `• ${f.name} (Qty: ${f.quantity})`).join('\n')
  const contactText = orderForm.value.telegram ? `\nMy Telegram / Phone: ${orderForm.value.telegram}` : ''
  const nameText = orderForm.value.name ? `\nName: ${orderForm.value.name}` : ''
  const notesText = orderForm.value.notes ? `\nNotes: ${orderForm.value.notes}` : ''
  const qrText = qrFile.value ? `\n(I have also attached my Telegram QR code)` : ''

  const msg = encodeURIComponent(
    `Hello AeroByte Maker Lab! 👋\nI would like a 3D printing price quote for my CAD files:${nameText}${contactText}\n\nFiles (${totalPartCount.value} parts total):\n${fileListText || '• CAD models'}${notesText}${qrText}\n\nPlease inspect the slicing and tell me the price. Thank you!`
  )
  return `https://t.me/aerobyte?text=${msg}`
})
</script>
