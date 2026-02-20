import os
import sqlite3
from textwrap import dedent
from typing import cast

import stoat


async def rolemenu(context):
    event: stoat.MessageCreateEvent = context["EVENT"]
    db: sqlite3.Cursor = context["DB"]
    client: stoat.Client = context["CLIENT"]

    msg = event.message.content
    subcommand = msg.split()[1] if len(msg.split()) > 1 else None
    args = msg.split()[2:] if len(msg.split()) > 2 else []

    subcommand_map = {
        "create": rolemenu_create,
        # "add": rolemenu_add,
        # "remove": rolemenu_remove,
        # "delete": rolemenu_delete,
        # "description": rolemenu_description
    }

    if subcommand in subcommand_map:
        await subcommand_map[subcommand](event, db, client, args)
    else:
        helper_embed = stoat.SendableEmbed(
            title="Rolemenu command",
            description=dedent("""
                # Command Usage
                **rolemenu create {title} {channel}**
                **Example**: *!rolemenu create "Game roles" #Roles*

                ## create
                - **create {title} {channel}**
                  Create a role selection embed in a given channel.

                """),
        )
        await event.message.channel.send("", embeds=[helper_embed])


async def rolemenu_create(
    event: stoat.MessageCreateEvent,
    db: sqlite3.Cursor,
    client: stoat.Client,
    args: list[str],
):
    """Makes a role selector embed and monitors it!"""
    # !createrolemenu {name} {channel id}

    # event: stoat.MessageCreateEvent = context["EVENT"]
    if event is None:
        return

    if len(args) < 2:
        await event.message.reply("Missing arguments")
        return

    server = event.message.get_server()[0]

    if server is None:
        await event.message.reply("Something went wrong!")
        return

    title = " ".join(args).split('"')[1::2]
    title = " ".join(title)

    print(f"Title: {title}")

    channel_id = args[-1]  # Should alwayas be last

    # name = msg.split()[1] if len(msg.split()) > 1 else None
    # channel_id = msg.split()[2] if len(msg.split()) > 2 else None

    if channel_id is None:
        await event.message.reply("Missing channel")
        return

    channel_id = channel_id.replace("<#", "").replace(">", "")

    menu_channel = next((c for c in server.channels if c.id == channel_id), None)
    if menu_channel is None:
        await event.message.reply(f"Could not find channel with id {channel_id}")
        return

    embed = stoat.SendableEmbed(title=title)

    sent_msg = await menu_channel.send(embeds=[embed])

    # Store the embed in DB
    db.execute(
        "insert into role_menus (message_id, channel_id) values (?, ?);",
        [sent_msg.id, channel_id],
    )

    await event.message.reply(
        "Created embed, use `rolemenu add ...` to add reactions to the menu."
    )
