<template>
  <footer 
    :class="[
      'fixed left-0 right-0 bottom-2 text-center text-sm text-[#7c7c7c] transition-[padding] duration-300 mb-4 mt-2',
      isSidebarOpen ? 'pl-[260px]' : 'pl-0'
    ]"
  >
    © 2025 Aero. | Developed by siniseong.
  </footer>
</template>

<script setup>
defineProps({
  isSidebarOpen: {
    type: Boolean,
    required: true
  }
})
</script>
