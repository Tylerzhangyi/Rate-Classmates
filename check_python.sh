#!/bin/bash

# Python 和 Django 诊断脚本

echo "🔍 检查 Python 和 Django 安装情况..."
echo ""

# 检查各个 Python 版本
for py_cmd in python3.9 python3.11 python3.10 python3.8 python3 python; do
    if command -v $py_cmd &> /dev/null; then
        echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
        echo "🐍 $py_cmd"
        echo "   版本: $($py_cmd --version 2>&1)"
        echo "   路径: $(which $py_cmd)"
        
        # 检查 Django
        if $py_cmd -c "import django" 2>/dev/null; then
            DJANGO_VERSION=$($py_cmd -c "import django; print(django.get_version())" 2>/dev/null)
            echo "   ✅ Django 已安装: $DJANGO_VERSION"
        else
            echo "   ❌ Django 未安装"
        fi
        
        # 检查 pip
        if command -v "${py_cmd%3.9}pip3.9" &> /dev/null; then
            PIP_CMD="${py_cmd%3.9}pip3.9"
        elif command -v "${py_cmd%3}pip3" &> /dev/null; then
            PIP_CMD="${py_cmd%3}pip3"
        else
            PIP_CMD="$py_cmd -m pip"
        fi
        echo "   📦 pip 命令: $PIP_CMD"
        echo ""
    fi
done

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
echo "💡 建议："
echo "   如果 Django 安装在 python3.9 中，请确保使用 python3.9 运行项目"
echo "   或者使用虚拟环境："
echo "   cd backend"
echo "   python3.9 -m venv .venv"
echo "   source .venv/bin/activate"
echo "   pip install -r requirements.txt"

