import streamlit as st

# 在全局位置调用 set_page_config
st.set_page_config(layout="wide")

# Import the page modules
from home_page import show_home_page
from ChatContents_page import show_ChatContents_page
from chatweb_page import show_chatweb_page  # Import the original ChatWeb page

# 添加标签页
tab1, tab2, tab3 = st.tabs(["首页","ChatWeb", "ChatContents"])

# 主应用程序
with tab1:
    show_home_page()
with tab2:
    show_chatweb_page()
with tab3:
    show_ChatContents_page()

