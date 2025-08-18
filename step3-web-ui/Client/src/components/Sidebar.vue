<template>
  <aside
    :class="[
      'fixed left-0 top-0 bottom-0 w-[260px] bg-[#151515] border-r border-[#2a2a2a] z-20 transition-transform duration-300',
      open ? 'translate-x-0' : '-translate-x-[244px]'
    ]"
  >
    <div class="h-16 flex items-center px-5 text-[#dedede] font-semibold text-lg">Aero</div>
    <nav class="py-2 space-y-1">
      <button type="button" class="block w-full text-left px-5 py-2 rounded-lg text-[#cfcfcf]">기록</button>
    </nav>
    <button
      class="absolute top-4 -right-4 w-8 h-8 rounded-full bg-[#2a2a2a] text-[#dedede] flex items-center justify-center shadow hover:bg-[#333]"
      @click="$emit('toggle')"
      aria-label="Toggle sidebar"
    >
      <img v-if="open" src="../assets/image/minus.svg" alt="collapse" class="w-5 h-5" />
      <img v-else src="../assets/image/bars.svg" alt="expand" class="w-5 h-5" />
    </button>
  </aside>
</template>

<script setup>
defineProps({
  open: {
    type: Boolean,
    default: true
  }
})

defineEmits(['toggle'])
</script>
