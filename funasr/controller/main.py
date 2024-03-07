import json
import ssl

import websocket
from fastapi import FastAPI, UploadFile

app = FastAPI()

# 全局变量用于存储 WSS 连接
wss_connection = None

# 初始化 WSS 连接
@app.on_event("startup")
async def startup_event():
    global wss_connection
    # 这里进行 WSS 连接的初始化，例如连接到 WSS 服务器
    wss_connection = websocket.create_connection("wss://192.168.102.32:10095/", sslopt={"cert_reqs": ssl.CERT_NONE})
    start_data = {
        "mode": "offline",
        "wav_name": "wav_name",
        "wav_format":"wav",
        "is_speaking": True,
        # "hotwords":"{\"阿里巴巴\":20,\"通义实验室\":30}",
        "itn":True
    }
    # 将字典对象序列化为 JSON 字符串
    json_string = json.dumps(start_data)
    print("初始化 WSS 连接 JSON 字符串: " + json_string)
    wss_connection.send(json_string)


@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    await fuck666(file)
    return {"result": "successfully"}

    #result = await fuck666(file)
    #return {"result": result}

async def fuck666(file: UploadFile):
    global wss_connection
    contents = await file.read()
    wss_connection.send_binary(contents)
    end_data = {
        "mode": "offline",
        "wav_name": "wav_name",
        "wav_format":"wav",
        "is_speaking": False
    }
    # 将字典对象序列化为 JSON 字符串
    end_json_string = json.dumps(end_data)
    print("将字典对象序列化为 JSON 字符串: " + end_json_string)
    wss_connection.send(end_json_string)
    result = wss_connection.recv()
    result_obj = json.loads(result)
    result_text = remove_period(result_obj['text'])
    print("识别结果: " + result_text)
    return result_text

def remove_period(text):
    # 移除文本末尾的句号
    if text.endswith(' 。'):
        text = text[:-1]
    return text