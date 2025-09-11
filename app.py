import os
from flask import Flask, jsonify, request
from config import Config
from controllers.user_controller import UserController
from controllers.task_controller import TaskController
from models import db  # CORRETO: importa db do pacote models
from flasgger import Swagger
from models.user import User
from models.task import Task

app = Flask(__name__, template_folder=os.path.join('view', 'templates'))
app.config.from_object(Config)
Swagger(app)

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

#Rotas Swagger Usuario
@app.route('/api/users', methods=['POST'])
def api_create_user():
    """
    Cria um novo usuário.
    ---
    tags:
      - Usuários
    description: Cria um novo usuário via JSON
    consumes:
      - application/json
    produces:
      - application/json
    parameters:
      - in: body
        name: user
        description: Objeto JSON com os dados do usuário
        required: true
        schema:
          type: object
          required:
            - nome
            - email
          properties:
            nome:
              type: string
              example: João Silva
            email:
              type: string
              example: joao@email.com
    responses:
      201:
        description: Usuário criado com sucesso
        schema:
          type: object
          properties:
            id:
              type: integer
              example: 1
            nome:
              type: string
              example: João Silva
            email:
              type: string
              example: joao@email.com
      400:
        description: Requisição inválida
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Nome e email são obrigatórios"
    """
    data = request.get_json()
    if not data or 'nome' not in data or 'email' not in data:
        return jsonify({"error": "Nome e email são obrigatórios"}), 400

    new_user = User(name=data['nome'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "nome": new_user.name,
        "email": new_user.email
    }), 201

#Rotas Swagger Tasks
@app.route('/api/tasks', methods=['GET'])
def api_list_task():
    """
    Lista todas as tarefas.
    ---
    tags:
        - Tarefas
    description: Retorna todas as tarefas em JSON
    produces:
        - application/json
    responses:
        200:
            description:
            schema:
                type: array
                items:
                    type: object
                    properties:
                        id:
                            type: integer
                            example: 1
                        title:
                            type: string
                            example: Comprar feijao
                        description:
                            type: string
                            example: 200 gramas
                        status:
                            type: string
                            example: Pendente
                        name:
                            type: string
                            example: Joao Silva
    """

    tasks = Task.query.all()
    tasks_list = [
        {
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "status": t.status,
            "name": t.user.name
        }
        for t in tasks
    ]
    return jsonify(tasks_list), 200

@app.route('/api/tasks', methods=['POST'])
def api_post_task():
    """
    Adicione novas tarefas.
    ---
    tags:
        - Tarefas
    description: Adiciona novas tarefas com titulo, descrição e usuario responsavel
    consumes:
        - application/json
    produces:
        - application/json
    parameters:
        - in: body
          name: task
          description: Objeto JSON com os dados da tarefa
          required: true
          schema:
            type: object
            required:
                - title
                - description
                - user_id
            properties:
                title:
                    type: string
                    example: Comprar o leite
                description:
                    type: string
                    example: Ir ao mercado comprar leite
                status:
                    type: string
                    example: Pendente
                user_id:
                    type: integer
                    example: 1
    responses:
        201:
            description: Tarefa criada com sucesso
            schema:
                type: object
                properties:
                    id:
                        type: integer
                        example: 1
                    title:
                        type: string
                        example: Comprar o leite
                    description:
                        type: string
                        example: Ir ao mercado comprar leite
                    status:
                        type: string
                        example: Pendente
                    user:
                        type: string
                        example: João Silva
        400:
            description: Requisição invalida, faltando algum campo
            schema:
                type: object
                properties:
                    error:
                        type: string
                        example:    "title, description e user_id são obrigatórios"
    """

    data = request.get_json()

    if not data or not all(k in data for k in ("title", "description", "user_id")):
        return jsonify({"error": "title, description e user_id são obrigatórios"}), 400
    
    user = User.query.get(data["user_id"])
    if not user:
        return jsonify({"error": "Usuário não encontrado"}), 400
    
    new_task = Task(
        title=data["title"],
        description=data["description"],
        user_id=data["user_id"]
    )
    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        "id": new_task.id,
        "title": new_task.title,
        "description": new_task.description,
        "status": new_task.status,
        "user": new_task.user.name
    }), 201


if __name__ == '__main__':
    app.run(debug=True, port=5002)