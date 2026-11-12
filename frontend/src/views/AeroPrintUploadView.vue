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
              <span>{{ t('Back to Creality K2 Plus') }}</span>
            </router-link>

            <div class="flex flex-wrap items-center gap-2.5">
              <h1 class="text-2xl sm:text-3xl font-bold tracking-[-0.02em] text-[#111112] dark:text-white">
                {{ t('Drop Your 3D CAD Files') }}
              </h1>
              <span class="inline-flex items-center gap-1.5 rounded-full bg-navy-900/10 dark:bg-blue-400/15 border border-navy-900/20 dark:border-blue-400/30 px-3 py-0.5 text-xs font-semibold text-navy-900 dark:text-blue-300">
                <span class="h-1.5 w-1.5 rounded-full bg-navy-900 dark:bg-blue-400"></span>
                Creality K2 Plus • {{ t('Instant 3D Quote') }}
              </span>
            </div>
            <p class="text-xs sm:text-sm text-[#575757] dark:text-white/65">
              {{ t('Instant Online 3D Printing Quotation & Rapid Prototyping Service in Cambodia') }}
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

    <!-- Main 2-Column Quotation & File Dropzone Container -->
    <main class="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8 mt-6 sm:mt-8">
      <div class="grid grid-cols-1 lg:grid-cols-12 gap-6 sm:gap-8 items-start">

        <!-- LEFT COLUMN: 3D CAD Dropzone & Customization (8 Cols) -->
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
          </section>

          <!-- 2. Manufacturing Technology (K2 Plus FDM, SLA, SLS) -->
          <section class="rounded-[24px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111112] p-5 sm:p-7 shadow-sm">
            <div class="flex items-center gap-3 mb-4">
              <span class="flex h-7 w-7 items-center justify-center rounded-full bg-navy-900 dark:bg-navy-600 text-white font-bold text-xs shadow-sm shadow-navy-900/25">
                2
              </span>
              <h2 class="text-base sm:text-lg font-bold text-[#111112] dark:text-white">
                {{ t('Select Printing Technology') }}
              </h2>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-3 gap-3.5">
              <button
                v-for="tech in technologies"
                :key="tech.id"
                type="button"
                @click="selectTechnology(tech.id)"
                class="rounded-2xl border p-4 text-left transition-all cursor-pointer relative"
                :class="selectedTech === tech.id
                  ? 'border-navy-900 dark:border-blue-400 bg-navy-50/70 dark:bg-blue-500/10 ring-2 ring-navy-900/15 dark:ring-blue-400/25'
                  : 'border-black/[0.07] dark:border-white/10 hover:border-black/20 dark:hover:border-white/25 bg-[#FAFAFA] dark:bg-white/[0.02]'"
              >
                <div class="flex items-center justify-between gap-2 mb-1.5">
                  <span class="text-sm font-bold text-[#111112] dark:text-white">{{ tech.name }}</span>
                  <span
                    class="rounded-full px-2 py-0.5 text-[10px] font-bold"
                    :class="selectedTech === tech.id ? 'bg-navy-900 dark:bg-blue-500 text-white' : 'bg-black/5 dark:bg-white/10 text-[#575757] dark:text-white/75'"
                  >
                    {{ tech.badge }}
                  </span>
                </div>
                <p class="text-[11px] text-[#575757] dark:text-white/65 leading-snug">
                  {{ tech.desc }}
                </p>
                <div class="mt-3 text-[10px] font-medium text-[#696969] dark:text-white/50">
                  {{ t('Precision') }}: {{ tech.precision }}
                </div>
              </button>
            </div>
          </section>

          <!-- 3. Material Selection -->
          <section class="rounded-[24px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111112] p-5 sm:p-7 shadow-sm">
            <div class="flex items-center justify-between mb-4">
              <div class="flex items-center gap-3">
                <span class="flex h-7 w-7 items-center justify-center rounded-full bg-navy-900 dark:bg-navy-600 text-white font-bold text-xs shadow-sm shadow-navy-900/25">
                  3
                </span>
                <h2 class="text-base sm:text-lg font-bold text-[#111112] dark:text-white">
                  {{ t('Material') }}
                </h2>
              </div>
              <span class="text-xs font-bold text-navy-900 dark:text-blue-300">
                {{ currentMaterials.length }} {{ t('Options available') }}
              </span>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-3.5">
              <button
                v-for="mat in currentMaterials"
                :key="mat.id"
                type="button"
                @click="selectedMaterial = mat.id"
                class="rounded-2xl border p-4 text-left transition-all cursor-pointer"
                :class="selectedMaterial === mat.id
                  ? 'border-navy-900 dark:border-blue-400 bg-navy-50/70 dark:bg-blue-500/10 ring-2 ring-navy-900/15 dark:ring-blue-400/25'
                  : 'border-black/[0.07] dark:border-white/10 hover:border-black/20 dark:hover:border-white/25 bg-[#FAFAFA] dark:bg-white/[0.02]'"
              >
                <div class="flex items-center justify-between gap-2">
                  <span class="text-xs sm:text-sm font-bold text-[#111112] dark:text-white">{{ mat.name }}</span>
                  <span class="text-[11px] font-bold" :class="selectedMaterial === mat.id ? 'text-navy-900 dark:text-blue-300' : 'text-[#575757] dark:text-white/60'">
                    {{ mat.priceTag }}
                  </span>
                </div>
                <p class="text-[11px] text-[#575757] dark:text-white/60 mt-1.5">
                  {{ mat.description }}
                </p>
                <div class="mt-2.5 flex flex-wrap gap-1.5">
                  <span
                    v-for="tag in mat.tags"
                    :key="tag"
                    class="rounded-full bg-[#F3F4F6] dark:bg-white/10 px-2 py-0.5 text-[10px] font-medium text-[#575757] dark:text-white/75"
                  >
                    {{ tag }}
                  </span>
                </div>
              </button>
            </div>
          </section>

          <!-- 4. Color, Infill & Layer Resolution -->
          <section class="rounded-[24px] border border-black/[0.06] dark:border-white/10 bg-white dark:bg-[#111112] p-5 sm:p-7 shadow-sm space-y-6">
            <div class="flex items-center gap-3">
              <span class="flex h-7 w-7 items-center justify-center rounded-full bg-navy-900 dark:bg-navy-600 text-white font-bold text-xs shadow-sm shadow-navy-900/25">
                4
              </span>
              <h2 class="text-base sm:text-lg font-bold text-[#111112] dark:text-white">
                {{ t('Specifications & Color') }}
              </h2>
            </div>

            <!-- Color Palette (Including CFS Multi-Color) -->
            <div>
              <label class="block text-xs font-bold text-[#575757] dark:text-white/70 mb-2.5 uppercase tracking-wider">
                {{ t('Color') }} • {{ t('K2 Plus CFS Ready') }}
              </label>
              <div class="flex flex-wrap gap-2.5">
                <button
                  v-for="color in colors"
                  :key="color.name"
                  type="button"
                  @click="selectedColor = color.name"
                  class="flex items-center gap-2 rounded-full border px-3.5 py-2 text-xs font-semibold transition cursor-pointer"
                  :class="selectedColor === color.name
                    ? 'border-navy-900 dark:border-blue-400 bg-navy-50/75 dark:bg-blue-500/15 text-[#111112] dark:text-white ring-2 ring-navy-900/15 dark:ring-blue-400/25 font-bold'
                    : 'border-black/[0.08] dark:border-white/15 bg-[#FAFAFA] dark:bg-white/5 text-[#575757] dark:text-white/75 hover:border-black/20'"
                >
                  <span
                    class="h-3.5 w-3.5 rounded-full border border-black/15 shrink-0"
                    :style="color.gradient ? { background: color.gradient } : { backgroundColor: color.hex }"
                  ></span>
                  <span>{{ color.name }}</span>
                </button>
              </div>
            </div>

            <div class="grid grid-cols-1 sm:grid-cols-2 gap-5 pt-1">
              <!-- Infill Density -->
              <div>
                <div class="flex justify-between items-center mb-2">
                  <label class="text-xs font-bold text-[#575757] dark:text-white/70 uppercase tracking-wider">
                    {{ t('Infill Density') }}
                  </label>
                  <span class="text-xs font-bold text-navy-900 dark:text-blue-300">{{ selectedInfill }}%</span>
                </div>
                <div class="grid grid-cols-4 gap-2">
                  <button
                    v-for="inf in [20, 40, 70, 100]"
                    :key="inf"
                    type="button"
                    @click="selectedInfill = inf"
                    class="rounded-xl border py-2 text-xs font-bold transition text-center cursor-pointer"
                    :class="selectedInfill === inf
                      ? 'border-navy-900 dark:border-blue-400 bg-navy-50/75 dark:bg-blue-500/15 text-navy-900 dark:text-blue-300 ring-2 ring-navy-900/15 dark:ring-blue-400/25'
                      : 'border-black/[0.08] dark:border-white/15 bg-[#FAFAFA] dark:bg-white/5 text-[#575757] dark:text-white/75 hover:border-black/20'"
                  >
                    {{ inf }}%
                  </button>
                </div>
                <p class="text-[11px] text-[#696969] dark:text-white/50 mt-1.5">
                  {{ selectedInfill === 100 ? t('100% Solid for maximum strength.') : `${selectedInfill}% ${t('ideal for standard structural parts.')}` }}
                </p>
              </div>

              <!-- Layer Resolution -->
              <div>
                <label class="block text-xs font-bold text-[#575757] dark:text-white/70 mb-2 uppercase tracking-wider">
                  {{ t('Layer Height') }}
                </label>
                <div class="grid grid-cols-3 gap-2">
                  <button
                    v-for="res in layerHeights"
                    :key="res.val"
                    type="button"
                    @click="selectedLayerHeight = res.val"
                    class="rounded-xl border py-2 px-1 text-center transition cursor-pointer"
                    :class="selectedLayerHeight === res.val
                      ? 'border-navy-900 dark:border-blue-400 bg-navy-50/75 dark:bg-blue-500/15 ring-2 ring-navy-900/15 dark:ring-blue-400/25'
                      : 'border-black/[0.08] dark:border-white/15 bg-[#FAFAFA] dark:bg-white/5 hover:border-black/20'"
                  >
                    <div class="text-xs font-bold" :class="selectedLayerHeight === res.val ? 'text-navy-900 dark:text-blue-300' : 'text-[#111112] dark:text-white'">{{ res.val }}</div>
                    <div class="text-[10px]" :class="selectedLayerHeight === res.val ? 'text-navy-800 dark:text-blue-300/85 font-semibold' : 'text-[#696969] dark:text-white/50'">{{ res.label }}</div>
                  </button>
                </div>
              </div>
            </div>

            <!-- Post-Processing Options -->
            <div class="pt-1">
              <label class="block text-xs font-bold text-[#575757] dark:text-white/70 mb-2.5 uppercase tracking-wider">
                {{ t('Post-Processing & Finishing') }}
              </label>
              <div class="space-y-2.5">
                <label
                  v-for="opt in postProcessOptions"
                  :key="opt.id"
                  :class="selectedPostProcess.includes(opt.id)
                    ? 'border-navy-900 dark:border-blue-400 bg-navy-50/60 dark:bg-blue-500/10 ring-1 ring-navy-900/20 dark:ring-blue-400/25'
                    : 'border-black/[0.07] dark:border-white/10 bg-[#FAFAFA] dark:bg-white/[0.02] hover:border-black/20'"
                  class="flex items-center justify-between p-3.5 rounded-2xl border cursor-pointer transition"
                >
                  <div class="flex items-center gap-3">
                    <input
                      type="checkbox"
                      :value="opt.id"
                      v-model="selectedPostProcess"
                      class="h-4 w-4 rounded border-slate-300 text-navy-900 dark:text-blue-400 focus:ring-navy-900 dark:focus:ring-blue-400 accent-[#102a49]"
                    />
                    <div>
                      <p class="text-xs font-bold text-[#111112] dark:text-white">{{ opt.name }}</p>
                      <p class="text-[11px] text-[#696969] dark:text-white/55">{{ opt.desc }}</p>
                    </div>
                  </div>
                  <span class="text-xs font-bold text-[#111112] dark:text-white">+${{ opt.price }}</span>
                </label>
              </div>
            </div>
          </section>
        </div>

        <!-- RIGHT COLUMN: Instant Quotation Summary (4 Cols, Sticky) -->
        <div class="lg:col-span-4 lg:sticky lg:top-20 space-y-5">
          <div class="rounded-[28px] border border-black/[0.07] dark:border-white/10 bg-white dark:bg-[#111112] p-6 shadow-xl shadow-black/[0.04]">
            <div class="flex items-center justify-between border-b border-black/[0.06] dark:border-white/10 pb-4">
              <h3 class="text-lg font-bold text-[#111112] dark:text-white">
                {{ t('Quotation Summary') }}
              </h3>
              <span class="inline-flex items-center rounded-full bg-emerald-50 dark:bg-emerald-950/50 px-2.5 py-0.5 text-[11px] font-bold text-emerald-700 dark:text-emerald-300">
                {{ t('Instant Calc') }}
              </span>
            </div>

            <!-- Parameters Overview -->
            <div class="mt-4 space-y-2.5 text-xs">
              <div class="flex justify-between text-[#575757] dark:text-white/60">
                <span>{{ t('Printer') }}</span>
                <span class="font-bold text-[#111112] dark:text-white">Creality K2 Plus</span>
              </div>
              <div class="flex justify-between text-[#575757] dark:text-white/60">
                <span>{{ t('Technology') }}</span>
                <span class="font-bold text-[#111112] dark:text-white">{{ currentTechName }}</span>
              </div>
              <div class="flex justify-between text-[#575757] dark:text-white/60">
                <span>{{ t('Material') }}</span>
                <span class="font-bold text-[#111112] dark:text-white">{{ currentMaterialName }}</span>
              </div>
              <div class="flex justify-between text-[#575757] dark:text-white/60">
                <span>{{ t('Color') }}</span>
                <span class="font-bold text-[#111112] dark:text-white">{{ selectedColor }}</span>
              </div>
              <div class="flex justify-between text-[#575757] dark:text-white/60">
                <span>{{ t('Infill / Layer') }}</span>
                <span class="font-bold text-[#111112] dark:text-white">{{ selectedInfill }}% / {{ selectedLayerHeight }}</span>
              </div>
              <div class="flex justify-between text-[#575757] dark:text-white/60">
                <span>{{ t('Total Parts') }}</span>
                <span class="font-bold text-[#111112] dark:text-white">{{ totalPartCount }} pcs</span>
              </div>
              <div class="flex justify-between text-[#575757] dark:text-white/60">
                <span>{{ t('Est. Material Weight') }}</span>
                <span class="font-bold text-[#111112] dark:text-white">{{ totalWeightGrams }} g</span>
              </div>
            </div>

            <!-- Cost Breakdown -->
            <div class="mt-5 border-t border-black/[0.06] dark:border-white/10 pt-4 space-y-2 text-xs">
              <div class="flex justify-between text-[#575757] dark:text-white/60">
                <span>{{ t('Base Machine Setup') }}</span>
                <span>${{ baseFee.toFixed(2) }}</span>
              </div>
              <div class="flex justify-between text-[#575757] dark:text-white/60">
                <span>{{ t('Material & Runtime') }}</span>
                <span>${{ materialCost.toFixed(2) }}</span>
              </div>
              <div v-if="postProcessCost > 0" class="flex justify-between text-[#575757] dark:text-white/60">
                <span>{{ t('Post-Processing') }}</span>
                <span>${{ postProcessCost.toFixed(2) }}</span>
              </div>
              <div v-if="quantityDiscount > 0" class="flex justify-between text-emerald-600 font-semibold">
                <span>{{ t('Volume Discount') }}</span>
                <span>-${{ quantityDiscount.toFixed(2) }}</span>
              </div>
            </div>

            <!-- Grand Total -->
            <div class="mt-5 border-t-2 border-black/[0.08] dark:border-white/15 pt-4">
              <div class="flex items-baseline justify-between">
                <span class="text-xs uppercase tracking-wider font-bold text-[#696969] dark:text-white/55">{{ t('Estimated Total') }}</span>
                <div class="text-right">
                  <div class="text-3xl font-extrabold text-[#111112] dark:text-white tracking-tight">
                    ${{ finalPriceUsd }}
                  </div>
                  <div class="text-xs font-semibold text-[#575757] dark:text-white/60 mt-0.5">
                    ≈ {{ finalPriceKhr }} KHR
                  </div>
                </div>
              </div>
            </div>

            <!-- Action Buttons -->
            <div class="mt-6 space-y-3">
              <button
                type="button"
                @click="openOrderModal = true"
                class="w-full rounded-full bg-navy-900 hover:bg-navy-800 dark:bg-navy-600 dark:hover:bg-navy-800 text-white font-bold py-3.5 px-5 text-sm shadow-[0_10px_25px_rgba(16,42,73,0.3)] active:scale-[0.99] transition flex items-center justify-center gap-2 cursor-pointer"
              >
                <span>{{ t('Submit Print Order') }}</span>
              </button>

              <a
                :href="telegramDirectLink"
                target="_blank"
                rel="noopener"
                class="w-full rounded-full border border-black/10 dark:border-white/15 bg-[#FAFAFA] dark:bg-white/5 hover:border-navy-900 dark:hover:border-blue-400 text-[#111112] dark:text-white font-bold py-3 px-4 text-xs transition flex items-center justify-center gap-2"
              >
                <span>{{ t('Direct Quote via Telegram') }}</span>
              </a>
            </div>

            <p class="text-[11px] text-center text-[#696969] dark:text-white/50 mt-4 leading-relaxed">
              {{ t('Need multi-color CFS sequencing or bulk engineering runs? Send your files and our Ta Khmau lab engineers will inspect slices before printing.') }}
            </p>
          </div>
        </div>
      </div>
    </main>

    <!-- Order Submission Modal -->
    <div
      v-if="openOrderModal"
      class="fixed inset-0 z-50 flex items-center justify-center bg-black/65 backdrop-blur-sm p-4"
    >
      <div class="relative w-full max-w-lg rounded-[28px] bg-white dark:bg-[#111112] p-6 sm:p-7 shadow-2xl border border-black/[0.08] dark:border-white/10">
        <div class="flex items-center justify-between pb-4 border-b border-black/[0.06] dark:border-white/10">
          <div>
            <h3 class="text-lg font-bold text-[#111112] dark:text-white">{{ t('Submit 3D Print Request') }}</h3>
            <p class="text-xs text-[#696969] dark:text-white/55 mt-0.5">Creality K2 Plus Lab Queue</p>
          </div>
          <button
            type="button"
            @click="openOrderModal = false"
            class="h-8 w-8 rounded-full flex items-center justify-center text-[#696969] hover:text-[#111112] dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/10 font-bold cursor-pointer"
          >
            ✕
          </button>
        </div>

        <div v-if="orderSubmitted" class="py-8 text-center space-y-3">
          <div class="mx-auto flex h-14 w-14 items-center justify-center rounded-full bg-emerald-100 dark:bg-emerald-950/60 text-emerald-600 text-2xl font-bold">
            ✓
          </div>
          <h4 class="text-xl font-bold text-[#111112] dark:text-white">{{ t('Quote Request Received!') }}</h4>
          <p class="text-xs text-[#575757] dark:text-white/65 max-w-xs mx-auto leading-relaxed">
            {{ t('Our Aero Print lab engineers will review your 3D files and contact you on Telegram / Phone within 2 hours.') }}
          </p>
          <button
            type="button"
            @click="openOrderModal = false; orderSubmitted = false"
            class="mt-4 rounded-full bg-navy-900 hover:bg-navy-800 dark:bg-navy-600 dark:hover:bg-navy-800 text-white font-bold px-7 py-2.5 text-xs shadow-[0_8px_20px_rgba(16,42,73,0.28)] cursor-pointer"
          >
            {{ t('Done') }}
          </button>
        </div>

        <form v-else @submit.prevent="submitPrintOrder" class="mt-5 space-y-3.5">
          <div>
            <label class="block text-xs font-bold text-[#575757] dark:text-white/75 mb-1">{{ t('Your Full Name') }}</label>
            <input
              v-model="orderForm.name"
              type="text"
              required
              placeholder="e.g. Sokha Chan"
              class="w-full rounded-xl border border-black/15 dark:border-white/15 bg-[#FAFAFA] dark:bg-white/5 px-3.5 py-2.5 text-xs text-[#111112] dark:text-white focus:outline-none focus:border-navy-900 dark:focus:border-blue-400"
            />
          </div>

          <div class="grid grid-cols-2 gap-3">
            <div>
              <label class="block text-xs font-bold text-[#575757] dark:text-white/75 mb-1">{{ t('Phone Number') }}</label>
              <input
                v-model="orderForm.phone"
                type="tel"
                required
                placeholder="012 345 678"
                class="w-full rounded-xl border border-black/15 dark:border-white/15 bg-[#FAFAFA] dark:bg-white/5 px-3.5 py-2.5 text-xs text-[#111112] dark:text-white focus:outline-none focus:border-navy-900 dark:focus:border-blue-400"
              />
            </div>
            <div>
              <label class="block text-xs font-bold text-[#575757] dark:text-white/75 mb-1">{{ t('Telegram Handle') }}</label>
              <input
                v-model="orderForm.telegram"
                type="text"
                placeholder="@username"
                class="w-full rounded-xl border border-black/15 dark:border-white/15 bg-[#FAFAFA] dark:bg-white/5 px-3.5 py-2.5 text-xs text-[#111112] dark:text-white focus:outline-none focus:border-navy-900 dark:focus:border-blue-400"
              />
            </div>
          </div>

          <div>
            <label class="block text-xs font-bold text-[#575757] dark:text-white/75 mb-1">{{ t('Delivery / Notes (Optional)') }}</label>
            <textarea
              v-model="orderForm.notes"
              rows="2"
              placeholder="Pick up at AeroByte Academy Lab, or deliver in Phnom Penh..."
              class="w-full rounded-xl border border-black/15 dark:border-white/15 bg-[#FAFAFA] dark:bg-white/5 px-3.5 py-2.5 text-xs text-[#111112] dark:text-white focus:outline-none focus:border-navy-900 dark:focus:border-blue-400"
            ></textarea>
          </div>

          <div class="rounded-2xl bg-[#FAFAFA] dark:bg-white/5 border border-black/[0.06] dark:border-white/10 p-3.5 text-xs text-[#575757] dark:text-white/75 flex justify-between items-center">
            <span>{{ t('Estimated Quote') }}:</span>
            <span class="font-bold text-sm text-[#111112] dark:text-white">${{ finalPriceUsd }} ({{ totalPartCount }} parts)</span>
          </div>

          <button
            type="submit"
            class="w-full rounded-full bg-navy-900 hover:bg-navy-800 dark:bg-navy-600 dark:hover:bg-navy-800 text-white font-bold py-3.5 text-xs shadow-[0_10px_25px_rgba(16,42,73,0.3)] transition cursor-pointer"
          >
            {{ t('Confirm & Send to Lab Engineers') }}
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
  { id: 'fdm', name: 'Creality K2 Plus (FDM)', badge: 'Flagship CoreXY', desc: '600 mm/s hyper-speed, 350³mm chamber & 16-color CFS multi-material.', precision: '±0.1mm' },
  { id: 'sla', name: 'SLA Resin', badge: 'Ultra Precision', desc: 'Smooth injection-mold surface finish for fine micro-details.', precision: '±0.05mm' },
  { id: 'sls', name: 'SLS Nylon', badge: 'Industrial Grade', desc: 'Support-free laser sintered nylon for complex mechanical gears.', precision: '±0.1mm' },
]

