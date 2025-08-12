import google.generativeai as genai
import os
import json

def get_gemini_model():
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    return genai.GenerativeModel("gemini-2.0-flash")

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

def stream_translation(user_input: str, intent: str, title_prompt: str, response_prompt: str) -> tuple[str, str]:
    model = get_gemini_model()
    full_title = ""
    full_response = ""

    print('{', flush=True)
    print(f'  "input": "{user_input}",', flush=True)
    print('  "title": "', end="", flush=True)

    try:
        title_response = model.generate_content(title_prompt, stream=True)
        for chunk in title_response:
            if chunk.text:
                for ch in chunk.text:
                    print(json_escape_char(ch), end="", flush=True)
                full_title += chunk.text
    except Exception as e:
        err_msg = "제목 생성 오류"
        for ch in err_msg:
            print(json_escape_char(ch), end="", flush=True)
        full_title = err_msg

    print('",', flush=True)
    print(f'  "intent": "{intent}",', flush=True)
    print('  "result": {', flush=True)
    
    escaped_input = ""
    for ch in user_input:
        escaped_input += json_escape_char(ch)
    print(f'    "original": "{escaped_input}",', flush=True)
    
    print('    "translation": "', end="", flush=True)

    try:
        response = model.generate_content(response_prompt, stream=True)
        for chunk in response:
            if chunk.text:
                for ch in chunk.text:
                    print(json_escape_char(ch), end="", flush=True)
                full_response += chunk.text
    except Exception as e:
        err_msg = f"오류 발생: {e}"
        for ch in err_msg:
            print(json_escape_char(ch), end="", flush=True)
        full_response = err_msg

    print('"', flush=True)
    print('  }', flush=True)
    print('}', flush=True)

    return full_title.strip(), full_response

def stream(user_input: str, intent: str, title_prompt: str, response_prompt: str) -> tuple[str, str]:
    model = get_gemini_model()
    full_title = ""
    full_response = ""

    print('{', flush=True)
    print(f'  "input": "{user_input}",', flush=True)
    print('  "title": "', end="", flush=True)

    try:
        title_response = model.generate_content(title_prompt, stream=True)
        for chunk in title_response:
            if chunk.text:
                for ch in chunk.text:
                    print(json_escape_char(ch), end="", flush=True)
                full_title += chunk.text
    except Exception as e:
        err_msg = "제목 생성 오류"
        for ch in err_msg:
            print(json_escape_char(ch), end="", flush=True)
        full_title = err_msg

    print('",', flush=True)
    print(f'  "intent": "{intent}",', flush=True)
    print('  "result": {', flush=True)
    print('    "response": "', end="", flush=True)

    try:
        response = model.generate_content(response_prompt, stream=True)
        for chunk in response:
            if chunk.text:
                for ch in chunk.text:
                    print(json_escape_char(ch), end="", flush=True)
                full_response += chunk.text
    except Exception as e:
        err_msg = f"오류 발생: {e}"
        for ch in err_msg:
            print(json_escape_char(ch), end="", flush=True)
        full_response = err_msg

    print('"', flush=True)
    print('  }', flush=True)
    print('}', flush=True)

    return full_title.strip(), full_response

def stream_gemini_response(user_input: str, title: str, intent: str, prompt: str) -> str:
    model = get_gemini_model()
    full_response = ""

    print('{', flush=True)
    print(f'  "input": "{user_input}",', flush=True)
    print(f'  "title": "{title}",', flush=True)
    print(f'  "intent": "{intent}",', flush=True)
    print('  "result": {', flush=True)
    print('    "response": "', end="", flush=True)

    try:
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:
                for ch in chunk.text:
                    print(json_escape_char(ch), end="", flush=True)
                full_response += chunk.text
    except Exception as e:
        err_msg = f"오류 발생: {e}"
        for ch in err_msg:
            print(json_escape_char(ch), end="", flush=True)
        full_response = err_msg

    print('"', flush=True)
    print('  }', flush=True)
    print('}', flush=True)

    return full_response