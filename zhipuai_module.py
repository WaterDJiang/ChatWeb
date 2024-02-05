#模型代码，负责模型的运行

import os
import streamlit as st
import json
from zhipuai import ZhipuAI
from functions import function_tools , function_map

# 设置智谱AI的API密钥
zhipu_api_key = "58fed83681006df393f2bf6bcffb3a9a.ILRQgQr0jUDGSPuX"
client = ZhipuAI(api_key=zhipu_api_key)


def sse_invoke_example(prompt_text):
    # 确保API密钥已设置
    if not zhipu_api_key:
        raise ValueError("API密钥未设置。")

    # 创建一个ZhipuAI客户端实例
    client = ZhipuAI(api_key=zhipu_api_key)

    # 构建prompt结构体
    prompt_input = [
        {"role": "system", "content": "你是人工智能助手Wattter.AI"},
        {"role": "user", "content": prompt_text}
    ]

    try:
        # 调用chat.completions.create函数并传递参数
        response = client.chat.completions.create(
            model="glm-4",  #"glm-3-turbo","glm-4"
            messages=prompt_input,
        )

        # 直接返回响应结果
        return response.choices[0].message.content
    except Exception as e:
        # 处理可能发生的异常
        return f"发生错误: {e}"

def glm_invoke(user_input):
    # 确保API密钥已设置
    if not zhipu_api_key:
        raise ValueError("API密钥未设置。")

    try:
        # 调用chat.completions.create函数并传递参数
        response = client.chat.completions.create(
            model="glm-4",  #"glm-3-turbo","glm-4"
            messages=user_input,
            tools=function_tools,
        )
        # print(response.choices[0].message)        # 调试项，查看内容
        return response
    except Exception as e:
        # 处理可能发生的异常
        return f"glm_invoke发生错误: {e}"
    
def parse_function_call(model_response, messages):
    try:
        if model_response.choices[0].message.tool_calls:
            tool_call = model_response.choices[0].message.tool_calls[0]
            args = tool_call.function.arguments
            function_result = {}
            
            # print(tool_call.function.name)                                                    # 调试项，查看内容

            function_to_call =tool_call.function.name

            if function_to_call:
                function_result =  function_map[function_to_call](**json.loads(args))
             
                print(function_result)                                                        # 调试项，查看内容

                messages.append({
                    "role": "tool",
                    "content": json.dumps(function_result),
                    "tool_call_id": tool_call.id
                })

                response = client.chat.completions.create(
                    model="glm-4",
                    messages=messages,
                    tools=function_tools
                )
                print(response)                                                                 # 调试项，查看内容
                return response.choices[0].message.content 
        
        else :
            response = model_response.choices[0].message.content       

            return response
    
    except Exception as e:
        print(f"Error in parse_function_call: {e}")


