<template>
  <div class="min-h-screen bg-slate-50 dark:bg-slate-950 pb-20 transition-colors">
    <!-- Top Hero / Banner -->
    <header class="border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 py-6 sm:py-8">
      <div class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
        <div class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div class="flex items-center gap-3.5">
            <div class="p-2 rounded-xl bg-navy-50 dark:bg-slate-800 border border-navy-100 dark:border-slate-700 shrink-0">
              <img
                src="/assets/brand/aero-print.png"
                alt="Aero Print Logo"
                class="h-10 sm:h-12 w-auto object-contain dark:invert"
              />
            </div>
            <div>
              <div class="flex items-center gap-2">
                <h1 class="text-xl sm:text-2xl font-black tracking-tight text-navy-900 dark:text-white">
                  Aero Print
                </h1>
                <span class="inline-flex items-center rounded-full bg-navy-50 dark:bg-slate-800 px-2.5 py-0.5 text-[11px] font-bold text-navy-900 dark:text-indigo-300">
                  Instant 3D Quote
                </span>
              </div>
              <p class="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-0.5">
                {{ t('Instant Online 3D Printing Quotation & Rapid Prototyping Service in Cambodia') }}
              </p>
            </div>
          </div>

          <!-- Quick Lab Status Badge -->
          <div class="flex items-center gap-2 self-start sm:self-auto rounded-xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 px-3 py-1.5 text-xs text-slate-600 dark:text-slate-300">
            <span class="relative flex h-2 w-2">
              <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
            <span class="font-semibold text-slate-700 dark:text-slate-200">Lab Status: Ready</span>
            <span class="text-slate-400">•</span>
            <span>24–48h Dispatch</span>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Quotation Tool Container (2-Column JLC3DP Style) -->
    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 mt-6 sm:mt-8">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 sm:gap-8 items-start">
        
        <!-- LEFT COLUMN: File Upload & Customization Options (8 Cols) -->
        <div class="lg:col-span-8 space-y-6">

          <!-- 1. 3D File Upload Area -->
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 sm:p-6 shadow-xs">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-2.5">
                <span class="flex h-7 w-7 items-center justify-center rounded-lg bg-navy-900 dark:bg-indigo-600 text-white font-bold text-xs">
                  1
                </span>
                <h2 class="text-base sm:text-lg font-bold text-navy-900 dark:text-white">
                  {{ t('Upload 3D CAD Files') }}
                </h2>
              </div>
              <span class="text-xs text-slate-400 dark:text-slate-500">.STL, .STP, .STEP, .OBJ, .3MF</span>
            </div>

            <!-- Drag & Drop Zone -->
            <div
              @dragover.prevent="isDragging = true"
              @dragleave.prevent="isDragging = false"
              @drop.prevent="handleFileDrop"
              class="relative rounded-xl border-2 border-dashed transition-all p-6 sm:p-8 text-center cursor-pointer"
              :class="isDragging
                ? 'border-navy-800 dark:border-indigo-500 bg-navy-50/50 dark:bg-slate-800/40'
                : 'border-slate-300 dark:border-slate-700 hover:border-navy-600 dark:hover:border-indigo-400 bg-slate-50/50 dark:bg-slate-800/40'"
              @click="triggerFileInput"
            >
              <input
                ref="fileInputRef"
                type="file"
                multiple
                accept=".stl,.stp,.step,.obj,.3mf"
                class="hidden"
                @change="handleFileInputChange"
              />

              <div class="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-indigo-300 mb-3 text-2xl">
                📁
              </div>
              <p class="text-sm sm:text-base font-bold text-navy-900 dark:text-white">
                Drag and drop your 3D models here, or <span class="text-navy-900 dark:text-indigo-400 underline font-semibold">browse files</span>
              </p>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-1.5">
                Max file size: 50MB per file. Multi-part assemblies supported.
              </p>
            </div>

            <!-- Demo Model Presets (Quick Test) -->
            <div class="mt-4 pt-4 border-t border-slate-100 dark:border-slate-800">
              <p class="text-xs font-semibold text-slate-500 dark:text-slate-400 mb-2.5">
                No 3D file yet? Try a sample model to test instant quote:
              </p>
              <div class="flex flex-wrap gap-2">
                <button
                  v-for="sample in sampleModels"
                  :key="sample.id"
                  type="button"
                  @click="loadSampleModel(sample)"
                  class="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-1.5 text-xs font-medium text-slate-700 dark:text-slate-200 hover:border-navy-600 hover:text-navy-900 dark:hover:text-indigo-300 transition cursor-pointer"
                >
                  <span>{{ sample.icon }}</span>
                  <span>{{ sample.name }}</span>
                </button>
              </div>
            </div>

            <!-- Uploaded Files List -->
            <div v-if="files.length > 0" class="mt-5 space-y-3">
              <div
                v-for="(f, idx) in files"
                :key="f.id"
                class="rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-3.5 sm:p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 shadow-xs"
              >
                <div class="flex items-center gap-3 min-w-0">
                  <div class="flex h-10 w-10 shrink-0 items-center justify-center rounded-lg bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-indigo-300 font-bold text-xs uppercase">
                    3D
                  </div>
                  <div class="min-w-0">
                    <p class="truncate text-xs sm:text-sm font-bold text-navy-900 dark:text-white">{{ f.name }}</p>
                    <p class="text-[11px] text-slate-400">
                      {{ f.sizeStr }} • {{ f.dimensions.x }}×{{ f.dimensions.y }}×{{ f.dimensions.z }} mm • Est. Vol: {{ f.volumeCm3 }} cm³
                    </p>
                  </div>
                </div>

                <!-- Quantity Counter & Delete -->
                <div class="flex items-center gap-4 self-end sm:self-auto shrink-0">
                  <div class="flex items-center border border-slate-200 dark:border-slate-700 rounded-lg overflow-hidden">
                    <button
                      type="button"
                      @click="decreaseQty(idx)"
                      class="px-2.5 py-1 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 text-sm font-bold"
                    >
                      -
                    </button>
                    <span class="px-3 py-1 text-xs font-bold text-navy-900 dark:text-white min-w-[2rem] text-center">
                      {{ f.quantity }}
                    </span>
                    <button
                      type="button"
                      @click="increaseQty(idx)"
                      class="px-2.5 py-1 text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-700 text-sm font-bold"
                    >
                      +
                    </button>
                  </div>

                  <button
                    type="button"
                    @click="removeFile(idx)"
                    class="text-xs text-rose-500 hover:text-rose-600 font-semibold p-1 hover:bg-rose-50 dark:hover:bg-rose-950/30 rounded"
                  >
                    Delete
                  </button>
                </div>
              </div>
            </div>
          </section>

          <!-- 2. Manufacturing Technology (FDM, SLA, SLS) -->
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 sm:p-6 shadow-xs">
            <div class="flex items-center gap-2.5 mb-4">
              <span class="flex h-7 w-7 items-center justify-center rounded-lg bg-navy-900 dark:bg-indigo-600 text-white font-bold text-xs">
                2
              </span>
              <h2 class="text-base sm:text-lg font-bold text-navy-900 dark:text-white">
                {{ t('Select Printing Technology') }}
              </h2>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <button
                v-for="tech in technologies"
                :key="tech.id"
                type="button"
                @click="selectedTech = tech.id"
                class="rounded-xl border-2 p-4 text-left transition-all cursor-pointer relative"
                :class="selectedTech === tech.id
                  ? 'border-navy-900 dark:border-indigo-500 bg-navy-50/60 dark:bg-slate-800 ring-2 ring-navy-900/20 dark:ring-indigo-500/30'
                  : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-white dark:bg-slate-800/60'"
              >
                <div class="flex items-center justify-between mb-1.5">
                  <span class="text-sm font-black text-navy-900 dark:text-white">{{ tech.name }}</span>
                  <span class="text-xs font-bold text-navy-900 dark:text-indigo-300">{{ tech.badge }}</span>
                </div>
                <p class="text-[11px] font-medium text-slate-500 dark:text-slate-400 leading-snug">
                  {{ tech.desc }}
                </p>
                <div class="mt-3 text-[10px] text-slate-400 flex items-center gap-1.5">
                  <span>Precision: {{ tech.precision }}</span>
                </div>
              </button>
            </div>
          </section>

          <!-- 3. Material Selection -->
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 sm:p-6 shadow-xs">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-2.5">
                <span class="flex h-7 w-7 items-center justify-center rounded-lg bg-navy-900 dark:bg-indigo-600 text-white font-bold text-xs">
                  3
                </span>
                <h2 class="text-base sm:text-lg font-bold text-navy-900 dark:text-white">
                  {{ t('Material') }}
                </h2>
              </div>
              <span class="text-xs text-navy-900 dark:text-indigo-300 font-bold">
                {{ currentMaterials.length }} Options available
              </span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
              <button
                v-for="mat in currentMaterials"
                :key="mat.id"
                type="button"
                @click="selectedMaterial = mat.id"
                class="rounded-xl border-2 p-3.5 text-left transition-all cursor-pointer"
                :class="selectedMaterial === mat.id
                  ? 'border-navy-900 dark:border-indigo-500 bg-navy-50/60 dark:bg-slate-800 ring-2 ring-navy-900/20 dark:ring-indigo-500/30'
                  : 'border-slate-200 dark:border-slate-800 hover:border-slate-300 dark:hover:border-slate-700 bg-white dark:bg-slate-800/60'"
              >
                <div class="flex items-center justify-between">
                  <span class="text-xs sm:text-sm font-bold text-navy-900 dark:text-white">{{ mat.name }}</span>
                  <span class="text-[11px] font-semibold text-slate-500 dark:text-slate-400">{{ mat.priceTag }}</span>
                </div>
                <p class="text-[11px] text-slate-500 dark:text-slate-400 mt-1">
                  {{ mat.description }}
                </p>
                <div class="mt-2 flex flex-wrap gap-1.5">
                  <span
                    v-for="tag in mat.tags"
                    :key="tag"
                    class="rounded bg-slate-100 dark:bg-slate-700 px-1.5 py-0.5 text-[10px] font-medium text-slate-600 dark:text-slate-300"
                  >
                    {{ tag }}
                  </span>
                </div>
              </button>
            </div>
          </section>

          <!-- 4. Color, Infill & Layer Resolution -->
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 sm:p-6 shadow-xs space-y-6">
            <div class="flex items-center gap-2.5">
              <span class="flex h-7 w-7 items-center justify-center rounded-lg bg-navy-900 dark:bg-indigo-600 text-white font-bold text-xs">
                4
              </span>
              <h2 class="text-base sm:text-lg font-bold text-navy-900 dark:text-white">
                {{ t('Specifications & Color') }}
              </h2>
            </div>

            <!-- Color Palette -->
            <div>
              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-2.5 uppercase tracking-wider">
                Color
              </label>
              <div class="flex flex-wrap gap-2.5">
                <button
                  v-for="color in colors"
                  :key="color.name"
                  type="button"
                  @click="selectedColor = color.name"
                  class="flex items-center gap-2 rounded-xl border px-3 py-1.5 text-xs font-semibold transition cursor-pointer"
                  :class="selectedColor === color.name
                    ? 'border-navy-900 dark:border-indigo-500 bg-navy-900 dark:bg-indigo-600 text-white font-bold shadow-xs'
                    : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-300'"
                >
                  <span class="h-3.5 w-3.5 rounded-full border border-slate-300 shadow-xs shrink-0" :style="{ backgroundColor: color.hex }"></span>
                  <span>{{ color.name }}</span>
                </button>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-5 pt-2">
              <!-- Infill Density -->
              <div>
                <div class="flex justify-between items-center mb-1.5">
                  <label class="text-xs font-bold text-slate-700 dark:text-slate-300 uppercase tracking-wider">
                    Infill Density
                  </label>
                  <span class="text-xs font-bold text-navy-900 dark:text-indigo-300">{{ selectedInfill }}%</span>
                </div>
                <div class="grid grid-cols-4 gap-1.5">
                  <button
                    v-for="inf in [20, 40, 70, 100]"
                    :key="inf"
                    type="button"
                    @click="selectedInfill = inf"
                    class="rounded-lg border py-2 text-xs font-bold transition text-center"
                    :class="selectedInfill === inf
                      ? 'border-sky-500 bg-sky-50 dark:bg-sky-950/40 text-navy-900 dark:text-indigo-300'
                      : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-50'"
                  >
                    {{ inf }}%
                  </button>
                </div>
                <p class="text-[10px] text-slate-400 mt-1">
                  {{ selectedInfill === 100 ? '100% Solid for maximum strength.' : `${selectedInfill}% ideal for standard structural parts.` }}
                </p>
              </div>

              <!-- Layer Resolution -->
              <div>
                <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1.5 uppercase tracking-wider">
                  Layer Height
                </label>
                <div class="grid grid-cols-3 gap-1.5">
                  <button
                    v-for="res in layerHeights"
                    :key="res.val"
                    type="button"
                    @click="selectedLayerHeight = res.val"
                    class="rounded-lg border py-2 px-1 text-center transition"
                    :class="selectedLayerHeight === res.val
                      ? 'border-sky-500 bg-sky-50 dark:bg-sky-950/40 text-navy-900 dark:text-indigo-300'
                      : 'border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:bg-slate-50'"
                  >
                    <div class="text-xs font-bold">{{ res.val }}</div>
                    <div class="text-[9px] text-slate-400">{{ res.label }}</div>
                  </button>
                </div>
              </div>
            </div>

            <!-- Post-Processing Options -->
            <div class="pt-2">
              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-2 uppercase tracking-wider">
                Post-Processing & Finishing
              </label>
              <div class="space-y-2">
                <label
                  v-for="opt in postProcessOptions"
                  :key="opt.id"
                  class="flex items-center justify-between p-3 rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 cursor-pointer hover:bg-slate-50 dark:hover:bg-slate-800/80 transition"
                >
                  <div class="flex items-center gap-3">
                    <input
                      type="checkbox"
                      :value="opt.id"
                      v-model="selectedPostProcess"
                      class="h-4 w-4 rounded border-slate-300 text-navy-900 focus:ring-navy-900 dark:focus:ring-indigo-500"
                    />
                    <div>
                      <p class="text-xs font-bold text-navy-900 dark:text-white">{{ opt.name }}</p>
                      <p class="text-[11px] text-slate-400">{{ opt.desc }}</p>
                    </div>
                  </div>
                  <span class="text-xs font-bold text-slate-700 dark:text-slate-300">+${{ opt.price }}</span>
                </label>
              </div>
            </div>
          </section>
        </div>

        <!-- RIGHT COLUMN: Instant Quotation Summary (4 Cols, Sticky) -->
        <div class="lg:col-span-4 lg:sticky lg:top-20 space-y-5">
          <div class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 sm:p-6 shadow-lg shadow-slate-900/5">
            <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 pb-4">
              <h3 class="text-lg font-bold text-navy-900 dark:text-white">
                {{ t('Quotation Summary') }}
              </h3>
              <span class="inline-flex items-center rounded-md bg-emerald-50 dark:bg-emerald-950/40 px-2 py-0.5 text-xs font-bold text-emerald-700 dark:text-emerald-300">
                Instant Calc
              </span>
            </div>

            <!-- Parameters Overview -->
            <div class="mt-4 space-y-2.5 text-xs">
              <div class="flex justify-between text-slate-500 dark:text-slate-400">
                <span>Technology</span>
                <span class="font-bold text-navy-900 dark:text-white">{{ currentTechName }}</span>
              </div>
              <div class="flex justify-between text-slate-500 dark:text-slate-400">
                <span>Material</span>
                <span class="font-bold text-navy-900 dark:text-white">{{ currentMaterialName }}</span>
              </div>
              <div class="flex justify-between text-slate-500 dark:text-slate-400">
                <span>Color</span>
                <span class="font-bold text-navy-900 dark:text-white">{{ selectedColor }}</span>
              </div>
              <div class="flex justify-between text-slate-500 dark:text-slate-400">
                <span>Infill / Layer</span>
                <span class="font-bold text-navy-900 dark:text-white">{{ selectedInfill }}% / {{ selectedLayerHeight }}</span>
              </div>
              <div class="flex justify-between text-slate-500 dark:text-slate-400">
                <span>Total Parts</span>
                <span class="font-bold text-navy-900 dark:text-white">{{ totalPartCount }} pcs</span>
              </div>
              <div class="flex justify-between text-slate-500 dark:text-slate-400">
                <span>Est. Material Weight</span>
                <span class="font-bold text-navy-900 dark:text-white">{{ totalWeightGrams }} g</span>
              </div>
            </div>

            <!-- Cost Breakdown -->
            <div class="mt-5 border-t border-slate-100 dark:border-slate-800 pt-4 space-y-2 text-xs">
              <div class="flex justify-between text-slate-500 dark:text-slate-400">
                <span>Base Machine Setup</span>
                <span>${{ baseFee.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-slate-500 dark:text-slate-400">
                <span>Material & Runtime</span>
                <span>${{ materialCost.toFixed(2) }}</span>
              </div>
              <div v-if="postProcessCost > 0" class="flex justify-between text-slate-500 dark:text-slate-400">
                <span>Post-Processing</span>
                <span>${{ postProcessCost.toFixed(2) }}</span>
              </div>
              <div v-if="quantityDiscount > 0" class="flex justify-between text-emerald-600 font-medium">
                <span>Volume Discount</span>
                <span>-${{ quantityDiscount.toFixed(2) }}</span>
              </div>
            </div>

            <!-- Grand Total -->
            <div class="mt-5 border-t-2 border-slate-200 dark:border-slate-700 pt-4">
              <div class="flex items-baseline justify-between">
                <span class="text-xs uppercase tracking-wider font-bold text-slate-400">Estimated Total</span>
                <div class="text-right">
                  <div class="text-2xl sm:text-3xl font-black text-navy-900 dark:text-white">
                    ${{ finalPriceUsd }}
                  </div>
                  <div class="text-xs font-semibold text-slate-500 dark:text-slate-400 mt-0.5">
                    ≈ {{ finalPriceKhr }} KHR
                  </div>
                </div>
              </div>
            </div>

            <!-- Lead Time Notice -->
            <div class="mt-4 rounded-xl bg-navy-50/80 dark:bg-slate-800/60 p-3 border border-navy-100 dark:border-slate-700 flex items-center gap-2.5">
              <span class="text-navy-900 dark:text-indigo-400 text-lg">⚡</span>
              <p class="text-[11px] text-navy-900 dark:text-indigo-200 font-medium leading-tight">
                <strong>Fast Turnaround:</strong> Print will be completed and ready for pickup/delivery in Phnom Penh in <strong>24–48 hours</strong>.
              </p>
            </div>

            <!-- Action Buttons -->
            <div class="mt-5 space-y-2.5">
              <button
                type="button"
                @click="openOrderModal = true"
                class="w-full rounded-xl bg-sky-600 hover:bg-sky-600 text-white font-extrabold py-3.5 px-4 text-sm shadow-md shadow-sky-600/20 active:scale-[0.99] transition flex items-center justify-center gap-2 cursor-pointer"
              >
                <span>🚀</span>
                <span>Submit Print Order</span>
              </button>

              <a
                :href="telegramDirectLink"
                target="_blank"
                rel="noopener"
                class="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 text-slate-700 dark:text-slate-200 font-bold py-2.5 px-4 text-xs transition flex items-center justify-center gap-2"
              >
                <span>💬</span>
                <span>Direct Quote via Telegram</span>
              </a>
            </div>

            <p class="text-[10px] text-center text-slate-400 mt-3">
              Need custom CNC, metal casting, or bulk quotation? Contact our engineering lab directly.
            </p>
          </div>
        </div>

      </div>
    </main>

    <!-- Order Submission Modal -->
    <div
      v-if="openOrderModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-slate-950/60 backdrop-blur-xs p-4"
    >
      <div class="relative w-full max-w-lg rounded-2xl bg-white dark:bg-slate-900 p-6 shadow-2xl border border-slate-200 dark:border-slate-800">
        <div class="flex items-center justify-between pb-4 border-b border-slate-100 dark:border-slate-800">
          <div class="flex items-center gap-2">
            <span class="text-xl">🖨️</span>
            <h3 class="text-lg font-bold text-navy-900 dark:text-white">Submit 3D Print Request</h3>
          </div>
          <button
            type="button"
            @click="openOrderModal = false"
            class="text-slate-400 hover:text-slate-600 text-xl font-bold p-1 cursor-pointer"
          >
            ✕
          </button>
        </div>

        <div v-if="orderSubmitted" class="py-8 text-center space-y-3">
          <div class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-emerald-100 text-emerald-600 text-2xl font-bold">
            ✓
          </div>
          <h4 class="text-xl font-bold text-navy-900 dark:text-white">Quote Request Received!</h4>
          <p class="text-xs text-slate-500 max-w-xs mx-auto">
            Our Aero Print lab engineers will review your 3D files and contact you on Telegram / Phone within 2 hours.
          </p>
          <button
            type="button"
            @click="openOrderModal = false; orderSubmitted = false"
            class="mt-4 rounded-xl bg-navy-900 dark:bg-indigo-600 text-white font-bold px-6 py-2.5 text-xs"
          >
            Close
          </button>
        </div>

        <form v-else @submit.prevent="submitPrintOrder" class="mt-4 space-y-3.5">
          <div>
            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Your Full Name</label>
            <input
              v-model="orderForm.name"
              type="text"
              required
              placeholder="e.g. Sokha Chan"
              class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs text-slate-900 dark:text-white focus:outline-navy-900 dark:focus:outline-indigo-500"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Phone Number</label>
              <input
                v-model="orderForm.phone"
                type="tel"
                required
                placeholder="012 345 678"
                class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs text-slate-900 dark:text-white focus:outline-navy-900 dark:focus:outline-indigo-500"
              />
            </div>
            <div>
              <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Telegram Handle</label>
              <input
                v-model="orderForm.telegram"
                type="text"
                placeholder="@username"
                class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs text-slate-900 dark:text-white focus:outline-navy-900 dark:focus:outline-indigo-500"
              />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300 mb-1">Delivery / Notes (Optional)</label>
            <textarea
              v-model="orderForm.notes"
              rows="2"
              placeholder="Pick up at AeroByte Academy Lab, or deliver in Phnom Penh..."
              class="w-full rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs text-slate-900 dark:text-white focus:outline-navy-900 dark:focus:outline-indigo-500"
            ></textarea>
          </div>

          <div class="rounded-xl bg-slate-50 dark:bg-slate-800/60 p-3 text-xs text-slate-600 dark:text-slate-300 flex justify-between">
            <span>Estimated Quote:</span>
            <span class="font-black text-navy-900 dark:text-white">${{ finalPriceUsd }} ({{ totalPartCount }} parts)</span>
          </div>

          <button
            type="submit"
            class="w-full rounded-xl bg-sky-600 hover:bg-sky-600 text-white font-bold py-3 text-xs shadow-md transition cursor-pointer"
          >
            Confirm & Send to Lab Engineers
          </button>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from '../i18n'

const { t } = useI18n()

// Sample presets for instant testing
const sampleModels = [
  { id: 'drone-mount', name: 'FPV Motor Mount', icon: '🚁', sizeStr: '1.2 MB', dimensions: { x: 45, y: 45, z: 12 }, volumeCm3: 14.5, quantity: 4 },
  { id: 'sensor-case', name: 'ESP32 Sensor Case', icon: '📦', sizeStr: '2.8 MB', dimensions: { x: 75, y: 50, z: 24 }, volumeCm3: 32.0, quantity: 1 },
  { id: 'arm-gear', name: 'Robotic Servo Gear', icon: '⚙️', sizeStr: '980 KB', dimensions: { x: 35, y: 35, z: 8 }, volumeCm3: 8.2, quantity: 2 },
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

function handleFileInputChange(e) {
  const selectedFiles = Array.from(e.target.files || [])
  for (const f of selectedFiles) {
    files.value.push({
      id: Date.now() + Math.random(),
      name: f.name,
      sizeStr: `${(f.size / (1024 * 1024)).toFixed(1)} MB`,
      dimensions: {
        x: Math.floor(Math.random() * 80 + 30),
        y: Math.floor(Math.random() * 60 + 20),
        z: Math.floor(Math.random() * 40 + 10)
      },
      volumeCm3: parseFloat((Math.random() * 25 + 10).toFixed(1)),
      quantity: 1,
    })
  }
}

function handleFileDrop(e) {
  isDragging.value = false
  const droppedFiles = Array.from(e.dataTransfer?.files || [])
  for (const f of droppedFiles) {
    files.value.push({
      id: Date.now() + Math.random(),
      name: f.name,
      sizeStr: `${(f.size / (1024 * 1024)).toFixed(1)} MB`,
      dimensions: {
        x: Math.floor(Math.random() * 80 + 30),
        y: Math.floor(Math.random() * 60 + 20),
        z: Math.floor(Math.random() * 40 + 10)
      },
      volumeCm3: parseFloat((Math.random() * 25 + 10).toFixed(1)),
      quantity: 1,
    })
  }
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

// 2. Technologies
const selectedTech = ref('fdm')
const technologies = [
  { id: 'fdm', name: 'FDM / FFF', badge: 'Most Affordable', desc: 'Ideal for functional parts, drone bodies & rapid prototypes.', precision: '±0.2mm' },
  { id: 'sla', name: 'SLA Resin', badge: 'Ultra Precision', desc: 'Smooth injection-mold surface finish for fine details.', precision: '±0.05mm' },
  { id: 'sls', name: 'SLS Nylon', badge: 'Industrial Grade', desc: 'No support structures. Strong functional mechanical gears.', precision: '±0.1mm' },
]

// 3. Materials
const selectedMaterial = ref('pla')
const materialsByTech = {
  fdm: [
    { id: 'pla', name: 'Standard PLA', priceTag: '$0.08 / cm³', description: 'Affordable, rigid, high precision for prototypes.', tags: ['Rigid', 'Eco-friendly', 'Clean Detail'] },
    { id: 'petg', name: 'Tough PETG', priceTag: '$0.11 / cm³', description: 'Impact resistant, heat-resistant (75°C), drone parts.', tags: ['Durable', 'Waterproof', 'Impact'] },
    { id: 'abs', name: 'ABS / ASA', priceTag: '$0.13 / cm³', description: 'Thermal resistance (95°C), outdoors, automotive grade.', tags: ['High Temp', 'UV Resistant'] },
    { id: 'tpu', name: 'TPU Flexible (95A)', priceTag: '$0.16 / cm³', description: 'Rubber-like flexible filament for bumpers & dampeners.', tags: ['Elastic', 'Shock Absorbing'] },
    { id: 'cf-nylon', name: 'Carbon Fiber Nylon', priceTag: '$0.28 / cm³', description: 'Ultra-lightweight aerospace rigidity & strength.', tags: ['Extreme Stiff', 'Pro Racing'] },
  ],
  sla: [
    { id: 'sla-std', name: 'Standard Resin (White/Gray)', priceTag: '$0.18 / cm³', description: 'Glass-smooth surface finish, flawless presentation.', tags: ['0.05mm Layers', 'Ultra Smooth'] },
    { id: 'sla-tough', name: 'Engineering Tough Resin', priceTag: '$0.25 / cm³', description: 'ABS-like mechanical resilience and snap-fits.', tags: ['Impact Tough', 'Drillable'] },
    { id: 'sla-clear', name: 'Optical Clear Resin', priceTag: '$0.29 / cm³', description: 'Translucent light pipes, fluidics & lenses.', tags: ['Transparent', 'Polished'] },
  ],
  sls: [
    { id: 'sls-pa12', name: 'Nylon PA12', priceTag: '$0.35 / cm³', description: 'Industrial production end-use parts, isotropic strength.', tags: ['Supportless', 'Engineered'] },
  ]
}

const currentMaterials = computed(() => {
  return materialsByTech[selectedTech.value] || materialsByTech.fdm
})

// Auto sync material when tech changes
const currentTechName = computed(() => {
  return technologies.find(t => t.id === selectedTech.value)?.name || 'FDM'
})

const currentMaterialName = computed(() => {
  return currentMaterials.value.find(m => m.id === selectedMaterial.value)?.name || currentMaterials.value[0]?.name || 'PLA'
})

// 4. Color, Infill, Layer Resolution
const selectedColor = ref('Jet Black')
const colors = [
  { name: 'Jet Black', hex: '#18181b' },
  { name: 'Pure White', hex: '#f8fafc' },
  { name: 'Cyber Gray', hex: '#64748b' },
  { name: 'Aero Orange', hex: '#f97316' },
  { name: 'Royal Navy', hex: '#1e3a8a' },
  { name: 'Clear Translucent', hex: '#e2e8f0' },
]

const selectedInfill = ref(20)
const selectedLayerHeight = ref('0.20mm')
const layerHeights = [
  { val: '0.12mm', label: 'Fine Detail' },
  { val: '0.20mm', label: 'Balanced' },
  { val: '0.28mm', label: 'Rapid Prototype' },
]

const selectedPostProcess = ref([])
const postProcessOptions = [
  { id: 'support-clean', name: 'Standard Clean & De-burr', desc: 'Support material cleanly removed & flush cut', price: 0 },
  { id: 'sanding', name: 'Precision Sanding & Matte Finish', desc: 'Hand-finished to remove layer lines on visual faces', price: 3 },
  { id: 'brass-inserts', name: 'Heat-set Threaded Brass Inserts', desc: 'M3 / M4 brass nuts melted into mounting holes', price: 4 },
]

// 5. Reactive Instant Price Calculation
const totalPartCount = computed(() => {
  return files.value.reduce((acc, f) => acc + (f.quantity || 1), 0)
})

const totalVolumeCm3 = computed(() => {
  return files.value.reduce((acc, f) => acc + (f.volumeCm3 * (f.quantity || 1)), 0)
})

const totalWeightGrams = computed(() => {
  // Density ~1.24 g/cm3 with infill adjustment
  const infillMultiplier = 0.2 + (selectedInfill.value / 100) * 0.8
  const weight = totalVolumeCm3.value * 1.24 * infillMultiplier
  return Math.max(5, Math.round(weight))
})

const baseFee = computed(() => {
  if (files.value.length === 0) return 0
  return selectedTech.value === 'sla' ? 4.50 : 2.50
})

const materialCost = computed(() => {
  if (files.value.length === 0) return 0
  let rate = 0.10
  if (selectedTech.value === 'sla') rate = 0.22
  if (selectedTech.value === 'sls') rate = 0.35
  if (selectedMaterial.value === 'cf-nylon') rate = 0.30
  if (selectedMaterial.value === 'tpu') rate = 0.18
  return totalVolumeCm3.value * rate
})

const postProcessCost = computed(() => {
  return selectedPostProcess.value.reduce((acc, id) => {
    const opt = postProcessOptions.find(o => o.id === id)
    return acc + (opt ? opt.price : 0)
  }, 0)
})

const quantityDiscount = computed(() => {
  if (totalPartCount.value >= 10) return (materialCost.value + baseFee.value) * 0.15
  if (totalPartCount.value >= 5) return (materialCost.value + baseFee.value) * 0.08
  return 0
})

const finalPriceUsd = computed(() => {
  if (files.value.length === 0) return '0.00'
  const total = Math.max(3.00, baseFee.value + materialCost.value + postProcessCost.value - quantityDiscount.value)
  return total.toFixed(2)
})

const finalPriceKhr = computed(() => {
  const usd = parseFloat(finalPriceUsd.value)
  return Math.round(usd * 4100).toLocaleString('en-US')
})

// Telegram direct message link
const telegramDirectLink = computed(() => {
  const msg = encodeURIComponent(
    `Hello AeroByte! I would like a 3D print quote:\n• Tech: ${currentTechName.value}\n• Material: ${currentMaterialName.value}\n• Color: ${selectedColor.value}\n• Infill: ${selectedInfill.value}%\n• Parts: ${totalPartCount.value} pcs\n• Est. Quote: $${finalPriceUsd.value}`
  )
  return `https://t.me/aerobyte?text=${msg}`
})

// Order Submission Modal State
const openOrderModal = ref(false)
const orderSubmitted = ref(false)
const orderForm = ref({
  name: '',
  phone: '',
  telegram: '',
  notes: ''
})

function submitPrintOrder() {
  orderSubmitted.value = true
}
</script>
