#!/bin/bash
# Shell script to run the Streamlit app on Linux/Mac

echo "Starting Logistics Multi-Agent System UI..."
echo ""

# Check if .env file exists
if [ ! -f .env ]; then
    echo "WARNING: .env file not found!"
    echo "Please create a .env file with your ANTHROPIC_API_KEY"
    echo ""
fi

# Run streamlit
streamlit run streamlit_app.py

