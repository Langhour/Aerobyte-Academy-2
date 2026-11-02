<template>
  <div class="min-h-screen bg-slate-100 dark:bg-slate-950 py-4 sm:py-8 px-2 sm:px-6 lg:px-8 transition-colors receipt-page-wrapper">
    <!-- Top Action Bar (Hidden on Print) -->
    <div class="max-w-4xl mx-auto mb-4 sm:mb-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-3 sm:gap-4 print:hidden">
      <div class="flex flex-wrap items-center gap-1.5 sm:gap-2 text-xs font-semibold text-slate-500 dark:text-slate-400">
        <RouterLink to="/courses" class="hover:text-navy-900 dark:hover:text-white transition flex items-center gap-1">
          <ArrowLeft class="w-3.5 h-3.5" />
          <span>{{ t('Back to Courses') }}</span>
        </RouterLink>
        <span>/</span>
        <RouterLink to="/profile" class="hover:text-navy-900 dark:hover:text-white transition">
          {{ t('Course history') }}
        </RouterLink>
        <span>/</span>
        <span class="text-navy-900 dark:text-white font-bold">{{ t('Academy Receipt & Admission Letter') }}</span>
      </div>

      <!-- Action Buttons -->
      <div class="flex items-center gap-2 sm:gap-2.5 w-full sm:w-auto">
        <button
          type="button"
          @click="copyReceiptLink"
          class="flex-1 sm:flex-none inline-flex items-center justify-center gap-2 px-3.5 py-2 text-xs font-bold rounded-xl border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-700 dark:text-slate-200 hover:bg-slate-50 dark:hover:bg-slate-700 shadow-2xs transition cursor-pointer"
          :title="t('Copy receipt link')"
        >
          <Copy v-if="!copied" class="w-3.5 h-3.5" />
          <Check v-else class="w-3.5 h-3.5 text-emerald-600 dark:text-emerald-400" />
          <span>{{ copied ? t('Link Copied!') : t('Share Link') }}</span>
        </button>

        <button
          type="button"
          @click="printReceipt"
          class="flex-1 sm:flex-none inline-flex items-center justify-center gap-2 px-4 py-2 text-xs font-bold rounded-xl bg-navy-900 dark:bg-indigo-600 text-white hover:bg-navy-800 dark:hover:bg-indigo-500 shadow-sm transition cursor-pointer"
        >
          <Printer class="w-3.5 h-3.5" />
          <span>{{ t('Print / Save PDF (2 Pages)') }}</span>
        </button>
      </div>
    </div>

    <!-- Error State -->
    <div v-if="loadError" class="max-w-xl mx-auto rounded-2xl border border-red-200 dark:border-red-900/50 bg-white dark:bg-slate-900 p-8 text-center shadow-card">
      <div class="w-12 h-12 rounded-full bg-red-50 dark:bg-red-950/50 text-red-600 dark:text-red-400 mx-auto flex items-center justify-center mb-3">
        <FileText class="w-6 h-6" />
      </div>
      <h2 class="text-lg font-extrabold text-navy-900 dark:text-white">{{ t('Receipt Not Found') }}</h2>
      <p class="mt-2 text-xs text-slate-500 dark:text-slate-400 leading-relaxed">{{ t(loadError) }}</p>
      <RouterLink
        to="/courses"
        class="mt-6 inline-flex items-center gap-2 rounded-xl bg-navy-900 dark:bg-indigo-600 px-5 py-2.5 text-xs font-bold text-white transition hover:bg-navy-800"
      >
        {{ t('Browse courses') }}
      </RouterLink>
    </div>

    <!-- Loading Skeleton -->
    <div v-else-if="loading" class="max-w-4xl mx-auto rounded-2xl border border-slate-200 dark:border-slate-800 bg-white dark:bg-slate-900 p-8 sm:p-12 shadow-card animate-pulse space-y-6">
      <div class="h-12 bg-slate-100 dark:bg-slate-800 rounded-xl w-1/3"></div>
      <div class="h-32 bg-slate-100 dark:bg-slate-800 rounded-2xl"></div>
      <div class="h-48 bg-slate-100 dark:bg-slate-800 rounded-2xl"></div>
    </div>

    <!-- 2-PAGE DOCUMENT WRAPPER -->
    <div v-else id="printable-receipt" class="max-w-4xl mx-auto space-y-6 sm:space-y-8 print:space-y-0">
      
      <!-- ========================================================= -->
      <!-- PAGE 1: OFFICIAL ACADEMY RECEIPT                          -->
      <!-- ========================================================= -->
      <div class="receipt-sheet receipt-page-1 rounded-2xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xl overflow-hidden print:border-none print:shadow-none print:rounded-none transition-colors">
        <div class="p-4 sm:p-8 lg:p-10 relative overflow-hidden space-y-4 print:p-3 print:space-y-3">
          <!-- Subtle Faint Academy Logo Watermark -->
          <div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-[0.035] dark:opacity-[0.05] print:opacity-[0.03] select-none">
            <img src="/aerobyte-logo.png" alt="" class="w-[420px] print:w-[320px] object-contain dark:brightness-0 dark:invert" />
          </div>

          <!-- Page 1 Header (Logo & Info on Left, ACADEMY RECEIPT on Right) -->
          <div class="flex flex-col sm:flex-row items-start sm:items-start justify-between gap-4 border-b border-sky-100 dark:border-slate-800 pb-3.5 print:pb-2">
            <!-- Left: Brand Logo & Academy Info -->
            <div class="space-y-1">
              <div class="flex items-center gap-2.5">
                <img
                  src="/aerobyte-logo.png"
                  alt="AeroByte Logo"
                  class="h-8 w-10 sm:h-9 sm:w-11 print:h-7 print:w-9 object-contain dark:brightness-0 dark:invert print:brightness-0 print:invert-0 shrink-0"
                />
                <span class="text-base sm:text-lg print:text-base font-extrabold tracking-tight text-navy-900 dark:text-white whitespace-nowrap">
                  AeroByte Academy
                </span>
              </div>
              <p class="text-[11px] print:text-[9px] text-slate-600 dark:text-slate-400 font-normal">
                Phone Number : 015 341 002
              </p>
              <p class="text-[11px] print:text-[9px] text-slate-600 dark:text-slate-400 font-normal">
                Email : aerobyte.academy@gmail.com
              </p>
              <p class="text-[11px] print:text-[9px] text-slate-600 dark:text-slate-400 font-normal">
                Location : Ta Kmau Krong, Kandal Province
              </p>
            </div>

            <!-- Right: ACADEMY RECEIPT Title & Metadata -->
            <div class="sm:text-right shrink-0 space-y-1 text-xs print:text-[9.5px]">
              <h2 class="text-xl sm:text-2xl print:text-xl font-black text-[#0f2444] dark:text-white tracking-tight uppercase">
                {{ t('ACADEMY RECEIPT') }}
              </h2>
              <p class="text-slate-600 dark:text-slate-400 pt-0.5">
                <span>{{ t('Receipt No') }}:</span>
                <span class="font-bold text-slate-900 dark:text-white ml-1.5">{{ receiptNo }}</span>
              </p>
              <p class="text-slate-600 dark:text-slate-400">
                <span>{{ t('Date') }}:</span>
                <span class="font-semibold text-slate-900 dark:text-white ml-1.5">{{ receiptDate }}</span>
              </p>
            </div>
          </div>

          <!-- Student & Course Information Block -->
          <div class="grid grid-cols-1 sm:grid-cols-12 gap-2 sm:gap-4 text-xs print:text-[9.5px] text-slate-700 dark:text-slate-300">
            <!-- Left Info -->
            <div class="sm:col-span-6 space-y-1">
              <p>
                <span class="text-slate-500 dark:text-slate-400">{{ t('Student Name') }}:</span>
                <strong class="text-slate-900 dark:text-white ml-1.5">{{ studentDisplayName }}</strong>
              </p>
              <p>
                <span class="text-slate-500 dark:text-slate-400">{{ t('Student ID') }}:</span>
                <span class="font-bold text-slate-800 dark:text-slate-200 ml-1.5">{{ studentId }}</span>
              </p>
              <p>
                <span class="text-slate-500 dark:text-slate-400">{{ t('Start Course') }}:</span>
                <span class="font-semibold text-slate-800 dark:text-slate-200 ml-1.5">{{ t('Upcoming Batch') }}</span>
              </p>
            </div>

            <!-- Right Info -->
            <div class="sm:col-span-6 sm:text-right space-y-1">
              <p>
                <span class="text-slate-500 dark:text-slate-400">{{ t('Course') }}:</span>
                <strong class="text-slate-900 dark:text-white ml-1.5">"{{ courseTitleDisplay }}"</strong>
              </p>
              <p>
                <span class="text-slate-500 dark:text-slate-400">{{ t('Time') }}:</span>
                <span class="font-semibold text-slate-900 dark:text-white ml-1.5">{{ timeSlot }}</span>
              </p>
            </div>
          </div>

          <!-- Line-Item Breakdown Table -->
          <div class="rounded-xl border border-sky-200/90 dark:border-slate-700 overflow-hidden text-xs print:text-[9.5px]">
            <table class="w-full border-collapse">
              <thead>
                <tr class="bg-[#1e3a61] dark:bg-slate-800 text-white font-bold text-[11px] print:text-[9.5px]">
                  <th class="py-2 px-3 w-12 text-center border-r border-[#2d5282] dark:border-slate-700">{{ t('No.') }}</th>
                  <th class="py-2 px-3 border-r border-[#2d5282] dark:border-slate-700 text-left">{{ t('Description') }}</th>
                  <th class="py-2 px-3 border-r border-[#2d5282] dark:border-slate-700 text-left">{{ t('Course') }}</th>
                  <th class="py-2 px-3 w-16 text-center border-r border-[#2d5282] dark:border-slate-700">{{ t('QTY') }}</th>
                  <th class="py-2 px-3 text-right w-28">{{ t('Amount') }}</th>
                </tr>
              </thead>
              <tbody class="divide-y divide-sky-100 dark:divide-slate-800 text-slate-700 dark:text-slate-200 font-medium">
                <tr>
                  <td class="py-2 px-3 text-center text-slate-400 border-r border-sky-100 dark:border-slate-800">1</td>
                  <td class="py-2 px-3 font-semibold text-slate-900 dark:text-white border-r border-sky-100 dark:border-slate-800">{{ courseDescription }}</td>
                  <td class="py-2 px-3 font-bold text-navy-900 dark:text-white border-r border-sky-100 dark:border-slate-800 align-middle" rowspan="4">
                    <div>"{{ courseTitleDisplay }}"</div>
                  </td>
                  <td class="py-2 px-3 text-center border-r border-sky-100 dark:border-slate-800">1</td>
                  <td class="py-2 px-3 text-right font-bold text-slate-900 dark:text-white">$ {{ basePrice.toFixed(2) }}</td>
                </tr>
                <tr>
                  <td class="py-1.5 px-3 text-center text-slate-400 border-r border-sky-100 dark:border-slate-800">2</td>
                  <td class="py-1.5 px-3 border-r border-sky-100 dark:border-slate-800">{{ t('Administration fee') }}</td>
                  <td class="py-1.5 px-3 text-center border-r border-sky-100 dark:border-slate-800">1</td>
                  <td class="py-1.5 px-3 text-right font-semibold">$ {{ adminFee.toFixed(2) }}</td>
                </tr>
                <tr>
                  <td class="py-1.5 px-3 text-center text-slate-400 border-r border-sky-100 dark:border-slate-800">3</td>
                  <td class="py-1.5 px-3 border-r border-sky-100 dark:border-slate-800">{{ t('Card fee') }}</td>
                  <td class="py-1.5 px-3 text-center border-r border-sky-100 dark:border-slate-800">1</td>
                  <td class="py-1.5 px-3 text-right font-semibold">$ {{ cardFee.toFixed(2) }}</td>
                </tr>
                <tr>
                  <td class="py-1.5 px-3 text-center text-slate-400 border-r border-sky-100 dark:border-slate-800">4</td>
                  <td class="py-1.5 px-3 border-r border-sky-100 dark:border-slate-800">{{ t('Certification fee') }}</td>
                  <td class="py-1.5 px-3 text-center border-r border-sky-100 dark:border-slate-800">1</td>
                  <td class="py-1.5 px-3 text-right font-semibold">$ {{ certFee.toFixed(2) }}</td>
                </tr>
                <!-- Aesthetic bottom spacer row matching image -->
                <tr>
                  <td class="py-1.5 px-3 border-r border-sky-100 dark:border-slate-800">&nbsp;</td>
                  <td class="py-1.5 px-3 border-r border-sky-100 dark:border-slate-800"></td>
                  <td class="py-1.5 px-3 border-r border-sky-100 dark:border-slate-800"></td>
                  <td class="py-1.5 px-3 border-r border-sky-100 dark:border-slate-800"></td>
                  <td class="py-1.5 px-3 text-right"></td>
                </tr>
              </tbody>
            </table>
          </div>

          <!-- Status Banners (Payment Method & Remark) -->
          <div class="space-y-2">
            <div class="rounded-xl bg-[#d9e6f7] dark:bg-indigo-950/80 border border-transparent dark:border-indigo-800/60 px-4 py-2 font-bold text-xs print:text-[10px] text-[#0f2444] dark:text-indigo-200">
              {{ t('Payment Method: ABA Pay / Bakong KHQR') }}
            </div>
            <div class="rounded-xl bg-[#eef4fc] dark:bg-slate-800/80 border border-sky-100 dark:border-slate-700 px-4 py-2 font-semibold text-xs print:text-[10px] text-[#1c3d6c] dark:text-sky-300">
              Remark: Course Enrollment Confirmed &amp; Verified ({{ receiptDate }})
            </div>
          </div>

          <!-- Bank References & Totals (Side by Side) -->
          <div class="grid grid-cols-1 sm:grid-cols-12 gap-4 items-start pt-1 text-xs print:text-[9.5px]">
            <!-- Left: Bank References -->
            <div class="sm:col-span-7 space-y-1">
              <p class="font-extrabold text-slate-900 dark:text-white">{{ t('Bank References:') }}</p>
              <p class="text-slate-700 dark:text-slate-300">
                {{ t('ABA Account No:') }} <strong class="text-navy-900 dark:text-indigo-300 text-sm print:text-xs tracking-wider ml-1">018 134 951</strong>
              </p>
              <p class="text-slate-500 dark:text-slate-400 text-[11px] print:text-[9px]">{{ t('Account Name:') }}</p>
              <p class="font-extrabold text-slate-900 dark:text-white tracking-wide">
                SOU SEANGLY AND KHEMARAK VIDHCHETRA
              </p>
            </div>

            <!-- Right: Totals Box -->
            <div class="sm:col-span-5 rounded-xl border border-sky-200 dark:border-slate-700 overflow-hidden text-xs print:text-[9.5px] bg-white dark:bg-slate-900">
              <div class="divide-y divide-sky-100 dark:divide-slate-800">
                <div class="flex justify-between px-3.5 py-1.5 bg-slate-50/60 dark:bg-slate-800/50">
                  <span class="text-slate-500 dark:text-slate-400">{{ t('Total') }}</span>
                  <span class="font-bold text-slate-800 dark:text-white">${{ subtotal.toFixed(2) }}</span>
                </div>
                <div v-if="discountAmount > 0" class="flex justify-between px-3.5 py-1.5 text-emerald-600 dark:text-emerald-400 font-bold">
                  <span>{{ t('Scholarship / Discount') }}</span>
                  <span>-${{ discountAmount.toFixed(2) }}</span>
                </div>
                <div class="flex justify-between px-3.5 py-1.5 font-bold bg-slate-50/60 dark:bg-slate-800/50">
                  <span class="text-slate-700 dark:text-slate-300">{{ t('Grand Total USD') }}</span>
                  <span class="text-slate-900 dark:text-white font-black">${{ totalAmountDue.toFixed(2) }}</span>
                </div>
                <div class="flex justify-between px-3.5 py-1.5">
                  <span class="text-slate-500 dark:text-slate-400">{{ t('Exchange rate') }}</span>
                  <span class="text-slate-700 dark:text-slate-300 font-medium">KHR 4,050.00</span>
                </div>
                <div class="flex justify-between px-3.5 py-2 bg-[#d9e6f7] dark:bg-indigo-950 font-black text-navy-900 dark:text-indigo-200">
                  <span>{{ t('Grand total in KHR') }}</span>
                  <span>KHR {{ grandTotalKHR }}</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Prominent THANK YOU Banner -->
          <div class="text-center font-black text-xl sm:text-2xl print:text-lg tracking-wider text-[#0f2444] dark:text-white py-2 print:py-1">
            {{ t('THANK YOU!') }}
          </div>

          <!-- Dual Signatures Section (Prepare By & Student/Parent Student) -->
          <div class="grid grid-cols-1 sm:grid-cols-2 gap-6 pt-3 border-t border-slate-200 dark:border-slate-800 text-xs print:text-[9px]">
            <!-- Left: Prepare By (Ms. Khemarak Vidhchetra) -->
            <div class="space-y-1">
              <p class="font-bold text-slate-900 dark:text-white">{{ t('Prepare By:') }}</p>
              <div class="h-10 print:h-8 flex items-center select-none">
                <img
                  src="/vidhchetra-signature.png"
                  alt="Signature Vidhchetra.K"
                  class="h-8 sm:h-9 print:h-7 object-contain dark:brightness-0 dark:invert print:brightness-0 print:invert-0"
                />
              </div>
              <p class="font-extrabold text-navy-950 dark:text-white">
                Signature &amp; Name: KHEMARAK VIDHCHETRA
              </p>
              <p class="text-slate-500 dark:text-slate-400">
                Date: {{ receiptDate }}
              </p>
            </div>

            <!-- Right: Student / Parent Student -->
            <div class="sm:text-right space-y-1">
              <p class="font-bold text-slate-900 dark:text-white">{{ t('Student/ Parent Student:') }}</p>
              <div class="h-10 print:h-8 flex items-end sm:justify-end">
                <span class="text-[11px] print:text-[8.5px] italic text-slate-400 dark:text-slate-500 border-b border-dashed border-slate-300 dark:border-slate-700 pb-0.5">
                  {{ t('Confirmed electronically') }}
                </span>
              </div>
              <p class="font-extrabold text-navy-950 dark:text-white">
                Signature &amp; Name: {{ studentDisplayName }}
              </p>
              <p class="text-slate-500 dark:text-slate-400">
                Date: {{ receiptDate }}
              </p>
            </div>
          </div>

          <!-- Page 1 Footer -->
          <div class="pt-2 border-t border-slate-100 dark:border-slate-800 text-[9px] print:text-[8px] text-center text-slate-400 dark:text-slate-500">
            Ta Kmau STEAM Hub, Kandal Province &bull; Hotline: 015 341 002 &bull; aerobyte.academy@gmail.com &bull; Page 1 of 2
          </div>
        </div>
      </div>

      <!-- Screen Separator Between Page 1 and Page 2 -->
      <div class="flex items-center justify-center gap-3 print:hidden py-1">
        <div class="h-px bg-slate-300 dark:bg-slate-800 flex-1"></div>
        <span class="px-3.5 py-1 rounded-full text-xs font-bold text-slate-500 dark:text-slate-400 bg-slate-200/80 dark:bg-slate-800 shadow-2xs">
          Page 2 of 2 &bull; Admission Confirmation Letter
        </span>
        <div class="h-px bg-slate-300 dark:bg-slate-800 flex-1"></div>
      </div>

      <!-- ========================================================= -->
      <!-- PAGE 2: OFFICIAL ADMISSION CONFIRMATION LETTER (FROM PDF) -->
      <!-- ========================================================= -->
      <div class="receipt-sheet receipt-page-2 rounded-2xl border border-slate-200/90 dark:border-slate-800 bg-white dark:bg-slate-900 shadow-xl overflow-hidden print:border-none print:shadow-none print:rounded-none transition-colors">
        <div class="p-4 sm:p-8 lg:p-10 relative overflow-hidden space-y-3 sm:space-y-3.5 print:p-3 print:space-y-2.5">
          <!-- Subtle Faint Academy Logo Watermark -->
          <div class="absolute inset-0 flex items-center justify-center pointer-events-none opacity-[0.035] dark:opacity-[0.05] print:opacity-[0.03] select-none">
            <img src="/aerobyte-logo.png" alt="" class="w-[420px] print:w-[320px] object-contain dark:brightness-0 dark:invert" />
          </div>

          <!-- Top Official Header Line -->
          <div class="flex flex-col sm:flex-row items-center justify-between text-center sm:text-left gap-1 text-[8.5px] sm:text-[9px] print:text-[8px] font-semibold text-slate-400 dark:text-slate-400 uppercase tracking-wider sm:tracking-widest border-b border-slate-100 dark:border-slate-800 pb-1">
            <span>AEROBYTE ACADEMY | OFFICIAL ADMISSIONS &amp; REGISTRATION SYSTEM</span>
            <span>Ta Kmau STEAM Hub &bull; 015 341 002 &bull; Page 2 of 2</span>
          </div>

          <!-- Brand Header -->
          <div class="flex items-center gap-3 border-b border-sky-100 dark:border-slate-800 pb-3 print:pb-1.5">
            <img
              src="/aerobyte-logo.png"
              alt="AeroByte Logo"
              class="h-10 w-12 sm:h-11 sm:w-13 print:h-8 print:w-10 object-contain dark:brightness-0 dark:invert print:brightness-0 print:invert-0"
            />
            <div>
              <h1 class="text-base sm:text-lg print:text-base font-black tracking-tight text-[#0f2444] dark:text-white leading-tight">
                AEROBYTE ACADEMY
              </h1>
              <p class="text-[9.5px] sm:text-[10px] print:text-[8.5px] font-bold text-[#e8590c] dark:text-orange-400 tracking-wide">
                The Academy of High-Tech Innovation &amp; Future Engineering
              </p>
              <p class="text-[9px] sm:text-[9.5px] print:text-[8px] text-slate-500 dark:text-slate-400">
                Ta Kmau Krong, Kandal Province | Hotline: 015 341 002 | Email: aerobyte.academy@gmail.com
              </p>
            </div>
          </div>

          <!-- Official Blue Acceptance & Confirmation Banner -->
          <div class="rounded-xl border border-sky-200/90 dark:border-indigo-900/60 bg-gradient-to-r from-sky-50/90 via-[#edf4fd] to-sky-50/90 dark:from-slate-800/90 dark:via-slate-800 dark:to-slate-800/90 p-2.5 sm:p-3 text-center space-y-1 shadow-2xs">
            <div class="inline-flex items-center px-3 py-0.5 rounded-full bg-[#102a49] dark:bg-indigo-600 text-white text-[10px] sm:text-[11px] print:text-[9px] font-black tracking-wider uppercase shadow-2xs">
              <span>APPLICATION ACCEPTED &amp; REGISTRATION CONFIRMED</span>
            </div>
            <p class="text-[10px] sm:text-[10.5px] print:text-[8.5px] text-[#1e3a61] dark:text-slate-300 font-medium leading-tight">
              You have successfully submitted your Student Registration Form. As stated on the application portal:
            </p>
            <p class="text-[10px] sm:text-[10.5px] print:text-[8.5px] font-bold italic text-[#102a49] dark:text-sky-200">
              &ldquo;You can consider your application accepted after you receive a confirmation email.&rdquo;
            </p>
          </div>

          <!-- Greeting & Formal Letter (From PDF) -->
          <div class="text-[11px] print:text-[9px] leading-relaxed text-slate-700 dark:text-slate-300 space-y-1">
            <p class="font-bold text-navy-950 dark:text-white">
              Dear {{ studentDisplayName }} / Respected Parent &amp; Guardian,
            </p>
            <p class="text-slate-600 dark:text-slate-300">
              Welcome to AeroByte Academy! We are pleased to confirm that your student registration submitted through our online admission form has been reviewed and officially approved. Your student seat is now reserved for the upcoming intake at our Ta Kmau Krong STEAM Hub.
            </p>
          </div>

          <!-- Summary of Submitted Registration Record (From PDF) -->
          <div class="rounded-xl border border-slate-200 dark:border-slate-700 overflow-hidden text-[10px] print:text-[8.5px]">
            <div class="bg-[#102a4e] dark:bg-slate-800 text-white font-bold px-3 py-1.5 text-[10px] sm:text-[10.5px] print:text-[9px] flex flex-wrap items-center justify-between gap-1">
              <span>Summary of Your Submitted Registration Record</span>
              <span class="text-[9px] print:text-[8px] font-normal text-slate-300">Seat Confirmed &bull; Verified Intake</span>
            </div>
            <div class="overflow-x-auto">
              <table class="w-full min-w-[480px] sm:min-w-full border-collapse">
                <tbody class="divide-y divide-slate-100 dark:divide-slate-800">
                  <tr>
                    <td class="w-1/4 py-1.5 px-3 font-semibold text-slate-600 dark:text-slate-300 bg-slate-50/80 dark:bg-slate-800/80">Student Full Name</td>
                    <td class="py-1.5 px-3 font-bold text-navy-900 dark:text-white" colspan="3">{{ studentDisplayName }}</td>
                  </tr>
                  <tr>
                    <td class="py-1.5 px-3 font-semibold text-slate-600 dark:text-slate-300 bg-slate-50/80 dark:bg-slate-800/80">Contact</td>
                    <td class="py-1.5 px-3 text-slate-700 dark:text-slate-200" colspan="3">
                      Email: <span class="font-medium text-slate-900 dark:text-white">{{ studentEmail }}</span> &bull; Phone/Telegram: <span class="font-medium text-slate-900 dark:text-white">{{ studentContact }}</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="py-1.5 px-3 font-semibold text-slate-600 dark:text-slate-300 bg-slate-50/80 dark:bg-slate-800/80">Address</td>
                    <td class="py-1.5 px-3 text-slate-700 dark:text-slate-200" colspan="3">{{ studentAddress }}</td>
                  </tr>
                  <tr>
                    <td class="py-1.5 px-3 font-semibold text-slate-600 dark:text-slate-300 bg-slate-50/80 dark:bg-slate-800/80">Confirmed Enrolled Course</td>
                    <td class="py-1.5 px-3 font-bold text-navy-900 dark:text-white" colspan="3">{{ courseTitleDisplay }}</td>
                  </tr>
                  <tr>
                    <td class="py-1.5 px-3 font-semibold text-slate-600 dark:text-slate-300 bg-slate-50/80 dark:bg-slate-800/80">Schedule &amp; Shift</td>
                    <td class="py-1.5 px-3 text-slate-700 dark:text-slate-200" colspan="3">
                      {{ studentScheduleDisplay }} &bull; Shift 1: <span class="font-semibold text-navy-900 dark:text-white">{{ timeSlot }}</span>
                    </td>
                  </tr>
                  <tr>
                    <td class="py-1.5 px-3 font-semibold text-slate-600 dark:text-slate-300 bg-slate-50/80 dark:bg-slate-800/80">Tuition &amp; Payment Plan</td>
                    <td class="py-1.5 px-3 text-slate-700 dark:text-slate-200" colspan="3">
                      <span class="font-bold text-navy-900 dark:text-white">Fully Payment: ${{ totalAmountDue.toFixed(2) }} - QR Pay</span>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          <!-- Next Steps & First Day Orientation (From PDF) -->
          <div class="rounded-xl border border-slate-200/80 dark:border-slate-700/80 bg-slate-50/60 dark:bg-slate-800/50 p-3 print:p-2 text-[10px] print:text-[8.5px] leading-relaxed space-y-1.5">
            <p class="font-bold text-navy-900 dark:text-white text-[10.5px] print:text-[9px]">Next Steps &amp; First Day Orientation</p>
            <ul class="list-disc list-inside space-y-1 text-slate-600 dark:text-slate-300">
              <li><strong class="text-slate-800 dark:text-slate-200">Student ID Card:</strong> Please arrive 15 minutes before your shift on your first day to receive your official physical Student ID badge ($2.50 included in tuition plan).</li>
              <li><strong class="text-slate-800 dark:text-slate-200">Hardware &amp; Tooling:</strong> All microcontrollers, sensors, 3D printing filaments, and robotic components are prepared in-house through our KH Maker / Factory.io partnership.</li>
              <li><strong class="text-slate-800 dark:text-slate-200">Laptop Requirement:</strong> Bring your laptop (Windows or Mac). Our instructors will configure all required development tools (VS Code, Arduino IDE, or Fusion 360).</li>
              <li><strong class="text-slate-800 dark:text-slate-200">Tuition Settlement:</strong> Your full course fee of ${{ totalAmountDue.toFixed(2) }} USD (${{ basePrice.toFixed(0) }} course fee, ${{ adminFee.toFixed(1) }} administration fee, ${{ cardFee.toFixed(2) }} ID card, and ${{ certFee.toFixed(0) }} certificate) has been fully settled via KHQR Pay with a $0.00 balance remaining, officially securing your workstation reservation and immediate certificate release upon graduation.</li>
            </ul>
            <p class="font-bold text-[#0f2444] dark:text-indigo-300 pt-1">We look forward to engineering the future with you!</p>
          </div>

          <!-- Official Signatures & Seal Block (From PDF) -->
          <div class="flex items-center justify-between pt-3 border-t border-slate-200 dark:border-slate-800 text-xs print:text-[9px]">
            <!-- Left: CEO Signature -->
            <div class="space-y-1">
              <p class="text-[10px] print:text-[8px] text-slate-500 dark:text-slate-400 font-semibold italic">Sincerely,</p>
              <div class="h-8 print:h-6 flex items-center select-none my-0.5">
                <img
                  src="/vidhchetra-signature.png"
                  alt="Signature Vidhchetra.K"
                  class="h-7 sm:h-8 print:h-6 object-contain dark:brightness-0 dark:invert print:brightness-0 print:invert-0"
                />
              </div>
              <div>
                <p class="font-extrabold text-navy-950 dark:text-white">Ms. Khemarak Vidhchetra</p>
                <p class="text-[9px] print:text-[7.5px] text-slate-500 dark:text-slate-400">Co-Founder &amp; Chief Executive Officer (CEO)</p>
                <p class="text-[8.5px] print:text-[7px] text-slate-400 dark:text-slate-500">AeroByte Academy | Ta Kmau STEAM Hub</p>
              </div>
            </div>

            <!-- Right: Official Academy Seal (From PDF) -->
            <div class="w-56 print:w-44 rounded-xl border border-slate-300 dark:border-slate-700 p-2.5 print:p-2 text-center bg-slate-50/60 dark:bg-slate-800/60">
              <p class="font-bold text-[9px] print:text-[7.5px] tracking-wider text-slate-500 dark:text-slate-400 uppercase">[ OFFICIAL ACADEMY SEAL ]</p>
              <p class="font-extrabold text-[11px] print:text-[9px] text-navy-900 dark:text-white mt-0.5">Admissions Approval Office</p>
              <p class="text-[9px] print:text-[7.5px] text-slate-600 dark:text-slate-300">AeroByte Academy</p>
              <div class="mt-1 pt-0.5 border-t border-slate-200 dark:border-slate-700 flex items-center justify-center gap-1.5 text-[8px] print:text-[7px] text-[#16365c] dark:text-indigo-300 font-bold uppercase tracking-wider">
                <span>&#10003; Verified</span>
                <span>&bull;</span>
                <span>Intake Confirmed</span>
              </div>
            </div>
          </div>

          <!-- Page 2 Footer -->
          <div class="pt-2 border-t border-slate-100 dark:border-slate-800 text-[9px] print:text-[8px] text-center text-slate-400 dark:text-slate-500">
            Ta Kmau STEAM Hub, Kandal Province | Hotline: 015 341 002 | Email: aerobyte.academy@gmail.com &bull; Page 2 of 2
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'
import {
  ArrowLeft,
  Check,
  Copy,
  FileText,
  Printer,
} from 'lucide-vue-next'
import { enrollmentService } from '../services/api'
import { useLanguage } from '../i18n'

