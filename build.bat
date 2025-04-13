@echo off
echo ====================================
echo      Python EXE 自動打包工具
echo ====================================

:: 嘗試自動找 Python 路徑
set PYTHON_EXE=python

:: 檢查 PyInstaller 是否安裝
%PYTHON_EXE% -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller 未安裝，正在安裝中...
    %PYTHON_EXE% -m pip install pyinstaller
)

echo.
echo === 開始使用 main.spec 打包 ===
%PYTHON_EXE% -m PyInstaller main.spec

echo.
echo === 打包完成！EXE 應該在 dist\ScreenTranslator\ScreenTranslator.exe ===
pause
