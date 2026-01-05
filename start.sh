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
    # 清理日志文件
    rm -f backend.log 2>/dev/null
    exit 0
}

# 捕获中断信号
trap cleanup SIGINT SIGTERM

# 启动后端
echo "🔧 启动后端服务 (Django)..."
cd backend

# 检测可用的 Python 版本（优先使用 python3.9）
detect_python() {
    for cmd in python3.9 python3.11 python3.10 python3.8 python3 python; do
        if command -v $cmd &> /dev/null; then
            # 检查这个 Python 是否有 Django
            if $cmd -c "import django" 2>/dev/null; then
                echo "$cmd"
                return 0
            fi
        fi
    done
    # 如果都没 Django，返回第一个可用的
    for cmd in python3.9 python3.11 python3.10 python3.8 python3 python; do
        if command -v $cmd &> /dev/null; then
            echo "$cmd"
            return 0
        fi
    done
    echo "python3"
}

# 检查虚拟环境是否存在
if [ -d ".venv" ]; then
    echo "📦 检测到虚拟环境，激活中..."
    source .venv/bin/activate 2>/dev/null || true
    PYTHON_CMD=$(detect_python)
    PIP_CMD="${PYTHON_CMD} -m pip"
else
    PYTHON_CMD=$(detect_python)
    # 尝试找到对应的 pip
    if command -v "${PYTHON_CMD%3.9}pip3.9" &> /dev/null; then
        PIP_CMD="${PYTHON_CMD%3.9}pip3.9"
    elif command -v "${PYTHON_CMD%3}pip3" &> /dev/null; then
        PIP_CMD="${PYTHON_CMD%3}pip3"
    else
        PIP_CMD="${PYTHON_CMD} -m pip"
    fi
fi

echo "🐍 使用 Python: $PYTHON_CMD"
echo "📦 使用 pip: $PIP_CMD"

# 检查并安装 Python 依赖
echo "📦 检查 Python 依赖..."
if [ -f "requirements.txt" ]; then
    # 检查 Django 是否已安装
    if ! $PYTHON_CMD -c "import django" 2>/dev/null; then
        echo "⚠️  Django 未安装，正在安装依赖..."
        $PIP_CMD install -r requirements.txt || {
            echo "❌ 依赖安装失败，请手动执行: $PIP_CMD install -r backend/requirements.txt"
            cd ..
            exit 1
        }
        echo "✅ 依赖安装完成"
    else
        DJANGO_VERSION=$($PYTHON_CMD -c "import django; print(django.get_version())" 2>/dev/null)
        echo "✅ Python 依赖已就绪 (Django $DJANGO_VERSION)"
    fi
else
    echo "⚠️  未找到 requirements.txt，跳过依赖检查"
fi

# 启动后端并保存日志
echo "🚀 启动 Django 服务器 (使用 $PYTHON_CMD)..."
$PYTHON_CMD manage.py runserver 0.0.0.0:5001 > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# 等待后端启动并验证
echo "⏳ 等待后端启动..."
sleep 3

# 检查后端是否成功启动
if ! kill -0 $BACKEND_PID 2>/dev/null; then
    echo "❌ 后端启动失败！"
    echo "📋 后端日志："
    tail -20 backend.log 2>/dev/null || echo "无法读取日志文件"
    exit 1
fi

# 检查端口是否在监听
if command -v lsof &> /dev/null; then
    if lsof -ti:5001 > /dev/null 2>&1; then
        echo "✅ 后端服务已启动 (PID: $BACKEND_PID)"
    else
        echo "⚠️  警告: 后端进程存在但端口 5001 未监听"
        echo "📋 后端日志："
        tail -20 backend.log 2>/dev/null || echo "无法读取日志文件"
    fi
else
    echo "✅ 后端进程已启动 (PID: $BACKEND_PID)"
fi

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

