<template>
  <div class="min-h-screen bg-[#1E1E1E] flex flex-col pb-32 transition-[padding] duration-300 pl-0 md:pl-0" 
       :class="isSidebarOpen && !isMobile ? 'md:pl-[260px]' : ''">
    <Sidebar :open="isSidebarOpen" @toggle="toggleSidebar" :is-mobile="isMobile" />
    <Header @toggle-sidebar="toggleSidebar" :is-mobile="isMobile" />
    <div class="flex-1 flex items-center justify-center flex-col pt-24 px-4">
      <h1 class="font-semibold mb-2 gradient-text text-3xl md:text-4xl">안녕하세요, siniseong님</h1>
      <h1 class="font-medium text-[#7c7c7c] mb-12 text-3xl md:text-4xl">무엇을 도와드릴까요?</h1>
    </div>
    <div class="fixed left-0 right-0 bottom-14 w-full flex items-start gap-2 mx-auto transition-[padding,max-width] duration-300 px-4 max-w-full md:max-w-[56rem] md:pl-0"
         :class="isSidebarOpen && !isMobile ? 'md:max-w-[72rem] md:pl-[260px]' : ''">
      <div class="relative flex-1">
        <textarea
          ref="textareaRef"
          v-model="message"
          rows="1"
          placeholder="오늘은 어떤걸 도와드릴까요?"
          class="w-full bg-[#303030] rounded-4xl focus:outline-none focus:ring-0 text-[#dedede] placeholder-[#a0a0a0] resize-none custom-scrollbar px-4 py-3 pr-12 text-base md:px-8 md:py-4.5 md:pr-16 md:text-lg"
          @input="handleResizeHeight"
          @keydown="handleKeydown"
        />
        <button 
          @click="sendMessage"
          class="absolute bottom-3 bg-white rounded-full flex items-center justify-center hover:bg-gray-100 transition-colors cursor-pointer right-3 w-8 h-8 md:right-4 md:bottom-4 md:w-10 md:h-10"
        >
          <img src="./assets/image/send-icon.svg" alt="Send" class="w-4 h-4 md:w-5 md:h-5" />
        </button>
      </div>
    </div>
    
    <Footer :is-sidebar-open="isSidebarOpen && !isMobile" :is-mobile="isMobile" />
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted, watch } from 'vue'
import Header from './components/Header.vue'
import Sidebar from './components/Sidebar.vue'
import Footer from './components/Footer.vue'

const message = ref('')
const textareaRef = ref(null)
const isSidebarOpen = ref(true)
const isMobile = ref(false)

const checkMobile = () => {
  const wasMobile = isMobile.value
  isMobile.value = window.innerWidth < 768
  
  if (!wasMobile && isMobile.value) {
    isSidebarOpen.value = false
  }
}

const toggleSidebar = () => {
  isSidebarOpen.value = !isSidebarOpen.value
}

watch([isMobile, isSidebarOpen], ([mobile, sidebarOpen]) => {
  if (mobile && sidebarOpen) {
    document.body.style.overflow = 'hidden'
  } else {
    document.body.style.overflow = ''
  }
})

onMounted(() => {
  checkMobile()
  window.addEventListener('resize', checkMobile)
})

onUnmounted(() => {
  window.removeEventListener('resize', checkMobile)
  document.body.style.overflow = ''
})

const handleResizeHeight = () => {
  nextTick(() => {
    const el = textareaRef.value
    if (!el) return

    el.style.height = 'auto'

    const computed = window.getComputedStyle(el)
    const lineHeight = parseFloat(computed.lineHeight) || 28
    const paddingTop = parseFloat(computed.paddingTop) || 0
    const paddingBottom = parseFloat(computed.paddingBottom) || 0
    const maxVisibleLines = 10
    const maxHeight = lineHeight * maxVisibleLines + paddingTop + paddingBottom

    const newHeight = Math.min(el.scrollHeight, maxHeight)
    el.style.height = newHeight + 'px'

    const isOverflowing = el.scrollHeight > maxHeight
    el.style.overflowY = isOverflowing ? 'auto' : 'hidden'

    if (isOverflowing) {
      requestAnimationFrame(() => {
        el.scrollTop = el.scrollHeight
      })
    } else {
      el.scrollTop = 0
    }
  })
}

const handleKeydown = (event) => {
  if (event.key === 'Enter' && !event.shiftKey) {
    event.preventDefault()
    sendMessage()
  }
}

const sendMessage = () => {
  if (!message.value.trim()) return
  message.value = ''
  nextTick(() => {
    const el = textareaRef.value
    if (el) {
      el.style.height = 'auto'
      el.style.overflowY = 'hidden'
      el.scrollTop = 0
    }
  })
}
</script>

<style scoped>
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #8b8b8b transparent;
}
.custom-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: #6b6b6b;
  border-radius: 9999px;
  border: 2px solid transparent;
  background-clip: padding-box;
}
.custom-scrollbar:hover::-webkit-scrollbar-thumb {
  background-color: #8b8b8b;
}
</style>