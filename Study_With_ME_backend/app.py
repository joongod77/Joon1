import streamlit as st
from backend import get_questions, grade_answer, get_curriculum, get_material
import time

st.set_page_config(page_title="STUDY with ME", layout="centered")

# -------------------------------
# 상태 초기화
# -------------------------------
if "stage" not in st.session_state:
    st.session_state["stage"] = "start"
if "school_type" not in st.session_state:
    st.session_state["school_type"] = ""
if "selected_grade" not in st.session_state:
    st.session_state["selected_grade"] = ""
if "chapter" not in st.session_state:
    st.session_state["chapter"] = ""
if "questions" not in st.session_state:
    st.session_state["questions"] = []
if "question_index" not in st.session_state:
    st.session_state["question_index"] = 0
if "user_answers" not in st.session_state:
    st.session_state["user_answers"] = []
if "show_answers" not in st.session_state:
    st.session_state["show_answers"] = False

# -------------------------------
# 교육과정 데이터
# -------------------------------
school_to_chapters = {
    '초등학교': {'초1': [], '초2': [], '초3': [], '초4': [], '초5': [], '초6': []},
    '중학교': {
        '중1': ['도형과 측정', '변화와 관계', '수와연산', '자료와 가능성'],
        '중2': ['도형과 측정', '변화와 관계', '수와연산', '자료와 가능성'],
        '중3': ['변화와 관계', '수와 연산', '자료와 가능성']
    },
    '고등학교': {
        '고1': ['경우의 수', '다항식', '도형의 방정식', '방정식과 부등식 ', '집합과 명제', '함수와 그래프', '행렬'],
        '고2': ['경우의 수', '미분법', '삼각함수', '수열', '적분법', '지수함수와 로그함수', '통계', '함수의 극한과 연속', '확률'],
        '고3': ['공간도형과 공간좌표', '미분법의 심화', '벡터', '수열의 극한', '이차곡선', '적분법의 심화']
    }
}

mascots = {
    "초1": "https://cdn-icons-png.flaticon.com/512/4140/4140048.png",
    "초2": "https://cdn-icons-png.flaticon.com/512/4140/4140051.png",
    "초3": "https://cdn-icons-png.flaticon.com/512/4140/4140061.png",
    "초4": "https://cdn-icons-png.flaticon.com/512/4140/4140086.png",
    "초5": "https://cdn-icons-png.flaticon.com/512/4140/4140095.png",
    "초6": "https://cdn-icons-png.flaticon.com/512/4140/4140070.png",
    "중1": "https://cdn-icons-png.flaticon.com/512/4140/4140038.png",
    "중2": "https://cdn-icons-png.flaticon.com/512/4140/4140008.png",
    "중3": "https://cdn-icons-png.flaticon.com/512/4140/4140027.png",
    "고1": "https://cdn-icons-png.flaticon.com/512/4140/4140011.png",
    "고2": "https://cdn-icons-png.flaticon.com/512/4140/4140045.png",
    "고3": "https://cdn-icons-png.flaticon.com/512/4140/4140042.png"
}

