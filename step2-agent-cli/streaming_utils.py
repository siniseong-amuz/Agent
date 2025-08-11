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
    stream_json_field("intent", intent, False)

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
