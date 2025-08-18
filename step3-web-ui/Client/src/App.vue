<template>
  <div class="min-h-screen bg-[#1E1E1E] flex items-center justify-center flex-col">
    <h1 class="text-4xl font-medium mb-2 gradient-text">안녕하세요, siniseong님</h1>
    <h1 class="text-4xl font-medium text-[#7c7c7c] mb-12">무엇을 도와드릴까요?</h1>

          <div class="w-full max-w-4xl flex items-center gap-2 px-4">
        <div class="relative flex-1">
          <input
            v-model="message"
            type="text"
            placeholder="오늘은 어떤걸 도와드릴까요?"
            class="w-full bg-[#303030] px-8 py-4.5 rounded-4xl focus:outline-none focus:ring-0 pr-16 text-lg text-[#d6d6d6] placeholder-[#a0a0a0]"
            @keyup.enter="sendMessage"
          />
          <button 
            @click="sendMessage"
            class="absolute right-2 top-1/2 transform -translate-y-1/2 w-10 h-10 bg-white rounded-full flex items-center justify-center hover:bg-gray-100 transition-colors cursor-pointer"
          >
            <img src="./assets/image/send-icon.svg" alt="Send" class="w-5 h-5 send-icon" />
          </button>
        </div>
      </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const message = ref('')

const sendMessage = () => {
  if (!message.value.trim()) return
  message.value = ''
}
</script>