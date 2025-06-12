# 파일 이름: ai_summary.py

import os
import json
import google.generativeai as genai

try:
    # 깃허브 액션 환경 변수에서 API 키와 PR 이벤트 정보 파일 경로를 가져옵니다.
    api_key = os.environ.get("GEMINI_API_KEY")
    event_path = os.environ.get("GITHUB_EVENT_PATH")

    # 필수 정보가 없는 경우 오류를 발생시켜 로그에서 확인할 수 있도록 합니다.
    if not api_key:
        raise ValueError("GEMINI_API_KEY secret이 설정되지 않았습니다.")
    if not event_path:
        raise ValueError("GITHUB_EVENT_PATH 환경 변수를 찾을 수 없습니다.")

    # PR 정보가 담긴 JSON 파일을 엽니다.
    with open(event_path, 'r', encoding='utf-8') as f:
        event_data = json.load(f)

    # PR의 제목과 본문 내용(설명)을 추출합니다.
    pr_title = event_data.get('pull_request', {}).get('title', '제목 없음')
    pr_body = event_data.get('pull_request', {}).get('body', '내용 없음')

    # Gemini API 설정을 합니다.
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    # AI에게 내릴 명령(프롬프트)을 구체적으로 작성합니다.
    prompt = f"""
    아래 Pull Request(PR) 정보를 바탕으로, README 파일에 추가할 "최근 변경 사항"을 작성해줘.
    - 주요 변경점을 글머리 기호(-)를 사용하여 한두 문장으로 간결하고 명확하게 요약해줘.
    - 비개발자도 이해하기 쉬운 친근한 어투로 작성해줘.

    ---
    PR 제목: {pr_title}
    PR 내용: {pr_body}
    ---
    """
    
    # Gemini API를 호출하여 요약문을 생성합니다.
    response = model.generate_content(prompt)
    
    # 생성된 요약문을 출력합니다. (이 출력을 깃허브 액션이 받아서 사용합니다)
    print(response.text)

except Exception as e:
    # 만약 이 스크립트 실행 중 오류가 발생하면, 오류 메시지를 출력합니다.
    # 이 메시지는 깃허브 액션 로그에 남아서 디버깅에 도움이 됩니다.d3sdd
    print(f"AI 요약 생성 중 오류 발생: {e}")