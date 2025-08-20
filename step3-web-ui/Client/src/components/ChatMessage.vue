<template>
  <div class="flex flex-col space-y-4">
    <div class="flex justify-end">
      <div class="max-w-[85%] lg:max-w-[75%]">
        <div class="bg-[var(--surface)] text-[var(--text)] rounded-3xl px-4 py-2">
          <p class="text-lg whitespace-pre-wrap">{{ message.input }}</p>
        </div>
      </div>
    </div>

    <div class="flex justify-start" v-if="message.result && (typeof message.result === 'object' ? Object.keys(message.result).length > 0 : String(message.result).trim() !== '')">
      <div class="max-w-[85%] lg:max-w-[75%]">
        <div class="space-y-3">
          <div v-if="message.intent" class="text-xs text-gray-500 dark:text-gray-400">
            <span class="font-medium"></span> {{ message.intent }}
          </div>
          
          <div class="text-xl text-[var(--text)] whitespace-pre-wrap">
            <template v-if="typeof parseAIResponse(message.result) === 'object' && parseAIResponse(message.result).type === 'translation'">
              <div class="translation-container">
                <div class="original-text">
                  <span class="label">원문: </span>
                  <span class="content">{{ parseAIResponse(message.result).original }}</span>
                </div>
                <div class="translation-text">
                  <span class="label">번역문: </span>
                  <span class="highlighted-text content">{{ parseAIResponse(message.result).translation }}</span>
                </div>
              </div>
            </template>
            <template v-else>
              {{ parseAIResponse(message.result) }}
            </template>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { parseAIResponse } from '../utils/responseParser.js';

const props = defineProps({
  message: {
    type: Object,
    required: true
  }
});
</script>

<style scoped>
.translation-container {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.original-text {
  margin-bottom: 4px;
}

.translation-text {
  margin-top: 4px;
}

.highlighted-text {
  background: linear-gradient(to top, rgba(59, 130, 246, 0.3) 50%, transparent 50%);
  padding: 2px 6px;
  display: inline;
  box-decoration-break: clone;
  -webkit-box-decoration-break: clone;
}
</style>