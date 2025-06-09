def get_materials(curriculum):
    if curriculum == "기초 커리큘럼":
        return {
            "text": "- 수의 범위 복습\n- 음수와 양수 비교 연습\n- 기초 개념 정리",
            "pdf_path": "static/basic_curriculum.pdf"
        }
    elif curriculum == "응용 커리큘럼":
        return {
            "text": "- 다단계 문제 풀이\n- 문제 유형별 정리\n- 응용 문제 연습",
            "pdf_path": "static/intermediate_curriculum.pdf"
        }
    elif curriculum == "심화 커리큘럼":
        return {
            "text": "- 고난도 문제 집중 학습\n- 서술형 문제 대비\n- 심화 문제집",
            "pdf_path": "static/advanced_curriculum.pdf"
        }
    else:
        return {
            "text": "해당 커리큘럼에 대한 자료가 없습니다.",
            "pdf_path": None
        }
