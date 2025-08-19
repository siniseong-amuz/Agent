<template>
  <aside :class="[
    'fixed left-0 top-0 bottom-0 border-r transition-transform duration-300 w-full z-20 md:w-[260px]',
    isDark ? 'bg-[#151515] border-[#2a2a2a]' : 'bg-gray-100 border-gray-200',
    open ? 'translate-x-0' : 'md:-translate-x-[244px] -translate-x-full'
  ]">
    <div :class="[
      'h-16 flex items-center px-5 font-semibold text-lg relative',
      isDark ? 'text-[#dedede]' : 'text-gray-800'
    ]">
      <img src="/logo.png" alt="Aero logo" class="w-6 h-6 mr-2" />
      <span>Aero</span>
      <button
        v-if="isMobile"
        @click="$emit('toggle')"
        :class="[
          'absolute right-5 w-8 h-8 rounded-full flex items-center justify-center shadow',
          isDark ? 'bg-[#2a2a2a] text-[#979797] hover:bg-[#333]' : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
        ]"
        aria-label="Close sidebar"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
          <path d="M5 12.75h14a.75.75 0 0 0 0-1.5H5a.75.75 0 0 0 0 1.5Z"/>
        </svg>
      </button>
    </div>
    <nav class="py-2 px-2 space-y-1">
      <button type="button" :class="[
        'flex items-center gap-2 w-full text-left px-3 py-2 rounded-lg',
        isDark ? 'text-[#dedede] hover:bg-[#2a2a2a]' : 'text-gray-800 hover:bg-gray-200'
      ]">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
          <path d="M12.75 5a.75.75 0 0 0-1.5 0v6.25H5a.75.75 0 0 0 0 1.5h6.25V19a.75.75 0 0 0 1.5 0v-6.25H19a.75.75 0 0 0 0-1.5h-6.25V5Z"/>
        </svg>
        <span>새 채팅</span>
      </button>
      <p type="button" :class="[
        'block w-full text-left px-3 py-2 rounded-lg mt-6',
        isDark ? 'text-[#cfcfcf]' : 'text-gray-600'
      ]">기록</p>
      <button type="button" :class="[
        'flex items-center w-full text-left px-3 py-2 rounded-lg text-lg font-medium transition-colors duration-200',
        isDark ? 'text-[#dedede] hover:bg-[#2a2a2a]' : 'text-gray-800 hover:bg-gray-200'
      ]">
        New Chat
      </button>
    </nav>
    <button
      v-if="!isMobile"
      :class="[
        'absolute top-4 -right-4 w-8 h-8 rounded-full flex items-center justify-center shadow',
        isDark ? 'bg-[#2a2a2a] text-[#979797] hover:bg-[#333]' : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
      ]"
      @click="$emit('toggle')"
      aria-label="Toggle sidebar"
    >
      <svg v-if="open" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
        <path d="M5 12.75h14a.75.75 0 0 0 0-1.5H5a.75.75 0 0 0 0 1.5Z"/>
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
        <path d="M3.75 5.25h16.5a.75.75 0 0 1 0 1.5H3.75a.75.75 0 0 1 0-1.5Zm0 6h16.5a.75.75 0 0 1 0 1.5H3.75a.75.75 0 0 1 0-1.5Zm0 6h16.5a.75.75 0 0 1 0 1.5H3.75a.75.75 0 0 1 0-1.5Z"/>
      </svg>
    </button>
  </aside>
</template>

<script setup>
defineProps({
  open: {
    type: Boolean,
    default: true
  },
  isMobile: {
    type: Boolean,
    default: false
  },
  isDark: {
    type: Boolean,
    default: false
  }
})

defineEmits(['toggle'])
</script>
