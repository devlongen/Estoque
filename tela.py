import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
import re
from menu import StockControlApp  

class LoginCadastro:
    def __init__(self, root):
        self.root = root
        self.root.title("Sl Systems - Painel de Acesso")
        self.root.geometry("400x450")
        self.root.configure(bg="#0F0C25")
        self.root.resizable(True, True)

        # Frame principal
        self.frame = tk.Frame(self.root, bg="#0F0C25", relief="raise", padx=20, pady=20)
        self.frame.place(relx=0.5, rely=0.5, anchor="center")

        # Logo
        try:
            self.logo_img = tk.PhotoImage(file="icons/logo.png")
            tk.Label(self.frame, image=self.logo_img, bg="#0F0C25").grid(row=0, column=0, columnspan=2, pady=10)
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

        # Campo de Nome (para cadastro)
        self.nome_label = tk.Label(self.frame, text="Nome:", font=("Century Gothic", 12), bg="#0F0C25", fg="white")
        self.nome_entry = ttk.Entry(self.frame, width=30)

        # Campo de Usuário
        self.usuario_label = tk.Label(self.frame, text="Usuário:", font=("Century Gothic", 12), bg="#0F0C25", fg="white")
        self.usuario_entry = ttk.Entry(self.frame, width=30)

        # Campo de Senha
        self.senha_label = tk.Label(self.frame, text="Senha:", font=("Century Gothic", 12), bg="#0F0C25", fg="white")
        self.senha_entry = ttk.Entry(self.frame, show="*", width=30)

        # Campo de Email (apenas para cadastro)
        self.email_label = tk.Label(self.frame, text="Email:", font=("Century Gothic", 12), bg="#0F0C25", fg="white")
        self.email_entry = ttk.Entry(self.frame, width=30)

        # Botões de Ação
        self.action_button = tk.Button(self.frame, text="Login", font=("Century Gothic", 12), command=self.login, width=20)
        self.action_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.toggle_button = tk.Button(self.frame, text="Cadastrar", font=("Century Gothic", 12), command=self.toggle_mode, width=20)
        self.toggle_button.grid(row=4, column=0, columnspan=2)

        self.is_login = True  # Estado para alternar entre Login e Cadastro

        # Iniciar no modo de Login
        self.update_ui()

    def login(self):
        """Função de login."""
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()

        if not usuario or not senha:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        # Validação do formato do usuário e senha
        if not self.is_valid_usuario(usuario):
            messagebox.showerror("Erro", "Usuário não pode conter números ou caracteres especiais!")
            return
        if len(senha) < 8:
            messagebox.showerror("Erro", "A senha deve ter no mínimo 8 caracteres!")
            return

        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="", database="estoque")
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (usuario, senha))
            result = cursor.fetchone()

            if result:
                messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
                self.root.destroy()
                menu_root = tk.Tk()
                menu_app = StockControlApp(menu_root)
                menu_root.mainloop()
            else:
                messagebox.showerror("Erro", "Usuário ou senha incorretos.")

        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def toggle_mode(self):
        """Alterna entre os modos de login e cadastro."""
        self.is_login = not self.is_login
        self.update_ui()

    def update_ui(self):
        """Atualiza a interface gráfica conforme o modo selecionado."""
        # Limpa a tela antes de reorganizar
        for widget in self.frame.winfo_children():
            widget.grid_forget()

        # Adiciona logo
        try:
            self.logo_img = tk.PhotoImage(file="icons/logo.png")
            tk.Label(self.frame, image=self.logo_img, bg="#0F0C25").grid(row=0, column=0, columnspan=2, pady=10)
        except Exception as e:
            print(f"Erro ao carregar a imagem: {e}")

        # Ajuste para o modo de login
        if self.is_login:
            self.nome_label.grid_forget()
            self.nome_entry.grid_forget()
            self.email_label.grid_forget()
            self.email_entry.grid_forget()

            self.usuario_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.usuario_entry.grid(row=1, column=1, padx=5, pady=5)

            self.senha_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.senha_entry.grid(row=2, column=1, padx=5, pady=5)

            self.action_button.config(text="Login", command=self.login)
            self.action_button.grid(row=3, column=0, columnspan=2, pady=10)

            self.toggle_button.config(text="Cadastrar", command=self.toggle_mode)
            self.toggle_button.grid(row=4, column=0, columnspan=2)

        else:
            self.nome_label.grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.nome_entry.grid(row=1, column=1, padx=5, pady=5)

            self.usuario_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.usuario_entry.grid(row=2, column=1, padx=5, pady=5)

            self.senha_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")
            self.senha_entry.grid(row=3, column=1, padx=5, pady=5)

            self.email_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")
            self.email_entry.grid(row=4, column=1, padx=5, pady=5)

            self.action_button.config(text="Cadastrar", command=self.register)
            self.action_button.grid(row=5, column=0, columnspan=2, pady=10)

            self.toggle_button.config(text="Já tenho uma conta", command=self.toggle_mode)
            self.toggle_button.grid(row=6, column=0, columnspan=2)

    def register(self):
        """Função de cadastro de novo usuário."""
        nome = self.nome_entry.get()
        usuario = self.usuario_entry.get()
        senha = self.senha_entry.get()
        email = self.email_entry.get()

        if not nome or not usuario or not senha or not email:
            messagebox.showerror("Erro", "Preencha todos os campos!")
            return

        # Validação do formato do nome, usuário e senha
        if not self.is_valid_nome(nome):
            messagebox.showerror("Erro", "Nome não pode conter números ou caracteres especiais!")
            return
        if not self.is_valid_usuario(usuario):
            messagebox.showerror("Erro", "Usuário não pode conter números ou caracteres especiais!")
            return
        if len(senha) < 8:
            messagebox.showerror("Erro", "A senha deve ter no mínimo 8 caracteres!")
            return

        try:
            conn = mysql.connector.connect(host="localhost", user="root", password="root", database="estoque")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (nome, username, password, email) VALUES (%s, %s, %s, %s)", (nome, usuario, senha, email))
            conn.commit()
            messagebox.showinfo("Sucesso", "Usuário cadastrado com sucesso!")

        except mysql.connector.Error as e:
            messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        finally:
            if conn.is_connected():
                cursor.close()
                conn.close()

    def is_valid_nome(self, nome):
        """Verifica se o nome contém apenas letras e espaços."""
        return bool(re.match("^[A-Za-záàãâäéèêíïóôõöúçÇ ]+$", nome))

    def is_valid_usuario(self, usuario):
        """Verifica se o usuário contém apenas letras e números (sem caracteres especiais)."""
        return bool(re.match("^[A-Za-z0-9]+$", usuario))

if __name__ == "__main__":
    root = tk.Tk()
    app = LoginCadastro(root)
    root.mainloop()
