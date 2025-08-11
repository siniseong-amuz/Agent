import sys
import time
from typing import Iterator

def json_escape_char(c: str) -> str:
    if c == '\\':
        return '\\\\'
    elif c == '"':
        return '\\"'
    elif c == '\n':
        return '\\n'
    elif c == '\r':
        return '\\r'
    elif c == '\t':
        return '\\t'
    else:
        return c

def stream_json_field(key: str, value: str, is_last: bool):
    print(f'\n  "{key}": "', end="", flush=True)
    for ch in value:
        print(json_escape_char(ch), end="", flush=True)
        time.sleep(0.01)
    print('"', end="", flush=True)
    if not is_last:
        print(',', end="", flush=True)
    else:
        print('', end="", flush=True)

def stream_json_response(
    user_input: str, title: str, intent: str, response_iterator: Iterator[str]
) -> str:
    print('{', end="", flush=True)

    stream_json_field("input", user_input, False)
    stream_json_field("title", title, False)
    stream_json_field("intent", intent, True)

    print(',\n  "result": {', end="", flush=True)
    print('\n    "response": "', end="", flush=True)
    full_response = ""
    for chunk in response_iterator:
        if chunk:
            for ch in chunk:
                print(json_escape_char(ch), end="", flush=True)
            full_response += chunk
    print('"\n  }', end="", flush=True)

    print('\n}', flush=True)
    return full_response

def stream_all_fields_response(
    input_iterator, title_iterator, intent_iterator, response_iterator
) -> tuple[str, str, str, str]:
    print('{', end="", flush=True)

    # input 스트리밍
    print('\n  "input": "', end="", flush=True)
    full_input = ""
    for chunk in input_iterator:
        if chunk:
            for ch in chunk:
                print(json_escape_char(ch), end="", flush=True)
                time.sleep(0.01)
            full_input += chunk
    print('"', end="", flush=True)

    # title 스트리밍  
    print(',\n  "title": "', end="", flush=True)
    full_title = ""
    for chunk in title_iterator:
        if chunk:
            for ch in chunk:
                print(json_escape_char(ch), end="", flush=True)
                time.sleep(0.01)
            full_title += chunk
    print('"', end="", flush=True)
    
    # intent 스트리밍
    print(',\n  "intent": "', end="", flush=True)
    full_intent = ""
    for chunk in intent_iterator:
        if chunk:
            for ch in chunk:
                print(json_escape_char(ch), end="", flush=True)
                time.sleep(0.01)
            full_intent += chunk
    print('"', end="", flush=True)

    # response 스트리밍
    print(',\n  "result": {', end="", flush=True)
    print('\n    "response": "', end="", flush=True)
    full_response = ""
    for chunk in response_iterator:
        if chunk:
            for ch in chunk:
                print(json_escape_char(ch), end="", flush=True)
                time.sleep(0.01)
            full_response += chunk
    print('"\n  }', end="", flush=True)

    print('\n}', flush=True)
    return full_input, full_title, full_intent, full_response
