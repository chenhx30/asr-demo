import json
import logging
import logging.config  # 导入 logging.config 模块
import ssl
import uvicorn
import websocket

from fastapi import FastAPI, UploadFile, HTTPException
from starlette.responses import JSONResponse

app = FastAPI()

# 加载日志配置文件
logging.config.fileConfig('../logging.conf')

# 创建日志记录器
logger = logging.getLogger(__name__)

# 全局变量用于存储 WSS 连接
wss_connection = None

async def initialize_wss_connection():
    global wss_connection
    try:
        # 创建 WebSocket 连接并设置 SSL 证书验证绕过选项
        wss_connection = websocket.create_connection("wss://192.168.102.32:10095/", sslopt={"cert_reqs": ssl.CERT_NONE})
        start_data = {
            "mode": "offline",
            "wav_name": "wav_name",
            "wav_format": "wav",
            "is_speaking": True,
            "itn": True
        }
        # 将字典对象序列化为 JSON 字符串
        json_string = json.dumps(start_data)
        logger.info("初始化 WSS 连接 JSON 字符串: %s", json_string)
        wss_connection.send(json_string)
    except Exception as e:
        logger.error("初始化 WSS 连接失败: %s", e, exc_info=True)

async def close_wss_connection():
    global wss_connection
    if wss_connection:
        await wss_connection.close()
        logger.info("关闭 WSS 连接")

# 初始化 WSS 连接
@app.on_event("startup")
async def startup_event():
    await initialize_wss_connection()

# 关闭 WSS 连接
@app.on_event("shutdown")
async def shutdown_event():
    await close_wss_connection()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    if not file:
        raise HTTPException(status_code=400, detail="未提供文件")
    result = await process_upload(file)
    return JSONResponse(content={"result": result})

async def process_upload(file: UploadFile):
    global wss_connection
    if not wss_connection:
        logger.error("WebSocket 连接未初始化")
        return None

    try:
        chunk_size = 8192  # 每次读取的文件块大小
        while True:
            contents = await file.read(chunk_size)
            if not contents:
                break
            wss_connection.send_binary(contents)

        end_data = {
            "mode": "offline",
            "wav_name": file.filename,
            "wav_format": "wav",
            "is_speaking": False
        }
        # 将字典对象序列化为 JSON 字符串
        end_json_string = json.dumps(end_data)
        logger.info("将字典对象序列化为 JSON 字符串: %s", end_json_string)
        wss_connection.send(end_json_string)
        result = wss_connection.recv()
        result_obj = json.loads(result)
        result_text = remove_period(result_obj['text'])
        logger.info("识别结果: %s", result_text)
        return result_text
    except Exception as e:
        logger.error("处理上传文件时发生错误: %s", e, exc_info=True)
        return None

def remove_period(text):
    # 移除文本末尾的句号
    if text.endswith('。'):
        text = text[:-1]
    return text

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
