import re
import sys
from pathlib import Path


def find_file(subpath, root=Path(".")):
    """Find a file with a path that ends like the specified path."""
    subpath = Path(subpath)
    for match in root.rglob(subpath.name):
        if match.parts[-len(subpath.parts):] == subpath.parts:
            return match.resolve()
    print("File", subpath, "not found under", root)
    sys.exit(1)


def edit_file(path, value, pattern, replacement_template):
    """Apply a regex substitution to a file, preserving its original line endings."""
    with open(path, 'r', newline='') as f:
        text = f.read()
    text = re.sub(pattern, replacement_template.format(value=value), text)
    with open(path, 'w', newline='') as f:
        f.write(text)


def ask_value_and_apply(prompt, default, value_type, pattern, replacement_template, file_path):
    """
    Ask the user for input, convert it to a number, and apply it into a file using the provided
    regex pattern and replacement template.

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
            value = value_type(value)
        except ValueError:
            print("Invalid number:", value)
            sys.exit(1)

    edit_file(file_path, value, pattern, replacement_template)

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
        default=20,
        value_type=int,
        pattern=r'(\["fontSize"\] = )\d+(,)',
        replacement_template=r'\g<1>{value}\g<2>  -- modified by dcs_mse.exe',
        file_path=game_messages_path,
    )

    ask_value_and_apply(
        "Enter the desired font scale multiplier for the radio command menu.\n"
        "This affects the radio menu font size.",
        default=1.75,
        value_type=float,
        pattern=r'(fontScale = fontScale \* )\d+\.?\d*',
        replacement_template=r'\g<1>{value}  -- modified by dcs_mse.exe',
        file_path=command_menu_path,
    )


if __name__ == "__main__":
    main()
