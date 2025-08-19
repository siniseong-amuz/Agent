<template>
  <button
    class="h-9 px-3 rounded-full bg-[var(--surface-2)] text-[var(--text)] flex items-center gap-2 hover:bg-[var(--hover)] transition-colors"
    @click="$emit('toggle')"
    :aria-label="isDark ? 'Switch to light mode' : 'Switch to dark mode'"
  >
    <span class="text-base" v-if="isDark">☀️</span>
    <span class="text-base" v-else>🌙</span>

  </button>
</template>

<script setup>
defineProps({
  isDark: {
    type: Boolean,
    default: false
  }
})
defineEmits(['toggle'])
</script>
