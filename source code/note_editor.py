import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
from pygments import lex
from pygments.lexers import get_lexer_by_name
from pygments.token import Token


class NoteEditor(ctk.CTkFrame):
    def __init__(self, master, on_save, on_delete, on_new):
        super().__init__(master, fg_color="#1D1D1D", corner_radius=10)

        self.on_save = on_save
        self.on_delete = on_delete
        self.on_new = on_new
        self.current_note_id = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(6, weight=1)

        self.title_entry = ctk.CTkEntry(
            self,
            placeholder_text="Note title...",
            height=42,
            font=("Arial", 20, "bold"),
            fg_color="#292929",
            border_color="#393939"
        )
        self.title_entry.grid(
            row=0, column=0, sticky="ew",
            padx=20, pady=(20, 12)
        )

        details_frame = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        details_frame.grid(
            row=1, column=0, sticky="ew",
            padx=20, pady=4
        )

        details_frame.grid_columnconfigure((0, 1), weight=1)

        self.category_entry = ctk.CTkEntry(
            details_frame,
            placeholder_text="Category (e.g. Python)",
            height=35
        )
        self.category_entry.grid(
            row=0, column=0, sticky="ew",
            padx=(0, 6)
        )

        self.type_menu = ctk.CTkOptionMenu(
            details_frame,
            values=["Note", "Tutorial", "Code Snippet"],
            height=35,
            fg_color="#343434",
            button_color="#444444"
        )
        self.type_menu.grid(
            row=0, column=1, sticky="ew",
            padx=(6, 0)
        )

        self.tags_entry = ctk.CTkEntry(
            self,
            placeholder_text="Tags separated by commas",
            height=35
        )
        self.tags_entry.grid(
            row=2, column=0, sticky="ew",
            padx=20, pady=6
        )

        toolbar = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        toolbar.grid(
            row=3, column=0, sticky="ew",
            padx=20, pady=6
        )

        self.language_menu = ctk.CTkOptionMenu(
            toolbar,
            values=[
                "python", "javascript", "html",
                "css", "java", "sql", "bash", "text"
            ],
            width=135,
            height=32,
            fg_color="#343434",
            button_color="#444444"
        )
        self.language_menu.pack(side="left", padx=(0, 10))

        self.favorite_var = tk.BooleanVar(value=False)

        self.favorite_check = ctk.CTkCheckBox(
            toolbar,
            text="Favorite",
            variable=self.favorite_var,
            checkbox_width=18,
            checkbox_height=18
        )
        self.favorite_check.pack(side="left", padx=5)

        ctk.CTkButton(
            toolbar,
            text="Highlight Code",
            width=115,
            height=32,
            fg_color="#343434",
            hover_color="#444444",
            command=self.highlight_code
        ).pack(side="right")

        self.content_box = tk.Text(
            self,
            wrap="word",
            undo=True,
            font=("Consolas", 12),
            bg="#151515",
            fg="#E5E5E5",
            insertbackground="white",
            selectbackground="#444444",
            relief="flat",
            padx=14,
            pady=14
        )
        self.content_box.grid(
            row=6, column=0, sticky="nsew",
            padx=20, pady=(8, 12)
        )

        self.configure_highlighting()

        buttons_frame = ctk.CTkFrame(
            self, fg_color="transparent"
        )
        buttons_frame.grid(
            row=7, column=0, sticky="ew",
            padx=20, pady=(0, 20)
        )

        ctk.CTkButton(
            buttons_frame,
            text="New Note",
            width=95,
            fg_color="#343434",
            hover_color="#444444",
            command=self.on_new
        ).pack(side="left", padx=(0, 8))

        ctk.CTkButton(
            buttons_frame,
            text="Copy Content",
            width=110,
            fg_color="#343434",
            hover_color="#444444",
            command=self.copy_content
        ).pack(side="left", padx=4)

        ctk.CTkButton(
            buttons_frame,
            text="Delete",
            width=80,
            fg_color="#713333",
            hover_color="#8A3D3D",
            command=self.on_delete
        ).pack(side="right", padx=(8, 0))

        ctk.CTkButton(
            buttons_frame,
            text="Save Note",
            width=110,
            fg_color="#E5E5E5",
            hover_color="#CCCCCC",
            text_color="#111111",
            command=self.on_save
        ).pack(side="right", padx=4)

    def configure_highlighting(self):
        self.content_box.tag_configure(
            "keyword", foreground="#C792EA"
        )
        self.content_box.tag_configure(
            "string", foreground="#C3E88D"
        )
        self.content_box.tag_configure(
            "comment", foreground="#777777"
        )
        self.content_box.tag_configure(
            "number", foreground="#F78C6C"
        )
        self.content_box.tag_configure(
            "function", foreground="#82AAFF"
        )
        self.content_box.tag_configure(
            "operator", foreground="#89DDFF"
        )

    def highlight_code(self):
        language = self.language_menu.get()

        if language == "text":
            messagebox.showinfo(
                "Code Highlighting",
                "Select a programming language first."
            )
            return

        content = self.content_box.get("1.0", "end-1c")

        try:
            lexer = get_lexer_by_name(language)
            tokens = list(lex(content, lexer))

            self.content_box.tag_remove(
                "keyword", "1.0", "end"
            )
            self.content_box.tag_remove(
                "string", "1.0", "end"
            )
            self.content_box.tag_remove(
                "comment", "1.0", "end"
            )
            self.content_box.tag_remove(
                "number", "1.0", "end"
            )
            self.content_box.tag_remove(
                "function", "1.0", "end"
            )
            self.content_box.tag_remove(
                "operator", "1.0", "end"
            )

            position = "1.0"

            for token_type, value in tokens:
                end_position = (
                    f"{position}+{len(value)}c"
                )

                if token_type in Token.Keyword:
                    tag = "keyword"
                elif token_type in Token.Literal.String:
                    tag = "string"
                elif token_type in Token.Comment:
                    tag = "comment"
                elif token_type in Token.Literal.Number:
                    tag = "number"
                elif token_type in Token.Name.Function:
                    tag = "function"
                elif token_type in Token.Operator:
                    tag = "operator"
                else:
                    tag = None

                if tag:
                    self.content_box.tag_add(
                        tag, position, end_position
                    )

                position = end_position

        except Exception as error:
            messagebox.showerror(
                "Highlighting Error",
                f"Could not highlight this code:\n{error}"
            )

    def copy_content(self):
        content = self.content_box.get("1.0", "end-1c")

        self.clipboard_clear()
        self.clipboard_append(content)
        self.update()

        messagebox.showinfo(
            "Copied",
            "Content copied to clipboard."
        )

    def get_data(self):
        return {
            "id": self.current_note_id,
            "title": self.title_entry.get(),
            "category": self.category_entry.get(),
            "tags": self.tags_entry.get(),
            "content": self.content_box.get("1.0", "end-1c"),
            "note_type": self.type_menu.get(),
            "language": self.language_menu.get(),
            "is_favorite": int(self.favorite_var.get())
        }

    def load_note(self, note):
        self.current_note_id = note["id"]

        self.title_entry.delete(0, "end")
        self.title_entry.insert(0, note["title"])

        self.category_entry.delete(0, "end")
        self.category_entry.insert(0, note["category"])

        self.tags_entry.delete(0, "end")
        self.tags_entry.insert(0, note["tags"])

        self.type_menu.set(note["note_type"])
        self.language_menu.set(note["language"])
        self.favorite_var.set(bool(note["is_favorite"]))

        self.content_box.delete("1.0", "end")
        self.content_box.insert("1.0", note["content"])

        self.highlight_code()

    def clear_editor(self):
        self.current_note_id = None

        self.title_entry.delete(0, "end")
        self.category_entry.delete(0, "end")
        self.tags_entry.delete(0, "end")
        self.content_box.delete("1.0", "end")

        self.type_menu.set("Note")
        self.language_menu.set("python")
        self.favorite_var.set(False)
