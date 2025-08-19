<template>
  <header class="w-full">
    <div class="px-4 h-16 flex items-center relative">
      <button
        v-if="isMobile"
        @click="$emit('toggle-sidebar')"
        class="mr-4 w-8 h-8 flex items-center justify-center text-[var(--text)] hover:bg-[var(--hover)] rounded-lg transition-colors z-10"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
          <path d="M3.75 5.25h16.5a.75.75 0 0 1 0 1.5H3.75a.75.75 0 0 1 0-1.5Zm0 6h16.5a.75.75 0 0 1 0 1.5H3.75a.75.75 0 0 1 0-1.5Zm0 6h16.5a.75.75 0 0 1 0 1.5H3.75a.75.75 0 0 1 0-1.5Z"/>
        </svg>
      </button>
      <div class="absolute inset-0 flex items-center justify-center text-[var(--text)] text-lg">
        {{ title }}
      </div>
    </div>
  </header>
</template>

<script setup>
defineProps({
  isMobile: {
    type: Boolean,
    default: false
  },
  isDark: {
    type: Boolean,
    default: false
  },
  title: {
    type: String,
    default: 'New Chat'
  }
});

defineEmits(['toggle-sidebar', 'toggle-theme']);
</script>