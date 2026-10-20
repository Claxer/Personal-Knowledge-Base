import customtkinter as ctk


class Sidebar(ctk.CTkFrame):
    def __init__(self, master, on_filter):
        super().__init__(
            master,
            width=220,
            corner_radius=0,
            fg_color="#171717"
        )

        self.on_filter = on_filter
        self.pack_propagate(False)

        ctk.CTkLabel(
            self,
            text="PERSONAL\nKNOWLEDGE BASE",
            font=("Arial", 19, "bold"),
            text_color="#FFFFFF",
            justify="left"
        ).pack(anchor="w", padx=20, pady=(25, 30))

        ctk.CTkLabel(
            self,
            text="LIBRARY",
            font=("Arial", 11, "bold"),
            text_color="#888888"
        ).pack(anchor="w", padx=20, pady=(0, 8))

        self.add_navigation_button("All Notes", "All Notes")
        self.add_navigation_button("Favorites", "Favorites")

        ctk.CTkLabel(
            self,
            text="CATEGORIES",
            font=("Arial", 11, "bold"),
            text_color="#888888"
        ).pack(anchor="w", padx=20, pady=(25, 8))

        self.category_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        self.category_frame.pack(fill="x", padx=10)

        self.category_buttons = {}

        ctk.CTkLabel(
            self,
            text="LOCAL STORAGE  •  SQLITE",
            font=("Arial", 10),
            text_color="#666666"
        ).pack(side="bottom", pady=20)

    def add_navigation_button(self, label, category):
        button = ctk.CTkButton(
            self,
            text=label,
            anchor="w",
            height=36,
            corner_radius=6,
            fg_color="transparent",
            hover_color="#303030",
            text_color="#DDDDDD",
            command=lambda: self.on_filter(category)
        )
        button.pack(fill="x", padx=10, pady=2)

    def update_categories(self, categories):
        for button in self.category_buttons.values():
            button.destroy()

        self.category_buttons.clear()

        for category in categories:
            button = ctk.CTkButton(
                self.category_frame,
                text=category,
                anchor="w",
                height=32,
                corner_radius=6,
                fg_color="transparent",
                hover_color="#303030",
                text_color="#BBBBBB",
                command=lambda value=category: self.on_filter(value)
            )
            button.pack(fill="x", pady=1)
            self.category_buttons[category] = button
