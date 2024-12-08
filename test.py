import mysql.connector

try:
            # Conectar ao MySQL com banco de dados específico
    conn = mysql.connector.connect(
        host="localhost",
        user="root",      
        password="root",  
        database="estoque"  # Nome do banco de dados
        )
    cursor = conn.cursor()
    print("Conectado ao banco de dados 'estoque'.")
    cursor.execute(
         '''
    INSERT INTO saida (nome, quantidadeSaida, valorEntrada, valorSaida, lucro, validade)
    VALUES ('Produto X', 10, 50.00, 80.00, 30.00, '2024-12-31 23:59:59')
''')
    conn.commit()
    print("Dados adicionado com sucesso.")
        
except mysql.connector.Error as e:
    print(f"Erro ao conectar ao banco de dados: {e}")
           