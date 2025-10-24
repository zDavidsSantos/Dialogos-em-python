import tkinter as tk
import random
import math
import time

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vela animada com botões "Acender" e "Soprar"
# Salve como efeito_vela.py e execute: python3 efeito_vela.py


class CandleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Vela animada")
        self.w, self.h = 360, 520
        self.canvas = tk.Canvas(root, width=self.w, height=self.h, bg="#222")
        self.canvas.pack()

        # estado
        self.lit = False
        self.blowing = False
        self.flame_size = 0.0
        self.flame_phase = 0.0
        self.smoke_particles = []

        # desenho da vela (posição fixa)
        self.candle_x = self.w // 2
        self.candle_y = self.h - 140
        self.candle_width = 120
        self.candle_height = 260
        self.wick_len = 12

        # botões
        frm = tk.Frame(root, bg="#222")
        frm.pack(fill="x", pady=6)
        self.btn_light = tk.Button(frm, text="Acender", command=self.light, width=12)
        self.btn_blow = tk.Button(frm, text="Soprar", command=self.blow, width=12, state="disabled")
        self.btn_light.pack(side="left", padx=8)
        self.btn_blow.pack(side="left", padx=8)

        # desenho inicial
        self.draw_static()
        # animação recorrente
        self.last_time = time.time()
        self.animate()

        # atalho pressionar espaço para soprar
        root.bind("<space>", lambda e: self.blow())

    def draw_static(self):
        self.canvas.delete("static")
        x, y = self.candle_x, self.candle_y
        w, h = self.candle_width, self.candle_height
        # sombra/base
        self.canvas.create_oval(x - w//2 - 20, y + h - 10, x + w//2 + 20, y + h + 30,
                                fill="#111", outline="", tags="static")
        # corpo da vela com gradiente aproximado (retângulos)
        for i in range(8):
            t = i / 7
            r = int(230 - 40 * t)
            g = int(230 - 40 * t)
            b = int(220 - 30 * t)
            color = f"#{r:02x}{g:02x}{b:02x}"
            y1 = y - h//2 + int(t * h)
            y2 = y - h//2 + int((t + 1/8) * h)
            self.canvas.create_rectangle(x - w//2, y1, x + w//2, y2,
                                         fill=color, outline=color, tags="static")
        # pingentes de cera (simples)
        for i in range(5):
            sx = x - w//2 + 20 + i * (w - 40) / 4
            sy = y - h//2 + int(h * 0.15 + (i % 2) * 8)
            self.canvas.create_oval(sx - 6, sy - 10, sx + 6, sy + 6, fill="#f5f0e6", outline="", tags="static")
        # pavio
        self.wick_x = x
        self.wick_y = y - h//2 - 1
        self.canvas.create_line(self.wick_x, self.wick_y, self.wick_x, self.wick_y - self.wick_len,
                                fill="#222", width=2, capstyle="round", tags="static")

    def draw_flame(self, size, offset_x=0, opacity=1.0):
        # remove flame layer
        self.canvas.delete("flame")
        x = self.wick_x + offset_x
        y = self.wick_y - self.wick_len - 2
        # sizes
        inner = max(2, int(size * 0.5))
        mid = max(4, int(size * 0.9))
        outer = max(8, int(size * 1.6))
        # color with simulated opacity by mixing to background color (#222)
        def mix_color(hex_color, a):
            # hex_color like "#rrggbb", a in [0,1] -> blends toward bg "#222"
            r = int(hex_color[1:3], 16)
            g = int(hex_color[3:5], 16)
            b = int(hex_color[5:7], 16)
            br, bg, bb = 0x22, 0x22, 0x22
            rr = int(r * a + br * (1 - a))
            gg = int(g * a + bg * (1 - a))
            bb2 = int(b * a + bb * (1 - a))
            return f"#{rr:02x}{gg:02x}{bb2:02x}"
        # outer (orange)
        self.canvas.create_oval(x - outer, y - outer*1.1, x + outer, y + outer*0.2,
                                fill=mix_color("#ff8a00", opacity), outline="", tags="flame")
        # mid (yellow)
        self.canvas.create_oval(x - mid, y - mid, x + mid, y + mid*0.2,
                                fill=mix_color("#ffd54d", opacity), outline="", tags="flame")
        # inner (bright)
        self.canvas.create_oval(x - inner, y - inner*1.1, x + inner, y + inner*0.1,
                                fill=mix_color("#fff6c8", opacity), outline="", tags="flame")
        # coração da chama (pequeno ponto)
        self.canvas.create_oval(x - 2, y - 3, x + 2, y + 1, fill=mix_color("#ffffff", opacity), outline="", tags="flame")

    def spawn_smoke(self, count=20):
        for _ in range(count):
            angle = random.uniform(-math.pi/2 - 0.7, -math.pi/2 + 0.7)
            speed = random.uniform(0.6, 2.4)
            vx = math.cos(angle) * speed
            vy = math.sin(angle) * speed
            p = {
                "x": self.wick_x + random.uniform(-6, 6),
                "y": self.wick_y - self.wick_len - 4 + random.uniform(-4, 4),
                "vx": vx * 0.7,
                "vy": vy * 0.7,
                "age": 0.0,
                "life": random.uniform(0.9, 1.8),
                "size": random.uniform(6, 20)
            }
            self.smoke_particles.append(p)

    def update_smoke(self, dt):
        # update positions and draw
        self.canvas.delete("smoke")
        new_particles = []
        for p in self.smoke_particles:
            p["age"] += dt
            if p["age"] >= p["life"]:
                continue
            # gentle drift and rise
            p["x"] += p["vx"]
            p["y"] += p["vy"] - 0.4 * dt * 60  # upward bias
            p["vx"] += random.uniform(-0.05, 0.05)
            p["vy"] += random.uniform(-0.03, 0.03)
            t = p["age"] / p["life"]
            # smoke color from dark gray to light gray
            v = int(120 + 135 * t)
            v = max(0, min(255, v))
            color = f"#{v:02x}{v:02x}{v:02x}"
            # size grows a bit
            s = p["size"] * (1 + 0.6 * t)
            self.canvas.create_oval(p["x"] - s, p["y"] - s, p["x"] + s, p["y"] + s,
                                    fill=color, outline="", tags="smoke")
            new_particles.append(p)
        self.smoke_particles = new_particles

    def light(self):
        if self.lit:
            return
        self.lit = True
        self.blowing = False
        self.btn_light.config(state="disabled")
        self.btn_blow.config(state="normal")
        # small initial flame
        self.flame_size = 6.0
        self.flame_phase = random.random() * 10

    def blow(self):
        if not self.lit:
            return
        # iniciar sopro: fade rápido e gerar fumaça
        self.blowing = True
        self.btn_blow.config(state="disabled")
        self.spawn_smoke(count=30)

    def animate(self):
        now = time.time()
        dt = now - self.last_time
        self.last_time = now

        # animação da chama
        if self.lit and not self.blowing:
            # flutuação natural
            self.flame_phase += dt * 6.0
            flick = math.sin(self.flame_phase * 2.0) * 1.8 + math.sin(self.flame_phase * 5.3) * 0.8
            target = 18 + flick + random.uniform(-1.2, 1.2)
            # suaviza
            self.flame_size += (target - self.flame_size) * min(1.0, dt * 8)
            offset = int(math.sin(self.flame_phase) * 4)
            # leve variação de brilho/opa
            opacity = 0.9 + 0.1 * math.sin(self.flame_phase * 1.7)
            self.draw_flame(self.flame_size, offset_x=offset, opacity=opacity)
        elif self.lit and self.blowing:
            # reduzir a chama rapidamente
            self.flame_size -= dt * 46.0  # apaga rápido
            if self.flame_size <= 0:
                self.flame_size = 0
                # apagar
                self.lit = False
                self.blowing = False
                self.canvas.delete("flame")
                self.btn_light.config(state="normal")
                # gerar mais fumaça residual
                self.spawn_smoke(count=18)
            else:
                # deslocamento mais forte durante sopro
                offset = int((random.random() - 0.5) * 24)
                opacity = max(0.0, self.flame_size / 18.0)
                self.draw_flame(self.flame_size, offset_x=offset, opacity=opacity)
        else:
            # apagada, desenhar possível brasa fraca
            self.canvas.delete("flame")
            # pequeno brilho ocasional (brasa)
            if random.random() < 0.02:
                self.draw_flame(4, offset_x=random.randint(-2, 2), opacity=0.15)

        # atualizar fumaça sempre
        self.update_smoke(dt)

        # agendar próximo frame
        self.root.after(30, self.animate)


if __name__ == "__main__":
    root = tk.Tk()
    app = CandleApp(root)
    root.mainloop()