import tkinter as tk
from tkinter import messagebox

# Função para cadastrar um produto
def cadastrar_produto():
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()
    quant_minima = entry_quant_minima.get()
    preco = entry_preco.get()
    validade = entry_validade.get()
    
    # Aqui você pode adicionar a lógica para salvar o produto no banco de dados
    messagebox.showinfo("Sucesso", f"Produto {nome} cadastrado com sucesso!")

# Função para editar um produto
def editar_produto():
    index = entry_index.get()
    nome = entry_nome.get()
    quantidade = entry_quantidade.get()
    quant_minima = entry_quant_minima.get()
    preco = entry_preco.get()
    validade = entry_validade.get()

    # Aqui você pode adicionar a lógica para editar o produto no banco de dados
    messagebox.showinfo("Sucesso", f"Produto {index} editado com sucesso!")

# Função para excluir um produto
def excluir_produto():
    index = entry_index.get()
    
    # Aqui você pode adicionar a lógica para excluir o produto do banco de dados
    messagebox.showinfo("Sucesso", f"Produto {index} excluído com sucesso!")

# Função para listar os produtos
def listar_produtos():
    # Aqui você pode adicionar a lógica para listar os produtos do banco de dados
    messagebox.showinfo("Lista de Produtos", "Produto 1, Produto 2, Produto 3")

# Configuração da janela principal
root = tk.Tk()
root.title("Sistema de Controle de Estoque")

# Configuração do estilo visual
root.configure(bg="#0f0d25")
root.geometry("500x500")

# Container principal
container = tk.Frame(root, bg="#fff", padx=20, pady=20)
container.pack(expand=True, fill="both", padx=20, pady=20)

# Título
titulo = tk.Label(container, text="Sistema de Controle de Estoque", font=("Arial", 16), bg="#fff", fg="#0f0d25")
titulo.grid(row=0, column=0, columnspan=2, pady=20)

# Entradas de dados
tk.Label(container, text="Nome do Produto:", bg="#fff", fg="#0f0d25").grid(row=1, column=0, pady=5, sticky="w")
entry_nome = tk.Entry(container)
entry_nome.grid(row=1, column=1, pady=5)

tk.Label(container, text="Quantidade:", bg="#fff", fg="#0f0d25").grid(row=2, column=0, pady=5, sticky="w")
entry_quantidade = tk.Entry(container)
entry_quantidade.grid(row=2, column=1, pady=5)

tk.Label(container, text="Quantidade Mínima:", bg="#fff", fg="#0f0d25").grid(row=3, column=0, pady=5, sticky="w")
entry_quant_minima = tk.Entry(container)
entry_quant_minima.grid(row=3, column=1, pady=5)

tk.Label(container, text="Preço:", bg="#fff", fg="#0f0d25").grid(row=4, column=0, pady=5, sticky="w")
entry_preco = tk.Entry(container)
entry_preco.grid(row=4, column=1, pady=5)

tk.Label(container, text="Validade (AAAA-MM-DD):", bg="#fff", fg="#0f0d25").grid(row=5, column=0, pady=5, sticky="w")
entry_validade = tk.Entry(container)
entry_validade.grid(row=5, column=1, pady=5)

tk.Label(container, text="Índice do Produto (para edição/exclusão):", bg="#fff", fg="#0f0d25").grid(row=6, column=0, pady=5, sticky="w")
entry_index = tk.Entry(container)
entry_index.grid(row=6, column=1, pady=5)

# Botões de ação
btn_cadastrar = tk.Button(container, text="Cadastrar Produto", bg="#5cb85c", fg="white", command=cadastrar_produto)
btn_cadastrar.grid(row=7, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

btn_editar = tk.Button(container, text="Editar Produto", bg="#f0ad4e", fg="white", command=editar_produto)
btn_editar.grid(row=8, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

btn_excluir = tk.Button(container, text="Excluir Produto", bg="#d9534f", fg="white", command=excluir_produto)
btn_excluir.grid(row=9, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

btn_listar = tk.Button(container, text="Listar Produtos", bg="#0275d8", fg="white", command=listar_produtos)
btn_listar.grid(row=10, column=0, columnspan=2, pady=10, padx=5, sticky="ew")

# Iniciar a interface
root.mainloop()
