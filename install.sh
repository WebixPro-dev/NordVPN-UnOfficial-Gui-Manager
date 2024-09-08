#!/bin/bash

APPIMAGE_PATH="nordvpngui"
APP_NAME="NordVPN Gui Manager"
ICON_PATH="nordvpngui.ico"

TARGET_DIR="$HOME/.nordvpnguiunofficial"
mkdir -p "$TARGET_DIR"

cp "$APPIMAGE_PATH" "$TARGET_DIR/"
cp "$ICON_PATH" "$TARGET_DIR/"

NEW_APPIMAGE_PATH="$TARGET_DIR/$(basename $APPIMAGE_PATH)"
NEW_ICON_PATH="$TARGET_DIR/$(basename $ICON_PATH)"

chmod +x "$NEW_APPIMAGE_PATH"

DESKTOP_FILE="$HOME/.local/share/applications/${APP_NAME}.desktop"
{
echo "[Desktop Entry]"
echo "Name=$APP_NAME"
echo "Comment=Opis aplikacji"
echo "Exec=$NEW_APPIMAGE_PATH"
if [ -n "$ICON_PATH" ]; then
    echo "Icon=$NEW_ICON_PATH"
fi
echo "Terminal=false"
echo "Type=Application"
echo "Categories=Utility;Application;"
} > "$DESKTOP_FILE"

chmod +x "$DESKTOP_FILE"

update-desktop-database ~/.local/share/applications

echo "Aplikacja $APP_NAME została zainstalowana!"
