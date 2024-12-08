import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# Função para lançar saída de produto
def connection_database():
    try:
        # Conectar ao MySQL
        conn = mysql.connector.connect(
            host="localhost",
            user="root",      
            password="root",
            database="estoque"
        )
        return conn
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None


def lançar_saida():
    conn = connection_database()
    if not conn:
        return

    cursor = conn.cursor()

    id_produto = entry_id_produto.get()
    nome = entry_nome.get()
    quantidade_saida = entry_quantidade_saida.get()
    valor_saida = entry_valor_saida.get()

    if not id_produto or not nome or not quantidade_saida or not valor_saida:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    valor_entrada = 10.0  # Exemplo de valor de entrada
    lucro = float(valor_saida) - valor_entrada  # Exemplo de lucro
    validade = "2024-12-31"

    query = """
    INSERT INTO saida (id, nome, quantidadeSaida, valorEntrada, valorSaida, lucro, validade)
    VALUES (%s, %s, %s, %s, %s, %s, %s);
    """
    cursor.execute(query, (id_produto, nome, int(quantidade_saida), valor_entrada, float(valor_saida), lucro, validade))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Produto lançado com sucesso!")
    atualizar_tabela()


def editar_saida():
    selected_item = tabela_saida.selection()
    if not selected_item:
        messagebox.showwarning("Aviso", "Selecione um produto para editar.")
        return

    item = tabela_saida.item(selected_item)
    produto = item['values']

    entry_id_produto.delete(0, tk.END)
    entry_id_produto.insert(0, produto[0])

    entry_nome.delete(0, tk.END)
    entry_nome.insert(0, produto[1])

    entry_quantidade_saida.delete(0, tk.END)
    entry_quantidade_saida.insert(0, produto[2])

    entry_valor_saida.delete(0, tk.END)
    entry_valor_saida.insert(0, produto[4])

    # Alterando o texto do botão para "Salvar Alterações"
    btn_lancar_saida.config(text="Salvar Alterações", command=lambda: salvar_alteracoes(selected_item))


def salvar_alteracoes(selected_item):
    conn = connection_database()
    if not conn:
        return

    cursor = conn.cursor()

    id_produto = entry_id_produto.get()
    nome = entry_nome.get()
    quantidade_saida = entry_quantidade_saida.get()
    valor_saida = entry_valor_saida.get()

    if not id_produto or not nome or not quantidade_saida or not valor_saida:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    valor_entrada = 10.0  # Exemplo de valor de entrada
    lucro = float(valor_saida) - valor_entrada  # Exemplo de lucro
    validade = "2024-12-31"

    query = """
    UPDATE saida
    SET nome = %s, quantidadeSaida = %s, valorEntrada = %s, valorSaida = %s, lucro = %s, validade = %s
    WHERE id = %s;
    """
    cursor.execute(query, (nome, int(quantidade_saida), valor_entrada, float(valor_saida), lucro, validade, id_produto))
    conn.commit()
    conn.close()

    messagebox.showinfo("Sucesso", "Produto alterado com sucesso!")
    atualizar_tabela()

    # Resetando o botão para lançar saída novamente
    btn_lancar_saida.config(text="Lançar Saída", command=lançar_saida)


def excluir_saida():
    selected_item = tabela_saida.selection()
    if not selected_item:
        messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
        return

    confirmacao = messagebox.askyesno("Confirmação", "Você tem certeza que deseja excluir este produto?")
    if confirmacao:
        item = tabela_saida.item(selected_item)
        produto = item['values']

        conn = connection_database()
        if not conn:
            return

        cursor = conn.cursor()

        query = """
        DELETE FROM saida WHERE id = %s;
        """
        cursor.execute(query, (produto[0],))
        conn.commit()
        conn.close()

        messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
        atualizar_tabela()


def consultar_saida():
    conn = connection_database()
    if not conn:
        return

    cursor = conn.cursor()

    query = "SELECT * FROM saida"
    cursor.execute(query)
    produtos = cursor.fetchall()
    conn.close()

    for row in tabela_saida.get_children():
        tabela_saida.delete(row)

    for produto in produtos:
        tabela_saida.insert("", "end", values=produto)


