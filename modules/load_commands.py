import stoat
from dotenv import load_dotenv
import os
import random
import json
from typing import cast
from pathlib import Path
import importlib

def load_commands():
    commands = {}
    commands_dir = Path('./commands')

    for file in commands_dir.glob('*.py'):
        if file.name.startswith('_'):
            continue

        module_name = file.stem
        module = importlib.import_module(f'commands.{module_name}')

        if hasattr(module, module_name):
            commands[module_name] = getattr(module, module_name)

    return commands