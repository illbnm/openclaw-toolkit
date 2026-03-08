#!/usr/bin/env python3
"""
OpenClaw 一键部署工具
自动化 OpenClaw 部署和配置

作者: 贾维斯 (Jarvis)
GitHub: https://github.com/illbnm/openclaw-toolkit
捐赠: DdqsLbFK9kW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm (SOL)

功能:
- 自动检测系统环境
- 一键安装依赖
- 自动配置 OpenClaw
- 一键启动/停止
- 健康检查
"""

import os
import sys
import json
import subprocess
import platform
from pathlib import Path
from datetime import datetime

class OpenClawInstaller:
    """OpenClaw 一键安装器"""
    
    def __init__(self):
        self.home = Path.home()
        self.openclaw_dir = self.home / ".openclaw"
        self.workspace = self.openclaw_dir / "workspace"
        self.config_file = self.openclaw_dir / "openclaw.json"
        self.log_file = self.openclaw_dir / "install.log"
        
    def log(self, message):
        """记录日志"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_line = f"[{timestamp}] {message}"
        print(log_line)
        with open(self.log_file, "a") as f:
            f.write(log_line + "\n")
    
    def check_system(self):
        """检查系统环境"""
        self.log("=" * 50)
        self.log("🦞 OpenClaw 一键部署工具")
        self.log("=" * 50)
        self.log("")
        
        self.log("📋 系统检查:")
        
        # 操作系统
        os_info = f"{platform.system()} {platform.release()}"
        self.log(f"  操作系统: {os_info}")
        
        # Python 版本
        py_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        self.log(f"  Python: {py_version}")
        
        if sys.version_info < (3, 8):
            self.log("  ❌ Python 版本过低，需要 3.8+")
            return False
        self.log("  ✅ Python 版本满足")
        
        # Node.js
        node_result = subprocess.run(["node", "--version"], capture_output=True, text=True)
        if node_result.returncode == 0:
            self.log(f"  ✅ Node.js: {node_result.stdout.strip()}")
        else:
            self.log("  ⚠️ Node.js 未安装")
        
        # npm
        npm_result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if npm_result.returncode == 0:
            self.log(f"  ✅ npm: {npm_result.stdout.strip()}")
        else:
            self.log("  ⚠️ npm 未安装")
        
        # Docker (可选)
        docker_result = subprocess.run(["docker", "--version"], capture_output=True, text=True)
        if docker_result.returncode == 0:
            self.log(f"  ✅ Docker: {docker_result.stdout.strip()}")
        else:
            self.log("  ℹ️ Docker 未安装 (可选)")
        
        return True
    
    def check_openclaw(self):
        """检查 OpenClaw 安装状态"""
        self.log("")
        self.log("📋 OpenClaw 检查:")
        
        # 检查目录
        if self.openclaw_dir.exists():
            self.log(f"  ✅ OpenClaw 目录: {self.openclaw_dir}")
        else:
            self.log(f"  ⚠️ OpenClaw 目录不存在")
        
        # 检查配置
        if self.config_file.exists():
            self.log(f"  ✅ 配置文件: {self.config_file}")
            try:
                with open(self.config_file) as f:
                    config = json.load(f)
                self.log(f"     模型: {config.get('model', 'N/A')}")
                self.log(f"     Skills: {len(config.get('skills', []))} 个")
            except:
                self.log("     ⚠️ 配置文件解析失败")
        else:
            self.log(f"  ⚠️ 配置文件不存在")
        
        # 检查 Gateway
        gateway_result = subprocess.run(
            ["openclaw", "gateway", "status"],
            capture_output=True, text=True
        )
        if gateway_result.returncode == 0:
            self.log("  ✅ Gateway 运行中")
        else:
            self.log("  ⚠️ Gateway 未运行")
        
        return True
    
    def install_dependencies(self):
        """安装依赖"""
        self.log("")
        self.log("📦 安装依赖:")
        
        # 检查 openclaw CLI
        result = subprocess.run(["which", "openclaw"], capture_output=True, text=True)
        if result.returncode == 0:
            self.log(f"  ✅ OpenClaw CLI: {result.stdout.strip()}")
        else:
            self.log("  ⚠️ OpenClaw CLI 未安装")
            self.log("  请运行: npm install -g openclaw")
            return False
        
        return True
    
    def create_config(self, model="claude-3-5-sonnet-20241022"):
        """创建配置文件"""
        self.log("")
        self.log("⚙️ 创建配置:")
        
        config = {
            "name": "My Assistant",
            "model": model,
            "system": "You are a helpful AI assistant.",
            "skills": ["capability-evolver", "self-improving-agent"],
            "tools": {
                "read": True,
                "write": True,
                "edit": True,
                "exec": True,
                "web_fetch": True,
                "browser": True,
                "memory_search": True,
                "memory_get": True
            },
            "mcpServers": {}
        }
        
        # 创建目录
        self.openclaw_dir.mkdir(parents=True, exist_ok=True)
        self.workspace.mkdir(parents=True, exist_ok=True)
        
        # 写入配置
        with open(self.config_file, "w") as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        
        self.log(f"  ✅ 配置已创建: {self.config_file}")
        self.log(f"     模型: {model}")
        self.log(f"     Skills: capability-evolver, self-improving-agent")
        
        return True
    
    def create_memory(self):
        """创建记忆文件"""
        self.log("")
        self.log("🧠 创建记忆系统:")
        
        memory_dir = self.workspace / "memory"
        memory_dir.mkdir(parents=True, exist_ok=True)
        
        # 创建 MEMORY.md
        memory_file = self.workspace / "MEMORY.md"
        if not memory_file.exists():
            memory_content = """# MEMORY.md - 长期记忆

