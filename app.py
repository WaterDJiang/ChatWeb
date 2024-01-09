import streamlit as st
import os
from scraper import scrape_website
from openai_module import generate_with_openai_stream
from zhipuai_module import sse_invoke_example
from datetime import datetime
import click
import io

# 一次性获取所有必要的环境变量
# openai_api_key, zhipuai_api_key = map(os.getenv, ['OPENAI_API_KEY', 'ZHIPUAI_API_KEY'])

# 保存内容到文件
def save_content_to_file(file_name, content):
    with open(file_name, "w", encoding="utf-8") as file:
        file.write(content)

# 判断内容是否为有效的文本或数据表
def is_valid_content(content):
    return isinstance(content, (str, list, dict))

# 重置除指定键外的所有会话状态
def reset_session_state(except_keys=None):
    for key in list(st.session_state.keys()):
        if not except_keys or key not in except_keys:
            del st.session_state[key]

# 保存内容到内存并写入文件
def save_content_to_memory(content, file_name):
    file_buffer = io.BytesIO()
    file_buffer.write(content.encode())
    with open(file_name, "wb") as f:
        f.write(file_buffer.getvalue())
    click.echo(f"文件已保存: {file_name}")

# 保存内容到文件并触发下载，返回文件名
def save_and_download(content, file_prefix):
    current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    file_name = f"{file_prefix}_{current_time}.txt"
    save_content_to_memory(content, file_name)
    return file_name

# 设置页面布局为宽屏模式
st.set_page_config(layout="wide")

# 创建页面总布局，左右布局，左边占比25%，右边占比75%
col1, col2 = st.columns([1, 3], gap="medium")

# 左侧容器
with col1:
    # 网页信息栏
    col1_1, col1_2 = st.columns([1, 4])
    #主页图片
    with col1_1:
        image_path = "头像.JPG"
        st.image(image_path, width=70)
    # 网页标题
    with col1_2:
        st.title("ChatWeb")
    # 添加作者和版本号信息
    st.caption("作者: [ Wattter ] - 版本 0.2.0")

    # 网址输入栏
    url_input = st.text_input("请输入想要对话的网址：", value='', key="url_input")
    clear_button, scrape_button = st.columns([1, 2])  # 创建清除和爬取按钮
    if clear_button.button("清除结果"):
        reset_session_state(['url_input'])  # 清除输入，保留url_input以防止重复清除
        st.rerun()  # 重新运行以更新页面
    if scrape_button.button("开始解析你的内容") and url_input:
        with st.spinner('正在解析内容，请稍候...'):
            try:
                title, content = scrape_website(url_input)  # 调用爬虫函数
                if content:
                    st.session_state.update({'scraped_content': content, 'scraped_title': title})
                    st.success('网页内容解析成功。')
                else:
                    st.error("解析失败：" + title)
            except Exception as e:
                st.error(f"解析过程中发生错误: {e}")
            
  # ai-prompt输入
    st.subheader("Chat with AI")
    ai_model_selector = st.selectbox("选择AI模型：", ["智谱AI", "OpenAI"])
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

# 右侧容器
with col2:
    # 爬取内容输出区域
    if 'scraped_content' in st.session_state:
        if st.session_state['scraped_content']:
            st.text_area("原文的内容", st.session_state['scraped_content'], height=250)
            if st.button("保存解析的内容"):
                current_time = datetime.now().strftime("%Y-%m-%d_%H-%M")
                file_name = f"{current_time}.txt" if is_valid_content(st.session_state['scraped_content']) else f"{current_time}.csv"
                save_content_to_file(file_name, st.session_state['scraped_content'])
                st.success(f"内容已保存为: {file_name}")
                
                # 使用st.download_button提供下载按钮
                with open(file_name, "rb") as f:
                    st.download_button(
                        label=f"下载 {file_name}",
                        data=f,
                        file_name=file_name,
                        mime="text/plain"
                    )
        else:
            # 爬取的内容存在但为空
            st.write("没有解析到内容或内容为空。")
    
    # AI处理输出区域
    if st.session_state.get('ai_response'):
        # 显示AI处理结果
        st.markdown(st.session_state['ai_response'])
        if st.button("保存AI结果"):
            current_time = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            file_name = f"ai结果_{current_time}.txt"
            save_content_to_file(file_name, st.session_state['ai_response'])
            st.success(f"AI结果已保存为: {file_name}")
            
            # 使用st.download_button提供下载按钮
            with open(file_name, "rb") as f:
                st.download_button(
                    label=f"下载 {file_name}",
                    data=f,
                    file_name=file_name,
                    mime="text/plain"
                )
