import os

SECRET_KEY = 'devops'

SQLALCHEMY_DATABASE_URI = '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD = 'mysql+mysqlconnector',
    usuario = 'root',
    senha = 'user',
    servidor = 'localhost',
    database = 'devops_culture'
)

UPLOAD_PATH = os.path.dirname(os.path.abspath(__file__)) + '/uploads'