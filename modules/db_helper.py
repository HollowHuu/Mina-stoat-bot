import sqlite3
import os

async def update_field(db: sqlite3.Cursor, pk, field, value) -> bool:
    """Update a specific field in the server_settings table for a given server_id."""

    try:
        db.execute(f'UPDATE server_settings SET {field} = ? WHERE server_id = ?', (value, pk))
        db.connection.commit()

    except Exception as e:
        print(f"Error updating {field} for server_id {pk}: {e}")
        return False
    
    return True