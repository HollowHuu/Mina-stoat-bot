import type { Command, Context, UserStats } from "../../types/types.ts";

const command: Command = {
  data: {
    name: "test",
  },
  async execute(ctx: Context) {
    let msg = ctx.message;
    console.log(ctx.message?.author?.username);
    console.log("hmmm");

    let db = ctx.db;
    let stats: UserStats[] = await db.all("select * from user_stats;");
    console.log(stats[0].user_id);
  },
};

export default command;
