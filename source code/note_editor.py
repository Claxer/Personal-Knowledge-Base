import tkinter as tk
import customtkinter as ctk

try:
    from pygments import lex
    from pygments.lexers import get_lexer_by_name, TextLexer
    from pygments.token import Token
except ImportError:
    lex = get_lexer_by_name = TextLexer = Token = None


class NoteEditor(ctk.CTkFrame):
    def __init__(self, master, on_save, on_delete, on_new):
        super().__init__(master, fg_color="transparent")
        self.on_save = on_save
        self.on_delete = on_delete
        self.on_new = on_new
        self.note_id = None
        self._build()

    def _build(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(4, weight=1)

        header = ctk.CTkFrame(self, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 12))
        ctk.CTkLabel(header, text="Note editor", font=ctk.CTkFont(size=22, weight="bold")).pack(side="left")
        ctk.CTkButton(header, text="New note", width=90, command=self.on_new).pack(side="right", padx=(8, 0))
        ctk.CTkButton(header, text="Delete", width=80, fg_color="#7f3030", hover_color="#963d3d",
                      command=self._delete).pack(side="right", padx=(8, 0))
        ctk.CTkButton(header, text="Save note", width=95, command=self._save).pack(side="right")

        self.title_entry = ctk.CTkEntry(self, placeholder_text="Note title")
        self.title_entry.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        metadata = ctk.CTkFrame(self, fg_color="transparent")
        metadata.grid(row=2, column=0, sticky="ew", pady=(0, 8))
        for col in range(4):
            metadata.grid_columnconfigure(col, weight=1)

        self.category_entry = ctk.CTkEntry(metadata, placeholder_text="Category (e.g. Python)")
        self.category_entry.grid(row=0, column=0, sticky="ew", padx=(0, 6))
        self.tags_entry = ctk.CTkEntry(metadata, placeholder_text="Tags, separated by commas")
        self.tags_entry.grid(row=0, column=1, sticky="ew", padx=6)
        self.language_menu = ctk.CTkOptionMenu(
            metadata, values=["Text", "Python", "JavaScript", "HTML", "CSS", "Java", "SQL", "Bash", "JSON"],
            command=self._language_changed
        )
        self.language_menu.grid(row=0, column=2, sticky="ew", padx=6)
        self.type_menu = ctk.CTkOptionMenu(metadata, values=["Note", "Tutorial", "Code Snippet"])
        self.type_menu.grid(row=0, column=3, sticky="ew", padx=(6, 0))

        flags = ctk.CTkFrame(self, fg_color="transparent")
        flags.grid(row=3, column=0, sticky="ew", pady=(0, 8))
        self.favorite_var = tk.BooleanVar(value=False)
        self.pinned_var = tk.BooleanVar(value=False)
        ctk.CTkCheckBox(flags, text="Favorite", variable=self.favorite_var).pack(side="left", padx=(0, 18))
        ctk.CTkCheckBox(flags, text="Pin note", variable=self.pinned_var).pack(side="left")

        self.content = ctk.CTkTextbox(
            self, wrap="word", font=ctk.CTkFont(family="Consolas", size=13),
            border_width=1, border_color="#343434"
        )
        self.content.grid(row=4, column=0, sticky="nsew")
        self.content.tag_config("keyword", foreground="#c792ea")
        self.content.tag_config("string", foreground="#c3e88d")
        self.content.tag_config("comment", foreground="#697565")
        self.content.tag_config("number", foreground="#f78c6c")
        self.content.tag_config("function", foreground="#82aaff")

        footer = ctk.CTkFrame(self, fg_color="transparent")
        footer.grid(row=5, column=0, sticky="ew", pady=(7, 0))
        ctk.CTkLabel(footer, text="Tip: Ctrl+S saves your note", text_color="gray").pack(side="left")
        self.content.bind("<KeyRelease>", self._schedule_highlight)
        self.content.bind("<Control-s>", lambda event: (self._save(), "break")[1])
        self._highlight_job = None

    def _schedule_highlight(self, _event=None):
        if self._highlight_job:
            self.after_cancel(self._highlight_job)
        self._highlight_job = self.after(350, self._highlight)

    def _language_changed(self, _value=None):
        self._highlight()

    def _highlight(self):
        self._highlight_job = None
        if not lex or not get_lexer_by_name:
            return
        language = self.language_menu.get().lower()
        aliases = {"text": "text", "javascript": "javascript", "html": "html",
                   "css": "css", "python": "python", "java": "java",
                   "sql": "sql", "bash": "bash", "json": "json"}
        try:
            lexer = get_lexer_by_name(aliases.get(language, "text"))
        except Exception:
            lexer = TextLexer()
        source = self.content.get("1.0", "end-1c")
        for tag in ("keyword", "string", "comment", "number", "function"):
            self.content.tag_remove(tag, "1.0", "end")
        try:
            for token, value in lex(source, lexer):
                tag = None
                if token in Token.Keyword or token in Token.Keyword.Type:
                    tag = "keyword"
                elif token in Token.Literal.String:
                    tag = "string"
                elif token in Token.Comment:
                    tag = "comment"
                elif token in Token.Literal.Number:
                    tag = "number"
                elif token in Token.Name.Function:
                    tag = "function"
                if tag:
                    start = self.content.index("insert")
                    # Rebuild offsets from the current source so tags work across lines.
                    self.content.mark_set("highlight_start", "1.0")
                    self.content.mark_gravity("highlight_start", tk.LEFT)
                    self.content.mark_set("highlight_end", "1.0")
                    self.content.mark_gravity("highlight_end", tk.RIGHT)
                    offset = 0
                    for part_token, part_value in lex(source, lexer):
                        if part_token == token and part_value == value:
                            break
                        offset += len(part_value)
                    start = f"1.0+{offset}c"
                    end = f"1.0+{offset + len(value)}c"
                    self.content.tag_add(tag, start, end)
        except Exception:
            pass

    def load_note(self, note):
        self.note_id = note["id"] if note else None
        for widget in (self.title_entry, self.category_entry, self.tags_entry):
            widget.delete(0, "end")
        self.content.delete("1.0", "end")
        if not note:
            self.language_menu.set("Text")
            self.type_menu.set("Note")
            self.favorite_var.set(False)
            self.pinned_var.set(False)
            return
        self.title_entry.insert(0, note["title"])
        self.category_entry.insert(0, note["category"] or "General")
        self.tags_entry.insert(0, note["tags"] or "")
        self.language_menu.set(note["language"] or "Text")
        self.type_menu.set(note["note_type"] or "Note")
        self.favorite_var.set(bool(note["favorite"]))
        self.pinned_var.set(bool(note["pinned"]))
        self.content.insert("1.0", note["content"] or "")
        self._highlight()

    def _save(self):
        self.on_save({
            "id": self.note_id,
            "title": self.title_entry.get(),
            "content": self.content.get("1.0", "end-1c"),
            "category": self.category_entry.get().strip() or "General",
            "tags": self.tags_entry.get().strip(),
            "language": self.language_menu.get(),
            "note_type": self.type_menu.get(),
            "favorite": self.favorite_var.get(),
            "pinned": self.pinned_var.get()
        })

    def _delete(self):
        if self.note_id is not None:
            self.on_delete(self.note_id)
