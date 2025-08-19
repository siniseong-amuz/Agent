<template>
  <footer 
    :class="[
      'fixed left-0 right-0 bottom-2 text-center text-[#7c7c7c] transition-[padding] duration-300 mb-4 mt-2 px-4',
      isMobile ? 'text-xs' : 'text-sm',
      isSidebarOpen ? 'pl-[260px]' : 'pl-0'
    ]"
  >
    <div class="max-w-full overflow-hidden">
      © 2025 Aero. | Developed by siniseong.
    </div>
  </footer>
</template>

<script setup>
defineProps({
  isSidebarOpen: {
    type: Boolean,
    required: true
  },
  isMobile: {
    type: Boolean,
    default: false
  }
})
</script>
