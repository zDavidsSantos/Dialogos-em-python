import tkinter as tk

class LampApp:
    def __init__(self, master):
        self.master = master
        master.title("Efeito Lâmpada")
        self.canvas = tk.Canvas(master, width=220, height=260, bg="#222")
        self.canvas.pack(padx=10, pady=10)
        # lamp position
        self.cx, self.cy, self.r = 110, 100, 60
        self.glow = self.canvas.create_oval(self.cx - self.r - 20, self.cy - self.r - 20,
                                            self.cx + self.r + 20, self.cy + self.r + 20,
                                            fill="#000000", outline="")
        self.bulb = self.canvas.create_oval(self.cx - self.r, self.cy - self.r,
                                            self.cx + self.r, self.cy + self.r,
                                            fill="#111111", outline="#333333", width=2)
        self.btn = tk.Button(master, text="Ligar", width=12, command=self.toggle)
        self.btn.pack(pady=(5,10))
        # animation state
        self.brightness = 0.0  # 0.0..1.0
        self.target = 0.0
        self.animating = False

    def toggle(self):
        self.target = 1.0 if self.target == 0.0 else 0.0
        self.btn.config(text="Desligar" if self.target == 1.0 else "Ligar")
        if not self.animating:
            self.animate()

    def animate(self):
        self.animating = True
        step = 0.06
        if self.brightness < self.target:
            self.brightness = min(self.brightness + step, self.target)
        elif self.brightness > self.target:
            self.brightness = max(self.brightness - step, self.target)
        self.update_visual()
        if abs(self.brightness - self.target) > 1e-3:
            self.master.after(30, self.animate)
        else:
            self.animating = False

    def update_visual(self):
        # interpolate color from dark to warm yellow
        def mix(a, b, t): return int(a + (b - a) * t)
        # bulb core: from very dark to warm yellow
        r = mix(17, 255, self.brightness)
        g = mix(17, 200, self.brightness)
        b = mix(17, 80, self.brightness)
        core_color = f"#{r:02x}{g:02x}{b:02x}"
        # glow: brighter and more transparent effect simulated by lighter color
        gr = mix(0, 255, min(1.0, self.brightness * 1.2))
        gg = mix(0, 200, min(1.0, self.brightness * 1.2))
        gb = mix(0, 80, min(1.0, self.brightness * 1.2))
        glow_color = f"#{gr:02x}{gg:02x}{gb:02x}"
        # scale glow size slightly with brightness
        extra = int(20 * self.brightness)
        self.canvas.coords(self.glow,
                           self.cx - self.r - 20 - extra, self.cy - self.r - 20 - extra,
                           self.cx + self.r + 20 + extra, self.cy + self.r + 20 + extra)
        self.canvas.itemconfig(self.bulb, fill=core_color)
        self.canvas.itemconfig(self.glow, fill=glow_color)

if __name__ == "__main__":
    root = tk.Tk()
    app = LampApp(root)
    root.mainloop()


