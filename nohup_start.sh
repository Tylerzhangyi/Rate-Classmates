#!/bin/bash

# 使用 nohup 同时启动后端 (5001) 和前端 (8805)
# 运行方式：bash nohup_start.sh

ROOT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT_DIR"

BACKEND_LOG="$ROOT_DIR/backend.nohup.log"
FRONTEND_LOG="$ROOT_DIR/frontend.nohup.log"

echo "🚀 使用 nohup 启动 Rate My Classmate..."

# 清理端口占用
for port in 8805 5001; do
  if command -v lsof &> /dev/null && lsof -ti:$port > /dev/null 2>&1; then
    echo "⚠️  端口 $port 被占用，正在清理..."
    lsof -ti:$port | xargs kill -9 2>/dev/null
    sleep 1
  fi
done

# 启动后端
echo "🔧 启动后端 (Django)..."
cd backend
nohup python3.9 manage.py runserver 0.0.0.0:5001 > "$BACKEND_LOG" 2>&1 &
BACKEND_PID=$!
cd "$ROOT_DIR"

# 启动前端
echo "🎨 启动前端 (Vite，端口 8805)..."
nohup npm run dev > "$FRONTEND_LOG" 2>&1 &
FRONTEND_PID=$!

echo ""
echo "✅ 已启动（后台运行，SSH 退出后仍保持）："
echo "   后端 PID: $BACKEND_PID，日志: $BACKEND_LOG"
echo "   前端 PID: $FRONTEND_PID，日志: $FRONTEND_LOG"
echo ""
echo "访问地址："
echo "   前端: http://tyler.yunguhs.com:8805"
echo "   后端: http://tyler.yunguhs.com:5001"
echo ""
echo "停止：kill $BACKEND_PID $FRONTEND_PID"
echo "查看日志：tail -f $BACKEND_LOG 或 tail -f $FRONTEND_LOG"


