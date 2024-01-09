import zhipuai

# 设置智谱AI的API密钥
zhipuai.api_key = "your-api-key"

#定义一个函数，用于调用智谱AI模型并处理前端传入的文本
def sse_invoke_example(prompt_text):
    # 直接构建prompt结构体
    promptinput = [
        {"role": "user", "content": prompt_text}
    ]
    # 调用sse_invoke函数并传递参数
    response = zhipuai.model_api.sse_invoke(
        model="chatglm_turbo",
        prompt=promptinput,
        temperature=0.9,
        top_p=0.7,
        incremental=True
    )
    
    result = ""
    for event in response.events():
        if event.event in ["add", "finish"]:
            result += event.data
            if event.event == "finish":
                break
        elif event.event in ["error", "interrupted"]:
            result += "Error or interrupted: " + event.data
            break

    return result
