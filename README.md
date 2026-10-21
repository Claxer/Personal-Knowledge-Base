# Personal Knowledge Base V2

A beginner-friendly **Personal Knowledge Base** built with Python that helps users organize programming notes, tutorials, and code snippets in one place. The application features a modern dark-themed desktop interface, an interactive dashboard, searchable notes, categories, tags, favorites, pinned notes, syntax highlighting, and local database management.

## Features

- **Note Management** — Create, edit, save, and delete programming notes, tutorials, and code snippets.
- **Dashboard** — View statistics for total notes, code snippets, favorites, and categories, along with recently updated notes.
- **Categories** — Organize notes by topics such as Python, Java, HTML, CSS, and SQL.
- **Tags** — Add comma-separated tags to make notes easier to organize and identify.
- **Advanced Search** — Search note titles, content, categories, tags, and programming languages.
- **Category Filtering** — Filter notes by category using the category selection menu.
- **Note Type Filtering** — Filter content by Note, Tutorial, or Code Snippet.
- **Favorites** — Mark important notes as favorites for quick access.
- **Pinned Notes** — Pin important notes so they appear higher in the note list.
- **Code Snippets** — Save programming code and select its programming language.
- **Syntax Highlighting** — Apply syntax colors to supported programming languages using Pygments.
- **Keyboard Shortcut** — Press `Ctrl + S` while editing to save the current note.
- **Local Database** — Store notes in SQLite so they remain available after closing the application.
- **Database Backup** — Create a separate copy of the database to protect saved notes.
- **Database Restore** — Restore a previously created database backup.
- **JSON Export** — Export saved notes and their metadata to a JSON file.
- **CSV Export** — Export saved notes to a CSV file for viewing in spreadsheet applications.
- **Dark Interface** — Use a clean, modern desktop interface built with CustomTkinter.
- **Modular Architecture** — Separate the application into multiple Python files to make the code easier to understand, maintain, and expand.

## Technologies Used

- **Python** — Main programming language.
- **CustomTkinter** — Modern desktop graphical user interface.
- **SQLite** — Local database for storing and managing notes.
- **Pygments** — Syntax highlighting for programming code.
- **Tkinter** — Text editing, keyboard events, dialogs, and other GUI functionality.
- **JSON** — Structured note data export.
- **CSV** — Spreadsheet-compatible data export.

## Project Structure

```text
PersonalKnowledgeBaseV2/
│
├── main.py
├── database.py
├── notes_manager.py
├── search_manager.py
├── sidebar.py
├── dashboard.py
├── note_editor.py
├── backup_manager.py
├── export_manager.py
├── settings.py
├── requirements.txt
├── README.md
│
├── backups/
│
└── knowledge_base.db
```

The `knowledge_base.db` file is created automatically when the application starts. The `backups/` folder is reserved for database backups if you choose to store them there; backups can also be saved to another location.

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/PersonalKnowledgeBase.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Open the Project

Open the extracted or cloned project folder in PyCharm or Visual Studio Code.

### 3. Install Dependencies

Make sure Python is installed, then run the following command in the project terminal:

```bash
python -m pip install -r requirements.txt
```

This installs CustomTkinter and Pygments.

### 4. Run the Application

```bash
python main.py
```

The application initializes the SQLite database automatically when it starts.

## How to Use

1. Launch the application by running `main.py`.
2. Open the **Dashboard** to view your knowledge base statistics and recently updated notes.
3. Click **All notes** to browse your saved notes.
4. Click **New note** to create a new entry.
5. Enter a title, category, tags, and content.
6. Select a programming language and note type when needed.
7. Mark the note as a favorite or pin it for easier access.
8. Click **Save note** to store your changes.
9. Use the search bar to find notes by title, content, category, tags, or programming language.
10. Use the category and note type menus to filter the note list.
11. Select a saved note to view or edit its content.
12. Press `Ctrl + S` while editing to save your note.
13. Click **Delete** to remove a selected note after confirming the deletion.
14. Open **Favorites** in the sidebar to view your favorite notes.
15. Select **Create backup** to save a copy of the database.
16. Select **Restore backup** to restore a database from a backup file. Restart the application after restoring.
17. Use **Export JSON** or **Export CSV** to export your saved notes.

## Database and Data Storage

The application uses SQLite to store note information, including:

- Note ID and title
- Content
- Category and tags
- Programming language
- Note type
- Favorite and pinned status
- Creation and update timestamps

The database is stored locally in `knowledge_base.db`. The application initializes the database and checks for missing supported columns when it starts, helping older databases remain compatible with the current structure.

**Important:** Back up your database before restoring another database or making major changes. Restoring a backup replaces the current database file. Close the application before restoring, then restart it to load the restored data.

## Current Limitations

- The application stores notes locally and does not synchronize data across devices.
- There are no user accounts, cloud storage, or online collaboration features.
- Notes are primarily text-based; file attachments are not currently supported.
- Syntax highlighting is provided through Pygments and depends on the selected programming language.
- The editor does not currently include a full IDE experience, such as code execution, debugging, or automatic code completion.
- The settings module provides basic settings storage but does not yet include a complete settings interface.
- Export functionality supports JSON and CSV; Markdown export and import are not currently implemented.
- Database restore requires restarting the application to load the restored database.

## Future Improvements

- Automatic saving and unsaved-change protection.
- Line numbers and improved code editing tools.
- Markdown editor and live preview.
- Import notes from JSON, CSV, and Markdown files.
- Related notes and internal links between topics.
- More advanced filtering, sorting, and tag management.
- Customizable themes and editor font sizes.
- Additional keyboard shortcuts.
- Improved dashboard statistics and note activity tracking.
- Search result highlighting.
- Cloud synchronization and cross-device access.
- Optional AI-powered note summaries and programming explanations.

## Purpose

This project was created to practice Python programming, GUI development, database management, search functionality, and modular code organization while building a practical tool for storing and reviewing programming knowledge.

Personal Knowledge Base V2 expands the original application with an improved dashboard, advanced note organization, syntax highlighting, backup and restore tools, and data export functionality.

## License

This project is open-source. You may add a license of your choice to define how others can use, modify, and distribute the code. Consider adding a `LICENSE` file to the repository to specify the terms clearly.
