import type { Command, Context } from "../../types/types.ts";

const command: Command = {
  data: {
    name: "test",
  },
  async execute(ctx: Context) {
    let msg = ctx.message;
    console.log(ctx.message?.author?.username);
    console.log("hmmm");
  },
};

export default command;
