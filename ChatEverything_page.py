
import streamlit as st
from zhipuai_module import sse_invoke_example
from content_processing import process_input
import time
import re
from collections import deque

def memory_prompt(process_prompt_text, history):
    """
    仅包含最近的5条历史记录。
    """
    if not isinstance(history, deque):
        history = deque(history, maxlen=5)

    history_str = "\n".join([f"{message['role']}: {message['content']}" for message in history])
    full_prompt = f"{history_str}\nUser: {process_prompt_text}"
    return full_prompt

def init_chat_interface():
    """
    初始化聊天界面。
    """
    with st.container():
        col1_1, col1_2 = st.columns([1, 15])
        with col1_1:
            image_path = "images/im2.jpg"  # 更改为您的图片路径
            st.image(image_path, width=70)
        with col1_2:
            st.title("ChatEverything")
    st.divider()

    if st.sidebar.button('清理聊天记录'):
        st.session_state.messages.clear()

def handle_user_input():
    """
    处理用户输入。
    """
    if prompt_text := st.chat_input("说点什么?"):
        user_avatar = "🤔"
        with st.chat_message("user", avatar=user_avatar):
            st.markdown(prompt_text)
        return prompt_text
    return None

def process_and_display_response(prompt_text):
    """
    处理并展示响应。
    """
    # 通过content_processing 模块处理内容
    process_input(prompt_text, uploaded_file = None, template_file = None , process_function = None) 
    process_prompt_text = st.session_state['combined_input']
    ai_avatar = "🤖"
    with st.chat_message("ai", avatar=ai_avatar):
        message_placeholder = st.empty()
        full_response = ""
        full_prompt = memory_prompt(process_prompt_text, st.session_state.messages)
        with st.spinner('处理中...'):
            # 历史文本整合后通过模型获取回复
            assistant_response = sse_invoke_example(full_prompt)   

            #模拟流式传输打字效果
            for chunk in assistant_response.split():  
                full_response += chunk + " "
                time.sleep(0.088)
                message_placeholder.markdown(full_response + "▌", unsafe_allow_html=True)

        # 在最终展示模型回复前添加短暂延迟作为过渡
        time.sleep(1)  # 这里的时间可以根据需要调整    

        #打字模拟完毕后，最后呈现模型返回的格式，避免流式打字的模版改变   
        message_placeholder.markdown(assistant_response, unsafe_allow_html=True)

    return assistant_response

def show_ChatEverything_page():
    """
    显示主页面。
    """
    if "messages" not in st.session_state:
        st.session_state.messages = deque(maxlen=5)

    init_chat_interface()

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.markdown((message["content"]), unsafe_allow_html=True)

    prompt_text = handle_user_input()
    if prompt_text:
        st.session_state.messages.append({"role": "user", "content": prompt_text, "avatar": "🤔"})
        full_response = process_and_display_response(prompt_text)
        st.session_state.messages.append({"role": "ai", "content": full_response, "avatar": "🤖"})

if __name__ == "__main__":
    show_ChatEverything_page()
