import asyncio
import os
import sqlite3
from typing import cast

import stoat
from dotenv import load_dotenv

from modules.handle_fact import handle_fact
from modules.load_commands import load_commands
from modules.stats import track_message

load_dotenv()

client = stoat.Client()
PREFIX = "!"


@client.on(stoat.ReadyEvent)
async def on_ready(event: stoat.ReadyEvent, /):
    print(f"We have logged in as {event.me.tag}")

    global commands
    commands = load_commands()
    print(f"Loaded {len(commands)} commands.")

    # Prepare Database
    global db
    db = sqlite3.connect(os.environ["SQLITE_DB_PATH"]).cursor()

    global WELCOME_IMAGE_BYTES
    with open("welcome_image.jpg", "rb") as f:
        WELCOME_IMAGE_BYTES = f.read()

    print("Bot is ready!")


@client.on(stoat.MessageCreateEvent)
async def on_message(event: stoat.MessageCreateEvent, /):
    message = event.message
    print(f"Message from {message.author.tag}: {message.content}")

    if message.author.relationship is stoat.RelationshipStatus.user:
        return

    if message.content.startswith(PREFIX):
        command = message.content[len(PREFIX) :].split()[0]

        if command in commands:
            await commands[command](get_context(event))

        if command == "test":
            member = event.message.author_as_member
            join_event = stoat.ServerMemberJoinEvent(shard=client.shard, member=member)

            await on_member_join(join_event)

            # await event.message.channel.send(f"Welcome to the gang {event.message.author.mention}", attachments=[
            #     cast(stoat.ResolvableResource, WELCOME_IMAGE_BYTES)
            # ])
            # print(len(FACTS))
    else:
        await handle_fact(get_context(event))
        await track_message(db, event)


@client.on(stoat.ServerMemberJoinEvent)
async def on_member_join(event: stoat.ServerMemberJoinEvent, /):

    print(f"Member {event.member.tag} joined server {event.member.server_id}")

    server = event.member.get_server()

    if server is None:
        print("Couldn't find server, aborting")
        return

    (welcome_message, welcome_channel_id, welcome_image_blob) = db.execute(
        "SELECT welcome_message, welcome_channel_id, welcome_image_blob FROM server_settings WHERE server_id = ?;",
        (server.id,),
    ).fetchone()

    print(welcome_channel_id)

    welcome_message = welcome_message.replace("{user}", event.member.mention)
    welcome_channel = next(
        (c for c in server.channels if c.id == welcome_channel_id), None
    )

    if welcome_channel is None:
        print(f"Couldn't find welcome channel with ID: {welcome_channel_id}")
        return

    await welcome_channel.send(
        welcome_message,
        attachments=[cast(stoat.ResolvableResource, welcome_image_blob)],
    )


def get_context(event=None):
    """Return context dict with shared data for commands."""
    return {
        "EVENT": event,  # Represents some kind of stoat event, can be used by commands to access event data if needed
        "DB": db,
        "CLIENT": client,
        "COMMANDS": commands,
    }


client.run(os.environ["BOT_TOKEN"])
