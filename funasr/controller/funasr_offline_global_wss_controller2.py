import uvicorn
import websocket
from fastapi import FastAPI, UploadFile, HTTPException, Depends
from starlette.responses import JSONResponse
from funasr.service.funasr_offline_global_wss_service import get_wss_connection, process_upload, remove_period

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile, wss: websocket.WebSocket = Depends(get_wss_connection)):
    if not file:
        raise HTTPException(status_code=400, detail="未提供文件")
    if not wss:
        raise HTTPException(status_code=500, detail="无法连接到 WebSocket")
    result = await process_upload(file, wss)
    return JSONResponse(content={"result": result})

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
