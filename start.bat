@echo off
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "Start-Process py -ArgumentList 'main.py' -Verb RunAs"
