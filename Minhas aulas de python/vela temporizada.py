import tkinter as tk
import time
import random

#!/usr/bin/env python3
# vela temporizada.py
# Vela animada que funciona como temporizador de 1 minuto.
# Conforme o tempo passa, a vela encolhe e a chama se apaga.


DURATION = 60.0  # segundos

class CandleTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Vela Temporizada - 1 minuto")
        self.canvas_w = 320
        self.canvas_h = 420
        self.canvas = tk.Canvas(root, width=self.canvas_w, height=self.canvas_h, bg="#222")
        self.canvas.pack()

        # Layout da vela
        self.candle_width = 100
        self.candle_bottom = 320
        self.candle_initial_height = 200
        self.candle_left = (self.canvas_w - self.candle_width) // 2
        self.candle_right = self.candle_left + self.candle_width

        # Texto do tempo
        self.time_text = self.canvas.create_text(self.canvas_w//2, 30, text="", fill="white", font=("Helvetica", 18, "bold"))

        # Desenhar elementos estáticos
        self._draw_base()
        self.start_time = time.time()
        self.flame_parts = []
        self.melt_pool = None

        # Cria a vela e a chama
        self.candle_rect = self.canvas.create_rectangle(
            self.candle_left, self.candle_bottom - self.candle_initial_height,
            self.candle_right, self.candle_bottom,
            fill="#FFF2CC", outline="#E6C57A"
        )
        # pavio (wick)
        wick_x = (self.candle_left + self.candle_right) // 2
        self.wick = self.canvas.create_line(wick_x, self.candle_bottom - self.candle_initial_height - 4,
                                            wick_x, self.candle_bottom - self.candle_initial_height - 16,
                                            fill="#222", width=2)
        # chama inicial
        self._create_flame()
        # pool de cera derretida
        self.melt_pool = self.canvas.create_oval(
            self.candle_left + 10, self.candle_bottom - 8,
            self.candle_right - 10, self.candle_bottom + 6,
            fill="#E6C57A", outline=""
        )

        # Inicia animação
        self._update()

    def _draw_base(self):
        # Suporte da vela (mesa)
        self.canvas.create_rectangle(0, self.candle_bottom + 10, self.canvas_w, self.canvas_h, fill="#2b2b2b", outline="")

    def _create_flame(self):
        # cria três camadas de flame (cores) como polígonos/ovais
        wick_x = (self.candle_left + self.candle_right) // 2
        top_y = self.candle_bottom - self.candle_initial_height - 30
        # camadas: externo laranja, meio amarelo, interno branco
        outer = self.canvas.create_oval(wick_x-18, top_y-24, wick_x+18, top_y+6, fill="#FF6A00", outline="")
        middle = self.canvas.create_oval(wick_x-12, top_y-18, wick_x+12, top_y+2, fill="#FFD24D", outline="")
        inner = self.canvas.create_oval(wick_x-6, top_y-12, wick_x+6, top_y+1, fill="#FFF9E6", outline="")
        self.flame_parts = [outer, middle, inner]

    def _remove_flame(self):
        for p in self.flame_parts:
            try:
                self.canvas.delete(p)
            except:
                pass
        self.flame_parts = []

    def _update(self):
        elapsed = time.time() - self.start_time
        t = min(max(elapsed, 0.0), DURATION)
        remaining = max(DURATION - t, 0.0)

        # Atualiza texto MM:SS
        mins = int(remaining) // 60
        secs = int(remaining) % 60
        self.canvas.itemconfigure(self.time_text, text=f"{mins:02d}:{secs:02d}")

        # Calcula nova altura da vela proporcional ao tempo restante
        frac = (remaining / DURATION) if DURATION > 0 else 0
        current_height = max(8, int(self.candle_initial_height * frac))  # mínimo para não sumir instantaneamente
        top_y = self.candle_bottom - current_height

        # Atualiza retângulo da vela (topo se move para baixo conforme derrete)
        self.canvas.coords(self.candle_rect, self.candle_left, top_y, self.candle_right, self.candle_bottom)

        # Move pavio para topo atual da vela
        wick_x = (self.candle_left + self.candle_right) // 2
        self.canvas.coords(self.wick, wick_x, top_y - 4, wick_x, top_y - 16)

        # Atualiza pool de cera: aumenta levemente conforme derrete
        pool_expand = int((1 - frac) * 14)
        self.canvas.coords(self.melt_pool,
                           self.candle_left + 10 - pool_expand//2,
                           self.candle_bottom - 8,
                           self.candle_right - 10 + pool_expand//2,
                           self.candle_bottom + 6 + pool_expand//3)

        # Atualiza chama (flicker) se ainda houver tempo
        if remaining > 0.15:
            if not self.flame_parts:
                self._create_flame()
            # pequeno flicker: varia posição e tamanho
            flicker = random.uniform(-2.2, 2.2)
            scale = 1.0 + random.uniform(-0.08, 0.08)
            # posição baseada no topo atual da vela
            flame_center_x = wick_x + flicker
            flame_center_y = top_y - 18 + random.uniform(-1.5, 1.5)
            # redesenha cada camada com offsets
            outer_r = 18 * scale
            middle_r = 12 * scale
            inner_r = 6 * scale
            # coords for ovals: (x-r, y-r, x+r, y+r)
            self.canvas.coords(self.flame_parts[0], flame_center_x - outer_r, flame_center_y - outer_r,
                               flame_center_x + outer_r, flame_center_y + outer_r)
            self.canvas.coords(self.flame_parts[1], flame_center_x - middle_r, flame_center_y - middle_r,
                               flame_center_x + middle_r, flame_center_y + middle_r)
            self.canvas.coords(self.flame_parts[2], flame_center_x - inner_r, flame_center_y - inner_r,
                               flame_center_x + inner_r, flame_center_y + inner_r)
            # ligeira mudança de cor para simular calor
            # quanto menor a vela (mais derretida), chama tende a diminuir e ficar menos intensa
            color_shift = int(255 * frac)
            orange = f"#{255:02x}{int(106*frac + 60*(1-frac)):02x}00"
            yellow = f"#ffd{int(36*frac):02x}"
            try:
                self.canvas.itemconfigure(self.flame_parts[0], fill=orange)
                self.canvas.itemconfigure(self.flame_parts[1], fill="#FFD24D")
                self.canvas.itemconfigure(self.flame_parts[2], fill="#FFF9E6")
            except Exception:
                pass
        else:
            # apagar a chama ao final
            if self.flame_parts:
                self._remove_flame()
            # mostrar mensagem de fim
            self.canvas.itemconfigure(self.time_text, text="Tempo esgotado")

        # repetir até o fim (chamada a cada 60 ms para suavidade)
        if elapsed < DURATION + 1.0:
            self.root.after(60, self._update)
        else:
            # garante chama removida
            self._remove_flame()

if __name__ == "__main__":
    root = tk.Tk()
    app = CandleTimer(root)
    root.mainloop()