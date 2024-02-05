import streamlit as st
import time
import re
from zhipuai_module import parse_function_call, glm_invoke
from collections import deque
from content_processing import process_input  # 导入内容处理模块

def memory_prompt(process_prompt_text, history):
    """
    结合用户的最新输入和聊天历史，但只包含最近的5条历史记录。
    """
    if not isinstance(history, deque):
        history = deque(history, maxlen=5)  # 确保历史记录为deque类型，最大长度为5

    # 将历史记录转换为字符串格式
    history_str = "\n".join([f"{message['role']}: {message['content']}" for message in history])
    full_prompt = f"{history_str}\nUser: {process_prompt_text}"  # 将用户最新输入添加到历史记录字符串
    return full_prompt

def init_chat_interface():
    """
    初始化聊天界面布局。
    """
    with st.container():
        col1_1, col1_2 = st.columns([1, 15])
        with col1_1:
            image_path = "images/im2.jpg"  # 设定图片路径
            st.image(image_path, width=70)  # 显示图片
        with col1_2:
            st.title("ChatEverything")  # 显示标题
    st.divider()  # 添加分割线

    with st.sidebar:

        st.divider()  # 添加分割线
        # 添加侧边栏按钮以清理聊天记录
        if st.sidebar.button('清理聊天记录'):
            st.session_state.messages.clear()  # 清理聊天记录
        st.divider()
        # 这里可以添加其他介绍性文字或说明
        st.write(
            """
        小提示：

        1、输入任意内容开始探索；

        2、链接直接输入对话框可以获取内容；

        3、支持多轮对话。

        """
        )

def memory_prompt(prompt_text, history):
    """
    结合用户的最新输入和聊天历史，但只包含最近的5条历史记录。
    """
    if not isinstance(history, deque):
        history = deque(history, maxlen=5)

    history_str = "\n".join([f"{message['role']}: {message['content']}" for message in history])
    full_prompt = f"{history_str}\nUser: {prompt_text}"
    return full_prompt

def handle_user_input():
    """
    获取并显示用户输入。
    """
    prompt_text = st.chat_input("说点什么?")
    if prompt_text:
        user_avatar = "🤔"
        with st.chat_message("user", avatar=user_avatar):
            st.markdown(prompt_text)
        return prompt_text
    return None

def model_response(prompt_text):
    """
    根据用户输入获取模型的响应。
    """

    # 处理用户输入内容
    process_input(prompt_text, uploaded_file=None, template_file=None, process_function=None) #因为共用内容处理模块，这里只传递部分的变量
    process_prompt_text = st.session_state['combined_input']

    user_input = memory_prompt(process_prompt_text, st.session_state.messages)
    if user_input:
        messages = [
            {"role": "system", "content": "不要假设或猜测传入函数的参数值。如果用户的描述不明确，请要求用户提供必要信息"},
            {"role": "user", "content": user_input}
        ]
        response = glm_invoke(messages)
        messages.append(response.choices[0].message.model_dump())
        
        ai_response = parse_function_call(response, messages)

        return ai_response

def show_ChatEverything_page():
    """
    显示整个聊天页面。
    """
    if "messages" not in st.session_state:
        st.session_state.messages = deque(maxlen=5)

    init_chat_interface()

    # 显示历史聊天记录，让历史消息保持显示
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # 处理新的用户输入
    prompt_text = handle_user_input()
    if prompt_text:
        st.session_state.messages.append({"role": "user", "content": prompt_text, "avatar": "🤔"})
        
        ai_response = model_response(prompt_text)
        if ai_response:
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(ai_response, unsafe_allow_html=True)
            st.session_state.messages.append({"role": "assistant", "content": ai_response, "avatar": "🤖"})

if __name__ == "__main__":
    show_ChatEverything_page()
