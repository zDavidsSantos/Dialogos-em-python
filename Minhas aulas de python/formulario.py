import tkinter as tk
from tkinter import messagebox

class CadastroPecasApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Peças")

        # Labels e Entradas
        tk.Label(root, text="Código da Peça:").grid(row=0, column=0, padx=10, pady=5)
        self.codigo_entry = tk.Entry(root)
        self.codigo_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(root, text="Nome da Peça:").grid(row=1, column=0, padx=10, pady=5)
        self.nome_entry = tk.Entry(root)
        self.nome_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(root, text="Quantidade:").grid(row=2, column=0, padx=10, pady=5)
        self.quantidade_entry = tk.Entry(root)
        self.quantidade_entry.grid(row=2, column=1, padx=10, pady=5)

        # Botões
        tk.Button(root, text="Cadastrar", command=self.cadastrar_peca).grid(row=3, column=0, padx=10, pady=10)
        tk.Button(root, text="Sair", command=root.quit).grid(row=3, column=1, padx=10, pady=10)

        # Lista de Peças
        self.lista_pecas = []
        self.lista_box = tk.Listbox(root, width=50)
        self.lista_box.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def cadastrar_peca(self):
        codigo = self.codigo_entry.get()
        nome = self.nome_entry.get()
        quantidade = self.quantidade_entry.get()

        if not codigo or not nome or not quantidade:
            messagebox.showwarning("Atenção", "Todos os campos devem ser preenchidos!")
            return

        try:
            quantidade = int(quantidade)
        except ValueError:
            messagebox.showerror("Erro", "Quantidade deve ser um número inteiro!")
            return

        peca = f"Código: {codigo}, Nome: {nome}, Quantidade: {quantidade}"
        self.lista_pecas.append(peca)
        self.lista_box.insert(tk.END, peca)

        # Limpar campos
        self.codigo_entry.delete(0, tk.END)
        self.nome_entry.delete(0, tk.END)
        self.quantidade_entry.delete(0, tk.END)

        messagebox.showinfo("Sucesso", "Peça cadastrada com sucesso!")

if __name__ == "__main__":
    root = tk.Tk()
    app = CadastroPecasApp(root)
    root.mainloop()