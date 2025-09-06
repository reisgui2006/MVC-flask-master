import os
from flask import Flask
from config import Config
from controllers.user_controller import UserController
from controllers.task_controller import TaskController
from models import db  # CORRETO: importa db do pacote models

app = Flask(__name__, template_folder=os.path.join('view', 'templates'))
app.config.from_object(Config)

# inicializa o banco de dados
db.init_app(app)

# cria tabelas
with app.app_context():
    db.create_all()

# Rotas Usuário
app.add_url_rule('/', view_func=UserController.index, endpoint='index')
app.add_url_rule('/users/new', view_func=UserController.contact, methods=['GET', 'POST'], endpoint='create_user')

# Rotas Tarefas
app.add_url_rule("/tasks", view_func=TaskController.list_tasks, endpoint="list_tasks")
app.add_url_rule("/tasks/new", view_func=TaskController.create_task, methods=["GET", "POST"], endpoint="create_task")
app.add_url_rule("/tasks/update/<int:task_id>", view_func=TaskController.update_task_status, methods=["POST"], endpoint="update_task_status")
app.add_url_rule("/tasks/delete/<int:task_id>", view_func=TaskController.delete_task, methods=["POST"], endpoint="delete_task")

if __name__ == '__main__':
    app.run(debug=True, port=5002)
