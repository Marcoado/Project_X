@echo off
setlocal
cd /d %~dp0
if not exist scripts\build_exe.ps1 (
  echo ERRO: scripts\build_exe.ps1 nao encontrado.
  pause
  exit /b 1
)
powershell -ExecutionPolicy Bypass -NoProfile -File .\scripts\build_exe.ps1 -Gui -Name Timerzone %*
if %errorlevel% neq 0 (
  echo Houve um erro durante o build. Veja as mensagens acima.
  pause
  exit /b %errorlevel%
)
echo.
echo Build concluido. O executavel esta na pasta dist\
pause


