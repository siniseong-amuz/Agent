<template>
  <div class="flex flex-col space-y-4">
    <div class="flex justify-end">
      <div class="max-w-[85%] lg:max-w-[75%]">
        <div class="bg-[var(--surface)] text-[var(--text)] rounded-3xl px-4 py-2">
          <p class="text-lg whitespace-pre-wrap">{{ message.input }}</p>
        </div>
        <div class="text-xs text-gray-500 mt-1 text-right">
          {{ formatTime(message.timestamp) }}
        </div>
      </div>
    </div>

    <div class="flex justify-start">
      <div class="max-w-[85%] lg:max-w-[75%]">
        <div class="space-y-3">
          <div v-if="message.intent" class="text-xs text-gray-500 dark:text-gray-400">
            <span class="font-medium"></span> {{ message.intent }}
          </div>
          
          <div class="text-xl text-gray-800 dark:text-gray-200 whitespace-pre-wrap">
            {{ message.result }}
          </div>
        </div>
        <div class="text-xs text-gray-500 mt-1">
          {{ formatTime(message.timestamp) }}
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const props = defineProps({
  message: {
    type: Object,
    required: true
  }
});

const formatTime = (timestamp) => {
  if (!timestamp) return '';
  
  const date = new Date(timestamp);
  const now = new Date();
  const diffInHours = (now - date) / (1000 * 60 * 60);
  
  if (diffInHours < 24) {
    return date.toLocaleTimeString('ko-KR', { 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false 
    });
  } else {
    return date.toLocaleDateString('ko-KR', { 
      month: 'short', 
      day: 'numeric',
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false 
    });
  }
};
</script>