  <template>
    <div class="flex-1 flex flex-col pt-16">

    <div v-if="chatHistory.length > 0" class="flex-1 overflow-y-auto px-4 py-6 space-y-4">
      <ChatMessage 
        v-for="(message, index) in chatHistory" 
        :key="index" 
        :message="message" 
      />
    </div>


  </div>
</template>

<script setup>
import ChatMessage from './ChatMessage.vue';
import { useChatHistory } from '../state/chatHistoryStore.js';

const { chatHistory } = useChatHistory();
</script>