import time
from typing import Iterator

def stream_json_response(user_input: str, title: str, intent: str, response_iterator: Iterator[str]) -> str:
    print('{', end="", flush=True)
    time.sleep(0.1)
    
    print('\n  "input": "', end="", flush=True)
    time.sleep(0.05)
    for char in user_input:
        print(char, end="", flush=True)
        time.sleep(0.03)
    print('",', end="", flush=True)
    time.sleep(0.05)
    
    print('\n  "title": "', end="", flush=True)
    time.sleep(0.05)
    for char in title:
        print(char, end="", flush=True)
        time.sleep(0.03)
    print('",', end="", flush=True)
    time.sleep(0.05)
    
    print('\n  "intent": "', end="", flush=True)
    time.sleep(0.05)
    for char in intent:
        print(char, end="", flush=True)
        time.sleep(0.03)
    print('",', end="", flush=True)
    time.sleep(0.05)
    
    print('\n  "result": {', end="", flush=True)
    time.sleep(0.1)
    
    print('\n    "response": "', end="", flush=True)
    time.sleep(0.1)
    
    full_response = ""
    for chunk in response_iterator:
        if chunk:
            escaped_chunk = chunk.replace('\\', '\\\\').replace('"', '\\"').replace('\n', ' ').replace('\r', ' ').replace('\t', ' ')
            print(escaped_chunk, end="", flush=True)
            full_response += chunk
    
    print('"\n  }\n}', flush=True)
    
    return full_response