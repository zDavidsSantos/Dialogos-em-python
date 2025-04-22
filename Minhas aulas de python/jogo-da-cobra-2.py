import pygame
import random
def update_score(new_score):
    global score
    score = new_score
# Inicialização do pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jogo da Cobra")

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PINK = (255, 192, 203)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
CYAN = (0, 255, 255)
colors = [RED, GREEN, BLUE, YELLOW, PINK, PURPLE, ORANGE, CYAN]


# Configurações da cobra
snake_pos = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
snake_direction = 'RIGHT'
change_to = snake_direction
speed = 15

# Configurações da comida
food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
food_spawn = True

# Pontuação
score = 0
font = pygame.font.SysFont('arial', 35)
def show_score(choice, color, font, size):
    score_surface = font.render('Score : ' + str(score), True, color)
    score_rect = score_surface.get_rect()
    screen.blit(score_surface, score_rect)
    score_rect.midtop = (WIDTH / 10, HEIGHT / 15)
    screen.blit(score_surface, score_rect)



# Função para mudar a cor da cobra
def get_random_color():
    return random.choice([RED, GREEN, BLUE, YELLOW, PINK, PURPLE, ORANGE, CYAN, colors[random.randint(0, len(colors)-1)]])

snake_color = GREEN

# Loop principal
clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not snake_direction == 'DOWN':
                change_to = 'UP'
            elif event.key == pygame.K_DOWN and not snake_direction == 'UP':
                change_to = 'DOWN'
            elif event.key == pygame.K_LEFT and not snake_direction == 'RIGHT':
                change_to = 'LEFT'
            elif event.key == pygame.K_RIGHT and not snake_direction == 'LEFT':
                change_to = 'RIGHT'

    # Mudança de direção
    snake_direction = change_to

    # Movimento da cobra
    if snake_direction == 'UP':
        snake_pos[1] -= 10
    if snake_direction == 'DOWN':
        snake_pos[1] += 10
    if snake_direction == 'LEFT':
        snake_pos[0] -= 10
    if snake_direction == 'RIGHT':
        snake_pos[0] += 10

    # Crescimento da cobra
    snake_body.insert(0, list(snake_pos))
    if snake_pos == food_pos:
        score += 1
        food_spawn = False
        snake_color = get_random_color()  # Muda a cor da cobra
    else:
        snake_body.pop()

    if not food_spawn:
        food_pos = [random.randrange(1, (WIDTH//10)) * 10, random.randrange(1, (HEIGHT//10)) * 10]
    food_spawn = True

    # Fim de jogo
    if (snake_pos[0] < 0 or snake_pos[0] > (WIDTH-10) or
            snake_pos[1] < 0 or snake_pos[1] > (HEIGHT-10)):
        running = False

    for block in snake_body[1:]:
        if snake_pos == block:
            running = False

    # Atualização da tela
    screen.fill(BLACK)
    for pos in snake_body:
        pygame.draw.rect(screen, snake_color, pygame.Rect(pos[0], pos[1], 10, 10))
    pygame.draw.rect(screen, WHITE, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()