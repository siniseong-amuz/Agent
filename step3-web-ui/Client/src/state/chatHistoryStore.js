import { atom, createStore } from 'jotai/vanilla';
import { ref, onMounted, onBeforeUnmount } from 'vue';

export const store = createStore();

export const chatHistoryAtom = atom([]);
export const currentChatIdAtom = atom(null);
export const historyLoadingAtom = atom(false);
export const historyErrorAtom = atom(null);

const apiUrl = import.meta.env.VITE_API_URL;

export function useChatHistory() {
  const chatHistory = ref(store.get(chatHistoryAtom));
  const currentChatId = ref(store.get(currentChatIdAtom));
  const historyLoading = ref(store.get(historyLoadingAtom));
  const historyError = ref(store.get(historyErrorAtom));

  let unsubHistory;
  let unsubChatId;
  let unsubHistoryLoading;
  let unsubHistoryError;

  const fetchChatHistory = async (chatId, limit = 50) => {
    if (!chatId) return;
    
    store.set(historyLoadingAtom, true);
    store.set(historyErrorAtom, null);
    store.set(currentChatIdAtom, chatId);

    try {
      const res = await fetch(`${apiUrl}/history/${encodeURIComponent(chatId)}?limit=${limit}`, {
        method: 'GET',
        headers: {
          Accept: 'application/json',
          'Content-Type': 'application/json'
        }
      });

      if (res.ok && res.headers.get('content-type')?.includes('application/json')) {
        const data = await res.json();
        store.set(chatHistoryAtom, Array.isArray(data) ? data : []);
      } else {
        store.set(historyErrorAtom, '채팅 히스토리를 불러올 수 없습니다.');
        store.set(chatHistoryAtom, []);
      }
    } catch (error) {
      store.set(historyErrorAtom, '채팅 히스토리를 불러올 수 없습니다.');
      store.set(chatHistoryAtom, []);
    } finally {
      store.set(historyLoadingAtom, false);
    }
  };

  const clearChatHistory = () => {
    store.set(chatHistoryAtom, []);
    store.set(currentChatIdAtom, null);
    store.set(historyErrorAtom, null);
  };



  onMounted(() => {
    unsubHistory = store.sub(chatHistoryAtom, () => (chatHistory.value = store.get(chatHistoryAtom)));
    unsubChatId = store.sub(currentChatIdAtom, () => (currentChatId.value = store.get(currentChatIdAtom)));
    unsubHistoryLoading = store.sub(historyLoadingAtom, () => (historyLoading.value = store.get(historyLoadingAtom)));
    unsubHistoryError = store.sub(historyErrorAtom, () => (historyError.value = store.get(historyErrorAtom)));
    
    chatHistory.value = store.get(chatHistoryAtom);
    currentChatId.value = store.get(currentChatIdAtom);
    historyLoading.value = store.get(historyLoadingAtom);
    historyError.value = store.get(historyErrorAtom);
  });

  onBeforeUnmount(() => {
    unsubHistory && unsubHistory();
    unsubChatId && unsubChatId();
    unsubHistoryLoading && unsubHistoryLoading();
    unsubHistoryError && unsubHistoryError();
  });

  return { 
    chatHistory, 
    currentChatId, 
    historyLoading, 
    historyError, 
    fetchChatHistory, 
    clearChatHistory
  };
}
