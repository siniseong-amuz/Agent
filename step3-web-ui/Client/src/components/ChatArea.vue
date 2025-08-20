<template>
  <div class="flex-1 flex flex-col">
    <div v-if="chatHistory.length > 0" class="flex-1 overflow-y-auto flex justify-center">
      <div class="w-full max-w-[56rem] px-4 py-4 space-y-6">
        <ChatMessage 
          v-for="(message, index) in chatHistory" 
          :key="index" 
          :message="message" 
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import ChatMessage from './ChatMessage.vue';
import { useChatHistory } from '../state/chatHistoryStore.js';

const { chatHistory } = useChatHistory();
</script>