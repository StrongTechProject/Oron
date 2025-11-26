#!/usr/bin/env python3
"""
Oron 1.0.1 - Local Context Adapter (oron.py)
[System Architecture Component: Layer 3]

Changes in v1.0.1:
- Renamed to Oron.
- Added WGC (Worker Granularity Control) prompt injection.
- "Soft Fail" for missing files (assumes Creation Mode).

Usage: 
    python oron.py inject --files "config.py,models.py" --task "Add User class"
"""

import sys
import os
import argparse

# 尝试导入剪贴板库，如果没有安装则优雅处理
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

def get_language_hint(filepath):
    """根据文件扩展名推断 Markdown 语言标签"""
    ext = os.path.splitext(filepath)[1].lower()
    mapping = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'javascript',
        '.tsx': 'typescript',
        '.html': 'html',
        '.css': 'css',
        '.sql': 'sql',
        '.sh': 'bash',
        '.md': 'markdown',
        '.json': 'json',
        '.yml': 'yaml',
        '.yaml': 'yaml',
        '.toml': 'toml'
    }
    return mapping.get(ext, '') # 默认为空，即纯文本

def read_file_safely(filepath):
    """
    读取文件内容。
    v1.0.1 优化: 如果文件不存在，不再报错，而是假设这是 Creation Mode。
    """
    if not os.path.exists(filepath):
        # 优化点：不再大喊大叫报错，而是给出温和提示，防止 Worker 产生幻觉认为系统故障
        return f"// [ORON INFO]: File '{filepath}' not found on disk.\n// Assuming CREATION MODE: You are expected to create this file from scratch."
    
    try:
        # 使用 errors='replace' 防止读取非 UTF-8 字符时崩溃
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            # 添加行号以便 Worker 精确引用 (Line numbers for precision)
            lines = [f"{i+1:4} | {line}" for i, line in enumerate(content.splitlines())]
            return "\n".join(lines)
    except Exception as e:
        return f"!!! SYSTEM ERROR READING {filepath}: {str(e)} !!!"

def build_worker_prompt(files_str, task_description):
    """构建发给 Worker 的最终 Prompt，包含 WGC 协议"""
    prompt = []
    
    # 1. Header & Task
    prompt.append("# 👷 ORON WORKER EXECUTION ORDER (v1.0.1)")
    prompt.append(f"**PRIMARY OBJECTIVE:** {task_description}\n")
    
    # 2. Context Injection
    prompt.append("## 📂 DYNAMIC CONTEXT (Read-Only)")
    
    has_files = False
    if files_str and files_str.strip():
        file_list = [f.strip() for f in files_str.split(',') if f.strip()]
        if file_list:
            has_files = True
            for fpath in file_list:
                lang = get_language_hint(fpath)
                prompt.append(f"\n### 📄 File: `{fpath}`")
                prompt.append(f"```{lang}")
                prompt.append(read_file_safely(fpath))
                prompt.append("```")
    
    if not has_files:
        prompt.append("(No context files provided. Pure CREATION mode active.)")
    
    # 3. WGC Protocol Enforcement (Worker Granularity Control)
    prompt.append("\n## ⚖️ WGC PROTOCOL (CRITICAL)")
    prompt.append("1. **Atomic Focus:** You are strictly limited to the scope defined in PRIMARY OBJECTIVE.")
    prompt.append("2. **No Lazy Coding:** Do NOT use placeholders like `# ... existing code ...`. Output COMPLETE, WORKING code for the requested changes.")
    prompt.append("3. **Line Number Accuracy:** If modifying, reference specific line numbers from the context.")

    # 4. Standard Output Format
    prompt.append("\n## 📝 OUTPUT FORMAT REQURIEMENT")
    prompt.append("Please end your response with a summary block:")
    prompt.append("```markdown")
    prompt.append("> **STATUS:** [COMPLETED / FAILED]")
    prompt.append("> **FILES CREATED/MODIFIED:** [List files]")
    prompt.append("> **VERIFICATION:** [One-line command to verify/test]")
    prompt.append("```")

    return "\n".join(prompt)

def main():
    parser = argparse.ArgumentParser(description='Oron v1.0.1 Adapter Layer')
    subparsers = parser.add_subparsers(dest='command')

    # Command: INJECT
    inject_parser = subparsers.add_parser('inject')
    inject_parser.add_argument('--files', type=str, default="", help='Comma separated file paths')
    inject_parser.add_argument('--task', type=str, required=True, help='Task instruction')

    args = parser.parse_args()

    if args.command == 'inject':
        full_prompt = build_worker_prompt(args.files, args.task)
        
        if CLIPBOARD_AVAILABLE:
            try:
                pyperclip.copy(full_prompt)
                print(f"\n✅ **Oron Payload Generated!** ({len(full_prompt)} chars)")
                print(f"   📂 Context: {args.files if args.files else '(None - Creation Mode)'}")
                print("   📋 Status: COPIED to Clipboard.")
                print("   👉 Action: Switch to Worker LLM and press [Ctrl+V]")
            except Exception as e:
                print(f"\n❌ Clipboard Error: {e}")
                print("⚠️  Printing content to stdout instead:\n")
                print(full_prompt)
        else:
            print("\n⚠️  `pyperclip` module not found. Printing content to stdout:")
            print("-" * 40)
            print(full_prompt)
            print("-" * 40)
            print("💡 Tip: Run `pip install pyperclip` for auto-copy functionality.")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()