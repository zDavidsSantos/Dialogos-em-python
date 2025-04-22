import requests
import tkinter as tk
from tkinter import ttk, messagebox


def search_torrents_gui():
    query = search_entry.get()
    category = category_combobox.get()
    if not query:
        messagebox.showwarning("Aviso", "Por favor, insira um termo de busca.")
        return
    
    result_text.delete(1.0, tk.END)
    base_url = "https://apibay.org/q.php"
    params = {"q": query, "cat": category}
    
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        torrents = response.json()
        
        if not torrents:
            result_text.insert(tk.END, "Nenhum resultado encontrado.\n")
            return
        
        for torrent in torrents[:10]:  # Limitar a 10 resultados
            result_text.insert(tk.END, f"Nome: {torrent['name']}\n")
            result_text.insert(tk.END, f"Seeders: {torrent['seeders']}\n")
            result_text.insert(tk.END, f"Leechers: {torrent['leechers']}\n")
            result_text.insert(tk.END, f"Magnet: magnet:?xt=urn:btih:{torrent['info_hash']}\n")
            result_text.insert(tk.END, "-" * 40 + "\n")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar torrents: {e}")

# Criar a interface gráfica
root = tk.Tk()
root.title("Buscador de Torrents")

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="Termo de busca:").grid(row=0, column=0, sticky=tk.W)
search_entry = ttk.Entry(frame, width=40)
search_entry.grid(row=0, column=1, sticky=(tk.W, tk.E))

ttk.Label(frame, text="Categoria:").grid(row=1, column=0, sticky=tk.W)
category_combobox = ttk.Combobox(frame, values=["all", "movies", "games", "music"], state="readonly")
category_combobox.set("all")
category_combobox.grid(row=1, column=1, sticky=(tk.W, tk.E))

search_button = ttk.Button(frame, text="Buscar", command=search_torrents_gui)
search_button.grid(row=2, column=0, columnspan=2, pady=5)

result_text = tk.Text(frame, wrap="word", height=20, width=60)
result_text.grid(row=3, column=0, columnspan=2, pady=5)

root.mainloop()


