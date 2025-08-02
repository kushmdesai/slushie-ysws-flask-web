#!/bin/bash

echo "Starting process..."

# --- Argument and Port Validation ---
# Exit if no port number is provided.
if [ "$#" -ne 1 ]; then
  echo "Parameter required: PORT"
  echo "Usage: ./setup.sh <PORT>"
  exit 1
fi

PORT="$1"

# Exit if the port is not a non-negative integer.
if ! [[ "$PORT" =~ ^[0-9]+$ ]]; then
  echo "PORT must be a non-negative integer."
  exit 1
fi

# --- Check and Kill Existing Process ---
# Kill any process currently using the specified port.
# The 'timeout' command prevents the script from getting stuck if lsof hangs.
echo "Checking for existing processes on port $PORT..."
PIDS=$(timeout 2s lsof -ti ":$PORT")
if [ -n "$PIDS" ]; then
  echo "Killing process(es) with PID: $PIDS"
  kill -9 $PIDS
fi

# --- Git Update ---
# Update code from GitHub repository.
echo "Pulling latest code from Git..."
if ! git pull; then
  echo "git pull failed. Please resolve any conflicts and try again."
  exit 1
fi

# --- Virtual Environment Setup and Dependencies ---
# Create virtual environment and install dependencies.
echo "Setting up virtual environment and installing dependencies..."
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# --- Start the Flask App with Gunicorn ---
# Use 'nohup' to run Gunicorn in the background and log output.
# The '&' at the end detaches the process from the terminal.
echo "✅ Installation done. Starting gunicorn..."
nohup gunicorn -w 1 -b 0.0.0.0:$1 app:app --log-level debug > gunicorn.log 2>&1 &

echo "Gunicorn has been started in the background. Check gunicorn.log for output."
echo "You can view running processes with: ps aux | grep gunicorn"