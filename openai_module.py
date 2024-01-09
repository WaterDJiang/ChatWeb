import openai
import os
import streamlit as st
# 填写你的秘钥
os.environ["openai.api_key"] = st.secrets["openai"]["openai.api_key"]

# 提问代码
def generate_with_openai_stream(prompt):
    # 你的问题
    user_msg = prompt  # 重命名 prompt 为 user_msg，以匹配原始代码

    # 构建消息列表，与原始代码中的 compose_msg 函数相似
    messages = [
        {"role": "user", "content": user_msg}
    ]

    # 调用 ChatGPT 接口，与原始代码中的 process_query 函数相似
    model_engine = "gpt-3.5-turbo-16k"
    # model = "gpt-4-1106-preview", "gpt-4-32k-0613"，"gpt-3.5-turbo-16k"
    response = openai.ChatCompletion.create(
        model=model_engine,
        messages=messages
    )

    chatbot_response = response.choices[0].message['content']
    return chatbot_response.strip()
