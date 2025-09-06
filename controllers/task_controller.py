from flask import render_template, request, redirect, url_for
from models import db
from models.task import Task
from models.user import User

class TaskController:

    @staticmethod
    def list_tasks():
        tasks = Task.query.all()
        # TODO buscar todas as tarefas do banco de dados
        return render_template("tasks.html", tasks=tasks)

    @staticmethod
    def create_task():
        
        if request.method == "POST":
            title = request.form['title']
            description = request.form['description']
            user_id = request.form['user_id']

            new_task = Task(title = title, description = description, user_id = user_id)
            db.session.add(new_task)
            db.session.commit()
            # TODO capturar dados do formulário (title, description, user_id)
            # TODO criar um novo objeto Task com os dados capturados
            # TODO adicionar no db.session e dar commit
            return redirect(url_for("list_tasks"))

        # TODO buscar todos os usuários para exibir no <select> do formulário
        users = User.query.all()
        return render_template("create_task.html", users=users)
    
    @staticmethod
    def update_task_status(task_id):
        task = Task.query.get(task_id)

        if task:
            if task.status == "Pendente":
                task.status = "Concluido"
            else:
                task.status == "Pendente"

            db.session.commit()
        # TODO buscar a tarefa pelo id
        # TODO: se existir, alternar status entre "Pendente" e "Concluído" e dar commit na alteração
        return redirect(url_for("list_tasks"))

    @staticmethod
    def delete_task(task_id):
        task = Task.query.get(task_id)

        if task:
            db.session.delete(task)
            db.session.commit()
        # TODO buscar a tarefa pelo id
        # TODO: se ela existir, remover do db.session e dar commit
    
        return redirect(url_for("list_tasks"))