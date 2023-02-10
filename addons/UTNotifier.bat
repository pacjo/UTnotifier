@echo OFF
SET mypath=%~dp0
echo %mypath%
cd mypath
cd..
python UTnotifier.py -dh
pause