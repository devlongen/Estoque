import subprocess
import os

def run_sql_script():
    try:
        # Definindo a senha via variável de ambiente
        os.environ['MYSQL_PWD'] = 'root'    
        # Comando com redirecionamento de entrada (<)
        result = subprocess.run(
            'mysql -u root < estoque.sql',  # Comando no formato de shell
            shell=True,  # Usando o shell para interpretar o < 
            check=True,
            text=True,
            capture_output=True
        )
        print("Comandos SQL executados com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o script SQL: {e}")
        print(f"Saída do erro: {e.stderr}")

if __name__ == "__main__":
    run_sql_script()
