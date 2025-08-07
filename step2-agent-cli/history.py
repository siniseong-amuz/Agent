import json
import os
from typing import List, Dict, Any
from datetime import datetime

class HistoryManager:
    def __init__(self, max_history: int = 10, file_path: str = "history.json"):
        self.max_history = max_history
        self.file_path = file_path
        self.history_data: List[Dict[str, Any]] = []
        self.load_history()
    
    def add_history(self, user_input: str, response: str, intent: str, title: str):
        history_entry = {
            "user_input": user_input,
            "response": response,
            "intent": intent,
            "title": title
        }
        
        self.history_data.append(history_entry)
        
        if len(self.history_data) > self.max_history:
            self.history_data = self.history_data[-self.max_history:]
        
        self.save_history()
    
    def get_recent_context(self, count: int = 3) -> str:
        if not self.history_data:
            return ""
        
        recent_entries = self.history_data[-count:]
        context_parts = []
        
        for entry in recent_entries:
            context_parts.append(f"사용자: {entry['user_input']}")
            context_parts.append(f"AI: {entry['response']}")
        
        return "\n".join(context_parts)
    
    def get_last_response(self) -> str:
        if self.history_data:
            return self.history_data[-1]['response']
        return ""
    
    def get_history_data(self) -> List[Dict[str, Any]]:
        return self.history_data.copy()
    
    def clear_history(self):
        self.history_data = []
        self.save_history()
    
    def save_history(self):
        try:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.history_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"히스토리 저장 중 오류: {e}")
    
    def load_history(self):
        try:
            if os.path.exists(self.file_path):
                with open(self.file_path, 'r', encoding='utf-8') as f:
                    self.history_data = json.load(f)
        except Exception as e:
            print(f"히스토리 로드 중 오류: {e}")
            self.history_data = []