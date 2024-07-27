import cv2
import numpy as np
import argparse
import os
from tqdm import tqdm
import json
import time
from datetime import datetime

LOG_FILE = "face_detection_log.json"

# Load the pre-trained face detection model from OpenCV's DNN module
face_modelFile = "models/res10_300x300_ssd_iter_140000_fp16.caffemodel"
face_configFile = "models/deploy.prototxt"
face_net = cv2.dnn.readNetFromCaffe(face_configFile, face_modelFile)

# Load the pre-trained pose estimation model from OpenPose
pose_protoFile = "models/pose_deploy_linevec.prototxt"
pose_weightsFile = "models/pose/coco/pose_iter_440000.caffemodel"
pose_net = cv2.dnn.readNetFromCaffe(pose_protoFile, pose_weightsFile)

def detect_faces(frame):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(frame, (300, 300)), 1.0, (300, 300), (104.0, 177.0, 123.0))
    face_net.setInput(blob)
    detections = face_net.forward()
    faces = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:  # Confidence threshold
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            faces.append((startX, startY, endX, endY))
    return faces

def detect_pose(frame):
    frame_width = frame.shape[1]
    frame_height = frame.shape[0]
    threshold = 0.1

    input_blob = cv2.dnn.blobFromImage(frame, 1.0 / 255, (368, 368), (0, 0, 0), swapRB=False, crop=False)
    pose_net.setInput(input_blob)
    output = pose_net.forward()

    H = output.shape[2]
    W = output.shape[3]

    # Empty list to store the detected keypoints
    points = []
    for i in range(15):  # COCO has 18 keypoints, for simplicity we'll use 15
        prob_map = output[0, i, :, :]  # Confidence map.
        min_val, prob, min_loc, point = cv2.minMaxLoc(prob_map)
        x = (frame_width * point[0]) / W
        y = (frame_height * point[1]) / H

        if prob > threshold: 
            points.append((int(x), int(y)))
        else:
            points.append(None)
    return points

def classify_pose(points):
    if points[11] and points[14]:  # Checking for left shoulder and left ankle
        if abs(points[11][1] - points[14][1]) < 50:  # Threshold to classify sitting
            return "Sitting"
    if points[11] and points[14]:  # Checking for left shoulder and left ankle
        if abs(points[11][1] - points[14][1]) >= 50:  # Threshold to classify standing
            return "Standing"
    return "Unknown"

def format_timestamp(ts):
    return datetime.fromtimestamp(ts).strftime('%H:%M:%S')

def process_video(video_path):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}.")
        return False

    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    frame_count = 0
    working_time = 0
    non_working_time = 0
    faces_detected = False
    start_time = None

    with tqdm(total=total_frames, desc=f"Processing {video_path}", unit="frame") as pbar:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            faces = detect_faces(frame)
            if faces:
                working_time += (1 / fps)
                if not faces_detected:
                    start_time = time.time()
                faces_detected = True
            else:
                non_working_time += (1 / fps)
                if faces_detected:
                    end_time = time.time()
                    duration = end_time - start_time
                    print(f"Face detected from {format_timestamp(start_time)} to {format_timestamp(end_time)} duration: {duration:.2f}s")
                faces_detected = False

            points = detect_pose(frame)
            pose = classify_pose(points)
            print(f"Detected Pose: {pose}")

            frame_count += 1
            pbar.update(1)

    cap.release()

    total_time = working_time + non_working_time
    print(f"Total time: {total_time:.2f}s, Working time: {working_time:.2f}s, Non-working time: {non_working_time:.2f}s")

    return {"total_time": total_time, "working_time": working_time, "non_working_time": non_working_time}

def save_progress(log):
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=4)

def load_progress():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    return {"processed_files": []}

def process_directory(directory_path):
    log = load_progress()
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Add other video formats if needed
                video_path = os.path.join(root, file)
                if video_path in log["processed_files"]:
                    print(f"Skipping already processed video: {video_path}")
                    continue

                print(f"Checking video: {video_path}")
                result = process_video(video_path)
                log["processed_files"].append(video_path)
                log[video_path] = result
                save_progress(log)

def main():
    parser = argparse.ArgumentParser(description="Detect faces and poses in CCTV videos and log working/non-working time.")
    parser.add_argument('directory', type=str, help='Path to the directory containing CCTV video files')
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' not found.")
        return
    
    print(f"Processing directory: {args.directory}")
    process_directory(args.directory)

if __name__ == "__main__":
    main()