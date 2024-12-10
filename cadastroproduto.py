import tkinter as tk
import subprocess
import sys
from tkinter import messagebox
import mysql.connector
from tkinter import ttk
from tkcalendar import Calendar


# Função para redirecionar ao menu
def sair_para_menu():
    root.destroy() # Fecha a janela atual
    subprocess.run(["python", "menu.py"])
    
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

# Função para cadastrar um produto
def cadastrar_produto():
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()
    quant_minima = entry_quant_minima.get()
    preco = entry_preco.get()
    validade = entry_validade.get()

    if not nome or not quantidade or not quant_minima or not preco or not validade:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    try:
        quantidade = int(quantidade)
        quant_minima = int(quant_minima)
        preco = float(preco)
    except ValueError:
        messagebox.showwarning("Aviso", "Quantidade, Quantidade Mínima e Preço devem ser numéricos!")
        return

    conn = connection_database()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        query = """
        INSERT INTO produtos (nome, quantidade, quant_minima, preco, validade)
        VALUES (%s, %s, %s, %s, %s)
        """
        cursor.execute(query, (nome, quantidade, quant_minima, preco, validade))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado com sucesso!")
        limpar_campos()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar produto: {e}")
    finally:
        conn.close()

# Função para editar um produto
def editar_produto():
    index = entry_index.get()
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()
    quant_minima = entry_quant_minima.get()
    preco = entry_preco.get()
    validade = entry_validade.get()

    if not index or not nome or not quantidade or not quant_minima or not preco or not validade:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    try:
        index = int(index)
        quantidade = int(quantidade)
        quant_minima = int(quant_minima)
        preco = float(preco)
    except ValueError:
        messagebox.showwarning("Aviso", "Índice, Quantidade, Quantidade Mínima e Preço devem ser numéricos!")
        return

    conn = connection_database()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        query = """
        UPDATE produtos
        SET nome = %s, quantidade = %s, quant_minima = %s, preco = %s, validade = %s
        WHERE id = %s
        """
        cursor.execute(query, (nome, quantidade, quant_minima, preco, validade, index))
        conn.commit()
        if cursor.rowcount == 0:
            messagebox.showwarning("Aviso", "Nenhum produto encontrado com este índice.")
        else:
            messagebox.showinfo("Sucesso", f"Produto '{nome}' editado com sucesso!")
        limpar_campos()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao editar produto: {e}")
    finally:
        conn.close()

# Função para excluir um produto
def excluir_produto():
    index = entry_index.get()

    if not index:
        messagebox.showwarning("Aviso", "Preencha o índice do produto para exclusão!")
        return

    try:
        index = int(index)
    except ValueError:
        messagebox.showwarning("Aviso", "Índice deve ser numérico!")
        return

    conn = connection_database()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        query = "DELETE FROM produtos WHERE id = %s"
        cursor.execute(query, (index,))
        conn.commit()
        if cursor.rowcount == 0:
            messagebox.showwarning("Aviso", "Nenhum produto encontrado com este índice.")
        else:
            messagebox.showinfo("Sucesso", f"Produto com índice '{index}' excluído com sucesso!")
        limpar_campos()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao excluir produto: {e}")
    finally:
        conn.close()

# Função para listar os produtos
def listar_produtos():
    conn = connection_database()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        query = "SELECT * FROM produtos"
        cursor.execute(query)
        produtos = cursor.fetchall()

        # Limpar a tabela antes de listar os produtos
        for row in tree.get_children():
            tree.delete(row)

        # Adicionar produtos à tabela
        for produto in produtos:
            tree.insert("", "end", values=produto)

    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao listar produtos: {e}")
    finally:
        conn.close()

# Função para limpar os campos de entrada
def limpar_campos():
    entry_nome.delete(0, tk.END)
    entry_quantidade.delete(0, tk.END)
    entry_quant_minima.delete(0, tk.END)
    entry_preco.delete(0, tk.END)
    entry_validade.delete(0, tk.END)
    entry_index.delete(0, tk.END)

# Função para formatar a validade
def formatar_validade(event):
    validade = entry_validade.get()
    validade = "".join(c for c in validade if c.isdigit())  # Remove tudo que não é número
    if len(validade) > 4:
        validade = validade[:4] + "-" + validade[4:]
    if len(validade) > 7:
        validade = validade[:7] + "-" + validade[7:]
    entry_validade.delete(0, tk.END)
    entry_validade.insert(0, validade)

