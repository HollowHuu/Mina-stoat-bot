import { Client, Collection, Message } from "revolt.js";
import fs from "node:fs";
import path, { dirname } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

import { config, configDotenv } from "dotenv";

import type { Command, Context } from "./types/types.ts";
import loadCommands from "./modules/loadCommands.ts";
import { commands } from "./command.ts";

configDotenv({
  path: ".env.local",
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
  }
});

client.loginBot(process.env.BOT_TOKEN ?? "");

function getContext(message: Message | null = null): Context {
  let context: Context = {
    message: message,
    client: client,
    commands: commands,
  };

  return context;
}
