from modules.load_commands import load_commands


async def reload(context):
    """reload the bot's commands"""
    commands = context["COMMANDS"]

    commands.clear()
    new_commands = load_commands()
    commands.update(new_commands)
    print(f"Reloaded {len(commands)} commands.", flush=True)