# Função para exibir e inserir a data selecionada do calendário
def escolher_data():
    data = cal.selection_get()
    entry_validade.delete(0, tk.END)
    entry_validade.insert(0, data.strftime("%Y-%m-%d"))
    cal.place_forget()  # Esconde o calendário após escolher a data

# Função para exibir o calendário
def exibir_calendario(event):
    cal.place(x=entry_validade.winfo_x(), y=entry_validade.winfo_y() + 30)  # Exibe o calendário abaixo do campo de validade
    cal.lift()  # Garante que o calendário fique acima dos outros elementos da interface

# Configuração da interface gráfica
root = tk.Tk()
root.title("Sistema de Controle de Estoque")
root.geometry("1900x900")
root.configure(bg="#0f0d25")  # Cor de fundo do root

# Layout
container = tk.Frame(root, bg="#0f0d25", padx=20, pady=20)  # Cor de fundo do container
container.pack(expand=True, fill="both", padx=20, pady=20)

titulo = tk.Label(container, text="Edite o seu produto com nossas funcionalidades!", font=("Arial", 16), bg="#0f0d25", fg="white")
titulo.grid(row=0, column=0, columnspan=2, pady=20)

# Entradas de dados
tk.Label(container, text="Nome do Produto:", bg="#0f0d25", fg="white").grid(row=1, column=0, pady=5, sticky="w")
entry_nome = tk.Entry(container)
entry_nome.grid(row=1, column=1, pady=5)

tk.Label(container, text="Quantidade:", bg="#0f0d25", fg="white").grid(row=2, column=0, pady=5, sticky="w")
entry_quantidade = tk.Entry(container)
entry_quantidade.grid(row=2, column=1, pady=5)

tk.Label(container, text="Quantidade Mínima:", bg="#0f0d25", fg="white").grid(row=3, column=0, pady=5, sticky="w")
entry_quant_minima = tk.Entry(container)
entry_quant_minima.grid(row=3, column=1, pady=5)

tk.Label(container, text="Preço:", bg="#0f0d25", fg="white").grid(row=4, column=0, pady=5, sticky="w")
entry_preco = tk.Entry(container)
entry_preco.grid(row=4, column=1, pady=5)

tk.Label(container, text="Validade (AAAA-MM-DD):", bg="#0f0d25", fg="white").grid(row=5, column=0, pady=5, sticky="w")
entry_validade = tk.Entry(container)
entry_validade.grid(row=5, column=1, pady=5)
entry_validade.bind("<KeyRelease>", formatar_validade)
entry_validade.bind("<FocusIn>", exibir_calendario)

tk.Label(container, text="Código do produto (Alterar/Excluir).", bg="#0f0d25", fg="white").grid(row=6, column=0, pady=5, sticky="w")
entry_index = tk.Entry(container)
entry_index.grid(row=6, column=1, pady=5)

# Botões
botao_cadastrar = tk.Button(container, text="Cadastrar Produto", command=cadastrar_produto, bg="#4CAF50", fg="white")
botao_cadastrar.grid(row=7, column=0, pady=20)

botao_editar = tk.Button(container, text="Editar Produto", command=editar_produto, bg="#FFA500", fg="white")
botao_editar.grid(row=7, column=1, pady=20)

botao_excluir = tk.Button(container, text="Excluir Produto", command=excluir_produto, bg="#f44336", fg="white")
botao_excluir.grid(row=8, column=0, pady=20)

botao_listar = tk.Button(container, text="Listar Produtos", command=listar_produtos, bg="#2196F3", fg="white")
botao_listar.grid(row=8, column=1, pady=20)

botao_sair = tk.Button(container, text="Sair", command=sair_para_menu, bg="red", fg="white", font=("Arial", 12))
botao_sair.grid(row=10, column=0, columnspan=2, pady=20)

# Tabela de produtos
tree = ttk.Treeview(container, columns=("ID", "Nome", "Quantidade", "Quantidade Mínima", "Preço", "Validade"), show="headings")
tree.grid(row=9, column=0, columnspan=2, pady=20)

# Calendário
cal = Calendar(root, selectmode='day', date_pattern='y-mm-dd')
cal.bind("<<CalendarSelected>>", lambda e: escolher_data())

# Iniciar a interface
root.mainloop()