const route = useRoute()
const { t } = useLanguage()

const enrollment = ref(null)
const loading = ref(true)
const loadError = ref('')
const copied = ref(false)

const adminFee = computed(() => Number(enrollment.value?.administration_fee ?? 7.50))
const certFee = computed(() => Number(enrollment.value?.certification_fee ?? 5.00))
const cardFee = computed(() => Number(enrollment.value?.card_fee ?? 2.50))
const discountAmount = computed(() => Number(enrollment.value?.discount_amount ?? 0))

const totalAmountDue = computed(() => Number(enrollment.value?.amount_due ?? 0))

const basePrice = computed(() => {
  if (enrollment.value?.base_price && enrollment.value.base_price > 0) {
    return Number(enrollment.value.base_price)
  }
  const total = totalAmountDue.value
  const fees = adminFee.value + certFee.value + cardFee.value - discountAmount.value
  return Math.max(0, total - fees)
})

const subtotal = computed(() => {
  return basePrice.value + adminFee.value + certFee.value + cardFee.value
})

const grandTotalKHR = computed(() => {
  const khr = Math.round(totalAmountDue.value * 4050)
  return khr.toLocaleString('en-US') + '.00'
})

const receiptNo = computed(() => {
  if (enrollment.value?.transaction_id) {
    return enrollment.value.transaction_id
  }
  const id = enrollment.value?.enrollment_id || '000000'
  return `ABA-${id.replace(/[^a-zA-Z0-9]/g, '').slice(-8).toUpperCase()}-0001`
})

