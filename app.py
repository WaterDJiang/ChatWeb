import streamlit as st
from datetime import datetime
import click
import io
import os

# Import specific functions instead of the whole modules
from scraper import scrape_website
from openai_module import generate_with_openai_stream
from zhipuai_module import sse_invoke_example

# Define constants for AI model selection
AI_MODELS = ["智谱AI", "OpenAI"]

# Initialize Streamlit page config
st.set_page_config(layout="wide")

# Create page layout: 25% for left and 75% for right
col1, col2 = st.columns([1, 3], gap="medium")

# Left container
with col1:
    # Web page info
    col1_1, col1_2 = st.columns([1, 4])
    # Main image
    with col1_1:
        image_path = "头像.JPG"
        st.image(image_path, width=70)
    # Web page title
    with col1_2:
        st.title("ChatWeb")
    # Author and version info
    st.caption("作者: [ Wattter ] - 版本 0.2.0")

    # Web URL input
    url_input = st.text_input("请输入想要对话的网址：", value='', key="url_input")
    clear_button, scrape_button = st.columns([1, 2])  # Create clear and scrape buttons
    if clear_button.button("清除结果"):
        st.session_state.clear()
        st.rerun()  # Rerun to update the page
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

    # AI prompt input
    st.subheader("Chat with AI")
    ai_model_selector = st.selectbox("选择AI模型：", AI_MODELS)
    ai_prompt_input = st.text_area("请输入想要AI做的事情：", height=200)
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

# Right container
with col2:
    # Display scraped content
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

    # Display AI response
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

