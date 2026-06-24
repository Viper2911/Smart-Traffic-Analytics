import cv2
import numpy as np
import math
from ultralytics import YOLO

def process_traffic_stream(video_path, model_path):
    model = YOLO(model_path)
    cap = cv2.VideoCapture(video_path)

    PIXELS_PER_METER = 15.0  
    vertices1 = np.array([(465, 350), (609, 350), (510, 630), (2, 630)], dtype=np.int32)
    vertices2 = np.array([(678, 350), (815, 350), (1203, 630), (743, 630)], dtype=np.int32)
    x1, x2 = 325, 635
    lane_threshold = 609
    font = cv2.FONT_HERSHEY_SIMPLEX

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps != fps: 
        fps = 30.0

    vehicle_history = {} 
    frame_count = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break
            
        frame_count += 1
        detection_frame = frame.copy()
        detection_frame[:x1, :] = 0
        detection_frame[x2:, :] = 0
        
        results = model.track(detection_frame, persist=True, imgsz=640, conf=0.4, verbose=False)
        processed_frame = results[0].plot(line_width=1)
        
        processed_frame[:x1, :] = frame[:x1, :].copy()
        processed_frame[x2:, :] = frame[x2:, :].copy()
        
        cv2.polylines(processed_frame, [vertices1], isClosed=True, color=(0, 255, 0), thickness=2)
        cv2.polylines(processed_frame, [vertices2], isClosed=True, color=(255, 0, 0), thickness=2)
        
        vehicles_in_left_lane = 0
        vehicles_in_right_lane = 0

        if results[0].boxes is not None and results[0].boxes.id is not None:
            boxes = results[0].boxes.xyxy.cpu().numpy()
            track_ids = results[0].boxes.id.int().cpu().tolist()

            for box, track_id in zip(boxes, track_ids):
                x1_box, y1_box, x2_box, y2_box = box
                
                if x1_box < lane_threshold:
                    vehicles_in_left_lane += 1
                else:
                    vehicles_in_right_lane += 1
                
                center_x = int((x1_box + x2_box) / 2)
                center_y = int((y1_box + y2_box) / 2)

                if track_id in vehicle_history:
                    prev_x, prev_y, prev_frame = vehicle_history[track_id]
                    time_elapsed = (frame_count - prev_frame) / fps
                    
                    if time_elapsed > 0:
                        pixel_distance = math.sqrt((center_x - prev_x)**2 + (center_y - prev_y)**2)
                        distance_meters = pixel_distance / PIXELS_PER_METER
                        speed_kmh = (distance_meters / time_elapsed) * 3.6
                        
                        cv2.putText(processed_frame, f"{int(speed_kmh)} km/h", (int(x1_box), int(y1_box) - 10), 
                                    font, 0.6, (0, 255, 255), 2, cv2.LINE_AA)
                
                vehicle_history[track_id] = (center_x, center_y, frame_count)

        processed_frame = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
        yield processed_frame, vehicles_in_left_lane, vehicles_in_right_lane

    cap.release()