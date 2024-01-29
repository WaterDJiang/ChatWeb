# ChatAnyting 前端交互部分
import streamlit as st
from datetime import datetime
from content_processing import (process_input, process_model , process_cogview)

def update_content_output(new_content):
    """更新展示窗口内容"""
    # 更新展示窗口内容，只展示当前提交的内容
    st.session_state['content_output'] = new_content


# 用户界面相关的函数
def show_buttons(col, button_label, on_click_function, key):
    """在指定列中显示按钮并绑定点击事件"""
    with col:
        if st.button(button_label, key=key):
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
        col1, col2 = st.columns([1, 1], gap="medium")

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
        col1, col2 = st.columns([1, 1], gap="medium")
        show_buttons(col1, "🚀 发送内容", lambda:  process_input(user_input, uploaded_file, template_file, process_model), key="send_button1")
        show_buttons(col2, "🧹 清除内容", clear_content_input, key="clear_button1")

        # 发送画图按钮
        col1, col2 = st.columns([1, 1], gap="medium")
        show_buttons(col1, "🖌️ 开始画图", lambda: process_input(user_input, uploaded_file, template_file, process_cogview), key="send_button2")
        # show_buttons(col2, "🧹 清除内容", clear_content_input, key="clear_button2")


        st.divider()
        # 这里可以添加其他介绍性文字或说明
        st.write(
            """
        小提示：

        1、输入任意内容开始探索；

        2、可上传PDF、DOC、PPT、CSV等资料互动；

        3、可添加回复模版获得你想要的格式内容；

        4、你甚至可以直接丢网址给我互动；

        5、画图功能上线啦 ✨；
        
        6、多轮对话功能正在努力上线中……  

        7、使用指南
        
          （1）点击“上传资料”（整合到一个文件上传）；
          
          （2）点击“上传模版”上传你需要的空白模版；
          
          （3）点击“发送内容、开始画图”，获得结果；
         
          （4）没有模版，也可以直接在输入框输入问题或要求。
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
        # 尝试获取ai_output和cogview_output
        ai_output = st.session_state.get("ai_output", None)
        cogview_output = st.session_state.get("cogview_output", None)

        # 判断获取到的内容是哪一种类型
        if ai_output is not None:
            # 如果是ai_output，则用markdown展示
            st.markdown(ai_output)
            # 如果有AI输出，提供下载按钮
            current_time = datetime.now().strftime("%Y%m%d%H%M%S")
            download_filename = f"ChatAnything_{current_time}.txt"
            st.download_button(label="下载AI处理结果", data=ai_output, file_name=download_filename)
        elif cogview_output is not None:
            # 如果是cogview_output，则用image展示
            st.image(cogview_output, width=500)
        else:
            # 如果都没有获取到，展示一个提示信息
            st.write("暂无输出内容")

if __name__ == "__main__":
    show_ChatAnything_page()
