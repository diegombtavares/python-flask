SECRET_KEY = 'alura'

SQLALCHEMY_DATABASE_URI = '{SGBD}://{usuario}:{senha}@{servidor}/{database}'.format(
    SGBD = 'mysql+mysqlconnector',
    usuario = 'root',
    senha = 'user',
    servidor = 'localhost',
    database = 'jogoteca'
)