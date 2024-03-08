import json
import logging.config  # 导入 logging.config 模块
import ssl
import time

import websocket
from fastapi import FastAPI, UploadFile, HTTPException
from starlette.responses import JSONResponse

app = FastAPI()

# 加载日志配置文件
logging.config.fileConfig('../logging.conf')

# 创建日志记录器
logger = logging.getLogger(__name__)

# WebSocket 服务器地址
WSS_URL = "wss://192.168.102.32:10095/"

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    if not file:
        raise HTTPException(status_code=400, detail="未提供文件")

    try:
        start_time = time.time()
        result = process_upload(file)
        end_time = time.time()
        logger.info("耗时: %.2f 秒", end_time - start_time)
        return JSONResponse(content={"result": result.strip()})
    except Exception as e:
        logger.error("处理上传文件时发生错误: %s", e, exc_info=True)
        return JSONResponse(content={"error": "上传文件时发生错误"}, status_code=500)

def process_upload(file: UploadFile):
    try:
        # 创建新的 WebSocket 连接
        wss_connection = websocket.create_connection(WSS_URL, sslopt={"cert_reqs": ssl.CERT_NONE})

        start_data = {
            "mode": "offline",
            "wav_name": file.filename,
            "wav_format": "wav",
            "is_speaking": True,
            "itn": True
        }
        json_string = json.dumps(start_data)
        wss_connection.send(json_string)

        chunk_size = 8192  # 每次读取的文件块大小
        while True:
            contents = file.file.read(chunk_size)
            if not contents:
                break
            wss_connection.send_binary(contents)

        end_data = {
            "mode": "offline",
            "wav_name": file.filename,
            "wav_format": "wav",
            "is_speaking": False
        }
        end_json_string = json.dumps(end_data)
        wss_connection.send(end_json_string)

        result = wss_connection.recv()
        result_obj = json.loads(result)
        result_text = remove_period(result_obj['text'])
        logger.info("识别结果: %s", result_text)
        wss_connection.close()
        return result_text
    except Exception as e:
        logger.error("处理上传文件时发生错误: %s", e, exc_info=True)
        return None

def remove_period(text):
    if text.endswith('。'):
        text = text[:-1]
    return text.strip()  # 移除前后的空格

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