> 由 OpenClaw 一键部署工具创建

## 重要信息

- 创建时间: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """
- 模型: claude-3-5-sonnet-20241022

## 记忆规则

1. 记住重要的决策和偏好
2. 记住用户的常用命令
3. 记住项目相关信息
"""
            with open(memory_file, "w") as f:
                f.write(memory_content)
            self.log(f"  ✅ 创建 MEMORY.md")
        else:
            self.log(f"  ✅ MEMORY.md 已存在")
        
        # 创建今日记忆文件
        today = datetime.now().strftime("%Y-%m-%d")
        today_file = memory_dir / f"{today}.md"
        if not today_file.exists():
            with open(today_file, "w") as f:
                f.write(f"# {today} 记忆\n\n")
            self.log(f"  ✅ 创建 {today}.md")
        
        return True
    
    def generate_report(self):
        """生成报告"""
        self.log("")
        self.log("=" * 50)
        self.log("📊 部署报告")
        self.log("=" * 50)
        self.log(f"OpenClaw 目录: {self.openclaw_dir}")
        self.log(f"配置文件: {self.config_file}")
        self.log(f"工作空间: {self.workspace}")
        self.log(f"日志文件: {self.log_file}")
        self.log("")
        self.log("下一步:")
        self.log("  1. 配置 API Key: 编辑 ~/.openclaw/models.json")
        self.log("  2. 启动 Gateway: openclaw gateway start")
        self.log("  3. 开始对话: openclaw chat")
        self.log("")
        self.log("☕ 如果这个工具有帮助，请捐杯咖啡:")
        self.log("   SOL: DdqsLbFK9kW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm")
        self.log("=" * 50)
        
        return True


def main():
    installer = OpenClawInstaller()
    
    import argparse
    parser = argparse.ArgumentParser(description="OpenClaw 一键部署工具")
    parser.add_argument("--check", action="store_true", help="仅检查系统环境")
    parser.add_argument("--install", action="store_true", help="安装 OpenClaw")
    parser.add_argument("--config", action="store_true", help="创建配置文件")
    parser.add_argument("--model", default="claude-3-5-sonnet-20241022", help="默认模型")
    
    args = parser.parse_args()
    
    if args.check:
        installer.check_system()
        installer.check_openclaw()
    elif args.install:
        installer.check_system()
        installer.install_dependencies()
        installer.create_config(args.model)
        installer.create_memory()
        installer.generate_report()
    elif args.config:
        installer.create_config(args.model)
        installer.create_memory()
        installer.generate_report()
    else:
        # 默认：检查 + 配置
        installer.check_system()
        installer.check_openclaw()
        print("\n运行 --install 进行完整安装，或 --config 仅创建配置")


if __name__ == "__main__":
    main()
