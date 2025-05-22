@echo off
REM Set Python path
SET PYTHON_PATH="C:\Users\DELL\AppData\Local\Programs\Python\Python313\python.exe"

REM Set folder where the script is
SET SCRIPT_DIR="C:\Users\DELL\Desktop\LogMonitor"

REM Move to that folder
cd /d %SCRIPT_DIR%

REM Run the Python script (no quotes needed here around script name)
%PYTHON_PATH% log_analyzer.py --keywords error,fail,critical
