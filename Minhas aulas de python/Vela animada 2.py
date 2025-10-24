import tkinter as tk
import random
import time
import math

#!/usr/bin/env python3
# teste2.py
# Animação de uma vela que queima até o fim e diminui com o tempo (tkinter)


LARGURA = 300
ALTURA = 420

CANDLE_W = 80
INITIAL_WAX_H = 220
BURN_DURATION_SEC = 30.0  # tempo total até apagar
UPDATE_MS = 40

class VelaApp:
    def __init__(self, root):
        self.root = root
        root.title("Vela Animada")
        self.canvas = tk.Canvas(root, width=LARGURA, height=ALTURA, bg="#222")
        self.canvas.pack()

        # posição da vela (centro)
        self.cx = LARGURA // 2
        self.base_y = ALTURA - 40

        # estado da cera
        self.wax_h = INITIAL_WAX_H
        self.burn_rate = INITIAL_WAX_H / (BURN_DURATION_SEC * 1000.0 / UPDATE_MS)

        # itens do canvas
        self.items = {}
        self.smoke_particles = []
        self.extinguished = False
        self.start_time = time.time()

        self.draw_static()
        self.update()

    def draw_static(self):
        # prato/base da vela
        self.canvas.create_oval(self.cx - 80, self.base_y + 10, self.cx + 80, self.base_y + 30, fill="#333", outline="#111")
        # label tempo (opcional)
        self.items['tempo_text'] = self.canvas.create_text(10, 10, anchor="nw", fill="#eee", font=("Helvetica", 10), text="")

    def draw_wax(self):
        # remove anterior
        if 'wax' in self.items:
            self.canvas.delete(self.items['wax'])
        if 'wick' in self.items:
            self.canvas.delete(self.items['wick'])

        top_y = self.base_y - self.wax_h
        left = self.cx - CANDLE_W // 2
        right = self.cx + CANDLE_W // 2

        # forma irregular da cera (ligeira ondulação superior)
        path = []
        steps = 12
        for i in range(steps + 1):
            t = i / steps
            x = left + t * (right - left)
            wobble = math.sin(t * math.pi * 3 + time.time() * 2) * 3
            y = top_y + wobble
            path.append((x, y))
        # completar o retângulo
        coords = []
        for x, y in path:
            coords.append(x); coords.append(y)
        coords.append(right); coords.append(self.base_y)
        coords.append(left); coords.append(self.base_y)

        self.items['wax'] = self.canvas.create_polygon(*coords, fill="#fff5e6", outline="#e6d5b8")

        # wick
        wick_x = self.cx
        wick_y1 = top_y - 1
        wick_y2 = wick_y1 - 12
        self.items['wick'] = self.canvas.create_line(wick_x, wick_y1, wick_x, wick_y2, fill="#2b2b2b", width=2)

    def draw_flame(self):
        # remove anterior
        if 'flame_outer' in self.items:
            self.canvas.delete(self.items['flame_outer'])
        if 'flame_inner' in self.items:
            self.canvas.delete(self.items['flame_inner'])
        if 'spark' in self.items:
            self.canvas.delete(self.items['spark'])

        if self.extinguished:
            return

        top_y = self.base_y - self.wax_h
        # flicker usando fator aleatório
        flick = 1.0 + (random.random() - 0.5) * 0.25
        flame_h = 30 * flick
        flame_w = 18 * flick

        cx = self.cx
        cy = top_y - 6 - flame_h / 2

        # outer (laranja)
        x0 = cx - flame_w
        y0 = cy - flame_h
        x1 = cx + flame_w
        y1 = cy + flame_h
        color_outer = "#ff8a1c"
        self.items['flame_outer'] = self.canvas.create_oval(x0, y0, x1, y1, fill=color_outer, outline="")

        # inner (amarelo)
        inner_h = flame_h * (0.6 + random.random() * 0.1)
        inner_w = flame_w * 0.6
        xi0 = cx - inner_w
        yi0 = cy - inner_h * 0.8
        xi1 = cx + inner_w
        yi1 = cy + inner_h * 0.4
        color_inner = "#ffe36b"
        self.items['flame_inner'] = self.canvas.create_oval(xi0, yi0, xi1, yi1, fill=color_inner, outline="")

        # pequena centelha (brilho)
        if random.random() < 0.2:
            sx = cx + (random.random() - 0.5) * flame_w * 0.8
            sy = yi0 - random.random() * 6
            self.items['spark'] = self.canvas.create_oval(sx-2, sy-2, sx+2, sy+2, fill="#fff7cc", outline="")

    def update_smoke(self):
        # criar novas partículas após apagar
        if self.extinguished and random.random() < 0.25:
            self.smoke_particles.append({
                'x': self.cx + (random.random() - 0.5) * 20,
                'y': self.base_y - 5 - self.wax_h,
                'r': 6 + random.random() * 8,
                'life': 1.0,
                'drift': (random.random() - 0.5) * 0.6
            })
        # atualizar partículas
        alive = []
        for p in self.smoke_particles:
            p['y'] -= 0.8 + random.random() * 0.8
            p['x'] += p['drift']
            p['r'] *= 1.01
            p['life'] -= 0.02
            alive.append(p) if p['life'] > 0.02 else None
        self.smoke_particles = alive

        # desenhar (apagar anteriores)
        # limpar itens smoke*
        for key in list(self.items.keys()):
            if key.startswith('smoke_'):
                self.canvas.delete(self.items.pop(key))
        # recriar
        for i, p in enumerate(self.smoke_particles):
            gray = int(180 + (1 - p['life']) * 60)
            gray = max(120, min(240, gray))
            col = f"#{gray:02x}{gray:02x}{gray:02x}"
            k = f"smoke_{i}"
            self.items[k] = self.canvas.create_oval(p['x']-p['r'], p['y']-p['r'], p['x']+p['r'], p['y']+p['r'], fill=col, outline="")

    def update(self):
        elapsed = time.time() - self.start_time
        remaining = max(0.0, BURN_DURATION_SEC - elapsed)
        self.canvas.itemconfig(self.items['tempo_text'], text=f"Tempo restante: {remaining:0.1f}s")

        if not self.extinguished:
            # reduzir cera
            self.wax_h -= self.burn_rate
            if self.wax_h <= 0:
                self.wax_h = 0
                self.extinguished = True

        self.draw_wax()
        # flame should shrink when almost out
        if not self.extinguished:
            # small shrink when near end
            self.draw_flame()
        else:
            # apagar chama (manter pequenas fumacinhas)
            if 'flame_outer' in self.items:
                self.canvas.delete(self.items.pop('flame_outer'))
            if 'flame_inner' in self.items:
                self.canvas.delete(self.items.pop('flame_inner'))
            if 'spark' in self.items:
                self.canvas.delete(self.items.pop('spark'))

        self.update_smoke()

        # se houve extinção e pouca fumaça restante, parar atualização final após algum tempo
        if self.extinguished and not self.smoke_particles:
            # manter a cena final por alguns instantes e parar a animação
            # aqui continuamos chamando update para manter UI responsiva; você pode parar se quiser.
            self.canvas.itemconfig(self.items['tempo_text'], text="Vela apagada")
            # ainda chamamos after para permitir fechar a janela normalmente
            self.root.after(UPDATE_MS, self.update)
        else:
            self.root.after(UPDATE_MS, self.update)

if __name__ == "__main__":
    root = tk.Tk()
    app = VelaApp(root)
    root.mainloop()