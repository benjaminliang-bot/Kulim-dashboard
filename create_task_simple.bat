@echo off
REM Simple batch file to create scheduled task using schtasks command
REM This may work without full admin privileges in some cases

set TASK_NAME=Weekly OC Performance Report
set SCRIPT_PATH=%~dp0run_weekly_report.bat
set WORK_DIR=%~dp0

echo Creating scheduled task: %TASK_NAME%
echo Script: %SCRIPT_PATH%
echo.

REM Remove existing task if it exists
schtasks /Delete /TN "%TASK_NAME%" /F 2>nul

REM Create new task (runs every Monday at 9:00 AM)
schtasks /Create /TN "%TASK_NAME%" ^
    /TR "\"%SCRIPT_PATH%\"" ^
    /SC WEEKLY ^
    /D MON ^
    /ST 09:00 ^
    /RU "%USERNAME%" ^
    /RL HIGHEST ^
    /F

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ✅ Scheduled task created successfully!
    echo.
    echo Task Details:
    echo   Name: %TASK_NAME%
    echo   Schedule: Every Monday at 9:00 AM
    echo   Script: %SCRIPT_PATH%
    echo.
    echo To view the task:
    echo   Open Task Scheduler and look for "%TASK_NAME%"
    echo.
    echo To test the task:
    echo   schtasks /Run /TN "%TASK_NAME%"
    echo.
) else (
    echo.
    echo ❌ Failed to create scheduled task.
    echo.
    echo This may require Administrator privileges.
    echo Please run this batch file as Administrator:
    echo   1. Right-click this file
    echo   2. Select "Run as administrator"
    echo.
    pause
)

