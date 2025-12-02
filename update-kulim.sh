#!/bin/bash
# Update Kulim Dashboard Command
# Usage: ./update-kulim.sh [optional: JSON data]

echo "================================================================================"
echo "KULIM DASHBOARD UPDATE"
echo "================================================================================"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "ERROR: Python not found. Please install Python."
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Run the update script
if [ -z "$1" ]; then
    echo "Running update script (no data provided - will show query)..."
    $PYTHON_CMD update_kulim.py
else
    echo "Running update script with provided data..."
    $PYTHON_CMD update_kulim.py "$1"
fi

echo ""
echo "================================================================================"


