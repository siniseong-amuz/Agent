<template>
  <aside
    :class="[
      'fixed left-0 top-0 bottom-0 w-[260px] bg-[#151515] border-r border-[#2a2a2a] z-20 transition-transform duration-300',
      open ? 'translate-x-0' : '-translate-x-[244px]'
    ]"
  >
    <div class="h-16 flex items-center px-5 text-[#dedede] font-semibold text-lg">Aero</div>
    <nav class="py-2 px-2 space-y-1">
      <button type="button" class="flex items-center gap-2 w-full text-left px-3 py-2 rounded-lg text-[#dedede] hover:bg-[#2a2a2a]">
        <img src="../assets/image/plus.svg" alt="새 채팅" class="w-4 h-4" />
        <span>새 채팅</span>
      </button>
      <p type="button" class="block w-full text-left px-3 py-2 rounded-lg mt-6 text-[#cfcfcf]">기록</p>
    </nav>
    <button
      class="absolute top-4 -right-4 w-8 h-8 rounded-full bg-[#2a2a2a] text-[#979797] flex items-center justify-center shadow hover:bg-[#333]"
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