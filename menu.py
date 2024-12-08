import tkinter as tk
from tkinter import messagebox
import os
import mysql.connector

class StockControlApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stock Control")
        self.root.geometry("1900x900")
        self.root.configure(bg="#0F0C25")
        
        # Verificar se as imagens existem
        logo_path = "icons/logo.png"
        cadastro_img_path = "icons/cadastro.png"
        quantidade_img_path = "icons/quantidade.png"
        calculadora_img_path = "icons/calculadora.png"
        
        for img_path in [logo_path, cadastro_img_path, quantidade_img_path, calculadora_img_path]:
            if not os.path.exists(img_path):
                messagebox.showerror("Erro", f"Imagem {img_path} não encontrada!")
                self.root.quit()
                return
           
        # Carregar imagens
        self.logo_img = tk.PhotoImage(file=logo_path)
        self.cadastro_img = tk.PhotoImage(file=cadastro_img_path)
        self.quantidade_img = tk.PhotoImage(file=quantidade_img_path)
        self.calculadora_img = tk.PhotoImage(file=calculadora_img_path)

        # Frame principal
        self.frame = tk.Frame(self.root, bg="#0F0C25")
        self.frame.grid(row=0, column=0, sticky="nsew")

        # Barra de navegação
        self.navbar = tk.Frame(self.root, bg="#0F0C25", padx=10, pady=5)
        self.navbar.grid(row=0, column=0, sticky="ew", padx=10, pady=5)

        # Adicionar logo
        self.logo_label = tk.Label(self.navbar, image=self.logo_img, bg="#0F0C25")
        self.logo_label.grid(row=0, column=0, padx=10)

        # Botões de navegação
        navbar_button_bg = "#CADA8D"
        self.home_button = tk.Button(self.navbar, text="Inicio", bg=navbar_button_bg, fg="black", command=self.show_home)
        self.home_button.grid(row=0, column=1, padx=10, pady=5)
        self.output_button = tk.Button(self.navbar, text="Saída", bg=navbar_button_bg, fg="black", command=self.show_output)
        self.output_button.grid(row=0, column=2, padx=10, pady=5)
        self.register_button = tk.Button(self.navbar, text="Cadastro", bg=navbar_button_bg, fg="black", command=self.show_register)
        self.register_button.grid(row=0, column=3, padx=10, pady=5)
        self.logout_button = tk.Button(self.navbar, text="Sair", bg=navbar_button_bg, fg="black", command=self.show_logout)
        self.logout_button.grid(row=0, column=4, padx=10, pady=5)

        # Centralizar botões na barra de navegação
        self.navbar.grid_columnconfigure(0, weight=1)
        self.navbar.grid_columnconfigure(1, weight=1)
        self.navbar.grid_columnconfigure(2, weight=1)
        self.navbar.grid_columnconfigure(3, weight=1)
        self.navbar.grid_columnconfigure(4, weight=1)

        # Conteúdo principal
        self.main_content = tk.Frame(self.root, bg="#0F0C25")
        self.main_content.grid(row=1, column=0, sticky="nsew")

        # Frame dos botões principais
        self.buttons_frame = tk.Frame(self.main_content, bg="#0F0C25")
        self.buttons_frame.grid(row=0, column=0, pady=50, padx=50, sticky="nsew")

        # Variáveis de contagem
        self.prod_count = tk.StringVar(value="0")  # Inicializa como "0"
        self.output_count = tk.StringVar(value="0")
        self.profit_count = tk.StringVar(value="0")

        # Organizar os itens lado a lado
        self.buttons_frame.grid_columnconfigure(0, weight=1)
        self.buttons_frame.grid_columnconfigure(1, weight=2)
        self.buttons_frame.grid_columnconfigure(2, weight=1)
        
        self.buttons_frame.grid_rowconfigure(0, weight=1)

        # Adicionar as labels com valores ao lado
        self.cadastro_label = tk.Label(self.buttons_frame, image=self.cadastro_img, bg="#0F0C25")
        self.cadastro_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.register_prod_label = tk.Label(self.buttons_frame, text="Cadastro de Produtos", bg="#0F0C25", fg="white", width=20)
        self.register_prod_label.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        self.prod_count_label = tk.Label(self.buttons_frame, textvariable=self.prod_count, bg="#0F0C25", fg="white", width=10)
        self.prod_count_label.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

        self.quantidade_label = tk.Label(self.buttons_frame, image=self.quantidade_img, bg="#0F0C25")
        self.quantidade_label.grid(row=0, column=3, padx=10, pady=10, sticky="nsew")

        self.output_prod_label = tk.Label(self.buttons_frame, text="Saída de Produtos", bg="#0F0C25", fg="white", width=20)
        self.output_prod_label.grid(row=0, column=4, padx=10, pady=10, sticky="nsew")

        self.output_count_label = tk.Label(self.buttons_frame, textvariable=self.output_count, bg="#0F0C25", fg="white", width=10)
        self.output_count_label.grid(row=0, column=5, padx=10, pady=10, sticky="nsew")

        self.calculadora_label = tk.Label(self.buttons_frame, image=self.calculadora_img, bg="#0F0C25")
        self.calculadora_label.grid(row=0, column=6, padx=10, pady=10, sticky="nsew")

        self.profit_calc_label = tk.Label(self.buttons_frame, text="Calculadora de Lucro", bg="#0F0C25", fg="white", width=20)
        self.profit_calc_label.grid(row=0, column=7, padx=10, pady=10, sticky="nsew")

        self.profit_count_label = tk.Label(self.buttons_frame, textvariable=self.profit_count, bg="#0F0C25", fg="white", width=10)
        self.profit_count_label.grid(row=0, column=8, padx=10, pady=10, sticky="nsew")

        # Chamar a função de atualização na inicialização
        self.update_counts()

        # Atualizar automaticamente a cada 10 segundos
        self.root.after(10000, self.update_counts_periodically)

    def update_counts(self):
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
            cursor.execute('SELECT COUNT(*) FROM produtos')
            qtd_estoque_var = cursor.fetchone()[0]  # Obtém o valor da contagem
            cursor.execute('SELECT COUNT(*) as Quantidade FROM saida')
            qtd_saida_var = cursor.fetchone()[0]  # Obtém o valor da contagem
            conn.close()  # Fechar a conexão
            self.prod_count.set(qtd_estoque_var)
            self.output_count.set(qtd_saida_var)
            self.profit_count.set(1)  # Aqui você pode calcular o lucro, se necessário
            return qtd_saida_var, qtd_estoque_var
        except mysql.connector.Error as e:
            print(f"Erro ao conectar ao banco de dados: {e}")
            return None  # Retorna None em caso de erro

    def update_counts_periodically(self):
        self.update_counts()
        # Chama a função novamente após 10 segundos
        self.root.after(10000, self.update_counts_periodically)

    def show_home(self):
        messagebox.showinfo("Tela Inicial", "Você está na Tela Inicial!")

    def show_output(self):
        # Mostra a tela de Saída
        messagebox.showinfo("Saída", "Você está na Tela de Saída de Produtos!")

    def show_register(self):
        # Mostra a tela de Cadastro de Produtos
        messagebox.showinfo("Cadastro", "Você está na Tela de Cadastro de Produtos!")

    def show_logout(self):
        messagebox.showinfo("Sair", "Você foi desconectado!")

if __name__ == "__main__":
    root = tk.Tk()
    app = StockControlApp(root)
    root.mainloop()
