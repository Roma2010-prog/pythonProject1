import pygame

pygame.init()

# Screen
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption("Mini Adventure")

# Colors
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (100, 200, 100)
YELLOW = (255, 215, 0)
PURPLE = (200, 0, 200)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

font = pygame.font.SysFont(None, 40)
small_font = pygame.font.SysFont(None, 30)

clock = pygame.time.Clock()

# Clouds
clouds = [[100, 80], [300, 50], [500, 100], [700, 70]]


# ---------------- ЗАГРУЗКА КАРТИНОК ----------------
def load_images():
    """Загружает картинки или создаёт их, если файлы не найдены"""
    images = {}

    # Игрок (пытаемся загрузить из файла)
    try:
        images['player'] = pygame.image.load('player.png')
        images['player'] = pygame.transform.scale(images['player'], (30, 30))
    except:
        # Создаём простую картинку игрока
        surf = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.circle(surf, BLUE, (15, 15), 12)
        pygame.draw.circle(surf, (255, 255, 255), (10, 10), 3)  # глаз
        pygame.draw.circle(surf, (255, 255, 255), (20, 10), 3)  # глаз
        images['player'] = surf

    # Монстр
    try:
        images['monster'] = pygame.image.load('monster.png')
        images['monster'] = pygame.transform.scale(images['monster'], (30, 30))
    except:
        surf = pygame.Surface((30, 30), pygame.SRCALPHA)
        pygame.draw.rect(surf, RED, (0, 0, 30, 30))
        pygame.draw.circle(surf, WHITE, (8, 8), 4)  # глаз
        pygame.draw.circle(surf, WHITE, (22, 8), 4)  # глаз
        pygame.draw.circle(surf, BLACK, (8, 8), 2)  # зрачок
        pygame.draw.circle(surf, BLACK, (22, 8), 2)  # зрачок
        pygame.draw.arc(surf, BLACK, (8, 15, 14, 10), 0, 3.14, 2)  # рот
        images['monster'] = surf

    # Монетка
    try:
        images['coin'] = pygame.image.load('coin.png')
        images['coin'] = pygame.transform.scale(images['coin'], (15, 15))
    except:
        surf = pygame.Surface((15, 15), pygame.SRCALPHA)
        pygame.draw.circle(surf, YELLOW, (7, 7), 7)
        pygame.draw.circle(surf, (255, 255, 100), (7, 7), 5)
        pygame.draw.line(surf, (200, 150, 0), (4, 7), (10, 7), 2)  # блик
        images['coin'] = surf

    # Портал
    try:
        images['door'] = pygame.image.load('portal.png')
        images['door'] = pygame.transform.scale(images['door'], (30, 40))
    except:
        surf = pygame.Surface((30, 40), pygame.SRCALPHA)
        pygame.draw.ellipse(surf, PURPLE, (0, 0, 30, 40))
        pygame.draw.ellipse(surf, (255, 0, 255), (5, 5, 20, 30))
        images['door'] = surf

    # Платформа
    try:
        images['platform'] = pygame.image.load('platform.png')
    except:
        surf = pygame.Surface((100, 10))
        surf.fill((80, 150, 80))
        pygame.draw.rect(surf, (50, 120, 50), (0, 0, 100, 3))  # деталь
        images['platform'] = surf

    # Фон (опционально)
    try:
        images['background'] = pygame.image.load('background.jpg')
        images['background'] = pygame.transform.scale(images['background'], (800, 400))
    except:
        images['background'] = None

    return images


# Загружаем картинки
images = load_images()


