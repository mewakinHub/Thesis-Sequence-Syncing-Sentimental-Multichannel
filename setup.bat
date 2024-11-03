@echo off
setlocal

REM Define a log file for output
set LOGFILE=setup_log.txt

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

@REM REM Temporarily change PowerShell execution policy to allow the script to run
@REM powershell -Command "Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass -Force"

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
call "%CONDA_EXE%" activate bag-detection

REM Confirm the environment was activated
IF NOT "%CONDA_DEFAULT_ENV%"=="bag-detection" (
    echo Conda environment 'bag-detection' activated successfully.
    echo Conda environment 'bag-detection' activated successfully. >> %LOGFILE%
) ELSE (
    echo Conda environment 'bag-detection' is not activated. Please activate it before proceeding.
    echo Conda environment 'bag-detection' is not activated. >> %LOGFILE%
    pause
    exit /b 1
)

REM ---------- Conda setup completed! ---------------------

REM Proceed with the setup process
echo Checking for CUDA Toolkit pre-installation...
nvcc --version
IF ERRORLEVEL 1 (
    echo CUDA Toolkit is not installed. Please install CUDA 12.1 Toolkit before proceeding.
    echo CUDA Toolkit is not installed. >> %LOGFILE%
    pause
    exit /b 1
) ELSE (
    echo CUDA Toolkit is installed.
    echo CUDA Toolkit is installed. >> %LOGFILE%
)

REM Install Matplotlib using Conda
echo Installing Matplotlib using Conda...
echo Installing Matplotlib using Conda... >> %LOGFILE%
call conda install matplotlib -y >> %LOGFILE% 2>&1

REM Check if Conda installation was successful
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install Matplotlib using Conda. Please check the setup_log.txt file for details.
    echo Failed to install Matplotlib using Conda. Please check the setup_log.txt file for details. >> %LOGFILE%
    pause
    exit /b 1
)

REM Continue to the next step if Matplotlib installation succeeded
echo Matplotlib installation completed. Continuing with the script...
echo Matplotlib installation completed. Continuing with the script... >> %LOGFILE%

REM Install Cython for scikit-learn dependencies
echo Installing Cython for scikit-learn dependencies...
echo Installing Cython for scikit-learn dependencies... >> %LOGFILE%
call conda install cython -y >> %LOGFILE% 2>&1

REM Check if Cython installation was successful
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install Cython. Please check the setup_log.txt file for details.
    echo Failed to install Cython. Please check the setup_log.txt file for details. >> %LOGFILE%
    pause
    exit /b 1
)

REM Install PyTorch with CUDA support
echo Installing PyTorch with CUDA 12.1 support...
echo Installing PyTorch with CUDA 12.1 support... >> %LOGFILE%
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu121 >> %LOGFILE% 2>&1

REM Check if PyTorch installation was successful
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install PyTorch. Please check the setup_log.txt file for details.
    echo Failed to install PyTorch. Please check the setup_log.txt file for details. >> %LOGFILE%
    pause
    exit /b 1
)

REM Install remaining Python packages from requirements.txt
echo Installing Python packages from requirements.txt...
echo Installing Python packages from requirements.txt... >> %LOGFILE%
pip install -r requirements.txt >> %LOGFILE% 2>&1

REM Check if Pip installation was successful
if %ERRORLEVEL% NEQ 0 (
    echo Failed to install some Python packages. Please check the setup_log.txt file for details.
    echo Failed to install some Python packages. Please check the setup_log.txt file for details. >> %LOGFILE%
    pause
    exit /b 1
)

REM Ensure the pre-trained model is in place
echo Setup complete. Please ensure the pre-trained model weight.pt is placed inside the assets/models directory.
echo Setup complete. Please ensure the pre-trained model weight.pt is placed inside the assets/models directory. >> %LOGFILE%
