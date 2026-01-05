#!/bin/bash

# 安装项目依赖脚本

echo "📦 安装项目依赖..."
echo ""

# 检查是否在项目根目录
if [ ! -f "package.json" ] || [ ! -d "backend" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 安装前端依赖
echo "1️⃣ 安装前端依赖 (Node.js)..."
if [ ! -d "node_modules" ]; then
    npm install
else
    echo "   ✅ node_modules 已存在，跳过"
fi

echo ""
echo "2️⃣ 安装后端依赖 (Python)..."
cd backend

# 检查虚拟环境
if [ -d ".venv" ]; then
    echo "   📦 检测到虚拟环境，激活中..."
    source .venv/bin/activate 2>/dev/null || true
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
else
    echo "   ℹ️  未检测到虚拟环境，使用系统 Python"
    PYTHON_CMD="python3"
    PIP_CMD="pip3"
fi

# 检查 requirements.txt
if [ -f "requirements.txt" ]; then
    echo "   📋 从 requirements.txt 安装依赖..."
    $PIP_CMD install -r requirements.txt
    if [ $? -eq 0 ]; then
        echo "   ✅ 后端依赖安装完成"
    else
        echo "   ❌ 后端依赖安装失败"
        cd ..
        exit 1
    fi
else
    echo "   ⚠️  未找到 requirements.txt"
    echo "   📦 手动安装 Django..."
    $PIP_CMD install "Django>=4.2,<5"
fi

cd ..

echo ""
echo "✅ 所有依赖安装完成！"
echo ""
echo "现在可以运行 ./start.sh 启动服务"

