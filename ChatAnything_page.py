# ChatAnyting 前端交互部分
import streamlit as st
import pandas as pd
from datetime import datetime
from ChatAnything_content_processing import *
from zhipuai_module import sse_invoke_example
import streamlit as st
from datetime import datetime


def use_info():
        st.divider()
        # 这里可以添加其他介绍性文字或说明
        st.info(
            """
        小提示：

        1、这是一个自媒体内容快速生产工具；

        2、通过“输入链接”获取 或 “上传资料”的方式准备你的原材料；

        3、通过添加“回复模版” 或直接输入的方式 添加你想要的内容生产模版；

        4、完成原材料和模版准备，点击“内容生产”就可以获得ai为你生产的内容；

        5、在内容修改区域，可以修改自己ai生成的内容，并可以在预览区看到修改后的效果。

        """
        )

def update_content_output(new_content):
    """更新展示窗口内容"""
    # 更新展示窗口内容，只展示当前提交的内容
    st.session_state['content_output'] = new_content


# 用户界面相关的函数
def show_buttons( button_label, on_click_function, key):
    """在指定列中显示按钮并绑定点击事件"""
    if st.button(button_label, key=key):
        on_click_function()

def clear_content_input():
    """清除内容输入"""
    st.session_state.pop("content_output", None)
    st.session_state.pop("ai_output", None)


def handle_web_input( web_input_key, button_key, content_output_key, expander_key): 
    # 使用st.columns创建两个列，分别用于放置web输入框和获取按钮
    col1, col2 = st.columns([3, 1])  # 调整列的宽度比例，可以根据需要进行调整

    with col1:
        web_input = st.text_input("", key=web_input_key,label_visibility = "collapsed") # 将输入框放在第一列

    with col2:
        if st.button("获取", key=button_key):  # 将获取按钮放在第二列
            with st.spinner("正在获取内容..."):
                urls, text_without_url = extract_url_and_text(web_input)
                scraped_content = process_scraped_content(urls)
                st.session_state[content_output_key] = scraped_content
    # 检查st.session_state中是否已经有获取的内容，如果有，则在expander中显示
    if content_output_key in st.session_state:
        scraped_content = st.session_state[content_output_key]
    else:
        scraped_content = ""

    with st.expander(f"获取内容 {expander_key.split('_')[-1]}"):
        st.text_area('', scraped_content, height=250, key=expander_key)


def show_ChatAnything_page():
    """显示主界面"""
    with st.sidebar:
        if 'show_file_uploader' not in st.session_state:
            st.session_state['show_file_uploader'] = False

        st.divider()

        #上传按钮
        uploaded_file = None
        if st.button("➕ 上传资料", key="btn_upload_file"):
            st.session_state['show_file_uploader'] = not st.session_state.get('show_file_uploader', False)

        if st.session_state.get('show_file_uploader', False):
            uploaded_file = st.file_uploader("选择需要上传的文件", type=["pdf", "docx", "txt", "xlsx", "xls", "pptx", "ppt", "csv"], key='file_uploader1')
            uploaded_content = process_uploaded_content(uploaded_file)
            st.session_state['uploaded_content'] = uploaded_content

        template_file = None

        if st.button("➕ 回复模版", key="btn_template_file"):
            st.session_state['show_template_uploader'] = not st.session_state.get('show_template_uploader', False)

        if st.session_state.get('show_template_uploader', False):
            template_file = st.file_uploader("选择需要上传的模版", type=["pdf", "docx", "txt", "xlsx", "xls", "pptx", "ppt", "csv"], key='file_uploader2')
            template_content = process_uploaded_content(template_file)
            st.session_state['template_content'] = template_content
        
        # 发送按钮
        show_buttons("🧹 清除内容", clear_content_input, key="clear_button1")
        
        #显示使用教程
        use_info()


    with st.container():
        main_col1, main_col2 = st.columns([1, 2.5])  # 创建两个主列

        with main_col1:  # 主列1用于网页内容获取
            st.write("内容获取区域")
            # 处理第一列的输入、获取按钮和显示内容
            handle_web_input("dummy_input1", "dummy_button1", "web1_content_output", "scraped_content_1")
            web1_content_output = st.session_state.get('web1_content_output', '')
            # 处理第二列的输入、获取按钮和显示内容
            handle_web_input("dummy_input2", "dummy_button2", "web2_content_output", "scraped_content_2")
            web2_content_output = st.session_state.get('web2_content_output', '')

            uploaded_content = st.session_state.get('uploaded_content', '')
            template_content = st.session_state.get('template_content', '')
            with st.expander("上传的内容"):
                st.text_area('', uploaded_content, height=250, key=uploaded_content)

            combine_content = web1_content_output + web2_content_output + uploaded_content

            st.caption("内容生产模版")
            user_input_template_content = st.text_area("", value=template_content, key="template_content", height=250, label_visibility="collapsed")
            if st.button("🚀 内容生产", key="button_key"):  # 将获取按钮放在第二列
                with st.spinner("烧脑中..."):
                    combine_input = f"请结合这里的内容：\n{combine_content}并按照这个模版或者要求：\n{user_input_template_content}完成文案创作，请用markdown格式回复，不要超过1000字"
                    process_content = sse_invoke_example(combine_input)
                    st.session_state['process_content'] = process_content

        with main_col2:  # 主列2用于显示上传文件或用户输入的内容以及其他功能
            # 显示上传文件或用户输入的内容
            st.write("内容修改区域")
            content_output_display = st.session_state.get('process_content')
            user_modify_content = st.text_area("", value=content_output_display,key="content_output_display", height=400, label_visibility="collapsed")
            st.divider()

            # AI模型的输出区域
            st.write("预览内容")
            # 尝试获取ai_output和cogview_output
            ai_output = user_modify_content

            # 初始化或获取会话状态变量
            if 'ready_to_download' not in st.session_state:
                st.session_state['ready_to_download'] = False
            if 'download_filename' not in st.session_state:
                st.session_state['download_filename'] = f"ChatAnything_{datetime.now().strftime('%Y%m%d%H%M%S')}.txt"

            # 判断获取到的内容是哪一种类型并相应展示
            if ai_output is not None:
                # 展示markdown格式的ai_output
                st.write(ai_output)

                if st.session_state['ready_to_download']:
                    # 如果用户已经准备下载，显示文件名输入和下载按钮
                    download_filename = st.text_input("请输入下载文件的名称：", st.session_state['download_filename'], key="download_filename_input")
                    if st.download_button(label="确认并下载AI处理结果", data=ai_output, file_name=download_filename):
                        st.session_state['ready_to_download'] = False  # 重置下载状态
                else:
                    # 显示初始下载按钮
                    if st.button("下载AI处理结果"):
                        st.session_state['ready_to_download'] = True
            else:
                # 如果都没有获取到，展示提示信息
                st.write("暂无输出内容")

if __name__ == "__main__":
    show_ChatAnything_page()

