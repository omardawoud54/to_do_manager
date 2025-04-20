from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db_utils import get_db_connection

add = Blueprint("add", __name__)

@add.route('/add', methods=['GET', 'POST'])
def add_task():
    # Get default priority first
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT default_priority FROM settings WHERE id = 1")
    default_priority = cursor.fetchone()
    default_priority = default_priority[0] if default_priority else 'medium'
    
    if request.method == 'POST':
        task = request.form.get('task')
        description = request.form.get('description') if request.form.get('description') else "N/A"
        due_date = request.form.get('due_date') if request.form.get('due_date') else "N/A"
        priority = request.form.get('priority', default_priority)
        
        if task:
            try:
                cursor.execute("""
                    INSERT INTO tasks (task, description, due_date, priority) 
                    VALUES (?, ?, ?, ?)""",
                    (task, description, due_date, priority))
                conn.commit()
                flash("Task added successfully!", "add_msg")
            except Exception as e:
                flash(f"Error adding task: {e}", "error_msg")
            finally:
                conn.close()
            return redirect(url_for("home.index"))
    
    return render_template("add.html", 
                         title="Add Task", 
                         custom_css="add.css",
                         default_priority=default_priority)
