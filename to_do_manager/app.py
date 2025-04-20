from flask import Flask
from modules.home import home
from modules.add import add
from modules.delete import delete
from modules.edit import edit
from modules.setting import setting
from modules.db_utils import init_db, old_init_db

app = Flask(__name__, 
           template_folder='templates',
           static_folder='static')
app.secret_key = 'fj94jfj_(@#f93fjf929fj9f02jf'

app.register_blueprint(home)
app.register_blueprint(add)
app.register_blueprint(delete)
app.register_blueprint(edit)
app.register_blueprint(setting)

# Initialize database
with app.app_context():
    init_db()
    old_init_db()

if __name__ == '__main__':
    app.run(debug=True)