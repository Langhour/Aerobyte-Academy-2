<!-- AeroByte Academy - User Profile & Account Management with Terms of Use & Privacy Policy views -->
<template>
  <div class="bg-slate-50 dark:bg-slate-950 min-h-screen transition-colors">
    <section class="border-b border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 transition-colors">
      <div class="mx-auto max-w-7xl px-3 py-6 sm:px-6 sm:py-8 lg:px-8">
        <nav aria-label="Breadcrumb" class="text-xs font-medium text-slate-500 dark:text-slate-400">
          <RouterLink to="/courses" class="transition hover:text-navy-900 dark:hover:text-white">Home</RouterLink>
          <span class="mx-2 text-slate-300 dark:text-slate-600" aria-hidden="true">/</span>
          <span class="text-navy-900 dark:text-white font-semibold">{{ activeSectionTitle }}</span>
        </nav>
        <div class="mt-5 flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
          <div>
            <p class="text-xs font-bold uppercase tracking-[0.16em] text-navy-600 dark:text-indigo-400">{{ t('Your account') }}</p>
            <h1 class="mt-2 text-3xl font-extrabold tracking-tight text-navy-900 dark:text-white sm:text-4xl">
              {{ activeSectionTitle }}
            </h1>
            <p class="mt-2 max-w-2xl text-sm leading-6 text-slate-500 dark:text-slate-400">
              {{ activeSectionDescription }}
            </p>
          </div>
          <span
            class="inline-flex w-fit items-center gap-2 rounded-full border border-emerald-100 dark:border-emerald-800/80 bg-emerald-50 dark:bg-emerald-950/50 px-3 py-1.5 text-xs font-semibold text-emerald-700 dark:text-emerald-300"
          >
            <ShieldCheck class="h-4 w-4" aria-hidden="true" />
            {{ t('Your information stays private') }}
          </span>
        </div>
      </div>
    </section>

    <div class="mx-auto grid max-w-7xl gap-6 px-3 py-5 sm:px-6 sm:py-8 lg:grid-cols-[280px_minmax(0,1fr)] lg:px-8">
      <aside class="space-y-5">
        <section class="overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs">
          <div class="h-20 bg-gradient-to-r from-navy-900 via-navy-800 to-[#315d89]"></div>
          <div class="-mt-9 px-5 pb-5">
            <div class="relative group/avatar w-fit">
              <div
                class="flex h-[76px] w-[76px] items-center justify-center rounded-2xl border-4 border-white dark:border-slate-900 bg-navy-50 dark:bg-slate-800 text-xl font-extrabold text-navy-800 dark:text-white shadow-md overflow-hidden relative cursor-pointer"
                aria-label="Profile avatar"
                :title="t('Change profile photo')"
                @click="triggerAvatarUpload"
              >
                <img
                  v-if="profile.avatarUrl && !avatarLoadFailed"
                  :src="resolveImageUrl(profile.avatarUrl)"
                  :alt="profile.fullName"
                  class="h-full w-full object-cover"
                  @error="onAvatarError"
                />
                <span v-else>{{ initials }}</span>
                <div v-if="avatarUploading" class="absolute inset-0 bg-black/50 flex items-center justify-center">
                  <RefreshCw class="w-5 h-5 text-white animate-spin" />
                </div>
              </div>
            </div>
            <h2 class="mt-3 text-base font-bold text-navy-900 dark:text-white">{{ profile.fullName || 'Your name' }}</h2>
            <p class="mt-1 break-all text-xs text-slate-500 dark:text-slate-400">
              {{ profile.email || 'Add your email address' }}
            </p>
            <div class="mt-5 border-t border-slate-100 dark:border-slate-800 pt-4">
              <div class="flex items-center justify-between text-xs">
                <span class="font-semibold text-slate-600 dark:text-slate-300">{{ t('Profile completeness') }}</span>
                <span class="font-bold text-navy-900 dark:text-white">{{ completion }}%</span>
              </div>
              <div
                class="mt-2 h-2 overflow-hidden rounded-full bg-slate-100 dark:bg-slate-800"
                role="progressbar"
                :aria-valuenow="completion"
                aria-valuemin="0"
                aria-valuemax="100"
                aria-label="Profile completeness"
              >
                <div
                  class="h-full rounded-full bg-accent-green transition-all duration-300"
                  :style="{ width: `${completion}%` }"
                ></div>
              </div>
              <p class="mt-2 text-xs leading-5 text-slate-500 dark:text-slate-400">
                {{ t('A complete profile helps our team support your learning journey.') }}
              </p>
            </div>
          </div>
        </section>

        <nav class="overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-2 shadow-xs" :aria-label="t('Account navigation')">
          <button
            v-for="item in accountSections"
            :key="item.id"
            type="button"
            class="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-semibold transition cursor-pointer"
            :class="activeSection === item.id
              ? 'bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-white font-bold'
              : 'text-slate-600 dark:text-slate-400 hover:bg-slate-50 dark:hover:bg-slate-800/60 hover:text-navy-900 dark:hover:text-white'"
            :aria-current="activeSection === item.id ? 'page' : undefined"
            @click="selectSection(item.id)"
          >
            <component :is="item.icon" class="h-4 w-4 shrink-0" aria-hidden="true" />
            {{ t(item.label) }}
            <span
              v-if="item.id === 'history' && courseHistory.length"
              class="ml-auto rounded-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 px-2 py-0.5 text-[11px] text-slate-500 dark:text-slate-400"
            >
              {{ courseHistory.length }}
            </span>
            <span
              v-if="item.id === 'orders' && (printOrders.length || storeOrders.length)"
              class="ml-auto rounded-full bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 px-2 py-0.5 text-[11px] text-slate-500 dark:text-slate-400"
            >
              {{ printOrders.length || storeOrders.length }}
            </span>
          </button>
          <div class="my-2 border-t border-slate-100 dark:border-slate-800"></div>
          <button
            type="button"
            class="flex w-full items-center gap-3 rounded-xl px-3 py-3 text-left text-sm font-semibold text-red-600 dark:text-red-400 transition hover:bg-red-50 dark:hover:bg-red-950/40 cursor-pointer"
            @click="logoutDialogOpen = true"
          >
            <LogOut class="h-4 w-4" aria-hidden="true" />
            {{ t('Log out') }}
          </button>
        </nav>

        <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-xs">
          <div class="flex items-start gap-3">
            <span class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
              <GraduationCap class="h-5 w-5" aria-hidden="true" />
            </span>
            <div>
              <h2 class="text-base font-extrabold leading-snug text-navy-900 dark:text-white">
                {{ t('Ready for your next step?') }}
              </h2>
              <p class="mt-1 text-xs leading-5 text-slate-500 dark:text-slate-400">
                {{ t('Explore hands-on courses designed for curious minds.') }}
              </p>
              <RouterLink
                to="/courses"
                class="mt-3 inline-flex items-center gap-1.5 text-xs font-bold text-navy-800 dark:text-indigo-400 transition hover:text-accent-orange"
              >
                {{ t('Browse courses') }}
                <ArrowRight class="h-3.5 w-3.5" aria-hidden="true" />
              </RouterLink>
            </div>
          </div>
        </section>
      </aside>

      <div class="min-w-0">
        <!-- Hidden file input for avatar upload -->
        <input
          ref="avatarFileInput"
          type="file"
          accept="image/png,image/jpeg,image/webp,image/gif"
          class="hidden"
          aria-hidden="true"
          @change="handleAvatarChange"
        />
        <div
          v-if="notice"
          class="mb-5 flex items-start gap-2 rounded-xl border px-4 py-3 text-sm"
          :class="noticeType === 'error'
            ? 'border-red-200 dark:border-red-900/50 bg-red-50 dark:bg-red-950/40 text-red-700 dark:text-red-300'
            : 'border-emerald-200 dark:border-emerald-900/50 bg-emerald-50 dark:bg-emerald-950/40 text-emerald-800 dark:text-emerald-300'"
          role="status"
        >
          <Check v-if="noticeType === 'success'" class="mt-0.5 h-4 w-4 shrink-0" aria-hidden="true" />
          <span>{{ notice }}</span>
        </div>

        <section v-if="activeSection === 'history'" class="space-y-5">
          <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 class="text-xl font-extrabold text-navy-900 dark:text-white">{{ t('Course history') }}</h2>
              <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">{{ t('Review your registrations and payment status.') }}</p>
            </div>
            <button
              v-if="courseHistory.length"
              type="button"
              class="inline-flex w-fit items-center gap-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs font-semibold text-slate-700 dark:text-slate-300 transition hover:bg-slate-50 dark:hover:bg-slate-700 cursor-pointer"
              :disabled="historyLoading"
              @click="loadCourseHistory"
            >
              <RefreshCw class="h-3.5 w-3.5" :class="{ 'animate-spin': historyLoading }" aria-hidden="true" />
              {{ t('Refresh history') }}
            </button>
          </div>

          <div
            v-if="historyError"
            class="rounded-xl border border-amber-200 dark:border-amber-900/50 bg-amber-50 dark:bg-amber-950/40 px-4 py-3 text-sm text-amber-800 dark:text-amber-300"
            role="status"
          >
            {{ historyError }}
          </div>

          <div
            v-if="!historyLoading && !courseHistory.length"
            class="rounded-2xl border border-dashed border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-6 py-12 text-center"
          >
            <span class="mx-auto flex h-12 w-12 items-center justify-center rounded-2xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
              <BookOpen class="h-6 w-6" aria-hidden="true" />
            </span>
            <h3 class="mt-4 text-base font-bold text-navy-900 dark:text-white">{{ t('No course history yet') }}</h3>
            <p class="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500 dark:text-slate-400">
              {{ t('Courses you register for will appear here.') }}
            </p>
            <RouterLink
              to="/courses"
              class="mt-5 inline-flex items-center gap-2 rounded-lg bg-navy-900 dark:bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-navy-800 dark:hover:bg-indigo-700"
            >
              {{ t('Browse courses') }}
              <ArrowRight class="h-4 w-4" aria-hidden="true" />
            </RouterLink>
          </div>

          <div v-else class="space-y-4">
            <article
              v-for="enrollment in courseHistory"
              :key="enrollment.enrollment_id"
              class="overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs"
            >
              <div class="flex flex-col gap-4 p-4 sm:flex-row sm:items-center sm:p-5">
                <div class="relative h-28 w-full sm:h-20 sm:w-28 shrink-0 overflow-hidden rounded-xl bg-slate-100 dark:bg-slate-800 border border-slate-200/80 dark:border-slate-700/80 shadow-xs">
                  <img
                    :src="getCourseImage(enrollment)"
                    :alt="enrollment.course_title"
                    class="h-full w-full object-cover transition-transform duration-300 hover:scale-105"
                    loading="lazy"
                    @error="handleCourseImageError($event, enrollment)"
                  />
                </div>
                <div class="min-w-0 flex-1">
                  <div class="flex flex-wrap items-center gap-2">
                    <span
                      class="rounded-full px-2.5 py-1 text-[11px] font-bold capitalize"
                      :class="statusClasses(enrollment.status)"
                    >
                      {{ t(enrollment.status) }}
                    </span>
                    <span class="text-xs text-slate-400 dark:text-slate-500">{{ formatCambodiaTime(enrollment.created_at) }}</span>
                  </div>
                  <h3 class="mt-2 text-base font-bold text-navy-900 dark:text-white">{{ enrollment.course_title }}</h3>
                  <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">
                    {{ t('Enrollment reference') }}: {{ enrollment.enrollment_id }}
                  </p>
                </div>
                <div class="flex items-center justify-between gap-4 border-t border-slate-100 dark:border-slate-800 pt-3 sm:flex-col sm:items-end sm:border-0 sm:pt-0">
                  <span class="text-base font-extrabold text-navy-900 dark:text-white">
                    ${{ enrollment.amount_due.toFixed(2) }}
                  </span>
                  <RouterLink
                    v-if="enrollment.status === 'pending'"
                    :to="{ name: 'ScanToPay', params: { enrollmentId: enrollment.enrollment_id } }"
                    class="text-xs font-bold text-navy-800 dark:text-indigo-400 hover:underline"
                  >
                    {{ t('Continue payment') }}
                  </RouterLink>
                  <RouterLink
                    v-else-if="enrollment.status === 'paid' || enrollment.status === 'confirmed'"
                    :to="{ name: 'PaymentSuccessful', params: { enrollmentId: enrollment.enrollment_id } }"
                    class="text-xs font-bold text-navy-800 dark:text-indigo-400 hover:underline"
                  >
                    {{ t('View receipt') }}
                  </RouterLink>
                  <RouterLink
                    v-else
                    :to="{ name: 'PaymentExpired', params: { enrollmentId: enrollment.enrollment_id } }"
                    class="text-xs font-bold text-navy-800 dark:text-indigo-400 hover:underline"
                  >
                    {{ t('View details') }}
                  </RouterLink>
                </div>
              </div>
            </article>
          </div>
        </section>

        <!-- 3D PRINT ORDERS SECTION -->
        <section v-else-if="activeSection === 'orders'" class="space-y-5">
          <div class="flex flex-col gap-3 sm:flex-row sm:items-end sm:justify-between">
            <div>
              <h2 class="text-xl font-extrabold text-navy-900 dark:text-white">{{ t('3D Print orders') }}</h2>
              <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">{{ t('Track 3D CAD files you submitted for quotation and printing.') }}</p>
            </div>
            <div class="flex items-center gap-2">
              <RouterLink
                to="/print/upload"
                class="inline-flex w-fit items-center gap-1.5 rounded-lg border border-navy-900/10 dark:border-white/10 bg-navy-900 dark:bg-indigo-600 px-3.5 py-2 text-xs font-semibold text-white transition hover:bg-navy-800 dark:hover:bg-indigo-700 cursor-pointer shadow-xs"
              >
                <Printer class="h-3.5 w-3.5" />
                {{ t('Drop 3D CAD files') }}
              </RouterLink>
              <button
                type="button"
                class="inline-flex w-fit items-center gap-1.5 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs font-semibold text-slate-700 dark:text-slate-300 transition hover:bg-slate-50 dark:hover:bg-slate-700 cursor-pointer"
                :disabled="printOrdersLoading"
                @click="loadPrintOrders(true)"
              >
                <RefreshCw class="h-3.5 w-3.5" :class="{ 'animate-spin': printOrdersLoading }" aria-hidden="true" />
                {{ t('Refresh') }}
              </button>
            </div>
          </div>

          <!-- Loading Skeleton (Shows instantly while fetching initial orders) -->
          <div v-if="printOrdersLoading && !printOrders.length && !storeOrders.length" class="space-y-4">
            <div v-for="i in 2" :key="i" class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-5 shadow-xs animate-pulse space-y-4">
              <div class="flex items-center justify-between pb-3 border-b border-slate-100 dark:border-slate-800">
                <div class="h-4 w-32 bg-slate-200 dark:bg-slate-700 rounded"></div>
                <div class="h-5 w-24 bg-slate-200 dark:bg-slate-700 rounded-full"></div>
              </div>
              <div class="flex items-center gap-3">
                <div class="h-10 w-10 bg-slate-200 dark:bg-slate-700 rounded-lg"></div>
                <div class="space-y-2 flex-1">
                  <div class="h-4 w-48 bg-slate-200 dark:bg-slate-700 rounded"></div>
                  <div class="h-3 w-28 bg-slate-100 dark:bg-slate-800 rounded"></div>
                </div>
              </div>
            </div>
          </div>

          <!-- Empty Orders State -->
          <div
            v-else-if="!printOrdersLoading && !printOrders.length && !storeOrders.length"
            class="rounded-2xl border border-dashed border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 px-6 py-12 text-center"
          >
            <span class="mx-auto flex h-14 w-14 items-center justify-center rounded-2xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
              <Printer class="h-7 w-7 text-navy-700 dark:text-indigo-400" aria-hidden="true" />
            </span>
            <h3 class="mt-4 text-base font-bold text-navy-900 dark:text-white">{{ t('No 3D print orders yet') }}</h3>
            <p class="mx-auto mt-2 max-w-md text-sm leading-6 text-slate-500 dark:text-slate-400">
              {{ t('Upload your 3D CAD files (.stl, .obj, .step) on the Aero Print page to request quotes and track printing progress.') }}
            </p>
            <RouterLink
              to="/print/upload"
              class="mt-5 inline-flex items-center gap-2 rounded-lg bg-navy-900 dark:bg-indigo-600 px-4 py-2.5 text-sm font-semibold text-white transition hover:bg-navy-800 dark:hover:bg-indigo-700"
            >
              <Printer class="h-4 w-4" aria-hidden="true" />
              {{ t('Drop 3D CAD files') }}
              <ArrowRight class="h-4 w-4" aria-hidden="true" />
            </RouterLink>
          </div>

          <!-- Print Orders List -->
          <div v-else class="space-y-4">
            <article
              v-for="order in printOrders"
              :key="order.order_number || order.id"
              class="overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs"
            >
              <!-- Order Header -->
              <div class="border-b border-slate-100 dark:border-slate-800 px-5 py-3.5 flex flex-wrap items-center justify-between gap-3 bg-slate-50/50 dark:bg-slate-800/40">
                <div class="flex items-center gap-3">
                  <span class="font-mono text-xs font-bold text-navy-900 dark:text-white">
                    #{{ order.order_number || order.id }}
                  </span>
                  <span class="text-xs text-slate-400">·</span>
                  <span class="text-xs text-slate-500 dark:text-slate-400">
                    {{ formatCambodiaTime(order.created_at || order.date) }}
                  </span>
                </div>
                <div class="flex items-center gap-2">
                  <span
                    class="inline-flex items-center gap-1 px-2.5 py-0.5 rounded-full text-xs font-bold border"
                    :class="(order.payment_status === 'Paid')
                      ? 'border-emerald-300 bg-emerald-50 text-emerald-800 dark:bg-emerald-950/60 dark:text-emerald-300 dark:border-emerald-700'
                      : 'border-amber-300 bg-amber-50 text-amber-800 dark:bg-amber-950/60 dark:text-amber-300 dark:border-amber-700'"
                  >
                    <span>{{ order.payment_status === 'Paid' ? t('Paid') : t('Not Paid') }}</span>
                  </span>
                  <span
                    class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold border"
                    :class="getPrintStatusBadge(order.status).bg"
                  >
                    <span class="h-1.5 w-1.5 rounded-full animate-pulse" :class="getPrintStatusBadge(order.status).dot"></span>
                    {{ t(order.status || 'Pending Review') }}
                  </span>
                </div>
              </div>

              <!-- Order Body -->
              <div class="p-5 space-y-4">
                <!-- CAD Files List -->
                <div class="space-y-2">
                  <div class="text-[11px] font-bold uppercase tracking-wider text-slate-400 dark:text-slate-500">
                    {{ t('Submitted 3D CAD Models') }}
                  </div>
                  <div class="divide-y divide-slate-100 dark:divide-slate-800 rounded-xl border border-slate-100 dark:border-slate-800/80 bg-slate-50/40 dark:bg-slate-800/30 p-2 sm:p-3">
                    <div
                      v-for="(file, idx) in (order.files || [{ original_name: order.part || 'CAD Part', size_str: '', quantity: order.total_parts || 1 }])"
                      :key="file.id || idx"
                      class="py-2.5 flex flex-col sm:flex-row sm:items-center sm:justify-between gap-2.5 first:pt-1 last:pb-1"
                    >
                      <div class="flex items-center gap-3 min-w-0">
                        <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-lg bg-navy-50 dark:bg-slate-800 text-navy-900 dark:text-indigo-400 border border-slate-200/60 dark:border-slate-700/60">
                          <Box class="h-4 w-4" />
                        </div>
                        <div class="min-w-0 flex-1">
                          <h4 class="text-xs sm:text-sm font-bold text-slate-900 dark:text-white truncate">
                            {{ file.original_name || file.name || 'CAD Model' }}
                          </h4>
                          <p class="text-[11px] text-slate-500 dark:text-slate-400 flex flex-wrap items-center gap-2 mt-0.5">
                            <span>Qty: <strong class="text-slate-700 dark:text-slate-200">{{ file.quantity || 1 }}</strong></span>
                            <span v-if="file.size_str">· {{ file.size_str }}</span>
                            <span v-if="file.material">· <span class="rounded bg-slate-200/60 dark:bg-slate-700 px-1.5 py-0.5">{{ file.material }}</span></span>
                          </p>
                        </div>
                      </div>
                      <div class="flex items-center gap-2 shrink-0 sm:self-center pl-12 sm:pl-0">
                        <a
                          v-if="file.download_url || file.stored_filename"
                          :href="getCadFileUrl(file)"
                          target="_blank"
                          rel="noopener"
                          download
                          class="inline-flex items-center gap-1 rounded-md border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-2.5 py-1 text-[11px] font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 transition"
                        >
                          <Download class="h-3 w-3" />
                          {{ t('Download') }}
                        </a>
                      </div>
                    </div>
                  </div>
                </div>

                <!-- Customer Notes if any -->
                <div v-if="order.notes" class="rounded-xl bg-amber-50/50 dark:bg-amber-950/20 border border-amber-200/50 dark:border-amber-800/40 p-3 text-xs text-amber-900 dark:text-amber-200">
                  <span class="font-bold">{{ t('Notes') }}:</span> {{ order.notes }}
                </div>

                <!-- Customer Review Display (if reviewed) -->
                <div v-if="order.review" class="rounded-xl border border-amber-200/80 dark:border-amber-900/50 bg-amber-50/40 dark:bg-amber-950/20 p-3.5 space-y-2">
                  <div class="flex items-center justify-between gap-2">
                    <div class="flex items-center gap-2">
                      <div class="flex items-center text-amber-500">
                        <Star
                          v-for="s in 5"
                          :key="s"
                          class="h-4 w-4"
                          :class="s <= (order.review.rating || 5) ? 'fill-amber-400 text-amber-500' : 'text-slate-300 dark:text-slate-600'"
                        />
                      </div>
                      <span class="text-xs font-bold text-amber-900 dark:text-amber-200">
                        {{ (order.review.rating || 5).toFixed(1) }} / 5.0
                      </span>
                      <span class="text-[11px] font-medium text-slate-400">· {{ t('Your Review') }}</span>
                    </div>
                    <button
                      type="button"
                      @click="openReviewModal(order)"
                      class="inline-flex items-center gap-1 text-[11px] font-bold text-amber-800 dark:text-amber-300 hover:text-amber-950 dark:hover:text-amber-100 hover:underline cursor-pointer"
                    >
                      <Pencil class="h-3 w-3" />
                      {{ t('Edit Review') }}
                    </button>
                  </div>
                  <p v-if="order.review.comment" class="text-xs text-slate-700 dark:text-slate-300 leading-relaxed italic">
                    "{{ order.review.comment }}"
                  </p>
                  <div v-if="order.review.tags && order.review.tags.length" class="flex flex-wrap gap-1.5 pt-0.5">
                    <span
                      v-for="tag in order.review.tags"
                      :key="tag"
                      class="inline-flex items-center px-2 py-0.5 rounded-md text-[10px] font-semibold bg-white dark:bg-slate-800 text-amber-900 dark:text-amber-200 border border-amber-200 dark:border-amber-800/60 shadow-2xs"
                    >
                      ✓ {{ t(tag) }}
                    </span>
                  </div>
                </div>

                <!-- Footer Summary & Actions -->
                <div class="border-t border-slate-100 dark:border-slate-800 pt-3 flex flex-wrap items-center justify-between gap-3 text-xs">
                  <div class="flex items-center gap-4 text-slate-500 dark:text-slate-400">
                    <div>
                      <span class="font-semibold">{{ t('Total parts') }}:</span>
                      <strong class="ml-1 text-slate-800 dark:text-slate-200">{{ order.total_parts || 1 }}</strong>
                    </div>
                    <div>
                      <span class="font-semibold">{{ t('Quote Price') }}:</span>
                      <span v-if="order.price > 0 || order.estimated_price > 0" class="ml-1 text-base font-black text-navy-900 dark:text-white">
                        ${{ Number(order.price || order.estimated_price).toFixed(2) }}
                        <span class="text-[11px] font-normal text-slate-400">({{ Math.round(Number(order.price || order.estimated_price) * 4100).toLocaleString() }} ៛)</span>
                      </span>
                      <span v-else class="ml-1 font-semibold text-amber-600 dark:text-amber-400 italic">
                        {{ t('Quote in progress') }}
                      </span>
                    </div>
                  </div>

                  <div class="flex items-center gap-2">
                    <!-- Review Order Button when Completed -->
                    <button
                      v-if="isPrintOrderCompleted(order) && !order.review"
                      type="button"
                      @click="openReviewModal(order)"
                      class="inline-flex items-center gap-1.5 rounded-lg border border-amber-300 dark:border-amber-700/60 bg-amber-50 hover:bg-amber-100 dark:bg-amber-950/40 dark:hover:bg-amber-900/40 text-amber-900 dark:text-amber-200 px-3 py-1.5 text-xs font-bold transition shadow-xs cursor-pointer"
                    >
                      <Star class="h-3.5 w-3.5 fill-amber-400 text-amber-500" />
                      {{ t('Review Order') }}
                    </button>

                    <button
                      v-else-if="order.review"
                      type="button"
                      @click="openReviewModal(order)"
                      class="inline-flex items-center gap-1.5 rounded-lg border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 px-3 py-1.5 text-xs font-semibold transition shadow-xs cursor-pointer"
                    >
                      <Star class="h-3.5 w-3.5 fill-amber-400 text-amber-500" />
                      {{ t('Edit Review') }}
                    </button>

                    <a
                      :href="getOrderTelegramLink(order)"
                      target="_blank"
                      rel="noopener"
                      class="inline-flex items-center gap-1.5 rounded-lg bg-navy-900 dark:bg-indigo-600 px-3 py-1.5 text-xs font-semibold text-white transition hover:bg-navy-800 dark:hover:bg-indigo-700 shadow-xs"
                    >
                      <Send class="h-3.5 w-3.5" />
                      {{ t('Ask on Telegram') }}
                    </a>
                  </div>
                </div>
              </div>
            </article>

            <!-- Also display legacy store orders if any exist -->
            <div v-if="storeOrders.length" class="mt-8 pt-6 border-t border-slate-200 dark:border-slate-800 space-y-4">
              <h3 class="text-sm font-bold text-slate-500 dark:text-slate-400 uppercase tracking-wider">
                {{ t('Store Purchases') }} ({{ storeOrders.length }})
              </h3>
              <article
                v-for="order in storeOrders"
                :key="order.id"
                class="overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs"
              >
                <div class="border-b border-slate-100 dark:border-slate-800 px-5 py-3.5 flex flex-wrap items-center justify-between gap-3 bg-slate-50/50 dark:bg-slate-800/40">
                  <div class="flex items-center gap-3">
                    <span class="font-mono text-xs font-bold text-navy-900 dark:text-white">
                      #{{ order.id }}
                    </span>
                    <span class="text-xs text-slate-400">·</span>
                    <span class="text-xs text-slate-500 dark:text-slate-400">
                      {{ formatCambodiaTime(order.date) }}
                    </span>
                  </div>
                  <span class="inline-flex items-center gap-1.5 px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border border-emerald-200 dark:border-emerald-800/60">
                    <span class="h-1.5 w-1.5 rounded-full bg-emerald-500 animate-pulse"></span>
                    {{ order.status || 'Confirmed' }}
                  </span>
                </div>
                <div class="p-5 space-y-3">
                  <div class="divide-y divide-slate-100 dark:divide-slate-800">
                    <div
                      v-for="item in order.items"
                      :key="item.id"
                      class="py-2.5 flex items-center justify-between gap-3 first:pt-0 last:pb-0"
                    >
                      <div class="flex items-center gap-3">
                        <div class="flex h-9 w-9 shrink-0 items-center justify-center rounded-xl bg-slate-100 dark:bg-slate-800 text-base border border-slate-200/50 dark:border-slate-700/50">
                          {{ item.icon }}
                        </div>
                        <div>
                          <h4 class="text-xs font-bold text-slate-900 dark:text-white line-clamp-1">
                            {{ item.name }}
                          </h4>
                          <p class="text-[11px] text-slate-400">Qty: {{ item.quantity }} × ${{ Number(item.priceUsd).toFixed(2) }}</p>
                        </div>
                      </div>
                      <span class="text-xs font-bold text-slate-900 dark:text-white">${{ (item.priceUsd * item.quantity).toFixed(2) }}</span>
                    </div>
                  </div>
                  <div class="border-t border-slate-100 dark:border-slate-800 pt-3 flex items-center justify-between text-xs">
                    <span class="text-slate-500 font-semibold">{{ t('Order Total') }}:</span>
                    <span class="text-sm font-black text-navy-900 dark:text-white">${{ Number(order.total || 0).toFixed(2) }}</span>
                  </div>
                </div>
              </article>
            </div>
          </div>
        </section>

        <section v-else-if="activeSection === 'settings'" class="space-y-5">
          <div>
            <h2 class="text-xl font-extrabold text-navy-900 dark:text-slate-100">{{ t('Settings') }}</h2>
            <p class="mt-1 text-sm text-slate-500 dark:text-slate-400">{{ t('Manage your language and local profile preferences.') }}</p>
          </div>

          <!-- Theme Mode Switch Card -->
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs transition-colors">
            <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800/80 px-5 py-5 sm:px-7">
              <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-50 dark:bg-slate-800 text-amber-500 dark:text-amber-400">
                <Sun v-if="!isDark" class="h-5 w-5" aria-hidden="true" />
                <Moon v-else class="h-5 w-5 text-indigo-400" aria-hidden="true" />
              </span>
              <div>
                <h3 class="text-sm font-bold text-navy-900 dark:text-slate-100">{{ t('Theme mode') }}</h3>
                <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">{{ t('Choose between light and dark mode for your experience.') }}</p>
              </div>
            </div>
            <div class="flex items-center justify-between px-5 py-5 sm:px-7">
              <div>
                <span class="text-sm font-semibold text-slate-800 dark:text-slate-200 block">{{ isDark ? t('Dark mode') : t('Light mode') }}</span>
                <span class="text-xs text-slate-400 dark:text-slate-500 block mt-0.5">
                  {{ isDark ? t('Dark theme is currently active') : t('Light theme is currently active') }}
                </span>
              </div>

              <!-- Only Toggle Switch Control -->
              <button
                type="button"
                role="switch"
                :aria-checked="isDark"
                :aria-label="isDark ? t('Switch to light mode') : t('Switch to dark mode')"
                @click="toggleTheme"
                class="relative inline-flex h-8 w-14 shrink-0 cursor-pointer rounded-full border-2 border-transparent transition-colors duration-300 ease-in-out focus:outline-none focus-visible:ring-2 focus-visible:ring-navy-800 dark:focus-visible:ring-indigo-400 shadow-inner"
                :class="isDark ? 'bg-indigo-600' : 'bg-slate-300 dark:bg-slate-700'"
              >
                <span class="sr-only">{{ t('Theme mode') }}</span>
                <span
                  aria-hidden="true"
                  class="pointer-events-none inline-flex h-7 w-7 transform items-center justify-center rounded-full bg-white shadow-md ring-0 transition duration-300 ease-in-out"
                  :class="isDark ? 'translate-x-6' : 'translate-x-0'"
                >
                  <Moon v-if="isDark" class="h-4 w-4 text-indigo-600" />
                  <Sun v-else class="h-4 w-4 text-amber-500" />
                </span>
              </button>
            </div>
          </section>

          <!-- Language Setting Card -->
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs transition-colors">
            <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800/80 px-5 py-5 sm:px-7">
              <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
                <Globe2 class="h-5 w-5" aria-hidden="true" />
              </span>
              <div>
                <h3 class="text-sm font-bold text-navy-900 dark:text-slate-100">{{ t('Language') }}</h3>
                <p class="mt-1 text-xs text-slate-500 dark:text-slate-400">{{ t('Choose the language used across the site.') }}</p>
              </div>
            </div>
            <div class="flex flex-col gap-3 px-5 py-5 sm:flex-row sm:items-center sm:justify-between sm:px-7">
              <span class="text-sm font-medium text-slate-700 dark:text-slate-200">{{ t('Display language') }}</span>
              <div ref="languageDropdownRef" class="relative sm:w-56">
                <button
                  type="button"
                  @click="languageDropdownOpen = !languageDropdownOpen"
                  class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 text-xs bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 flex items-center justify-between text-left focus:outline-none focus:ring-2 focus:ring-navy-800 transition cursor-pointer"
                  :class="languageDropdownOpen ? 'border-navy-800 ring-2 ring-navy-800/20' : 'hover:border-slate-300 dark:hover:border-slate-600'"
                >
                  <span class="font-medium">
                    {{ locale === 'kh' ? 'KH - ភាសាខ្មែរ' : 'EN - English' }}
                  </span>
                  <ChevronDown class="w-4 h-4 text-slate-400 transition-transform duration-200 shrink-0" :class="{ 'rotate-180 text-navy-800': languageDropdownOpen }" />
                </button>

                <div
                  v-if="languageDropdownOpen"
                  class="absolute left-0 right-0 top-full z-30 mt-1.5 overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-1.5 shadow-xl space-y-1"
                >
                  <button
                    type="button"
                    @click="setLocale('en'); languageDropdownOpen = false"
                    class="flex w-full items-center justify-between rounded-xl px-3 py-2 text-xs transition cursor-pointer"
                    :class="locale === 'en'
                      ? 'bg-navy-50 dark:bg-slate-700 text-navy-900 dark:text-white font-bold'
                      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/60 font-medium'"
                  >
                    <span>EN - {{ t('English') }}</span>
                    <Check v-if="locale === 'en'" class="w-4 h-4 text-navy-900 dark:text-white shrink-0" />
                  </button>
                  <button
                    type="button"
                    @click="setLocale('kh'); languageDropdownOpen = false"
                    class="flex w-full items-center justify-between rounded-xl px-3 py-2 text-xs transition cursor-pointer"
                    :class="locale === 'kh'
                      ? 'bg-navy-50 dark:bg-slate-700 text-navy-900 dark:text-white font-bold'
                      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/60 font-medium'"
                  >
                    <span>KH - {{ t('Khmer') }}</span>
                    <Check v-if="locale === 'kh'" class="w-4 h-4 text-navy-900 dark:text-white shrink-0" />
                  </button>
                </div>
              </div>
            </div>
          </section>

          <section class="rounded-2xl border border-red-200 dark:border-red-900/50 bg-white dark:bg-slate-900 p-5 sm:p-7">
            <div class="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
              <div>
                <h3 class="text-sm font-bold text-slate-900 dark:text-white">{{ t('Local profile data') }}</h3>
                <p class="mt-1 max-w-xl text-xs leading-5 text-slate-500 dark:text-slate-400">
                  {{ t('Your profile and history are stored in this browser for this demo.') }}
                </p>
              </div>
              <button
                type="button"
                class="inline-flex w-fit items-center gap-2 rounded-lg border border-red-200 dark:border-red-900/50 px-3.5 py-2 text-xs font-semibold text-red-600 dark:text-red-400 transition hover:bg-red-50 dark:hover:bg-red-950/40 cursor-pointer"
                @click="clearLocalProfile"
              >
                <Trash2 class="h-3.5 w-3.5" aria-hidden="true" />
                {{ t('Clear profile') }}
              </button>
            </div>
          </section>
        </section>

        <form v-else-if="isEditing" class="space-y-5" @submit.prevent="saveProfile">
          <!-- Profile Photo Card in Editing Mode -->
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs overflow-hidden">
            <div class="flex flex-col sm:flex-row items-center sm:items-start gap-5 p-5 sm:p-6">
              <div class="relative group shrink-0">
                <div class="flex h-20 w-20 sm:h-24 sm:w-24 items-center justify-center rounded-2xl border-2 border-slate-200 dark:border-slate-700 bg-navy-50 dark:bg-slate-800 text-2xl font-black text-navy-800 dark:text-white shadow-xs overflow-hidden">
                  <img
                    v-if="(draft.avatarUrl || profile.avatarUrl) && !avatarLoadFailed"
                    :src="resolveImageUrl(draft.avatarUrl || profile.avatarUrl)"
                    :alt="draft.fullName || profile.fullName"
                    class="h-full w-full object-cover"
                    @error="onAvatarError"
                  />
                  <span v-else>{{ initials }}</span>
                </div>
                <button
                  type="button"
                  class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center text-white text-xs font-bold rounded-2xl cursor-pointer"
                  :title="t('Change profile photo')"
                  @click="triggerAvatarUpload"
                >
                  <Camera class="w-5 h-5 mb-1" />
                  <span>{{ t('Change') }}</span>
                </button>
              </div>

              <div class="space-y-1.5 text-center sm:text-left flex-1 min-w-0">
                <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2">
                  <h3 class="text-sm font-bold text-navy-900 dark:text-white">{{ t('Profile photo') }}</h3>
                  <span v-if="(draft.avatarUrl || profile.avatarUrl) && !avatarLoadFailed" class="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/50 px-2 py-0.5 rounded-full border border-emerald-200 dark:border-emerald-800/60">
                    Active
                  </span>
                </div>
                <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed max-w-lg">
                  {{ t('Upload a photo or avatar image. Recommended size: at least 256x256 px (JPG, PNG, or WebP).') }}
                </p>
                <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2.5 pt-2">
                  <button
                    type="button"
                    class="inline-flex items-center gap-1.5 rounded-lg bg-navy-900 dark:bg-indigo-600 px-3.5 py-2 text-xs font-semibold text-white hover:bg-navy-800 dark:hover:bg-indigo-500 shadow-2xs transition cursor-pointer"
                    :disabled="avatarUploading"
                    @click="triggerAvatarUpload"
                  >
                    <RefreshCw v-if="avatarUploading" class="h-3.5 w-3.5 animate-spin" />
                    <Upload v-else class="h-3.5 w-3.5" />
                    <span>{{ avatarUploading ? 'Uploading...' : (((draft.avatarUrl || profile.avatarUrl) && !avatarLoadFailed) ? t('Change photo') : t('Upload photo')) }}</span>
                  </button>
                  <button
                    v-if="(draft.avatarUrl || profile.avatarUrl) && !avatarLoadFailed"
                    type="button"
                    class="inline-flex items-center gap-1.5 rounded-lg border border-red-200 dark:border-red-900/60 bg-red-50/60 dark:bg-red-950/40 px-3.5 py-2 text-xs font-semibold text-red-700 dark:text-red-400 hover:bg-red-100 dark:hover:bg-red-900/50 transition cursor-pointer"
                    @click="removeAvatar"
                  >
                    <Trash2 class="h-3.5 w-3.5" />
                    <span>{{ t('Remove photo') }}</span>
                  </button>
                </div>
              </div>
            </div>
          </section>
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs">
            <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 px-5 py-5 sm:px-7">
              <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
                <UserRound class="h-5 w-5" aria-hidden="true" />
              </span>
              <div>
                <h2 class="text-base font-bold text-navy-900 dark:text-white">{{ t('Personal details') }}</h2>
                <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-400">{{ t('Your contact and personal information.') }}</p>
              </div>
            </div>
            <div class="grid gap-x-5 gap-y-4 px-5 py-6 sm:grid-cols-2 sm:px-7">
              <label class="block">
                <span class="mb-1.5 block text-xs font-semibold text-slate-700 dark:text-slate-200">{{ t('Full name') }} <span class="text-red-500">*</span></span>
                <input
                  v-model.trim="draft.fullName"
                  autocomplete="name"
                  required
                  maxlength="120"
                  :placeholder="t('Enter full name')"
                  class="profile-input"
                />
              </label>
              <label class="block">
                <span class="mb-1.5 block text-xs font-semibold text-slate-700 dark:text-slate-200">{{ t('Email address') }} <span class="text-red-500">*</span></span>
                <input
                  v-model.trim="draft.email"
                  type="email"
                  autocomplete="email"
                  required
                  maxlength="254"
                  placeholder="you@example.com"
                  class="profile-input"
                />
              </label>
              <div>
                <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                  {{ t('Phone number') }}
                </label>
                <input
                  v-model="draft.phone"
                  type="tel"
                  inputmode="tel"
                  autocomplete="tel"
                  maxlength="20"
                  @keypress="onPhoneKeypress"
                  @input="onPhoneInput"
                  placeholder="+855 12 345 678"
                  class="profile-input"
                />
                <p class="mt-1 text-[10px] text-slate-400 dark:text-slate-500">
                  {{ t('Numbers and "+" sign only (e.g. +85512345678)') }}
                </p>
              </div>
              <label class="block">
                <span class="mb-1.5 block text-xs font-semibold text-slate-700 dark:text-slate-200">{{ t('Telegram username') }}</span>
                <input
                  v-model.trim="draft.telegram"
                  maxlength="64"
                  placeholder="@yourusername"
                  class="profile-input"
                />
              </label>
              <label class="block">
                <span class="mb-1.5 block text-xs font-semibold text-slate-700 dark:text-slate-200">{{ t('Date of birth') }}</span>
                <DatePicker
                  v-model="draft.dateOfBirth"
                  :placeholder="t('Select date of birth')"
                  :min-year="1950"
                  :max-year="new Date().getFullYear()"
                />
              </label>
              <label class="block">
                <span class="mb-1.5 block text-xs font-semibold text-slate-700 dark:text-slate-200">{{ t('City or province') }}</span>
                <input
                  v-model.trim="draft.location"
                  autocomplete="address-level2"
                  maxlength="100"
                  :placeholder="t('e.g. Phnom Penh')"
                  class="profile-input"
                />
              </label>
            </div>
          </section>

          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs">
            <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 px-5 py-5 sm:px-7">
              <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
                <GraduationCap class="h-5 w-5" aria-hidden="true" />
              </span>
              <div>
                <h2 class="text-base font-bold text-navy-900 dark:text-white">{{ t('Learning background') }}</h2>
                <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-400">{{ t('Your education and experience.') }}</p>
              </div>
            </div>
            <div class="grid gap-x-5 gap-y-4 px-5 py-6 sm:grid-cols-2 sm:px-7">
              <div ref="qualificationDropdownRef" class="relative">
                <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                  {{ t('Highest qualification') }}
                </label>
                <button
                  type="button"
                  @click="qualificationDropdownOpen = !qualificationDropdownOpen; experienceDropdownOpen = false"
                  class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 text-xs bg-white dark:bg-slate-800 text-slate-900 dark:text-white flex items-center justify-between text-left focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500 transition cursor-pointer"
                  :class="qualificationDropdownOpen ? 'border-navy-800 dark:border-indigo-500 ring-2 ring-navy-800/20' : 'hover:border-slate-300 dark:hover:border-slate-600'"
                >
                  <span :class="draft.qualification ? 'text-slate-800 dark:text-white font-medium' : 'text-slate-400 dark:text-slate-500'">
                    {{ t(draft.qualification) || t('Select your education level') }}
                  </span>
                  <ChevronDown class="w-4 h-4 text-slate-400 transition-transform duration-200 shrink-0" :class="{ 'rotate-180 text-navy-800 dark:text-indigo-400': qualificationDropdownOpen }" />
                </button>

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
                    :class="draft.qualification === option
                      ? 'bg-navy-50 dark:bg-slate-700 text-navy-900 dark:text-white font-bold'
                      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/60 hover:text-navy-900 dark:hover:text-white font-medium'"
                  >
                    <span>{{ t(option) }}</span>
                    <Check v-if="draft.qualification === option" class="w-4 h-4 text-navy-900 dark:text-white shrink-0" />
                  </button>
                </div>

                <input
                  v-if="draft.qualification === 'Other'"
                  v-model.trim="draft.qualificationOther"
                  required
                  maxlength="120"
                  :aria-label="t('Please specify your qualification')"
                  :placeholder="t('Please specify your qualification')"
                  class="profile-input mt-3"
                />
              </div>
              <label class="block">
                <span class="mb-1.5 block text-xs font-semibold text-slate-700 dark:text-slate-200">{{ t('Current occupation') }}</span>
                <input
                  v-model.trim="draft.occupation"
                  maxlength="120"
                  :placeholder="t('e.g. Student, Engineer')"
                  class="profile-input"
                  @keypress="(e) => { if (/[0-9\u17E0-\u17E9]/.test(e.key)) e.preventDefault() }"
                  @input="draft.occupation = draft.occupation.replace(/[0-9\u17E0-\u17E9]/g, '')"
                />
              </label>
              <div ref="experienceDropdownRef" class="relative sm:col-span-2">
                <label class="block text-xs font-semibold text-slate-700 dark:text-slate-200 mb-1.5">
                  {{ t('Coding experience') }}
                </label>
                <button
                  type="button"
                  @click="experienceDropdownOpen = !experienceDropdownOpen; qualificationDropdownOpen = false"
                  class="w-full px-3.5 py-2.5 rounded-xl border border-slate-200 dark:border-slate-700 text-xs bg-white dark:bg-slate-800 text-slate-900 dark:text-white flex items-center justify-between text-left focus:outline-none focus:ring-2 focus:ring-navy-800 dark:focus:ring-indigo-500 transition cursor-pointer"
                  :class="experienceDropdownOpen ? 'border-navy-800 dark:border-indigo-500 ring-2 ring-navy-800/20' : 'hover:border-slate-300 dark:hover:border-slate-600'"
                >
                  <span :class="draft.experience ? 'text-slate-800 dark:text-white font-medium' : 'text-slate-400 dark:text-slate-500'">
                    {{ t(draft.experience) || t('Choose your experience level') }}
                  </span>
                  <ChevronDown class="w-4 h-4 text-slate-400 transition-transform duration-200 shrink-0" :class="{ 'rotate-180 text-navy-800 dark:text-indigo-400': experienceDropdownOpen }" />
                </button>

                <div
                  v-if="experienceDropdownOpen"
                  class="absolute left-0 right-0 top-full z-30 mt-1.5 overflow-hidden rounded-2xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-1.5 shadow-xl space-y-1"
                >
                  <button
                    v-for="option in experienceOptions"
                    :key="option"
                    type="button"
                    @click="selectExperience(option)"
                    class="flex w-full items-center justify-between rounded-xl px-3 py-2 text-xs transition cursor-pointer"
                    :class="draft.experience === option
                      ? 'bg-navy-50 dark:bg-slate-700 text-navy-900 dark:text-white font-bold'
                      : 'text-slate-600 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700/60 hover:text-navy-900 dark:hover:text-white font-medium'"
                  >
                    <span>{{ t(option) }}</span>
                    <Check v-if="draft.experience === option" class="w-4 h-4 text-navy-900 dark:text-white shrink-0" />
                  </button>
                </div>
              </div>
            </div>
          </section>

          <div class="flex flex-col-reverse gap-3 sm:flex-row sm:justify-end">
            <button
              type="button"
              class="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-4 py-2.5 text-sm font-semibold text-slate-700 dark:text-slate-300 transition hover:bg-slate-50 dark:hover:bg-slate-700 cursor-pointer"
              @click="cancelEditing"
            >
              <X class="h-4 w-4" aria-hidden="true" />
              {{ t('Cancel') }}
            </button>
            <button
              type="submit"
              class="inline-flex items-center justify-center gap-2 rounded-lg bg-navy-900 dark:bg-indigo-600 px-5 py-2.5 text-sm font-semibold text-white transition hover:bg-navy-800 dark:hover:bg-indigo-700 cursor-pointer"
            >
              <Check class="h-4 w-4" aria-hidden="true" />
              {{ t('Save changes') }}
            </button>
          </div>
        </form>

        <div v-else class="space-y-5">
          <!-- Profile Photo Card -->
          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs overflow-hidden">
            <div class="flex flex-col sm:flex-row items-center sm:items-start gap-5 p-5 sm:p-6">
              <div class="relative group shrink-0">
                <div class="flex h-20 w-20 sm:h-24 sm:w-24 items-center justify-center rounded-2xl border-2 border-slate-200 dark:border-slate-700 bg-navy-50 dark:bg-slate-800 text-2xl font-black text-navy-800 dark:text-white shadow-xs overflow-hidden">
                  <img
                    v-if="profile.avatarUrl && !avatarLoadFailed"
                    :src="resolveImageUrl(profile.avatarUrl)"
                    :alt="profile.fullName"
                    class="h-full w-full object-cover"
                    @error="onAvatarError"
                  />
                  <span v-else>{{ initials }}</span>
                </div>
                <button
                  type="button"
                  class="absolute inset-0 bg-black/40 opacity-0 group-hover:opacity-100 transition-opacity flex flex-col items-center justify-center text-white text-xs font-bold rounded-2xl cursor-pointer"
                  :title="t('Change profile photo')"
                  @click="triggerAvatarUpload"
                >
                  <Camera class="w-5 h-5 mb-1" />
                  <span>{{ t('Change') }}</span>
                </button>
              </div>

              <div class="space-y-1.5 text-center sm:text-left flex-1 min-w-0">
                <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2">
                  <h3 class="text-sm font-bold text-navy-900 dark:text-white">{{ t('Profile photo') }}</h3>
                  <span v-if="profile.avatarUrl && !avatarLoadFailed" class="text-[11px] font-semibold text-emerald-600 dark:text-emerald-400 bg-emerald-50 dark:bg-emerald-950/50 px-2 py-0.5 rounded-full border border-emerald-200 dark:border-emerald-800/60">
                    Active
                  </span>
                </div>
                <p class="text-xs text-slate-500 dark:text-slate-400 leading-relaxed max-w-lg">
                  {{ t('Upload a photo or avatar image. Recommended size: at least 256x256 px (JPG, PNG, or WebP).') }}
                </p>
                <div class="flex flex-wrap items-center justify-center sm:justify-start gap-2.5 pt-2">
                  <button
                    type="button"
                    class="inline-flex items-center gap-1.5 rounded-lg bg-navy-900 dark:bg-indigo-600 px-3.5 py-2 text-xs font-semibold text-white hover:bg-navy-800 dark:hover:bg-indigo-500 shadow-2xs transition cursor-pointer"
                    :disabled="avatarUploading"
                    @click="triggerAvatarUpload"
                  >
                    <RefreshCw v-if="avatarUploading" class="h-3.5 w-3.5 animate-spin" />
                    <Upload v-else class="h-3.5 w-3.5" />
                    <span>{{ avatarUploading ? 'Uploading...' : (profile.avatarUrl && !avatarLoadFailed ? t('Change photo') : t('Upload photo')) }}</span>
                  </button>
                  <button
                    v-if="profile.avatarUrl && !avatarLoadFailed"
                    type="button"
                    class="inline-flex items-center gap-1.5 rounded-lg border border-red-200 dark:border-red-900/60 bg-red-50/60 dark:bg-red-950/40 px-3.5 py-2 text-xs font-semibold text-red-700 dark:text-red-400 hover:bg-red-100 dark:hover:bg-red-900/50 transition cursor-pointer"
                    @click="removeAvatar"
                  >
                    <Trash2 class="h-3.5 w-3.5" />
                    <span>{{ t('Remove photo') }}</span>
                  </button>
                </div>
              </div>
            </div>
          </section>

          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs">
            <div class="flex flex-col gap-4 border-b border-slate-100 dark:border-slate-800 px-5 py-5 sm:flex-row sm:items-center sm:justify-between sm:px-7">
              <div class="flex items-center gap-3">
                <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
                  <UserRound class="h-5 w-5" aria-hidden="true" />
                </span>
                <div>
                  <h2 class="text-base font-bold text-navy-900 dark:text-white">{{ t('Personal details') }}</h2>
                  <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-400">{{ t('Your contact and personal information.') }}</p>
                </div>
              </div>
              <button
                type="button"
                class="inline-flex items-center justify-center gap-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 px-3.5 py-2 text-xs font-semibold text-navy-900 dark:text-white transition hover:border-navy-800 dark:hover:border-slate-600 hover:bg-navy-50 dark:hover:bg-slate-700 cursor-pointer"
                @click="startEditing"
              >
                <Pencil class="h-3.5 w-3.5" aria-hidden="true" />
                {{ hasProfile ? t('Edit profile') : t('Add profile details') }}
              </button>
            </div>
            <dl class="grid gap-x-6 sm:grid-cols-2">
              <ProfileDetail label="Full name" :value="profile.fullName" :icon="UserRound" />
              <ProfileDetail label="Email address" :value="profile.email" :icon="Mail" />
              <ProfileDetail label="Phone number" :value="profile.phone" :icon="Phone" />
              <ProfileDetail label="Telegram username" :value="profile.telegram" :icon="Send" />
              <ProfileDetail label="Date of birth" :value="formattedDate" :icon="CalendarDays" />
              <ProfileDetail label="City or province" :value="profile.location" :icon="MapPin" />
            </dl>
          </section>

          <section class="rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xs">
            <div class="flex items-center gap-3 border-b border-slate-100 dark:border-slate-800 px-5 py-5 sm:px-7">
              <span class="flex h-10 w-10 items-center justify-center rounded-xl bg-navy-50 dark:bg-slate-800 text-navy-800 dark:text-slate-200">
                <GraduationCap class="h-5 w-5" aria-hidden="true" />
              </span>
              <div>
                <h2 class="text-base font-bold text-navy-900 dark:text-white">{{ t('Learning background') }}</h2>
                <p class="mt-0.5 text-xs text-slate-500 dark:text-slate-400">{{ t('Your education and experience.') }}</p>
              </div>
            </div>
            <dl class="grid gap-x-6 sm:grid-cols-2">
              <ProfileDetail label="Highest qualification" :value="displayQualification" :icon="GraduationCap" />
              <ProfileDetail label="Current occupation" :value="profile.occupation" :icon="BriefcaseBusiness" />
              <ProfileDetail label="Coding experience" :value="profile.experience" :icon="Code2" />
            </dl>
          </section>

          <p class="px-1 text-xs leading-5 text-slate-500 dark:text-slate-400">
            {{ t('Your account details and profile information are securely saved to your account.') }}
          </p>

        </div>
      </div>
    </div>

    <div
      v-if="logoutDialogOpen"
      class="fixed inset-0 z-[60] flex items-center justify-center bg-slate-950/40 px-4 py-6"
      @click.self="logoutDialogOpen = false"
    >
      <section
        role="dialog"
        aria-modal="true"
        :aria-labelledby="'logout-dialog-title'"
        class="w-full max-w-md rounded-2xl bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-6 shadow-xl"
      >
        <div class="flex h-11 w-11 items-center justify-center rounded-xl bg-red-50 dark:bg-red-950/60 text-red-600 dark:text-red-400">
          <LogOut class="h-5 w-5" aria-hidden="true" />
        </div>
        <h2 id="logout-dialog-title" class="mt-4 text-lg font-bold text-navy-900 dark:text-white">{{ t('Log out of your account?') }}</h2>
        <p class="mt-2 text-sm leading-6 text-slate-500 dark:text-slate-400">
          {{ t('You will be signed out of this account on this device.') }}
        </p>
        <div class="mt-6 flex justify-end gap-3">
          <button
            type="button"
            class="rounded-lg border border-slate-300 dark:border-slate-600 px-4 py-2.5 text-sm font-semibold text-slate-700 dark:text-slate-300 hover:bg-slate-50 dark:hover:bg-slate-700 cursor-pointer"
            @click="logoutDialogOpen = false"
          >
            {{ t('Cancel') }}
          </button>
          <button
            type="button"
            class="rounded-lg bg-red-600 px-4 py-2.5 text-sm font-semibold text-white hover:bg-red-700 cursor-pointer"
            @click="confirmLogout"
          >
            {{ t('Log out') }}
          </button>
        </div>
      </section>
    </div>

    <!-- 3D Print Order Review Modal -->
    <div
      v-if="reviewModalOpen && reviewingOrder"
      class="fixed inset-0 z-[60] flex items-center justify-center bg-slate-950/60 dark:bg-black/75 backdrop-blur-xs px-4 py-6"
      @click.self="reviewModalOpen = false"
    >
      <section
        role="dialog"
        aria-modal="true"
        class="w-full max-w-lg rounded-2xl bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-800 shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150"
      >
        <!-- Modal Header -->
        <div class="flex items-center justify-between border-b border-slate-100 dark:border-slate-800 px-6 py-4 bg-slate-50/50 dark:bg-slate-800/40">
          <div class="flex items-center gap-3">
            <div class="flex h-10 w-10 items-center justify-center rounded-xl bg-amber-100 dark:bg-amber-950/60 text-amber-600 dark:text-amber-400">
              <Star class="h-5 w-5 fill-amber-400 text-amber-500" />
            </div>
            <div>
              <h2 class="text-base font-extrabold text-navy-900 dark:text-white">
                {{ t('Review Your 3D Print Order') }}
              </h2>
              <p class="text-xs text-slate-500 dark:text-slate-400 mt-0.5">
                #{{ reviewingOrder.order_number || reviewingOrder.id }} · {{ t('Completed') }}
              </p>
            </div>
          </div>
          <button
            type="button"
            @click="reviewModalOpen = false"
            class="p-2 rounded-xl text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 hover:bg-slate-100 dark:hover:bg-slate-800 cursor-pointer transition"
          >
            <X class="w-5 h-5" />
          </button>
        </div>

        <!-- Modal Body -->
        <div class="p-6 space-y-5 text-xs">
          <!-- Star Rating -->
          <div class="text-center space-y-2 py-2">
            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300">
              {{ t('Rating') }}
            </label>
            <div class="flex items-center justify-center gap-2">
              <button
                v-for="star in 5"
                :key="star"
                type="button"
                @mouseenter="reviewRatingHover = star"
                @mouseleave="reviewRatingHover = 0"
                @click="reviewRating = star"
                class="p-1 transition-transform hover:scale-125 cursor-pointer focus:outline-hidden"
              >
                <Star
                  class="h-8 w-8 transition-colors"
                  :class="star <= (reviewRatingHover || reviewRating) ? 'fill-amber-400 text-amber-500' : 'text-slate-300 dark:text-slate-700'"
                />
              </button>
            </div>
            <p
              class="text-sm font-bold transition-colors"
              :class="(reviewRatingHover || reviewRating) > 0 ? 'text-navy-900 dark:text-white' : 'text-slate-400 dark:text-slate-500 font-medium'"
            >
              {{ getRatingLabel(reviewRatingHover || reviewRating) }}
            </p>
          </div>

          <!-- Quick Feedback Tags -->
          <div class="space-y-2">
            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300">
              {{ t('What did you like most?') }}
            </label>
            <div class="flex flex-wrap gap-2">
              <button
                v-for="tag in availableReviewTags"
                :key="tag"
                type="button"
                @click="toggleReviewTag(tag)"
                class="px-3 py-1.5 rounded-full text-xs font-semibold transition border cursor-pointer"
                :class="reviewTags.includes(tag)
                  ? 'bg-amber-100 dark:bg-amber-950/60 text-amber-900 dark:text-amber-200 border-amber-300 dark:border-amber-700 ring-1 ring-amber-400/30'
                  : 'bg-slate-50 dark:bg-slate-800 text-slate-600 dark:text-slate-300 border-slate-200 dark:border-slate-700 hover:bg-slate-100 dark:hover:bg-slate-700'"
              >
                <span v-if="reviewTags.includes(tag)" class="mr-1">✓</span>
                {{ t(tag) }}
              </button>
            </div>
          </div>

          <!-- Written Comment -->
          <div class="space-y-1.5">
            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300">
              {{ t('Detailed Feedback (Optional)') }}
            </label>
            <textarea
              v-model="reviewComment"
              rows="3"
              maxlength="500"
              class="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 p-3 text-xs text-slate-900 dark:text-white placeholder-slate-400 focus:border-navy-900 focus:outline-hidden dark:focus:border-indigo-500 transition"
              :placeholder="t('Tell us about the print tolerances, surface smoothness, turnaround speed, or service...')"
            ></textarea>
            <div class="flex justify-end text-[10px] text-slate-400">
              {{ reviewComment.length }} / 500
            </div>
          </div>

          <!-- Reviewer Name -->
          <div class="space-y-1.5">
            <label class="block text-xs font-bold text-slate-700 dark:text-slate-300">
              {{ t('Your Display Name') }}
            </label>
            <input
              v-model="reviewerName"
              type="text"
              maxlength="60"
              class="w-full rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 px-3 py-2 text-xs text-slate-900 dark:text-white focus:border-navy-900 focus:outline-hidden dark:focus:border-indigo-500 transition"
              placeholder="e.g. Sokha Chan"
            />
          </div>
        </div>

        <!-- Modal Footer -->
        <div class="border-t border-slate-100 dark:border-slate-800 px-6 py-4 bg-slate-50/50 dark:bg-slate-800/40 flex items-center justify-end gap-3">
          <button
            type="button"
            @click="reviewModalOpen = false"
            class="px-4 py-2 rounded-xl text-xs font-semibold text-slate-600 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition cursor-pointer"
          >
            {{ t('Cancel') }}
          </button>
          <button
            type="button"
            :disabled="isSubmittingReview || !reviewRating || reviewRating <= 0"
            @click="submitReviewHandler"
            class="inline-flex items-center gap-1.5 rounded-xl bg-navy-900 dark:bg-indigo-600 hover:bg-navy-800 dark:hover:bg-indigo-700 px-5 py-2 text-xs font-bold text-white transition shadow-sm cursor-pointer disabled:opacity-50 disabled:cursor-not-allowed"
          >
            <RefreshCw v-if="isSubmittingReview" class="h-3.5 w-3.5 animate-spin" />
            <Star v-else class="h-3.5 w-3.5 fill-amber-400 text-amber-500" />
            {{ isSubmittingReview ? t('Submitting...') : t('Submit Review') }}
          </button>
        </div>
      </section>
    </div>
  </div>
