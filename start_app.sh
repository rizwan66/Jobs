#!/bin/bash

# Start script for German Job Portal Scanner
# Handles port conflicts and starts the app cleanly

echo "================================================"
echo "German Job Portal Scanner"
echo "================================================"
echo ""

# Default port
PORT=8501

# Check if port is in use
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo "⚠️  Port $PORT is already in use"
    echo ""

    # Find the process using the port
    PID=$(lsof -ti:$PORT)

    if [ ! -z "$PID" ]; then
        echo "Process ID: $PID"
        echo ""
        read -p "Do you want to kill this process and start fresh? (y/n): " choice

        if [ "$choice" = "y" ] || [ "$choice" = "Y" ]; then
            echo "Killing process $PID..."
            kill -9 $PID 2>/dev/null
            sleep 1
            echo "✅ Process killed"
            echo ""
        else
            # Use alternative port
            PORT=8502
            echo "Using alternative port: $PORT"
            echo ""
        fi
    fi
fi

# Start the app
echo "🚀 Starting app on port $PORT..."
echo ""
echo "The app will open in your browser automatically."
echo "If not, open: http://localhost:$PORT"
echo ""
echo "Press Ctrl+C to stop the app"
echo ""
echo "================================================"
echo ""

# Run streamlit
if [ "$PORT" = "8501" ]; then
    streamlit run app.py
else
    streamlit run app.py --server.port=$PORT
fi
