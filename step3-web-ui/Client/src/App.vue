<template>
  <div :class="['min-h-screen bg-[#1E1E1E] flex flex-col pb-32 transition-[padding] duration-300', isSidebarOpen ? 'pl-[260px]' : 'pl-0']">
    <Sidebar :open="isSidebarOpen" @toggle="isSidebarOpen = !isSidebarOpen" />
    <Header />
    <div class="flex-1 flex items-center justify-center flex-col pt-24">
      <h1 class="text-4xl font-medium mb-2 gradient-text">안녕하세요, siniseong님</h1>
      <h1 class="text-4xl font-medium text-[#7c7c7c] mb-12">무엇을 도와드릴까요?</h1>
    </div>
    <div
      :class="[
        'fixed left-0 right-0 bottom-14 w-full flex items-start gap-2 px-4 mx-auto transition-[padding,max-width] duration-300',
        isSidebarOpen ? 'max-w-[72rem] pl-[260px]' : 'max-w-[56rem] pl-0'
      ]"
    >
      <div class="relative flex-1">
        <textarea
          ref="textareaRef"
          v-model="message"
          rows="1"
          placeholder="오늘은 어떤걸 도와드릴까요?"
          class="w-full bg-[#303030] px-8 py-4.5 rounded-4xl focus:outline-none focus:ring-0 pr-16 text-lg text-[#dedede] placeholder-[#a0a0a0] resize-none custom-scrollbar"
          @input="handleResizeHeight"
          @keydown="handleKeydown"
        />
        <button 
          @click="sendMessage"
          class="absolute right-4 bottom-4 w-10 h-10 bg-white rounded-full flex items-center justify-center hover:bg-gray-100 transition-colors cursor-pointer"
        >
          <img src="./assets/image/send-icon.svg" alt="Send" class="w-5 h-5 send-icon" />
        </button>
      </div>
    </div>
    
    <Footer :is-sidebar-open="isSidebarOpen" />
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'
import Header from './components/Header.vue'
import Sidebar from './components/Sidebar.vue'
import Footer from './components/Footer.vue'

const message = ref('')
const textareaRef = ref(null)
const isSidebarOpen = ref(true)

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