</template>

<script setup>
import { computed, defineComponent, h, onBeforeUnmount, onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useLanguage } from '../i18n'
import DatePicker from '../components/common/DatePicker.vue'
import { accountService, enrollmentService, printOrderService } from '../services/api'
import { formatCambodiaTime } from '../utils/date'
import { resolveImageUrl } from '../utils/image'
import { useTheme } from '../composables/useTheme'
import {
  AlertCircle,
  ArrowRight,
  BookOpen,
  Box,
  BriefcaseBusiness,
  CalendarDays,
  Camera,
  Check,
  CheckCircle2,
  ChevronDown,
  Code2,
  Download,
  FileText,
  GraduationCap,
  Globe2,
  HelpCircle,
  Lock,
  LogOut,
  Mail,
  MapPin,
  Moon,
  Pencil,
  Phone,
  Printer,
  RefreshCw,
  Send,
  Settings,
  ShieldCheck,
  ShoppingBag,
  Sparkles,
  Star,
  Sun,
  Trash2,
  Upload,
  UserCheck,
  UserRound,
  X,
} from 'lucide-vue-next'

const { locale, setLocale, t } = useLanguage()
const { isDark, toggleTheme, setTheme } = useTheme()
const router = useRouter()
const accountSections = [
  { id: 'profile', label: 'Profile information', icon: UserRound },
  { id: 'history', label: 'Course history', icon: BookOpen },
  { id: 'orders', label: '3D Print orders', icon: Printer },
  { id: 'settings', label: 'Settings', icon: Settings },
]

