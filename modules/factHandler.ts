import { Context, ServerSettings } from "../types/types";

// TODO - Optimise the DB calls
async function factHandler(ctx: Context) {
  const randomChance = Math.random() * 100;
  const db = ctx.db;
  const msg = ctx.message;

  if (!msg) return;

  let server = msg.server;
  if (!server) {
    console.log("Couldn't find server.");
    return;
  }

  let serverSettings: ServerSettings | undefined = await db.get(
    "select * from server_settings where server_id = ?;",
    [server.id],
  );

  if (!serverSettings) {
    await db.run("insert into server_settings (server_id) values (?);", [
      server.id,
    ]);
    serverSettings = await db.get(
      "select * from server_settings where server_id = ?;",
      [server.id],
    );
  }

  if (!serverSettings) return; // Atp there is probably an issue with the server
  console.log(serverSettings);

  // TODO - check if chance matches, then fetch facts, send next in line
}

export default factHandler;
