from flask import Blueprint, render_template, request, redirect, url_for, flash
from .db_utils import read_completed_tasks, get_db_connection

setting = Blueprint("setting", __name__)

@setting.route("/setting", methods=["GET", "POST"])
def setting_page():
    completed_count = len(read_completed_tasks())
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Add new columns one by one to avoid SQLite limitations
    try:
        cursor.execute("ALTER TABLE settings ADD COLUMN default_priority TEXT DEFAULT 'medium'")
    except:
        pass
    
    try:
        cursor.execute("ALTER TABLE settings ADD COLUMN tasks_per_page INTEGER DEFAULT 10")
    except:
        pass
    
    try:
        cursor.execute("ALTER TABLE settings ADD COLUMN sort_by TEXT DEFAULT 'due_date'")
    except:
        pass
    
    try:
        cursor.execute("ALTER TABLE settings ADD COLUMN auto_archive INTEGER DEFAULT 0")
    except:
        pass
    
    try:
        cursor.execute("ALTER TABLE settings ADD COLUMN show_completed INTEGER DEFAULT 1")
    except:
        pass

    conn.commit()

    if request.method == "POST":
        name = request.form.get("name")
        default_priority = request.form.get("default_priority", "medium")
        tasks_per_page = request.form.get("tasks_per_page", 10)
        sort_by = request.form.get("sort_by", "due_date")
        auto_archive = 1 if request.form.get("auto_archive") else 0
        show_completed = 1 if request.form.get("show_completed") else 0

        if name:
            cursor.execute("""
                UPDATE settings 
                SET name = ?, default_priority = ?, tasks_per_page = ?,
                    sort_by = ?, auto_archive = ?, show_completed = ?
                WHERE id = 1""", 
                (name, default_priority, tasks_per_page, sort_by, 
                auto_archive, show_completed))
            conn.commit()
            flash("Settings updated successfully!", "setting_msg")
            return redirect(url_for("home.index"))

    # Get all settings, handle case where columns might not exist yet
    try:
        cursor.execute("""
            SELECT name, default_priority, tasks_per_page, sort_by, 
                   auto_archive, show_completed
            FROM settings WHERE id = 1""")
        settings = cursor.fetchone()
    except:
        settings = None
    
    conn.close()
    
    return render_template("setting.html", 
                         title="Settings", 
                         custom_css="setting.css",
                         completed_count=completed_count,
                         settings=settings)