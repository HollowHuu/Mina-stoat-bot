import { Client, Collection, Message } from "revolt.js";
import fs from "node:fs";
import path, { dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";
import sqlite3 from "sqlite3";
import { open } from "sqlite";

import { configDotenv } from "dotenv";

import type { Command, Context } from "./types/types.ts";
import loadCommands from "./modules/loadCommands.ts";
import { commands } from "./globals.ts";
import { exit } from "node:process";
import { trackMessage } from "./modules/stats.ts";

configDotenv({
  path: ".env.local",
});

if (!process.env.SQLITE_DB_PATH) {
  console.log("Missing SQLITE_DB_PATH");
  exit();
}

const db = await open({
  filename: process.env.SQLITE_DB_PATH,
  driver: sqlite3.Database,
});

const prefix = "!";

let client = new Client();

client.on("ready", async () => {
  console.info(`Logged in as ${client.user?.username}!`);
  await loadCommands();
});

client.on("messageCreate", async (message) => {
  console.log(`Message received: ${message.content}`);

  if (message.content.startsWith(prefix)) {
    let commandName = message.content.split(" ")[0].replace(prefix, "");
    let command = commands.get(commandName);
    if (!command) {
      await message.reply(`Unable to find command ${commandName}`);
    }

    try {
      await command?.execute(getContext((message = message)));
    } catch (e) {
      await message.reply("There was an error while executing the command");
      return;
    }
  } else {
    // This is just a normal message
    await trackMessage(db, message);
  }
});

client.loginBot(process.env.BOT_TOKEN ?? "");

function getContext(message: Message | null = null): Context {
  let context: Context = {
    message: message,
    client: client,
    commands: commands,
    db: db,
  };

  return context;
}
