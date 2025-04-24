import os
from tkinter import Tk, Label, Entry, Button, filedialog, StringVar, messagebox
from pytube import YouTube

def download_video():
    url = url_var.get()
    folder = folder_var.get()
    if not url or not folder:
        messagebox.showerror("Erro", "Por favor, insira a URL e selecione a pasta de destino.")
        return

    try:
        yt = YouTube(url)
        stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
        if stream:
            stream.download(output_path=folder)
            messagebox.showinfo("Sucesso", f"Vídeo '{yt.title}' baixado com sucesso!")
        else:
            messagebox.showerror("Erro", "Não foi possível encontrar um stream MP4 para este vídeo.")
    except Exception as e:
        messagebox.showerror("Erro", f"Erro ao baixar o vídeo: {e}")

def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        folder_var.set(folder)

# Configuração da interface gráfica
root = Tk()
root.title("Downloader de Vídeos do YouTube")

Label(root, text="URL do Vídeo:").grid(row=0, column=0, padx=10, pady=10)
url_var = StringVar()
Entry(root, textvariable=url_var, width=50).grid(row=0, column=1, padx=10, pady=10)

Label(root, text="Pasta de Destino:").grid(row=1, column=0, padx=10, pady=10)
folder_var = StringVar()
Entry(root, textvariable=folder_var, width=50).grid(row=1, column=1, padx=10, pady=10)
Button(root, text="Selecionar", command=select_folder).grid(row=1, column=2, padx=10, pady=10)

Button(root, text="Baixar Vídeo", command=download_video).grid(row=2, column=1, pady=20)

root.mainloop()