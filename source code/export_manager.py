import csv
import json
from tkinter import filedialog, messagebox
from notes_manager import get_notes


def export_notes(parent, file_type="json"):
    notes = get_notes()
    if not notes:
        messagebox.showinfo("Export", "There are no notes to export.", parent=parent)
        return

    extension = ".json" if file_type == "json" else ".csv"
    destination = filedialog.asksaveasfilename(
        parent=parent, title="Export notes", defaultextension=extension,
        filetypes=[("JSON file", "*.json")] if file_type == "json" else [("CSV file", "*.csv")]
    )
    if not destination:
        return

    records = [dict(note) for note in notes]
    try:
        if file_type == "json":
            with open(destination, "w", encoding="utf-8") as file:
                json.dump(records, file, indent=2, ensure_ascii=False)
        else:
            with open(destination, "w", newline="", encoding="utf-8-sig") as file:
                writer = csv.DictWriter(file, fieldnames=records[0].keys())
                writer.writeheader()
                writer.writerows(records)
        messagebox.showinfo("Export complete", f"Exported {len(records)} note(s).", parent=parent)
    except (OSError, TypeError) as error:
        messagebox.showerror("Export failed", str(error), parent=parent)
