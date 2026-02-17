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
    event: stoat.MessageCreateEvent = context['EVENT']
    db = context['DB']

    if event is None:
        print("No event provided in context for handle_fact. Skipping fact handling.")
        return
    
    facts = db.execute(f'SELECT fact FROM facts where server_id = "{event.message.get_server()[1]}"').fetchall()
    (last_fact, chance) = db.execute(f'SELECT last_fact, fact_chance FROM server_settings where server_id = "{event.message.get_server()[1]}"').fetchone()

    if last_fact is None:
        last_fact = -1
        # server_settings entry doesn't exist for this server, create it
        db.execute(f'INSERT INTO server_settings (server_id) VALUES ("{event.message.get_server()[1]}")')
        db.connection.commit()
    else:
        print(f'Last fact index: {last_fact}, Chance: {chance}, Random Chance: {random_chance}')

    if random_chance <= chance:

        if last_fact >= len(facts) - 1:
            last_fact = -1

        # We do some string manipulation since the fact output looks like this ('test fact',)
        fact = facts[last_fact + 1][0]

        print(f'Chance hit! Sending fact: {fact}')
        await event.message.reply(f'Did you know: *{fact}*')
        
        last_fact += 1
        db.execute(f'UPDATE server_settings SET last_fact = {last_fact} WHERE server_id = "{event.message.get_server()[1]}"')
        db.connection.commit()