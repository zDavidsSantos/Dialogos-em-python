import turtle
import time
import math

# Configuração da tela
screen = turtle.Screen()
screen.bgcolor("black")
screen.title("Relógio de Anéis")
screen.setup(width=600, height=600)
screen.tracer(0)

# Função para desenhar um anel
def draw_ring(t, radius, color):
    t.penup()
    t.goto(0, -radius)
    t.pendown()
    t.color(color)
    t.circle(radius)

# Função para posicionar o marcador no anel
def move_marker(t, radius, angle):
    t.penup()
    x = radius * math.cos(math.radians(angle))
    y = radius * math.sin(math.radians(angle))
    t.goto(x, y)
    t.pendown()

# Criar tartarugas para os anéis
hour_ring = turtle.Turtle()
minute_ring = turtle.Turtle()
second_ring = turtle.Turtle()

hour_marker = turtle.Turtle()
minute_marker = turtle.Turtle()
second_marker = turtle.Turtle()

# Configuração dos anéis
for t in [hour_ring, minute_ring, second_ring]:
    t.hideturtle()
    t.speed(0)
    t.width(2)

hour_ring.color("blue")
minute_ring.color("green")
second_ring.color("red")

# Configuração dos marcadores
for t in [hour_marker, minute_marker, second_marker]:
    t.shape("circle")
    t.shapesize(0.5)
    t.penup()

hour_marker.color("blue")
minute_marker.color("green")
second_marker.color("red")

# Loop principal do relógio
while True:
    # Obter o horário atual
    current_time = time.localtime()
    hours = current_time.tm_hour % 12
    minutes = current_time.tm_min
    seconds = current_time.tm_sec

    # Calcular os ângulos para os marcadores
    hour_angle = 360 * (hours / 12)
    minute_angle = 360 * (minutes / 60)
    second_angle = 360 * (seconds / 60)

    # Desenhar os anéis
    hour_ring.clear()
    minute_ring.clear()
    second_ring.clear()

    draw_ring(hour_ring, 100, "blue")
    draw_ring(minute_ring, 150, "green")
    draw_ring(second_ring, 200, "red")

    # Posicionar os marcadores
    move_marker(hour_marker, 100, hour_angle)
    move_marker(minute_marker, 150, minute_angle)
    move_marker(second_marker, 200, second_angle)

    # Atualizar a tela
    screen.update()
    time.sleep(1)