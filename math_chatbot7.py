import streamlit as st
import google.generativeai as genai

# 🔑 여기에 Gemini API 키 붙여넣기
genai.configure(api_key="AIzaSyD_03LuomftfGRzZugDUy54kkFfBxxMDLs")

model = genai.GenerativeModel("models/gemini-1.5-pro")

st.title("수학 과외 챗봇 (Gemini 버전) 🎓")
st.write("학년/단원을 입력하면 진단평가 문제를 자동으로 생성해드릴게요.")

user_input = st.text_input("원하는 학습 범위 예: '중1-1 정수와 유리수'")

if st.button("문제 생성하기") and user_input:
    with st.spinner("문제 생성 중입니다..."):
        prompt = f"""
        너는 수학 선생님이야. '{user_input}' 단원에 대한 진단평가 문제 3개를 만들어줘.
        문제만 먼저 보여주고, 마지막에 정답을 한 줄씩 써줘.
        """
        response = model.generate_content(prompt)
        st.write(response.text)
