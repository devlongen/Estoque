import mysql.connector

class Database:
    """Classe responsável pela conexão com o banco de dados e criação da tabela."""

    def __init__(self):
        try:
            # Conectar ao MySQL com banco de dados específico
            self.conn = mysql.connector.connect(
                host="localhost",
                user="root",      
                password="root",  
                database="estoque"  # Nome do banco de dados
            )
            self.cursor = self.conn.cursor()
            print("Conectado ao banco de dados 'estoque'.")
        
        except mysql.connector.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            self.conn = None
            self.cursor = None

    def create_table_users(self):
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

    def create_table_saida(self):
        """Cria a tabela 'saida' no banco de dados."""
        try:
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS saida (
                    id VARCHAR(50) PRIMARY KEY,
                    nome VARCHAR(255) NOT NULL,
                    quantidadeSaida INT NOT NULL,
                    valorEntrada FLOAT NOT NULL,
                    valorSaida FLOAT NOT NULL,
                    lucro FLOAT NOT NULL,
                    validade DATE NOT NULL
                )
            """)
            self.conn.commit()
            print("Tabela 'saida' criada ou já existente.")
        except mysql.connector.Error as e:
            print(f"Erro ao criar a tabela 'saida': {e}")

    def add_user(self, nome, username, password):
        """Adiciona um novo usuário à tabela 'users'."""
        try:
            query = "INSERT INTO users (nome, username, password) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (nome, username, password))
            self.conn.commit()
            print(f"Usuário '{username}' adicionado com sucesso.")
        except mysql.connector.Error as e:
            print(f"Erro ao adicionar o usuário: {e}")

    def validate_user(self, username, password):
        """Valida se o usuário e a senha correspondem aos dados no banco de dados."""
        try:
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

    def add_saida(self, id_produto, nome, quantidade_saida, valor_entrada, valor_saida, lucro, validade):
        """Adiciona um novo registro na tabela 'saida'."""
        try:
            query = """
                INSERT INTO saida (id, nome, quantidadeSaida, valorEntrada, valorSaida, lucro, validade)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            self.cursor.execute(query, (id_produto, nome, quantidade_saida, valor_entrada, valor_saida, lucro, validade))
            self.conn.commit()
            print(f"Registro do produto '{id_produto}' adicionado com sucesso na tabela 'saida'.")
        except mysql.connector.Error as e:
            print(f"Erro ao adicionar o registro na tabela 'saida': {e}")

    def close(self):
        """Fecha a conexão com o banco de dados de forma segura."""
        try:
            if self.conn and self.conn.is_connected():
                self.cursor.close()  # Fechando o cursor
                self.conn.close()    # Fechando a conexão
                print("Conexão fechada com sucesso.")
        except mysql.connector.Error as e:
            print(f"Erro ao fechar a conexão com o banco de dados: {e}")
        finally:
            self.cursor = None  # Garantindo que o cursor seja definido como None
            self.conn = None    # Garantindo que a conexão seja definida como None
