from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db_utils import get_db_connection, read_tasks

edit = Blueprint("edit", __name__)

@edit.route("/edit/", methods=["GET", "POST"])
def edit_tasks():
    if request.method == "POST":
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            # Get all task IDs from the form
            task_ids = request.form.getlist("task_id")
            
            for task_id in task_ids:
                task_name = request.form.get(f"task_{task_id}")
                description = request.form.get(f"description_{task_id}")
                due_date = request.form.get(f"due_date_{task_id}")
                priority = request.form.get(f"priority_{task_id}")
                
                if task_name:  # Only update if task name exists
                    cursor.execute("""
                        UPDATE tasks 
                        SET task = ?, description = ?, due_date = ?, priority = ?
                        WHERE id = ?""", 
                        (task_name, description, due_date, priority, task_id))
            
            conn.commit()
            flash("Tasks updated successfully!", "edit_msg")
            return redirect(url_for("home.index"))
            
        except Exception as e:
            print(f"Error updating tasks: {e}")
            flash("Error updating tasks!", "edit_msg")
            return redirect(url_for("edit.edit_tasks"))
        finally:
            conn.close()
    
    tasks = read_tasks()
    return render_template("edit.html", title="Edit Tasks", custom_css="edit.css", tasks=tasks)