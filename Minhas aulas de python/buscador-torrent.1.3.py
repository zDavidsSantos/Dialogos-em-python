import requests
import tkinter as tk
from tkinter import ttk, messagebox

def buscar_torrents(termo):
    url = f"https://apibay.org/q.php?q={termo.replace(' ', '%20')}"
    try:
        resposta = requests.get(url)
        if resposta.status_code == 200:
            torrents = resposta.json()
            if torrents:
                resultados.delete(*resultados.get_children())  # Limpa os resultados anteriores
                for i, torrent in enumerate(torrents[:20], start=1):  # Mostra os 20 primeiros resultados
                    resultados.insert("", "end", values=(
                        torrent['name'], torrent['seeders'], torrent['leechers'], f"magnet:?xt=urn:btih:{torrent['info_hash']}"
                    ))
            else:
                messagebox.showinfo("Informação", "Nenhum resultado encontrado.")
        else:
            messagebox.showerror("Erro", "Erro ao acessar a API.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro: {e}")

def buscar():
    termo = entrada_termo.get()
    if termo.strip():
        buscar_torrents(termo)
    else:
        messagebox.showwarning("Aviso", "Por favor, insira um termo para busca.")

def copiar_link():
    try:
        item_selecionado = resultados.selection()[0]  # Obtém o item selecionado
        valores = resultados.item(item_selecionado, "values")  # Obtém os valores do item
        link_magnet = valores[3]  # O link magnet está na quarta coluna
        janela.clipboard_clear()  # Limpa o clipboard
        janela.clipboard_append(link_magnet)  # Adiciona o link magnet ao clipboard
        janela.update()  # Atualiza o clipboard
        messagebox.showinfo("Informação", "Link magnet copiado para a área de transferência.")
    except IndexError:
        messagebox.showwarning("Aviso", "Nenhum item selecionado.")

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Buscador de Torrents v1.3 David Santos")

frame_busca = tk.Frame(janela)
frame_busca.pack(pady=10)

tk.Label(frame_busca, text="Termo de busca:").pack(side=tk.LEFT, padx=5)
entrada_termo = tk.Entry(frame_busca, width=40)
entrada_termo.pack(side=tk.LEFT, padx=5)
botao_buscar = tk.Button(frame_busca, text="Buscar", command=buscar)
botao_buscar.pack(side=tk.LEFT, padx=5)

frame_resultados = tk.Frame(janela)
frame_resultados.pack(pady=10)

colunas = ("Nome", "Seeds", "Peers", "Magnet Link")
resultados = ttk.Treeview(frame_resultados, columns=colunas, show="headings", height=10)
for coluna in colunas:
    resultados.heading(coluna, text=coluna)
    resultados.column(coluna, width=200 if coluna == "Nome" else 100)

resultados.pack(side=tk.LEFT)

scrollbar = ttk.Scrollbar(frame_resultados, orient="vertical", command=resultados.yview)
resultados.configure(yscroll=scrollbar.set)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

botao_copiar = tk.Button(janela, text="Copiar Link Selecionado", command=copiar_link)
botao_copiar.pack(pady=10)

janela.mainloop()