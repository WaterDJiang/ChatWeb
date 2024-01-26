import streamlit as st
import streamlit_analytics #引入外部统计组件

# 加入网页点击记录
with streamlit_analytics.track(): #在访问路由后加上“?analytics=on”就能在网页上看到如下统计组件图

    # 在全局位置调用 set_page_config
    st.set_page_config(
        page_title="Wattter.AI",
        page_icon="🧊",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    # 导入页面模块
    from home_page import show_home_page
    # from ChatContents_page import show_ChatContents_page
    from ChatEverything_page import show_ChatEverything_page
    from ChatAnything_page import show_ChatAnything_page

    # 创建侧边栏
    with st.sidebar:
            col1_1, col1_2 = st.columns([1,3])
            with col1_1:
                image_path = "images/im3.png"
                st.image(image_path, width=70)
            with col1_2:
                st.title("Wattter.AI")
                # 显示固定的版本信息
                st.sidebar.caption("作者：[ Water.D.J ] -- 版本： 0.6.1")
                st.sidebar.caption("https://chatweb.streamlit.app")


    # 定义页面选项
    page_options = ["ChatAnything","ChatEverything","介绍页"] #"ChatWeb", "ChatContents"

    # 创建下拉菜单以选择页面
    selected_page = st.sidebar.radio("选择工具开启你的AI之旅吧", page_options)


    # 根据所选页面显示相应内容
    if selected_page == "介绍页":
        show_home_page()
    elif selected_page == "ChatEverything":
        show_ChatEverything_page()
    # elif selected_page == "ChatContents":
    #     show_ChatContents_page()
    elif selected_page == "ChatAnything":
        show_ChatAnything_page()
