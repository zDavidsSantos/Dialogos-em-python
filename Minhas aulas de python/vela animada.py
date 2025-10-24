import math
import random
import pygame
from collections import deque

# Configurações
WIDTH, HEIGHT = 480, 720
FPS = 60

# Candle physics / timer mapping
MAX_WAX_HEIGHT = 380  # pixels of wax when full
MIN_WAX_HEIGHT = 30
WAX_PER_SECOND = 1.5  # pixels of wax consumed per second
DEFAULT_SECONDS = int(MAX_WAX_HEIGHT / WAX_PER_SECOND)  # default full time

# Add time amounts
ADD_SPACE_SECONDS = 30
ADD_CLICK_SECONDS = 10
MAX_SECONDS_CAP = int(MAX_WAX_HEIGHT / WAX_PER_SECOND)

# Colors
BG = (20, 20, 28)
WAX_COLOR = (255, 245, 230)
WAX_SHADOW = (210, 190, 170)
CANDLE_BASE = (100, 40, 30)
FLAME_INNER = (255, 245, 140)
FLAME_MID = (255, 170, 40)
FLAME_OUTER = (255, 100, 10)
SMOKE_COLOR = (180, 180, 190)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Vela temporizador")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 28)
bigfont = pygame.font.SysFont(None, 44)


class SmokeParticle:
    def __init__(self, x, y):
        self.x = x + random.uniform(-6, 6)
        self.y = y
        self.vx = random.uniform(-10, 10) * 0.01
        self.vy = random.uniform(-20, -50) * 0.01
        self.life = random.uniform(1.0, 1.8)
        self.age = 0
        self.size = random.uniform(6, 14)

    def update(self, dt):
        self.age += dt
        self.x += self.vx * dt * 60
        self.y += self.vy * dt * 60 - (0.02 * self.age * 60)
        self.size += 0.02 * dt * 60

    def draw(self, surf):
        a = max(0, 200 * (1 - self.age / self.life))
        if a <= 0:
            return
        s = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
        pygame.draw.circle(s, (SMOKE_COLOR[0], SMOKE_COLOR[1], SMOKE_COLOR[2], int(a)), (int(self.size), int(self.size)), int(self.size))
        surf.blit(s, (self.x - self.size, self.y - self.size))


def draw_candle(surf, center_x, base_y, wax_height, wick_length, melted_top_offset):
    candle_width = 120
    candle_half = candle_width // 2

    # base (stand)
    base_rect = pygame.Rect(center_x - candle_half - 10, base_y + 6, candle_width + 20, 24)
    pygame.draw.rect(surf, CANDLE_BASE, base_rect, border_radius=6)

    # wax body
    top_y = base_y - wax_height
    body_rect = pygame.Rect(center_x - candle_half, top_y, candle_width, wax_height)
    # body shadow
    shadow = pygame.Surface((body_rect.w, body_rect.h), pygame.SRCALPHA)
    for i in range(body_rect.h):
        shade = 8 + int(60 * (i / body_rect.h))
        pygame.draw.line(shadow, (shade, shade - 20, shade - 60, 6), (0, i), (body_rect.w, i))
    surf.blit(shadow, (body_rect.x, body_rect.y), special_flags=pygame.BLEND_RGBA_ADD)

    pygame.draw.rect(surf, WAX_COLOR, body_rect, border_radius=14)

    # melted top (irregular)
    top_surface = pygame.Surface((candle_width, 40), pygame.SRCALPHA)
    top_surface.fill((0, 0, 0, 0))
    # draw a wavy top
    points = []
    for i in range(0, candle_width + 1, 6):
        angle = i * 0.2 + melted_top_offset
        y = 8 * math.sin(angle) + random.uniform(-1.4, 1.4)
        points.append((i, 20 + y))
    points = [(0, 40)] + points + [(candle_width, 40)]
    pygame.draw.polygon(top_surface, WAX_SHADOW, points)
    top_surface2 = pygame.Surface((candle_width, 40), pygame.SRCALPHA)
    pygame.draw.polygon(top_surface2, WAX_COLOR, points)
    surf.blit(top_surface2, (center_x - candle_half, top_y - 20))
    surf.blit(top_surface, (center_x - candle_half, top_y - 20), special_flags=pygame.BLEND_RGBA_MIN)

    # wick
    wick_x = center_x
    wick_y_top = top_y - 10
    pygame.draw.line(surf, (20, 20, 20), (wick_x, wick_y_top), (wick_x, wick_y_top + wick_length), 2)
    return wick_x, wick_y_top


