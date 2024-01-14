import streamlit as st

def show_home_page():
    
    # 侧边栏
    with st.sidebar:
        st.divider() #画一条分界线
        st.title("这里是首页哟")

        tool_selected = st.sidebar.radio("点击以下按钮可以查看介绍", ["简介", "使用说明", "联系我们"])
    
    with st.container():
        if tool_selected == "简介":
            show_main_page()
        elif tool_selected == "使用说明":
            show_note_tool()
        elif tool_selected == "联系我们":
            show_contact_us()

def show_main_page():
    image_path = "images/im3.png"
    st.image(image_path, width=70)
    
    st.write("""
    ## 不仅仅是阅读，试试和你喜欢的内容交谈，让AI带你深入“内容”之心。
    ## 发现、解析、互动——一切尽在掌握！
    """)
    st.divider() #画一条分界线

    st.write("""
    ##  ChatAnything ：释放内容新魅力

    ### 轻松获取内容精华
    - 只需输入你感兴趣的**网页、PDF、DOC…**，我们就能帮你迅速捕获关键信息。无论是深入探索还是快速浏览摘要，都能得到你所需要的内容。

    ### 个性化内容重塑
    - 喜欢某篇文章但觉得它可以更好？告诉我们，AI将为你重新编排文字，以全新面貌呈现信息。

    ### 智慧总结一键呈现
    - 长篇大论不再费时。ChatAnything会按照你的思路进行智能总结，帮助你节省时间同时吸收核心信息。

    ### 提问探求深层次理解
    - 直接向任何内容提出问题！像有个专家在旁边解答疑惑一样。AI将对整个网页进行分析，并针对你的问题给出详尽回复。

    ### 随手存储知识宝藏
    - 发现珍贵资料？一键保存后稍后查看也行。聚集知识，随时翻阅。

    - 用AI开启高效率学习和工作方式！

    """)

def show_note_tool():
    st.write("""
    ## 使用说明

    ChatAnything 是一个用于处理文本和应用AI模型交互的应用程序。以下是如何使用它的简单步骤：

    ### 主页面

    在主页面中，您将看到两个主要部分：左边侧边栏的“内容输入”和“AI处理需求”和右边的内容输出界面。

    ### 内容输入

    1. 在左侧边栏的文本框中，您可以输入文本或者网址。或者如果您有一个文件，您可以上传它（支持的文件类型包括pdf、docx、txt、xlsx、xls、pptx、ppt、csv）。

    2. 点击“发送内容”按钮，ChatAnything 将处理您的输入并在右边的内容输出栏显示处理后的内容。

    3. 如果您想清除内容输入，可以点击“清除内容”按钮。

    ### AI处理需求

    1. 在左侧边栏的AI文本框中，您可以输入AI处理的需求或模板。同样，您也可以上传一个需求模板文件。

    2. 选择AI模型（目前为默认模型）。

    3. 点击“发送内容”按钮，ChatAnything 将使用您的内容和需求来进行AI处理，并在右方显示处理后的结果。

    4. 如果您想清除AI输入，可以点击“清除AI内容”按钮。

    ### 结果和下载

    如果AI处理完成，并且有结果显示，您可以点击“下载”按钮来下载结果文本文件。
   
    """)
    st.divider() #画一条分界线

    st.write("""### 使用案例 """)

    image_path = "images/web.jpg"
    st.image(image_path, caption='ChatWeb', width=None)

    st.divider() #画一条分界线

    image_path = "images/fin.jpg"
    st.image(image_path, caption='ChatData', width=None)

    st.divider() #画一条分界线

    image_path = "images/template.jpg"
    st.image(image_path, caption='ChatAnything', width=None)

    st.divider() #画一条分界线

    pass


def show_contact_us():
    st.subheader("欢迎通过以下方式与我联系：")
    col1, col2 = st.columns([5, 5], gap="small")

    with col1:
        # 显示微信二维码
        st.image("images/Wechat.jpg", caption="微信", width=300)

    with col2:
        # 显示 Telegram 二维码
        st.image("images/telegram.jpg", caption="Telegram", width=300)
    pass


if __name__ == "__main__":
    show_home_page()

