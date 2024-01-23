from zhipuai import ZhipuAI
import os
import streamlit as st

# 设置智谱AI的API密钥
zhipu_api_key = st.secrets["zhipuai"]["api_key"]

def cogview_huatu(viewprompt_text):
    client = ZhipuAI(api_key=zhipu_api_key) 

    response = client.images.generations(
        model="cogview-3", #填写需要调用的模型名称
        prompt=viewprompt_text,
    )
    return response.data[0].url