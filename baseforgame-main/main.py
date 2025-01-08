import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пепельный рассвет")

# Загрузка ресурсов
background = pygame.image.load("assets/background.jpg")
player_img = pygame.image.load("assets/player.png")
enemy_img = pygame.image.load("assets/enemy.png")
bullet_img = pygame.image.load("assets/bullet.png")
health_img = pygame.image.load("assets/health.png")
ammo_img = pygame.image.load("assets/ammo.png")

# Звуки
shot_sound = pygame.mixer.Sound("assets/shot.wav")
pickup_sound = pygame.mixer.Sound("assets/pickup.wav")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")

# Игрок
player_size = 50
player_pos = [WIDTH // 2, HEIGHT // 2]
player_speed = 5
player_health = 100
player_ammo = 10

# Враги
enemy_list = []
enemy_spawn_time = 2000  # Интервал появления врагов
last_enemy_spawn = pygame.time.get_ticks()

# Пули
bullets = []

# Ресурсы
resources = []
resource_spawn_time = 5000
last_resource_spawn = pygame.time.get_ticks()

# Функции
def spawn_enemy():
    x_pos = random.randint(0, WIDTH - 50)
    y_pos = random.choice([-50, HEIGHT + 50])  # Враги появляются сверху или снизу
    enemy_list.append([x_pos, y_pos])

def spawn_resource():
    x_pos = random.randint(0, WIDTH - 30)
    y_pos = random.randint(0, HEIGHT - 30)
    resource_type = random.choice(["health", "ammo"])
    resources.append([x_pos, y_pos, resource_type])

def draw_game():
    screen.blit(background, (0, 0))
    screen.blit(player_img, (player_pos[0], player_pos[1]))
    for enemy in enemy_list:
        screen.blit(enemy_img, (enemy[0], enemy[1]))
    for bullet in bullets:
        screen.blit(bullet_img, (bullet[0], bullet[1]))
    for resource in resources:
        if resource[2] == "health":
            screen.blit(health_img, (resource[0], resource[1]))
        elif resource[2] == "ammo":
            screen.blit(ammo_img, (resource[0], resource[1]))

def move_enemies():
    for enemy in enemy_list:
        if enemy[1] < HEIGHT // 2:
            enemy[1] += 2  # Враги движутся вниз
        else:
            enemy[1] -= 2  # Враги движутся вверх

def shoot_bullet(mouse_pos):
    if player_ammo > 0:
        bullet_x = player_pos[0] + 25
        bullet_y = player_pos[1] + 25
        bullets.append([bullet_x, bullet_y, mouse_pos])
        pygame.mixer.Sound.play(shot_sound)

def move_bullets():
    for bullet in bullets[:]:
        dx = bullet[2][0] - bullet[0]
        dy = bullet[2][1] - bullet[1]
        dist = (dx**2 + dy**2)**0.5
        bullet[0] += (dx / dist) * 10
        bullet[1] += (dy / dist) * 10
        if bullet[0] < 0 or bullet[0] > WIDTH or bullet[1] < 0 or bullet[1] > HEIGHT:
            bullets.remove(bullet)

# Игровой цикл
running = True
clock = pygame.time.Clock()

while running:
    screen.fill((0, 0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            shoot_bullet(pygame.mouse.get_pos())

    # Управление игроком
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w] and player_pos[1] > 0:
        player_pos[1] -= player_speed
    if keys[pygame.K_s] and player_pos[1] < HEIGHT - player_size:
        player_pos[1] += player_speed
    if keys[pygame.K_a] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_d] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed

    # Спавн врагов
    if pygame.time.get_ticks() - last_enemy_spawn > enemy_spawn_time:
        spawn_enemy()
        last_enemy_spawn = pygame.time.get_ticks()

    # Спавн ресурсов
    if pygame.time.get_ticks() - last_resource_spawn > resource_spawn_time:
        spawn_resource()
        last_resource_spawn = pygame.time.get_ticks()

    # Движение врагов и пуль
    move_enemies()
    move_bullets()

    # Отрисовка игры
    draw_game()
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
