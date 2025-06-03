import openai
import streamlit as st

st.title("수학 과외 챗봇")

# 비밀 키 불러오기
api_key = st.secrets["OPENAI_API_KEY"]

# client에 키 명시적으로 전달
client = openai.OpenAI(api_key=api_key)

user_input = st.text_input("원하는 학습 범위를 입력하세요")

if user_input:
    with st.spinner("문제 생성 중입니다..."):
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 또는 gpt-4 (유료일 경우)
            messages=[
                {"role": "user", "content": f"{user_input} 단원에 맞는 수학 문제 3개 만들어줘"}
            ]
        )
        st.write(response.choices[0].message.content)
