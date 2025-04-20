import sqlite3, os

DB_PATH = os.path.join(os.path.dirname(__file__), "tasks.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def read_tasks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, task, description, due_date, priority 
            FROM tasks 
            ORDER BY 
                CASE priority
                    WHEN 'high' THEN 1
                    WHEN 'medium' THEN 2
                    WHEN 'low' THEN 3
                    ELSE 4
                END
        """)
        tasks = cursor.fetchall()
        conn.close()
        return tasks
    except Exception as e:
        print(f"Error reading tasks: {e}")
        return []

def init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task TEXT NOT NULL,
            description TEXT,
            due_date TEXT,
            priority TEXT CHECK(priority IN ('high', 'medium', 'low')),
            user TEXT
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT
        )
    """)
    
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM settings")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO settings (name) VALUES (?)", ("User",))
    
    conn.commit()
    conn.close()

def old_init_db():
    conn = get_db_connection()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS completed_tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_name TEXT NOT NULL,
            description TEXT,
            completion_date TEXT,
            priority TEXT,
            completed_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

def read_completed_tasks():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, task_name, description, completion_date, priority, completed_date FROM completed_tasks")
        tasks = cursor.fetchall()
        return [{
            "id": task[0],
            "task": task[1],
            "description": task[2],
            "due_date": task[3],
            "priority": task[4],
            "completion_date": task[5]
        } for task in tasks]
    except Exception:
        return []
    finally:
        conn.close()
