def parse_questions(text):
    questions = []
    current = None
    lines = text.strip().splitlines()

    for line in lines:
        line = line.strip()

        if line.startswith("문제"):
            if current:
                questions.append(current)
            current = {"question": line.split(":", 1)[1].strip(), "choices": []}

        elif line.startswith("(") and current:
            current["choices"].append(line)

        elif line.startswith("정답:") and current:
            current["answer"] = line.split("정답:")[1].strip()

    if current:
        questions.append(current)

    # 필터링: 필수 키가 빠진 문제는 제외
    clean_questions = [
        q for q in questions
        if "question" in q and "choices" in q and "answer" in q
    ]

    return (
        [q["question"] for q in clean_questions],
        [q["choices"] for q in clean_questions],
        [q["answer"] for q in clean_questions],
    )
