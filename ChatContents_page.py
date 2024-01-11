import streamlit as st
from datetime import datetime
import io
import os

# 导入特定的功能而不是整个模块
from file_handler import handle_uploaded_file
from openai_module import generate_with_openai_stream
from zhipuai_module import sse_invoke_example

def show_ChatContents_page():
    # 定义AI模型选择的常量
    AI_MODELS = ["智谱AI", "OpenAI"]

    # 创建页面布局：左侧25%和右侧75%
    col1, col2 = st.columns([1, 3], gap="medium")

    # 左侧容器
    with col1:
        # 网页信息
        col1_1, col1_2 = st.columns([1, 4])
        # 主图像
        with col1_1:
            image_path = "im2.JPG"
            st.image(image_path, width=70)
        # 网页标题
        with col1_2:
            st.title("ChatContents")
        # 作者和版本信息
        st.caption("作者: [ Wattter ] - 版本 0.4.0")

        # 文件上传与解析
        st.subheader("1. 上传文件进行解析：")
        uploaded_file = st.file_uploader("上传文件", type=["pdf", "docx", "txt", "xlsx", "xls", "pptx", "ppt", "jpeg", "png"])

        if uploaded_file is not None:
            # 使用后端函数处理文件
            file_content = handle_uploaded_file(uploaded_file)
            st.session_state['uploaded_content'] = file_content

            # 清除按钮
            if st.button("清除结果", key="clear_results_button_2"):
                st.session_state.clear()
                st.rerun()

            # 与AI交互输入
            st.subheader("2. 通过AI与内容对话")
            ai_model_selector = st.selectbox("选择AI模型：", AI_MODELS, key="ai_model_selector")
            ai_prompt_input = st.text_area("请输入想要AI做的事情：", height=200)
            ai_prompt_combined = st.session_state.get('uploaded_content', '') + "\n" + ai_prompt_input

            if st.button("提交",key="click_button_2"):
                with st.spinner('AI正在处理，请稍候...'):
                    try:
                        if ai_model_selector == "OpenAI":
                            generated_text = generate_with_openai_stream(ai_prompt_combined)
                        else:
                            generated_text = sse_invoke_example(ai_prompt_combined)

                        st.session_state['ai_response'] = generated_text
                        st.success('AI处理完成。')
                    except Exception as e:
                        st.error(f"AI处理失败：{e}")

    # 右侧容器
    with col2:
        # 显示上传的内容
        uploaded_content = st.session_state.get('uploaded_content')
        if uploaded_content:
            st.text_area("上传文件的内容", uploaded_content, height=250)
            if st.button("保存解析的内容",key="save_button_11"):
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
                file_name = f"{current_time}.txt"
                with io.BytesIO() as buffer:
                    buffer.write(uploaded_content.encode())
                    buffer.seek(0)
                    st.download_button(
                        label=f"下载 {file_name}",
                        data=buffer,
                        file_name=file_name,
                        mime="text/plain"
                    )
                st.success(f"内容已保存，点击链接下载: {file_name}")
            else:
                st.write("没有解析到内容或内容为空。")

        # 显示AI响应
        ai_response = st.session_state.get('ai_response')
        if ai_response:
            st.markdown(ai_response)
            if st.button("保存AI结果",key="save_button2"):
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
                file_name = f"ai结果_{current_time}.txt"
                with io.BytesIO() as buffer:
                    buffer.write(ai_response.encode())
                    buffer.seek(0)
                    st.download_button(
                        label=f"下载 {file_name}",
                        data=buffer,
                        file_name=file_name,
                        mime="text/plain"
                    )
                st.success(f"AI结果已保存，点击链接下载: {file_name}")

