<template>
  <div
    class="min-h-screen flex flex-col bg-slate-50 dark:bg-slate-950 text-slate-800 dark:text-slate-100 transition-colors duration-200 overflow-x-clip"
    :class="{ 'h-screen overflow-hidden': route.name === 'admin' }"
  >
    <Navbar v-if="!['account', 'admin'].includes(route.name)" />
    <main class="flex-1 min-h-0" :class="{ 'h-screen overflow-hidden': route.name === 'admin' }">
      <RouterView />
    </main>
    <Footer v-if="!['account', 'admin'].includes(route.name)" />
  </div>
</template>

<script setup>
import { onUnmounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import Navbar from './components/layout/Navbar.vue'
import Footer from './components/layout/Footer.vue'

const route = useRoute()

watch(
  () => route.name,
  (name) => {
    if (name === 'admin') {
      document.documentElement.classList.add('admin-locked-viewport')
      document.body.classList.add('admin-locked-viewport')
    } else {
      document.documentElement.classList.remove('admin-locked-viewport')
      document.body.classList.remove('admin-locked-viewport')
    }
  },
  { immediate: true },
)

onUnmounted(() => {
  document.documentElement.classList.remove('admin-locked-viewport')
  document.body.classList.remove('admin-locked-viewport')
})
</script>
