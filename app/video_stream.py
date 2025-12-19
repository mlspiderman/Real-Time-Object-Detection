import cv2
from app.detector import ObjectDetector

detector = ObjectDetector()

def generate_frames():
    cap = cv2.VideoCapture(0)
    
    while True:
        success, frame = cap.read()
        if not success:
            break
        
        frame_resized = cv2.resize(frame, (640, 480))
        detections = detector.predict(frame_resized)
        
        for det in detections:
            x1, y1, x2, y2 = map(int, det["bbox"])
            label = det["class_name"]
            conf = det["confidence"]
            
            cv2.rectangle(frame, (x1, y1,), (x2, y2), (0,255,0), 2)
            cv2.putText(
                frame,
                f"{label} {conf:.2f}",
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0,255,0),
                2
            )
           
            ret, buffer = cv2.imencode('.jpg', frame)
            frame_bytes = buffer.tobytes()
          
            yield (
                b'--frame\r\n'
                b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
    cap.release()
