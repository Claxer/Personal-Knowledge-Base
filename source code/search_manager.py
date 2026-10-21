def search_notes(search_text, category="All", note_type="All", favorites_only=False):
    from notes_manager import get_notes
    return get_notes(search_text, category, note_type, favorites_only)
