@echo off
REM Batch script to run the Streamlit app on Windows

echo Starting Logistics Multi-Agent System UI...
echo.

REM Check if .env file exists
if not exist .env (
    echo WARNING: .env file not found!
    echo Please create a .env file with your ANTHROPIC_API_KEY
    echo.
)

REM Run streamlit
streamlit run streamlit_app.py

pause

