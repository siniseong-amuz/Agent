<template>
  <aside
    :class="[
      'fixed left-0 top-0 bottom-0 border-r transition-transform duration-300 w-full z-20 md:w-[260px]',
      isDark ? 'bg-[#151515] border-[#2a2a2a]' : 'bg-gray-100 border-gray-200',
      open ? 'translate-x-0' : 'md:-translate-x-[244px] -translate-x-full'
    ]"
  >
    <div :class="['h-16 flex items-center px-5 font-semibold text-lg relative', isDark ? 'text-[#dedede]' : 'text-gray-800']">
      <img src="/logo.png" alt="Aero logo" class="w-6 h-6 mr-2" />
      <span>Aero</span>
    </div>

    <nav class="py-2 px-2 space-y-1 overflow-y-auto custom-scrollbar" style="height: calc(100% - 8rem)">
      <button
        type="button"
        :class="[
          'flex items-center gap-2 w-full text-left px-3 py-2 rounded-lg',
          isDark ? 'text-[#dedede] hover:bg-[#2a2a2a]' : 'text-gray-800 hover:bg-gray-200'
        ]"
        @click="handleCreateChat"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
          <path d="M12.75 5a.75.75 0 0 0-1.5 0v6.25H5a.75.75 0 0 0 0 1.5h6.25V19a.75.75 0 0 0 1.5 0v-6.25H19a.75.75 0 0 0 0-1.5h-6.25V5Z" />
        </svg>
        <span>새 채팅</span>
      </button>

      <p :class="['block w-full text-left px-3 py-2 rounded-lg mt-6', isDark ? 'text-[#cfcfcf]' : 'text-gray-600']">기록</p>

      <div v-if="!isInitialized" :class="['px-3 py-2', isDark ? 'text-[#979797]' : 'text-gray-500']">
        <div class="animate-pulse">채팅방을 불러오는 중...</div>
      </div>

      <div v-else-if="loading" :class="['px-3 py-2', isDark ? 'text-[#979797]' : 'text-gray-500']">
        <div class="animate-pulse">채팅방을 불러오는 중...</div>
      </div>

      <div v-else-if="error" :class="['px-3 py-2 text-sm', isDark ? 'text-red-400' : 'text-red-600']">{{ error }}</div>

      <div v-else class="space-y-1">
        <div
          v-for="chatroom in chatrooms"
          :key="chatroom.id"
          :class="[
            'group relative flex items-center w-full text-left px-3 py-2 rounded-lg transition-colors duration-200 cursor-pointer',
            isDark ? 'text-[#dedede] hover:bg-[#2a2a2a]' : 'text-gray-800 hover:bg-gray-200'
          ]"
          @click="handleChatSelect(chatroom.id)"
          :title="chatroom.title"
          role="button"
          tabindex="0"
        >
          <span class="flex-1 truncate">
            {{ (isTyping && chatroom.id === typingTargetId) ? typingText : chatroom.title }}
            <span v-if="isTyping && chatroom.id === typingTargetId" class="cursor">|</span>
          </span>
          <span
            class="opacity-0 group-hover:opacity-100 transition-opacity"
            @click.stop="deleteChatroom(chatroom.id)"
            :aria-label="'삭제'"
            :title="'삭제'"
          >
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-4 h-4"
                 :class="isDark ? 'text-[#979797] hover:text-[#cfcfcf]' : 'text-gray-600 hover:text-gray-800'">
              <path stroke-linecap="round" stroke-linejoin="round" d="m14.74 9-.346 9m-4.788 0L9.26 9m9.968-3.21c.342.052.682.107 1.022.166m-1.022-.165L18.16 19.673a2.25 2.25 0 0 1-2.244 2.077H8.084a2.25 2.25 0 0 1-2.244-2.077L4.772 5.79m14.456 0a48.108 48.108 0 0 0-3.478-.397m-12 .562c.34-.059.68-.114 1.022-.165m0 0a48.11 48.11 0 0 1 3.478-.397m7.5 0v-.916c0-1.18-.91-2.164-2.09-2.201a51.964 51.964 0 0 0-3.32 0c-1.18.037-2.09 1.022-2.09 2.201v.916m7.5 0a48.667 48.667 0 0 0-7.5 0" />
            </svg>
          </span>
        </div>
      </div>

      <div v-if="isInitialized && !loading && !error && chatrooms.length === 0" :class="['px-3 py-2 text-sm', isDark ? 'text-[#979797]' : 'text-gray-500']">채팅방이 없습니다.</div>
    </nav>

    <button
      :class="[
        'absolute top-4 w-8 h-8 rounded-full flex items-center justify-center shadow z-30',
        'right-4 md:-right-4',
        isDark ? 'bg-[#2a2a2a] text-[#979797] hover:bg-[#333]' : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
      ]"
      @click="$emit('toggle')"
    >
      <svg v-if="open" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
        <path d="M5 12.75h14a.75.75 0 0 0 0-1.5H5a.75.75 0 0 0 0 1.5Z" />
      </svg>
      <svg v-else xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-5 h-5">
        <path d="M3.75 5.25h16.5a.75.75 0 0 1 0 1.5H3.75a.75.75 0 0 1 0-1.5Zm0 6h16.5a.75.75 0 0 1 0 1.5H3.75a.75.75 0 0 1 0-1.5Zm0 6h16.5a.75.75 0 0 1 0 1.5H3.75a.75.75 0 0 1 0-1.5Z" />
      </svg>
    </button>

    <div class="absolute left-4 bottom-4">
      <ThemeToggle :is-dark="isDark" @toggle="$emit('toggle-theme')" />
    </div>
  </aside>
