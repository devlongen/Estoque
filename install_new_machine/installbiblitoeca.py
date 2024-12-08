import subprocess
import sys

# Lista de pacotes para instalar
packages = [
    'mysql-connector-python',
    'tk',
    'pillow',
    'tkcalendar',
    'customtkinter',
    'babel',
    'packaging',
    'darkdetect'
]

# Função para instalar pacotes
def install_packages():
    for package in packages:
        try:
            print(f'Instalando {package}...')
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f'{package} instalado com sucesso!')
        except subprocess.CalledProcessError as e:
            print(f'Erro ao tentar instalar {package}: {e}')

# Executando a instalação
if __name__ == "__main__":
    install_packages()
