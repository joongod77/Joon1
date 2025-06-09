# get_questions.py
import requests

def get_questions(grade, chapter):
    prompt = f"""
너는 수학 선생님이야. 아래 형식을 정확히 지켜서 한국어로 된 {grade} 수준의 수학 객관식 문제 **5개**를 생성해줘.

- 난이도: 중간 수준
- 형식: 5지선다형
- 반드시 아래와 같은 형식과 흐름으로 출력해줘.

문제1: 다음 중 소수가 아닌 것은?
(A) 2
(B) 3
(C) 4
(D) 5
(E) 7
정답: C

문제2: ...
...

이제 문제를 만들어줘:
{grade}의 "{chapter}" 단원에 해당하는 문제 5개
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "instruct",
                "prompt": prompt,
                "stream": False
            },
            timeout=300
        )

        result = response.json()
        response_text = result.get("response", "").strip()

        if not response_text or "문제" not in response_text or "정답:" not in response_text:
            print("❗ 문제 포맷 이상 또는 비어 있음")
            return ""

        print("\n📦 최종 문제 출력:\n", response_text)
        return response_text

    except requests.exceptions.Timeout:
        print("⏱ Ollama 응답 시간 초과!")
        return ""

    except Exception as e:
        print(f"❌ 요청 실패: {e}")
        return ""
