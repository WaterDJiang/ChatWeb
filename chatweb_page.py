import streamlit as st
from datetime import datetime
import click
import io
import os

# 导入特定的功能而不是整个模块
from scraper import scrape_website
from openai_module import generate_with_openai_stream
from zhipuai_module import sse_invoke_example

def show_chatweb_page():
    

    # 定义AI模型选择的常量
    AI_MODELS = ["智谱AI"] # "OpenAI"

    # 创建页面布局：左侧25%和右侧75%
    col1, col2 = st.columns([1, 3], gap="medium")

    # 左侧容器
    with col1:
        # 网页信息
        col1_1, col1_2 = st.columns([1, 4])
        # 主图像
        with col1_1:
            image_path = "im1.JPG"
            st.image(image_path, width=70)
        # 网页标题
        with col1_2:
            st.title("ChatWeb")
        # 作者和版本信息
        st.caption("作者: [ Wattter ] - 版本 0.4.0")

        # 网址输入
        url_input = st.text_input("1.请输入想要对话的网址：", value='', key="url_input")
        clear_button, scrape_button = st.columns([1, 2])  # 创建清除和解析按钮
        if clear_button.button("清除结果", key="clear_results_button"):
            st.session_state.clear()
            st.rerun()  # 重新运行以更新页面
        if scrape_button.button("开始解析你的内容") and url_input:
            with st.spinner('正在解析内容，请稍候...'):
                try:
                    title, content = scrape_website(url_input)
                    if content:
                        st.session_state.update({'scraped_content': content, 'scraped_title': title})
                        st.success('网页内容解析成功。')
                    else:
                        st.error("解析失败：" + title)
                except Exception as e:
                    st.error(f"解析过程中发生错误: {e}")

        # 与AI交互输入
        st.subheader("通过AI与内容对话")
        ai_model_selector = st.selectbox("选择AI模型：", AI_MODELS)
        ai_prompt_input = st.text_area("2.请输入想要AI做的事情：", height=200)
        ai_prompt_combined = st.session_state.get('scraped_content', '') + "\n" + ai_prompt_input
        if st.button("提交"):
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
        # 显示解析的内容
        if 'scraped_content' in st.session_state:
            scraped_content = st.session_state['scraped_content']
            if scraped_content:
                st.text_area("原文的内容", scraped_content, height=250)
                if st.button("保存解析的内容"):
                    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
                    file_name = f"{current_time}.txt" if isinstance(scraped_content, str) else f"{current_time}.csv"
                    with io.BytesIO() as buffer:
                        buffer.write(scraped_content.encode())
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
            if st.button("保存AI结果"):
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
