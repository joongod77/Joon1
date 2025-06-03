
import streamlit as st
import openai

# 🔑 본인의 OpenAI API 키 입력
openai.api_key = "sk-여기에-당신의-API키-입력"

st.set_page_config(page_title="나랑 공부할래?", page_icon="📘")
st.title("📘 나랑 공부할래?")
st.write("학년과 단원을 입력하면 레벨테스트 문제를 만들어드릴게요!")

# 사용자 입력
grade = st.text_input("학년 (예: 중1, 중2, 고1)")
chapter = st.text_input("단원명 (예: 정수와 유리수, 함수)")

# 문제 및 정답 저장
questions = []
choices = []
answers = []

if grade and chapter and st.button("문제 생성하기"):
    with st.spinner("레벨테스트 문제를 생성 중입니다..."):
        prompt = f"""
        너는 수학 선생님이야. 학년은 {grade}, 단원은 {chapter}야.
        아래 조건에 따라 5문제짜리 객관식(5지선다형) 레벨테스트를 만들어줘.
        - 쉬운 문제 2문제
        - 응용 문제 2문제
        - 심화 문제 1문제
        각 문제는 다음 형식으로 출력해줘:
        문제1: [문제 내용]
        (A) 보기1
        (B) 보기2
        (C) 보기3
        (D) 보기4
        (E) 보기5
        정답: [정답 보기 문자 예: C]
        """

        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "넌 수학 선생님이야."},
                {"role": "user", "content": prompt}
            ]
        )
        output = response['choices'][0]['message']['content']
        st.session_state['test_content'] = output

# 문제 파싱
if 'test_content' in st.session_state:
    st.subheader("📄 레벨테스트 문제")

    lines = st.session_state['test_content'].splitlines()
    q_num = -1
    for line in lines:
        if line.startswith("문제"):
            q_num += 1
            questions.append(line)
            choices.append([])
        elif line.startswith("("):
            choices[q_num].append(line)
        elif line.startswith("정답:"):
            answers.append(line.split("정답:")[1].strip())

    user_answers = []
    for i in range(len(questions)):
        st.markdown(f"**{questions[i]}**")
        user_answers.append(st.radio(f"답 선택 (문제 {i+1})", choices[i], key=f"q{i}"))

    if st.button("채점하기"):
        st.subheader("📊 채점 결과")
        correct_count = 0
        for i in range(len(user_answers)):
            correct_option = [c for c in choices[i] if c.startswith(f"({answers[i]})")]
            st.markdown(f"**문제 {i+1}**")
            st.write(f"내 답: {user_answers[i]}")
            st.write(f"정답: {correct_option[0] if correct_option else answers[i]}")
            if user_answers[i].startswith(f"({answers[i]})"):
                st.success("정답입니다!")
                correct_count += 1
            else:
                st.error("오답입니다.")

        st.markdown(f"### ✅ 총 {correct_count}개 맞았습니다!")

        # 커리큘럼 추천
        st.subheader("📚 추천 커리큘럼")
        if correct_count <= 2:
            recommended = "기초 커리큘럼"
        elif correct_count <= 4:
            recommended = "응용 커리큘럼"
        else:
            recommended = "심화 커리큘럼"
        st.success(f"추천: {recommended}")
        st.session_state['curriculum'] = recommended

# 자료 제공
if 'curriculum' in st.session_state:
    st.subheader("📎 커리큘럼 자료 보기")
    selected = st.selectbox("커리큘럼을 선택하세요", ["기초 커리큘럼", "응용 커리큘럼", "심화 커리큘럼"])
    if st.button("자료 보기"):
        st.info(f"{selected}에 맞는 학습 자료를 준비했어요!")
        if selected == "기초 커리큘럼":
            st.markdown("- 수의 범위 복습
- 음수와 양수 비교 연습
- 기초 개념 정리 PDF 제공 예정")
        elif selected == "응용 커리큘럼":
            st.markdown("- 다단계 문제 풀이
- 문제 유형별 정리
- 응용 문제 PDF 제공 예정")
        else:
            st.markdown("- 고난도 문제 집중 학습
- 서술형 대비 자료
- 심화 문제집 PDF 제공 예정")
