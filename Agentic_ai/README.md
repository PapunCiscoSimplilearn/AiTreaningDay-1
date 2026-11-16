# Worklist To-Do App

A single-page Flask app for managing a simple worklist. Each task has a name, priority, category, and due date. Tasks are displayed in due-date order and can be added, edited, or deleted.

Tasks are stored in an in-memory Python list, so they are cleared when the app stops.

## Requirements

- Python 3
- Flask

## Setup

From the project directory, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Install Flask:

```bash
python -m pip install Flask
```

## Run

Start the development server from the project directory:

```bash
python app.py
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000) in your browser. Stop the server with `Ctrl+C`.