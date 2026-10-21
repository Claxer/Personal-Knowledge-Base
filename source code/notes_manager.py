from database import get_connection


def get_notes(search="", category="All", note_type="All", favorites_only=False):
    query = "SELECT * FROM notes WHERE 1=1"
    params = []
    if search.strip():
        term = f"%{search.strip()}%"
        query += " AND (title LIKE ? OR content LIKE ? OR category LIKE ? OR tags LIKE ? OR language LIKE ?)"
        params.extend([term, term, term, term, term])
    if category and category != "All":
        query += " AND category = ?"
        params.append(category)
    if note_type and note_type != "All":
        query += " AND note_type = ?"
        params.append(note_type)
    if favorites_only:
        query += " AND favorite = 1"
    query += " ORDER BY pinned DESC, favorite DESC, updated_at DESC"
    with get_connection() as connection:
        return connection.execute(query, params).fetchall()


def get_note(note_id):
    with get_connection() as connection:
        return connection.execute("SELECT * FROM notes WHERE id = ?", (note_id,)).fetchone()


def save_note(note_id, title, content, category, tags, language, note_type, favorite, pinned):
    title = title.strip()
    if not title:
        raise ValueError("Please enter a title.")
    with get_connection() as connection:
        if note_id:
            connection.execute("""
                UPDATE notes
                SET title=?, content=?, category=?, tags=?, language=?, note_type=?,
                    favorite=?, pinned=?, updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            """, (title, content, category, tags, language, note_type,
                  int(favorite), int(pinned), note_id))
            saved_id = note_id
        else:
            cursor = connection.execute("""
                INSERT INTO notes
                (title, content, category, tags, language, note_type, favorite, pinned)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (title, content, category, tags, language, note_type,
                  int(favorite), int(pinned)))
            saved_id = cursor.lastrowid
        connection.commit()
        return saved_id


def delete_note(note_id):
    with get_connection() as connection:
        connection.execute("DELETE FROM notes WHERE id = ?", (note_id,))
        connection.commit()


def get_categories():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT DISTINCT category FROM notes ORDER BY category COLLATE NOCASE"
        ).fetchall()
    return [row["category"] for row in rows]


def get_statistics():
    with get_connection() as connection:
        total = connection.execute("SELECT COUNT(*) FROM notes").fetchone()[0]
        snippets = connection.execute("SELECT COUNT(*) FROM notes WHERE note_type='Code Snippet'").fetchone()[0]
        favorites = connection.execute("SELECT COUNT(*) FROM notes WHERE favorite=1").fetchone()[0]
        categories = connection.execute("SELECT COUNT(DISTINCT category) FROM notes").fetchone()[0]
        recent = connection.execute(
            "SELECT id, title, category, note_type, updated_at FROM notes ORDER BY updated_at DESC LIMIT 5"
        ).fetchall()
    return {"total": total, "snippets": snippets, "favorites": favorites,
            "categories": categories, "recent": recent}
