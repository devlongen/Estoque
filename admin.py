import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# Função para conectar ao banco de dados
def connection_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="estoque"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para listar usuários
def listar_usuarios():
    conn = connection_database()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        query = "SELECT id, nome, email, username, flag_admin FROM users"
        cursor.execute(query)
        usuarios = cursor.fetchall()

        # Limpar a tabela antes de listar os usuários
        for row in tree.get_children():
            tree.delete(row)

        # Adicionar usuários à tabela
        for usuario in usuarios:
            tree.insert("", "end", values=usuario)

    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao listar usuários: {e}")
    finally:
        conn.close()

# Função para editar um usuário
def editar_usuario():
    user_id = entry_id.get()
    nome = entry_nome.get()
    email = entry_email.get()
    username = entry_username.get()
    flag_admin = entry_flag_admin.get()

    if not user_id or not nome or not email or not username or not flag_admin:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    try:
        user_id = int(user_id)
        flag_admin = int(flag_admin)
        if flag_admin not in [0, 1]:
            raise ValueError("Flag admin deve ser 0 ou 1.")
    except ValueError:
        messagebox.showwarning("Aviso", "ID e Flag Admin devem ser numéricos e válidos!")
        return

    conn = connection_database()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        query = """
        UPDATE users
        SET nome = %s, email = %s, username = %s, flag_admin = %s
        WHERE id = %s
        """
        cursor.execute(query, (nome, email, username, flag_admin, user_id))
        conn.commit()
        if cursor.rowcount == 0:
            messagebox.showwarning("Aviso", "Nenhum usuário encontrado com este ID.")
        else:
            messagebox.showinfo("Sucesso", f"Usuário '{nome}' editado com sucesso!")
        listar_usuarios()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao editar usuário: {e}")
    finally:
        conn.close()

# Função para excluir um usuário
def excluir_usuario():
    user_id = entry_id.get()

    if not user_id:
        messagebox.showwarning("Aviso", "Preencha o ID do usuário para exclusão!")
        return

    try:
        user_id = int(user_id)
    except ValueError:
        messagebox.showwarning("Aviso", "ID deve ser numérico!")
        return

    conn = connection_database()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        query = "DELETE FROM users WHERE id = %s"
        cursor.execute(query, (user_id,))
        conn.commit()
        if cursor.rowcount == 0:
            messagebox.showwarning("Aviso", "Nenhum usuário encontrado com este ID.")
        else:
            messagebox.showinfo("Sucesso", f"Usuário com ID '{user_id}' excluído com sucesso!")
        listar_usuarios()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao excluir usuário: {e}")
    finally:
        conn.close()

# Interface gráfica
admin_root = tk.Tk()
admin_root.title("Gerenciamento de Usuários - Admin")
admin_root.geometry("800x600")

# Layout
container = tk.Frame(admin_root, padx=20, pady=20)
container.pack(expand=True, fill="both")

# Título
titulo = tk.Label(container, text="Gerenciamento de Usuários", font=("Arial", 16))
titulo.grid(row=0, column=0, columnspan=2, pady=20)

# Entradas de dados
tk.Label(container, text="ID do Usuário:").grid(row=1, column=0, pady=5, sticky="w")
entry_id = tk.Entry(container)
entry_id.grid(row=1, column=1, pady=5)

tk.Label(container, text="Nome:").grid(row=2, column=0, pady=5, sticky="w")
entry_nome = tk.Entry(container)
entry_nome.grid(row=2, column=1, pady=5)

tk.Label(container, text="Email:").grid(row=3, column=0, pady=5, sticky="w")
entry_email = tk.Entry(container)
entry_email.grid(row=3, column=1, pady=5)

tk.Label(container, text="Username:").grid(row=4, column=0, pady=5, sticky="w")
entry_username = tk.Entry(container)
entry_username.grid(row=4, column=1, pady=5)

tk.Label(container, text="Tornar Administrador (0 - Não adm ou 1 - Adm):").grid(row=5, column=0, pady=5, sticky="w")
entry_flag_admin = tk.Entry(container)
entry_flag_admin.grid(row=5, column=1, pady=5)

# Botões
botao_listar = tk.Button(container, text="Listar Usuários", command=listar_usuarios, bg="#2196F3", fg="white")
botao_listar.grid(row=6, column=0, pady=20)

botao_editar = tk.Button(container, text="Editar Usuário", command=editar_usuario, bg="#FFA500", fg="white")
botao_editar.grid(row=6, column=1, pady=20)

botao_excluir = tk.Button(container, text="Excluir Usuário", command=excluir_usuario, bg="#f44336", fg="white")
botao_excluir.grid(row=7, column=0, pady=20)

# Tabela de usuários
tree = ttk.Treeview(container, columns=("ID", "Nome", "Email", "Username", "Ativo Admin"), show="headings")
tree.grid(row=8, column=0, columnspan=2, pady=20)

# Configuração das colunas da tabela
for col in ("ID", "Nome", "Email", "Username", "Ativo Admin"):
    tree.heading(col, text=col)
    tree.column(col, width=150)

# Inicializar a listagem de usuários
listar_usuarios()

# Iniciar a interface
admin_root.mainloop()
