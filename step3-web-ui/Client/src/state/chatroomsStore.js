import { atom, createStore } from 'jotai/vanilla';
import { ref, onMounted, onBeforeUnmount } from 'vue';

export const store = createStore();

export const chatroomsAtom = atom([]);
export const loadingAtom = atom(false);
export const errorAtom = atom(null);
const apiUrl = import.meta.env.VITE_API_URL;

export function useChatrooms() {
  const chatrooms = ref(store.get(chatroomsAtom));
  const loading = ref(store.get(loadingAtom));
  const error = ref(store.get(errorAtom));

  let unsubRooms;
  let unsubLoading;
  let unsubError;

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

  const deleteChatroom = async (id) => {
    const confirmed = window.confirm('이 채팅방을 삭제하시겠습니까?');
    if (!confirmed) return;
    try {
      const res = await fetch(`${apiUrl}/chatrooms/${encodeURIComponent(id)}`, {
        method: 'DELETE',
        headers: {
          Accept: 'application/json'
        }
      });

      if (!res.ok) {
        store.set(errorAtom, '채팅방을 삭제할 수 없습니다.');
        return;
      }

      const remaining = store.get(chatroomsAtom).filter((c) => c.id !== id);
      store.set(chatroomsAtom, remaining);
    } catch (e) {
      store.set(errorAtom, '채팅방을 삭제할 수 없습니다.');
    }
  };

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

  return { chatrooms, loading, error, fetchChatrooms, createChat, deleteChatroom };
}