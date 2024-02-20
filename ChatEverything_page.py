import streamlit as st
import time
import re
from zhipuai_module import parse_function_call, glm_invoke
from collections import deque
from content_processing import process_input  # 导入内容处理模块

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
        """显示边栏"""
        if 'show_file_uploader' not in st.session_state:
            st.session_state['show_file_uploader'] = False
        if 'show_template_uploader' not in st.session_state:
            st.session_state['show_template_uploader'] = False

        st.divider()

        # 上传按钮
        col1, col2 = st.columns([1, 1], gap="medium")

        with col1:
            if st.button("➕ 上传资料", key="btn_upload_file2"):
                st.session_state['show_file_uploader'] = not st.session_state['show_file_uploader']

        if st.session_state['show_file_uploader']:
            st.session_state['uploaded_file'] = st.file_uploader("选择需要上传的文件", type=["pdf", "docx", "txt", "xlsx", "xls", "pptx", "ppt", "csv"], key='file_uploader3')

        with col2:
            if st.button("➕ 回复模版", key="btn_template_file2"):
                st.session_state['show_template_uploader'] = not st.session_state['show_template_uploader']

        if st.session_state['show_template_uploader']:
            st.session_state['template_file'] = st.file_uploader("选择需要上传的模版", type=["pdf", "docx", "txt", "xlsx", "xls", "pptx", "ppt", "csv"], key='file_uploader4')

        st.divider()  # 添加分割线
       
        # 添加侧边栏按钮以清理聊天记录
        if st.sidebar.button('清理聊天记录'):
            st.session_state.messages.clear()  # 清理聊天记录
        st.divider()
        # 这里可以添加其他介绍性文字或说明
        st.info(
            """
         **小提示**:

        - **探索聊天**: 

            输入任意内容开始与AI的互动。
        - **上传文件**: 

            点击“➕ 上传资料”以上传文件。AI可以帮助进行文本处理和分析。
        - **使用模版**: 

            通过“➕ 回复模版”，上传你的模版文件，AI将根据模版内容进行智能回复，例如生成分析报告。
        - **多功能支持**: 

            除了基本对话，本系统支持画图、网址内容获取和多轮对话，为你提供更丰富的互动体验。
        """
        )

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


def model_response(prompt_text, recent_messages):
    """
    根据用户输入获取模型的响应。
    """
    with st.spinner('Wattter烧脑中...'):
        # 获取会话状态中的文件
        uploaded_file = st.session_state.get('uploaded_file')
        template_file = st.session_state.get('template_file')

        # 处理用户输入内容
        process_input(prompt_text, uploaded_file, template_file, process_function=None)  # 因为共用模块，本流出不需要的变量，用 None 表示
        process_prompt_text = st.session_state['combined_input']

        user_input = memory_prompt(process_prompt_text, recent_messages)  # 使用最近的消息列表
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
    # 确保session_state中有messages和recent_messages两个列表
    if "messages" not in st.session_state:
        st.session_state.messages = []  # 保存所有历史记录
    if "recent_messages" not in st.session_state:
        st.session_state.recent_messages = deque(maxlen=5)  # 仅保存用于模型输入的最近5条记录

    init_chat_interface()

    # 显示所有历史聊天记录
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.markdown(message["content"], unsafe_allow_html=True)

    # 处理新的用户输入
    prompt_text = handle_user_input()
    if prompt_text:
        user_message = {"role": "user", "content": prompt_text, "avatar": "🤔"}
        st.session_state.messages.append(user_message)  # 添加到所有历史记录
        st.session_state.recent_messages.append(user_message)  # 添加到最近的5条记录

        # 注意这里将recent_messages传递给model_response，而不是messages
        ai_response = model_response(prompt_text, st.session_state.recent_messages)
        if ai_response:
            ai_message = {"role": "assistant", "content": ai_response, "avatar": "🤖"}
            with st.chat_message("assistant", avatar="🤖"):
                st.markdown(ai_response, unsafe_allow_html=True)
            st.session_state.messages.append(ai_message)  # 添加到所有历史记录
            st.session_state.recent_messages.append(ai_message)  # 添加到最近的5条记录

if __name__ == "__main__":
    show_ChatEverything_page()
