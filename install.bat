@echo off
chcp 65001 >nul
title GiWiFi Auto Login - Install

:: Get the folder where this batch file lives
set "SCRIPT_DIR=%~dp0"

:: Check admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo 请右键选择"以管理员身份运行"
    echo Press any key to exit...
    pause >nul
    exit /b 1
)

:: Remove old task if exists
schtasks /query /tn "GiWiFi Auto Login" >nul 2>&1
if %errorlevel% equ 0 (
    schtasks /delete /tn "GiWiFi Auto Login" /f >nul 2>&1
    echo 已删除旧任务
)

:: Create scheduled task - runs at user logon
schtasks /create /tn "GiWiFi Auto Login" /tr "wscript.exe \"%SCRIPT_DIR%auto_login_launcher.vbs\"" /sc onlogon /ru "%USERDOMAIN%\%USERNAME%" /it /f >nul 2>&1

if %errorlevel% equ 0 (
    echo.
    echo ==========================================
    echo   GiWiFi 自动登录 安装成功！
    echo ==========================================
    echo.
    echo 下次开机会自动在后台运行。
    echo.
    echo 现在启动中...
    start /min "" wscript.exe "%SCRIPT_DIR%auto_login_launcher.vbs"
    echo 已启动！
) else (
    echo 安装失败，请重试。
)

echo.
echo Press any key to exit...
pause >nul
