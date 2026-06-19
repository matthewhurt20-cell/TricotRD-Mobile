#!/bin/bash
# Tricot R&D Platform — Linux Launcher
cd "$(dirname "$0")"
echo ""
echo "================================================"
echo "  Tricot R&D Platform — Warp Knitting Simulator"
echo "================================================"
echo ""

if command -v python3 &>/dev/null; then
    python3 launch_app.py
elif command -v python &>/dev/null; then
    python launch_app.py
else
    echo "Python not found. Opening directly in browser..."
    xdg-open TricotRD.html 2>/dev/null || firefox TricotRD.html 2>/dev/null || google-chrome TricotRD.html
fi
