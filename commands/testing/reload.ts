import type { Command, Context } from "../../types/types.ts";
import loadCommands from "../../modules/loadCommands.ts";
import { commands } from "../../globals.ts";

const command: Command = {
  data: {
    name: "reload",
  },
  async execute(ctx: Context) {
    await loadCommands();

    ctx.message?.reply(`Reloaded ${ctx.commands.size} commands!`);
  },
};

export default command;
