import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "knowledge_base.db"


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database():
    with get_connection() as connection:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL DEFAULT '',
                category TEXT NOT NULL DEFAULT 'General',
                tags TEXT NOT NULL DEFAULT '',
                language TEXT NOT NULL DEFAULT 'Text',
                note_type TEXT NOT NULL DEFAULT 'Note',
                favorite INTEGER NOT NULL DEFAULT 0,
                pinned INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
        """)
        connection.execute("""
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT NOT NULL
            )
        """)
        # Add columns if the database came from an older version.
        columns = {row["name"] for row in connection.execute("PRAGMA table_info(notes)")}
        migrations = {
            "category": "TEXT NOT NULL DEFAULT 'General'",
            "tags": "TEXT NOT NULL DEFAULT ''",
            "language": "TEXT NOT NULL DEFAULT 'Text'",
            "note_type": "TEXT NOT NULL DEFAULT 'Note'",
            "favorite": "INTEGER NOT NULL DEFAULT 0",
            "pinned": "INTEGER NOT NULL DEFAULT 0",
            "created_at": "TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP",
            "updated_at": "TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP",
        }
        for name, definition in migrations.items():
            if name not in columns:
                connection.execute(f"ALTER TABLE notes ADD COLUMN {name} {definition}")
        connection.commit()
