import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
import mysql.connector

# Função para lançar saída de produto

def connection_database():
    try:
            # Conectar ao MySQL sem selecionar um banco de dados
            conn = mysql.connector.connect(
                host="localhost",
                user="root",      
                password="root",
                database="estoque"
            )
            cursor = conn.cursor()
            print("Conectado ao banco de dados 'estoque'.")
        
    except mysql.connector.Error as e:
        print(f"Erro ao conectar ao banco de dados: {e}")


def lançar_saida():
    id_produto = entry_id_produto.get()
    nome = entry_nome.get()
    quantidade_saida = entry_quantidade_saida.get()
    valor_saida = entry_valor_saida.get()

    if not id_produto or not nome or not quantidade_saida or not valor_saida:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    produto = {
        "id": id_produto,
        "nome": nome,
        "quantidadeSaida": int(quantidade_saida),
        "valorEntrada": 10.0,  # Exemplo de valor de entrada
        "valorSaida": float(valor_saida),
        "lucro": float(valor_saida) - 10.0,  # Exemplo de lucro
        "validade": "2024-12-31"
    }

    produtos = get_data_localstorage('saida')
    produtos.append(produto)
    save_data_localstorage('saida', produtos)

    # Atualizando a tabela
    atualizar_tabela()

    messagebox.showinfo("Sucesso", "Produto lançado com sucesso!")

# Função para editar a saída de produto
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

# Função para salvar as alterações após editar
def salvar_alteracoes(selected_item):
    id_produto = entry_id_produto.get()
    nome = entry_nome.get()
    quantidade_saida = entry_quantidade_saida.get()
    valor_saida = entry_valor_saida.get()

    if not id_produto or not nome or not quantidade_saida or not valor_saida:
        messagebox.showwarning("Aviso", "Preencha todos os campos.")
        return

    produtos = get_data_localstorage('saida')
    item = tabela_saida.item(selected_item)
    produto = item['values']

    # Atualizando os dados do produto
    produto_editado = {
        "id": id_produto,
        "nome": nome,
        "quantidadeSaida": int(quantidade_saida),
        "valorEntrada": 10.0,  # Exemplo de valor de entrada
        "valorSaida": float(valor_saida),
        "lucro": float(valor_saida) - 10.0,  # Exemplo de lucro
        "validade": "2024-12-31"
    }

    # Substituindo o produto na lista
    index = produtos.index({
        "id": produto[0],
        "nome": produto[1],
        "quantidadeSaida": produto[2],
        "valorEntrada": produto[3],
        "valorSaida": produto[4],
        "lucro": produto[5],
        "validade": produto[6]
    })

    produtos[index] = produto_editado
    save_data_localstorage('saida', produtos)

    # Atualizando a tabela
    atualizar_tabela()

    # Resetando o botão para lançar saída novamente
    btn_criar_saida.config(text="Lançar Saída", command=lançar_saida)

    messagebox.showinfo("Sucesso", "Produto alterado com sucesso!")

# Função para excluir a saída de produto
def excluir_saida():
    selected_item = tabela_saida.selection()
    if not selected_item:
        messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
        return

    confirmacao = messagebox.askyesno("Confirmação", "Você tem certeza que deseja excluir este produto?")
    if confirmacao:
        item = tabela_saida.item(selected_item)
        produto = item['values']

        produtos = get_data_localstorage('saida')

        # Encontrando o produto na lista e removendo
        produtos = [p for p in produtos if p["id"] != produto[0]]

        save_data_localstorage('saida', produtos)

        # Atualizando a tabela
        atualizar_tabela()

        messagebox.showinfo("Sucesso", "Produto excluído com sucesso!")
    def consultar_saida():
        selected_item = tabela_saida.selection()
        if not selected_item:
            messagebox.showwarning("Aviso", "Selecione um produto para excluir.")
            return

# Função para atualizar a tabela
def atualizar_tabela():
    for row in tabela_saida.get_children():
        tabela_saida.delete(row)

    produtos = get_data_localstorage('saida')
    for produto in produtos:
        tabela_saida.insert("", "end", values=(
            produto["id"],
            produto["nome"],
            produto["quantidadeSaida"],
            produto["valorEntrada"],
            produto["valorSaida"],
            produto["lucro"],
            produto["validade"]
        ))

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

btn_criar_saida = tk.Button(container, text="Criar Saída", bg="#f0ad4e", fg="white", command=lançar_saida, width=15)
btn_criar_saida.grid(row=5, column=1, pady=10, padx=5, sticky="ew")

btn_consultar_saida = tk.Button(container, text="Consultar Saída", bg="#5cb85c", fg="white", command=consultar_saida, width=15)
btn_consultar_saida.grid(row=5, column=0, pady=10, padx=5, sticky="ew")


btn_editar_saida = tk.Button(container, text="Editar Saída", bg="#f0ad4e", fg="white", command=editar_saida, width=15)
btn_editar_saida.grid(row=5, column=1, pady=10, padx=5, sticky="ew")

btn_excluir_saida = tk.Button(container, text="Excluir Saída", bg="#d9534f", fg="white", command=excluir_saida, width=15)
btn_excluir_saida.grid(row=5, column=2, pady=10, padx=5, sticky="ew")



# Tabela (Treeview) para mostrar a saída de produtos
columns = ("ID", "Nome", "Quantidade Saída", "Valor Entrada", "Valor Saída", "Lucro", "Validade")
tabela_saida = ttk.Treeview(container, columns=columns, show='headings', height=10)

# Definindo as colunas da tabela
for col in columns:
    tabela_saida.heading(col, text=col)
    tabela_saida.column(col, width=100)

tabela_saida.grid(row=6, column=0, columnspan=3, pady=10, padx=5)

# Iniciar a interface e atualizar a tabela
atualizar_tabela()

root.mainloop()
