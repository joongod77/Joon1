import re

def parse_questions(text):
    questions = []
    current = None
    lines = text.strip().splitlines()

    for line in lines:
        line = line.strip()

        # 문제 시작: 다양한 패턴 대응 (문제1: 또는 문제 1: 등)
        if re.match(r"^문제\s*\d+\s*:", line):
            if current:
                questions.append(current)
            question_text = line.split(":", 1)[1].strip()
            current = {"question": question_text, "choices": []}

        # 선택지: (A) ~ (E) 형태 감지
        elif re.match(r"^\([A-Ea-e]\)", line) and current:
            current["choices"].append(line.strip())

        # 정답: 정답: A 또는 정답: (A) 형식 모두 대응
        elif line.startswith("정답:") and current:
            answer_raw = line.split("정답:", 1)[1].strip()
            if answer_raw.startswith("(") and len(answer_raw) >= 3:
                answer = answer_raw[1]  # (A) → A
            else:
                answer = answer_raw[0]  # A
            current["answer"] = answer.upper()

    if current:
        questions.append(current)

    # 유효한 문제만 필터링 (문제 + 보기 5개 + 정답)
    clean_questions = [
        q for q in questions
        if "question" in q and len(q["choices"]) == 5 and "answer" in q
    ]

    return (
        [q["question"] for q in clean_questions],
        [q["choices"] for q in clean_questions],
        [q["answer"] for q in clean_questions],
    )
