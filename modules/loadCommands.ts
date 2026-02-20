import path, { dirname } from "node:path";
import fs from "node:fs";
import { pathToFileURL, fileURLToPath } from "node:url";

import type { Command } from "../types/types.ts";
import { commands } from "../globals.ts";

export default async function loadCommands() {
  commands.clear(); // In case of reload

  const __dirname = dirname(fileURLToPath(import.meta.url));
  const commandsPath = path.join(__dirname, "../commands");
  const subdirs = fs
    .readdirSync(commandsPath)
    .filter((file) => fs.statSync(path.join(commandsPath, file)).isDirectory());

  for (const subdir of subdirs) {
    const subdirPath = path.join(commandsPath, subdir);
    const commandFiles = fs
      .readdirSync(subdirPath)
      .filter((file) => file.endsWith(".ts"));
    for (const file of commandFiles) {
      const filePath = path.join(subdirPath, file);

      try {
        const module = await import(
          pathToFileURL(filePath).href + `?update=${Date.now()}` // We need node to treat it like a new module
        );
        const command: Command = module.default;

        commands.set(command.data.name, command);
        console.log(`[INFO] loaded command: ${command.data.name}`);
      } catch (err) {
        console.log(
          `[ERROR] failed to load command from: ${file}\nError: ${err} `,
        );
        continue;
      }
    }
  }
}
