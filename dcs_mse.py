import re
import sys
from pathlib import Path


DEFAULT_GAME_MESSAGES_FONT_SIZE = 20
DEFAULT_COMMAND_MENU_FONT_SCALE = 1.75


def find_file(subpath, root=Path(".")):
    """Find a file with a path that ends like the specified path."""
    subpath = Path(subpath)
    for match in root.rglob(subpath.name):
        if match.parts[-len(subpath.parts):] == subpath.parts:
            return match.resolve()
    print("File", subpath, "not found under", root)
    sys.exit(1)


def edit_game_messages(path, font_size):
    """Set all fontSize values in gameMessages.dlg to font_size."""
    with open(path, 'r', newline='') as f:
        text = f.read()
    text = re.sub(
        r'(\["fontSize"\] = )\d+(,)',
        rf'\g<1>{font_size}\g<2>  -- modified by dcs_mse.exe',
        text
    )
    with open(path, 'w', newline='') as f:
        f.write(text)


def edit_command_menu(path, font_scale):
    """Set the radio command menu font scale multiplier in CommandMenu.lua."""
    with open(path, 'r', newline='') as f:
        text = f.read()
    text = re.sub(
        r'(fontScale = fontScale \* )\d+\.?\d*',
        rf'\g<1>{font_scale}  -- modified by dcs_mse.exe',
        text
    )
    with open(path, 'w', newline='') as f:
        f.write(text)


def ask_value_and_apply(prompt, default, converter, apply_func, file_path):
    """
    Ask the user for input, convert it to a number, and apply it using the provided function.
    If the user enters an empty string, the current value is kept.
    If the user enters 'r', the value is reset to the default.
    """
    print()
    print(prompt)
    print("(empty to keep the current value, or 'r' to reset to DCS defaults)")
    value = input("Value: ").strip().lower()

    if not value:
        print("Skipped, file not modified.")
        return

    if value == "r":
        print("Resetting to default value:", default)
        value = default
    else:
        try:
            value = converter(value)
        except ValueError:
            print("Invalid number:", value)
            sys.exit(1)

    apply_func(file_path, value)

    print("Value applied to", file_path)


def main():
    """
    This script allows you to modify the font size of game messages and the font scale of the radio command menu in DCS World.
    """
    if len(sys.argv) == 1:
        root = Path(".")
    elif len(sys.argv) == 2:
        root = Path(sys.argv[1])
    else:
        print("Usage: dcs_mse.py [root_directory]")
        sys.exit(1)

    game_messages_path = find_file("Scripts/UI/gameMessages.dlg", root)
    command_menu_path = find_file("Scripts/UI/RadioCommandDialogPanel/CommandMenu.lua", root)

    print("Files found at:")
    print(f"  {game_messages_path}")
    print(f"  {command_menu_path}")

    ask_value_and_apply(
        "Enter the desired font size for game messages.\n"
        "This affects messages that usually appear in the top corners of DCS, like subtitles, mission messages, etc.",
        DEFAULT_GAME_MESSAGES_FONT_SIZE,
        int,
        edit_game_messages,
        game_messages_path,
    )

    ask_value_and_apply(
        "Enter the desired font scale multiplier for the radio command menu.\n"
        "This affects the radio menu font size.",
        DEFAULT_COMMAND_MENU_FONT_SCALE,
        float,
        edit_command_menu,
        command_menu_path,
    )


if __name__ == "__main__":
    main()
