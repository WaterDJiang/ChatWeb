
# 定义各种 function 的细节

from zhipuai import ZhipuAI
import streamlit as st
import os
import json
import requests
from datetime import datetime, timedelta

# 设置智谱AI的API密钥
zhipu_api_key = "58fed83681006df393f2bf6bcffb3a9a.ILRQgQr0jUDGSPuX"
birth_info_key ="9923c679819f4e94af8ddb1f798b95ee"
footprint_key = "VJjxd5IbAsj8vbYp66wLbOxwJLNas6bB7D+zPo+JHAriJt4Bdy8zsRyBaOPmdI0G"


# GLM 画图函数
def get_cogview(viewprompt_text):
    client = ZhipuAI(api_key=zhipu_api_key) 

    response = client.images.generations(
        model="cogview-3", #填写需要调用的模型名称
        prompt=viewprompt_text,
    )
    response = response.data[0].url
    return response

# 读取 智谱 知识库 函数
def retrieval(query):
    client = ZhipuAI(api_key=zhipu_api_key)  # 确保zhipu_api_key已经被正确定义和初始化
    response = client.chat.completions.create(
        model="glm-4",  # 确认这是正确的模型名称
        messages=[
            {"role": "user", "content": query},  # 使用函数参数query
        ],
        tools=[
            {
                "type": "retrieval",
                "retrieval": {
                    "knowledge_id": "1749753525874864128",  # 确保knowledge_id已正确设置
                    "prompt_template": (
                        "从文档\n"
                        """\n"""
                        "{{knowledge}}\n"
                        """\n"""
                        "中找问题\n"
                        """\n"""
                        "{{question}}\n"
                        """\n"""
                        "的答案，找到答案就仅使用文档语句回答，找不到答案就用自身知识回答并告诉用户该信息不是来自文档。\n"
                        "不要复述问题，直接开始回答。"
                    ),
                }
            }
        ],
    )
    return response.choices[0].message.content

# 获取生辰八字的 API
def get_birth_info(year, month, day, hour):
    """
    通过生辰助手API获取八字等信息。

    :param year: 出生年份（公历）
    :param month: 出生月份（公历）
    :param day: 出生日期（公历）
    :param hour: 出生小时（可选，默认为None）
    :return: 返回API调用结果，一般为JSON格式数据
    """

    # 假设这是API的URL，实际使用时请替换成真实的API URL
    url = "http://apis.juhe.cn/birthEight/query"

    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }

    # API请求的参数，根据实际情况填写
    params = {
        "key":birth_info_key,  # 替换成实际的API Key
        "year": year,
        "month": month,
        "day": day,
        "hour": hour 
    }

    # 发起请求
    try:
        response = requests.get(url, params=params)
        # 判断响应状态码
        if response.status_code == 200:
            # 返回JSON数据
            return response.json()
        else:
            # 返回错误信息
            return {"error_code": response.status_code, "error_message": "Request failed"}
    except requests.RequestException as e:
        # 网络请求异常处理
        return {"error_code": 10014, "error_message": str(e)}
    

# moneyflow api
def get_moneyflow_info(token_address):
    today = datetime.today().date()
    midnight = datetime.combine(today, datetime.min.time())

    start_time = midnight- timedelta(days=7)
    print(start_time)
    end_time = midnight
    print(end_time)

    url = "https://api.footprint.network/api/v3/moneyFlow/getTokenMoneyFlow"

    payload = {
        "chain": "Ethereum",
        "res_include": ["tx_size", "tx_type"],
        "token_address": [token_address],
        "tx_size": "All",
        "tx_type": "All",
        "start_time": start_time.isoformat(),
        "end_time": end_time.isoformat(),
        "limit": 10,
        "offset": 10
    }
    headers = {
        "accept": "application/json",
        "api-key": footprint_key,
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)
    data = response.json()
    return json.dumps(data)


# # 外部API模版
# def get_api():
#     '''
#     定义一个获取api的函数样例代码
#     '''
#     # 第一步，构建请求，写入api地址
#     url = "https://api.example.com/data"

#     #第二步，设置查询参数
#     params={
#         "param1":"value1",
#         "appid":"your_appid",  # api key
#         "param2":"value2",
#         "param3":"value3"
#     }

#     #第三步，发送get请求
#     response = requests.get(url, params=params)

#     #第四步，解析响应
#     data = response.json()
#     return json.dumps(data)


# 定义函数库，函数名称和函数同名的格式
function_map = {
    "get_cogview" : get_cogview,
    "retrieval" : retrieval,
    "get_birth_info" : get_birth_info,
    "get_moneyflow_info" : get_moneyflow_info,
}



#函数字典编写

function_tools = [
            # 智谱知识库参数
            {                          #  function 开始
                "type": "function",
                "function":
                {
                    "name":"retrieval",
                    "description":"命理八字、易经风水、流年运势的知识库。",
                    "parameters":{ 
                        "type":"object",
                        "properties":{
                            "query":{
                                "description":"用户命理八字、易经风水、流年运势相关的问题",
                                "type":"string",
                            }
                        },
                        "required":["query"]
                    },
                }
            },                         #  function 结束

            # GLM4画图参数
            {                          #  function 开始
                "type": "function",
                "function":
                {
                    "name":"get_cogview",
                    "description":"使用ZhipuAI的画图API进行图像生成，并返回生成的图像URL。",
                    "parameters":{
                        "type":"object",
                        "properties":{
                            "viewprompt_text":{
                                "description":"图像生成的提示文本",
                                "type":"string",   
                            }
                        },
                        "required":["viewprompt_text"]
                    },
                } 
            },                        #  function 结束

            # 生辰八字获取api
            {                          #  function 开始
                "type": "function",
                "function":
                {
                    "name":"get_birth_info",
                    "description":"用户输入自己的出生年月日以及时间，譬如‘1988年11月12日8时’，获取生辰八字的排盘。",
                    "parameters":{
                        "type":"object",
                        "properties":{
                            "year":{
                                "description":"公历出生的年份",
                                "type":"string",
                            },
                            "month":{
                                "description":"出生的月份",
                                "type":"string",
                            },
                            "day":{
                                "description":"几号出生的",
                                "type":"string",
                            },
                            "hour":{
                                "description":"几点出生的",
                                "type":"string",
                            }
                        },
                        "required":["year", "month","day","hour"]
                    },
                } 
            },                        #  function 结束
                        # moneyflow
            {                          #  function 开始
                "type": "function",
                "function":
                {
                    "name":"get_moneyflow_info",
                    "description":"获取区块链地址的moneyflow、资金流向分析数据。",
                    "parameters":{
                        "type":"object",
                        "properties":{
                            "token_address":{
                                "description":"token地址信息",
                                "type":"string",   
                            }
                        },
                        "required":["token_address"]
                    },
                } 
            },                        #  function 结束
]