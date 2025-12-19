from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from app.video_stream import generate_frames
import numpy as np
import cv2
from app.detector import ObjectDetector

app = FastAPI()
detector = ObjectDetector()
app.mount("/dashboard", StaticFiles(directory="dashboard"), name="dashboard")

@app.get("/")
def root():
    return {"status": "ok"}
    
@app.post("/detect-image")
async def detect_image(file: UploadFile = File(...)):
    image_data = await file.read()
    nparr = np.frombuffer(image_data, np.uint8)
    frame = cv2. imdecode(nparr, cv2.IMREAD_COLOR)
    
    detections = detector.predict(frame)
    
    return {"detections": detections}

@app.get("/video-stream")
def video_stream():
    return StreamingResponse(
        generate_frames(),
        media_type="multipart/x-mixed-replace; boundary=frame"
    )

@app.get("/dashboard-page", response_class=HTMLResponse)
def dashboard_page():
    with open("dashboard/index.html") as f:
        return f.read()
