@echo off
setlocal

REM Define a log file for output and a temporary file for intermediate output
set LOGFILE=run_log.txt
set TEMPFILE=temp_output.txt

REM Start logging
echo Log started at %date% %time% > %LOGFILE%

REM Attempt to find the Conda executable
FOR /f "tokens=* USEBACKQ" %%F IN (`where conda`) DO SET CONDA_EXE=%%F

REM Check if Conda was found
IF NOT DEFINED CONDA_EXE (
    echo Conda is not installed or not in the PATH. Please install Conda and add it to your PATH.
    echo Conda is not installed or not in the PATH. >> %LOGFILE%
    pause
    exit /b 1
)

REM Ensure Conda has been initialized (conda init)
call "%CONDA_EXE%" init cmd.exe >nul 2>&1

REM Check if Conda initialization was successful
IF ERRORLEVEL 1 (
    echo Conda initialization failed. Please run 'conda init' manually in your shell.
    echo Conda initialization failed. >> %LOGFILE%
    pause
    exit /b 1
)

REM Activate the Conda environment
call conda activate bag-detection
echo Activated Conda environment: %CONDA_DEFAULT_ENV% >> %LOGFILE%

REM Confirm the environment was activated
IF "%CONDA_DEFAULT_ENV%"=="bag-detection" (
    echo Conda environment 'bag-detection' activated successfully.
    echo Conda environment 'bag-detection' activated successfully. >> %LOGFILE%
) ELSE (
    echo Conda environment 'bag-detection' is not activated. Please activate it before proceeding.
    echo Conda environment 'bag-detection' is not activated. >> %LOGFILE%
    pause
    exit /b 1
)

REM ---------- Conda setup completed! ---------------------

REM Check if the model file exists
IF NOT EXIST "assets\models\best.pt" (
    echo Model file 'best.pt' not found in 'assets\models'. Please ensure the file is in the correct location.
    echo Model file 'best.pt' not found in 'assets\models'. >> %LOGFILE%
    pause
    exit /b 1
)

REM Start the application and capture output to a temporary file
echo Starting the application...
echo Starting the application... >> %LOGFILE%
python main.py > %TEMPFILE% 2>&1

REM Append the temporary output to the log file
type %TEMPFILE% >> %LOGFILE%

REM Display specific lines (like the ones you want) in the terminal
findstr /i /c:"Model loaded with class names:" /c:"INFO: Using device:" /c:"FutureWarning" /c:"INFO: Average Inference Time" /c:"INFO: Saved count bag results" /c:"95th Percentile Inference Time:" /c:"CUDA Available" /c:"Device Name" %TEMPFILE%

REM Clean up temporary file
del %TEMPFILE%

REM Check for errors during execution
if %ERRORLEVEL% NEQ 0 (
    echo The application encountered an error during execution. Please check the run_log.txt file for details.
    echo The application encountered an error during execution. Please check the run_log.txt file for details. >> %LOGFILE%
    echo Review CUDA installation and RTSP stream URL if necessary. >> %LOGFILE%
    pause
    exit /b 1
)

echo Application finished successfully.
echo Application finished successfully. >> %LOGFILE%
pause
