import database


class NotesManager:
    def __init__(self):
        database.initialize_database()

    def get_notes(self):
        return database.get_all_notes()

    def get_note(self, note_id):
        return database.get_note(note_id)

    def save(self, note_data):
        return database.save_note(note_data)

    def delete(self, note_id):
        database.delete_note(note_id)

    def get_categories(self):
        return database.get_categories()
