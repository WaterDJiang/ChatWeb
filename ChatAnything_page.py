import streamlit as st
import re
from file_handler import handle_uploaded_file
from openai_module import generate_with_openai_stream
from zhipuai_module import sse_invoke_example
from scraper import scrape_website
from datetime import datetime

# 编译好的正则表达式，用于检测URL
URL_REGEX = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # 域名
    r'localhost|'  # 本地主机
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # 或IP
    r'(?::\d+)?'  # 可选端口
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

# 判断字符串是否为有效URL的函数
def is_url(string):
    return re.match(URL_REGEX, string) is not None

# 显示两列布局中的按钮
def show_buttons(col, button_label, on_click_function):
    with col:
        if st.button(button_label):
            on_click_function()

# 主页面函数
def show_ChatAnything_page():
    with st.sidebar:
        st.write(""" --- """)
        user_input = st.text_area("1.请输入文本，甚至试试网址", height=100)
        uploaded_file = st.file_uploader("或上传文件", type=["pdf", "docx", "txt", "xlsx", "xls", "pptx", "ppt", "csv"])

        col1, col2 = st.columns(2)
        show_buttons(col1, "提交内容", lambda: process_content_input(user_input, uploaded_file))
        show_buttons(col2, "清除内容", clear_content_input)

        ai_model_selector = "智谱AI"  # 默认，不显示模型可选项目
        # ai_model_selector = st.selectbox("选择AI模型", ["智谱AI", "OpenAI"]) #显示模型可选项目
        ai_input = st.text_area("2.输入AI处理需求", height=100)
        ai_uploaded_file = st.file_uploader("或上传需求模版", type=["pdf", "docx", "txt", "xlsx", "xls", "pptx", "ppt", "csv"])

        col3, col4 = st.columns(2)
        show_buttons(col3, "提交AI", lambda: process_ai_input(ai_input, ai_uploaded_file, ai_model_selector))
        show_buttons(col4, "清除AI内容", clear_ai_input)

    with st.container():
        col1_1, col1_2 = st.columns([1,15])
        with col1_1:
            image_path = "images/im2.jpg"
            st.image(image_path, width=70)
        with col1_2:
            st.title("ChatAnything")
        st.caption("作者: [ Wattter ] - 版本 0.5.0")

        content_output_display = st.session_state.get('content_output', '')
        st.text_area("已提交的内容", content_output_display, height=300)

        ai_output_display = st.session_state.get("ai_output", '')
        st.write(ai_output_display)

        if ai_output_display:
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            download_filename = f"ChatAnything_{current_time}.txt"
            st.download_button(label="下载AI处理结果", data=ai_output_display, file_name=download_filename)

def process_content_input(user_input, uploaded_file):
    with st.spinner('正在处理内容...'):
        try:
            processed_input = ""
            if is_url(user_input):
                processed_input = scrape_website(user_input)
            elif uploaded_file is not None:
                file_content = handle_uploaded_file(uploaded_file)
                processed_input = file_content + "\n" + user_input
            else:
                processed_input = user_input
            st.session_state["content_output"] = processed_input
            st.session_state['user_input'] = user_input
        except Exception as e:
            st.error(f"处理内容时出错: {e}")

def clear_content_input():
    st.session_state.pop("content_output", None)
    st.session_state.pop('user_input', None)

def process_ai_input(ai_input, ai_uploaded_file, ai_model):
    with st.spinner('AI处理中...'):   
        try:
            user_input = st.session_state.get("content_output", "")
            user_input = str(user_input)

            # 确保 ai_uploaded_file 的内容是字符串
            ai_file_content = handle_uploaded_file(ai_uploaded_file) if ai_uploaded_file is not None else ""
            ai_file_content = str(ai_file_content)

            combined_input = user_input + "\n" + "请根据以上资料按以下要求或模版输出内容" + "\n"+ ai_input + ai_file_content 

            if ai_model == "智谱AI":
                response = sse_invoke_example(combined_input)
            else:
                response = generate_with_openai_stream(combined_input)

            st.session_state["ai_output"] = response
        except Exception as e:
            st.error(f"处理AI输入时出错: {e}")

def clear_ai_input():
    st.session_state.pop("ai_output", None)

if __name__ == "__main__":
    show_ChatAnything_page()
