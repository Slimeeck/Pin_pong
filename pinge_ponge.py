import pygame
import sys

pygame.init()

# Налаштування екрану
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пінг-Понг")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Кольори
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_SIZE = 15

# Налаштування ракеток та м'ячика
paddle_a = pygame.Rect(0, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
paddle_b = pygame.Rect(WIDTH - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)

# Швидкість
ball_speed_x = 3
ball_speed_y = 3
paddle_speed = 5

clock = pygame.time.Clock()

# Режим гри
game_mode = "bot"  # Можливі змінні: menu, player, bot

score_a = 0
score_b = 0

font = pygame.font.Font(None, 36)


def reset_ball():
    global ball_speed_x
    ball.x = WIDTH // 2 - BALL_SIZE // 2
    ball.y = HEIGHT // 2 - BALL_SIZE // 2
    ball_speed_x = -ball_speed_x

def draw_menu():
    menu_font = pygame.font.Font(None, 48)
    start_text = menu_font.render("Старт", True, WHITE)
    start_button = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    pygame.draw.rect(screen, WHITE, start_button.inflate(20, 20), 2)
    screen.blit(start_text, start_button)

def check_start_button_click(event):
    start_button = pygame.Rect(WIDTH // 2 - 50, HEIGHT // 2 - 25, 100, 50)
    if event.type == pygame.MOUSEBUTTONDOWN and start_button.collidepoint(event.pos):
        return True
    return False

game_mode = "menu"

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if game_mode == "menu" and check_start_button_click(event):
            game_mode = "bot"

    screen.fill(BLACK)

    if game_mode == "menu":
        draw_menu()

# Рух бота
def bot_move():
    if ball.centery > paddle_b.centery and paddle_b.bottom < HEIGHT:
        paddle_b.y += paddle_speed
    elif ball.centery < paddle_b.centery and paddle_b.top > 0:
        paddle_b.y -= paddle_speed


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

# Заповнює задній екран кольором чорний
    screen.fill(BLACK)

    if game_mode == "menu":
        pass

# Керування з гравцями
    elif game_mode == "player":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle_a.top > 0:
            paddle_a.y -= paddle_speed
        if keys[pygame.K_s] and paddle_a.bottom < HEIGHT:
            paddle_a.y += paddle_speed
        if keys[pygame.K_UP] and paddle_b.top > 0:
            paddle_b.y -= paddle_speed
        if keys[pygame.K_DOWN] and paddle_b.bottom < HEIGHT:
            paddle_b.y += paddle_speed

# Керування з ботом
    elif game_mode == "bot":
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle_a.top > 0:
            paddle_a.y -= paddle_speed
        if keys[pygame.K_s] and paddle_a.bottom < HEIGHT:
            paddle_a.y += paddle_speed
        bot_move()

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.top <= 0 or ball.bottom >= HEIGHT:
        ball_speed_y = -ball_speed_y
    if ball.colliderect(paddle_a) or ball.colliderect(paddle_b):
        ball_speed_x = -ball_speed_x
    if ball.left <= 0:
        score_b += 1
        reset_ball()
    elif ball.right >= WIDTH:
        score_a += 1
        reset_ball()

# Промалювання
    pygame.draw.rect(screen, WHITE, paddle_a)
    pygame.draw.rect(screen, WHITE, paddle_b)
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.aaline(screen, WHITE, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))

    score_text = font.render(f"{score_a} - {score_b}", True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    pygame.display.flip()
    clock.tick(90)