import streamlit as st
from backend import get_questions, grade_answer, get_curriculum, get_material
import time
import os

st.set_page_config(page_title="스윗미 : STUDY with ME", layout="centered")

# 상태 초기화
if "stage" not in st.session_state:
    st.session_state["stage"] = "start"
if "selected_school" not in st.session_state:
    st.session_state["selected_school"] = ""
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

base_path = os.path.dirname(os.path.abspath(__file__))

school_images = {
    "초등학교": os.path.join(base_path, "images", "mascot.png"),
    "중학교": os.path.join(base_path, "images", "mascot_mid_1.png"),
    "고등학교": os.path.join(base_path, "images", "mascot_high_1.png"),
}

mascots = {
    "초1": os.path.join(base_path, "images", "mascot.png"),
    "초2": os.path.join(base_path, "images", "mascot.png"),
    "초3": os.path.join(base_path, "images", "mascot.png"),
    "초4": os.path.join(base_path, "images", "mascot.png"),
    "초5": os.path.join(base_path, "images", "mascot.png"),
    "초6": os.path.join(base_path, "images", "mascot.png"),
    "중1": os.path.join(base_path, "images", "mascot_mid_1.png"),
    "중2": os.path.join(base_path, "images", "mascot_mid_2.png"),
    "중3": os.path.join(base_path, "images", "mascot_mid_3.png"),
    "고1": os.path.join(base_path, "images", "mascot_high_1.png"),
    "고2": os.path.join(base_path, "images", "mascot_high_2.png"),
    "고3": os.path.join(base_path, "images", "mascot_high_3.png"),
}

main_mascot_path = os.path.join(base_path, "images", "mascot.png")
loading_video_path = os.path.join(base_path, "images", "mascot_run.gif")

st.markdown("""
<style>
body {
    background-color: #FFF8F8;
}
h1, h2, h3, h4 {
    color: #FF69B4;
    font-family: 'Comic Sans MS', cursive;
}
.stButton > button {
    background-color: #FFB6C1;
    color: white;
    border-radius: 10px;
    font-size: 18px;
    padding: 8px 20px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

if st.session_state["stage"] == "start":
    st.image(main_mascot_path, width=180)
    st.title(" 스윗미 : STUDY with ME")
    st.markdown("#### 수학 실력을 진단해보고 나에게 맞는 커리큘럼을 추천받아보세요!")
    if st.button("시작하기"):
        st.session_state["stage"] = "school"
    st.stop()

if st.session_state["stage"] == "school":
    st.markdown("## 학교를 선택해주세요")
    for school in ["초등학교", "중학교", "고등학교"]:
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image(school_images[school], width=60)
        with col2:
            if st.button(f"{school} 선택"):
                st.session_state["selected_school"] = school
                st.session_state["stage"] = "grade"
                st.rerun()

elif st.session_state["stage"] == "grade":
    st.markdown("## 학년을 선택해주세요")
    grade_options = {
        "초등학교": ["초1", "초2", "초3", "초4", "초5", "초6"],
        "중학교": ["중1", "중2", "중3"],
        "고등학교": ["고1", "고2", "고3"]
    }
    for grade in grade_options.get(st.session_state["selected_school"], []):
        col1, col2 = st.columns([1, 5])
        with col1:
            st.image(mascots.get(grade, main_mascot_path), width=60)
        with col2:
            if st.button(f"{grade} 선택하기"):
                st.session_state["selected_grade"] = grade
                st.session_state["stage"] = "chapter"
                st.rerun()

elif st.session_state["stage"] == "chapter":
    st.markdown(f"### ✏️ 선택한 학년: **{st.session_state['selected_grade']}**")
    st.markdown("""
    <div style='background-color:#FFF0F5; padding:20px; border-radius:10px;'>
        <h4 style='color:#FF69B4;'>배우고 싶은 수학 단원을 입력해 주세요 ✨</h4>
    </div>
    """, unsafe_allow_html=True)
    chapter = st.text_input("단원 입력 (예: 함수, 도형의 성질 등)", value=st.session_state["chapter"])

    if st.button("진단평가 시작"):
        st.session_state["chapter"] = chapter
        st.session_state["stage"] = "loading"
        st.rerun()

elif st.session_state["stage"] == "loading":
    st.image(loading_video_path, use_container_width=True)
    st.markdown("<p style='text-align:center; color: gray; font-size: 14px;'>문제를 가져오는 중...</p>", unsafe_allow_html=True)

    time.sleep(2.5)  # ⏳ 약간 기다렸다가
    questions = get_questions(st.session_state["selected_grade"], st.session_state["chapter"])
    if not questions:
        st.error("❌ 문제를 불러오는 데 실패했습니다. 다시 시도해 주세요.")
        st.stop()  # ❗여기서는 사용 가능
    st.session_state["questions"] = questions[:5]
    st.session_state["question_index"] = 0
    st.session_state["user_answers"] = []
    st.session_state["stage"] = "quiz"
    st.rerun()


elif st.session_state["stage"] == "quiz":
    questions = st.session_state["questions"]
    index = st.session_state["question_index"]
    current = questions[index]

    st.markdown(f"### 문제 {index+1}")
    st.write(current["text"])
    user_answer = st.radio("보기", current["choices"], key=index)

    if st.button("다음 문제"):
        st.session_state["user_answers"].append(user_answer)
        if index + 1 < len(questions):
            st.session_state["question_index"] += 1
            st.rerun()
        else:
            st.session_state["stage"] = "result"
            st.rerun()

elif st.session_state["stage"] == "result":
    score = 0
    for i, ans in enumerate(st.session_state["user_answers"]):
        correct = st.session_state["questions"][i]["answer"]
        if grade_answer(ans, correct):
            score += 1

    st.markdown("## 🎓 진단 결과")
    st.write(f"총 {score} / 5 문제 맞았습니다!")

    if score == 5:
        level = "A"
    elif score == 4:
        level = "B"
    elif score == 3:
        level = "C"
    elif score == 2:
        level = "D"
    else:
        level = "E"

    st.success(f"당신의 등급은 {level}입니다!")

    curriculum = get_curriculum(st.session_state["selected_grade"], st.session_state["chapter"])
    selected = st.selectbox("추천 커리큘럼을 선택하세요:", curriculum)
    material = get_material(selected)

    st.markdown("### 📘 학습 자료")
    st.markdown(material["text"])
    if material["pdf_path"]:
        st.markdown(f"[📌 PDF 다운로드]({material['pdf_path']})")
