import cv2
import subprocess
import os
import sys
from pathlib import Path

def detect_motion(video_file, threshold=30, min_duration=10):
    cap = cv2.VideoCapture(video_file)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    motion_timestamps = []
    motion = False
    start_time = 0
    end_time = 0

    while cap.isOpened():
        diff = cv2.absdiff(frame1, frame2)
        gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blur, threshold, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if len(contours) > 0:
            if not motion:
                start_time = int(cap.get(cv2.CAP_PROP_POS_MSEC)) / 1000
                motion = True
        else:
            if motion:
                end_time = int(cap.get(cv2.CAP_PROP_POS_MSEC)) / 1000
                motion = False
                duration = end_time - start_time
                if duration >= min_duration:
                    motion_timestamps.append((start_time, end_time))
        frame1 = frame2
        ret, frame2 = cap.read()

        if not ret:
            break

    cap.release()
    cv2.destroyAllWindows()
    return motion_timestamps


def verbose_progress(current, total):
    progress = (current / total) * 100
    print(f"Progress: {progress:.2f}%")


def process_videos(folder):
    video_extensions = ['.mp4', '.avi', '.mkv', '.mov']
    video_files = [v for v in Path(folder).iterdir() if v.suffix.lower() in video_extensions]
    total_files = len(video_files)

    for index, video_file in enumerate(video_files, start=1):
        motion_timestamps = detect_motion(str(video_file))
        if len(motion_timestamps) > 0:
            output_file = video_file.stem + "_motion" + video_file.suffix
            ffmpeg_cmd = ['ffmpeg', '-y', '-i', str(video_file)]
            for start, end in motion_timestamps:
                ffmpeg_cmd.extend([
                        '-ss', str(max(0, start - 3)),
                        '-to', str(end + 3),
                        '-c', 'copy',
                        '-map', '0',
                        '-f', 'segment',
                        '-segment_time', '0.01',
                        '-reset_timestamps', '1',
                        '-segment_format', 'mp4',
                        output_file + '_%d' + video_file.suffix
              ])
            subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            print(f'Processed {video_file} - motion detected')
        verbose_progress(index, total_files)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python motion_detection.py <folder>")
        sys.exit(1)

    folder = sys.argv[1]
    if not os.path.isdir(folder):
        print(f"{folder} is not a valid directory")
        sys.exit(1)

    process_videos(folder)
