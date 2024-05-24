# CCTV Video Black Frame Checker

This Python script is designed to check if CCTV videos in a specified directory are mostly black (empty). It can process various video formats, sample frames at specified intervals, and optionally delete videos that are deemed empty.

## Features

- **Frame Sampling**: Instead of reading every frame, the script samples frames at regular intervals to determine if the video is empty.
- **Customizable Threshold**: Set the threshold for what percentage of black frames constitutes an empty video.
- **Logging**: Keeps track of processed videos, including which were deleted and which were not, to allow resuming operations.
- **Resumable Operations**: If interrupted, the script can resume from where it left off using a log file.
- **Multi-format Support**: Supports common video formats like `.mp4`, `.avi`, `.mov`, and `.mkv`.

## Requirements

- Python 3.x
- OpenCV (`cv2`)
- NumPy (`numpy`)
- tqdm (`tqdm`)

## Installation

1. Clone the repository or download the script.
2. Install the required Python packages:

    ```bash
    pip install opencv-python numpy tqdm
    ```

## Usage

### Command-Line Arguments

- `-f` or `--file`: Path to the directory containing CCTV video files (required).
- `-d` or `--delete`: Delete empty video files after evaluation (optional).
- `-s` or `--sample_rate`: Sampling rate for checking frames (default: `0.1`).
- `-t` or `--threshold`: Threshold for determining if a video is empty (default: `0.99`).

### Example Command

```bash
python check_video_black.py -f '/path/to/your/directory' -d -s 0.1 -t 0.99
```

In this example:

- `-f '/path/to/your/directory'` specifies the directory containing your CCTV video files.
- `-d` specifies that you want to delete empty video files after evaluation.
- `-s 0.1` specifies the sampling rate, meaning the script will check 10% of the frames.
- `-t 0.99` specifies the threshold for determining if a video is empty, meaning 99% of the sampled frames must be black for the video to be considered empty.

### Detailed Steps

1. Set up the Python environment: Ensure you have Python 3.x installed on your system. Install the required packages using pip.
2. Prepare the directory: Place all your CCTV video files in a directory. Note the path to this directory.
3. Run the script: Use the command-line interface to run the script with your desired parameters. For example:

    ```bash
    python check_video_black.py -f '/path/to/your/directory' -d -s 0.1 -t 0.99
    ```

4. Monitor the output: The script will process each video file in the specified directory, checking for mostly black frames. It will display progress and log the status of each video.
5. Check logs: The script maintains a log file (video_processing_log.json) to track processed files. This log helps resume operations if the script is interrupted.

### Notes

- Sampling Rate: Adjust the sampling rate (-s) based on your performance needs and accuracy requirements. A higher sampling rate checks more frames but takes longer to process.
- Threshold: Adjust the threshold (-t) to define what proportion of black frames constitutes an empty video. The default is 0.99 (99%).
- Resumable Operations: If the script is interrupted, it can resume from the last processed file using the log file. Ensure the log file (video_processing_log.json) is in the same directory as the script.

## License

This project is licensed under the MIT License.

## Author
Erick Servin
@servin