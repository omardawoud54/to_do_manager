from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db_utils import read_tasks, get_db_connection
from datetime import datetime

home = Blueprint("home", __name__)

@home.route("/", methods=["GET", "POST"])
def index():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Get user settings
    cursor.execute("""
        SELECT name, tasks_per_page, sort_by, auto_archive, show_completed 
        FROM settings WHERE id = 1
    """)
    settings = cursor.fetchone()
    username = settings[0] if settings else "User"
    tasks_per_page = settings[1] if settings else 10
    sort_by = settings[2] if settings else "due_date"
    auto_archive = settings[3] if settings else 0
    show_completed = settings[4] if settings else 1

    if request.method == "POST":
        if "done_tasks" in request.form:
            task_ids = request.form.getlist("done_tasks")
            if task_ids:
                try:
                    for task_id in task_ids:
                        cursor.execute("SELECT task, description, due_date, priority FROM tasks WHERE id = ?", (task_id,))
                        task = cursor.fetchone()
                        if task:
                            if auto_archive:
                                cursor.execute("""
                                    INSERT INTO completed_tasks (task_name, description, completion_date, priority)
                                    VALUES (?, ?, ?, ?)""", (task[0], task[1], task[2], task[3]))
                            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                    conn.commit()
                    flash("Selected tasks marked as done!", "add_msg")
                except Exception as e:
                    return f"Error marking tasks as done: {e}", 500
                finally:
                    conn.close()
        return redirect(url_for("home.index"))
    
    # Get tasks with sorting and pagination
    page = request.args.get('page', 1, type=int)
    offset = (page - 1) * tasks_per_page
    
    cursor.execute(f"""
        SELECT * FROM tasks 
        ORDER BY 
            CASE 
                WHEN ? = 'priority' THEN 
                    CASE priority
                        WHEN 'high' THEN 1
                        WHEN 'medium' THEN 2
                        WHEN 'low' THEN 3
                    END
                WHEN ? = 'name' THEN task
                ELSE due_date
            END
        LIMIT ? OFFSET ?
    """, (sort_by, sort_by, tasks_per_page, offset))
    
    tasks = cursor.fetchall()
    
    # Get total tasks count for pagination
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cursor.fetchone()[0]
    total_pages = (total_tasks + tasks_per_page - 1) // tasks_per_page
    
    # Get completed tasks count if enabled
    completed_count = None
    if show_completed:
        cursor.execute("SELECT COUNT(*) FROM completed_tasks")
        completed_count = cursor.fetchone()[0]
    
    conn.close()
    
    return render_template("home.html", 
                         title="Dashboard", 
                         custom_css="home.css", 
                         tasks=tasks,
                         username=username,
                         page=page,
                         total_pages=total_pages,
                         completed_count=completed_count)