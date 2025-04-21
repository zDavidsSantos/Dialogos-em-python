import tkinter as tk
from tkinter import messagebox

class JogoDaForca:
    def __init__(self, palavra_secreta):
        self.palavra_secreta = palavra_secreta.upper()
        self.letras_descobertas = ["_" for _ in self.palavra_secreta]
        self.tentativas_restantes = 6
        self.letras_erradas = []

        self.janela = tk.Tk()
        self.janela.title("Jogo da Forca")

        self.label_palavra = tk.Label(self.janela, text=" ".join(self.letras_descobertas), font=("Helvetica", 20))
        self.label_palavra.pack(pady=10)

        self.label_tentativas = tk.Label(self.janela, text=f"Tentativas restantes: {self.tentativas_restantes}", font=("Helvetica", 14))
        self.label_tentativas.pack(pady=5)

        self.label_erradas = tk.Label(self.janela, text="Letras erradas: Nenhuma", font=("Helvetica", 14))
        self.label_erradas.pack(pady=5)

        self.entry_letra = tk.Entry(self.janela, font=("Helvetica", 14))
        self.entry_letra.pack(pady=10)

        self.botao_tentar = tk.Button(self.janela, text="Tentar", command=self.tentar_letra, font=("Helvetica", 14))
        self.botao_tentar.pack(pady=5)

        self.janela.mainloop()

    def tentar_letra(self):
        letra = self.entry_letra.get().upper()
        self.entry_letra.delete(0, tk.END)

        if len(letra) != 1 or not letra.isalpha():
            messagebox.showwarning("Entrada inválida", "Por favor, insira apenas uma letra.")
            return

        if letra in self.letras_descobertas or letra in self.letras_erradas:
            messagebox.showinfo("Letra repetida", "Você já tentou essa letra.")
            return

        if letra in self.palavra_secreta:
            for i, l in enumerate(self.palavra_secreta):
                if l == letra:
                    self.letras_descobertas[i] = letra
            self.label_palavra.config(text=" ".join(self.letras_descobertas))
        else:
            self.tentativas_restantes -= 1
            self.letras_erradas.append(letra)
            self.label_tentativas.config(text=f"Tentativas restantes: {self.tentativas_restantes}")
            self.label_erradas.config(text=f"Letras erradas: {', '.join(self.letras_erradas)}")

        if "_" not in self.letras_descobertas:
            messagebox.showinfo("Parabéns!", "Você venceu o jogo!")
            self.janela.destroy()
        elif self.tentativas_restantes == 0:
            messagebox.showinfo("Fim de jogo", f"Você perdeu! A palavra era: {self.palavra_secreta}")
            self.janela.destroy()

if __name__ == "__main__":
    palavra = "mingau"  # Substitua pela palavra desejada
    JogoDaForca(palavra)
