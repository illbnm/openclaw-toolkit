#!/bin/bash
# OpenClaw Toolkit 一键安装脚本
# 作者: 贾维斯 (Jarvis)
# 捐赠: DdqsLbFK9kW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm (SOL)

set -e

echo "🦞 OpenClaw Toolkit 一键安装"
echo "================================"
echo ""

# 检查 Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 未安装，请先安装 Python 3.8+"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python: $PYTHON_VERSION"

# 检查 Node.js
if ! command -v node &> /dev/null; then
    echo "⚠️ Node.js 未安装，部分功能可能不可用"
else
    NODE_VERSION=$(node --version)
    echo "✅ Node.js: $NODE_VERSION"
fi

# 创建目录
TOOLKIT_DIR="$HOME/.openclaw-toolkit"
mkdir -p "$TOOLKIT_DIR"

echo ""
echo "📦 下载工具包..."

# 克隆或下载
if command -v git &> /dev/null; then
    git clone https://github.com/illbnm/openclaw-toolkit.git "$TOOLKIT_DIR" 2>/dev/null || {
        echo "⚠️ 克隆失败，使用本地文件"
    }
else
    echo "⚠️ Git 未安装，跳过克隆"
fi

echo ""
echo "⚙️ 安装依赖..."
pip3 install -q requests python-dotenv 2>/dev/null || true

echo ""
echo "✅ 安装完成！"
echo ""
echo "使用方法:"
echo "  cd $TOOLKIT_DIR"
echo "  python3 installer.py --install    # 一键部署 OpenClaw"
echo "  python3 proxy_monitor.py --check  # 检测中转站质量"
echo "  python3 cost_monitor.py           # 监控成本"
echo ""
echo "☕ 如果这个工具有帮助，请捐杯咖啡:"
echo "   SOL: DdqsLbFK9kW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm"
