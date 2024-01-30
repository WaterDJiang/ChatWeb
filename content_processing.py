# # 输入内容处理 + 模型内容处理
# import streamlit as st
# import re
# from file_handler import handle_uploaded_file
# from openai_module import generate_with_openai_stream
# from zhipuai_module import sse_invoke_example
# from scraper import scrape_website
# from datetime import datetime
# from cogview import cogview_huatu

# # 正则表达式用于检测URL
# URL_REGEX = re.compile(
#     r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*(),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
#     re.IGNORECASE)

# def is_url(string):
#     """检查字符串是否为URL"""
#     return re.match(URL_REGEX, string) is not None

# # 辅助函数
# def extract_url_and_text(user_input):
#     """从用户输入中提取网址和其他文本"""
#     urls = re.findall(URL_REGEX, user_input)
#     text_without_url = re.sub(URL_REGEX, '', user_input)
#     print("URLs found:", urls)  # 调试信息
#     return urls, text_without_url

# def process_scraped_content(urls):
#     """处理爬虫内容，并更新展示窗口及准备模型输入"""
#     try:
#         scraped_content = ""
#         if urls:
#             scraped_content = scrape_website(urls[0])
#             scraped_content = str(scraped_content)
#         return scraped_content
#     except Exception as e:
#         print("Error in process_scraped_content:", e)
#     return ""

# def update_content_output(new_content):
#     """更新展示窗口内容"""
#     # 更新展示窗口内容，只展示当前提交的内容
#     st.session_state['content_output'] = new_content

# def process_uploaded_or_template_content(file, content_type):
#     """通用函数处理上传的文件或模板并返回内容"""
#     try:
#         content = handle_uploaded_file(file)
#         if content_type == 'file':
#             # 使用一个唯一的键来存储每个文件的内容
#             key = f'uploaded_file_content_{file.name}'
#             st.session_state[key] = content
#         return content
#     except Exception as e:
#         st.error(f"处理上传的{content_type}时出错: {e}")
#         return ""

# def combine_input(scraped_content, file_content_for_model, text_without_url, template_content):
#     """组合来自不同来源的输入内容"""
#     def ensure_str(content):
#         # 如果内容是字符串，直接返回
#         if isinstance(content, str):
#             return content
#         # 如果内容是其他类型（例如Markdown对象），转换为字符串
#         else:
#             return str(content)  # 或者适当的转换方法

#     # 确保所有部分都是字符串
#     scraped_content_str = ensure_str(scraped_content)
#     file_content_for_model_str = ensure_str(file_content_for_model)
#     text_without_url_str = ensure_str(text_without_url)
#     template_content_str = ensure_str(template_content)

#     combined_input_parts = [
#         part for part in [
#             scraped_content_str,
#             file_content_for_model_str,
#             text_without_url_str,
#             "请综合以上内容进行回复，回复的格式要求如下，请用markdown方式呈现：",  # 手动添加的模版提示
#             template_content_str] 
#         if part.strip()
#     ]

#     combined_input = "\n".join(combined_input_parts)
#     st.session_state['combined_input'] = combined_input
#     return combined_input

# def process_content_input(user_input, uploaded_file, template_file):
#     """处理用户输入和上传文件的内容"""
#     with st.spinner('烧脑中...'):
#         try:
#             urls, text_without_url = extract_url_and_text(user_input)
#             scraped_content = process_scraped_content(urls) if urls else ""
#             file_content_for_model = process_uploaded_or_template_content(uploaded_file, 'file') if uploaded_file else ""
#             template_content = process_uploaded_or_template_content(template_file, 'file') if template_file else ""
            
#             current_display_content = "\n".join([scraped_content, file_content_for_model]).strip()
#             update_content_output(current_display_content)
#             all_scraped_content = st.session_state.get('scraped_content', '') + "\n" + scraped_content
#             all_uploaded_content = st.session_state.get('uploaded_file_content', '') + "\n" + file_content_for_model
#             combined_input = combine_input(all_scraped_content, all_uploaded_content, text_without_url, template_content)
#             st.session_state['combined_input'] = combined_input

#             process_model(combined_input)

#             st.session_state['scraped_content'] = all_scraped_content
#             st.session_state['uploaded_file_content'] = all_uploaded_content
#         except Exception as e:
#             st.error(f"处理内容时出错: {e}")

# def process_cogview_input(user_input, uploaded_file, template_file):
#     """处理用户画图需求"""
#     with st.spinner('烧脑中...'):
#         try:
#             urls, text_without_url = extract_url_and_text(user_input)
#             scraped_content = process_scraped_content(urls) if urls else ""
#             file_content_for_model = process_uploaded_or_template_content(uploaded_file,  'file') if uploaded_file else ""
#             template_content = process_uploaded_or_template_content(template_file, 'file') if template_file else ""
            
