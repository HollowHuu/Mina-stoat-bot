-- These are just some SQLite queries used to help me test the early stages, will be removed later


PRAGMA writable_schema = 1;
delete from sqlite_master where type in ('table', 'index', 'trigger');
PRAGMA writable_schema = 0;

VACUUM;

PRAGMA integrity_check;
PRAGMA foreign_keys = ON;


CREATE TABLE IF NOT EXISTS facts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    server_id TEXT NOT NULL,
    fact TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS server_settings (
    server_id TEXT PRIMARY KEY,
    welcome_message TEXT DEFAULT 'Welcome to the gang {user}!',
    welcome_channel_id TEXT,
    welcome_image_blob BLOB,
    last_fact INTEGER DEFAULT -1,
    fact_chance INTEGER DEFAULT 1000
);

CREATE TABLE IF NOT EXISTS user_stats (
    user_id TEXT PRIMARY KEY,
    messages_sent INTEGER DEFAULT 0,
    total_message_length INTEGER DEFAULT 0,
    time_spent_in_voice INTEGER DEFAULT 0,
    people_invited INTEGER DEFAULT 0,
    current_streak INTEGER DEFAULT 0,
    longest_streak INTEGER DEFAULT 0,
    last_message_timestamp INTEGER DEFAULT 0
);

CREATE TABLE IF NOT EXISTS role_menus (
    message_id TEXT PRIMARY KEY, -- Refers to the message that contains the embed
    channel_id TEXT NOT NULL
    -- server_id TEXT NOT NULL -- we dont need server id, it will always be accessed from the server its relevant
);

CREATE TABLE IF NOT EXISTS roles (
    role_id TEXT NOT NULL,
    role_menu_id TEXT NOT NULL,
    reaction_id TEXT NOT NULL,

    PRIMARY KEY(role_id, role_menu_id),
    FOREIGN KEY (role_menu_id) REFERENCES role_menus (message_id)
);


insert into server_settings (server_id) values ('01JQJ2A4VHNQVG50MCBF7SJW55');
insert into facts (server_id, fact) values ('01JQJ2A4VHNQVG50MCBF7SJW55', 'eggs are technically a type of meat');
insert into facts (server_id, fact) values ('01JQJ2A4VHNQVG50MCBF7SJW55', 'Please kill me');
