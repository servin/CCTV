import cv2
import numpy as np
import argparse
import os
from tqdm import tqdm
import json

LOG_FILE = "video_processing_log.json"

def is_frame_mostly_black(frame, threshold=0.99):
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    non_black_pixels = np.count_nonzero(gray_frame)
    total_pixels = frame.shape[0] * frame.shape[1]
    black_ratio = (total_pixels - non_black_pixels) / total_pixels
    return black_ratio >= threshold

def check_video_black(video_path, sample_rate=0.1, threshold=0.99):
    cap = cv2.VideoCapture(video_path)
    
    if not cap.isOpened():
        print(f"Error: Could not open video {video_path}.")
        return False
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    sample_interval = int(1 / sample_rate)
    frame_count = 0
    black_frame_count = 0
    
    with tqdm(total=total_frames, desc=f"Processing {video_path}", unit="frame") as pbar:
        for i in range(0, total_frames, sample_interval):
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            ret, frame = cap.read()
            if not ret:
                break
            
            frame_count += 1
            
            if is_frame_mostly_black(frame, threshold=threshold):
                black_frame_count += 1
            
            pbar.update(sample_interval)

    cap.release()
    
    if frame_count == 0:
        print(f"Error: No frames found in the video {video_path}.")
        return False
    
    is_empty = black_frame_count / frame_count >= threshold
    return is_empty

def save_progress(log):
    with open(LOG_FILE, 'w') as f:
        json.dump(log, f, indent=4)

def load_progress():
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, 'r') as f:
            return json.load(f)
    return {"deleted": [], "not_deleted": [], "processed_files": []}

def process_directory(directory_path, delete_empty=False, sample_rate=0.1, threshold=0.99):
    log = load_progress()
    for root, _, files in os.walk(directory_path):
        for file in files:
            if file.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):  # Add other video formats if needed
                video_path = os.path.join(root, file)
                if video_path in log["processed_files"]:
                    print(f"Skipping already processed video: {video_path}")
                    continue
                
                print(f"Checking video: {video_path}")
                is_empty = check_video_black(video_path, sample_rate=sample_rate, threshold=threshold)
                if is_empty:
                    print(f"The video {video_path} is empty.")
                    log["processed_files"].append(video_path)
                    if delete_empty:
                        os.remove(video_path)
                        log["deleted"].append(video_path)
                        print(f"The empty video {video_path} has been deleted.")
                    else:
                        log["not_deleted"].append(video_path)
                else:
                    print(f"The video {video_path} has content.")
                    log["not_deleted"].append(video_path)
                save_progress(log)

def main():
    parser = argparse.ArgumentParser(description="Check if CCTV videos in a directory are empty.")
    parser.add_argument('-d', '--directory', type=str, required=True, help='Path to the directory containing CCTV video files')
    parser.add_argument('--delete', action='store_true', help='Delete empty video files after evaluation')
    parser.add_argument('-s', '--sample_rate', type=float, default=0.1, help='Sampling rate for checking frames (default: 0.1)')
    parser.add_argument('-t', '--threshold', type=float, default=0.99, help='Threshold for determining if a video is empty (default: 0.99)')
    args = parser.parse_args()

    if not os.path.isdir(args.directory):
        print(f"Error: Directory '{args.directory}' not found.")
        return
    
    print(f"Processing directory: {args.directory}")
    process_directory(args.directory, delete_empty=args.delete, sample_rate=args.sample_rate, threshold=args.threshold)

if __name__ == "__main__":
    main()