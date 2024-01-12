import streamlit as st

def show_home_page():
    image_path = "images/im1.jpg"
    st.image(image_path, width=70)
    text = """
    
## 不仅仅是阅读，试试和你喜欢的内容交谈，让AI带你深入“内容”之心。
## 发现、解析、互动——一切尽在掌握！
    """
    st.write(text)

    text = """
    ---
## ChatWeb & ChatContents：释放内容新魅力

### 轻松获取内容精华
- 只需输入你感兴趣的**网页、PDF、DOC…**，我们就能帮你迅速捕获关键信息。无论是深入探索还是快速浏览摘要，都能得到你所需要的内容。

### 个性化内容重塑
- 喜欢某篇文章但觉得它可以更好？告诉我们，AI将为你重新编排文字，以全新面貌呈现信息。

### 智慧总结一键呈现
- 长篇大论不再费时。ChatWeb会按照你的思路进行智能总结，帮助你节省时间同时吸收核心信息。

### 提问探求深层次理解
- 直接向任何内容提出问题！像有个专家在旁边解答疑惑一样。AI将对整个网页进行分析，并针对你的问题给出详尽回复。

### 随手存储知识宝藏
- 发现珍贵资料？一键保存后稍后查看也行。聚集知识，随时翻阅。

- 用AI开启高效率学习和工作方式！
---
    """
    st.write(text)

    # 使用st.columns创建两个并排的列
    col1, col2 = st.columns(2)

    # 在第一列中显示第一张图像
    with col1:
        image_path = "images/web.jpg"
        st.image(image_path, caption='ChatWeb',width=800)  # 调整宽度以适应列宽

    # 在第二列中显示第二张图像
    with col2:
        image_path = "images/contents.jpg"
        st.image(image_path, caption='ChatContents', width=800)  # 调整宽度以适应列宽

    text = """
    ---
## 如何使用

### 步骤1: 输入网址并解析内容
- 在页面上找到输入框并填入想要探究的**网址**。
- 点击`开始解析`按钮, ChatWeb将展示网页标题和重点内容。
- 如果需要重新操作，使用`清除结果`按钮来移除当前显示的信息。

### 步骤2: 与AI进行互动对话
- 在`选择AI模型`下拉菜单中挑选您偏爱的AI（智谱AI或OpenAI）。
- 将您希望了解或请求 AI 做的事情输入到文本框中。
- 提交请求后等待片刻, AI将提供您所需的答案或服务。

### 步骤3: 保存结果以便之后参考

#### - 保存已解析的内容：
    - 解析完成后，在右侧预览区查看原文及其要点。
    - 点击 `保存解析的内容` 按钮即可下载该信息为文本文件备用。

#### - 保存AI生成的响应：
    - 待AI生成反馈后, 同样在右侧预览区内查看完整回复。
    - 使用 `保存AI结果` 功能把这段智慧成果转存为文本文件。


    """
    st.write(text)
    st.write("欢迎通过以下方式与我们联系：")
    col1, col2 = st.columns([5, 5], gap="small")

    with col1:
        # 显示微信二维码
        st.image("images/Wechat.jpg", caption="微信", width=400)

    with col2:
        # 显示 Telegram 二维码
        st.image("images/telegram.jpg", caption="Telegram", width=400)

