import stoat
import sqlite3
import os
from textwrap import dedent
from typing import cast

async def settings(context):
    """Manage server settings. Subcommands: welcome_message, welcome_channel, welcome_image, fact_chance."""
    event: stoat.MessageCreateEvent = context['EVENT']
    db: sqlite3.Cursor = context['DB']
    client: stoat.Client = context['CLIENT']

    msg = event.message.content
    subcommand = msg.split()[1] if len(msg.split()) > 1 else None
    args = msg.split()[2:] if len(msg.split()) > 2 else []

    subcommand_mapping = {
        'welcome_message': settings_welcome_message,
        'welcome_channel': settings_welcome_channel,
        'welcome_image': settings_welcome_image,
        'fact_chance': settings_fact_chance
    }

    if subcommand in subcommand_mapping:
        await subcommand_mapping[subcommand](event, db, client, args)
    else:
        helper_embed = stoat.SendableEmbed(
            title="Settings command",
            description=dedent('''
            # Command usage
            **settings {subcommand} {mode} [args]**
            **Example**: *settings welcome_message set WELCOME {user}!*
            
            ## welcome_message
            - **set {welcome_message}**
              *Sets your welcome message to the contents of {welcome_message}. You can use {user} to mention the member.*
            
            - **view**
              *Shows you the set welcome message*

            ## welcome_channel
            - **set {channel_mention}**
              *Sets the channel where welcome messages will be sent*
            
            - **view**
              *Shows the currently set welcome channel*
            
            - **disable**
              *Disables welcome messages*

            ## welcome_image
            - **set**
              *Sets an image to be sent with welcome messages. This requires an image to be attached.*
            
            - **view**
              *Shows the currently set welcome image*
            
            - **remove**
              *Removes the welcome image*

            ## fact_chance
            - **set {chance}**
              *Sets the chance (0-100.000) for the bot reply with a fact to any message*
            
            - **view**
              *Shows the currently set fact chance percentage*
            '''),
            color="#fa7ed5"
        )

        await event.message.channel.send("Invalid use of command, see embed for proper usage.", embeds=[helper_embed])


async def settings_welcome_message(event: stoat.MessageCreateEvent, db: sqlite3.Cursor, client: stoat.Client, args: list[str]):
    """Manage the welcome message for new members. Use {user} to mention the new member."""
    
    if not args:
        await event.message.reply("Please specify a mode: `set {message}` or `view`")
        return
    
    mode = args[0].lower()
    server_id = event.message.get_server()[1]
    
    if mode == "set":
        if len(args) < 2:
            await event.message.reply("Please provide a welcome message. Use {user} to mention the new member.")
            return
        
        new_message = ' '.join(args[1:])

        db.execute("UPDATE server_settings SET welcome_message = ? where server_id = ?;", [new_message, server_id])
        db.connection.commit()
        await event.message.reply("Welcome message updated successfully!")
    
    elif mode == "view":
        (current_message,) = db.execute("select welcome_message from server_settings where server_id = ?", [server_id]).fetchone()
        
        if current_message:
            await event.message.reply(f"Current welcome message: {current_message}")
        else:
            await event.message.reply("No welcome message has been set for this server yet.")
    
    else:
        await event.message.reply("Invalid mode. Use `set {message}` or `view`.")


