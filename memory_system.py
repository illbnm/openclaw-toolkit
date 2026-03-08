#!/usr/bin/env python3
"""
OpenClaw 记忆增强系统
实现 3 层记忆架构

作者: 贾维斯 (Jarvis)
GitHub: https://github.com/illbnm/openclaw-toolkit
捐赠: DdqsLbFK9kW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm (SOL)

功能:
- Layer 1: 会话记忆 (当前对话)
- Layer 2: 工作记忆 (任务上下文)
- Layer 3: 长期记忆 (持久化存储)
"""

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import hashlib

class MemorySystem:
    """3 层记忆系统"""
    
    def __init__(self, workspace: str = None):
        self.workspace = Path(workspace or Path.home() / ".openclaw" / "workspace")
        self.memory_dir = self.workspace / "memory"
        self.long_term_file = self.workspace / "MEMORY.md"
        self.session_file = self.memory_dir / "session.json"
        self.work_file = self.memory_dir / "work.json"
        
        # 确保目录存在
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # 初始化记忆
        self.session_memory = self._load_session()
        self.work_memory = self._load_work()
        self.long_term_memory = self._load_long_term()
    
    # ==================== Layer 1: 会话记忆 ====================
    
    def _load_session(self) -> Dict:
        """加载会话记忆"""
        if self.session_file.exists():
            try:
                with open(self.session_file) as f:
                    return json.load(f)
            except:
                pass
        return {
            "messages": [],
            "context": {},
            "start_time": datetime.now().isoformat()
        }
    
    def _save_session(self):
        """保存会话记忆"""
        with open(self.session_file, "w") as f:
            json.dump(self.session_memory, f, indent=2, ensure_ascii=False)
    
    def add_message(self, role: str, content: str):
        """添加消息到会话记忆"""
        self.session_memory["messages"].append({
            "role": role,
            "content": content,
            "timestamp": datetime.now().isoformat()
        })
        # 只保留最近 100 条消息
        if len(self.session_memory["messages"]) > 100:
            self.session_memory["messages"] = self.session_memory["messages"][-100:]
        self._save_session()
    
    def get_recent_messages(self, limit: int = 10) -> List[Dict]:
        """获取最近的消息"""
        return self.session_memory["messages"][-limit:]
    
    def set_context(self, key: str, value: Any):
        """设置会话上下文"""
        self.session_memory["context"][key] = value
        self._save_session()
    
    def get_context(self, key: str = None) -> Any:
        """获取会话上下文"""
        if key:
            return self.session_memory["context"].get(key)
        return self.session_memory["context"]
    
    # ==================== Layer 2: 工作记忆 ====================
    
    def _load_work(self) -> Dict:
        """加载工作记忆"""
        if self.work_file.exists():
            try:
                with open(self.work_file) as f:
                    return json.load(f)
            except:
                pass
        return {
            "current_task": None,
            "task_history": [],
            "important_facts": [],
            "user_preferences": {}
        }
    
    def _save_work(self):
        """保存工作记忆"""
        with open(self.work_file, "w") as f:
            json.dump(self.work_memory, f, indent=2, ensure_ascii=False)
    
    def set_current_task(self, task: str):
        """设置当前任务"""
        if self.work_memory["current_task"]:
            self.work_memory["task_history"].append({
                "task": self.work_memory["current_task"],
                "completed_at": datetime.now().isoformat()
            })
        self.work_memory["current_task"] = task
        self._save_work()
    
    def add_important_fact(self, fact: str, category: str = "general"):
        """添加重要事实"""
        self.work_memory["important_facts"].append({
            "fact": fact,
            "category": category,
            "added_at": datetime.now().isoformat()
        })
        # 去重
        seen = set()
        unique = []
        for f in self.work_memory["important_facts"]:
            key = f["fact"]
            if key not in seen:
                seen.add(key)
                unique.append(f)
        self.work_memory["important_facts"] = unique[-100:]  # 只保留最近 100 条
        self._save_work()
    
    def set_user_preference(self, key: str, value: Any):
        """设置用户偏好"""
        self.work_memory["user_preferences"][key] = value
        self._save_work()
    
    def get_user_preference(self, key: str = None) -> Any:
        """获取用户偏好"""
        if key:
            return self.work_memory["user_preferences"].get(key)
        return self.work_memory["user_preferences"]
    
    # ==================== Layer 3: 长期记忆 ====================
    
    def _load_long_term(self) -> str:
        """加载长期记忆"""
        if self.long_term_file.exists():
            return self.long_term_file.read_text()
        return "# MEMORY.md - 长期记忆\n\n> 由 OpenClaw Toolkit 创建\n\n"
    
    def _save_long_term(self):
        """保存长期记忆"""
        self.long_term_file.write_text(self.long_term_memory)
    
    def add_long_term_memory(self, content: str, section: str = None):
        """添加长期记忆"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        if section:
            # 查找或创建 section
            section_header = f"## {section}"
            if section_header not in self.long_term_memory:
                self.long_term_memory += f"\n\n{section_header}\n\n"
            # 在 section 下添加内容
            lines = self.long_term_memory.split("\n")
            insert_idx = -1
            for i, line in enumerate(lines):
                if line == section_header:
                    insert_idx = i + 2
                    break
            if insert_idx > 0:
                lines.insert(insert_idx, f"- [{timestamp}] {content}")
                self.long_term_memory = "\n".join(lines)
        else:
            self.long_term_memory += f"\n- [{timestamp}] {content}\n"
        self._save_long_term()
    
    def search_long_term(self, query: str) -> List[str]:
        """搜索长期记忆"""
        results = []
        lines = self.long_term_memory.split("\n")
        for line in lines:
            if query.lower() in line.lower():
                results.append(line.strip())
        return results
    
    # ==================== 工具方法 ====================
    
    def get_memory_hash(self) -> str:
        """获取记忆哈希（用于去重）"""
        content = json.dumps(self.session_memory) + json.dumps(self.work_memory) + self.long_term_memory
        return hashlib.md5(content.encode()).hexdigest()
    
    def export_memory(self) -> Dict:
        """导出所有记忆"""
        return {
            "session": self.session_memory,
            "work": self.work_memory,
            "long_term": self.long_term_memory,
            "exported_at": datetime.now().isoformat()
        }
    
    def import_memory(self, data: Dict):
        """导入记忆"""
        if "session" in data:
            self.session_memory = data["session"]
            self._save_session()
        if "work" in data:
            self.work_memory = data["work"]
            self._save_work()
        if "long_term" in data:
            self.long_term_memory = data["long_term"]
            self._save_long_term()
    
    def clear_session(self):
        """清除会话记忆"""
        self.session_memory = {
            "messages": [],
            "context": {},
            "start_time": datetime.now().isoformat()
        }
        self._save_session()
    
    def generate_report(self) -> str:
        """生成记忆报告"""
        report = []
        report.append("=" * 60)
        report.append("🧠 OpenClaw 记忆系统报告")
        report.append("=" * 60)
        report.append(f"报告时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        # Layer 1
        report.append("📋 Layer 1: 会话记忆")
        report.append(f"  消息数量: {len(self.session_memory['messages'])}")
        report.append(f"  上下文项: {len(self.session_memory['context'])}")
        report.append("")
        
        # Layer 2
        report.append("📝 Layer 2: 工作记忆")
        report.append(f"  当前任务: {self.work_memory['current_task'] or '无'}")
        report.append(f"  任务历史: {len(self.work_memory['task_history'])} 条")
        report.append(f"  重要事实: {len(self.work_memory['important_facts'])} 条")
        report.append(f"  用户偏好: {len(self.work_memory['user_preferences'])} 项")
        report.append("")
        
        # Layer 3
        report.append("📚 Layer 3: 长期记忆")
        lines = self.long_term_memory.split("\n")
        non_empty = [l for l in lines if l.strip() and not l.startswith("#")]
        report.append(f"  记忆条目: ~{len(non_empty)} 条")
        report.append(f"  文件大小: {len(self.long_term_memory)} 字符")
        report.append("")
        
        report.append("-" * 60)
        report.append("☕ 如果这个工具有帮助，请捐杯咖啡:")
        report.append("   SOL: DdqsLbFK9kW2Sq8vktTjD36bmuhheG13L9sGAzhmyTm")
        report.append("=" * 60)
        
        return "\n".join(report)


def main():
    import argparse
    parser = argparse.ArgumentParser(description="OpenClaw 记忆增强系统")
    parser.add_argument("--report", action="store_true", help="生成记忆报告")
    parser.add_argument("--clear-session", action="store_true", help="清除会话记忆")
    parser.add_argument("--add-fact", type=str, help="添加重要事实")
    parser.add_argument("--set-task", type=str, help="设置当前任务")
    parser.add_argument("--search", type=str, help="搜索长期记忆")
    parser.add_argument("--export", type=str, help="导出记忆到文件")
    parser.add_argument("--import", dest="import_file", type=str, help="从文件导入记忆")
    
    args = parser.parse_args()
    
    memory = MemorySystem()
    
    if args.report:
        print(memory.generate_report())
    elif args.clear_session:
        memory.clear_session()
        print("✅ 会话记忆已清除")
    elif args.add_fact:
        memory.add_important_fact(args.add_fact)
        print(f"✅ 已添加事实: {args.add_fact}")
    elif args.set_task:
        memory.set_current_task(args.set_task)
        print(f"✅ 已设置任务: {args.set_task}")
    elif args.search:
        results = memory.search_long_term(args.search)
        print(f"找到 {len(results)} 条记忆:")
        for r in results[:10]:
            print(f"  - {r}")
    elif args.export:
        data = memory.export_memory()
        with open(args.export, "w") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"✅ 记忆已导出到: {args.export}")
    elif args.import_file:
        with open(args.import_file) as f:
            data = json.load(f)
        memory.import_memory(data)
        print(f"✅ 已从 {args.import_file} 导入记忆")
    else:
        print(memory.generate_report())


if __name__ == "__main__":
    main()
