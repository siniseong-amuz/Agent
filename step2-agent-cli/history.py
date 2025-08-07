import json
import os
from typing import List, Dict, Any
from datetime import datetime
import glob

class HistoryManager:
    def __init__(self, max_history: int = 10, base_path: str = "history"):
        self.max_history = max_history
        self.base_path = base_path
        self.file_path = None
        self.history_data: List[Dict[str, Any]] = []
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
    
    def start_new_session(self) -> int:
        pattern = os.path.join(self.base_path, "history_*.json")
        existing_files = glob.glob(pattern)
        
        session_number = 1
        if existing_files:
            numbers = []
            for file_path in existing_files:
                try:
                    num = int(os.path.basename(file_path).replace("history_", "").replace(".json", ""))
                    numbers.append(num)
                except ValueError:
                    continue
            session_number = max(numbers) + 1 if numbers else 1
        
        self.file_path = os.path.join(self.base_path, f"history_{session_number}.json")
        self.history_data = []
        return session_number
    
    def add_history(self, input: str, response: str, intent: str):
        if self.file_path is None:
            self.start_new_session()
        
        self.history_data.append({
            "input": input,
            "response": response,
            "intent": intent,
            "timestamp": datetime.now().isoformat()
        })
        
        if len(self.history_data) > self.max_history:
            self.history_data = self.history_data[-self.max_history:]
        
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(self.history_data, f, ensure_ascii=False, indent=2)
    
    def get_recent_context(self, count: int = 3) -> str:
        if not self.history_data:
            return ""
        
        recent_entries = self.history_data[-count:]
        context_parts = []
        
        for entry in recent_entries:
            context_parts.append(f"사용자: {entry['input']}")
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
        if self.file_path:
            with open(self.file_path, 'w', encoding='utf-8') as f:
                json.dump(self.history_data, f, ensure_ascii=False, indent=2)