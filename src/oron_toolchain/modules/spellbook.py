"""
Oron Spellbook Module
Responsibilities: Reading static templates and copying to clipboard.
"""
import os
import sys

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

def get_template_path(filename):
    """Resolves absolute path to templates based on this file's location."""
    # current_dir is .../oron_toolchain/modules
    current_dir = os.path.dirname(os.path.abspath(__file__))
    # templates_dir is .../oron_toolchain/templates
    return os.path.join(current_dir, '..', 'templates', filename)

def cast_spell(spell_name, filename):
    """Reads the template and copies to clipboard."""
    path = get_template_path(filename)
    
    if not os.path.exists(path):
        print(f"❌ Error: Template file not found at {path}")
        return

    try:
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if CLIPBOARD_AVAILABLE:
            pyperclip.copy(content)
            print(f"\n✨ **{spell_name}** copied to clipboard!")
            print(f"   📄 Source: {filename}")
            print("   👉 Action: Paste into a new LLM session.")
        else:
            print(f"\n⚠️  `pyperclip` missing. Printing {spell_name}:\n")
            print(content)
            
    except Exception as e:
        print(f"❌ Error reading template: {e}")

def copy_architect():
    cast_spell("Architect Blueprint Prompt", "architect.md")

def copy_conductor():
    cast_spell("Conductor Core Prompt", "conductor.md")