const activeSectionTitle = computed(() => {
  switch (activeSection.value) {
    case 'history': return t('Course history')
    case 'orders': return t('3D Print orders')
    case 'settings': return t('Settings')
    default: return t('Profile information')
  }
})

const activeSectionDescription = computed(() => {
  switch (activeSection.value) {
    case 'history': return t('Review your registrations and payment status.')
    case 'orders': return t('Track 3D CAD files you submitted for quotation and printing.')
    case 'settings': return t('Manage your language and local profile preferences.')
    default: return t('Keep your contact and learning details up to date so we can make your AeroByte experience more personal.')
  }
})
const emptyProfile = () => ({
  fullName: '',
  email: '',
  avatarUrl: '',
  phone: '',
  telegram: '',
  dateOfBirth: '',
  location: '',
  qualification: '',
  qualificationOther: '',
  occupation: '',
  experience: '',
})

function getActiveUserCredentials() {
  let uid = ''
  let uemail = ''
  let uname = ''
  let utg = ''

  try {
    const rawSess = localStorage.getItem('aerobyte_user_session')
    if (rawSess) {
      const sess = JSON.parse(rawSess)
      const u = sess.user || sess
      if (u) {
        if (!uid && u.id) uid = u.id
        if (!uemail && u.email) uemail = u.email
        if (!uname && (u.name || u.full_name)) uname = u.name || u.full_name
        if (!utg && u.telegram) utg = u.telegram
      }
    }
  } catch (_) {}

  try {
    const rawProf = localStorage.getItem('aerobyte-profile-current') || localStorage.getItem('aerobyte-profile')
    if (rawProf) {
      const p = JSON.parse(rawProf)
      if (p) {
        if (!uid && p.id) uid = p.id
        if (!uemail && p.email) uemail = p.email
        if (!uname && p.fullName) uname = p.fullName
        if (!utg && p.telegram) utg = p.telegram
      }
    }
  } catch (_) {}

  if (!uemail) {
    try {
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i)
        if (k && k.startsWith('aerobyte-profile:')) {
          const val = JSON.parse(localStorage.getItem(k) || '{}')
          if (val.email) {
            uemail = val.email
            if (!uname && val.fullName) uname = val.fullName
            break
          }
        }
      }
    } catch (_) {}
  }

  return { id: uid, email: uemail, name: uname, telegram: utg }
}

