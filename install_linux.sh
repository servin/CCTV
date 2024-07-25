#!/bin/bash

# Function to check if a command exists
command_exists () {
    command -v "$1" >/dev/null 2>&1 ;
}

# Check for Python 3
if ! command_exists python3; then
    echo "Python 3 is not installed. Please install Python 3 and rerun this script."
    exit 1
fi

# Create a virtual environment
echo "Creating virtual environment..."
python3 -m venv venv

# Activate the virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install required Python packages
echo "Installing required Python packages..."
pip install opencv-python numpy tqdm

# Check for ffmpeg
if ! command_exists ffmpeg; then
    echo "ffmpeg is not installed. Installing ffmpeg..."
    if command_exists apt-get; then
        sudo apt-get update
        sudo apt-get install ffmpeg -y
    elif command_exists brew; then
        brew install ffmpeg
    else
        echo "Please install ffmpeg manually."
        exit 1
    fi
else
    echo "ffmpeg is already installed."
fi

# Print success message
echo "Setup complete. To activate the virtual environment, run 'source venv/bin/activate'."