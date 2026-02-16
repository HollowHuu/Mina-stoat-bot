import stoat
from dotenv import load_dotenv
import os
import random
import json
from typing import cast
from pathlib import Path
import importlib

async def handle_fact(context):
    random_chance = random.randrange(start=0, stop=100_000, step=1) # Cant have steps of floats in randrange
    chance = context['CHANCE']
    event = context['EVENT']
    facts = context['FACTS']
    last_fact = context['LAST_FACT']

    if random_chance <= chance:

        if last_fact >= len(facts) - 1:
            last_fact = -1

        print(f'Chance hit! Sending fact: {facts[last_fact + 1]}')
        # await event.message.reply(f'Did you know: *{facts[last_fact + 1]}*')
        
        last_fact += 1