import streamlit as st
import re
from file_handler import handle_uploaded_file
from openai_module import generate_with_openai_stream
from zhipuai_module import sse_invoke_example
from scraper import scrape_website
from datetime import datetime

# 正则表达式用于检测URL
URL_REGEX = re.compile(
    r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
    re.IGNORECASE)

def is_url(string):
    """检查字符串是否为URL"""
    return re.match(URL_REGEX, string) is not None

# 辅助函数
def extract_url_and_text(user_input):
    """从用户输入中提取网址和其他文本"""
    urls = re.findall(URL_REGEX, user_input)
    text_without_url = re.sub(URL_REGEX, '', user_input)
    return urls, text_without_url

def process_scraped_content(urls):
    """处理爬虫内容，并更新展示窗口及准备模型输入"""
    scraped_content = ""
    if urls:
        scraped_content = scrape_website(urls[0])
        scraped_content = str(scraped_content)
    return scraped_content

def update_content_output(new_content):
    """更新展示窗口内容"""
    # 更新展示窗口内容，只展示当前提交的内容
    st.session_state['content_output'] = new_content

def process_uploaded_or_template_content(file, content_type):
    """通用函数处理上传的文件或模板并返回内容"""
    try:
        content = handle_uploaded_file(file)
        if content_type == 'file':
            # 使用一个唯一的键来存储每个文件的内容
            key = f'uploaded_file_content_{file.name}'
            st.session_state[key] = content
        return content
    except Exception as e:
        st.error(f"处理上传的{content_type}时出错: {e}")
        return ""

# 主处理函数
def process_content_input(user_input, uploaded_file, template_file):
    """处理用户输入和上传文件的内容"""
    with st.spinner('烧脑中...'):
        try:
            urls, text_without_url = extract_url_and_text(user_input)
            scraped_content = process_scraped_content(urls) if urls else ""
            file_content_for_model = process_uploaded_or_template_content(uploaded_file, 'file') if uploaded_file else ""
            template_content = process_uploaded_or_template_content(template_file, 'file') if template_file else ""
            
            current_display_content = "\n".join([scraped_content, file_content_for_model]).strip()
            update_content_output(current_display_content)
            all_scraped_content = st.session_state.get('scraped_content', '') + "\n" + scraped_content
            all_uploaded_content = st.session_state.get('uploaded_file_content', '') + "\n" + file_content_for_model
            combined_input = combine_input(all_scraped_content, all_uploaded_content, text_without_url, template_content)
            st.session_state['combined_input'] = combined_input

            process_model(combined_input)

            st.session_state['scraped_content'] = all_scraped_content
            st.session_state['uploaded_file_content'] = all_uploaded_content
        except Exception as e:
            st.error(f"处理内容时出错: {e}")

def combine_input(scraped_content, file_content_for_model, text_without_url, template_content):
    """组合来自不同来源的输入内容"""
    def ensure_str(content):
        # 如果内容是字符串，直接返回
        if isinstance(content, str):
            return content
        # 如果内容是其他类型（例如Markdown对象），转换为字符串
        else:
            return str(content)  # 或者适当的转换方法

    # 确保所有部分都是字符串
    scraped_content_str = ensure_str(scraped_content)
    file_content_for_model_str = ensure_str(file_content_for_model)
    text_without_url_str = ensure_str(text_without_url)
    template_content_str = ensure_str(template_content)

    combined_input_parts = [
        part for part in [
            scraped_content_str,
            file_content_for_model_str,
            text_without_url_str,
            "请综合以上内容进行回复，回复的格式要求如下，请用markdown方式呈现：",  # 手动添加的模版提示
            template_content_str] 
        if part.strip()
    ]

    combined_input = "\n".join(combined_input_parts)
    st.session_state['combined_input'] = combined_input
    return combined_input

def process_model(combined_input):
    """调用AI模型处理"""
    ai_model = "智谱AI"
    response = sse_invoke_example(combined_input) if ai_model == "智谱AI" else generate_with_openai_stream(combined_input)
    st.session_state["ai_output"] = response

# 用户界面相关的函数
def show_buttons(col, button_label, on_click_function):
    """在指定列中显示按钮并绑定点击事件"""
    with col:
        if st.button(button_label):
            on_click_function()

def clear_content_input():
    """清除内容输入"""
    st.session_state.pop("content_output", None)
    st.session_state.pop("ai_output", None)

def show_ChatAnything_page():
    """显示主界面"""
    with st.sidebar:
        if 'show_file_uploader' not in st.session_state:
            st.session_state['show_file_uploader'] = False

        st.divider()

        user_input = st.text_area("输入任意内容开始探索吧", height=120)

        #上传按钮
        col1, col2 = st.columns([1, 2], gap="medium")

        uploaded_file = None
        with col1:
            if st.button("➕ 上传资料", key="btn_upload_file"):
                st.session_state['show_file_uploader'] = not st.session_state.get('show_file_uploader', False)

        if st.session_state.get('show_file_uploader', False):
            uploaded_file = st.file_uploader("选择需要上传的文件", type=["pdf", "docx", "txt", "xlsx", "xls", "pptx", "ppt", "csv"], key='file_uploader1')

        template_file = None
        with col2:
            if st.button("➕ 回复模版", key="btn_template_file"):
                st.session_state['show_template_uploader'] = not st.session_state.get('show_template_uploader', False)

        if st.session_state.get('show_template_uploader', False):
            template_file = st.file_uploader("选择需要上传的模版", type=["pdf", "docx", "txt", "xlsx", "xls", "pptx", "ppt", "csv"], key='file_uploader2')
        
        # 发送按钮
        col1, col2 = st.columns([1, 2], gap="medium")
        show_buttons(col1, "🚀 发送内容", lambda: process_content_input(user_input, uploaded_file, template_file))
        show_buttons(col2, "🧹 清除内容", clear_content_input)


        st.divider()
        # 这里可以添加其他介绍性文字或说明
        st.write(
            """
        小提示：

        1、输入任意内容开始探索；

        2、可上传PDF、DOC、PPT、CSV等资料互动；

        3、可添加回复模版获得你想要的格式内容；

        4、你甚至可以直接丢网址给我互动；

        5、多轮对话功能正在努力上线中……  
        """
        )

    with st.container():
        col1_1, col1_2 = st.columns([1, 15])
        with col1_1:
            image_path = "images/im2.jpg"  # 更改为您的图片路径
            st.image(image_path, width=70)
        with col1_2:
            st.title("ChatAnything")

        # 显示上传文件或用户输入的内容
        content_output_display = st.session_state.get('content_output', '')
        st.text_area("已发送的内容", content_output_display, height=250)

        st.divider()

        # AI模型的输出区域
        st.write("Wattter.AI")
        ai_output_display = st.session_state.get("ai_output", '')
        st.markdown(ai_output_display)

        # 如果有AI输出，提供下载按钮
        if ai_output_display:
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            download_filename = f"ChatAnything_{current_time}.txt"
            st.download_button(label="下载AI处理结果", data=ai_output_display, file_name=download_filename)

if __name__ == "__main__":
    show_ChatAnything_page()


