@echo off
REM Automatically run log_analyzer.py with default keywords and today's date

REM Get today's date in YYYY-MM-DD format (Windows batch)
for /f %%a in ('powershell -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set TODAY=%%a

REM Run Python script with --date parameter set to today
REM No keywords passed so the script uses default keywords automatically
python log_analyzer.py --date %TODAY%

pause
