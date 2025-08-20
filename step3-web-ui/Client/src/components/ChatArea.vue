<template>
  <div class="flex-1 flex flex-col">
    <div v-if="chatHistory.length > 0" class="flex-1 overflow-y-auto flex justify-center chat-scrollbar" style="max-height: calc(100vh - 235px);">
      <div class="w-full max-w-[56rem] px-4 py-4 space-y-6">
        <ChatMessage 
          v-for="(message, index) in chatHistory" 
          :key="index" 
          :message="message" 
        />
        <div class="h-20"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ChatMessage from './ChatMessage.vue';
import { useChatHistory } from '../state/chatHistoryStore.js';

const { chatHistory } = useChatHistory();
</script>

<style scoped>
.chat-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: #8b8b8b transparent;
}
.chat-scrollbar::-webkit-scrollbar {
  width: 6px;
}
.chat-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}
.chat-scrollbar::-webkit-scrollbar-thumb {
  background-color: #6b6b6b;
  border-radius: 9999px;
  border: 2px solid transparent;
  background-clip: padding-box;
}
.chat-scrollbar:hover::-webkit-scrollbar-thumb {
  background-color: #8b8b8b;
}
</style>