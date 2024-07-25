## CCTV Video Processing Script

This script processes CCTV video files in a specified directory to determine if they are mostly empty (black) and optionally deletes empty videos. It also supports motion detection in videos.

### Setup Instructions

1. **Clone the Repository**

   Clone the repository to your local machine:

   ```sh
   git clone https://github.com/yourusername/CCTV.git
   cd CCTV
   ```

2. **Create and Activate a Virtual Environment**

   Create and activate a virtual environment to manage dependencies:

   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Required Packages**

   Install the required Python packages using the provided `install.sh` script:

   ```sh
   chmod +x install.sh
   ./install.sh
   ```

   Alternatively, you can manually install the required packages:

   ```sh
   pip install opencv-python numpy tqdm
   ```

4. **Ensure `ffmpeg` is Installed**

   The script requires `ffmpeg` for processing videos. If it's not installed, you can install it using Homebrew:

   ```sh
   brew install ffmpeg
   ```

### Usage

The script can be run with default values or with customized parameters for sample rate, threshold, and whether to delete empty videos.

#### Default Usage

To process a directory with default values:

```sh
python check_video_black.py /path/to/directory
```

#### Custom Usage

To customize the sample rate, threshold, and delete empty videos:

```sh
python check_video_black.py /path/to/directory --delete --sample_rate 0.2 --threshold 0.95
```

### Parameters

- `directory`: (required) The path to the directory containing CCTV video files.
- `--delete`: (optional) Delete empty video files after evaluation. This flag does not require a value.
- `--sample_rate`: (optional) Sampling rate for checking frames (default: 0.1). Specifies the fraction of frames to be sampled.
- `--threshold`: (optional) Threshold for determining if a video is empty (default: 0.99). Specifies the ratio of black frames required to consider the video empty.

### Script Explanation

1. **Imports and Constants**

   The script imports necessary modules and defines constants.

2. **Functions**

   - `is_frame_mostly_black(frame, threshold)`: Determines if a frame is mostly black.
   - `check_video_black(video_path, sample_rate, threshold)`: Checks if a video is mostly black by sampling frames.
   - `save_progress(log)`: Saves the progress log to a JSON file.
   - `load_progress()`: Loads the progress log from a JSON file.
   - `process_directory(directory_path, delete_empty, sample_rate, threshold)`: Processes all video files in the specified directory.

3. **Main Function**

   The `main()` function sets up argument parsing and calls `process_directory()` with the appropriate parameters.

### Example

#### Process a Directory with Default Values

```sh
python check_video_black.py /Volumes/CCTV/
```

#### Process a Directory with Custom Values and Delete Empty Videos

```sh
python check_video_black.py /Volumes/CCTV/ --delete --sample_rate 0.2 --threshold 0.95
```

### Additional Notes

- The script logs the progress and processed files in a JSON file named `video_processing_log.json` in the current directory.
- The script skips already processed videos based on the log file to avoid redundant processing.

### Troubleshooting

If you encounter issues with missing modules, ensure that the virtual environment is activated and the required packages are installed:

```sh
source venv/bin/activate
pip install -r requirements.txt
```

If `ffmpeg` is not found, ensure it is installed and available in your system's PATH. For macOS, you can install it using Homebrew:

```sh
brew install ffmpeg
```

---

This documentation should provide a comprehensive guide to setting up, running, and customizing the CCTV video processing script.