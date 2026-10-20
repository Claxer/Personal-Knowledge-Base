
import sqlite3
from datetime import datetime

DATABASE_NAME = "knowledge_base.db"


def get_connection():
    connection = sqlite3.connect(DATABASE_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_database():
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'General',
            tags TEXT DEFAULT '',
            content TEXT DEFAULT '',
            note_type TEXT DEFAULT 'Note',
            language TEXT DEFAULT 'python',
            is_favorite INTEGER DEFAULT 0,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    connection.commit()
    connection.close()


def get_all_notes():
    connection = get_connection()
    cursor = connection.execute(
        "SELECT * FROM notes ORDER BY updated_at DESC"
    )
    notes = [dict(row) for row in cursor.fetchall()]
    connection.close()
    return notes


def get_note(note_id):
    connection = get_connection()
    cursor = connection.execute(
        "SELECT * FROM notes WHERE id = ?",
        (note_id,)
    )
    row = cursor.fetchone()
    connection.close()

    if row:
        return dict(row)

    return None


def save_note(note_data):
    connection = get_connection()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    title = note_data["title"].strip()
    category = note_data["category"].strip() or "General"
    tags = note_data.get("tags", "").strip()
    content = note_data.get("content", "")
    note_type = note_data.get("note_type", "Note")
    language = note_data.get("language", "python")
    is_favorite = int(note_data.get("is_favorite", 0))
    note_id = note_data.get("id")

    if not title:
        connection.close()
        raise ValueError("The note title cannot be empty.")

    if note_id:
        connection.execute("""
            UPDATE notes
            SET title = ?,
                category = ?,
                tags = ?,
                content = ?,
                note_type = ?,
                language = ?,
                is_favorite = ?,
                updated_at = ?
            WHERE id = ?
        """, (
            title, category, tags, content, note_type,
            language, is_favorite, now, note_id
        ))
    else:
        cursor = connection.execute("""
            INSERT INTO notes (
                title, category, tags, content, note_type,
                language, is_favorite, created_at, updated_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            title, category, tags, content, note_type,
            language, is_favorite, now, now
        ))

        note_id = cursor.lastrowid

    connection.commit()
    connection.close()

    return note_id


def delete_note(note_id):
    connection = get_connection()
    connection.execute(
        "DELETE FROM notes WHERE id = ?",
        (note_id,)
    )
    connection.commit()
    connection.close()


def get_categories():
    connection = get_connection()
    cursor = connection.execute("""
        SELECT DISTINCT category
        FROM notes
        WHERE category != ''
        ORDER BY category COLLATE NOCASE
    """)

    categories = [row["category"] for row in cursor.fetchall()]
    connection.close()

    return categories
