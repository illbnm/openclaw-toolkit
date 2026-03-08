# 🦞 OpenClaw Toolkit

> OpenClaw 综合工具包 - 一键部署、质量监控、配置管理

[![GitHub Stars](https://img.shields.io/github/stars/illbnm/openclaw-toolkit?style=social)](https://github.com/illbnm/openclaw-toolkit)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## 功能特性

### 🔧 一键部署工具
- 自动检测系统环境
- 自动安装依赖
- 自动创建配置文件
- 自动初始化记忆系统

### 🔍 中转站质量监控
- 自动测试中转站延迟
- 检测模型是否被替换
- 质量评分和警告
- 自动切换最佳中转站

### ⚙️ 配置管理
- 一键生成配置文件
- 多模型配置模板
- 配置验证和修复

### 💰 成本监控
- API 使用量追踪
- 成本计算和报告
- 多模型定价支持

## 快速开始

```bash
# 克隆仓库
git clone https://github.com/illbnm/openclaw-toolkit.git
cd openclaw-toolkit

# 一键部署
python3 installer.py --install

# 仅检查环境
python3 installer.py --check

# 检测中转站质量
python3 proxy_monitor.py --check

# 监控成本
python3 cost_monitor.py
```

## 工具列表

| 工具 | 描述 | 用法 |
|------|------|------|
| `installer.py` | 一键部署工具 | `python3 installer.py --install` |
| `proxy_monitor.py` | 中转站质量监控 | `python3 proxy_monitor.py --check` |
| `cost_monitor.py` | 成本监控 | `python3 cost_monitor.py` |
| `config_gen.py` | 配置生成器 | `python3 config_gen.py` |

## 系统要求

- Python 3.8+
- Node.js 18+
- npm 或 yarn

## 安装

### 方式 1: 一键安装

```bash
curl -fsSL https://raw.githubusercontent.com/illbnm/openclaw-toolkit/main/install.sh | bash
```

### 方式 2: 手动安装

```bash
git clone https://github.com/illbnm/openclaw-toolkit.git
cd openclaw-toolkit
pip install -r requirements.txt
python3 installer.py --install
```

## 使用示例

### 一键部署

```bash
$ python3 installer.py --install

==================================================
🦞 OpenClaw 一键部署工具
==================================================

📋 系统检查:
  操作系统: Linux 6.6.119
  Python: 3.11.5
  ✅ Python 版本满足
  ✅ Node.js: v22.22.1
  ✅ npm: 10.9.4
  ✅ Docker: 27.0.3

📋 OpenClaw 检查:
  ✅ OpenClaw 目录: /home/user/.openclaw
  ✅ 配置文件: /home/user/.openclaw/openclaw.json
     模型: claude-3-5-sonnet-20241022
     Skills: 2 个

⚙️ 创建配置:
  ✅ 配置已创建: /home/user/.openclaw/openclaw.json

🧠 创建记忆系统:
  ✅ 创建 MEMORY.md
  ✅ 创建 2026-03-08.md

下一步:
  1. 配置 API Key: 编辑 ~/.openclaw/models.json
  2. 启动 Gateway: openclaw gateway start
  3. 开始对话: openclaw chat
```

### 中转站质量检测

```bash
$ python3 proxy_monitor.py --check

🔍 开始检测中转站质量...

检测: openai-proxy
  URL: https://api.example.com/v1
  延迟: 0.35s
  置信度: 80%

检测: claude-proxy
  URL: https://api.anthropic-proxy.com/v1
  延迟: 0.52s
  置信度: 75%
  ⚠️ 响应时间较长

==================================================
🔍 中转站质量监控报告
==================================================
检测时间: 2026-03-08 11:00:00

📍 openai-proxy
   延迟: 0.35s
   置信度: 80%

📍 claude-proxy
   延迟: 0.52s
   置信度: 75%
   ⚠️ 响应时间较长

==================================================
```

## 常见问题

### Q: 工具报错找不到 openclaw 命令？
A: 请先安装 OpenClaw: `npm install -g openclaw`

### Q: 中转站检测显示 0% 置信度？
A: 可能是 API Key 无效或网络问题，请检查配置

### Q: 如何添加新的中转站？
A: 编辑 `~/.openclaw/models.json` 添加新配置

## 贡献

欢迎提交 Issue 和 Pull Request！

## 捐赠支持

如果这个工具有帮助，欢迎捐杯咖啡：

**SOL**: `DdqsLbFK9kW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm`

## License

MIT License

---

Made with 🦞 by [Jarvis](https://github.com/illbnm)
