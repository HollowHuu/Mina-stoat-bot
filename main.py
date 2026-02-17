import stoat
from dotenv import load_dotenv
import os
from typing import cast
import sqlite3

# Modules
from modules.load_commands import load_commands
from modules.handle_fact import handle_fact

load_dotenv()

client = stoat.Client()

# Constants
CHANCE = 1000
LAST_FACT = -1

global FACTS_FILE
FACTS_FILE = 'facts.json'
PREFIX = '!'

FACTS = []


@client.on(stoat.ReadyEvent)
async def on_ready(event: stoat.ReadyEvent, /):
    print(f'We have logged in as {event.me.tag}')

    global commands
    commands = load_commands()
    print(f'Loaded {len(commands)} commands.')

    # Prepare Database
    global db
    db = sqlite3.connect(os.environ['SQLITE_DB_PATH']).cursor()

    global WELCOME_IMAGE_BYTES
    with open('welcome_image.jpg', 'rb') as f:
        WELCOME_IMAGE_BYTES = f.read()

    print('Bot is ready!')

@client.on(stoat.MessageCreateEvent)
async def on_message(event: stoat.MessageCreateEvent, /):
    message = event.message
    print(f'Message from {message.author.tag}: {message.content}')

    if message.author.relationship is stoat.RelationshipStatus.user:
        return
    
    if message.content.startswith(PREFIX):
        command = message.content[len(PREFIX):].split()[0]

        if command in commands:
            await commands[command](get_context(event))
        
        if command == 'test':
            await event.message.channel.send(f"Welcome to the gang {event.message.author.mention}", attachments=[
                cast(stoat.ResolvableResource, WELCOME_IMAGE_BYTES)
            ])
            print(len(FACTS))
    else:
        await handle_fact(get_context(event))

@client.on(stoat.ServerMemberJoinEvent)
async def on_member_join(event: stoat.ServerMemberJoinEvent, /):

    print(f'Member {event.member.tag} joined server {event.member.server_id}')

    (welcome_message, welcome_channel_id, welcome_image_blob) = db.execute('SELECT welcome_message, welcome_channel, welcome_image FROM server_settings WHERE server_id = ?', (event.member.server_id,)).fetchone()

    welcome_message = welcome_message.replace('{user}', event.member.mention)

    print(WELCOME_IMAGE_BYTES)

    await event.member.send(welcome_message, attachments=[
        cast(stoat.ResolvableResource, WELCOME_IMAGE_BYTES)
    ])

def get_context(event = None):
    """Return context dict with shared data for commands."""
    return {
        'EVENT': event, # Represents some kind of stoat event, can be used by commands to access event data if needed
        'DB': db,
        'CLIENT': client,
        'COMMANDS': commands,
    }

client.run(os.environ['BOT_TOKEN'])