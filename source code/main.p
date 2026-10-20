import customtkinter as ctk
from tkinter import messagebox

from notes_manager import NotesManager
from sidebar import Sidebar
from note_editor import NoteEditor
from search_manager import filter_notes


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class PersonalKnowledgeBase(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Personal Knowledge Base")
        self.geometry("1250x780")
        self.minsize(1000, 650)
        self.configure(fg_color="#111111")

        self.notes_manager = NotesManager()
        self.selected_category = "All Notes"
        self.all_notes = []

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(
            self,
            on_filter=self.change_filter
        )
        self.sidebar.grid(
            row=0, column=0, sticky="ns"
        )

        self.main_frame = ctk.CTkFrame(
            self,
            fg_color="#111111",
            corner_radius=0
        )
        self.main_frame.grid(
            row=0, column=1, sticky="nsew",
            padx=20, pady=15
        )

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)

        self.create_header()
        self.create_workspace()
        self.refresh_notes()

    def create_header(self):
        header = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        header.grid(
            row=0, column=0, sticky="ew",
            pady=(0, 15)
        )

        header.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            header,
            text="Your Knowledge",
            font=("Arial", 26, "bold"),
            text_color="#F5F5F5"
        ).grid(row=0, column=0, sticky="w")

        self.search_entry = ctk.CTkEntry(
            header,
            width=250,
            height=38,
            placeholder_text="Search notes, tags, content...",
            fg_color="#222222",
            border_color="#393939"
        )
        self.search_entry.grid(
            row=0, column=1, padx=(10, 0)
        )
        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.refresh_notes()
        )

    def create_workspace(self):
        workspace = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )
        workspace.grid(
            row=1, column=0, sticky="nsew"
        )

        workspace.grid_columnconfigure(1, weight=1)
        workspace.grid_rowconfigure(0, weight=1)

        self.notes_panel = ctk.CTkFrame(
            workspace,
            width=270,
            fg_color="#1A1A1A",
            corner_radius=10
        )
        self.notes_panel.grid(
            row=0, column=0, sticky="nsew",
            padx=(0, 12)
        )
        self.notes_panel.grid_propagate(False)
        self.notes_panel.grid_rowconfigure(1, weight=1)
        self.notes_panel.grid_columnconfigure(0, weight=1)

        self.notes_heading = ctk.CTkLabel(
            self.notes_panel,
            text="ALL NOTES",
            font=("Arial", 12, "bold"),
            text_color="#AAAAAA"
        )
        self.notes_heading.grid(
            row=0, column=0, sticky="w",
            padx=15, pady=15
        )

        self.notes_list = ctk.CTkScrollableFrame(
            self.notes_panel,
            fg_color="transparent"
        )
        self.notes_list.grid(
            row=1, column=0, sticky="nsew",
            padx=8, pady=(0, 8)
        )

        self.editor = NoteEditor(
            workspace,
            on_save=self.save_current_note,
            on_delete=self.delete_current_note,
            on_new=self.new_note
        )
        self.editor.grid(
            row=0, column=1, sticky="nsew"
        )

        self.status_label = ctk.CTkLabel(
            self.main_frame,
            text="Your notes are stored locally.",
            font=("Arial", 11),
            text_color="#777777"
        )
        self.status_label.grid(
            row=2, column=0, sticky="w", pady=(10, 0)
        )

    def change_filter(self, category):
        self.selected_category = category

        self.notes_heading.configure(
            text=category.upper()
        )

        self.refresh_notes()

    def refresh_notes(self, select_id=None):
        self.all_notes = self.notes_manager.get_notes()

        categories = self.notes_manager.get_categories()
        self.sidebar.update_categories(categories)

        search_text = self.search_entry.get()

        filtered_notes = filter_notes(
            self.all_notes,
            search_text=search_text,
            category=self.selected_category,
            favorites_only=(
                self.selected_category == "Favorites"
            )
        )

        for widget in self.notes_list.winfo_children():
            widget.destroy()

        if not filtered_notes:
            ctk.CTkLabel(
                self.notes_list,
                text="No notes found.",
                text_color="#777777",
                wraplength=200
            ).pack(pady=20)
        else:
            for note in filtered_notes:
                self.create_note_item(note)

        self.status_label.configure(
            text=(
                f"{len(self.all_notes)} total notes  •  "
                f"{len(filtered_notes)} shown"
            )
        )

        if select_id is not None:
            note = self.notes_manager.get_note(select_id)

            if note:
                self.editor.load_note(note)

    def create_note_item(self, note):
        card = ctk.CTkFrame(
            self.notes_list,
            fg_color="#262626",
            corner_radius=8
        )
        card.pack(fill="x", pady=4, padx=2)

        favorite_symbol = "★ " if note["is_favorite"] else ""

        title_button = ctk.CTkButton(
            card,
            text=favorite_symbol + note["title"],
            anchor="w",
            fg_color="transparent",
            hover_color="#353535",
            text_color="#EEEEEE",
            font=("Arial", 12, "bold"),
            height=32,
            command=lambda note_id=note["id"]: (
                self.select_note(note_id)
            )
        )
        title_button.pack(fill="x", padx=5, pady=(5, 0))

        ctk.CTkLabel(
            card,
            text=(
                f'{note["category"]}  •  '
                f'{note["note_type"]}'
            ),
            anchor="w",
            text_color="#999999",
            font=("Arial", 10)
        ).pack(fill="x", padx=10, pady=(0, 3))

        if note["tags"].strip():
            ctk.CTkLabel(
                card,
                text=note["tags"],
                anchor="w",
                text_color="#777777",
                font=("Arial", 10),
                wraplength=220
            ).pack(fill="x", padx=10, pady=(0, 6))

    def select_note(self, note_id):
        note = self.notes_manager.get_note(note_id)

        if note:
            self.editor.load_note(note)

    def new_note(self):
        self.editor.clear_editor()
        self.status_label.configure(
            text="Creating a new note..."
        )

    def save_current_note(self):
        note_data = self.editor.get_data()

        try:
            note_id = self.notes_manager.save(note_data)

            self.refresh_notes(select_id=note_id)

            self.status_label.configure(
                text="Note saved successfully."
            )

        except ValueError as error:
            messagebox.showwarning(
                "Missing Title",
                str(error)
            )

        except Exception as error:
            messagebox.showerror(
                "Save Error",
                f"Could not save the note:\n{error}"
            )

    def delete_current_note(self):
        note_id = self.editor.current_note_id

        if note_id is None:
            messagebox.showinfo(
                "Delete Note",
                "Select a saved note before deleting."
            )
            return

        confirm = messagebox.askyesno(
            "Delete Note",
            "Are you sure you want to delete this note?"
        )

        if confirm:
            try:
                self.notes_manager.delete(note_id)
                self.editor.clear_editor()
                self.refresh_notes()

                self.status_label.configure(
                    text="Note deleted successfully."
                )

            except Exception as error:
                messagebox.showerror(
                    "Delete Error",
                    f"Could not delete the note:\n{error}"
                )


if __name__ == "__main__":
    app = PersonalKnowledgeBase()
    app.mainloop()
