import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import ttk
from tkcalendar import Calendar

# Função para conectar ao banco de dados
def connection_database():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="root",
            database="estoque"
        )
        return conn
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao conectar ao banco de dados: {e}")
        return None

# Função para cadastrar um produto
def cadastrar_produto():
    nome = entry_nome.get()
    quantidadeSaida = entry_quantidade.get()
    valorEntrada = entry_valorEntrada.get()
    valorSaida = entry_valorSaida.get()
    lucro = entry_lucro.get()
    validade = entry_validade.get()

    if not nome or not quantidadeSaida or not valorEntrada or not valorSaida or not lucro or not validade:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    try:
        quantidadeSaida = int(quantidadeSaida)
        valorEntrada = float(valorEntrada)
        valorSaida = float(valorSaida)
        lucro = float(lucro)
    except ValueError:
        messagebox.showwarning("Aviso", "Quantidade, Valor de Entrada, Valor de Saída e Lucro devem ser numéricos!")
        return

    conn = connection_database()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        query = '''
            INSERT INTO saida (nome, quantidadeSaida, valorEntrada, valorSaida, lucro, validade)
            VALUES (%s, %s, %s, %s, %s, %s)
        '''
        cursor.execute(query, (nome, quantidadeSaida, valorEntrada, valorSaida, lucro, validade))
        conn.commit()
        messagebox.showinfo("Sucesso", f"Produto '{nome}' cadastrado com sucesso!")
        limpar_campos()
    except mysql.connector.Error as e:
        messagebox.showerror("Erro", f"Erro ao cadastrar produto: {e}")
    finally:
        conn.close()

# Função para editar um produto
def editar_produto():
    index = entry_oodigo_produto.get()
    nome = entry_nome.get()
    quantidadeSaida = entry_quantidade.get()
    valorEntrada = entry_valorEntrada.get()
    valorSaida = entry_valorSaida.get()
    lucro = entry_lucro.get()
    validade = entry_validade.get()

    if not nome or not quantidadeSaida or not valorEntrada or not valorSaida or not lucro or not validade:
        messagebox.showwarning("Aviso", "Preencha todos os campos!")
        return

    if not index:
        messagebox.showwarning("Aviso", "Preencha o índice do produto para edição!")
        return

    try:
        index = int(index)
        quantidadeSaida = int(quantidadeSaida)
        valorEntrada = float(valorEntrada)
        valorSaida = float(valorSaida)
        lucro = float(lucro)
    except ValueError:
        messagebox.showwarning("Aviso", "Índice, Quantidade, Valor de Entrada, Valor de Saída e Lucro devem ser numéricos!")
        return

    conn = connection_database()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        query = '''
            UPDATE saida
            SET 
                nome = %s, 
                quantidadeSaida = %s, 
                valorEntrada = %s, 
                valorSaida = %s, 
                lucro = %s, 
                validade = %s
            WHERE id = %s
        '''
        cursor.execute(query, (nome, quantidadeSaida, valorEntrada, valorSaida, lucro, validade, index))
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
    index = entry_oodigo_produto.get()

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
        query = "DELETE FROM saida WHERE id = %s"
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
def listar_saida():
    conn = connection_database()
    if not conn:
        return

    try:
        cursor = conn.cursor()
        query = "SELECT * FROM saida"
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

def listar_estoque():
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
    entry_valorEntrada.delete(0, tk.END)
    entry_valorSaida.delete(0, tk.END)
    entry_lucro.delete(0, tk.END)
    entry_validade.delete(0, tk.END)
    entry_oodigo_produto.delete(0, tk.END)

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

titulo = tk.Label(container, text="Saída de estoque", font=("Arial", 16), bg="#0f0d25", fg="white")
titulo.grid(row=0, column=0, columnspan=2, pady=20)

# Entradas de dados
tk.Label(container, text="Código do produto:", bg="#0f0d25", fg="white").grid(row=1, column=0, pady=5, sticky="w")
entry_oodigo_produto = tk.Entry(container)
entry_oodigo_produto.grid(row=1, column=1, pady=5)

tk.Label(container, text="Nome do Produto:", bg="#0f0d25", fg="white").grid(row=2, column=0, pady=5, sticky="w")
entry_nome = tk.Entry(container)
entry_nome.grid(row=2, column=1, pady=5)

tk.Label(container, text="Quantidade:", bg="#0f0d25", fg="white").grid(row=3, column=0, pady=5, sticky="w")
entry_quantidade = tk.Entry(container)
entry_quantidade.grid(row=3, column=1, pady=5)

tk.Label(container, text="Valor de Entrada:", bg="#0f0d25", fg="white").grid(row=4, column=0, pady=5, sticky="w")
entry_valorEntrada = tk.Entry(container)
entry_valorEntrada.grid(row=4, column=1, pady=5)

tk.Label(container, text="Valor de Saída:", bg="#0f0d25", fg="white").grid(row=5, column=0, pady=5, sticky="w")
entry_valorSaida = tk.Entry(container)
entry_valorSaida.grid(row=5, column=1, pady=5)

tk.Label(container, text="Lucro:", bg="#0f0d25", fg="white").grid(row=6, column=0, pady=5, sticky="w")
entry_lucro = tk.Entry(container)
entry_lucro.grid(row=6, column=1, pady=5)

tk.Label(container, text="Validade (AAAA-MM-DD):", bg="#0f0d25", fg="white").grid(row=7, column=0, pady=5, sticky="w")
entry_validade = tk.Entry(container)
entry_validade.grid(row=7, column=1, pady=5)
entry_validade.bind("<FocusIn>", exibir_calendario)
entry_validade.bind("<KeyRelease>", formatar_validade)

# Botões
button_frame = tk.Frame(container, bg="#0f0d25")
button_frame.grid(row=8, column=0, columnspan=2, pady=20)

botao_cadastrar = tk.Button(button_frame, text="Cadastrar", bg="#4CAF50", fg="white", command=cadastrar_produto)
botao_cadastrar.grid(row=0, column=0, padx=10)

botao_editar = tk.Button(button_frame, text="Editar", bg="#008CBA", fg="white", command=editar_produto)
botao_editar.grid(row=0, column=1, padx=10)

botao_excluir = tk.Button(button_frame, text="Excluir", bg="#f44336", fg="white", command=excluir_produto)
botao_excluir.grid(row=0, column=2, padx=10)

botao_listar = tk.Button(button_frame, text="Listar Saida de estoque", bg="#9C27B0", fg="white", command=listar_saida)
botao_listar.grid(row=0, column=3, padx=10)

botao_listar_estoque = tk.Button(button_frame, text="Listar Estoque", bg="#FF5722", fg="white", command=listar_estoque)
botao_listar_estoque.grid(row=0, column=4, padx=10)

# Tabela de produtos
tree = ttk.Treeview(container, columns=("id", "nome", "quantidadeSaida", "valorEntrada", "valorSaida", "lucro", "validade"), show="headings")
tree.grid(row=9, column=0, columnspan=2, pady=10, sticky="nsew")

tree.heading("id", text="ID")
tree.heading("nome", text="Nome")
tree.heading("quantidadeSaida", text="Quantidade")
tree.heading("valorEntrada", text="Valor Entrada")
tree.heading("valorSaida", text="Valor Saída")
tree.heading("lucro", text="Lucro")
tree.heading("validade", text="Validade")

# Calendário
cal = Calendar(root, selectmode='day', date_pattern='y-mm-dd')
cal.bind("<<CalendarSelected>>", lambda e: escolher_data())

root.mainloop()
