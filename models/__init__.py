from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Importa modelos depois que db está definido
from .user import User
from .task import Task