<template>
  <div class="min-h-screen bg-[#1E1E1E] flex flex-col">
    <div class="flex-1 flex items-center justify-center flex-col pt-30">
      <h1 class="text-4xl font-medium mb-2 gradient-text">안녕하세요, siniseong님</h1>
      <h1 class="text-4xl font-medium text-[#7c7c7c] mb-12">무엇을 도와드릴까요?</h1>
    </div>

    <div class="w-full max-w-4xl flex items-start gap-2 px-4 mb-8 mx-auto">
      <div class="relative flex-1">
        <textarea
          ref="textareaRef"
          v-model="message"
          rows="1"
          placeholder="오늘은 어떤걸 도와드릴까요?"
          class="w-full bg-[#303030] px-8 py-4.5 rounded-4xl focus:outline-none focus:ring-0 pr-16 text-lg text-[#dedede] placeholder-[#a0a0a0] resize-none overflow-hidden"
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
  </div>
</template>

<script setup>
import { ref, nextTick } from 'vue'

const message = ref('')
const textareaRef = ref(null)

const handleResizeHeight = () => {
  nextTick(() => {
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto'
      textareaRef.value.style.height = textareaRef.value.scrollHeight + 'px'
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
    if (textareaRef.value) {
      textareaRef.value.style.height = 'auto'
    }
  })
}
</script>