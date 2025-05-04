import pygame
import time
import math

# Inicializar o pygame
pygame.init()

# Configurações da tela
LARGURA, ALTURA = 800, 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Relógio de Fogo")

# Cores
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)
LARANJA = (255, 165, 0)
AMARELO = (255, 255, 0)

# Função para desenhar as chamas
def desenhar_chamas(horas, minutos, segundos):
    tela.fill(PRETO)
    centro_x, centro_y = LARGURA // 2, ALTURA // 2
    raio_max = 200

    # Calcula o tamanho das chamas baseado no tempo
    fator_horas = (12 - horas) / 12
    fator_minutos = (60 - minutos) / 60
    fator_segundos = (60 - segundos) / 60

    # Desenha as chamas
    for i in range(12):
        angulo = math.radians(i * 30)
        raio = raio_max * fator_horas
        x = centro_x + raio * math.cos(angulo)
        y = centro_y + raio * math.sin(angulo)
        pygame.draw.line(tela, VERMELHO, (centro_x, centro_y), (x, y), 3)

    for i in range(60):
        angulo = math.radians(i * 6)
        raio = raio_max * fator_minutos
        x = centro_x + raio * math.cos(angulo)
        y = centro_y + raio * math.sin(angulo)
        pygame.draw.line(tela, LARANJA, (centro_x, centro_y), (x, y), 2)

    for i in range(60):
        angulo = math.radians(i * 6)
        raio = raio_max * fator_segundos
        x = centro_x + raio * math.cos(angulo)
        y = centro_y + raio * math.sin(angulo)
        pygame.draw.line(tela, AMARELO, (centro_x, centro_y), (x, y), 1)

# Loop principal
rodando = True
while rodando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

    # Obtém o horário atual
    agora = time.localtime()
    horas = agora.tm_hour % 12
    minutos = agora.tm_min
    segundos = agora.tm_sec

    # Desenha o relógio de fogo
    desenhar_chamas(horas, minutos, segundos)

    # Atualiza a tela
    pygame.display.flip()
    pygame.time.delay(1000)

# Finaliza o pygame
pygame.quit()