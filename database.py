import mysql.connector

class Database:
    """Classe responsável pela conexão com o banco de dados e criação da tabela."""

    def __init__(self):
        try:
            # Conectar ao MySQL sem selecionar um banco de dados
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",      
                password="root"  
            )
            self.cursor = self.conn.cursor()

            # Criar o banco de dados se não existir
            self.cursor.execute("CREATE DATABASE IF NOT EXISTS estoque")
            self.conn.database = "estoque"

            # Criar a tabela se não existir
            self.create_table()
            print("Conectado ao banco de dados 'estoque'.")
        
        except mysql.connector.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.conn = None
            self.cursor = None

    def create_table(self):
        """Cria a tabela 'users' no banco de dados."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id INT AUTO_INCREMENT PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    username VARCHAR(255) NOT NULL UNIQUE,
                    password VARCHAR(255) NOT NULL
                )
            """)
            self.conn.commit()
            print("Tabela 'users' criada ou já existente.")
        except mysql.connector.Error as e:
            print(f"Erro ao criar a tabela 'users': {e}")

    def add_user(self, nome, username, password):
        """Adiciona um novo usuário à tabela 'users'."""
        try:
            # Inserir um novo usuário na tabela
            query = "INSERT INTO users (nome, username, password) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (nome, username, password))
            self.conn.commit()
            print(f"Usuário '{username}' adicionado com sucesso.")
        except mysql.connector.Error as e:
            print(f"Erro ao adicionar o usuário: {e}")

    def validate_user(self, username, password):
        """Valida se o usuário e a senha correspondem aos dados no banco de dados."""
        try:
            # Verificar se o usuário existe e a senha é correta
            query = "SELECT * FROM users WHERE username = %s AND password = %s"
            self.cursor.execute(query, (username, password))
            result = self.cursor.fetchone()

            if result:
                return True  # Usuário encontrado e senha válida
            else:
                return False  # Usuário não encontrado ou senha inválida

        except mysql.connector.Error as e:
            print(f"Erro ao validar o usuário: {e}")
            return False

    def close(self):
        """Fecha a conexão com o banco de dados de forma segura."""
        try:
            # Verifica se a conexão ainda está aberta
            if self.conn and self.conn.is_connected():
                self.cursor.close()  # Fecha o cursor
                self.conn.close()    # Fecha a conexão com o banco de dados
                print("Conexão fechada com sucesso.")
        except mysql.connector.Error as e:
            print(f"Erro ao fechar a conexão com o banco de dados: {e}")
        finally:
            # Garantir que as variáveis de conexão sejam limpas
            self.cursor = None
            self.conn = None
