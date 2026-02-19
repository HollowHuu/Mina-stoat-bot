import os
import sqlite3
from textwrap import dedent
from typing import cast

import stoat


# FIXME - Should make this into a full context menu similar to settings
async def createrolemenu(context):
    """Makes a role selector embed and monitors it!"""
    # !createrolemenu {name} {channel id}

    event: stoat.MessageCreateEvent = context["EVENT"]
    if event is None:
        return

    msg = event.message.content
    server = event.message.get_server()[0]

    if server is None:
        event.message.reply("Something went wrong!")
        return

    name = msg.split()[1] if len(msg.split()) > 1 else None
    channel_id = msg.split()[2] if len(msg.split()) > 2 else None

    if channel_id is None:
        event.message.reply("Missing channel")
        return

    channel_id = channel_id.replace("<#", "").replace(">", "")

    menu_channel = next((c for c in server.channels if c.id == channel_id), None)
    if menu_channel is None:
        event.message.reply(f"Could not find channel with id {channel_id}")
        return

    embed = stoat.SendableEmbed(title=name)

    # TODO - Make attachment and send it off

    menu_channel.send(attachments=[])

    print(name, channel_id)

    pass
