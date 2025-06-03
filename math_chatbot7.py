import openai
import streamlit as st

openai.api_key = "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"  # 여기에 키 입력

st.title("수학 과외 챗봇")

user_input = st.text_input("원하는 학습 범위를 입력하세요")

if user_input:
    with st.spinner("문제 생성 중입니다..."):
        client = openai.OpenAI()  # 최신 버전에서는 client 객체 생성 필요

        response = client.chat.completions.create(
            model="gpt-3.5-turbo",  # 또는 "gpt-3.5-turbo"
            messages=[
                {"role": "user", "content": f"{user_input} 단원에 맞는 수학 문제 3개 만들어줘"},
            ]
        )

        st.write(response.choices[0].message.content)
