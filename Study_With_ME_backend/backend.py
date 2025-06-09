# backend.py
from get_questions import get_questions as original_get_questions
from parse_questions import parse_questions
from grading import grade_answers
from materials import get_materials

# 문제 여러 개 가져오기 (최대 5개)
def get_questions(grade, chapter):
    raw = original_get_questions(grade, chapter)
    print("\U0001F4E6 Ollama 응답:\n", raw)

    questions, choices, answers = parse_questions(raw)
    print("\U0001F4DA 추출된 문제 개수:", len(questions))

    if questions:
        return [
            {"text": q, "choices": c, "answer": a}
            for q, c, a in zip(questions, choices, answers)
        ]
    else:
        return []

def grade_answer(user_answer, correct_answer):
    return user_answer.strip().startswith(f"({correct_answer})")

def get_curriculum(grade, chapter):
    return ["기초 커리큘럼", "응용 커리큘럼", "심화 커리큘럼"]

def get_material(topic):
    return get_materials(topic)
