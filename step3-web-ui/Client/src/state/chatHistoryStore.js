import { atom, createStore } from 'jotai/vanilla';
import { ref, onMounted, onBeforeUnmount } from 'vue';

export const store = createStore();

const getStoredChatHistory = () => {
  try {
    const stored = localStorage.getItem('chatHistory');
    return stored ? JSON.parse(stored) : [];
  } catch {
    return [];
  }
};

const getStoredCurrentChatId = () => {
  return localStorage.getItem('currentChatId') || null;
};

export const chatHistoryAtom = atom(getStoredChatHistory());
export const currentChatIdAtom = atom(getStoredCurrentChatId());
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
    
    localStorage.setItem('currentChatId', chatId);

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
        const historyData = Array.isArray(data) ? data : [];
        store.set(chatHistoryAtom, historyData);
        
        localStorage.setItem('chatHistory', JSON.stringify(historyData));
      } else {
        store.set(historyErrorAtom, '채팅 히스토리를 불러올 수 없습니다.');
        store.set(chatHistoryAtom, []);
        localStorage.setItem('chatHistory', JSON.stringify([]));
      }
    } catch (error) {
      store.set(historyErrorAtom, '채팅 히스토리를 불러올 수 없습니다.');
      store.set(chatHistoryAtom, []);
      localStorage.setItem('chatHistory', JSON.stringify([]));
    } finally {
      store.set(historyLoadingAtom, false);
    }
  };

  const clearChatHistory = () => {
    store.set(chatHistoryAtom, []);
    store.set(currentChatIdAtom, null);
    store.set(historyErrorAtom, null);
    localStorage.removeItem('chatHistory');
    localStorage.removeItem('currentChatId');
  };

  const addMessageToHistory = (message) => {
    const currentHistory = store.get(chatHistoryAtom);
    const updatedHistory = [...currentHistory, message];
    store.set(chatHistoryAtom, updatedHistory);

    localStorage.setItem('chatHistory', JSON.stringify(updatedHistory));
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
    clearChatHistory,
    addMessageToHistory
  };
}
