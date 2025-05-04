import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import Calendar
import sqlite3
from datetime import datetime, timedelta


class CalendarioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calendário com Timer e Prioridades")
        self.dias_espera = []
        self._setup_database()
        self._create_widgets()
        self._carregar_dias_salvos()

    # Configuração do banco de dados
    def _setup_database(self):
        with sqlite3.connect("calendario.db") as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS eventos (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    data TEXT NOT NULL,
                    prioridade TEXT NOT NULL
                )
            ''')

    def _salvar_data(self, data, prioridade):
        with sqlite3.connect("calendario.db") as conn:
            conn.execute("INSERT INTO eventos (data, prioridade) VALUES (?, ?)", (data, prioridade))

    def _deletar_data(self, data):
        with sqlite3.connect("calendario.db") as conn:
            conn.execute("DELETE FROM eventos WHERE data = ?", (data,))

    def _carregar_dias(self):
        with sqlite3.connect("calendario.db") as conn:
            return conn.execute("SELECT data, prioridade FROM eventos").fetchall()

    # Funções para manipulação de dias
    def _adicionar_dia_lista_espera(self, data, prioridade):
        if data not in [d['data'] for d in self.dias_espera]:
            self.dias_espera.append({'data': data, 'prioridade': prioridade})
            self.dias_espera.sort(key=lambda d: datetime.strptime(d['data'], "%d/%m/%Y").date())
            self._salvar_data(data, prioridade)
            self._atualizar_lista()
            self._destacar_dias()
            messagebox.showinfo("Dia adicionado", f"O dia {data} foi adicionado com prioridade {prioridade}.")
        else:
            messagebox.showwarning("Dia duplicado", f"O dia {data} já está na lista de espera.")

    def _remover_dia_lista_espera(self):
        selecionado = self.lista_dias.curselection()
        if selecionado:
            indice = selecionado[0]
            dia_removido = self.dias_espera.pop(indice)
            self._deletar_data(dia_removido['data'])
            self._atualizar_lista()
            self._destacar_dias()
            messagebox.showinfo("Dia removido", f"O dia {dia_removido['data']} foi removido.")
        else:
            messagebox.showwarning("Seleção inválida", "Por favor, selecione um dia para remover.")

    def _destacar_dias(self):
        self.cal.calevent_remove("all")  # Remove os eventos anteriores
        for dia in self.dias_espera:
            data = datetime.strptime(dia['data'], "%d/%m/%Y").date()
            prioridade = dia['prioridade']
            tag = prioridade.lower()
            self.cal.calevent_create(data, prioridade, tag)
        self.cal.tag_config("alta", background="red", foreground="white")
        self.cal.tag_config("media", background="yellow", foreground="black")
        self.cal.tag_config("baixa", background="green", foreground="white")

    def _iniciar_timer(self):
        if self.dias_espera:
            data_mais_proxima = min(self.dias_espera, key=lambda d: datetime.strptime(d['data'], "%d/%m/%Y").date())
            data_final = datetime.strptime(data_mais_proxima['data'], "%d/%m/%Y")
            self._atualizar_timer(data_final)
        else:
            self.lbl_timer.config(text="Nenhuma data marcada.")

    def _atualizar_timer(self, data_final):
        agora = datetime.now()
        delta = data_final - agora
        if delta.total_seconds() > 0:
            dias, resto = divmod(delta.total_seconds(), 86400)
            horas, resto = divmod(resto, 3600)
            minutos, segundos = divmod(resto, 60)
            self.lbl_timer.config(text=f"Tempo restante: {int(dias)}d {int(horas)}h {int(minutos)}m {int(segundos)}s")
            self.root.after(1000, self._atualizar_timer, data_final)
        else:
            self.lbl_timer.config(text="O dia chegou!")

    # Atualização da lista de datas marcadas
    def _atualizar_lista(self):
        self.lista_dias.delete(0, tk.END)
        for dia in self.dias_espera:
            self.lista_dias.insert(tk.END, f"{dia['data']} - {dia['prioridade']}")

    # Configuração da interface gráfica
    def _create_widgets(self):
        frame = ttk.Frame(self.root, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        self.cal = Calendar(frame, selectmode="day", date_pattern="dd/MM/yyyy")
        self.cal.grid(row=0, column=0, columnspan=3, pady=10)

        self.prioridade_var = tk.StringVar(value="Média")
        ttk.Label(frame, text="Prioridade:").grid(row=1, column=0, padx=5, pady=5)
        prioridade_menu = ttk.OptionMenu(frame, self.prioridade_var, "Média", "Alta", "Média", "Baixa")
        prioridade_menu.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(frame, text="Adicionar Dia", command=lambda: self._adicionar_dia_lista_espera(self.cal.get_date(), self.prioridade_var.get())).grid(row=1, column=2, padx=5, pady=5)
        ttk.Button(frame, text="Iniciar Timer", command=self._iniciar_timer).grid(row=2, column=0, columnspan=3, pady=10)

        self.lbl_timer = ttk.Label(frame, text="Tempo restante: --")
        self.lbl_timer.grid(row=3, column=0, columnspan=3, pady=10)

        ttk.Label(frame, text="Datas Marcadas:").grid(row=4, column=0, columnspan=3, pady=5)
        self.lista_dias = tk.Listbox(frame, height=10, width=40)
        self.lista_dias.grid(row=5, column=0, columnspan=3, pady=5)

        ttk.Button(frame, text="Remover Dia", command=self._remover_dia_lista_espera).grid(row=6, column=0, columnspan=3, pady=10)
        ttk.Button(frame, text="Sair", command=self.root.destroy).grid(row=7, column=1, pady=10)

    def _carregar_dias_salvos(self):
        for data, prioridade in self._carregar_dias():
            self.dias_espera.append({'data': data, 'prioridade': prioridade})
        self._atualizar_lista()
        self._destacar_dias()


if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarioApp(root)
    root.mainloop()
