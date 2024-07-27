#!/bin/bash

# Create a virtual environment
python3 -m venv face_detection_env

# Activate the virtual environment
source face_detection_env/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install opencv-python tqdm

# Download the required face detection model files
MODEL_DIR="models"
mkdir -p $MODEL_DIR

# URLs for the model files
PROTOTXT_URL="https://raw.githubusercontent.com/opencv/opencv/master/samples/dnn/face_detector/deploy.prototxt"
CAFFEMODEL_URL="https://github.com/opencv/opencv_3rdparty/raw/dnn_samples_face_detector_20170830/res10_300x300_ssd_iter_140000.caffemodel"

# Download deploy.prototxt
curl -L -o $MODEL_DIR/deploy.prototxt $PROTOTXT_URL

# Download res10_300x300_ssd_iter_140000.caffemodel
curl -L -o $MODEL_DIR/res10_300x300_ssd_iter_140000_fp16.caffemodel $CAFFEMODEL_URL

echo "Setup completed. Virtual environment created and dependencies installed."
echo "To activate the virtual environment, run: source face_detection_env/bin/activate"