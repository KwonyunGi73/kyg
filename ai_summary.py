# 파일 이름: ai_summary.py

import os
import json
import google.generativeai as genai

try:
    # 깃허브 액션 환경에서 API 키와 이벤트 정보를 가져옵니다.
    api_key = os.environ.get("GEMINI_API_KEY")
    event_path = os.environ.get("GITHUB_EVENT_PATH")

    # PR 정보 읽기
    with open(event_path, 'r', encoding='utf-8') as f:
        event_data = json.load(f)

    # PR의 제목과 본문 내용 추출
    pr_title = event_data['pull_request']['title']
    pr_body = event_data['pull_request']['body']

    # Gemini API 설정
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro-latest')

    # AI에게 내릴 명령 (프롬프트)
    prompt = f"""
    아래 Pull Request(PR) 정보를 바탕으로, README 파일에 추가할 "최근 변경 사항"을 한두 문장으로 요약해줘.
    비개발자도 이해하기 쉬운 친근한 어투로 작성해줘.

    - PR 제목: {pr_title}
    - PR 내용: {pr_body}
    """
    
    # Gemini API 호출
    response = model.generate_content(prompt)
    
    # 생성된 요약문을 출력 (이 출력을 깃허브 액션이 받아서 사용함)
    print(response.text)

except Exception as e:
    print(f"AI 요약 생성 중 오류 발생: {e}")
    #test12321