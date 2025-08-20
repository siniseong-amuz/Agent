<template>
  <div class="min-h-screen bg-[var(--bg)] flex flex-col pb-32 transition-[padding] duration-300 pl-0 md:pl-0" 
       :class="isSidebarOpen && !isMobile ? 'md:pl-[260px]' : ''">
    <Sidebar 
      :open="isSidebarOpen" 
      @toggle="toggleSidebar" 
      @toggle-theme="toggleTheme" 
      @select-chat="selectChat"
      :is-mobile="isMobile" 
      :is-dark="isDark" 
    />
    <Header @toggle-sidebar="toggleSidebar" :is-mobile="isMobile" :is-dark="isDark" @toggle-theme="toggleTheme" :title="currentChatTitle" />
    
    <div class="flex-1 flex flex-col pt-8">
      <div v-if="!currentChatId || (currentChatId && (!chatHistory || chatHistory.length === 0))" class="flex-1 flex items-center justify-center flex-col px-4">
        <h1 class="font-semibold mb-2 gradient-text text-3xl md:text-4xl">안녕하세요, siniseong님</h1>
        <h1 class="font-medium text-gray-600 dark:text-[#7c7c7c] mb-12 text-3xl md:text-4xl">무엇을 도와드릴까요?</h1>
      </div>
      
      <div v-else class="flex-1 flex flex-col">
        <ChatArea />
      </div>
    </div>
    <div class="fixed left-0 right-0 bottom-14 w-full flex items-start gap-2 mx-auto transition-[padding,max-width] duration-300 px-4 max-w-full md:max-w-[56rem] md:pl-0"
         :class="isSidebarOpen && !isMobile ? 'md:max-w-[72rem] md:pl-[260px]' : ''">
      <div class="relative flex-1">
        <textarea
          ref="textareaRef"
          v-model="message"
          rows="1"
          placeholder="메시지를 입력하세요..."
          class="w-full bg-[var(--surface)] rounded-4xl focus:outline-none focus:ring-0 text-[var(--text)] placeholder-[var(--subtext)] resize-none custom-scrollbar px-4 py-3 pr-12 text-base md:px-8 md:py-4.5 md:pr-16 md:text-lg"
          @input="handleResizeHeight"
          @keydown="handleKeydown"
        />
        <button 
          @click="sendMessage"
          :disabled="!message.trim()"
          :class="[
            'absolute bottom-3 rounded-full flex items-center justify-center transition-colors cursor-pointer right-3 w-8 h-8 md:right-4 md:bottom-4 md:w-10 md:h-10',
            isDark ? 'bg-gray-200 hover:bg-gray-300 disabled:bg-gray-100 disabled:cursor-not-allowed' : 'bg-black hover:bg-gray-800 disabled:bg-gray-400 disabled:cursor-not-allowed'
          ]"
        >
          <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" :class="['w-4 h-4 md:w-5 md:h-5', isDark ? 'text-gray-800' : 'text-white']">
            <path stroke-linecap="round" stroke-linejoin="round" d="M4.5 10.5 12 3m0 0 7.5 7.5M12 3v18" />
          </svg>
        </button>
      </div>
    </div>
    
    <Footer :is-sidebar-open="isSidebarOpen && !isMobile" :is-mobile="isMobile" />
  </div>
</template>

<script setup>
import { ref, nextTick, onMounted, onUnmounted, watch, computed } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import Header from '../components/Header.vue'
import Sidebar from '../components/Sidebar.vue'
import Footer from '../components/Footer.vue'
import ChatArea from '../components/ChatArea.vue'
import { useChatHistory } from '../state/chatHistoryStore.js'
import { useChatrooms } from '../state/chatroomsStore.js'

const router = useRouter()
const route = useRoute()

const message = ref('')
const textareaRef = ref(null)
const isSidebarOpen = ref(true)
const isMobile = ref(false)
const isDark = ref(false)

const { currentChatId, chatHistory, fetchChatHistory, clearChatHistory } = useChatHistory()
const { chatrooms } = useChatrooms()

const currentChatTitle = computed(() => {
  if (!currentChatId.value) return 'New Chat'
  const currentChat = chatrooms.value.find(chat => chat.id === currentChatId.value)
  return currentChat ? currentChat.title : 'New Chat'
})

watch(() => route.params.id, async (newChatId) => {
  if (newChatId && newChatId !== currentChatId.value) {
    await fetchChatHistory(newChatId)
  } else if (!newChatId && currentChatId.value) {
    clearChatHistory()
  }
}, { immediate: true })

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

  const stored = localStorage.getItem('theme')
  if (stored === 'dark') {
    isDark.value = true
  } else if (stored === 'light') {
    isDark.value = false
  } else {
    isDark.value = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches
  }
  document.documentElement.classList.toggle('dark', isDark.value)
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

const selectChat = async (chatId) => {
  if (chatId === currentChatId.value) return
  
  if (isMobile.value) {
    isSidebarOpen.value = false
  }
  
  if (chatId) {
    await router.push(`/chat/${chatId}`)
  } else {
    await router.push('/')
  }
}

const sendMessage = async () => {
  if (!message.value.trim()) return
  
  const userMessage = message.value.trim()
  message.value = ''
  
  nextTick(() => {
    const el = textareaRef.value
    if (el) {
      el.style.height = 'auto'
      el.style.overflowY = 'hidden'
      el.scrollTop = 0
    }
  })
  
  console.log('Sending message:', userMessage, 'to chat:', currentChatId.value)
}

const toggleTheme = () => {
  isDark.value = !isDark.value
  localStorage.setItem('theme', isDark.value ? 'dark' : 'light')
  document.documentElement.classList.toggle('dark', isDark.value)
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
