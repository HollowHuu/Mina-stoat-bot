import { Client, Message } from "revolt.js";
import { Database } from "sqlite";
import sqlite3 from "sqlite3";

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
  db: Database<sqlite3.Database, sqlite3.Statement>;
}

// Database models
export interface UserStats {
  user_id: string;
  messages_sent: number;
  total_message_length: number;
  time_spent_in_voice: number;
  people_invited: number;
  current_streak: number;
  longest_streak: number;
  last_message_timestamp: number;
}

export interface ServerSettings {
  server_id: string;
  welcome_message: string;
  welcome_channel_id: string | undefined;
  welcome_image_blob: Blob | undefined;
  last_fact: number;
  fact_chance: number;
}

export interface Facts {
  id: number;
  server_id: string;
  fact: string;
}

export interface RoleMenus {
  message_id: string;
  channel_id: string;
}

export interface Roles {
  role_id: string;
  role_menu_id: string;
  reaction_id: string;
}
