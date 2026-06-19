@echo off
title Tricot R&D Platform
echo.
echo  ================================================
echo    Tricot R&D Platform — Warp Knitting Simulator
echo  ================================================
echo.

REM Try Python launcher first (best experience)
python --version >nul 2>&1
if %errorlevel% == 0 (
    echo  Starting with Python launcher...
    python launch_app.py
    goto end
)

python3 --version >nul 2>&1
if %errorlevel% == 0 (
    echo  Starting with Python3 launcher...
    python3 launch_app.py
    goto end
)

REM Fallback: open HTML directly in browser
echo  Python not found. Opening directly in browser...
echo  Note: AI analysis requires internet access.
start "" "%~dp0TricotRD.html"

:end
