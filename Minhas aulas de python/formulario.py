import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class Equipamento:
    def __init__(self, numero_serie, data_entrada, nome_empresa, tipo_produto, marca, modelo, adicionais, defeito_reclamado, defeito_encontrado, andamento_manutencao):
        self.numero_serie = numero_serie
        self.data_entrada = data_entrada
        self.nome_empresa = nome_empresa
        self.tipo_produto = tipo_produto
        self.marca = marca
        self.modelo = modelo
        self.adicionais = adicionais
        self.defeito_reclamado = defeito_reclamado
        self.defeito_encontrado = defeito_encontrado
        self.andamento_manutencao = andamento_manutencao

    def __str__(self):
        return (f"Número de Série: {self.numero_serie}\n"
                f"Data de Entrada: {self.data_entrada}\n"
                f"Nome da Empresa: {self.nome_empresa}\n"
                f"Tipo de Produto: {self.tipo_produto}\n"
                f"Marca: {self.marca}\n"
                f"Modelo: {self.modelo}\n"
                f"Adicionais: {self.adicionais}\n"
                f"Defeito Reclamado: {self.defeito_reclamado}\n"
                f"Defeito Encontrado: {self.defeito_encontrado}\n"
                f"Andamento da Manutenção: {self.andamento_manutencao}\n")

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Cadastro de Equipamentos")
        self.equipamentos = []

        # Labels e Entradas
        self.labels = ["Nome da Empresa", "Tipo de Produto", "Número de Série", "Marca", "Modelo", "Adicionais", "Defeito Reclamado", "Defeito Encontrado", "Andamento da Manutenção"]
        self.entries = {}

        for idx, label in enumerate(self.labels):
            tk.Label(root, text=label).grid(row=idx, column=0, padx=10, pady=5, sticky="w")
            if label == "Tipo de Produto":
                combobox = ttk.Combobox(root, values=["Eletrônico", "Mecânico", "Outro"], state="readonly", width=37)
                combobox.grid(row=idx, column=1, padx=10, pady=5)
                self.entries[label] = combobox
            else:
                entry = tk.Entry(root, width=40)
                entry.grid(row=idx, column=1, padx=10, pady=5)
                self.entries[label] = entry

        # Botões
        tk.Button(root, text="Cadastrar", command=self.cadastrar_equipamento).grid(row=len(self.labels), column=0, padx=10, pady=10)
        tk.Button(root, text="Listar Equipamentos", command=self.listar_equipamentos).grid(row=len(self.labels), column=1, padx=10, pady=10)
        tk.Button(root, text="Salvar em Arquivo", command=self.salvar_em_arquivo).grid(row=len(self.labels) + 1, column=0, padx=10, pady=10)
        tk.Button(root, text="Editar Equipamento", command=self.editar_equipamento).grid(row=len(self.labels) + 1, column=1, padx=10, pady=10)

    def cadastrar_equipamento(self):
        data_entrada = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        valores = {label: entry.get() for label, entry in self.entries.items()}

        if any(not valor for valor in valores.values()):
            messagebox.showwarning("Aviso", "Todos os campos devem ser preenchidos!")
            return

        equipamento = Equipamento(valores["Número de Série"], data_entrada, valores["Nome da Empresa"], valores["Tipo de Produto"], valores["Marca"], valores["Modelo"],
                                  valores["Adicionais"], valores["Defeito Reclamado"], valores["Defeito Encontrado"], valores["Andamento da Manutenção"])
        self.equipamentos.append(equipamento)
        messagebox.showinfo("Sucesso", "Equipamento cadastrado com sucesso!")

        # Limpar campos
        for entry in self.entries.values():
            if isinstance(entry, ttk.Combobox):
                entry.set("")
            else:
                entry.delete(0, tk.END)

    def listar_equipamentos(self):
        if not self.equipamentos:
            messagebox.showinfo("Informação", "Nenhum equipamento cadastrado.")
            return

        lista = "\n\n".join([f"Equipamento {idx + 1}:\n{equipamento}" for idx, equipamento in enumerate(self.equipamentos)])
        janela_listagem = tk.Toplevel(self.root)
        janela_listagem.title("Equipamentos Cadastrados")
        text = tk.Text(janela_listagem, wrap="word", width=80, height=20)
        text.insert("1.0", lista)
        text.config(state="disabled")
        text.pack(padx=10, pady=10)

    def salvar_em_arquivo(self):
        if not self.equipamentos:
            messagebox.showinfo("Informação", "Nenhum equipamento cadastrado para salvar.")
            return

        with open("equipamentos.txt", "w") as file:
            for equipamento in self.equipamentos:
                file.write(str(equipamento) + "\n\n")
        messagebox.showinfo("Sucesso", "Equipamentos salvos em 'equipamentos.txt'.")

    def editar_equipamento(self):
        if not self.equipamentos:
            messagebox.showinfo("Informação", "Nenhum equipamento cadastrado para editar.")
            return

        janela_edicao = tk.Toplevel(self.root)
        janela_edicao.title("Editar Equipamento")
        tk.Label(janela_edicao, text="Número de Série do Equipamento:").grid(row=0, column=0, padx=10, pady=5)
        numero_serie_entry = tk.Entry(janela_edicao, width=40)
        numero_serie_entry.grid(row=0, column=1, padx=10, pady=5)

        def buscar_equipamento():
            numero_serie = numero_serie_entry.get()
            for equipamento in self.equipamentos:
                if equipamento.numero_serie == numero_serie:
                    for idx, label in enumerate(self.labels):
                        if label != "Número de Série":
                            tk.Label(janela_edicao, text=label).grid(row=idx + 1, column=0, padx=10, pady=5, sticky="w")
                            if label == "Tipo de Produto":
                                combobox = ttk.Combobox(janela_edicao, values=["Eletrônico", "Mecânico", "Outro"], state="readonly", width=37)
                                combobox.grid(row=idx + 1, column=1, padx=10, pady=5)
                                combobox.set(getattr(equipamento, label.lower().replace(" ", "_")))
                                self.entries[label] = combobox
                            else:
                                entry = tk.Entry(janela_edicao, width=40)
                                entry.grid(row=idx + 1, column=1, padx=10, pady=5)
                                entry.insert(0, getattr(equipamento, label.lower().replace(" ", "_")))
                                self.entries[label] = entry

                    def salvar_edicao():
                        for label, entry in self.entries.items():
                            if label != "Número de Série":
                                setattr(equipamento, label.lower().replace(" ", "_"), entry.get())
                        messagebox.showinfo("Sucesso", "Equipamento editado com sucesso!")
                        janela_edicao.destroy()

                    tk.Button(janela_edicao, text="Salvar Alterações", command=salvar_edicao).grid(row=len(self.labels) + 1, column=0, columnspan=2, pady=10)
                    return

            messagebox.showwarning("Aviso", "Equipamento não encontrado.")

        tk.Button(janela_edicao, text="Buscar", command=buscar_equipamento).grid(row=1, column=0, columnspan=2, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()