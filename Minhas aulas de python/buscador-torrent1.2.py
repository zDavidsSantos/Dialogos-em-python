import requests
import tkinter as tk
from tkinter import ttk, messagebox

#

    

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
        
        for torrent in torrents[:20]:  # Limitar a 20 resultados
            result_text.insert(tk.END, f"Nome: {torrent['name']}\n")
            result_text.insert(tk.END, f"Seeders: {torrent['seeders']}\n")
            result_text.insert(tk.END, f"Leechers: {torrent['leechers']}\n")
            result_text.insert(tk.END, f"Magnet: magnet:?xt=urn:btih:{torrent['info_hash']}\n")
            result_text.insert(tk.END, "-" * 40 + "\n")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao buscar torrents: {e}")
#
def create_gui():
    global search_entry, category_combobox, result_text

    root = tk.Tk()
    root.title("Buscador de Torrents v1.2 David Santos")

    # Frame de busca
    search_frame = ttk.Frame(root, padding="10")
    search_frame.grid(row=0, column=0, sticky="ew")

    ttk.Label(search_frame, text="Termo de busca:").grid(row=0, column=0, sticky="w")
    search_entry = ttk.Entry(search_frame, width=40)
    search_entry.grid(row=0, column=1, padx=5)

    ttk.Label(search_frame, text="Categoria:").grid(row=0, column=2, sticky="w")
    category_combobox = ttk.Combobox(search_frame, values=["0", "100", "200", "300", "400", "600"], width=10)
    category_combobox.grid(row=0, column=3, padx=5)
    category_combobox.set("0")  # Categoria padrão

    search_button = ttk.Button(search_frame, text="Buscar", command=search_torrents_gui)
    search_button.grid(row=0, column=4, padx=5)

    # Frame de resultados
    result_frame = ttk.Frame(root, padding="10")
    result_frame.grid(row=1, column=0, sticky="nsew")

    result_text = tk.Text(result_frame, wrap="word", height=20, width=80)
    result_text.grid(row=0, column=0, sticky="nsew")

    scrollbar = ttk.Scrollbar(result_frame, orient="vertical", command=result_text.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    result_text["yscrollcommand"] = scrollbar.set

    # Botão para copiar o magnet link
    def copy_magnet_link():
        try:
            selected_text = result_text.get(tk.SEL_FIRST, tk.SEL_LAST)
            if "magnet:?xt=urn:btih:" in selected_text:
                root.clipboard_clear()
                root.clipboard_append(selected_text.strip())
                root.update()  # Atualiza o clipboard
                messagebox.showinfo("Copiado", "Magnet link copiado para a área de transferência.")
            else:
                messagebox.showwarning("Aviso", "Selecione um magnet link válido.")
        except tk.TclError:
            messagebox.showwarning("Aviso", "Nenhum texto selecionado.")

    copy_button = ttk.Button(result_frame, text="Copiar Magnet Link", command=copy_magnet_link)
    copy_button.grid(row=1, column=0, pady=5, sticky="w")

    root.mainloop()


if __name__ == "__main__":
    create_gui()