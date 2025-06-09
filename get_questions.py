# get_questions.py
import requests
import os

# ✅ OpenAI API Key 설정
OPENAI_API_KEY = "여기에 키를 입력하세요"
MODEL_NAME = "gpt-3.5-turbo"

def get_questions(grade, chapter):
    prompt = f"""
    너는 {grade} 수학 선생님이야. '{chapter}' 단원에 대한 수학 객관식 문제 5개를 아래 형식처럼 만들어줘.
    - 난이도는 중간 수준
    - 형식은 객관식 5지선다형
    - 출력 예시:

    문제1: 다음 중 소수가 아닌 것은?
    (A) 2
    (B) 3
    (C) 4
    (D) 5
    (E) 7
    정답: C

    문제2: ...
    """

    try:
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {OPENAI_API_KEY}"
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": "너는 유능한 수학 선생님이야."},
                    {"role": "user", "content": prompt}
                ],
                "temperature": 0.7
            },
            timeout=60
        )

        result = response.json()
        response_text = result['choices'][0]['message']['content'].strip()

        if not response_text or "문제" not in response_text or "정답" not in response_text:
            print("⚠️ 문제 형식 이상 또는 응답 없음")
            return ""

        print("\n📦 생성된 문제:\n", response_text)
        return response_text

    except requests.exceptions.Timeout:
        print("⏰ OpenAI 응답 시간 초과")
        return ""

    except Exception as e:
        print(f"❌ 요청 실패: {e}")
        return ""