page_bg = """
<style>
body {
    background-color: #FFF6F6;
    color: #333333;
}
.stButton > button {
    background-color: #FFB6C1;
    color: white;
    border-radius: 10px;
    font-size: 18px;
    padding: 10px 20px;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# -------------------------------
# 시작 화면
# -------------------------------
if st.session_state["stage"] == "start":
    st.image("https://cdn-icons-png.flaticon.com/512/888/888879.png", width=100)
    st.title("🌸스윗미 : STUDY with ME 🌸")
    st.markdown("#### 재미있고 귀엽고 효과적인 수학 공부!")

    if st.button("시작하기"):
        st.session_state["stage"] = "grade"
    st.stop()

# -------------------------------
# 학교급/학년 선택
# -------------------------------
elif st.session_state["stage"] == "grade":
    st.markdown("## 🐥 학교급과 학년을 선택하세요")
    school_type = st.selectbox("학교급을 선택하세요", ["초등학교", "중학교", "고등학교"])

    if school_type == "초등학교":
        grade_options = [f"초{i}" for i in range(1, 7)]
    elif school_type == "중학교":
        grade_options = [f"중{i}" for i in range(1, 4)]
    else:
        grade_options = [f"고{i}" for i in range(1, 4)]

    selected_grade = st.selectbox("학년을 선택하세요", grade_options)

    if st.button("학년 선택 완료"):
        st.session_state["school_type"] = school_type
        st.session_state["selected_grade"] = selected_grade
        st.session_state["stage"] = "chapter"
        st.rerun()

# -------------------------------
# 단원 선택
# -------------------------------
elif st.session_state["stage"] == "chapter":
    grade = st.session_state["selected_grade"]
    school_type = st.session_state["school_type"]

    st.markdown(f"### ✏️ 선택한 학년: **{grade}**")
    chapters = school_to_chapters[school_type].get(grade, [])
    selected_chapter = st.selectbox("단원을 선택하세요", chapters)

    if st.button("진단평가 시작"):
        st.session_state["chapter"] = selected_chapter
        st.session_state["stage"] = "loading"
        st.rerun()
        
# -------------------------------
# 로딩 화면 → 문제 생성 후 퀴즈로 이동
# -------------------------------
elif st.session_state["stage"] == "loading":
    st.image("https://cdn-icons-png.flaticon.com/512/6796/6796800.png", width=120)
    st.title("문제를 생성 중입니다...")
    st.markdown("귀여운 AI 선생님이 문제를 만들고 있어요! ✨")
    with st.spinner("⏳ 잠시만 기다려주세요..."):
        time.sleep(2.5)
        questions = get_questions(st.session_state["selected_grade"], st.session_state["chapter"])
        if not questions:
            st.error("❌ 문제를 불러올 수 없습니다. 다시 시도해 주세요.")
            st.stop()
        st.session_state["questions"] = questions[:5]  # 정확히 5개
        st.session_state["question_index"] = 0
        st.session_state["user_answers"] = []
        st.session_state["stage"] = "quiz"
        st.rerun()

# -------------------------------
# 문제 풀이 화면
# -------------------------------
elif st.session_state["stage"] == "quiz":
    idx = st.session_state["question_index"]
    questions = st.session_state["questions"]

    if idx >= len(questions):
        st.session_state["stage"] = "result"
        st.rerun()

    q = questions[idx]
    st.image("https://cdn-icons-png.flaticon.com/512/2942/2942931.png", width=80)
    st.markdown(f"### 문제 {idx+1}: <span style='color:#FF69B4'>{q['text']}</span>", unsafe_allow_html=True)
    user_answer = st.radio("정답을 선택하세요:", q["choices"], key=f"answer_{idx}")

    if st.button("다음 문제"):
        st.session_state["user_answers"].append(user_answer)
        st.session_state["question_index"] += 1
        st.rerun()

# -------------------------------
# 결과 및 정답 공개
# -------------------------------
elif st.session_state["stage"] == "result":
    st.header("🎯 진단 결과")

    if not st.session_state["show_answers"]:
        if st.button("정답 보기"):
            st.session_state["show_answers"] = True
            st.rerun()
    else:
        score = 0
        st.markdown("### 📋 정답 및 해설")
        for i, (user, q) in enumerate(zip(st.session_state["user_answers"], st.session_state["questions"])):
            correct = q["answer"]
            result = "✅ 정답" if grade_answer(user, correct) else f"❌ 오답 (정답: ({correct}))"
            if grade_answer(user, correct):
                score += 1
            st.markdown(f"**문제 {i+1}:** {q['text']}")
            st.markdown(f"내 답변: {user} → {result}")
            st.markdown("---")

        st.success(f"총 {score} / 5개 맞았습니다!")

        if score == 5:
            level = "A등급"
        elif score == 4:
            level = "B등급"
        else:
            level = "C등급"

        st.subheader(f"🏅 당신의 등급은: {level}")

        st.markdown("### 🤖 AI 추천 커리큘럼")
        st.write("AI가 분석한 결과, 당신에게 가장 잘 맞는 학습 자료는 다음과 같아요!")
        curriculum = get_curriculum(st.session_state["selected_grade"], st.session_state["chapter"])
        selected = st.selectbox("추천 커리큘럼을 선택하세요:", curriculum)
        material = get_material(selected)

        st.markdown("### 📘 학습 자료")
        st.markdown(material["text"])
        if material["pdf_path"]:
            st.markdown(f"[📎 PDF 다운로드]({material['pdf_path']})")