def draw_flame(surf, x, y, alive, flicker):
    if not alive:
        return
    # flicker offsets
    sx = math.sin(flicker * 3.1) * 2 + random.uniform(-1.2, 1.2)
    sy = math.cos(flicker * 2.7) * 1.2 + random.uniform(-0.8, 0.8)

    # outer glow
    out_size = 28 + int(abs(math.sin(flicker * 1.3)) * 6)
    s = pygame.Surface((out_size * 2, out_size * 2), pygame.SRCALPHA)
    pygame.draw.circle(s, (FLAME_OUTER[0], FLAME_OUTER[1], FLAME_OUTER[2], 80), (out_size, out_size), out_size)
    surf.blit(s, (x - out_size + sx, y - out_size + sy), special_flags=pygame.BLEND_RGBA_ADD)

    # mid flame (teardrop)
    points = [
        (x + sx, y - 4 + sy),
        (x + 10 + sx, y + 10 + sy),
        (x - 10 + sx, y + 10 + sy)
    ]
    pygame.draw.polygon(surf, FLAME_MID, points)

    # inner core
    pygame.draw.circle(surf, FLAME_INNER, (int(x + sx), int(y + sy)), 6)


def format_time(secs):
    secs = max(0, int(round(secs)))
    m = secs // 60
    s = secs % 60
    return f"{m:02}:{s:02}"


def main():
    running = True
    center_x = WIDTH // 2
    base_y = HEIGHT - 120

    seconds_remaining = DEFAULT_SECONDS
    wax_height = min(MAX_WAX_HEIGHT, max(MIN_WAX_HEIGHT, seconds_remaining * WAX_PER_SECOND))
    melted_offset = 0.0
    particles = deque()
    flame_alive = True
    smoke_timer = 0.0
    flicker = 0.0

    last_add_time_cooldown = 0.0

    while running:
        dt = clock.tick(FPS) / 1000.0
        flicker += dt * 6.0
        melted_offset += dt * 2.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    seconds_remaining = min(MAX_SECONDS_CAP, seconds_remaining + ADD_SPACE_SECONDS)
                elif event.key == pygame.K_PLUS or event.key == pygame.K_EQUALS:
                    seconds_remaining = min(MAX_SECONDS_CAP, seconds_remaining + 5)
                elif event.key == pygame.K_MINUS:
                    seconds_remaining = max(0, seconds_remaining - 5)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    seconds_remaining = min(MAX_SECONDS_CAP, seconds_remaining + ADD_CLICK_SECONDS)

        # update timer & wax height
        if seconds_remaining > 0:
            seconds_remaining -= dt
            wax_height = seconds_remaining * WAX_PER_SECOND
            wax_height = max(MIN_WAX_HEIGHT, min(MAX_WAX_HEIGHT, wax_height))
            flame_alive = True
        else:
            seconds_remaining = 0
            flame_alive = False
            # slowly settle wax to minimum
            wax_height = max(MIN_WAX_HEIGHT, wax_height - dt * 5)

        # spawn smoke when flame just extinguished or when still alive occasionally
        smoke_timer += dt
        if flame_alive and smoke_timer > 0.08:
            # small smoke from flame
            particles.append(SmokeParticle(center_x, base_y - wax_height - 28))
            if len(particles) > 120:
                particles.popleft()
            smoke_timer = 0.0
        elif not flame_alive and smoke_timer > 0.2:
            # occasional single puff when out
            if random.random() < 0.4:
                particles.append(SmokeParticle(center_x, base_y - wax_height - 20))
            smoke_timer = 0.0

        # update particles
        for p in list(particles):
            p.update(dt)
            if p.age >= p.life:
                particles.popleft()

        # draw
        screen.fill(BG)

        # glow behind candle
        glow = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        gx = 140 + int(90 * math.sin(flicker * 1.2))
        pygame.draw.ellipse(glow, (255, 220, 180, 40), (center_x - gx, base_y - wax_height - 180, gx * 2, 220))
        screen.blit(glow, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        wick_x, wick_y_top = draw_candle(screen, center_x, base_y, wax_height, wick_length=10, melted_top_offset=melted_offset)
        # flame position (above wick)
        flame_x, flame_y = wick_x, wick_y_top - 6
        draw_flame(screen, flame_x, flame_y, flame_alive, flicker)

        # draw drips: occasional falling droplets near top
        if flame_alive and random.random() < 0.02:
            drop_x = center_x + random.uniform(-40, 40)
            drop_y = base_y - wax_height + random.uniform(4, 18)
            pygame.draw.circle(screen, WAX_COLOR, (int(drop_x), int(drop_y)), 4)

        # draw smoke particles
        for p in particles:
            p.draw(screen)

        # HUD: time
        time_text = bigfont.render(format_time(seconds_remaining), True, (240, 240, 245))
        screen.blit(time_text, (20, 20))

        hint = font.render("SPACE +30s  |  Click +10s  |  +/- change", True, (200, 200, 210))
        screen.blit(hint, (20, 64))

        # realistic details: small label showing wax % left
        percent = int((wax_height - MIN_WAX_HEIGHT) / (MAX_WAX_HEIGHT - MIN_WAX_HEIGHT) * 100)
        label = font.render(f"Cera: {max(0, percent)}%", True, (220, 220, 220))
        screen.blit(label, (20, 100))

        if not flame_alive:
            out = font.render("A vela foi apagada", True, (200, 140, 140))
            screen.blit(out, (WIDTH - out.get_width() - 20, 20))

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()