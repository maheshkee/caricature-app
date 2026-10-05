#!/bin/bash
set -e

echo "========================================="
echo "   AI Doppelgänger Hub - Setup Script    "
echo "========================================="

echo "[1/4] Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "Python 3 could not be found. Please install Python 3."
    exit 1
fi

echo "[2/4] Creating virtual environment (venv)..."
python3 -m venv venv

echo "[3/4] Activating virtual environment & installing dependencies..."
source venv/bin/activate
# Install PyTorch CPU directly to save massive amounts of disk space (avoids CUDA downloads)
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu
# Install remaining requirements
pip install -r requirements.txt

echo "[4/4] Setup Complete!"
echo "-----------------------------------------"
echo "To start the application, run:"
echo "  source venv/bin/activate"
echo "  python app.py"
echo "-----------------------------------------"
