import zhipuai
import os
import streamlit as st

# 设置智谱AI的API密钥
zhipuai.api_key = st.secrets["zhipuai"]["api_key"]

#定义一个函数，用于调用智谱AI模型并处理前端传入的文本
def sse_invoke_example(prompt_text):
    # 确保API密钥已设置
    if not zhipu_api_key:
        raise ValueError("API密钥未设置。")

    # 创建一个ZhipuAI客户端实例
    client = ZhipuAI(api_key=zhipu_api_key)

    # 构建prompt结构体
    prompt_input = [
        {"role": "system", "content": "你是一个人工智能助手Wattter.AI"},
        {"role": "user", "content": prompt_text}
    ]

    try:
        # 调用chat.completions.create函数并传递参数
        response = client.chat.completions.create(
            model="glm-4",
            messages=prompt_input,
        )

        # 直接返回响应结果
        return response.choices[0].message.content

    except Exception as e:
        # 处理可能发生的异常
        return f"发生错误: {e}"