const receiptDate = computed(() => {
  const raw = enrollment.value?.created_at
  const date = raw ? new Date(raw) : new Date()
  const day = String(date.getDate()).padStart(2, '0')
  const months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
  const month = months[date.getMonth()]
  const year = date.getFullYear()
  return `${day}-${month}-${year}`
})

const studentId = computed(() => {
  if (enrollment.value?.enrollment_id) {
    return enrollment.value.enrollment_id.toUpperCase()
  }
  return 'ABA-STU-0001-1026'
})

const courseDescription = computed(() => {
  const duration = enrollment.value?.duration || '45 Hours'
  return `*${duration}`
})

const timeSlot = computed(() => {
  if (enrollment.value?.time_slot) return enrollment.value.time_slot
  if (enrollment.value?.preferred_schedule) return enrollment.value.preferred_schedule
  return '6:00 - 8:00 PM'
})

const studentDisplayName = computed(() => {
  return enrollment.value?.student_name 
    || enrollment.value?.full_name 
    || 'Valued Student'
})

const studentEmail = computed(() => {
  return enrollment.value?.email || 'aerobyte.academy@gmail.com'
})

const studentContact = computed(() => {
  return enrollment.value?.phone_telegram 
    || enrollment.value?.phone_number 
    || enrollment.value?.contact 
    || '015 341 002'
})

