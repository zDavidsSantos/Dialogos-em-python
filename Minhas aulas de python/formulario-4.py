import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox

DB_PATH = "relatorios.db"

def carregar_dados():
    """Carrega os dados do banco de dados."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM relatorios")
        return cursor.fetchall()

def pesquisar_dados(termo):
    """Pesquisa os dados no banco de dados."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = "SELECT * FROM relatorios WHERE cliente LIKE ? OR produto LIKE ?"
        cursor.execute(query, (f"%{termo}%", f"%{termo}%"))
        return cursor.fetchall()

def salvar_dados(id, dados):
    """Salva os dados editados no banco de dados."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        query = """
            UPDATE relatorios
            SET data = ?, tecnico = ?, cliente = ?, produto = ?, serie = ?, estado_produto = ?, 
                itens_produto = ?, defeito_reclamado = ?, defeito_encontrado = ?, itens_trocados = ?
            WHERE id = ?
        """
        cursor.execute(query, (*dados, id))
        conn.commit()

def deletar_dados(id):
    """Deleta um registro do banco de dados."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM relatorios WHERE id = ?", (id,))
        conn.commit()

def atualizar_lista():
    """Atualiza a lista de registros."""
    for item in tree.get_children():
        tree.delete(item)
    for row in carregar_dados():
        tree.insert("", "end", values=row)

def pesquisar():
    """Pesquisa registros e atualiza a lista."""
    termo = entry_pesquisa.get()
    for item in tree.get_children():
        tree.delete(item)
    for row in pesquisar_dados(termo):
        tree.insert("", "end", values=row)

def editar():
    """Carrega os dados selecionados para edição."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Nenhum item selecionado.")
        return
    item = tree.item(selected_item)
    valores = item["values"]
    for i, entry in enumerate(entries):
        entry.delete(0, tk.END)
        entry.insert(0, valores[i + 1])  # Ignora o ID
    global registro_id
    registro_id = valores[0]

def salvar():
    """Salva os dados editados."""
    if registro_id is None:
        messagebox.showerror("Erro", "Nenhum registro para salvar.")
        return
    dados = [entry.get() for entry in entries]
    salvar_dados(registro_id, dados)
    atualizar_lista()
    messagebox.showinfo("Sucesso", "Registro salvo com sucesso.")

def deletar():
    """Deleta o registro selecionado."""
    selected_item = tree.selection()
    if not selected_item:
        messagebox.showerror("Erro", "Nenhum item selecionado.")
        return
    item = tree.item(selected_item)
    registro_id = item["values"][0]
    deletar_dados(registro_id)
    atualizar_lista()
    messagebox.showinfo("Sucesso", "Registro deletado com sucesso.")

# Configuração da interface
root = tk.Tk()
root.title("Gerenciador de Relatórios")

frame_pesquisa = tk.Frame(root)
frame_pesquisa.pack(pady=10)

tk.Label(frame_pesquisa, text="Pesquisar:").pack(side=tk.LEFT, padx=5)
entry_pesquisa = tk.Entry(frame_pesquisa)
entry_pesquisa.pack(side=tk.LEFT, padx=5)
btn_pesquisar = tk.Button(frame_pesquisa, text="Pesquisar", command=pesquisar)
btn_pesquisar.pack(side=tk.LEFT, padx=5)

tree = ttk.Treeview(root, columns=("ID", "Data", "Técnico", "Cliente", "Produto", "Série", "Estado", "Itens", "Defeito Reclamado", "Defeito Encontrado", "Itens Trocados"), show="headings")
tree.pack(pady=10, fill=tk.BOTH, expand=True)

for col in tree["columns"]:
    tree.heading(col, text=col)
    tree.column(col, width=100)

frame_edicao = tk.Frame(root)
frame_edicao.pack(pady=10)

labels = ["Data", "Técnico", "Cliente", "Produto", "Série", "Estado", "Itens", "Defeito Reclamado", "Defeito Encontrado", "Itens Trocados"]
entries = []
for label in labels:
    tk.Label(frame_edicao, text=label).pack()
    entry = tk.Entry(frame_edicao)
    entry.pack()
    entries.append(entry)

frame_botoes = tk.Frame(root)
frame_botoes.pack(pady=10)

btn_editar = tk.Button(frame_botoes, text="Editar", command=editar)
btn_editar.pack(side=tk.LEFT, padx=5)
btn_salvar = tk.Button(frame_botoes, text="Salvar", command=salvar)
btn_salvar.pack(side=tk.LEFT, padx=5)
btn_deletar = tk.Button(frame_botoes, text="Deletar", command=deletar)
btn_deletar.pack(side=tk.LEFT, padx=5)

registro_id = None
atualizar_lista()

root.mainloop()
