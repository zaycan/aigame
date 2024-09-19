import pygame
import sys
import random
import math

# Инициализация Pygame
pygame.init()

# Настройки экрана
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("3D Shooter")

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Прямоугольное препятствие
obstacle_rect = pygame.Rect(350, 250, 100, 100)


# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.center = (600, 500)
        self.speed = 5
        self.angle = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:  # Влево
            self.rect.x -= self.speed
        if keys[pygame.K_d]:  # Вправо
            self.rect.x += self.speed
        if keys[pygame.K_w]:  # Вверх
            self.rect.y -= self.speed
        if keys[pygame.K_s]:  # Вниз
            self.rect.y += self.speed

        # Проверка столкновения с препятствием
        if self.rect.colliderect(obstacle_rect):
            if keys[pygame.K_a]:  # Влево
                self.rect.x += self.speed
            if keys[pygame.K_d]:  # Вправо
                self.rect.x -= self.speed
            if keys[pygame.K_w]:  # Вверх
                self.rect.y += self.speed
            if keys[pygame.K_s]:  # Вниз
                self.rect.y -= self.speed

        # Получение позиции мыши
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Вычисление угла поворота к мыши
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
        self.angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)

    def draw(self, surface):
        points = [
            (self.rect.centerx + math.cos(math.radians(self.angle)) * 25,
             self.rect.centery - math.sin(math.radians(self.angle)) * 25),
            (self.rect.centerx + math.cos(math.radians(self.angle + 120)) * 25,
             self.rect.centery - math.sin(math.radians(self.angle + 120)) * 25),
            (self.rect.centerx + math.cos(math.radians(self.angle - 120)) * 25,
             self.rect.centery - math.sin(math.radians(self.angle - 120)) * 25)
        ]
        pygame.draw.polygon(surface, WHITE, points)

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.centery, self.angle)
        all_sprites.add(bullet)
        bullets.add(bullet)


# Класс пули игрока
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, WHITE, (5, 5), 5)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 10
        self.angle = angle

    def update(self):
        self.rect.x += math.cos(math.radians(self.angle)) * self.speed
        self.rect.y -= math.sin(math.radians(self.angle)) * self.speed
        if (self.rect.bottom < 0 or self.rect.top > 600 or
                self.rect.right < 0 or self.rect.left > 800):
            self.kill()

        # Проверка столкновения с препятствием
        if self.rect.colliderect(obstacle_rect):
            self.kill()


# Класс пули мишени
class TargetBullet(pygame.sprite.Sprite):
    def __init__(self, x, y, angle):
        super().__init__()
        self.image = pygame.Surface((10, 10), pygame.SRCALPHA)
        pygame.draw.circle(self.image, RED, (5, 5), 5)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = 10
        self.angle = angle

    def update(self):
        self.rect.x += math.cos(math.radians(self.angle)) * self.speed
        self.rect.y -= math.sin(math.radians(self.angle)) * self.speed
        if (self.rect.bottom < 0 or self.rect.top > 600 or
                self.rect.right < 0 or self.rect.left > 800):
            self.kill()

        # Проверка столкновения с препятствием
        if self.rect.colliderect(obstacle_rect):
            self.kill()

# Класс мишени
class Target(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 50), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.reset_position()
        self.angle = random.randint(0, 360)

    def update(self):
        if random.randint(0, 100) < 15:  # Вероятность выстрела
            target_angle = random.randint(0, 360)
            bullet = TargetBullet(self.rect.centerx, self.rect.centery, target_angle)
            all_sprites.add(bullet)
            target_bullets.add(bullet)

        # Проверка столкновения с препятствием
        if self.rect.colliderect(obstacle_rect):
            self.rect.x = random.randint(0, 750)
            self.rect.y = random.randint(0, 550)

    def draw(self, surface):
        points = [
            (self.rect.centerx + math.cos(math.radians(self.angle)) * 25,
             self.rect.centery - math.sin(math.radians(self.angle)) * 25),
            (self.rect.centerx + math.cos(math.radians(self.angle + 120)) * 25,
             self.rect.centery - math.sin(math.radians(self.angle + 120)) * 25),
            (self.rect.centerx + math.cos(math.radians(self.angle - 120)) * 25,
             self.rect.centery - math.sin(math.radians(self.angle - 120)) * 25)
        ]
        pygame.draw.polygon(surface, RED, points)

    def reset_position(self):
        while True:
            x = random.randint(0, 750)
            y = random.randint(0, 550)
            if not obstacle_rect.collidepoint(x, y):
                self.rect.x = x
                self.rect.y = y
                break


# Группы спрайтов
all_sprites = pygame.sprite.Group()
bullets = pygame.sprite.Group()
target_bullets = pygame.sprite.Group()
targets = pygame.sprite.Group()


def start_game():
    global all_sprites, bullets, target_bullets, targets, player, target, score

    # Группы спрайтов
    all_sprites.empty()
    bullets.empty()
    target_bullets.empty()
    targets.empty()

    # Создание игрока и мишени
    player = Player()
    all_sprites.add(player)

    target = Target()
    all_sprites.add(target)
    targets.add(target)

    # Счет
    score = 0


start_game()

# Шрифт для текста и кнопки
font = pygame.font.Font(None, 36)


def draw_button(surface, text, x, y):
    button_rect = pygame.Rect(x - 50, y - 20, 100, 40)
    pygame.draw.rect(surface, GREEN, button_rect)
    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x, y))
    surface.blit(text_surface, text_rect)
    return button_rect


# Основной цикл игры
running = True
game_over = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_over:
                if restart_button.collidepoint(event.pos):
                    game_over = False
                    start_game()
            else:
                if event.button == 1:  # Левая кнопка мыши
                    player.shoot()

    if not game_over:
        # Обновление
        all_sprites.update()

        # Проверка попадания пули в мишень
        hits = pygame.sprite.groupcollide(bullets, targets, True, False)
        for hit in hits:
            score += 1
            target.reset_position()

        # Проверка попадания пули мишени в игрока
        if pygame.sprite.spritecollideany(player, target_bullets):
            game_over = True

        # Рендеринг
        screen.fill(BLACK)
        all_sprites.draw(screen)
        player.draw(screen)
        target.draw(screen)

        # Отображение препятствия
        pygame.draw.rect(screen, BLUE, obstacle_rect)

        # Отображение счета
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

    else:
        # Отображение финального счета и кнопки перезапуска
        screen.fill(BLACK)
        final_score_text = font.render(f"Final Score: {score}", True, WHITE)
        screen.blit(final_score_text, (300, 250))
        restart_button = draw_button(screen, "Restart", 400, 300)

    pygame.display.flip()

    # Ограничение FPS
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()