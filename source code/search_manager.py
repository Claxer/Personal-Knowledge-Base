def filter_notes(notes, search_text="", category="All Notes",
                 favorites_only=False):

    search_text = search_text.strip().lower()
    filtered_notes = []

    for note in notes:
        if favorites_only and not note["is_favorite"]:
            continue

        if category == "Favorites" and not note["is_favorite"]:
            continue

        if category not in ("All Notes", "Favorites"):
            if note["category"].lower() != category.lower():
                continue

        searchable_text = (
            note["title"] + " " +
            note["content"] + " " +
            note["category"] + " " +
            note["tags"]
        ).lower()

        if search_text and search_text not in searchable_text:
            continue

        filtered_notes.append(note)

    return filtered_notes
