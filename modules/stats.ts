import { Message } from "revolt.js";
import { Database } from "sqlite";
import sqlite3 from "sqlite3";

export async function trackMessage(db: Database, message: Message) {
  let msg = message.content;
  if (msg.toLowerCase().includes("streak")) return;

  const member = message.member;
  if (!member) return;

  await db.run("insert or ignore into user_stats (user_id) values (?)", [
    member.id.user,
  ]);

  await db.run(
    "update user_stats set messages_sent = messages_sent + 1, total_message_length = total_message_length + ? where user_id = ?;",
    [msg.length, member.id.user],
  );

  await updateStreak(db, member.id.user);
}

async function updateStreak(db: Database, userId: string) {
  const now = Date.now();
  await db.run(
    `
    UPDATE user_stats
      SET
          current_streak =
              CASE
                  WHEN DATE(last_message_timestamp, 'unixepoch') = DATE('now')
                      THEN current_streak
                  WHEN DATE(last_message_timestamp, 'unixepoch') = DATE('now', '-1 day')
                      THEN current_streak + 1
                  ELSE 1
              END,
          longest_streak =
              MAX(
                  longest_streak,
                  CASE
                      WHEN DATE(last_message_timestamp, 'unixepoch') = DATE('now')
                          THEN current_streak
                      WHEN DATE(last_message_timestamp, 'unixepoch') = DATE('now', '-1 day')
                          THEN current_streak + 1
                      ELSE 1
                  END
              ),
          last_message_timestamp = ?
      WHERE user_id = ?
    `,
    [now, userId],
  );
}
