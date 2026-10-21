import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, on_dashboard, on_all_notes, on_favorites, on_new_note,
                 on_backup, on_restore, on_export_json, on_export_csv):
        super().__init__(master, width=215, corner_radius=0, fg_color="#151515")
        self.grid_propagate(False)
        ctk.CTkLabel(self, text="KNOWLEDGE BASE", font=ctk.CTkFont(size=15, weight="bold"),
                     text_color="#f2f2f2").pack(anchor="w", padx=20, pady=(26, 4))
        ctk.CTkLabel(self, text="Your personal developer library", font=ctk.CTkFont(size=11),
                     text_color="#8a8a8a").pack(anchor="w", padx=20, pady=(0, 26))

        self._button("Dashboard", on_dashboard)
        self._button("All notes", on_all_notes)
        self._button("Favorites", on_favorites)
        self._button("+ New note", on_new_note, accent=True)

        ctk.CTkLabel(self, text="DATA TOOLS", font=ctk.CTkFont(size=10, weight="bold"),
                     text_color="#777777").pack(anchor="w", padx=20, pady=(30, 8))
        self._button("Create backup", on_backup)
        self._button("Restore backup", on_restore)
        self._button("Export JSON", on_export_json)
        self._button("Export CSV", on_export_csv)

        ctk.CTkLabel(self, text="V2.0  •  Local storage", font=ctk.CTkFont(size=10),
                     text_color="#777777").pack(side="bottom", anchor="w", padx=20, pady=20)

    def _button(self, text, command, accent=False):
        button = ctk.CTkButton(
            self, text=text, command=command, anchor="w", height=38, corner_radius=8,
            fg_color="#303030" if accent else "transparent",
            hover_color="#292929", text_color="#ffffff"
        )
        button.pack(fill="x", padx=12, pady=3)
