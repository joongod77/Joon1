import requests

def get_questions(grade, chapter):
    prompt = f"""
{grade}의 "{chapter}" 단원에 대한 수학 객관식 문제 5개를 만들어줘.
- 난이도: 쉬움 2개, 보통 2개, 어려움 1개
- 문제 형식: 객관식 5지선다형
- 출력 예시:
문제1: 다음 중 소수가 아닌 것은?
(A) 2
(B) 3
(C) 4
(D) 5
(E) 7
정답: C
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "mistral",  # 또는 mistral:instruct
            "prompt": prompt,
            "stream": False
        }
    )

    result = response.json()
    
    # 응답 확인용 디버깅 출력
    print("======== 응답 내용 ========")
    print(result.get("response", "[응답 없음]"))
    print("===========================")

    return result.get("response", "[응답 없음]")

# 실행 테스트
if __name__ == "__main__":
    print("Ollama(Mistral)에게 문제 요청 중...")
    output = get_questions("중1", "정수와 유리수")
    print("응답 도착! 결과:")
    print(output)
