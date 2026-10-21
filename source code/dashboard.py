import customtkinter as ctk


class Dashboard(ctk.CTkFrame):
    def __init__(self, master, stats, on_open_notes):
        super().__init__(master, fg_color="transparent")
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        ctk.CTkLabel(self, text="Your knowledge, organized.", font=ctk.CTkFont(size=27, weight="bold")
                     ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(4, 4))
        ctk.CTkLabel(self, text="A home for your programming notes, ideas, and code snippets.",
                     text_color="gray").grid(row=1, column=0, columnspan=4, sticky="w", pady=(0, 22))

        cards = [
            ("Total notes", stats["total"]),
            ("Code snippets", stats["snippets"]),
            ("Favorites", stats["favorites"]),
            ("Categories", stats["categories"])
        ]
        for index, (label, value) in enumerate(cards):
            card = ctk.CTkFrame(self, corner_radius=12, border_width=1, border_color="#303030")
            card.grid(row=2, column=index, sticky="nsew", padx=(0 if index == 0 else 7, 7), pady=(0, 22))
            ctk.CTkLabel(card, text=label, text_color="#a0a0a0").pack(anchor="w", padx=15, pady=(15, 4))
            ctk.CTkLabel(card, text=str(value), font=ctk.CTkFont(size=28, weight="bold")
                         ).pack(anchor="w", padx=15, pady=(0, 15))

        ctk.CTkLabel(self, text="Recently updated", font=ctk.CTkFont(size=18, weight="bold")
                     ).grid(row=3, column=0, columnspan=4, sticky="w", pady=(0, 10))
        if not stats["recent"]:
            ctk.CTkLabel(self, text="No notes yet. Create your first note to start building your library.",
                         text_color="gray").grid(row=4, column=0, columnspan=4, sticky="w", pady=12)
        else:
            for row_index, note in enumerate(stats["recent"], start=4):
                item = ctk.CTkFrame(self, corner_radius=8, border_width=1, border_color="#292929")
                item.grid(row=row_index, column=0, columnspan=4, sticky="ew", pady=4)
                ctk.CTkLabel(item, text=note["title"], font=ctk.CTkFont(size=13, weight="bold")
                             ).pack(side="left", padx=14, pady=12)
                ctk.CTkLabel(item, text=f'{note["category"]}  ·  {note["note_type"]}',
                             text_color="gray").pack(side="right", padx=14)
        ctk.CTkButton(self, text="Browse all notes", width=150, command=on_open_notes
                      ).grid(row=10, column=0, sticky="w", pady=(20, 0))
