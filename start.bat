@echo off
REM Rate My Classmate - 一键启动脚本 (Windows)
REM 同时启动前端和后端服务

echo 🚀 正在启动 Rate My Classmate...
echo.

REM 检查是否在项目根目录
if not exist "package.json" (
    echo ❌ 错误: 请在项目根目录运行此脚本
    exit /b 1
)

if not exist "backend" (
    echo ❌ 错误: 请在项目根目录运行此脚本
    exit /b 1
)

REM 检查 Node.js 是否安装
where node >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 Node.js，请先安装 Node.js
    exit /b 1
)

REM 检查 Python 是否安装
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ 错误: 未找到 Python，请先安装 Python
    exit /b 1
)

REM 检查 node_modules 是否存在
if not exist "node_modules" (
    echo 📦 正在安装前端依赖...
    call npm install
)

echo 🔧 启动后端服务 (Django)...
start "Django Backend" cmd /k "cd backend && python manage.py runserver"

timeout /t 2 /nobreak >nul

echo 🎨 启动前端服务 (Vite)...
start "Vite Frontend" cmd /k "npm run dev"

echo.
echo ✅ 服务已启动！
echo 📱 前端地址: http://localhost:5173
echo 🔧 后端地址: http://localhost:8000
echo.
echo 关闭此窗口将停止所有服务
echo.

pause

