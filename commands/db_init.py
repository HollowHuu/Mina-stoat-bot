import json
import os
import sqlite3

import stoat

from modules.check_owner import check_bot_owner


async def db_init(context):

    event: stoat.MessageCreateEvent = context["EVENT"]

    if not await check_bot_owner(context):
        return

    db: sqlite3.Cursor = context["DB"]
    db.execute("""CREATE TABLE IF NOT EXISTS facts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        server_id TEXT NOT NULL,
        fact TEXT NOT NULL
    )""")

    db.execute("""CREATE TABLE IF NOT EXISTS server_settings (
        server_id TEXT PRIMARY KEY,
        welcome_message TEXT,
        welcome_channel_id TEXT,
        welcome_image_blob BLOB,
        welcome_message_enabled INTEGER DEFAULT 0,
        last_fact INTEGER DEFAULT -1
        fact_chance INTEGER DEFAULT 1000
    )""")

    db.execute("""CREATE TABLE IF NOT EXISTS user_stats (
        user_id TEXT PRIMARY KEY,
        messages_sent INTEGER DEFAULT 0,
        total_message_length INTEGER DEFAULT 0,
        time_spent_in_voice INTEGER DEFAULT 0,
        people_invited INTEGER DEFAULT 0,
        current_streak INTEGER DEFAULT 0,
        longest_streak INTEGER DEFAULT 0,
        last_message_timestamp INTEGER DEFAULT 0
    )""")

    db.connection.commit()

    await event.message.reply("Database initialized successfully.")
