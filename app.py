import streamlit as st

# 在全局位置调用 set_page_config
st.set_page_config(layout="wide")

# 导入页面模块
from home_page import show_home_page
# from ChatContents_page import show_ChatContents_page
# from chatweb_page import show_chatweb_page
from ChatAnything_page import show_ChatAnything_page

# 创建侧边栏

st.sidebar.title("Wattter.AI")
st.caption("作者: [ Water.J ] - 版本 0.5.0")

# 定义页面选项
page_options = ["首页", "ChatAnything"] #"ChatWeb", "ChatContents"

# 创建下拉菜单以选择页面
selected_page = st.sidebar.selectbox("选择工具开启你的AI之旅吧", page_options)


# 根据所选页面显示相应内容
if selected_page == "首页":
    show_home_page()
# elif selected_page == "ChatWeb":
#     show_chatweb_page()
# elif selected_page == "ChatContents":
#     show_ChatContents_page()
elif selected_page == "ChatAnything":
    show_ChatAnything_page()

