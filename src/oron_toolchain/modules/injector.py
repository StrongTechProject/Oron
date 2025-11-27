"""
Oron Injector Module (v1.1.1)
Inherits logic from Oron 1.0.1.
Responsibilities: Context gathering, WGC protocol enforcement, Prompt generation.
"""

import os
import argparse
import sys

# Clipboard handling
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

def get_language_hint(filepath):
    """Infer markdown language tag from extension."""
    ext = os.path.splitext(filepath)[1].lower()
    mapping = {
        '.py': 'python', '.js': 'javascript', '.ts': 'typescript',
        '.jsx': 'javascript', '.tsx': 'typescript', '.html': 'html',
        '.css': 'css', '.sql': 'sql', '.sh': 'bash', '.md': 'markdown',
        '.json': 'json', '.yml': 'yaml', '.yaml': 'yaml', '.toml': 'toml'
    }
    return mapping.get(ext, '')

def read_file_safely(filepath):
    """
    Reads file content with path awareness.
    CRITICAL: Uses os.getcwd() implicitly by open(), ensuring functionality 
    regardless of where the toolchain is installed.
    """
    # Resolve path relative to where the user executed the command
    target_path = os.path.abspath(filepath)
    
    if not os.path.exists(target_path):
        return f"// [ORON INFO]: File '{filepath}' not found.\n// Assuming CREATION MODE: You are expected to create this file."
    
    try:
        with open(target_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
            # Add line numbers for WGC precision
            lines = [f"{i+1:4} | {line}" for i, line in enumerate(content.splitlines())]
            return "\n".join(lines)
    except Exception as e:
        return f"!!! SYSTEM ERROR READING {filepath}: {str(e)} !!!"

def build_payload(files_str, task_description):
    """Constructs the WGC-compliant prompt."""
    prompt = []
    
    # 1. Header & Task
    prompt.append("# 👷 ORON WORKER EXECUTION ORDER (v1.1.1)")
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
    
    # 3. WGC Protocol
    prompt.append("\n## ⚖️ WGC PROTOCOL (CRITICAL)")
    prompt.append("1. **Atomic Focus:** Strictly limited to the PRIMARY OBJECTIVE.")
    prompt.append("2. **No Lazy Coding:** No placeholders. Output COMPLETE code.")
    prompt.append("3. **Line Number Accuracy:** Reference specific line numbers.")

    # 4. Output Format
    prompt.append("\n## 📝 OUTPUT FORMAT REQUIREMENT")
    prompt.append("End response with:")
    prompt.append("```markdown")
    prompt.append("> **STATUS:** [COMPLETED / FAILED]")
    prompt.append("> **FILES CREATED/MODIFIED:** [List]")
    prompt.append("> **VERIFICATION:** [Command to verify]")
    prompt.append("```")

    return "\n".join(prompt)

def dispatch_payload(payload, file_info):
    """Handles the final output (Clipboard vs Stdout)."""
    if CLIPBOARD_AVAILABLE:
        try:
            pyperclip.copy(payload)
            print(f"\n✅ **Oron Payload Generated!** ({len(payload)} chars)")
            print(f"   📂 Context: {file_info}")
            print("   📋 Status: COPIED to Clipboard.")
            print("   👉 Action: Switch to Worker LLM and press [Ctrl+V]")
        except Exception as e:
            print(f"\n❌ Clipboard Error: {e}")
            print(payload)
    else:
        print("\n⚠️  `pyperclip` missing. Payload:\n")
        print("-" * 40)
        print(payload)
        print("-" * 40)

def run_cli(args_list):
    """Entry point for CLI arguments (from Conductor)."""
    parser = argparse.ArgumentParser(description='Oron Injector')
    subparsers = parser.add_subparsers(dest='command')
    
    # Compatibility with "oron inject ..."
    inject_parser = subparsers.add_parser('inject')
    inject_parser.add_argument('--files', type=str, default="", help='Comma separated files')
    inject_parser.add_argument('--task', type=str, required=True, help='Task instruction')

    args = parser.parse_args(args_list)

    if args.command == 'inject':
        payload = build_payload(args.files, args.task)
        dispatch_payload(payload, args.files if args.files else "(None - Creation Mode)")
    else:
        parser.print_help()

def run_interactive():
    """Entry point for Interactive Menu Mode."""
    print("\n--- 🚀 Interactive Injection Mode ---")
    files = input("Files (comma separated, optional): ").strip()
    task = input("Task (Required): ").strip()
    
    if not task:
        print("❌ Task is required.")
        return

    payload = build_payload(files, task)
    dispatch_payload(payload, files if files else "(None - Creation Mode)")