const studentAddress = computed(() => {
  return enrollment.value?.address 
    || 'Ta Kmau Krong, Kandal Province'
})

const studentScheduleDisplay = computed(() => {
  return enrollment.value?.preferred_schedule || 'Weekend Morning'
})

const courseTitleDisplay = computed(() => {
  return enrollment.value?.course_title || 'Robotics & STEAM Engineering Course'
})

async function fetchEnrollment() {
  loading.value = true
  loadError.value = ''

  // 1. Immediately read cached enrollment from local storage if available
  let cached = null
  try {
    const paramId = route.params.enrollmentId
    const stored = (paramId ? localStorage.getItem(`aerobyte-enrollment:${paramId}`) : null) 
      || localStorage.getItem('aerobyte-latest-enrollment')
    if (stored) {
      cached = JSON.parse(stored)
      if (!cached.student_name && cached.full_name) {
        cached.student_name = cached.full_name
      }
      enrollment.value = cached
    }
  } catch (e) {
    console.warn('Could not read cached enrollment:', e)
  }

  // 2. Fetch latest record from backend API
  try {
    const { data } = await enrollmentService.getEnrollment(route.params.enrollmentId)
    if (data) {
      const merged = { ...(cached || {}), ...data }
      if (!merged.student_name && merged.full_name) {
        merged.student_name = merged.full_name
      }
      enrollment.value = merged
    }
  } catch (error) {
    console.warn('API fetch failed, falling back to cache if present:', error)
    if (!enrollment.value && !cached) {
      loadError.value = 'Failed to load enrollment record. Please check the receipt URL.'
    }
  } finally {
    loading.value = false
  }
}

