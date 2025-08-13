import google.generativeai as genai
import os
from typing import List, Tuple, Union

def get_gemini_model():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel("gemini-2.0-flash")

def json_escape(text: str) -> str:
    return text.replace('\\', '\\\\').replace('"', '\\"').replace('\n', '\\n').replace('\r', '\\r').replace('\t', '\\t')

def stream_text(text: str) -> str:
    for char in text:
        print(json_escape(char), end="", flush=True)
    return text

def stream_ai_response(prompt: str) -> str:
    model = get_gemini_model()
    full_response = ""
    
    try:
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                for char in chunk.text:
                    print(json_escape(char), end="", flush=True)
                full_response += chunk.text
    except Exception as e:
        error_msg = f"오류 발생: {e}"
        full_response = stream_text(error_msg)
    
    return full_response

class StreamingResponse:
    def __init__(self, user_input: str, intent: str):
        self.user_input = user_input
        self.intent = intent
        self.results = []
        
    def add_title(self, title_prompt: str) -> str:
        print('{', flush=True)
        print(f'  "input": "{self.user_input}",', flush=True)
        print('  "title": "', end="", flush=True)
        
        try:
            title = stream_ai_response(title_prompt)
        except:
            title = stream_text("제목 생성 오류")
            
        print('",', flush=True)
        print(f'  "intent": "{self.intent}",', flush=True)
        print('  "result": {', flush=True)
        return title.strip()
        
    def add_field(self, field_name: str, content: Union[str, tuple], is_last: bool = False):
        print(f'    "{field_name}": "', end="", flush=True)
        
        if isinstance(content, tuple) and len(content) == 2:
            prompt, is_ai = content
            result = stream_ai_response(prompt) if is_ai else stream_text(prompt)
        else:
            result = stream_ai_response(content)
            
        comma = "" if is_last else ","
        print(f'"{comma}', flush=True)
        self.results.append(result)
        
    def finish(self):
        print('  }', flush=True)
        print('}', flush=True)

def stream_with_fields(user_input: str, intent: str, title_prompt: str, fields: List[Tuple]) -> Tuple:
    response = StreamingResponse(user_input, intent)
    title = response.add_title(title_prompt)
    
    for i, (field_name, content) in enumerate(fields):
        is_last = i == len(fields) - 1
        response.add_field(field_name, content, is_last)
    
    response.finish()
    return tuple([title] + response.results)

def stream_translation(user_input: str, intent: str, title_prompt: str, response_prompt: str) -> Tuple[str, str, str]:
    fields = [
        ("original", (user_input, False)),
        ("translation", (response_prompt, True))
    ]
    return stream_with_fields(user_input, intent, title_prompt, fields)

def stream(user_input: str, intent: str, title_prompt: str, response_prompt: str) -> Tuple[str, str]:
    fields = [("response", response_prompt)]
    return stream_with_fields(user_input, intent, title_prompt, fields)

def stream_emotion(user_input: str, intent: str, title_prompt: str, emotion_prompt: str, message_prompt: str) -> Tuple[str, str, str]:
    fields = [
        ("response", emotion_prompt),
        ("message", message_prompt)
    ]
    return stream_with_fields(user_input, intent, title_prompt, fields)