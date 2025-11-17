@echo off
echo ============================================
echo  SafeBank AI - Chat Assistant
echo ============================================
echo.

REM Activate virtual environment if it exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Warning: Virtual environment not found
    echo Using system Python...
)

echo.
echo Starting SafeBank AI Chat Assistant...
echo.
echo Access the chat at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

REM Run the chat app
streamlit run chat_app.py --server.port 8501 --server.address localhost

pause