#             current_display_content = "\n".join([scraped_content, file_content_for_model]).strip()
#             update_content_output(current_display_content)
#             all_scraped_content = st.session_state.get('scraped_content', '') + "\n" + scraped_content
#             all_uploaded_content = st.session_state.get('uploaded_file_content', '') + "\n" + file_content_for_model
#             combined_input = combine_input(all_scraped_content, all_uploaded_content, text_without_url, template_content)
#             st.session_state['combined_input'] = combined_input

#             process_cogview(combined_input)

#             st.session_state['scraped_content'] = all_scraped_content
#             st.session_state['uploaded_file_content'] = all_uploaded_content
#         except Exception as e:
#             st.error(f"处理内容时出错: {e}")

# def process_model(combined_input):
#     """调用AI模型处理"""
#     ai_model = "智谱AI"
#     response = sse_invoke_example(combined_input) if ai_model == "智谱AI" else generate_with_openai_stream(combined_input)
#     st.session_state["ai_output"] = response

# def process_cogview(combined_input):  # 定义画图工具
#     """调用AI画图处理"""
#     ai_model = "智谱AI"
#     response = cogview_huatu(combined_input) if ai_model == "智谱AI" else generate_with_openai_stream(combined_input)
#     st.session_state["cogview_output"] = response

import streamlit as st
import re
from file_handler import handle_uploaded_file
from zhipuai_module import sse_invoke_example
from scraper import scrape_website
from datetime import datetime
from cogview import cogview_huatu

# 正则表达式用于检测URL
URL_REGEX = re.compile(r'http[s]?://\S+', re.IGNORECASE)

def is_url(string):
    """检查字符串是否为URL"""
    return re.match(URL_REGEX, string) is not None

def extract_url_and_text(user_input):
    """从用户输入中提取网址和其他文本"""
    urls = re.findall(URL_REGEX, user_input)
    text_without_url = re.sub(URL_REGEX, '', user_input)
    return urls, text_without_url

def process_scraped_content(urls):
    """处理爬虫内容"""
    try:
        return scrape_website(urls[0]) if urls else ""
    except Exception as e:
        st.error(f"处理爬取内容时出错: {e}")
        return ""

def update_content_output(new_content):
    """更新展示窗口内容"""
    st.session_state['content_output'] = new_content

def process_uploaded_content(file):
    """处理上传的文件内容"""
    try:
        return handle_uploaded_file(file) if file else ""
    except Exception as e:
        st.error(f"处理上传的文件时出错: {e}")
        return ""

def combine_input(scraped_content, uploaded_content, text_without_url, template_content):
    """组合输入内容"""

    def ensure_str(content):
        # 确保内容是字符串类型
        return str(content) if content is not None else ""

    # 将所有内容转换为字符串
    scraped_content_str = ensure_str(scraped_content)
    uploaded_content_str = ensure_str(uploaded_content)
    text_without_url_str = ensure_str(text_without_url)
    template_content_str = ensure_str(template_content)

    # 组合输入内容
    combined_input_parts = [
        part for part in [
            scraped_content_str, 
            uploaded_content_str, 
            text_without_url_str, 
            "请综合以上内容进行回复，回复的格式要求如下：",  # 手动添加的模版提示
            template_content_str,
            "请用markdown方式输出。"
        ] if part.strip()
    ]
    update_content_output(scraped_content_str + uploaded_content_str)
    combined_input = "\n".join(combined_input_parts)
    return combined_input

def process_input(user_input, uploaded_file, template_file, process_function=None):
    """通用函数处理输入"""
    with st.spinner('烧脑中...'):
        try:
            urls, text_without_url = extract_url_and_text(user_input)

            # 只在存在URLs时进行爬虫
            scraped_content = process_scraped_content(urls) if urls else ""

            # 只在存在上传文件时处理文件内容
            uploaded_content = process_uploaded_content(uploaded_file) if uploaded_file else ""
            template_content = process_uploaded_content(template_file) if template_file else ""
            
            combined_input = combine_input(scraped_content, uploaded_content, text_without_url, template_content)
            
            # 初始化 session_state 中的 combined_input
            st.session_state['combined_input'] = combined_input

            # 仅当提供了有效的处理函数时才调用
            if process_function is not None:
                process_function(combined_input)

            # 保存爬取和上传的内容，以备未来使用
            st.session_state['scraped_content'] = scraped_content
            st.session_state['uploaded_file_content'] = uploaded_content
        except Exception as e:
            st.error(f"处理输入时出错: {e}")

def process_model(combined_input):
    """调用AI模型处理"""
    response = sse_invoke_example(combined_input)
    st.session_state["ai_output"] = response

def process_cogview(combined_input):
    """调用AI画图处理"""
    response = cogview_huatu(combined_input)
    st.session_state["cogview_output"] = response
