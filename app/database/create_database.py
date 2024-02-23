import mysql.connector
from mysql.connector  import errorcode
from flask_bcrypt import generate_password_hash

print('Conectando...')

try:
    conn = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='user'
    )

except mysql.connector.Error as err:
    if err.errno == 1045:  # Código de erro para acesso negado
        print('Erro de autenticação: ', err.msg)
    else:
        print('Erro ao conectar:', err)
else:
    print('Conectado')

cursor = conn.cursor()

cursor.execute("DROP DATABASE IF EXISTS devops_culture;")

cursor.execute("CREATE DATABASE devops_culture;")

cursor.execute("USE devops_culture")

# criando tabelas
TABLES = {}

TABLES['Jogos'] = ('''
    CREATE TABLE `devops_culture`.`jogos` (
      `id` INT NOT NULL AUTO_INCREMENT,
      `nome` VARCHAR(50) NOT NULL,
      `categoria` VARCHAR(40) NOT NULL,
      `console` VARCHAR(20) NOT NULL,
      PRIMARY KEY (`id`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin; ''')

TABLES['Usuarios'] = ('''
    CREATE TABLE `devops_culture`.`usuarios` (   
      `id` INT NOT NULL AUTO_INCREMENT,
      `nome` VARCHAR(50) NOT NULL,
      `nickname` VARCHAR(10) NOT NULL,
      `senha` VARCHAR(100) NOT NULL,
      PRIMARY KEY (`id`))
    ENGINE = InnoDB
    DEFAULT CHARACTER SET = utf8
    COLLATE = utf8_bin;  ''')

for tabela_nome in TABLES:
    tabela_sql = TABLES[tabela_nome]
    try:
        print(f'Criando tabela {tabela_nome}')
        cursor.execute(tabela_sql)
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
            print('Tabela já existe')
        else:
            print(err.msg)
    else:
        print('ok')

# inserindo usuários
usuario_sql = 'INSERT INTO usuarios (nome, nickname, senha) values (%s,%s,%s)'

usuarios = [
    ("Administrator", "adm", generate_password_hash("123").decode('utf-8')),
]

cursor.executemany(usuario_sql,usuarios)

cursor.execute('select * from devops_culture.usuarios')
print('---------------- Usuários ----------------')
for user in cursor.fetchall():
    print(user[0])

# inserindo jogos
jogo_sql = 'INSERT INTO jogos (nome, categoria, console) values (%s,%s,%s)'

jogos = [
    ("Rainbow Six", "FPS", "PC"),
    ("God of War", "Hack and Slash", "PS5"),
    ("Red Dead Redemption II", "Ação", "PC"),
]

cursor.executemany(jogo_sql,jogos)

cursor.execute('select * from devops_culture.jogos')
print('---------------- Jogos ----------------')
for jogo in cursor.fetchall():
    print(jogo[1])

# commitando pra gravar no banco
conn.commit()

cursor.close()
conn.close()