def atualizar_tabela():
    conn = connection_database()
    if not conn:
        return

    cursor = conn.cursor()

    query = "SELECT * FROM saida"
    cursor.execute(query)
    produtos = cursor.fetchall()
    conn.close()

    for row in tabela_saida.get_children():
        tabela_saida.delete(row)

    for produto in produtos:
        tabela_saida.insert("", "end", values=produto)


# Configuração da janela principal
root = tk.Tk()
root.title("Sistema de Controle de Estoque")

# Configuração do estilo visual
root.configure(bg="#0f0d25")
root.geometry("700x600")

# Container principal
container = tk.Frame(root, bg="#0f0d25", padx=20, pady=20)
container.pack(expand=True, fill="both", padx=20, pady=20)

# Título
titulo = tk.Label(container, text="Sistema de Controle de Estoque", font=("Arial", 16), bg="#0f0d25", fg="white")
titulo.grid(row=0, column=0, columnspan=2, pady=20)

# Entradas de dados
tk.Label(container, text="Código do produto:", bg="#0f0d25", fg="white").grid(row=1, column=0, pady=5, sticky="w")
entry_id_produto = tk.Entry(container)
entry_id_produto.grid(row=1, column=1, pady=5)

tk.Label(container, text="Nome:", bg="#0f0d25", fg="white").grid(row=2, column=0, pady=5, sticky="w")
entry_nome = tk.Entry(container)
entry_nome.grid(row=2, column=1, pady=5)

tk.Label(container, text="Quantidade Saída:", bg="#0f0d25", fg="white").grid(row=3, column=0, pady=5, sticky="w")
entry_quantidade_saida = tk.Entry(container)
entry_quantidade_saida.grid(row=3, column=1, pady=5)

tk.Label(container, text="Valor Saída:", bg="#0f0d25", fg="white").grid(row=4, column=0, pady=5, sticky="w")
entry_valor_saida = tk.Entry(container)
entry_valor_saida.grid(row=4, column=1, pady=5)

# Botões de ação (ajustando a posição na parte inferior e lado a lado)

btn_lancar_saida = tk.Button(container, text="Criar Saída", bg="#f0ad4e", fg="white", command=lançar_saida, width=15)
btn_lancar_saida.grid(row=5, column=1, pady=10, padx=5, sticky="ew")

btn_consultar_saida = tk.Button(container, text="Consultar Saída", bg="#5cb85c", fg="white", command=consultar_saida, width=15)
btn_consultar_saida.grid(row=5, column=0, pady=10, padx=5, sticky="ew")

btn_editar_saida = tk.Button(container, text="Editar Saída", bg="#f0ad4e", fg="white", command=editar_saida, width=15)
btn_editar_saida.grid(row=5, column=1, pady=10, padx=5, sticky="ew")

btn_excluir_saida = tk.Button(container, text="Excluir Saída", bg="#d9534f", fg="white", command=excluir_saida, width=15)
btn_excluir_saida.grid(row=5, column=2, pady=10, padx=5, sticky="ew")

# Tabela (Treeview) para mostrar a saída de produtos
columns = ("ID", "Nome", "Quantidade Saída", "Valor Entrada", "Valor Saída", "Lucro", "Validade")
tabela_saida = ttk.Treeview(container, columns=columns, show="headings")

# Configuração das colunas
for col in columns:
    tabela_saida.heading(col, text=col)
    tabela_saida.column(col, minwidth=0, width=100)

# Inserção da tabela no layout
tabela_saida.grid(row=6, column=0, columnspan=2, pady=10, sticky="nsew")

# Barra de rolagem para a tabela
scrollbar = ttk.Scrollbar(container, orient="vertical", command=tabela_saida.yview)
tabela_saida.configure(yscrollcommand=scrollbar.set)
scrollbar.grid(row=6, column=2, sticky="ns")

# Configuração da expansão no layout
container.grid_rowconfigure(6, weight=1)
container.grid_columnconfigure(1, weight=1)

# Iniciar a interface
root.mainloop()