// 3. Materials
const selectedMaterial = ref('pla')
const materialsByTech = {
  fdm: [
    { id: 'pla', name: 'Hyper PLA', priceTag: '$0.08 / cm³', description: 'Crisp high-speed prototypes tuned for K2 Plus 600mm/s motion.', tags: ['High Speed', 'Clean Detail'] },
    { id: 'petg', name: 'Tough PETG', priceTag: '$0.11 / cm³', description: 'Impact & water resistant functional mounts for FPV drones.', tags: ['Durable', 'Waterproof'] },
    { id: 'abs', name: 'ABS / ASA (60°C Chamber)', priceTag: '$0.13 / cm³', description: 'Actively heated enclosure for warp-free outdoor & thermal parts.', tags: ['Heated Chamber', 'UV Safe'] },
    { id: 'tpu', name: 'TPU Flexible (95A)', priceTag: '$0.16 / cm³', description: 'Shock-absorbing GoPro mounts, drone skids & rubber bumpers.', tags: ['Elastic', 'Crash-Proof'] },
    { id: 'cf-nylon', name: 'PA-CF Carbon Fiber', priceTag: '$0.28 / cm³', description: '350°C Unicorn nozzle aerospace rigidity for structural frames.', tags: ['Extreme Stiff', '350°C Printed'] },
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

function selectTechnology(techId) {
  selectedTech.value = techId
  const list = materialsByTech[techId] || materialsByTech.fdm
  if (list.length > 0) {
    selectedMaterial.value = list[0].id
  }
}

const currentTechName = computed(() => {
  return technologies.find(t => t.id === selectedTech.value)?.name || 'Creality K2 Plus (FDM)'
})

const currentMaterialName = computed(() => {
  return currentMaterials.value.find(m => m.id === selectedMaterial.value)?.name || currentMaterials.value[0]?.name || 'Hyper PLA'
})

// 4. Color, Infill, Layer Resolution
const selectedColor = ref('Jet Black')
const colors = [
  { name: 'Jet Black', hex: '#18181b' },
  { name: 'Pure White', hex: '#f8fafc' },
  { name: 'Cyber Gray', hex: '#64748b' },
  { name: 'Aero Orange', hex: '#FF5E0E' },
  { name: 'Royal Navy', hex: '#1034A6' },
  { name: 'CFS Multi-Color (Up to 16)', hex: '#FF5E0E', gradient: 'linear-gradient(135deg, #FF5E0E, #1034A6, #18181b)' },
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
  if (files.value.length === 0) return 0
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
  const cfsAdder = selectedColor.value.includes('Multi-Color') ? 1.25 : 1.0
  return totalVolumeCm3.value * rate * cfsAdder
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
    `Hello AeroByte! I would like a Creality K2 Plus 3D print quote:\n• Tech: ${currentTechName.value}\n• Material: ${currentMaterialName.value}\n• Color: ${selectedColor.value}\n• Infill: ${selectedInfill.value}%\n• Parts: ${totalPartCount.value} pcs\n• Est. Quote: $${finalPriceUsd.value}`
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
