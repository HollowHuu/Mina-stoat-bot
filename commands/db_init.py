import sqlite3
import os
import json
import stoat


async def init_db(context):
    db: sqlite3.Cursor = context['DB']
    db.execute('''CREATE TABLE IF NOT EXISTS facts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        server_id TEXT NOT NULL,
        fact TEXT NOT NULL
    )''')
    # create server settings table with server_id, welcome_message, welcome_channel_id, welcome_image_url and last_fact columns 

