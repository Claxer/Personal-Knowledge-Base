import customtkinter as ctk
from tkinter import messagebox

from database import initialize_database
from notes_manager import (
    get_notes, get_note, save_note, delete_note, get_categories, get_statistics
)
from search_manager import search_notes
from sidebar import Sidebar
from note_editor import NoteEditor
from dashboard import Dashboard
from backup_manager import create_backup, restore_backup
from export_manager import export_notes

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")


class PersonalKnowledgeBase(ctk.CTk):
    def __init__(self):
        super().__init__()
        initialize_database()
        self.title("Personal Knowledge Base V2")
        self.geometry("1280x800")
        self.minsize(1000, 650)
        self.configure(fg_color="#101010")
        self.selected_note_id = None
        self.favorites_only = False
        self.dashboard_view = True

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = Sidebar(
            self, self.show_dashboard, self.show_all_notes, self.show_favorites,
            self.new_note, lambda: create_backup(self), lambda: restore_backup(self),
            lambda: export_notes(self, "json"), lambda: export_notes(self, "csv")
        )
        self.sidebar.grid(row=0, column=0, sticky="nsw")

        self.workspace = ctk.CTkFrame(self, fg_color="transparent")
        self.workspace.grid(row=0, column=1, sticky="nsew", padx=24, pady=22)
        self.workspace.grid_columnconfigure(0, weight=1)
        self.workspace.grid_rowconfigure(1, weight=1)

        self.topbar = ctk.CTkFrame(self.workspace, fg_color="transparent")
        self.topbar.grid(row=0, column=0, sticky="ew", pady=(0, 18))
        self.topbar.grid_columnconfigure(0, weight=1)
        self.search_entry = ctk.CTkEntry(
            self.topbar, placeholder_text="Search titles, notes, tags, categories...",
            height=38, width=360
        )
        self.search_entry.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda _event: self.refresh_notes())
        self.category_filter = ctk.CTkOptionMenu(
            self.topbar, values=["All"], width=145, command=lambda _value: self.refresh_notes()
        )
        self.category_filter.grid(row=0, column=1, padx=(0, 10))
        self.type_filter = ctk.CTkOptionMenu(
            self.topbar, values=["All", "Note", "Tutorial", "Code Snippet"],
            width=135, command=lambda _value: self.refresh_notes()
        )
        self.type_filter.grid(row=0, column=2, padx=(0, 10))
        self.clear_filter_button = ctk.CTkButton(
            self.topbar, text="Clear filters", width=95, command=self.clear_filters
        )
        self.clear_filter_button.grid(row=0, column=3)

        self.content_area = ctk.CTkFrame(self.workspace, fg_color="transparent")
        self.content_area.grid(row=1, column=0, sticky="nsew")
        self.content_area.grid_columnconfigure(0, weight=1)
        self.content_area.grid_rowconfigure(0, weight=1)

        self.editor = NoteEditor(self.content_area, self.save_current_note,
                                 self.delete_current_note, self.new_note)
        self.show_dashboard()
        self.refresh_category_filter()

    def _clear_content(self):
        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_dashboard(self):
        self.dashboard_view = True
        self._clear_content()
        self.topbar.grid_remove()
        dashboard = Dashboard(self.content_area, get_statistics(), self.show_all_notes)
        dashboard.grid(row=0, column=0, sticky="nsew")

    def show_all_notes(self):
        self.favorites_only = False
        self.dashboard_view = False
        self.topbar.grid()
        self._show_notes_view()

    def show_favorites(self):
        self.favorites_only = True
        self.dashboard_view = False
        self.topbar.grid()
        self._show_notes_view()

    def _show_notes_view(self):
        self._clear_content()
        view = ctk.CTkFrame(self.content_area, fg_color="transparent")
        view.grid(row=0, column=0, sticky="nsew")
        view.grid_columnconfigure(1, weight=1)
        view.grid_rowconfigure(1, weight=1)

        ctk.CTkLabel(view, text="Favorites" if self.favorites_only else "All notes",
                     font=ctk.CTkFont(size=24, weight="bold")
                     ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 14))

        list_frame = ctk.CTkFrame(view, width=260, corner_radius=10)
        list_frame.grid(row=1, column=0, sticky="nsw", padx=(0, 16))
        list_frame.grid_propagate(False)
        list_frame.configure(width=260)
        list_frame.grid_rowconfigure(0, weight=1)
        self.notes_scroll = ctk.CTkScrollableFrame(list_frame, width=238, fg_color="transparent")
        self.notes_scroll.pack(fill="both", expand=True, padx=5, pady=5)

        self.editor = NoteEditor(view, self.save_current_note, self.delete_current_note, self.new_note)
        self.editor.grid(row=1, column=1, sticky="nsew")
        self.refresh_notes()

    def refresh_category_filter(self):
        current = self.category_filter.get()
        values = ["All"] + get_categories()
        self.category_filter.configure(values=values)
        self.category_filter.set(current if current in values else "All")

    def refresh_notes(self):
        if self.dashboard_view or not hasattr(self, "notes_scroll"):
            return
        for widget in self.notes_scroll.winfo_children():
            widget.destroy()
        notes = search_notes(
            self.search_entry.get(), self.category_filter.get(), self.type_filter.get(),
            self.favorites_only
        )
        if not notes:
            ctk.CTkLabel(self.notes_scroll, text="No notes found.", text_color="gray",
                         wraplength=200).pack(padx=12, pady=20)
            return
        for note in notes:
            label = ("★ " if note["favorite"] else "") + ("📌 " if note["pinned"] else "") + note["title"]
            button = ctk.CTkButton(
                self.notes_scroll, text=label, anchor="w", height=42,
                fg_color="#303030" if note["id"] == self.selected_note_id else "transparent",
                hover_color="#292929",
                command=lambda note_id=note["id"]: self.open_note(note_id)
            )
            button.pack(fill="x", pady=2)
            ctk.CTkLabel(
                self.notes_scroll, text=f'{note["category"]} · {note["note_type"]}',
                text_color="#8b8b8b", font=ctk.CTkFont(size=10), anchor="w"
            ).pack(fill="x", padx=10, pady=(0, 5))

    def open_note(self, note_id):
        note = get_note(note_id)
        if note:
            self.selected_note_id = note_id
            self.editor.load_note(note)
            self.refresh_notes()

    def new_note(self):
        if self.dashboard_view or not hasattr(self, "notes_scroll"):
            self.show_all_notes()
        self.selected_note_id = None
        self.editor.load_note(None)
        self.refresh_notes()

    def save_current_note(self, data):
        try:
            self.selected_note_id = save_note(
                data["id"], data["title"], data["content"], data["category"],
                data["tags"], data["language"], data["note_type"],
                data["favorite"], data["pinned"]
            )
            self.refresh_category_filter()
            self.refresh_notes()
            if self.selected_note_id:
                self.editor.load_note(get_note(self.selected_note_id))
            messagebox.showinfo("Saved", "Your note has been saved.", parent=self)
        except ValueError as error:
            messagebox.showwarning("Missing title", str(error), parent=self)
        except Exception as error:
            messagebox.showerror("Save failed", f"Could not save the note:\n{error}", parent=self)

    def delete_current_note(self, note_id):
        if messagebox.askyesno("Delete note", "Are you sure you want to permanently delete this note?", parent=self):
            try:
                delete_note(note_id)
                self.selected_note_id = None
                self.editor.load_note(None)
                self.refresh_category_filter()
                self.refresh_notes()
            except Exception as error:
                messagebox.showerror("Delete failed", str(error), parent=self)

    def clear_filters(self):
        self.search_entry.delete(0, "end")
        self.category_filter.set("All")
        self.type_filter.set("All")
        self.refresh_notes()


if __name__ == "__main__":
    app = PersonalKnowledgeBase()
    app.mainloop()
