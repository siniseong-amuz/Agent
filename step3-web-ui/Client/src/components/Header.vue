<template>
  <header class="w-full">
    <div class="px-4 h-16 flex items-center relative">
      <button
        v-if="isMobile"
        @click="$emit('toggle-sidebar')"
        class="mr-4 w-8 h-8 flex items-center justify-center text-[#dedede] hover:bg-[#2a2a2a] rounded-lg transition-colors z-10"
      >
        <img src="../assets/image/bars.svg" alt="메뉴" class="w-5 h-5" />
      </button>
      <div class="absolute inset-0 flex items-center justify-center text-[#dedede] text-lg">title</div>
    </div>
  </header>
</template>

<script setup>
defineProps({
  isMobile: {
    type: Boolean,
    default: false
  }
})

defineEmits(['toggle-sidebar'])
</script>
