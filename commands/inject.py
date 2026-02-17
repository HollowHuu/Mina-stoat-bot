import sqlite3

from modules.check_owner import check_bot_owner


async def inject(context):
    """Injects SQL into the database. Expects context dict with 'DB', 'CLIENT' and 'EVENT' keys."""
    db: sqlite3.Cursor = context['DB']
    event = context['EVENT']

    if event is None:
        print("No event provided in context for inject. Skipping SQL injection.")
        return
    
    if not await check_bot_owner(context):
        return
    
    # We dont care about safety here, just execute raw SQL for testing purposes
    sql = event.message.content[len('!inject '):].strip()
    try:
        cursor_result = db.execute(sql)
        db.connection.commit()
        
        # Try to fetch results if this was a SELECT query
        try:
            results = cursor_result.fetchall()
            if results:
                response = f"SQL executed successfully.\nResults:\n{results}"
            else:
                response = "SQL executed successfully. No results returned."
        except sqlite3.ProgrammingError:
            # No results to fetch (INSERT, UPDATE, DELETE, etc.)
            response = f"SQL executed successfully. Rows affected: {db.rowcount}"
        
        print(response)
        await event.message.reply(response)
    except Exception as e:
        print(f"Error executing SQL: {e}")
        await event.message.reply(f"Error executing SQL: {e}")



     