</template>

<script setup>
import ThemeToggle from './ThemeToggle.vue';
import { useChatrooms } from '../state/chatroomsStore.js';
import { ref, onMounted, watch } from 'vue';
import { startTypingAnimation } from '../utils/typingAnimation.js';

const props = defineProps({
  open: { type: Boolean, default: true },
  isDark: { type: Boolean, default: false }
});

const emit = defineEmits(['toggle', 'toggle-theme', 'select-chat']);

const { chatrooms, loading, error, fetchChatrooms, createChat, deleteChatroom } = useChatrooms();

const typingText = ref('');
const isTyping = ref(false);
const typingTargetId = ref(null);
let lastTitlesById = {};

// 저장된 데이터가 있으면 즉시 사용하고, 없으면 API 호출
const isInitialized = ref(false);

onMounted(() => {
  // 저장된 데이터가 있으면 즉시 사용
  if (chatrooms.value.length > 0) {
    isInitialized.value = true;
    lastTitlesById = Object.fromEntries(chatrooms.value.map(r => [r.id, r.title]));
  } else {
    // 저장된 데이터가 없으면 API 호출 후 초기화 완료
    fetchChatrooms().then(() => {
      isInitialized.value = true;
      lastTitlesById = Object.fromEntries(chatrooms.value.map(r => [r.id, r.title]));
    });
  }
});

const handleChatSelect = (chatId) => {
  emit('select-chat', chatId);
};

const handleCreateChat = async () => {
  const newChat = await createChat();
  if (newChat) {
    emit('select-chat', newChat.id);
    
    startTypingAnimation(
      newChat.title,
      (text) => {
        typingTargetId.value = newChat.id;
        isTyping.value = true;
        typingText.value = text;
      },
      () => {
        isTyping.value = false;
        typingText.value = '';
        typingTargetId.value = null;
      },
      80,
      200
    );
  }
};

defineExpose({ refreshChatrooms: fetchChatrooms });

watch(
  chatrooms,
  (rooms) => {
    if (!Array.isArray(rooms) || rooms.length === 0) return;
    const mapNow = Object.fromEntries(rooms.map(r => [r.id, r.title]));
    for (const room of rooms) {
      const prevTitle = lastTitlesById[room.id];
      const currTitle = mapNow[room.id];
      if (prevTitle && currTitle && prevTitle !== currTitle && currTitle !== 'new chat') {
        typingTargetId.value = room.id;
        isTyping.value = true;
        typingText.value = '';
        startTypingAnimation(
          currTitle,
          (text) => {
            typingText.value = text;
          },
          () => {
            isTyping.value = false;
            typingText.value = '';
            typingTargetId.value = null;
          },
          80,
          0
        );
        break;
      }
    }
    lastTitlesById = mapNow;
  },
  { deep: true }
);
</script>

<style scoped>
.custom-scrollbar {
  scrollbar-width: none;
}
.custom-scrollbar::-webkit-scrollbar {
  display: none;
}

.cursor {
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 50% { opacity: 1; }
  51%, 100% { opacity: 0; }
}
</style>