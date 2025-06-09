def grade_answers(user_answers, choices, answers):
    correct_count = 0
    feedback = []

    for i in range(len(user_answers)):
        user = user_answers[i]
        correct = answers[i]

        is_correct = user.startswith(f"({correct})")
        if is_correct:
            correct_count += 1
            comment = f"✅ 정답입니다! ({correct})"
        else:
            comment = f"❌ 오답입니다. 정답은 ({correct}) 입니다."

        feedback.append(comment)

    return correct_count, feedback


def recommend_curriculum(score):
    if score <= 2:
        return "기초 커리큘럼"
    elif score <= 4:
        return "응용 커리큘럼"
    else:
        return "심화 커리큘럼"
