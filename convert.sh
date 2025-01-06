#!/usr/bin/env bash
set -e

usage() {
    echo "Usage: $0 SOURCE_DIRECTORY TARGET_DIRECTORY"
    echo
    echo "Arguments:"
    echo "  SOURCE_DIRECTORY   Path to the directory containing files to process."
    echo "  TARGET_DIRECTORY   Path to the directory where processed files will be saved."
    echo
    echo "Description:"
    echo "  This script activates a Python virtual environment, removes unwanted '.DS_Store' files"
    echo "  from the source directory, and processes files using the Python 'convert_to_jpegxl.py' script."
    echo
    echo "Example:"
    echo "  $0 tmp/source tmp/converted"
    exit 1
}

# Check arguments
if [[ $# -ne 2 ]]; then
    echo "Error: Invalid number of arguments."
    usage
fi

SOURCE_DIR="$1"
TARGET_DIR="$2"

# Ensure source directory exists
if [[ ! -d "$SOURCE_DIR" ]]; then
    echo "Error: Source directory '$SOURCE_DIR' does not exist."
    exit 1
fi

# Ensure target directory does not exist to avoid overwriting
if [[ -d "$TARGET_DIR" ]]; then
    echo "Error: Target directory '$TARGET_DIR' already exists."
    exit 1
fi

# Activate the virtual environment
VENV_DIR=${VENV_DIR:-venv}

if [[ ! -f "$VENV_DIR/bin/activate" ]]; then
    echo "Error: Virtual environment not found. Please create one in '$VENV_DIR/'."
    exit 1
fi
source "$VENV_DIR/bin/activate"

# Remove unwanted files
find "$SOURCE_DIR" -name '.DS_Store' -exec rm {} \;

# Run the Python script
if python3 convert_to_jpegxl.py "$SOURCE_DIR" "$TARGET_DIR" --move; then
    echo "File processing completed successfully."
else
    echo "Error during file processing."
    exit 1
fi