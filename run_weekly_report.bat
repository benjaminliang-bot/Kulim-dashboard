@echo off
REM Weekly Report Automation Script
REM This batch file runs the weekly report Python script

cd /d "%~dp0"
py process_and_send_weekly_report.py >> weekly_report.log 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [%date% %time%] Weekly report executed successfully >> weekly_report.log
) else (
    echo [%date% %time%] Weekly report failed with error code %ERRORLEVEL% >> weekly_report.log
)

exit /b %ERRORLEVEL%

