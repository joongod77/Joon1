import streamlit as st
import openai

api_key = st.secrets["OPENAI_API_KEY"]  # 🔥 여기에 오타 나면 KeyError
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