# ---------------- BUTTON ----------------
def draw_button(text, x, y, w, h, color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    pygame.draw.rect(screen, color, (x, y, w, h))
    txt = small_font.render(text, True, BLACK)
    screen.blit(txt, (x + 10, y + 10))

    if x < mouse[0] < x + w and y < mouse[1] < y + h:
        if click[0] == 1:
            pygame.time.delay(150)
            return True
    return False


# ---------------- BACKGROUND ----------------
def draw_background():
    # Рисуем фон (если есть картинка фона)
    if images['background']:
        screen.blit(images['background'], (0, 0))
    else:
        # Градиент неба
        for i in range(400):
            color = (135 - i // 5, 206 - i // 4, 235 - i // 6)
            pygame.draw.line(screen, color, (0, i), (800, i))

        # Холмы
        pygame.draw.polygon(screen, (90, 120, 90), [(0, 300), (200, 180), (400, 300)])
        pygame.draw.polygon(screen, (70, 100, 70), [(300, 300), (500, 150), (700, 300)])

    # Облака
    for cloud in clouds:
        cloud[0] += 0.3
        if cloud[0] > 850:
            cloud[0] = -100

        pygame.draw.circle(screen, WHITE, (int(cloud[0]), cloud[1]), 20)
        pygame.draw.circle(screen, WHITE, (int(cloud[0]) + 25, cloud[1] + 5), 25)
        pygame.draw.circle(screen, WHITE, (int(cloud[0]) + 50, cloud[1]), 20)

    # Солнце
    pygame.draw.circle(screen, (255, 255, 180), (700, 80), 50)
    pygame.draw.circle(screen, YELLOW, (700, 80), 40)


# ---------------- LEVEL ----------------
def load_level(level):
    global monsters

    base = [pygame.Rect(0, 370, 800, 30)]

    levels = {
        1: {
            "platforms": [(150, 280, 120, 10), (350, 230, 120, 10), (550, 120, 120, 10)],
            "coins": [(170, 250), (370, 200), (570, 90)],
            "monsters": [(600, 340, -1)]
        },
        2: {
            "platforms": [(150, 270, 120, 10), (350, 150, 120, 10), (550, 170, 120, 10)],
            "coins": [(170, 240), (370, 120), (570, 140), (700, 340)],
            "monsters": [(700, 340, -1)]
        },
        3: {
            "platforms": [(120, 290, 100, 10), (260, 250, 100, 10), (420, 120, 100, 10), (600, 170, 100, 10)],
            "coins": [(140, 260), (280, 220), (440, 90), (620, 140)],
            "monsters": [(500, 340, -1), (650, 340, -1)]
        },
        4: {
            "platforms": [(100, 270, 100, 10), (250, 220, 100, 10), (400, 170, 100, 10), (550, 120, 100, 10)],
            "coins": [(120, 240), (270, 190), (420, 140), (570, 90)],
            "monsters": [(300, 340, -1), (600, 340, -1)]
        },
        5: {
            "platforms": [(100, 290, 120, 10), (300, 250, 120, 10), (500, 210, 120, 10), (650, 150, 120, 10)],
            "coins": [(120, 260), (320, 220), (520, 180), (670, 130), (750, 340)],
            "monsters": [(200, 340, -1), (500, 340, -1)]
        },
        6: {
            "platforms": [(150, 270, 100, 10), (300, 220, 100, 10), (450, 170, 100, 10), (600, 120, 100, 10)],
            "coins": [(170, 240), (320, 190), (470, 140), (620, 90)],
            "monsters": [(250, 340, -1), (450, 340, -1), (650, 340, -1)]
        }
    }

    if level not in levels:
        return None, None, None

    data = levels[level]

    platforms = base + [pygame.Rect(*p) for p in data["platforms"]]
    coins = [pygame.Rect(x, y, 15, 15) for x, y in data["coins"]]
    monsters = [{"rect": pygame.Rect(x, y, 30, 30), "dir": d} for x, y, d in data["monsters"]]

    door = pygame.Rect(750, 330, 30, 40)
    return platforms, coins, door


# ---------------- RESET ----------------
def reset_game():
    global player, vy, lives, score, level, platforms, coins, door, stars

    player = pygame.Rect(50, 300, 30, 30)
    vy = 0
    lives = 3
    score = 0
    stars = 0
    level = 1

    platforms, coins, door = load_level(level)


# ---------------- SCREENS ----------------
def start_screen():
    while True:
        draw_background()

        title = font.render("Mini Adventure", True, BLACK)
        screen.blit(title, (260, 120))

        if draw_button("Play", 300, 200, 120, 50, GREEN):
            return

        if draw_button("Quit", 450, 200, 120, 50, RED):
            pygame.quit()
            exit()

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()


def game_over_screen():
    while True:
        draw_background()

        txt = font.render("GAME OVER", True, RED)
        screen.blit(txt, (300, 120))

        if draw_button("Restart", 300, 200, 140, 50, GREEN):
            return

        if draw_button("Quit", 470, 200, 120, 50, RED):
            pygame.quit()
            exit()

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()


def win_screen():
    while True:
        draw_background()

        txt = font.render("YOU WIN!", True, GREEN)
        screen.blit(txt, (320, 120))

        if draw_button("Play Again", 300, 200, 150, 50, GREEN):
            return

        if draw_button("Quit", 470, 200, 120, 50, RED):
            pygame.quit()
            exit()

        pygame.display.update()

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                exit()


# ---------------- GAME FUNCTIONS ----------------
def move_player(keys):
    global vy, on_ground

    if keys[pygame.K_LEFT]:
        player.x -= 3
    if keys[pygame.K_RIGHT]:
        player.x += 3

    if keys[pygame.K_UP] and on_ground:
        vy = -12
        on_ground = False

    vy += 0.5
    player.y += vy


def handle_collisions():
    global vy, on_ground
    on_ground = False

    for p in platforms:
        if player.colliderect(p) and vy > 0:
            player.bottom = p.top
            vy = 0
            on_ground = True


def update_monsters():
    global lives, vy, stars

    for m in monsters[:]:
        m["rect"].x += 2 * m["dir"]

        if m["rect"].left <= 0 or m["rect"].right >= 800:
            m["dir"] *= -1

        m["rect"].y = 340

        if player.colliderect(m["rect"]):
            if vy > 0:
                monsters.remove(m)
                vy = -6
                stars += 1
            else:
                lose_life()


def collect_coins():
    global score
    for c in coins[:]:
        if player.colliderect(c):
            coins.remove(c)
            score += 1


def lose_life():
    global lives, vy
    lives -= 1
    player.x, player.y = 50, 300
    vy = 0


def next_level():
    global level, platforms, coins, door, vy

    level += 1
    result = load_level(level)

    if result[0] is None:
        win_screen()
        reset_game()
        return

    platforms, coins, door = result
    player.x, player.y = 50, 300
    vy = 0


# ---------------- DRAW С КАРТИНКАМИ ----------------
def draw():
    draw_background()

    # Земля
    pygame.draw.rect(screen, (50, 180, 50), (0, 360, 800, 40))

    # Платформы с картинками
    for p in platforms:
        # Масштабируем картинку под размер платформы
        plat_img = pygame.transform.scale(images['platform'], (p.width, p.height))
        screen.blit(plat_img, (p.x, p.y))

    # Монетки с картинками
    for c in coins:
        screen.blit(images['coin'], (c.x, c.y))

    # Монстры с картинками
    for m in monsters:
        screen.blit(images['monster'], (m["rect"].x, m["rect"].y))

    # Портал с картинкой
    screen.blit(images['door'], (door.x, door.y))

    # Игрок с картинкой
    screen.blit(images['player'], (player.x, player.y))

    # UI текст
    screen.blit(small_font.render(f"Lives: {lives}", True, BLACK), (10, 10))
    screen.blit(small_font.render(f"Coins: {score}", True, BLACK), (10, 35))
    screen.blit(small_font.render(f"Level: {level}", True, BLACK), (10, 60))
    screen.blit(small_font.render(f"Stars: {stars}", True, BLACK), (10, 85))

    pygame.display.update()


# ---------------- MAIN ----------------
start_screen()
reset_game()

run = True
while run:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()

    move_player(keys)
    handle_collisions()
    collect_coins()
    update_monsters()

    if player.bottom > 370:
        player.bottom = 370
        vy = 0
        on_ground = True

    if player.colliderect(door) and not coins:
        next_level()

    if lives <= 0:
        game_over_screen()
        reset_game()

    draw()

pygame.quit()