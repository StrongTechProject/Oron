#!/bin/bash

# Get absolute path of the directory containing this script
INSTALL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLI_PATH="$INSTALL_DIR/oron_cli.py"

echo "Configuring Oron Toolchain..."
echo "Location: $INSTALL_DIR"

# Ensure executable permission
chmod +x "$CLI_PATH"

# Detect Shell
SHELL_CONFIG=""
if [ -n "$ZSH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.zshrc"
elif [ -n "$BASH_VERSION" ]; then
    SHELL_CONFIG="$HOME/.bashrc"
else
    echo "⚠️  Could not detect Bash or Zsh. Please manually add the alias."
    exit 1
fi

# Prepare Alias command
ALIAS_CMD="alias oron='python3 \"$CLI_PATH\"'"

# Check if alias already exists to avoid duplicates
if grep -q "alias oron=" "$SHELL_CONFIG"; then
    echo "ℹ️  Alias 'oron' already exists in $SHELL_CONFIG. Please check it manually if it's outdated."
else
    echo "" >> "$SHELL_CONFIG"
    echo "# Oron Toolchain" >> "$SHELL_CONFIG"
    echo "$ALIAS_CMD" >> "$SHELL_CONFIG"
    echo "✅ Alias added to $SHELL_CONFIG"
fi

echo "------------------------------------------------"
echo "🎉 Setup Complete!"
echo "👉 Please run: source $SHELL_CONFIG"
echo "👉 Then type 'oron' to start."
echo "------------------------------------------------"