function readCachedPrintOrders() {
  try {
    const raw = localStorage.getItem('aerobyte_print_orders')
    if (raw) {
      const parsed = JSON.parse(raw)
      if (Array.isArray(parsed) && parsed.length) return parsed
    }
  } catch (_) {}
  return []
}

function readCachedStoreOrders() {
  try {
    const raw = localStorage.getItem('aerobyte_store_orders')
    if (raw) {
      const parsed = JSON.parse(raw)
      if (Array.isArray(parsed) && parsed.length) return parsed
    }
  } catch (_) {}
  return []
}

const initialCreds = getActiveUserCredentials()
const account = ref(initialCreds.id ? { id: initialCreds.id, email: initialCreds.email, name: initialCreds.name, telegram: initialCreds.telegram } : null)
const profile = reactive({
  ...emptyProfile(),
  fullName: initialCreds.name || '',
  email: initialCreds.email || '',
  telegram: initialCreds.telegram || '',
})
const draft = reactive({ ...profile })
const storageKey = computed(() => account.value ? `aerobyte-profile:${account.value.id}` : 'aerobyte-profile')
const storageEmailKey = computed(() => (account.value?.email || profile.email) ? `aerobyte-profile:${(account.value?.email || profile.email).toLowerCase()}` : null)
const historyStorageKey = computed(() => account.value ? `aerobyte-course-history:${account.value.id}` : 'aerobyte-course-history')
const historyEmailKey = computed(() => (account.value?.email || profile.email) ? `aerobyte-course-history:${(account.value?.email || profile.email).toLowerCase()}` : null)
const isEditing = ref(false)
const notice = ref('')
const noticeType = ref('success')
const activeSection = ref(
  ['orders', 'history', 'settings'].includes(router.currentRoute.value.query.section)
    ? router.currentRoute.value.query.section
    : 'profile'
)
const printOrders = ref(readCachedPrintOrders())
const printOrdersLoading = ref(false)
const storeOrders = ref(readCachedStoreOrders())
const ordersLoading = ref(false)

