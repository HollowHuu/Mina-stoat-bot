import { Client, Message } from "revolt.js";

export interface Command {
  data: {
    name: string;
  };
  execute(ctx: Context): Promise<void>;
}

export interface Context {
  message: Message | null;
  client: Client;
  commands: Map<string, Command>;
}
