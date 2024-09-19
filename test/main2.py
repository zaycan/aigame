import pygame
import random
import math

# Инициализация Pygame
pygame.init()

# Размеры экрана
screen_size = 720
screen = pygame.display.set_mode((screen_size, screen_size))

# Цвета
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

# Игрок
player_size = 50
player_pos = [screen_size // 2, screen_size // 2]
player_speed = 5

# Мишень
target_size = 50
target_pos = [random.randint(0, screen_size - target_size), random.randint(0, screen_size - target_size)]
target_speed = 3

# Препятствие
obstacle_size = 100
obstacle_pos = [random.randint(0, screen_size - obstacle_size), random.randint(0, screen_size - obstacle_size)]

# Пули игрока
player_bullets = []
bullet_speed = 7

# Пули мишени
target_bullets = []
target_bullet_speed = 5

# Очки
score = 0

# Шрифт
font = pygame.font.SysFont("monospace", 35)


# Функция для отрисовки игрока
def draw_player():
    pygame.draw.rect(screen, green, (player_pos[0], player_pos[1], player_size, player_size))


# Функция для отрисовки мишени
def draw_target():
    pygame.draw.rect(screen, red, (target_pos[0], target_pos[1], target_size, target_size))


# Функция для отрисовки препятствия
def draw_obstacle():
    pygame.draw.rect(screen, white, (obstacle_pos[0], obstacle_pos[1], obstacle_size, obstacle_size))


# Функция для отрисовки пуль игрока
def draw_player_bullets():
    for bullet in player_bullets:
        pygame.draw.rect(screen, white, (bullet[0], bullet[1], 10, 10))


# Функция для отрисовки пуль мишени
def draw_target_bullets():
    for bullet in target_bullets:
        pygame.draw.rect(screen, red, (bullet[0], bullet[1], 10, 10))


# Функция для обновления позиции мишени и стрельбы по игроку
def update_target():
    if target_pos[0] < player_pos[0]:
        target_pos[0] += target_speed
    else:
        target_pos[0] -= target_speed
    if target_pos[1] < player_pos[1]:
        target_pos[1] += target_speed
    else:
        target_pos[1] -= target_speed

    # Стрельба по игроку
    if random.random() < 0.02:  # Вероятность выстрела мишени в каждом кадре
        angle = math.atan2(player_pos[1] - target_pos[1], player_pos[0] - target_pos[0])
        target_bullets.append([target_pos[0] + target_size // 2, target_pos[1] + target_size // 2, angle])


# Основной игровой цикл
running = True
while running:
    screen.fill(black)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                angle = math.atan2(mouse_y - player_pos[1], mouse_x - player_pos[0])
                player_bullets.append([player_pos[0] + player_size // 2, player_pos[1] + player_size // 2, angle])

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_pos[1] > 10:
        player_pos[1] -= player_speed
    if keys[pygame.K_s] and player_pos[1] < screen_size - player_size - 10:
        player_pos[1] += player_speed
    if keys[pygame.K_a] and player_pos[0] > 10:
        player_pos[0] -= player_speed
    if keys[pygame.K_d] and player_pos[0] < screen_size - player_size - 10:
        player_pos[0] += player_speed

    for bullet in player_bullets:
        bullet[0] += bullet_speed * math.cos(bullet[2])
        bullet[1] += bullet_speed * math.sin(bullet[2])

        # Проверка попадания в мишень
        if bullet[0] > target_pos[0] and bullet[0] < target_pos[0] + target_size and bullet[1] > target_pos[1] and \
                bullet[1] < target_pos[1] + target_size:
            score += 1
            player_bullets.remove(bullet)
            target_pos = [random.randint(0, screen_size - target_size), random.randint(0, screen_size - target_size)]

        # Проверка выхода за границы экрана или попадания в препятствие
        if bullet[0] < 10 or bullet[0] > screen_size - 10 or bullet[1] < 10 or bullet[1] > screen_size - 10 or \
                (obstacle_pos[0] < bullet[0] < obstacle_pos[0] + obstacle_size and obstacle_pos[1] < bullet[1] <
                 obstacle_pos[1] + obstacle_size):
            player_bullets.remove(bullet)

    for bullet in target_bullets:
        bullet[0] += target_bullet_speed * math.cos(bullet[2])
        bullet[1] += target_bullet_speed * math.sin(bullet[2])

        # Проверка попадания в игрока
        if bullet[0] > player_pos[0] and bullet[0] < player_pos[0] + player_size and bullet[1] > player_pos[1] and \
                bullet[1] < player_pos[1] + player_size:
            running = False

        # Проверка выхода за границы экрана или попадания в препятствие
        if bullet[0] < 10 or bullet[0] > screen_size - 10 or bullet[1] < 10 or bullet[1] > screen_size - 10 or \
                (obstacle_pos[0] < bullet[0] < obstacle_pos[0] + obstacle_size and obstacle_pos[1] < bullet[1] <
                 obstacle_pos[1] + obstacle_size):
            target_bullets.remove(bullet)

    update_target()

    draw_player()
    draw_target()
    draw_obstacle()
    draw_player_bullets()
    draw_target_bullets()

    score_text = font.render("Score: {}".format(score), True, white)
    screen.blit(score_text, (10, 10))

    pygame.draw.rect(screen, blue, (0, 0, screen_size, 10))  # Верхняя граница
    pygame.draw.rect(screen, blue, (0, 0, 10, screen_size))  # Левая граница
    pygame.draw.rect(screen, blue, (0, screen_size - 10, screen_size, 10))  # Нижняя граница
    pygame.draw.rect(screen, blue, (screen_size - 10, 0, 10, screen_size))  # Правая граница

    pygame.display.flip()
    pygame.time.Clock().tick(30)
# test asdasd asdfsdf
# Конец игры
screen.fill(black)
end_text = font.render("Game Over! Score: {}".format(score), True, white)
screen.blit(end_text, (screen_size // 2 - end_text.get_width() // 2, screen_size // 2 - end_text.get_height() // 2))
restart_text = font.render("Press R to Restart", True, white)
screen.blit(restart_text, (screen_size // 2 - restart_text.get_width() // 2, screen_size // 2 + end_text.get_height()))

pygame.display.flip()

# Ожидание нажатия кнопки рестарт
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                waiting = False
                running = True
                player_pos = [screen_size // 2, screen_size // 2]
                target_pos = [random.randint(0, screen_size - target_size),
                              random.randint(0, screen_size - target_size)]
                obstacle_pos = [random.randint(0, screen_size - obstacle_size),
                                random.randint(0, screen_size - obstacle_size)]
                player_bullets = []
                target_bullets = []
                score = 0

pygame.quit()