function getPrintStatusBadge(status) {
  const s = String(status || '').toLowerCase()
  if (s.includes('ready') || s.includes('complete') || s.includes('delivered')) {
    return {
      bg: 'bg-emerald-50 dark:bg-emerald-950/60 text-emerald-700 dark:text-emerald-300 border-emerald-200 dark:border-emerald-800/60',
      dot: 'bg-emerald-500',
    }
  }
  if (s.includes('production') || s.includes('printing')) {
    return {
      bg: 'bg-purple-50 dark:bg-purple-950/60 text-purple-700 dark:text-purple-300 border-purple-200 dark:border-purple-800/60',
      dot: 'bg-purple-500',
    }
  }
  if (s.includes('quoted')) {
    return {
      bg: 'bg-blue-50 dark:bg-blue-950/60 text-blue-700 dark:text-blue-300 border-blue-200 dark:border-blue-800/60',
      dot: 'bg-blue-500',
    }
  }
  if (s.includes('cancel')) {
    return {
      bg: 'bg-rose-50 dark:bg-rose-950/60 text-rose-700 dark:text-rose-300 border-rose-200 dark:border-rose-800/60',
      dot: 'bg-rose-500',
    }
  }
  return {
    bg: 'bg-amber-50 dark:bg-amber-950/60 text-amber-700 dark:text-amber-300 border-amber-200 dark:border-amber-800/60',
    dot: 'bg-amber-500',
  }
}