function printReceipt() {
  window.print()
}

async function copyReceiptLink() {
  try {
    await navigator.clipboard.writeText(window.location.href)
    copied.value = true
    setTimeout(() => {
      copied.value = false
    }, 2500)
  } catch (err) {
    console.error('Failed to copy receipt URL:', err)
  }
}

onMounted(() => {
  fetchEnrollment()
})
</script>

<style>
/* Universal Font Enforcement: Kantumruy Pro only */
.receipt-page-wrapper,
.receipt-page-wrapper *,
#printable-receipt,
#printable-receipt * {
  font-family: "Kantumruy Pro", sans-serif !important;
}

@media print {
  @page {
    size: A4 portrait;
    margin: 8mm 10mm 8mm 10mm;
  }

  html,
  body,
  #app,
  main,
  .receipt-page-wrapper {
    height: auto !important;
    min-height: 0 !important;
    max-height: none !important;
    margin: 0 !important;
    padding: 0 !important;
    background: white !important;
    overflow: visible !important;
    -webkit-print-color-adjust: exact !important;
    print-color-adjust: exact !important;
  }

  /* Reset Dark Mode when printing so PDF is always clean light print */
  html.dark,
  html.dark body,
  html.dark #app,
  html.dark .receipt-page-wrapper,
  html.dark #printable-receipt,
  html.dark .receipt-sheet {
    background: #ffffff !important;
    color: #0f172a !important;
  }

  html.dark #printable-receipt * {
    color-scheme: light !important;
  }

  /* Hide navigation, header, footer, utility action bar and any surrounding UI */
  header,
  footer,
  nav,
  .print\:hidden,
  .receipt-page-wrapper > div:first-child {
    display: none !important;
  }

  #printable-receipt {
    max-width: 100% !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 !important;
    background: white !important;
  }

  /* 2-Page Printing Rules: Page 1 on Sheet 1, Page 2 on Sheet 2 */
  .receipt-sheet {
    box-shadow: none !important;
    border: none !important;
    border-radius: 0 !important;
    margin: 0 !important;
    background: white !important;
    page-break-inside: avoid !important;
    break-inside: avoid !important;
  }

  .receipt-page-1 {
    page-break-after: always !important;
    break-after: page !important;
  }

  .receipt-page-2 {
    page-break-before: always !important;
    break-before: page !important;
  }

  /* Force exact colors and clean borders when printing */
  #printable-receipt .bg-\[\#102a4e\],
  html.dark #printable-receipt .bg-\[\#102a4e\],
  html.dark #printable-receipt .dark\:bg-slate-800 {
    background-color: #102a4e !important;
    color: #ffffff !important;
  }

  #printable-receipt .bg-\[\#1e3a61\],
  html.dark #printable-receipt .bg-\[\#1e3a61\] {
    background-color: #1e3a61 !important;
    color: #ffffff !important;
  }

  #printable-receipt .bg-\[\#d9e6f7\],
  html.dark #printable-receipt .bg-\[\#d9e6f7\] {
    background-color: #d9e6f7 !important;
    color: #0f2444 !important;
  }

  #printable-receipt .bg-\[\#eef4fc\],
  html.dark #printable-receipt .bg-\[\#eef4fc\] {
    background-color: #eef4fc !important;
    color: #1c3d6c !important;
  }

  /* Blue Acceptance Banner on print */
  #printable-receipt .bg-gradient-to-r,
  html.dark #printable-receipt .bg-gradient-to-r {
    background: #edf4fd !important;
    border-color: #b8d4f6 !important;
  }

  #printable-receipt th,
  #printable-receipt td {
    border-color: #cbd5e1 !important;
  }
}
</style>
