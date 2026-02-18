import importlib
import sys
from pathlib import Path


def load_commands():
    commands = {}
    commands_dir = Path("./commands")

    for file in commands_dir.glob("*.py"):
        if file.name.startswith("_"):
            continue

        module_name = f"commands.{file.stem}"

        # Reload if already loaded, otherwise import fresh
        if module_name in sys.modules:
            module = importlib.reload(sys.modules[module_name])
        else:
            module = importlib.import_module(module_name)

        if hasattr(module, file.stem):
            commands[file.stem] = getattr(module, file.stem)

    return commands
