from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db_utils import get_db_connection, read_tasks, read_completed_tasks

delete = Blueprint("delete", __name__, template_folder="templates")

def restore_completed_task(task_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        # Get completed task details
        cursor.execute("""
            SELECT task_name, description, completion_date, priority 
            FROM completed_tasks WHERE id = ?""", (task_id,))
        task = cursor.fetchone()
        if task:
            # Insert back into tasks
            cursor.execute("""
                INSERT INTO tasks (task, description, due_date, priority)
                VALUES (?, ?, ?, ?)""", task)
            # Remove from completed tasks
            cursor.execute("DELETE FROM completed_tasks WHERE id = ?", (task_id,))
            conn.commit()
    except Exception as e:
        print(f"Error restoring task: {e}")
    finally:
        conn.close()

@delete.route("/delete/", methods=["GET", "POST"])
def delete_task():
    if request.method == "POST":
        task_ids = request.form.getlist("tasks")
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            
            if task_ids:
                # Delete selected tasks
                for task_id in task_ids:
                    cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                flash("Selected tasks deleted successfully!", "delete_msg")
            else:
                # Delete all tasks if no selection
                cursor.execute("DELETE FROM tasks")
                flash("All tasks deleted successfully!", "delete_msg")
            conn.commit()
        except Exception:
            return "Error deleting tasks", 500
        finally:
            conn.close()
        return redirect(url_for("home.index"))
    tasks = read_tasks()
    return render_template("delete.html", title="Delete Task", custom_css="delete.css", tasks=tasks)

@delete.route("/completed/", methods=["GET", "POST"])
def view_completed():
    if request.method == "POST":
        if "restore_tasks" in request.form:
            selected_tasks = request.form.getlist("selected_tasks")
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                if selected_tasks:
                    for task_id in selected_tasks:
                        restore_completed_task(task_id)
                    flash("Selected tasks restored successfully!", "add_msg")
                else:
                    cursor.execute("SELECT id FROM completed_tasks")
                    all_tasks = [row[0] for row in cursor.fetchall()]
                    conn.close()
                    for task_id in all_tasks:
                        restore_completed_task(task_id)
                    flash("All tasks restored successfully!", "add_msg")
            except Exception as e:
                return f"Error restoring tasks: {e}", 500
            return redirect(url_for("delete.view_completed"))
        
        elif "delete_completed" in request.form:
            selected_tasks = request.form.getlist("selected_tasks")
            try:
                conn = get_db_connection()
                cursor = conn.cursor()
                if selected_tasks:
                    for task_id in selected_tasks:
                        cursor.execute("DELETE FROM completed_tasks WHERE id = ?", (task_id,))
                    flash("Selected tasks deleted successfully!", "delete_msg")
                else:
                    cursor.execute("DELETE FROM completed_tasks")
                    flash("All tasks deleted successfully!", "delete_msg")
                conn.commit()
            except Exception as e:
                return f"Error deleting tasks: {e}", 500
            finally:
                conn.close()
            return redirect(url_for("delete.view_completed"))
    
    completed_tasks = read_completed_tasks()
    return render_template("delete.html", 
                         title="Completed Tasks", 
                         custom_css="delete.css", 
                         completed_tasks=completed_tasks)