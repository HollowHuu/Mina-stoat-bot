import sqlite3
import time

import stoat


async def track_message(db: sqlite3.Cursor, event: stoat.MessageCreateEvent):
    if event.message.content.lower().__contains__("streak"):
        # We don't appreciate the word streak here
        return

    member = event.message.author_as_member
    if member is None:
        return

    db.execute(
        "insert or ignore into user_stats (user_id) values (?)",
        [member.id],
    )

    message_length = len(event.message.content)

    db.execute(
        "update user_stats set messages_sent = messages_sent + 1, total_message_length = total_message_length + ? where user_id = ?",
        [message_length, member.id],
    )

    update_streak(db, member.id)


def update_streak(db: sqlite3.Cursor, user_id: str):
    now = int(time.time())

    # This may be some of the funkiest shit I've written yet
    db.execute(
        """
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
    """,
        (now, user_id),
    )

    db.connection.commit()
