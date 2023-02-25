@echo off

REM check if pip is installed
py -m pip -V >nul 2>&1
if errorlevel 1 (
    echo Installing pip...
    py -m ensurepip --default-pip >nul 2>&1
    if errorlevel 1 (
        echo Failed to install pip.
        exit /b 1
    )
) else (
    REM check if pip is up to date
    setlocal EnableDelayedExpansion
    for /f "tokens=3" %%v in ('py -m pip -V') do set pip_version=%%v
    set pip_version=!pip_version:~0,-1!
    py -m pip install --upgrade pip >nul 2>&1
    for /f "tokens=3" %%v in ('py -m pip -V') do set new_pip_version=%%v
    set new_pip_version=!new_pip_version:~0,-1!
    if "!pip_version!" equ "!new_pip_version!" (
        echo pip is up to date.
    ) else (
        echo Upgraded pip from !pip_version! to !new_pip_version!.
    )
)

echo pip is installed and up to date.
