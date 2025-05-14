#!/bin/bash

# Configuration
INSTALL_DIR="$HOME/.chatroom"
BIN_PATH="/usr/local/bin/chatroom"
CLIENT_URL="https://raw.githubusercontent.com/heroinsh/chroom_client/main/client.py"

echo ""
echo "📦 Installing Chatroom Client Tool..."
echo "🔧 Developed by heroinsh (H0lwin)"
echo ""

# Ensure sudo is available
if ! command -v sudo &> /dev/null; then
    echo "❌ 'sudo' is required but not found. Please install sudo or run as root."
    exit 1
fi

# Create install directory
mkdir -p "$INSTALL_DIR"

# Download client.py
echo "⬇️ Downloading client.py from GitHub..."
if ! curl -fsSL "$CLIENT_URL" -o "$INSTALL_DIR/client.py"; then
    echo "❌ Failed to download client.py"
    exit 1
fi

# Create launcher script
LAUNCHER="$INSTALL_DIR/run_chatroom.sh"
cat << EOF > "$LAUNCHER"
#!/bin/bash
python3 "$INSTALL_DIR/client.py"
EOF

chmod +x "$LAUNCHER"

# Link to system PATH
echo "🔗 Linking 'chatroom' command to system..."
if sudo ln -sf "$LAUNCHER" "$BIN_PATH"; then
    echo ""
    echo "✅ Chatroom installed successfully!"
    echo "🔧 Developed by heroinsh (H0lwin)"
    echo ""
    echo "💡 You can now run 'chatroom' from any terminal."
    echo "🗨️  Happy chatting!"
else
    echo "❌ Failed to create symlink. Try running as sudo."
    exit 1
fi