function getOrderTelegramLink(order) {
  const orderNum = order.order_number || order.id || ''
  const text = encodeURIComponent(
    `Hello AeroByte team! I would like to check on my 3D print order #${orderNum}.\nParts: ${order.total_parts || (order.files ? order.files.length : 1)}`
  )
  return `https://t.me/aerobyte168?text=${text}`
}

function getCadFileUrl(file) {
  if (file.download_url) {
    if (file.download_url.startsWith('http://') || file.download_url.startsWith('https://')) {
      return file.download_url
    }
    if (file.download_url.startsWith('/api')) {
      return file.download_url
    }
    return `/api${file.download_url.startsWith('/') ? '' : '/'}${file.download_url}`
  }
  if (file.stored_filename) {
    return printOrderService.getFileDownloadUrl(file.stored_filename, file.original_name)
  }
  return '#'
}

function isPrintOrderCompleted(order) {
  if (!order) return false
  const s = String(order.status || '').toLowerCase()
  return s.includes('complete') || s === 'completed'
}

// 3D Print Order Review State & Methods
const reviewModalOpen = ref(false)
const reviewingOrder = ref(null)
const reviewRating = ref(0)
const reviewRatingHover = ref(0)
const reviewComment = ref('')
const reviewTags = ref([])
const reviewerName = ref('')
const isSubmittingReview = ref(false)

const availableReviewTags = [
  'Clean layer lines',
  'Strong & sturdy',
  'Accurate dimensions',
  'Smooth finish',
  'Fast turnaround',
  'Great support',
]

function getRatingLabel(rating) {
  if (!rating || rating === 0) return t('Select your rating (1 to 5 stars)')
  if (rating >= 5) return t('Outstanding print quality!')
  if (rating === 4) return t('Very good')
  if (rating === 3) return t('Good quality')
  if (rating === 2) return t('Fair')
  return t('Needs improvement')
}

function openReviewModal(order) {
  reviewingOrder.value = order
  if (order.review && order.review.rating) {
    reviewRating.value = Number(order.review.rating) || 0
    reviewComment.value = order.review.comment || ''
    reviewTags.value = Array.isArray(order.review.tags) ? [...order.review.tags] : []
    reviewerName.value = order.review.reviewer_name || order.customer_name || profile.fullName || ''
  } else {
    reviewRating.value = 0
    reviewComment.value = ''
    reviewTags.value = []
    reviewerName.value = order.customer_name || profile.fullName || account.value?.name || ''
  }
  reviewRatingHover.value = 0
  reviewModalOpen.value = true
}

function toggleReviewTag(tag) {
  const idx = reviewTags.value.indexOf(tag)
  if (idx >= 0) {
    reviewTags.value.splice(idx, 1)
  } else {
    reviewTags.value.push(tag)
  }
}

async function submitReviewHandler() {
  if (!reviewingOrder.value || !reviewRating.value || reviewRating.value <= 0) return
  isSubmittingReview.value = true
  const orderId = reviewingOrder.value.order_number || reviewingOrder.value.id

  const payload = {
    rating: reviewRating.value,
    comment: reviewComment.value.trim(),
    tags: reviewTags.value,
    reviewer_name: reviewerName.value.trim() || profile.fullName || 'Customer',
    created_at: new Date().toISOString(),
  }

  try {
    const res = await printOrderService.submitReview(orderId, payload)
    if (res?.data?.order?.review) {
      reviewingOrder.value.review = res.data.order.review
    } else {
      reviewingOrder.value.review = payload
    }
  } catch (err) {
    console.warn('Backend review submission failed, saving locally:', err)
    reviewingOrder.value.review = payload
  } finally {
    // Synchronize local cached orders
    try {
      const local = JSON.parse(localStorage.getItem('aerobyte_print_orders') || '[]')
      const targetId = reviewingOrder.value.order_number || reviewingOrder.value.id
      const match = local.find((o) => (o.order_number === targetId || o.id === targetId))
      if (match) {
        match.review = reviewingOrder.value.review
      } else {
        local.unshift(reviewingOrder.value)
      }
      localStorage.setItem('aerobyte_print_orders', JSON.stringify(local))
    } catch (_) {}

    // Also sync admin cache if present on same browser
    try {
      const adminLocal = JSON.parse(localStorage.getItem('aerobyte_admin_print_orders') || '[]')
      const targetId = reviewingOrder.value.order_number || reviewingOrder.value.id
      const adminMatch = adminLocal.find((o) => (o.order_number === targetId || o.id === targetId))
      if (adminMatch) {
        adminMatch.review = reviewingOrder.value.review
        localStorage.setItem('aerobyte_admin_print_orders', JSON.stringify(adminLocal))
      }
    } catch (_) {}

    window.dispatchEvent(new Event('aerobyte-orders-updated'))

    isSubmittingReview.value = false
    reviewModalOpen.value = false
    notice.value = t('Review submitted successfully!')
    noticeType.value = 'success'
  }
}

