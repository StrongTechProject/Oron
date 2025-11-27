#!/usr/bin/env python3
"""
Oron Toolchain CLI (v1.1.2)
The central router for the Oron system.
"""

import sys
import os
from modules import injector, spellbook

def clear_screen():
    """Clears the terminal screen based on OS."""
    os.system('cls' if os.name == 'nt' else 'clear')

def pause():
    """Waits for user input before clearing screen."""
    input("\nPress [Enter] to return to menu...")

def print_menu():
    print("\n========================================")
    print("      🔮 Oron v1.1.1 Toolchain")
    print("========================================")
    print("1. Copy Architect Blueprint Prompt (Layer 0)")
    print("2. Copy Conductor System Prompt    (Layer 2)")
    print("3. Run Injector (Interactive Mode) (Layer 3)")
    print("0. Exit")
    print("========================================")

def main():
    # Case A: Conductor generated command (Arguments present)
    # Example: oron inject --files "..." --task "..."
    # 这种情况不需要清屏，直接执行并退出
    if len(sys.argv) > 1:
        injector.run_cli(sys.argv[1:])
        return

    # Case B: Human User Cold Start (No arguments)
    while True:
        clear_screen() # 每次循环开始时清屏
        print_menu()
        choice = input("Select option: ").strip()

        if choice == '1':
            spellbook.copy_architect()
            pause() # 暂停，让你看清结果
        elif choice == '2':
            spellbook.copy_conductor()
            pause() # 暂停，让你看清结果
        elif choice == '3':
            injector.run_interactive()
            pause() # 暂停，让你看清结果
        elif choice == '0':
            print("👋 Exiting Oron.")
            sys.exit(0)
        else:
            print("❌ Invalid option.")
            pause()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n👋 Operation cancelled.")
        sys.exit(0)