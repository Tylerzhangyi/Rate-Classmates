#!/bin/bash

# 后端服务诊断脚本

echo "🔍 检查后端服务状态..."
echo ""

# 检查端口 5001 是否在监听
echo "1️⃣ 检查端口 5001 监听状态："
if command -v lsof &> /dev/null; then
    if lsof -ti:5001 > /dev/null 2>&1; then
        echo "✅ 端口 5001 正在监听"
        echo "   进程信息："
        lsof -i:5001 | grep LISTEN
    else
        echo "❌ 端口 5001 未监听"
    fi
elif command -v netstat &> /dev/null; then
    if netstat -tuln 2>/dev/null | grep -q ":5001 "; then
        echo "✅ 端口 5001 正在监听"
        netstat -tulpn 2>/dev/null | grep ":5001 "
    else
        echo "❌ 端口 5001 未监听"
    fi
else
    echo "⚠️  无法检查端口状态（需要 lsof 或 netstat）"
fi

echo ""
echo "2️⃣ 检查 Django 进程："
ps aux | grep -E "manage.py runserver|python.*runserver" | grep -v grep || echo "❌ 未找到 Django 进程"

echo ""
echo "3️⃣ 测试后端连接："
if command -v curl &> /dev/null; then
    echo "   测试 http://localhost:5001/api/auth/login"
    curl -s -o /dev/null -w "   HTTP 状态码: %{http_code}\n" http://localhost:5001/api/auth/login || echo "   ❌ 连接失败"
else
    echo "   ⚠️  curl 未安装，无法测试连接"
fi

echo ""
echo "4️⃣ 检查后端日志（如果存在）："
if [ -f "backend.log" ]; then
    echo "   最近 10 行日志："
    tail -10 backend.log
else
    echo "   ℹ️  未找到 backend.log 文件"
fi

echo ""
echo "5️⃣ 手动启动后端（如果未运行）："
echo "   cd backend"
echo "   python3 manage.py runserver 0.0.0.0:5001"

