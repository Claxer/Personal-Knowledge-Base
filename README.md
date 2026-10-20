# Personal Knowledge Base

A beginner-friendly **Personal Knowledge Base** built with Python that helps users organize programming notes, tutorials, and code snippets in one place. The application features a modern dark-themed desktop interface, searchable notes, categories, tags, favorites, and code syntax highlighting.

## Features

- **Note Management** — Create, edit, save, and delete notes.
- **Categories** — Organize notes by topics such as Python, Java, HTML, CSS, and SQL.
- **Tags** — Add comma-separated tags to make notes easier to organize.
- **Search System** — Search through note titles, content, categories, and tags.
- **Favorites** — Mark important notes as favorites for quick access.
- **Code Snippets** — Save programming code and select its programming language.
- **Syntax Highlighting** — Apply syntax colors to code using Pygments.
- **Copy to Clipboard** — Copy note content and code snippets.
- **Note Types** — Organize content as notes, tutorials, or code snippets.
- **Local Database** — Store notes using SQLite so they remain available after closing the application.
- **Dark Theme** — Use a clean, dark-themed desktop interface built with CustomTkinter.

## Technologies Used

- **Python** — Main programming language.
- **CustomTkinter** — Desktop graphical user interface.
- **SQLite** — Local database for storing notes.
- **Pygments** — Syntax highlighting for programming code.
- **Tkinter** — Text editor and clipboard functionality.

## Project Structure

```text
PersonalKnowledgeBase/
│
├── main.py
├── database.py
├── notes_manager.py
├── sidebar.py
├── note_editor.py
├── search_manager.py
├── requirements.txt
└── knowledge_base.db
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR-USERNAME/PersonalKnowledgeBase.git
```

Replace `YOUR-USERNAME` with your GitHub username.

### 2. Open the Project

Open the project folder in PyCharm or Visual Studio Code.

### 3. Install Dependencies

Make sure Python is installed, then run:

```bash
pip install -r requirements.txt
```

### 4. Run the Application

```bash
python main.py
```

The SQLite database file will be created automatically when the application starts.

## How to Use

1. Launch the application.
2. Click **New Note** to create a note.
3. Enter a title, category, tags, and content.
4. Select a note type and programming language when needed.
5. Click **Save Note** to store the note.
6. Use the search bar to find saved notes.
7. Select a category in the sidebar to filter notes.
8. Mark notes as favorites to access important information quickly.
9. Use **Highlight Code** to apply syntax colors to supported programming languages.
10. Use **Copy Content** to copy a note or code snippet to the clipboard.
11. Select a saved note and click **Delete** to remove it.

## Database and Data Storage

The application uses SQLite to store note information, including titles, categories, tags, content, note types, programming languages, favorite status, and creation and update timestamps.

The database is stored locally in `knowledge_base.db`. Keep a backup of this file to preserve your saved notes.

## Current Limitations

- The application stores data locally and does not synchronize notes across devices.
- Syntax highlighting is applied manually using the Highlight Code button.
- The application does not currently support user accounts or cloud storage.
- Notes are stored as text rather than as uploaded files or attachments.

## Future Improvements

- Automatic saving.
- Improved code editor with line numbers.
- Recently edited notes dashboard.
- Markdown preview.
- Import and export notes.
- Note backup and restore.
- Customizable themes.
- Advanced filtering and sorting.
- Cloud synchronization.

## Purpose

This project was created to practice Python programming, GUI development, database management, and modular code organization while building a useful tool for storing and reviewing programming knowledge.

## License

This project is open-source. You may add a license of your choice to define how others can use, modify, and distribute the code.
