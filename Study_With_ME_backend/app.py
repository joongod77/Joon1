import streamlit as st
from get_questions import get_questions
from parse_questions import parse_questions
from grading import grade_answers
from materials import get_materials

st.set_page_config(page_title="스윗미:Study With ME?", page_icon="📘")
st.title("📘 스윗미:Study With ME?")
st.write("학년과 단원을 입력하면 레벨테스트 문제를 만들어드릴게요!")

# 사용자 입력
grade = st.text_input("학년 (예: 중1, 중2, 고1)")
chapter = st.text_input("단원명 (예: 정수와 유리수, 함수)")

# 문제 및 정답 저장
questions = []
choices = []
answers = []

# 문제 생성
if grade and chapter and st.button("문제 생성하기"):
    with st.spinner("레벨테스트 문제를 생성 중입니다..."):
        raw_text = get_questions(grade, chapter)
        questions, choices, answers = parse_questions(raw_text)
        st.session_state["questions"] = questions
        st.session_state["choices"] = choices
        st.session_state["answers"] = answers

# 문제 표시
if "questions" in st.session_state:
    st.subheader("📄 레벨테스트 문제")
    user_answers = []
    for i in range(len(st.session_state["questions"])):
        st.markdown(f"**{st.session_state['questions'][i]}**")
        user_input = st.radio(f"답 선택 (문제 {i+1})", st.session_state["choices"][i], key=f"q{i}")
        user_answers.append(user_input)

    if st.button("채점하기"):
        correct_count, feedback = grade_answers(user_answers, st.session_state["choices"], st.session_state["answers"])
        st.subheader("📊 채점 결과")
        for i, comment in enumerate(feedback):
            st.markdown(f"**문제 {i+1}**")
            st.write(comment)

        st.success(f"총 {correct_count}개 맞았습니다!")

        if correct_count <= 2:
            curriculum = "기초 커리큘럼"
        elif correct_count <= 4:
            curriculum = "응용 커리큘럼"
        else:
            curriculum = "심화 커리큘럼"

        st.session_state["curriculum"] = curriculum
        st.success(f"추천 커리큘럼: {curriculum}")

# 커리큘럼 자료 보기
if "curriculum" in st.session_state:
    st.subheader("📎 커리큘럼 자료 보기")
    selected = st.selectbox("커리큘럼을 선택하세요", ["기초 커리큘럼", "응용 커리큘럼", "심화 커리큘럼"])
    if st.button("자료 보기"):
        material_text = get_materials(selected)
        st.markdown(material_text)

