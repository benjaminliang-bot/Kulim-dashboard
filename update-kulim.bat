@echo off
REM Update Kulim Dashboard Command
REM Usage: update-kulim [optional: JSON data]

echo ================================================================================
echo KULIM DASHBOARD UPDATE
echo ================================================================================
echo.

REM Check if Python is available
where py >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo ERROR: Python not found. Please install Python or add it to PATH.
    pause
    exit /b 1
)

REM Run the update script
if "%1"=="" (
    echo Running update script (no data provided - will show query)...
    py update_kulim.py
) else (
    echo Running update script with provided data...
    py update_kulim.py "%1"
)

echo.
echo ================================================================================
pause

