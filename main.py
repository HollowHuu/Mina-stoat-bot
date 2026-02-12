import stoat
from dotenv import load_dotenv
import os
import random

load_dotenv()

client = stoat.Client()

# Constants
CHANCE = 0.01
LAST_FACT = 0

@client.on(stoat.ReadyEvent)
async def on_ready(event, /):
    print(f'We have logged in as {event.me.tag}')

@client.on(stoat.MessageCreateEvent)
async def on_message(event, /):
    message = event.message

    if message.author.relationship is stoat.RelationshipStatus.user:
        return



client.run(os.environ['BOT_TOKEN'])

async def handle_fact(event):
    print("")