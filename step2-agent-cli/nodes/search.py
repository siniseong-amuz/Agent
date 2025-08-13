import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from langchain_core.runnables import RunnableLambda
from langchain.tools import tool
from langchain_core.tools import Tool
from typing import Dict
from streaming_utils import stream



@tool
def web(url: str) -> str:
    """페이지 내용 추출"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.content, 'html.parser')
        
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()
        
        title = soup.find('title')
        title_text = title.get_text().strip() if title else ""
        
        content_selectors = [
            'article', 'main', '.content', '#content', 
            '.post-content', '.entry-content', '.article-content'
        ]
        
        main_content = ""
        for selector in content_selectors:
            content_elem = soup.select_one(selector)
            if content_elem:
                main_content = content_elem.get_text()
                break
        
        if not main_content:
            main_content = soup.get_text()
        
        main_content = re.sub(r'\s+', ' ', main_content).strip()
        main_content = main_content[:3000]
        
        return f"제목: {title_text}\n\n내용: {main_content}"
        
    except Exception as e:
        return f"URL 내용을 가져오는 중 오류가 발생했습니다: {str(e)}"

search_tools = [web]

def get_search_node(llm=None) -> RunnableLambda:
    def _search(state: Dict) -> Dict:
        user_input = state["input"]
        history_context = state.get("history", "")
        
        title_prompt_text = f"다음을 3~5단어로 간단히 제목만 출력: {user_input}"
        
        url_pattern = re.compile(
            r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
        )
        urls = url_pattern.findall(user_input)
        
        if urls:
            url = urls[0]
            content = web.invoke({"url": url})
            search_prompt_text = f"{content}\n\n{user_input}"
        else:
            search_prompt_text = user_input

        title, full_response = stream(
            user_input=user_input,
            intent="검색/링크분석",
            title_prompt=title_prompt_text,
            response_prompt=search_prompt_text
        )

        return {
            "input": user_input,
            "title": title or "검색 결과",
            "intent": "검색/링크분석", 
            "result": {"response": full_response}
        }

    return RunnableLambda(_search)