import tkinter as tk
from tkinter import messagebox
import random

# Lista de palavras para o jogo
palavras = ["Nala", "Symba", "Mufasa", "Scar", "Timon", "Pumba", "Kiara", "Zazu", "Rafiki", "Sarabi","Kovu", "Taka", "Zira", "Nne", "Tano", "Janja", "Bunga", "Fuli", "Beshte", "Kion", "Rani"]

# Seleciona uma palavra aleatória
palavra_secreta = random.choice(palavras)
palavra_oculta = ["_"] * len(palavra_secreta)
tentativas_restantes = 6
letras_tentadas = set()

def verificar_letra():
    global tentativas_restantes
    letra = entrada_letra.get().lower()
    entrada_letra.delete(0, tk.END)

    if len(letra) != 1 or not letra.isalpha():
        messagebox.showwarning("Aviso", "Digite apenas uma letra!")
        return

    if letra in letras_tentadas:
        messagebox.showinfo("Aviso", "Você já tentou essa letra!")
        return

    letras_tentadas.add(letra)

    if letra in palavra_secreta:
        for i, l in enumerate(palavra_secreta):
            if l == letra:
                palavra_oculta[i] = letra
        atualizar_palavra()
        if "_" not in palavra_oculta:
            messagebox.showinfo("Parabéns!", "Você venceu!")
            reiniciar_jogo()
    else:
        tentativas_restantes -= 1
        atualizar_tentativas()
        if tentativas_restantes == 0:
            messagebox.showerror("Game Over", f"Você perdeu! A palavra era '{palavra_secreta}'.")
            reiniciar_jogo()

def atualizar_palavra():
    lbl_palavra.config(text=" ".join(palavra_oculta))

def atualizar_tentativas():
    lbl_tentativas.config(text=f"Tentativas restantes: {tentativas_restantes}")

def reiniciar_jogo():
    global palavra_secreta, palavra_oculta, tentativas_restantes, letras_tentadas
    palavra_secreta = random.choice(palavras)
    palavra_oculta = ["_"] * len(palavra_secreta)
    tentativas_restantes = 6
    letras_tentadas = set()
    atualizar_palavra()
    atualizar_tentativas()

# Configuração da interface gráfica
janela = tk.Tk()
janela.title("Jogo da Forca")

lbl_titulo = tk.Label(janela, text="Jogo da Forca", font=("Arial", 20))
lbl_titulo.pack(pady=10)

lbl_palavra = tk.Label(janela, text=" ".join(palavra_oculta), font=("Arial", 16))
lbl_palavra.pack(pady=10)

lbl_tentativas = tk.Label(janela, text=f"Tentativas restantes: {tentativas_restantes}", font=("Arial", 14))
lbl_tentativas.pack(pady=10)

entrada_letra = tk.Entry(janela, font=("Arial", 14))
entrada_letra.pack(pady=5)

btn_verificar = tk.Button(janela, text="Verificar", command=verificar_letra, font=("Arial", 14))
btn_verificar.pack(pady=5)

btn_reiniciar = tk.Button(janela, text="Reiniciar Jogo", command=reiniciar_jogo, font=("Arial", 14))
btn_reiniciar.pack(pady=5)

janela.mainloop()