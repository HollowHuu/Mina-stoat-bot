import stoat
import sqlite3
import os

from modules.db_helper import update_field

async def settings(context):
    """Manage server settings. Subcommands: welcome_message, welcome_channel, welcome_image, fact_chance."""
    event: stoat.MessageCreateEvent = context['EVENT']
    db: sqlite3.Cursor = context['DB']
    client: stoat.Client = context['CLIENT']

    msg = event.message.content
    subcommand = msg.split()[1] if len(msg.split()) > 1 else None
    args = msg.split()[2:] if len(msg.split()) > 2 else []

    print(f'Settings command invoked with subcommand: {subcommand} and args: {args}')
    print("Test!!s")

    subcommand_mapping = {
        'welcome_message': settings_welcome_message,
        # 'welcome_channel': settings_welcome_channel,
        # 'welcome_image': settings_welcome_image,
        # 'fact_chance': settings_fact_chance
    }

    if subcommand in subcommand_mapping:
        await subcommand_mapping[subcommand](event, db, client, args)
    else:
        await event.message.reply(f"Invalid subcommand. Available subcommands: {subcommand_mapping.keys().__str__()}")



async def settings_welcome_message(event: stoat.MessageCreateEvent, db: sqlite3.Cursor, client: stoat.Client, args: list[str]):
    """Set the welcome message for new members. Use {user} to mention the new member."""

    if not args:
        await event.message.reply("Please provide a welcome message. Use {user} to mention the new member.")
        return
    
    new_message = ' '.join(args)
    server_id = event.message.get_server()[1]
    success = await update_field(db, server_id, 'welcome_message', new_message)

    if success:
        await event.message.reply("Welcome message updated successfully!")
    else:
        await event.message.reply("Failed to update welcome message. Please try again later.")