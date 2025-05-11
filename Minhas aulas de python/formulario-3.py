import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import datetime
import sqlite3

# Configuração do banco de dados
DB_PATH = "relatorios.db"

def inicializar_banco():
    """Inicializa o banco de dados."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS relatorios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT,
                tecnico TEXT,
                cliente TEXT,
                produto TEXT,
                serie TEXT,
                estado_produto TEXT,
                itens_produto TEXT,
                defeito_reclamado TEXT,
                defeito_encontrado TEXT,
                itens_trocados TEXT
            )
        """)

def salvar_em_txt(relatorio):
    """Salva o relatório em um arquivo .txt."""
    with open("relatorio.txt", "w") as arquivo:
        arquivo.write(relatorio)
    messagebox.showinfo("Salvo", "Relatório salvo em relatorio.txt")

def salvar_no_banco(dados):
    """Salva o relatório no banco de dados."""
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO relatorios (data, tecnico, cliente, produto, serie, estado_produto, itens_produto, defeito_reclamado, defeito_encontrado, itens_trocados)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, dados)
    messagebox.showinfo("Salvo", "Relatório salvo no banco de dados.")

def editar_relatorio():
    """Permite editar relatórios salvos no banco de dados."""
    def carregar_relatorio():
        id_relatorio = entry_id.get()
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM relatorios WHERE id = ?", (id_relatorio,))
            relatorio = cursor.fetchone()
        if relatorio:
            text_editar.delete("1.0", tk.END)
            text_editar.insert(tk.END, "\n".join(map(str, relatorio[1:])))
        else:
            messagebox.showerror("Erro", "Relatório não encontrado.")

    def salvar_edicao():
        id_relatorio = entry_id.get()
        novo_conteudo = text_editar.get("1.0", tk.END).strip().split("\n")
        if len(novo_conteudo) == 10:
            with sqlite3.connect(DB_PATH) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE relatorios
                    SET data = ?, tecnico = ?, cliente = ?, produto = ?, serie = ?, estado_produto = ?, itens_produto = ?, defeito_reclamado = ?, defeito_encontrado = ?, itens_trocados = ?
                    WHERE id = ?
                """, (*novo_conteudo, id_relatorio))
            messagebox.showinfo("Editado", "Relatório editado com sucesso.")
        else:
            messagebox.showerror("Erro", "Formato inválido para edição.")

    janela_editar = tk.Toplevel(root)
    janela_editar.title("Editar Relatório")
    janela_editar.geometry("400x400")

    ttk.Label(janela_editar, text="ID do Relatório:").pack(pady=5)
    entry_id = ttk.Entry(janela_editar, width=30)
    entry_id.pack(pady=5)

    ttk.Button(janela_editar, text="Carregar", command=carregar_relatorio).pack(pady=5)

    text_editar = tk.Text(janela_editar, width=50, height=15)
    text_editar.pack(pady=10)

    ttk.Button(janela_editar, text="Salvar Edição", command=salvar_edicao).pack(pady=5)

def solicitar_dado(titulo, mensagem):
    """Solicita um dado ao usuário."""
    return tk.simpledialog.askstring(titulo, mensagem)

def gerar_relatorio():
    """Coleta os dados e gera o relatório."""
    data_formatada = datetime.date.today().strftime("%d/%m/%Y")

    campos = [
        ("Técnico Responsável", "Informe o técnico responsável:"),
        ("Nome do Cliente", "Informe o nome do cliente:"),
        ("Nome do Produto", "Informe o nome do produto:"),
        ("Número de Série", "Informe o número de série:"),
        ("Estado do Produto", "Informe o estado do produto:"),
        ("Itens do Produto", "Informe os itens do produto:"),
        ("Defeito Reclamado", "Informe o defeito reclamado:"),
        ("Defeito Encontrado", "Informe o defeito encontrado:"),
        ("Itens Trocados", "Informe os itens trocados:")
    ]

    dados = [solicitar_dado(titulo, mensagem) for titulo, mensagem in campos]
    if None in dados:
        messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
        return

    tecnico, cliente, produto, serie, estado_produto, itens_produto, defeito_reclamado, defeito_encontrado, itens_trocados = dados

    relatorio = (
        f" Cliente: {cliente}   Data: {data_formatada}   Produto: {produto}\n"
        f" Itens do Produto: {itens_produto}\n"
        f" Estado do Produto: {estado_produto}\n"
        f" Defeito Reclamado: {defeito_reclamado}\n"
        f" Defeito Encontrado: {defeito_encontrado}\n"
        f" Relatório de Peças Trocadas: {itens_trocados}\n"
        f" Técnico Responsável: {tecnico}"
    )

    salvar_em_txt(relatorio)
    salvar_no_banco((data_formatada, tecnico, cliente, produto, serie, estado_produto, itens_produto, defeito_reclamado, defeito_encontrado, itens_trocados))

# Inicializa o banco de dados
inicializar_banco()

# Criação da janela principal
root = tk.Tk()
root.title("Formulário de Ficha de Produto e Cliente")
root.geometry("300x200")

# Botão para iniciar o processo de geração do relatório
ttk.Button(root, text="Gerar Relatório", command=gerar_relatorio).pack(expand=True, pady=10)

# Botão para editar relatórios
ttk.Button(root, text="Editar Relatório", command=editar_relatorio).pack(expand=True, pady=10)

# Inicia o loop da interface gráfica
root.mainloop()
