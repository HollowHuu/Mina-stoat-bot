import stoat
from dotenv import load_dotenv
import os
import random
import json
from typing import cast

load_dotenv()

client = stoat.Client()

# Constants
CHANCE = 1000
LAST_FACT = -1
FACTS_FILE = 'facts.json'
PREFIX = '!'

FACTS = []

@client.on(stoat.ReadyEvent)
async def on_ready(event: stoat.ReadyEvent, /):
    global FACTS
    print(f'We have logged in as {event.me.tag}')

    FACTS = await load_facts()
    print(f'Loaded {len(FACTS)} facts.')

    global WELCOME_IMAGE_BYTES
    with open('welcome_image.jpg', 'rb') as f:
        WELCOME_IMAGE_BYTES = f.read()

@client.on(stoat.MessageCreateEvent)
async def on_message(event: stoat.MessageCreateEvent, /):
    message = event.message

    if message.author.relationship is stoat.RelationshipStatus.user:
        return
    
    if message.content.startswith(PREFIX):
        command = message.content[len(PREFIX):].split()[0]

        if command == 'reload':
            await load_facts()
            await message.reply(f'Reloaded {len(FACTS)} facts.')
        
        if command == 'test_join':
            await event.message.channel.send(f"Welcome to the gang {event.message.author.mention}", attachments=[
                cast(stoat.ResolvableResource, WELCOME_IMAGE_BYTES)
            ])
    else:
        await handle_fact(event)

@client.on(stoat.ServerMemberJoinEvent)
async def on_member_join(event: stoat.ServerMemberJoinEvent, /):
   await event.member.send(f"Welcome to the gang {event.member.mention}", attachments=[
        cast(stoat.ResolvableResource, WELCOME_IMAGE_BYTES)
    ])

async def handle_fact(event: stoat.MessageCreateEvent):
    random_chance = random.randrange(start=0, stop=100_000, step=1) # Cant have steps of floats in randrange
    if random_chance <= CHANCE:
        global LAST_FACT

        if LAST_FACT >= len(FACTS) - 1:
            LAST_FACT = -1

        await event.message.reply(f'Did you know: *{FACTS[LAST_FACT + 1]}*')
        
        LAST_FACT += 1

async def load_facts():
    
    file = open(FACTS_FILE, 'r', encoding='utf-8')
    return json.load(file)

client.run(os.environ['BOT_TOKEN'])