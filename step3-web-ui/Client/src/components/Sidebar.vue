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
        @click="createChat"
      >
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" class="w-4 h-4">
          <path d="M12.75 5a.75.75 0 0 0-1.5 0v6.25H5a.75.75 0 0 0 0 1.5h6.25V19a.75.75 0 0 0 1.5 0v-6.25H19a.75.75 0 0 0 0-1.5h-6.25V5Z" />
        </svg>
        <span>새 채팅</span>
      </button>

      <p :class="['block w-full text-left px-3 py-2 rounded-lg mt-6', isDark ? 'text-[#cfcfcf]' : 'text-gray-600']">기록</p>

      <div v-if="loading" :class="['px-3 py-2', isDark ? 'text-[#979797]' : 'text-gray-500']">
        <div class="animate-pulse">채팅방을 불러오는 중...</div>
      </div>

      <div v-else-if="error" :class="['px-3 py-2 text-sm', isDark ? 'text-red-400' : 'text-red-600']">{{ error }}</div>

      <div v-else class="space-y-1">
        <button
          v-for="chatroom in chatrooms"
          :key="chatroom.id"
          type="button"
          :class="[
            'flex items-center w-full text-left px-3 py-2 rounded-lg transition-colors duration-200',
            isDark ? 'text-[#dedede] hover:bg-[#2a2a2a]' : 'text-gray-800 hover:bg-gray-200'
          ]"
          @click="$emit('select-chat', chatroom.id)"
          :title="chatroom.title"
        >
          <span class="truncate">{{ chatroom.title }}</span>
        </button>
      </div>

      <div v-if="!loading && !error && chatrooms.length === 0" :class="['px-3 py-2 text-sm', isDark ? 'text-[#979797]' : 'text-gray-500']">채팅방이 없습니다.</div>
    </nav>

    <button
      :class="[
        'absolute top-4 w-8 h-8 rounded-full flex items-center justify-center shadow z-30',
        'right-4 md:-right-4',
        isDark ? 'bg-[#2a2a2a] text-[#979797] hover:bg-[#333]' : 'bg-gray-200 text-gray-600 hover:bg-gray-300'
      ]"
      @click="$emit('toggle')"
      :aria-label="open ? '사이드바 닫기' : '사이드바 열기'"
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
import { ref, onMounted, onBeforeUnmount } from 'vue';
import ThemeToggle from './ThemeToggle.vue';
import { atom, createStore } from 'jotai/vanilla';

const props = defineProps({
  open: { type: Boolean, default: true },
  isDark: { type: Boolean, default: false }
});

defineEmits(['toggle', 'toggle-theme', 'select-chat']);

const store = createStore();
const chatroomsAtom = atom([]);
const loadingAtom = atom(false);
const errorAtom = atom(null);

const chatrooms = ref([]);
const loading = ref(false);
const error = ref(null);

const apiUrl = import.meta.env.VITE_API_URL;

const fetchChatrooms = async () => {
  store.set(loadingAtom, true);
  store.set(errorAtom, null);

  try {
    const res = await fetch(`${apiUrl}/chatrooms`, {
      method: 'GET',
      headers: {
        Accept: 'application/json',
        'Content-Type': 'application/json'
      }
    });

    if (res.ok && res.headers.get('content-type')?.includes('application/json')) {
      const data = await res.json();
      store.set(chatroomsAtom, Array.isArray(data) ? data : []);
    } else {
      store.set(errorAtom, '채팅방 목록을 불러올 수 없습니다.');
    }
  } catch {
    store.set(errorAtom, '채팅방 목록을 불러올 수 없습니다.');
  } finally {
    store.set(loadingAtom, false);
  }
};

const createChat = async () => {
  const res = await fetch(`${apiUrl}/newchat`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
      'Content-Type': 'application/json'
    }
  });

  if (res.ok && res.headers.get('content-type')?.includes('application/json')) {
    const created = await res.json();
    store.set(chatroomsAtom, [created, ...store.get(chatroomsAtom)]);
  } else {
    store.set(errorAtom, '새 채팅을 생성할 수 없습니다.');
  }
};

let unsubRooms;
let unsubLoading;
let unsubError;

onMounted(() => {
  unsubRooms = store.sub(chatroomsAtom, () => (chatrooms.value = store.get(chatroomsAtom)));
  unsubLoading = store.sub(loadingAtom, () => (loading.value = store.get(loadingAtom)));
  unsubError = store.sub(errorAtom, () => (error.value = store.get(errorAtom)));
  chatrooms.value = store.get(chatroomsAtom);
  loading.value = store.get(loadingAtom);
  error.value = store.get(errorAtom);
  fetchChatrooms();
});

onBeforeUnmount(() => {
  unsubRooms && unsubRooms();
  unsubLoading && unsubLoading();
  unsubError && unsubError();
});

defineExpose({ refreshChatrooms: fetchChatrooms });
</script>

<style scoped>
.custom-scrollbar {
  scrollbar-width: none;
}
.custom-scrollbar::-webkit-scrollbar {
  display: none;
}
</style>