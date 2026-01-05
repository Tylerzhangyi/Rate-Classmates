#!/bin/bash

# Rate My Classmate - 一键启动脚本
# 同时启动前端和后端服务

echo "🚀 正在启动 Rate My Classmate..."
echo ""

# 检查是否在项目根目录
if [ ! -f "package.json" ] || [ ! -d "backend" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 检查 Node.js 是否安装
if ! command -v node &> /dev/null; then
    echo "❌ 错误: 未找到 Node.js，请先安装 Node.js"
    exit 1
fi

# 检查 Python3 是否安装
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3，请先安装 Python3"
    exit 1
fi

# 检查 node_modules 是否存在
if [ ! -d "node_modules" ]; then
    echo "📦 正在安装前端依赖..."
    npm install
fi

# 检查并清理端口占用
echo "🔍 检查端口占用情况..."

# 清理端口 5002（前端）和 5001（后端）
clean_port() {
    local port=$1
    local pids
    
    # 尝试使用 lsof
    if command -v lsof &> /dev/null; then
        pids=$(lsof -ti:$port 2>/dev/null)
        if [ ! -z "$pids" ]; then
            echo "⚠️  端口 $port 被占用，正在清理进程: $pids"
            echo "$pids" | xargs kill -9 2>/dev/null
            sleep 2
        fi
    fi
    
    # 尝试使用 fuser（如果可用）
    if command -v fuser &> /dev/null; then
        fuser -k $port/tcp 2>/dev/null
        sleep 1
    fi
    
    # 尝试使用 netstat + kill
    if command -v netstat &> /dev/null; then
        pids=$(netstat -tulpn 2>/dev/null | grep ":$port " | awk '{print $7}' | cut -d'/' -f1 | grep -v '-' | sort -u)
        if [ ! -z "$pids" ]; then
            echo "⚠️  端口 $port 被占用，正在清理进程: $pids"
            echo "$pids" | xargs kill -9 2>/dev/null
            sleep 2
        fi
    fi
    
    # 验证端口是否已释放
    if command -v lsof &> /dev/null; then
        if lsof -ti:$port > /dev/null 2>&1; then
            echo "❌ 警告: 端口 $port 仍被占用，请手动清理"
            return 1
        else
            echo "✅ 端口 $port 已释放"
        fi
    fi
}

clean_port 5002
clean_port 5001

# 启动函数
cleanup() {
    echo ""
    echo "🛑 正在停止服务..."
    kill $FRONTEND_PID $BACKEND_PID 2>/dev/null
    exit 0
}

# 捕获中断信号
trap cleanup SIGINT SIGTERM

# 启动后端
echo "🔧 启动后端服务 (Django)..."
cd backend
python3 manage.py runserver 0.0.0.0:5001 > /dev/null 2>&1 &
BACKEND_PID=$!
cd ..

# 等待后端启动
sleep 2

# 启动前端
echo "🎨 启动前端服务 (Vite)..."
npm run dev &
FRONTEND_PID=$!

echo ""
echo "✅ 服务已启动！"
echo "📱 前端地址: http://0.0.0.0:5002"
echo "🔧 后端地址: http://0.0.0.0:5001"
echo ""
echo "按 Ctrl+C 停止所有服务"
echo ""

# 等待进程
wait

