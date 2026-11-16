"""Flask application for an in-memory, due-date-sorted to-do list."""

from datetime import date

from flask import Flask, redirect, render_template, request, url_for

app = Flask(__name__)

tasks = []
priorities = ("High", "Medium", "Low")
categories = ("Work", "Personal", "Health")


def task_from_form():
    """Build a task dictionary from valid submitted form data.

    Returns:
        dict[str, str] | None: The task data, or None if any field is invalid.
    """
    task_name = request.form.get("task", "").strip()
    priority = request.form.get("priority", "")
    category = request.form.get("category", "")
    due_date = request.form.get("due_date", "")

    try:
        date.fromisoformat(due_date)
    except ValueError:
        return None

    if not task_name or priority not in priorities or category not in categories:
        return None

    return {
        "task": task_name,
        "priority": priority,
        "category": category,
        "due_date": due_date,
    }


@app.get("/")
def index():
    """Render the task list, optionally opening one task for editing.

    Returns:
        Response: The rendered task-list page.
    """
    edit_task_index = request.args.get("edit", type=int)
    if edit_task_index is not None and not 0 <= edit_task_index < len(tasks):
        edit_task_index = None

    # Keep original positions so actions still target the right tasks after sorting.
    sorted_tasks = sorted(enumerate(tasks), key=lambda item: item[1]["due_date"])
    return render_template(
        "index.html",
        sorted_tasks=sorted_tasks,
        edit_task_index=edit_task_index,
        priorities=priorities,
        categories=categories,
    )


@app.post("/tasks")
def add_task():
    """Add a valid task submitted from the task-list form.

    Returns:
        Response: A redirect to the task-list page.
    """
    task = task_from_form()
    if task:
        tasks.append(task)

    return redirect(url_for("index"))


@app.post("/tasks/<int:task_index>/edit")
def edit_task(task_index):
    """Replace a task at its original list position with submitted data.

    Args:
        task_index: The task's index in the in-memory list.

    Returns:
        Response: A redirect to the task-list page.
    """
    task = task_from_form()
    if task and 0 <= task_index < len(tasks):
        tasks[task_index] = task

    return redirect(url_for("index"))


@app.post("/tasks/<int:task_index>/delete")
def delete_task(task_index):
    """Delete the task at the given original list position.

    Args:
        task_index: The task's index in the in-memory list.

    Returns:
        Response: A redirect to the task-list page.
    """
    if 0 <= task_index < len(tasks):
        del tasks[task_index]
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)