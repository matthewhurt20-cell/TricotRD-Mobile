#!/bin/bash
# Tricot R&D Platform — macOS Launcher
# Double-click this file to launch the app

cd "$(dirname "$0")"
echo ""
echo "================================================"
echo "  Tricot R&D Platform — Warp Knitting Simulator"
echo "================================================"
echo ""

if command -v python3 &>/dev/null; then
    echo "  Starting with Python3..."
    python3 launch_app.py
elif command -v python &>/dev/null; then
    echo "  Starting with Python..."
    python launch_app.py
else
    echo "  Python not found. Opening directly..."
    open TricotRD.html
fi
