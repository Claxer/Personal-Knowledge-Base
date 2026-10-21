import shutil
from datetime import datetime
from pathlib import Path
from tkinter import filedialog, messagebox
from database import DB_PATH


def create_backup(parent):
    if not DB_PATH.exists():
        messagebox.showinfo("Backup", "There is no database to back up yet.", parent=parent)
        return
    default_name = f"knowledge_base_backup_{datetime.now():%Y%m%d_%H%M%S}.db"
    destination = filedialog.asksaveasfilename(
        parent=parent, title="Save database backup", initialfile=default_name,
        defaultextension=".db", filetypes=[("SQLite database", "*.db"), ("All files", "*.*")]
    )
    if destination:
        try:
            shutil.copy2(DB_PATH, destination)
            messagebox.showinfo("Backup complete", f"Backup saved to:\n{destination}", parent=parent)
        except OSError as error:
            messagebox.showerror("Backup failed", str(error), parent=parent)


def restore_backup(parent):
    source = filedialog.askopenfilename(
        parent=parent, title="Choose a database backup",
        filetypes=[("SQLite database", "*.db"), ("All files", "*.*")]
    )
    if not source:
        return
    confirm = messagebox.askyesno(
        "Restore backup",
        "Restoring replaces the current database file. Close the app and keep a backup first.\n\nContinue?",
        parent=parent
    )
    if not confirm:
        return
    try:
        shutil.copy2(Path(source), DB_PATH)
        messagebox.showinfo(
            "Backup restored",
            "Backup copied successfully. Restart the application to load it.",
            parent=parent
        )
    except OSError as error:
        messagebox.showerror("Restore failed", str(error), parent=parent)