async def settings_welcome_channel(event: stoat.MessageCreateEvent, db: sqlite3.Cursor, client: stoat.Client, args: list[str]):
    """Manage the welcome channel for new member messages."""
    
    if not args:
        await event.message.reply("Please specify a mode: `set {channel}`, `view`, or `disable`")
        return
    
    mode = args[0].lower()
    server_id = event.message.get_server()[1]
    
    if mode == "set":
        if len(args) < 2:
            await event.message.reply("Please mention a channel to set as the welcome channel.")
            return
        
        # Extract channel ID from mention (format: <#123456789>)
        channel_mention = args[1]
        channel_id = channel_mention.replace("<#", "").replace(">", "")
        
        db.execute("update server_settings set welcome_channel_id = ? where server_id = ?", [channel_id, server_id])
        db.connection.commit()
        await event.message.reply(f"Set welcome channel to <#{channel_id}>")
    
    elif mode == "view":
        [channel_id] = db.execute("select welcome_channel_id from server_settings where server_id = ?", [server_id]).fetchone()
        if channel_id is None:
            await event.message.reply(f"Welcome channel does not exist")
            return
        
        await event.message.reply(f"Welcome channel is: <#{channel_id}>")

    elif mode == "disable":
        # Placeholder for disabling welcome channel
        await event.message.reply("Welcome channel disable functionality not yet implemented.")
    
    else:
        await event.message.reply("Invalid mode. Use `set {channel}`, `view`, or `disable`.")


async def settings_welcome_image(event: stoat.MessageCreateEvent, db: sqlite3.Cursor, client: stoat.Client, args: list[str]):
    """Manage the welcome image for new member messages."""
    
    if not args:
        await event.message.reply("Please specify a mode: `set {image_url}`, `view`, or `remove`")
        return
    
    mode = args[0].lower()
    server_id = event.message.get_server()[1]
    
    if mode == "set":
        attachments = event.message.attachments
        if len(attachments) < 1:
            await event.message.reply("Please attach an image.")
            return
        
        asset = attachments[0]

        # Logging for testing purposes
        print(f"[Attachment details] Content type: {asset.content_type}, tags: {asset.tag}, metadata: {asset.metadata}")

        allowed_datatypes = [
            "image/jpeg",
            "image/jpg",
            "image/png",
        ]

        if not allowed_datatypes.__contains__(asset.content_type):
            await event.message.reply(f"Incorrect type, these are the allowed image types: {allowed_datatypes.__str__()}")

        byte_data = await asset.read()
        
        if byte_data is None:
            await event.message.reply("There was an error parsing the image")

        db.execute("update server_settings set welcome_image_blob = ? where server_id = ?", [byte_data, server_id])
        db.connection.commit()
        await event.message.reply("Updated welcome image!")
    
    elif mode == "view":
        (welcome_image_blob,) = db.execute("select welcome_image_blob from server_settings where server_id = ?;", [server_id]).fetchone()
        if welcome_image_blob is None:
            await event.message.reply("There's no welcome image currently.")
            return
        await event.message.reply("Here's the current welcome image!", attachments=[cast(stoat.ResolvableResource, welcome_image_blob)])
    
    elif mode == "remove":
        # Placeholder for removing welcome image
        await event.message.reply("Welcome image remove functionality not yet implemented.")
    
    else:
        await event.message.reply("Invalid mode. Use `set {image_url}`, `view`, or `remove`.")


async def settings_fact_chance(event: stoat.MessageCreateEvent, db: sqlite3.Cursor, client: stoat.Client, args: list[str]):
    """Manage the fact chance percentage for welcome messages."""
    
    if not args:
        await event.message.reply("Please specify a mode: `set {percentage}` or `view`")
        return
    
    mode = args[0].lower()
    server_id = event.message.get_server()[1]
    
    if mode == "set":
        if len(args) < 2:
            await event.message.reply("Please provide a percentage (0-100) for the fact chance.")
            return
        
        try:
            percentage = int(args[1])
            if 0 <= percentage <= 100:
                # Placeholder for setting fact chance
                await event.message.reply(f"Fact chance functionality not yet implemented. Would set to {percentage}%.")
            else:
                await event.message.reply("Percentage must be between 0 and 100.")
        except ValueError:
            await event.message.reply("Please provide a valid number for the percentage.")
    
    elif mode == "view":
        # Placeholder for viewing fact chance
        await event.message.reply("Fact chance view functionality not yet implemented.")
    
    else:
        await event.message.reply("Invalid mode. Use `set {percentage}` or `view`.")