@echo off
echo ============================================
echo  SafeBank AI - With Authentication
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
echo Starting SafeBank AI with Authentication...
echo.
echo Access the application at: http://localhost:8501
echo Press Ctrl+C to stop the server
echo.

REM Run the authenticated Streamlit app
streamlit run app_with_auth.py --server.port 8501 --server.address localhost

pause
