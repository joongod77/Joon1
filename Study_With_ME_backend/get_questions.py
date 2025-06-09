import requests

def get_questions(grade, chapter):
    prompt = f"""
당신은 {grade} 학생을 위한 수학 선생님입니다.
아래 조건을 충실히 지켜서 "{chapter}" 단원에 대한 수학 객관식 문제 5개를 반드시 생성해주세요.

- 문제 수: 5문제 (쉬운 문제 2개, 중간 수준 2개, 어려운 문제 1개)
- 형식: 5지선다형 객관식
- 각 문제는 반드시 아래와 같은 형식을 따르세요.
- 선택지는 (A), (B), (C), (D), (E)로 반드시 표기하세요.
- 출력은 반드시 문제1 ~ 문제5 까지 순서대로 포함되어야 하며, 각 문제에는 반드시 정답이 포함되어야 합니다.

출력 예시:
문제1: 다음 중 소수가 아닌 것은?
(A) 2
(B) 3
(C) 4
(D) 5
(E) 7
정답: C

이제 문제를 생성해 주세요.
"""

    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi3:instruct",
                "prompt": prompt,
                "stream": False
            },
            timeout=90
        )

        print("📤 전송된 프롬프트:\n", prompt)
        result = response.json()

        response_text = result.get("response", "").strip()
        print("📥 Ollama 응답:\n", response_text)

        if not response_text:
            print("⚠️ 응답이 비어 있습니다.")
            return ""

        # 문제와 정답이 모두 포함되어 있는지 확인
        if "문제" not in response_text or "정답:" not in response_text:
            print("⚠️ '문제' 또는 '정답:' 형식이 누락되었습니다.")
            return ""

        return response_text

    except requests.exceptions.Timeout:
        print("⏱ 타임아웃: Ollama에서 응답이 없습니다.")
        return ""

    except Exception as e:
        print(f"❌ 예외 발생: {e}")
        return ""

# 테스트 실행
if __name__ == "__main__":
    print("🧪 테스트 실행 중...")
    output = get_questions("중1", "정수와 유리수")
    print("✅ 최종 결과:\n", output)
