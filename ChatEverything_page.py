
import streamlit as st
from zhipuai_module import sse_invoke_example
import time


def memory_prompt(prompt_text, history):
    """
    将用户的输入和聊天历史结合起来，但只包括最近的5条历史记录。

    参数:
    prompt_text (str): 用户的最新消息。
    history (list of dict): 聊天历史，其中每条消息是一个包含 'role' 和 'content' 键的字典。

    返回:
    str: 包含历史的完整提示文本。
    """
    # 仅选择最近的5条聊天记录
    recent_history = history[-5:]

    # 将聊天历史转换为字符串
    history_str = "\n".join([f"{message['role']}: {message['content']}" for message in recent_history])
    
    # 将最新的用户输入添加到历史字符串中
    full_prompt = history_str + "\nUser: " + prompt_text

    return full_prompt


def show_ChatEverything_page():
    # 初始化聊天历史，设置版头
    with st.container():
        col1_1, col1_2 = st.columns([1, 15])
        with col1_1:
            image_path = "images/im2.jpg"  # 更改为您的图片路径
            st.image(image_path, width=70)
        with col1_2:
            st.title("ChatEverything")
    st.divider()

    # 添加删除聊天历史的按钮
    if st.sidebar.button('清理聊天记录'):
        st.session_state.messages = []

    # 初始化聊天历史
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # 在应用重新运行时显示历史聊天信息
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    # 接受用户输入
    if prompt_text := st.chat_input("说点什么?"):
        # 在聊天消息容器中显示用户消息
        user_avatar = "🤵"
        with st.chat_message("user", avatar=user_avatar):
            st.write(prompt_text)
        # 将用户消息添加到聊天历史中
        st.session_state.messages.append({"role": "user", "content": prompt_text, "avatar": user_avatar})

        # 生成并显示助手响应
        ai_avatar = "🤖"
        with st.chat_message("ai", avatar=ai_avatar):
            message_placeholder = st.empty()
            full_response = ""
            # 结合用户输入与聊天历史
            full_prompt = memory_prompt(prompt_text, st.session_state.messages)
            assistant_response = sse_invoke_example(full_prompt)

            # 模拟响应的流式传输，带有毫秒级延迟
            for chunk in assistant_response.split():
                full_response += chunk + " "
                time.sleep(0.08)
                # 添加闪烁的光标以模拟打字
                message_placeholder.write(full_response + "▌")
            message_placeholder.write(full_response)
        # 将助手的响应添加到聊天历史中
        st.session_state.messages.append({"role": "ai", "content": full_response, "avatar": ai_avatar})

if __name__ == "__main__":
    show_ChatEverything_page()