async function loadPrintOrders(forceRefresh = false) {
  if (!printOrders.value.length || forceRefresh) {
    printOrdersLoading.value = true
  }

  // 1. Read cached orders from localStorage for 0ms hydration
  try {
    const raw = localStorage.getItem('aerobyte_print_orders')
    if (raw) {
      const parsed = JSON.parse(raw)
      if (Array.isArray(parsed) && parsed.length) {
        printOrders.value = parsed
      }
    }
  } catch (_) {}

  // 2. Immediately synchronize with aerobyte_admin_print_orders if updated via admin on same browser
  try {
    const adminRaw = localStorage.getItem('aerobyte_admin_print_orders')
    if (adminRaw) {
      const adminParsed = JSON.parse(adminRaw)
      if (Array.isArray(adminParsed) && adminParsed.length) {
        const adminMap = new Map()
        for (const ao of adminParsed) {
          const k = String(ao.order_number || ao.id || '').replace(/^#/, '')
          if (k) adminMap.set(k, ao)
        }
        let updated = false
        for (const po of printOrders.value) {
          const pk = String(po.order_number || po.id || '').replace(/^#/, '')
          if (pk && adminMap.has(pk)) {
            const ao = adminMap.get(pk)
            if (ao.status && ao.status !== po.status) {
              po.status = ao.status
              updated = true
            }
            if (ao.review && !po.review) {
              po.review = ao.review
              updated = true
            }
            const adminP = Number(ao.price || ao.estimated_price || 0)
            if (adminP > 0 && (po.price !== adminP || po.estimated_price !== adminP)) {
              po.price = adminP
              po.estimated_price = adminP
              updated = true
            }
          }
        }
        if (updated) {
          localStorage.setItem('aerobyte_print_orders', JSON.stringify(printOrders.value))
        }
      }
    }
  } catch (_) {}

  // 3. Fetch latest status from backend
  try {
    const creds = getActiveUserCredentials()
    const userEmail = creds.email || account.value?.email || profile.email || ''
    const userTg = creds.telegram || account.value?.telegram || profile.telegram || ''
    const userName = creds.name || account.value?.name || profile.fullName || ''
    const userId = creds.id || account.value?.id || ''
    const knownIds = printOrders.value.map((o) => String(o.order_number || o.id || '').replace(/^#/, '')).filter(Boolean)

    let serverOrders = []
    try {
      const queryParams = {}
      if (userEmail) queryParams.email = userEmail
      if (userTg) queryParams.telegram = userTg
      if (userName) queryParams.name = userName
      if (knownIds.length) queryParams.order_ids = knownIds.join(',')
      const res = await accountService.getUserPrintOrders(queryParams)
      if (Array.isArray(res.data)) {
        serverOrders = res.data
      }
    } catch (e1) {
      try {
        const queryParams2 = {}
        if (userId) queryParams2.user_id = userId
        if (userEmail) queryParams2.email = userEmail
        if (userTg) queryParams2.telegram = userTg
        if (userName) queryParams2.name = userName
        if (knownIds.length) queryParams2.order_ids = knownIds.join(',')
        const res2 = await printOrderService.getMyOrders(queryParams2)
        if (Array.isArray(res2.data?.orders)) {
          serverOrders = res2.data.orders
        }
      } catch (e2) {}
    }

    if (serverOrders.length) {
      const serverMap = new Map()
      for (const so of serverOrders) {
        const sk = String(so.order_number || so.id || '').replace(/^#/, '')
        if (sk) serverMap.set(sk, so)
      }

      // Update existing orders with fresh status and data from server
      for (const loc of printOrders.value) {
        const lk = String(loc.order_number || loc.id || '').replace(/^#/, '')
        if (lk && serverMap.has(lk)) {
          const fresh = serverMap.get(lk)
          loc.status = fresh.status || loc.status
          if (fresh.review) loc.review = fresh.review
          if (fresh.estimated_price !== undefined || fresh.price !== undefined) {
            loc.price = Number(fresh.price || fresh.estimated_price || 0)
            loc.estimated_price = Number(fresh.estimated_price || fresh.price || 0)
          }
          serverMap.delete(lk)
        }
      }

      // Prepend any server orders that were not already in local cache
      for (const remaining of serverMap.values()) {
        printOrders.value.unshift(remaining)
      }

      try {
        localStorage.setItem('aerobyte_print_orders', JSON.stringify(printOrders.value))
      } catch (_) {}
    } else if (knownIds.length) {
      // Fallback: poll individual known order status directly
      for (const id of knownIds) {
        try {
          const res = await printOrderService.getOrder(id)
          if (res?.data?.order) {
            const fresh = res.data.order
            const match = printOrders.value.find((o) => String(o.order_number || o.id || '').replace(/^#/, '') === id)
            if (match) {
              if (fresh.status && match.status !== fresh.status) {
                match.status = fresh.status
              }
              if (fresh.review) match.review = fresh.review
              if (fresh.estimated_price !== undefined || fresh.price !== undefined) {
                match.price = Number(fresh.price || fresh.estimated_price || 0)
                match.estimated_price = Number(fresh.estimated_price || fresh.price || 0)
              }
            }
          }
        } catch (_) {}
      }
      try {
        localStorage.setItem('aerobyte_print_orders', JSON.stringify(printOrders.value))
      } catch (_) {}
    }
  } catch (err) {
    console.warn('Could not load print orders from server, using local cache:', err)
  } finally {
    printOrdersLoading.value = false
  }
}

async function loadStoreOrders() {
  ordersLoading.value = true
  try {
    // 1. Fetch persistent orders from database
    const { data } = await accountService.getUserOrders()
    const serverOrders = Array.isArray(data) ? data : []

    // 2. Check if there are local orders created before login that can be synced
    try {
      const raw = localStorage.getItem('aerobyte_store_orders')
      const localOrders = raw ? JSON.parse(raw) : []
      const serverOrderIds = new Set(serverOrders.map((o) => o.id))
      for (const localOrder of localOrders) {
        if (!serverOrderIds.has(localOrder.id)) {
          try {
            await accountService.createStoreOrder({
              id: localOrder.id,
              name: localOrder.customer?.name || localOrder.name || account.value?.name || 'Customer',
              phone: localOrder.customer?.phone || localOrder.phone || account.value?.phone || '',
              telegram: localOrder.customer?.telegram || localOrder.telegram || '',
              address: localOrder.customer?.address || localOrder.address || '',
              fulfillment: localOrder.fulfillment || 'pickup',
              items: localOrder.items || [],
              subtotal: localOrder.subtotal || 0,
              delivery_fee: localOrder.delivery_fee || localOrder.deliveryFee || 0,
              discount: localOrder.discount || 0,
              total: localOrder.total || 0,
            })
            serverOrders.unshift(localOrder)
          } catch (syncErr) {
            console.warn('Could not sync local order to database:', syncErr)
          }
        }
      }
    } catch (_) {}

    storeOrders.value = serverOrders
    try {
      localStorage.setItem('aerobyte_store_orders', JSON.stringify(serverOrders))
    } catch {}
    return
  } catch (e) {
    console.warn('Could not fetch store orders from server, using local cache:', e)
  } finally {
    ordersLoading.value = false
  }

  try {
    const raw = localStorage.getItem('aerobyte_store_orders')
    storeOrders.value = raw ? JSON.parse(raw) : []
  } catch (e) {
    console.error('Failed to parse store orders', e)
    storeOrders.value = []
  }
}

const courseHistory = ref([])
const historyLoading = ref(false)
const historyError = ref('')
const logoutDialogOpen = ref(false)
const avatarFileInput = ref(null)
const avatarUploading = ref(false)
const avatarLoadFailed = ref(false)

const qualificationDropdownRef = ref(null)
const qualificationDropdownOpen = ref(false)
const experienceDropdownRef = ref(null)
const experienceDropdownOpen = ref(false)
const languageDropdownRef = ref(null)
const languageDropdownOpen = ref(false)

const qualificationOptions = [
  'High school',
  'Undergraduate / University',
  'Graduate degree',
  'Other',
]

const experienceOptions = [
  'New to coding',
  'Some experience',
  'Confident coder',
  'Experienced developer',
]

function selectQualification(option) {
  draft.qualification = option
  qualificationDropdownOpen.value = false
}

function selectExperience(option) {
  draft.experience = option
  experienceDropdownOpen.value = false
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
  draft.phone = filtered
  event.target.value = filtered
}

function handleDropdownClickOutside(event) {
  if (qualificationDropdownRef.value && !qualificationDropdownRef.value.contains(event.target)) {
    qualificationDropdownOpen.value = false
  }
  if (experienceDropdownRef.value && !experienceDropdownRef.value.contains(event.target)) {
    experienceDropdownOpen.value = false
  }
  if (languageDropdownRef.value && !languageDropdownRef.value.contains(event.target)) {
    languageDropdownOpen.value = false
  }
}

const completion = computed(() => {
  const hasAvatar = Boolean(
    profile.avatarUrl?.trim() &&
    !avatarLoadFailed.value &&
    !profile.avatarUrl.includes('avatar_ff685636-ad2f-434a-86f2-89406c51962a_11f4b3349942')
  )
  const fields = [
    Boolean(profile.fullName?.trim()),
    Boolean(profile.email?.trim()),
    hasAvatar,
    Boolean(profile.phone?.trim()),
    Boolean(profile.telegram?.trim()),
    Boolean(profile.dateOfBirth?.trim()),
    Boolean(profile.location?.trim()),
    Boolean(
      profile.qualification?.trim() &&
      (profile.qualification !== 'Other' || profile.qualificationOther?.trim())
    ),
    Boolean(profile.occupation?.trim()),
    Boolean(profile.experience?.trim()),
  ]
  const completedCount = fields.filter(Boolean).length
  return Math.round((completedCount / fields.length) * 100)
})
const hasProfile = computed(() => Object.values(profile).some((value) => value.trim()))
const displayQualification = computed(() =>
  profile.qualification === 'Other'
    ? profile.qualificationOther || t('Other')
    : profile.qualification,
)
const initials = computed(() => {
  const names = profile.fullName.trim().split(/\s+/).filter(Boolean)
  return names.length ? names.slice(0, 2).map((name) => name[0].toUpperCase()).join('') : 'AA'
})
const formattedDate = computed(() => {
  if (!profile.dateOfBirth) return ''
  const date = new Date(`${profile.dateOfBirth}T00:00:00`)
  return Number.isNaN(date.getTime())
    ? profile.dateOfBirth
    : new Intl.DateTimeFormat('en', { dateStyle: 'long' }).format(date)
})

const ProfileDetail = defineComponent({
  props: {
    label: { type: String, required: true },
    value: { type: String, default: '' },
    icon: { type: [Object, Function], required: true },
  },
  setup(props) {
    return () =>
      h('div', { class: 'flex gap-3 border-b border-slate-100 dark:border-slate-800 px-5 py-4 last:border-0 sm:px-7' }, [
        h('span', { class: 'mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-slate-50 dark:bg-slate-800 text-slate-500 dark:text-slate-400' }, [
          h(props.icon, { class: 'h-4 w-4', 'aria-hidden': 'true' }),
        ]),
        h('div', { class: 'min-w-0' }, [
          h('dt', { class: 'text-[11px] font-semibold uppercase tracking-wide text-slate-400 dark:text-slate-400' }, props.label),
          h('dd', { class: ['mt-1 break-words text-sm font-medium', props.value ? 'text-slate-700 dark:text-slate-200' : 'text-slate-400 dark:text-slate-500'] }, props.value || t('Not added yet')),
        ]),
      ])
  },
})

function copyProfile(target, source) {
  Object.keys(target).forEach((key) => {
    let val = typeof source[key] === 'string' ? source[key] : ''
    if (key === 'avatarUrl' && val.includes('avatar_ff685636-ad2f-434a-86f2-89406c51962a_11f4b3349942')) {
      val = ''
    }
    target[key] = val
  })
}

onMounted(async () => {
  let hasLocalProfile = false

  // 1. Instant local pre-hydration on tick 0 before any network request
  try {
    const creds = getActiveUserCredentials()
    if (creds.name || creds.email || creds.telegram) {
      hasLocalProfile = true
    }
    const findCached = () => {
      const direct = localStorage.getItem('aerobyte-profile-current') || localStorage.getItem('aerobyte-profile')
      if (direct) {
        try {
          const parsed = JSON.parse(direct)
          if (parsed && (parsed.fullName || parsed.email || parsed.phone)) return parsed
        } catch (_) {}
      }
      for (let i = 0; i < localStorage.length; i++) {
        const k = localStorage.key(i)
        if (k && k.startsWith('aerobyte-profile:')) {
          try {
            const parsed = JSON.parse(localStorage.getItem(k) || '{}')
            if (parsed && (parsed.fullName || parsed.email || parsed.phone)) return parsed
          } catch (_) {}
        }
      }
      return null
    }
    const localCached = findCached()
    if (localCached) {
      hasLocalProfile = true
      copyProfile(profile, localCached)
      copyProfile(draft, localCached)
    }
  } catch (_) {}

  // 2. Instantly load orders and history in parallel (0ms delay!)
  loadPrintOrders()
  loadStoreOrders()
  loadCourseHistory()

  // 3. Fetch authenticated session from server
  try {
    const { data } = await accountService.getSession()
    if (!data.authenticated) {
      const rawSess = localStorage.getItem('aerobyte_user_session')
      let hasValidSess = false
      if (rawSess) {
        try {
          const parsed = JSON.parse(rawSess)
          if (parsed && (parsed.email || parsed.id)) hasValidSess = true
        } catch (_) {}
      }
      if (!hasValidSess) {
        await router.replace('/courses')
        return
      }
    } else {
      account.value = data.user
      try {
        localStorage.setItem('aerobyte_user_session', JSON.stringify(data.user))
      } catch (_) {}
      // Server data is single source of truth across all devices/browsers!
      if (account.value?.name) profile.fullName = account.value.name
      if (account.value?.email) profile.email = account.value.email
      if (account.value?.avatar_url && !account.value.avatar_url.includes('avatar_ff685636-ad2f-434a-86f2-89406c51962a_11f4b3349942')) {
        profile.avatarUrl = account.value.avatar_url
        avatarLoadFailed.value = false
      } else {
        profile.avatarUrl = ''
      }
      if (account.value?.phone) profile.phone = account.value.phone
      if (account.value?.telegram) profile.telegram = account.value.telegram
      if (account.value?.date_of_birth) profile.dateOfBirth = account.value.date_of_birth
      if (account.value?.gender) profile.gender = account.value.gender
      if (account.value?.location) profile.location = account.value.location
      if (account.value?.qualification) profile.qualification = account.value.qualification
      if (account.value?.qualification_other) profile.qualificationOther = account.value.qualification_other
      if (account.value?.occupation) profile.occupation = account.value.occupation
      if (account.value?.experience) profile.experience = account.value.experience
    }

    const pendingEnrollRedirect = sessionStorage.getItem('aerobyte_enroll_redirect')
    if (pendingEnrollRedirect && pendingEnrollRedirect.startsWith('/')) {
      sessionStorage.removeItem('aerobyte_enroll_redirect')
      await router.replace(pendingEnrollRedirect)
      return
    }

    // Merge server data with local cache for any offline fields
    let cached = {}
    try {
      const raw = (storageEmailKey.value && localStorage.getItem(storageEmailKey.value)) ||
                  (storageKey.value && localStorage.getItem(storageKey.value)) ||
                  localStorage.getItem('aerobyte-profile-current') ||
                  localStorage.getItem('aerobyte-profile')
      if (raw) {
        cached = JSON.parse(raw)
        // Only fill empty fields from local cache, server data is primary
        for (const k of Object.keys(profile)) {
          if (!profile[k] && cached[k]) {
            profile[k] = cached[k]
          }
        }
      }
    } catch (_) {}

    // Server data strictly takes precedence if present
    if (account.value?.name) profile.fullName = account.value.name
    if (account.value?.email) profile.email = account.value.email
    if (account.value?.avatar_url && !account.value.avatar_url.includes('avatar_ff685636-ad2f-434a-86f2-89406c51962a_11f4b3349942')) {
      profile.avatarUrl = account.value.avatar_url
      avatarLoadFailed.value = false
    } else {
      profile.avatarUrl = ''
    }
    if (account.value?.phone) profile.phone = account.value.phone
    if (account.value?.telegram) profile.telegram = account.value.telegram
    if (account.value?.date_of_birth) profile.dateOfBirth = account.value.date_of_birth
    if (account.value?.gender) profile.gender = account.value.gender
    if (account.value?.location) profile.location = account.value.location
    if (account.value?.qualification) profile.qualification = account.value.qualification
    if (account.value?.qualification_other) profile.qualificationOther = account.value.qualification_other
    if (account.value?.occupation) profile.occupation = account.value.occupation
    if (account.value?.experience) profile.experience = account.value.experience

    // If server had missing fields that were restored from local cache, auto-sync back to server!
    const hasLocalRestore = account.value && (
      (!account.value.phone && profile.phone) ||
      (!account.value.telegram && profile.telegram) ||
      (!account.value.date_of_birth && profile.dateOfBirth) ||
      (!account.value.gender && profile.gender) ||
      (!account.value.location && profile.location) ||
      (!account.value.qualification && profile.qualification) ||
      (!account.value.occupation && profile.occupation) ||
      (!account.value.experience && profile.experience)
    )
    if (hasLocalRestore) {
      accountService.updateProfile({
        full_name: profile.fullName,
        email: profile.email,
        avatar_url: profile.avatarUrl,
        phone: profile.phone,
        telegram: profile.telegram,
        date_of_birth: profile.dateOfBirth,
        gender: profile.gender,
        location: profile.location,
        qualification: profile.qualification,
        qualification_other: profile.qualificationOther,
        occupation: profile.occupation,
        experience: profile.experience,
      }).catch((err) => console.warn('Background profile auto-sync failed:', err))
    }

    // Save full authoritative profile back to local storage under all keys
    try {
      localStorage.setItem('aerobyte-profile-current', JSON.stringify(profile))
      if (storageEmailKey.value) localStorage.setItem(storageEmailKey.value, JSON.stringify(profile))
      if (storageKey.value) localStorage.setItem(storageKey.value, JSON.stringify(profile))
      localStorage.setItem('aerobyte-profile', JSON.stringify(profile))
    } catch (_) {}

    copyProfile(draft, profile)

    // Re-sync user's orders and history with confirmed session user
    if (account.value?.email) {
      loadPrintOrders(true)
      loadStoreOrders()
      loadCourseHistory()
    }
  } catch (error) {
    console.warn('Could not load session from server, maintaining cached state:', error)
    if (!profile.fullName && !profile.email) {
      notice.value = t('Unable to load your account. Please try again.')
      noticeType.value = 'error'
    }
  }

  const handleOrdersSync = (event) => {
    if (event?.detail?.orderId) {
      const cleanId = String(event.detail.orderId).replace(/^#/, '')
      const match = printOrders.value.find((o) => String(o.order_number || o.id || '').replace(/^#/, '') === cleanId)
      if (match) {
        if (event.detail.price !== undefined) {
          match.price = Number(event.detail.price)
          match.estimated_price = Number(event.detail.price)
        }
        if (event.detail.status !== undefined) {
          match.status = event.detail.status
        }
      }
    }
    loadPrintOrders()
    loadStoreOrders()
  }
  window.addEventListener('storage', handleOrdersSync)
  window.addEventListener('aerobyte-orders-updated', handleOrdersSync)
  const targetSection = router.currentRoute.value.query.section
  if (['orders', 'history', 'settings'].includes(targetSection)) {
    activeSection.value = targetSection
  }
  document.addEventListener('click', handleDropdownClickOutside)
})

onBeforeUnmount(() => {
  document.removeEventListener('click', handleDropdownClickOutside)
  window.removeEventListener('storage', handleOrdersSync)
  window.removeEventListener('aerobyte-orders-updated', handleOrdersSync)
})

function selectSection(section) {
  activeSection.value = section
  notice.value = ''
  if (section !== 'profile') isEditing.value = false
  if (section === 'history' && !courseHistory.value.length) loadCourseHistory()
  if (section === 'orders') {
    loadPrintOrders()
    loadStoreOrders()
  }
}

function statusClasses(status) {
  if (status === 'paid' || status === 'confirmed') return 'bg-emerald-50 text-emerald-700 dark:bg-emerald-950/40 dark:text-emerald-400'
  if (status === 'expired' || status === 'cancelled') return 'bg-red-50 text-red-700 dark:bg-red-950/40 dark:text-red-400'
  return 'bg-amber-50 text-amber-700 dark:bg-amber-950/40 dark:text-amber-400'
}

async function loadCourseHistory() {
  historyLoading.value = true
  historyError.value = ''
  try {
    let savedIds = []
    try {
      const parsed1 = JSON.parse(localStorage.getItem(historyStorageKey.value) || '[]')
      const parsed2 = JSON.parse((historyEmailKey.value && localStorage.getItem(historyEmailKey.value)) || '[]')
      const parsed3 = JSON.parse(localStorage.getItem('aerobyte-course-history') || '[]')
      const allParsed = [...(Array.isArray(parsed1) ? parsed1 : []), ...(Array.isArray(parsed2) ? parsed2 : []), ...(Array.isArray(parsed3) ? parsed3 : [])]
      savedIds = [...new Set(allParsed.filter((id) => typeof id === 'string' && id))]
    } catch (_) {}

    // Fetch user enrollments from the database by account email and/or cached IDs
    const userEmail = account.value?.email || profile.email || ''
    const { data } = await accountService.getUserEnrollments({
      email: userEmail,
      ids: savedIds.join(','),
    })

    const records = Array.isArray(data) ? data : []
    courseHistory.value = records

    // Cache enrollment IDs locally for offline fallback
    try {
      const allIds = [...new Set([...records.map((r) => r.enrollment_id), ...savedIds])]
      if (allIds.length > 0) {
        localStorage.setItem(historyStorageKey.value, JSON.stringify(allIds))
        if (historyEmailKey.value) {
          localStorage.setItem(historyEmailKey.value, JSON.stringify(allIds))
        }
        localStorage.setItem('aerobyte-course-history', JSON.stringify(allIds))
      }
    } catch (_) {}
  } catch (error) {
    console.error('Could not load course history:', error)
    historyError.value = t('Could not load course history. Please try refreshing.')
  } finally {
    historyLoading.value = false
  }
}

const fallbackCourseImages = {
  'microbit-robotics-courses': '/auth-workshop.jpg',
  'super-class-fpv-drone-training': 'https://images.unsplash.com/photo-1473968512647-3e447244af8f?auto=format&fit=crop&w=900&q=85',
  'internet-of-things': 'https://images.unsplash.com/photo-1558494949-ef010cbdcc31?auto=format&fit=crop&w=900&q=85',
  'robotics': 'https://images.unsplash.com/photo-1535378620166-273708d44e4c?auto=format&fit=crop&w=900&q=85',
  'blender-3d-animation': 'https://images.unsplash.com/photo-1633356122544-f134324a6cee?auto=format&fit=crop&w=900&q=85',
  'battle-robot-courses': 'https://images.unsplash.com/photo-1581092160562-40aa08e78837?auto=format&fit=crop&w=900&q=85',
  'pcb-electronic-board-designs': 'https://images.unsplash.com/photo-1518770660439-4636190af475?auto=format&fit=crop&w=900&q=85',
  'advance-arm-robotics': 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?auto=format&fit=crop&w=900&q=85',
  'iot-data-scientists-advanced-analytics': 'https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&w=900&q=85',
  'technology-course-levels-1-to-8': 'https://images.unsplash.com/photo-1516321318423-f06f85e504b3?auto=format&fit=crop&w=900&q=85',
  'special-3d-designs-course': 'https://images.unsplash.com/photo-1581092334651-ddf26d9a09d0?auto=format&fit=crop&w=900&q=85',
  'micropython-and-python': 'https://images.unsplash.com/photo-1515879218367-8466d910aaa4?auto=format&fit=crop&w=900&q=85',
}

function getCourseImage(enrollment) {
  const raw = enrollment?.course_image
  if (raw && typeof raw === 'string' && !raw.startsWith('/course-') && raw.trim() !== '') {
    return resolveImageUrl(raw)
  }
  const slug = enrollment?.course_slug || ''
  if (slug && fallbackCourseImages[slug]) {
    return resolveImageUrl(fallbackCourseImages[slug])
  }
  return '/auth-workshop.jpg'
}

function handleCourseImageError(event, enrollment) {
  const target = event.target
  if (target && !target.dataset.fallbackApplied) {
    target.dataset.fallbackApplied = 'true'
    const slug = enrollment?.course_slug || ''
    if (slug && fallbackCourseImages[slug] && target.src !== fallbackCourseImages[slug]) {
      target.src = fallbackCourseImages[slug]
    } else {
      target.src = '/auth-workshop.jpg'
    }
  }
}

function clearLocalProfile() {
  try {
    localStorage.removeItem('aerobyte-profile-current')
    if (storageKey.value) localStorage.removeItem(storageKey.value)
    if (storageEmailKey.value) localStorage.removeItem(storageEmailKey.value)
    localStorage.removeItem('aerobyte-profile')
  } catch (error) {
    console.error('Could not clear saved profile:', error)
    notice.value = t('Could not clear profile information from this browser.')
    noticeType.value = 'error'
    return
  }
  copyProfile(profile, { ...emptyProfile(), fullName: account.value?.name || '', email: account.value?.email || '' })
  copyProfile(draft, profile)
  window.dispatchEvent(new Event('aerobyte-profile-updated'))
  notice.value = t('Profile information cleared from this browser.')
  noticeType.value = 'success'
}

async function confirmLogout() {
  logoutDialogOpen.value = false
  try {
    await accountService.logout()
  } catch (error) {
    console.warn('Backend sign out error (continuing local logout):', error)
  }

  try {
    localStorage.removeItem('aerobyte_user_session')
    localStorage.removeItem('aerobyte-profile-current')
    if (storageKey.value) localStorage.removeItem(storageKey.value)
    if (storageEmailKey.value) localStorage.removeItem(storageEmailKey.value)
    localStorage.removeItem('aerobyte-profile')
    for (let i = localStorage.length - 1; i >= 0; i--) {
      const k = localStorage.key(i)
      if (k && (k.startsWith('aerobyte-profile:') || k.startsWith('aerobyte_user_'))) {
        localStorage.removeItem(k)
      }
    }
  } catch (_) {}

  copyProfile(profile, emptyProfile())
  copyProfile(draft, emptyProfile())
  courseHistory.value = []
  window.dispatchEvent(new Event('aerobyte-profile-updated'))
  window.dispatchEvent(new Event('aerobyte-auth-updated'))
  account.value = null

  try {
    await router.replace('/courses')
  } catch (_) {}

  if (window.location.pathname.includes('/profile')) {
    window.location.href = '/courses'
  }
}

function startEditing() {
  notice.value = ''
  avatarLoadFailed.value = false
  qualificationDropdownOpen.value = false
  experienceDropdownOpen.value = false
  copyProfile(draft, profile)
  if (!draft.avatarUrl && profile.avatarUrl) {
    draft.avatarUrl = profile.avatarUrl
  }
  isEditing.value = true
}

function cancelEditing() {
  qualificationDropdownOpen.value = false
  experienceDropdownOpen.value = false
  copyProfile(draft, profile)
  isEditing.value = false
}

function triggerAvatarUpload() {
  avatarFileInput.value?.click()
}

function onAvatarError() {
  avatarLoadFailed.value = true
  // Safe UI fallback: Never delete or clear avatar from user record on temporary load failure!
}

async function handleAvatarChange(event) {
  const file = event.target.files?.[0]
  if (!file) return
  if (!file.type.startsWith('image/')) {
    notice.value = t('Please select a valid image file (JPG, PNG, WEBP).')
    noticeType.value = 'error'
    return
  }
  if (file.size > 5 * 1024 * 1024) {
    notice.value = t('Image file size must be less than 5MB.')
    noticeType.value = 'error'
    return
  }

  avatarUploading.value = true
  avatarLoadFailed.value = false
  notice.value = ''

  const previewUrl = URL.createObjectURL(file)
  profile.avatarUrl = previewUrl
  draft.avatarUrl = previewUrl

  try {
    const userEmail = account.value?.email || profile.email || ''
    const { data } = await accountService.uploadAvatar(file, userEmail)
    if (data.avatar_url) {
      profile.avatarUrl = data.avatar_url
      draft.avatarUrl = data.avatar_url
      if (account.value) {
        account.value.avatar_url = data.avatar_url
      }
      avatarLoadFailed.value = false
      const updateAvatarCache = (key) => {
        if (!key) return
        try {
          const s = JSON.parse(localStorage.getItem(key) || '{}')
          s.avatarUrl = data.avatar_url
          localStorage.setItem(key, JSON.stringify(s))
        } catch (_) {}
      }
      updateAvatarCache('aerobyte-profile-current')
      updateAvatarCache(storageEmailKey.value)
      updateAvatarCache(storageKey.value)
      updateAvatarCache('aerobyte-profile')
      window.dispatchEvent(new Event('aerobyte-profile-updated'))
      window.dispatchEvent(new Event('aerobyte-auth-updated'))
      notice.value = t('Profile photo updated successfully!')
      noticeType.value = 'success'
    }
  } catch (error) {
    console.error('Failed to upload avatar to server:', error)
    profile.avatarUrl = ''
    draft.avatarUrl = ''
    avatarLoadFailed.value = false
    const detail = error.response?.data?.detail
    const detailMsg = Array.isArray(detail)
      ? (detail[0]?.msg || '')
      : (typeof detail === 'string' ? detail : (error.message || ''))
    notice.value = detailMsg || t('Failed to upload avatar image. Please try again.')
    noticeType.value = 'error'
  } finally {
    avatarUploading.value = false
    if (event.target) event.target.value = ''
  }
}

async function removeAvatar() {
  avatarLoadFailed.value = false
  profile.avatarUrl = ''
  draft.avatarUrl = ''
  if (account.value) {
    account.value.avatar_url = ''
  }
  try {
    await accountService.updateProfile({
      full_name: profile.fullName,
      email: profile.email,
      phone: profile.phone,
      telegram: profile.telegram,
      date_of_birth: profile.dateOfBirth,
      gender: profile.gender,
      location: profile.location,
      qualification: profile.qualification,
      qualification_other: profile.qualificationOther,
      occupation: profile.occupation,
      experience: profile.experience,
      avatar_url: '',
    })
  } catch (e) {
    console.warn('Could not clear avatar on server:', e)
  }
  const clearAvatarCache = (key) => {
    if (!key) return
    try {
      const s = JSON.parse(localStorage.getItem(key) || '{}')
      s.avatarUrl = ''
      localStorage.setItem(key, JSON.stringify(s))
    } catch (_) {}
  }
  clearAvatarCache('aerobyte-profile-current')
  clearAvatarCache(storageEmailKey.value)
  clearAvatarCache(storageKey.value)
  clearAvatarCache('aerobyte-profile')
  window.dispatchEvent(new Event('aerobyte-profile-updated'))
  window.dispatchEvent(new Event('aerobyte-auth-updated'))
  notice.value = t('Profile photo removed.')
  noticeType.value = 'success'
}

async function saveProfile() {
  const nextProfile = { ...draft }
  if (nextProfile.occupation) {
    nextProfile.occupation = nextProfile.occupation.replace(/[0-9\u17E0-\u17E9]/g, '').trim()
  }

  // Preserve existing avatar if not explicitly changed
  if (!nextProfile.avatarUrl && profile.avatarUrl) {
    nextProfile.avatarUrl = profile.avatarUrl
  }
  if (!nextProfile.avatarUrl && account.value?.avatar_url) {
    nextProfile.avatarUrl = account.value.avatar_url
  }

  let avatarToSend = nextProfile.avatarUrl
  if (avatarToSend && (avatarToSend.startsWith('data:') || avatarToSend.startsWith('blob:'))) {
    avatarToSend = (profile.avatarUrl && !profile.avatarUrl.startsWith('data:') && !profile.avatarUrl.startsWith('blob:'))
      ? profile.avatarUrl
      : (account.value?.avatar_url || '')
  }

  try {
    const { data } = await accountService.updateProfile({
      full_name: nextProfile.fullName,
      email: nextProfile.email,
      avatar_url: avatarToSend,
      phone: nextProfile.phone,
      telegram: nextProfile.telegram,
      date_of_birth: nextProfile.dateOfBirth,
      gender: nextProfile.gender,
      location: nextProfile.location,
      qualification: nextProfile.qualification,
      qualification_other: nextProfile.qualificationOther,
      occupation: nextProfile.occupation,
      experience: nextProfile.experience,
    })
    account.value = data.user
    nextProfile.fullName = data.user.name
    nextProfile.email = data.user.email
    if (data.user.avatar_url !== undefined) {
      nextProfile.avatarUrl = data.user.avatar_url
    }
    if (data.user.phone !== undefined) nextProfile.phone = data.user.phone
    if (data.user.telegram !== undefined) nextProfile.telegram = data.user.telegram
    if (data.user.date_of_birth !== undefined) nextProfile.dateOfBirth = data.user.date_of_birth
    if (data.user.gender !== undefined) nextProfile.gender = data.user.gender
    if (data.user.location !== undefined) nextProfile.location = data.user.location
    if (data.user.qualification !== undefined) nextProfile.qualification = data.user.qualification
    if (data.user.qualification_other !== undefined) nextProfile.qualificationOther = data.user.qualification_other
    if (data.user.occupation !== undefined) nextProfile.occupation = data.user.occupation
    if (data.user.experience !== undefined) nextProfile.experience = data.user.experience
  } catch (error) {
    console.error('Could not update the account profile:', error)
    notice.value = error.response?.data?.detail || t('Your account details could not be updated. Please try again.')
    noticeType.value = 'error'
    return
  }

  try {
    localStorage.setItem('aerobyte-profile-current', JSON.stringify(nextProfile))
    if (storageEmailKey.value) localStorage.setItem(storageEmailKey.value, JSON.stringify(nextProfile))
    if (storageKey.value) localStorage.setItem(storageKey.value, JSON.stringify(nextProfile))
    localStorage.setItem('aerobyte-profile', JSON.stringify(nextProfile))
  } catch (error) {
    console.warn('Could not cache additional profile details to local storage:', error)
  }

  copyProfile(profile, nextProfile)
  avatarLoadFailed.value = false
  window.dispatchEvent(new Event('aerobyte-profile-updated'))
  window.dispatchEvent(new Event('aerobyte-auth-updated'))
  isEditing.value = false
  notice.value = t('Profile details saved.')
  noticeType.value = 'success'
}
</script>

<style>
.profile-input {
  display: block;
  width: 100%;
  border: 1px solid #cbd5e1;
  border-radius: 0.5rem;
  background: #fff;
  padding: 0.625rem 0.75rem;
  color: #334155;
  font-size: 0.875rem;
  outline: none;
  transition: border-color 150ms ease, box-shadow 150ms ease, background-color 150ms ease, color 150ms ease;
}

.profile-input::placeholder {
  color: #94a3b8;
}

.profile-input:focus {
  border-color: #27466d;
  box-shadow: 0 0 0 3px rgb(39 70 109 / 0.12);
}

html.dark .profile-input {
  background-color: #1e293b !important;
  border-color: #334155 !important;
  color: #f8fafc !important;
}

html.dark .profile-input::placeholder {
  color: #64748b !important;
}

html.dark .profile-input:focus {
  border-color: #6366f1 !important;
  box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.2) !important;
}
</style>
