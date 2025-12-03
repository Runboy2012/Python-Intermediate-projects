# freelance_survival_final.py
import pygame
import random
import sys

pygame.init()
WIDTH, HEIGHT = 1000, 650
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Фриланс-выживалка — 30 дней до свободы")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
GREEN = (0, 200, 0)
RED = (200, 0, 0)
BLUE = (0, 120, 255)
YELLOW = (255, 220, 0)
BG = (25, 25, 50)

font_big = pygame.font.SysFont("arial", 40, bold=True)
font_med = pygame.font.SysFont("arial", 28)
font_small = pygame.font.SysFont("arial", 22)

class Player:
    def __init__(self):
        self.day = 1
        self.money = 8000
        self.energy = 100
        self.skills = {"prompt": 10, "python": 10, "video": 5, "copy": 10, "design": 5}
        self.current_order = None

player = Player()

ORDERS_POOL = [
    ("5 промптов MidJourney", 1500, 2, "prompt", 5),
    ("Парсер цен → Excel", 5000, 8, "python", 10),
    ("10 Shorts", 12000, 24, "video", 15),
    ("Текст 3000 зн.", 3500, 4, "copy", 8),
    ("Баннер Canva", 2500, 3, "design", 7),
    ("Telegram-бот", 15000, 20, "python", 12),
]

def new_orders():
    return random.sample(ORDERS_POOL, k=4)

orders = new_orders()
state = "main"
selected = None
work = 0
need = 0

def txt(text, font, col, x, y, center=False):
    s = font.render(text, True, col)
    r = s.get_rect(center=(x, y)) if center else s.get_rect(topleft=(x, y))
    screen.blit(s, r)

running = True
while running:
    screen.fill(BG)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            x, y = e.pos

            if state == "main":
                if 700 <= x <= 960 and 480 <= y <= 550:      # Биржа
                    state = "orders"
                    orders = new_orders()
                if player.current_order is None and 700 <= x <= 960 and 570 <= y <= 620:  # Пропустить
                    player.day += 1
                    player.energy = min(100, player.energy + 35)

            elif state == "orders":
                for i in range(4):
                    if 60 <= x <= 940 and 120 + i*110 <= y <= 200 + i*110:
                        selected = orders[i]
                        state = "detail"

            elif state == "detail" and selected:
                if 350 <= x <= 650 and 520 <= y <= 590:       # Взять заказ
                    player.current_order = selected
                    need = selected[2] * 10
                    work = 0
                    state = "work"

            elif state == "work":
                work += 12
                player.energy = max(0, player.energy - 1)

    # конец игры
    if player.day > 30:
        state = "end"

    # отрисовка
    txt(f"День {player.day}/30", font_big, YELLOW, WIDTH//2, 30, True)
    txt(f"💰 {player.money} тг", font_med, GREEN, 40, 30)
    txt(f"⚡ {player.energy}/100", font_med, WHITE, 40, 80)

    if state in ("main", "work"):
        if player.current_order:
            o = player.current_order
            txt("Работаю:", font_med, YELLOW, 40, 180)
            txt(o[0], font_med, WHITE, 60, 230)
            prog = min(100, work * 100 // max(1, need))
            txt(f"Прогресс: {prog}%", font_small, WHITE, 60, 280)
            txt("КЛИКАЙ!", font_big, RED, WIDTH//2, 420, True)

            if work >= need:
                if random.randint(1, 100) <= o[4]:
                    txt("Кинули :(", font_big, RED, WIDTH//2, 500, True)
                else:
                    player.money += o[1]
                    player.skills[o[3]] += random.randint(15, 30)
                    txt(f"+{o[1]} тг!", font_big, GREEN, WIDTH//2, 500, True)
                pygame.display.flip()
                pygame.time.wait(1500)
                player.current_order = None
                state = "main"
        else:
            txt("Квартира грузчика", font_big, WHITE, WIDTH//2, 220, True)
            pygame.draw.rect(screen, GRAY, (700, 480, 260, 70))
            txt("Биржа заказов", font_big, BLACK, 830, 510, True)
            pygame.draw.rect(screen, (70,70,90), (700, 570, 260, 50))
            txt("Пропустить день", font_med, WHITE, 830, 590, True)

    elif state == "orders":
        txt("Доступные заказы", font_big, YELLOW, WIDTH//2, 60, True)
        for i, (name, price, hrs, sk, _) in enumerate(orders):
            col = GREEN if player.skills[sk] > 30 else WHITE
            y0 = 120 + i*110
            pygame.draw.rect(screen, GRAY, (60, y0, 880, 90), border_radius=15)
            txt(name, font_med, col, 90, y0+15)
            txt(f"{price} тг • {hrs} ч • {sk}", font_small, WHITE, 90, y0+55)

    elif state == "detail" and selected:
        n, p, h, s, _ = selected
        txt("Детали заказа", font_big, YELLOW, WIDTH//2, 80, True)
        txt(n, font_big, WHITE, WIDTH//2, 180, True)
        txt(f"{p} тг", font_med, GREEN, WIDTH//2, 260, True)
        txt(f"{h} часов", font_med, WHITE, WIDTH//2, 320, True)
        txt(f"Навык {s}: {player.skills[s]}", font_med, WHITE, WIDTH//2, 380, True)
        pygame.draw.rect(screen, BLUE, (350, 520, 300, 70))
        txt("ВЗЯТЬ ЗАКАЗ", font_big, WHITE, WIDTH//2, 555, True)

    elif state == "end":
        screen.fill((0,0,0))
        if player.money >= 50000:
            txt("ПОБЕДА!", font_big, GREEN, WIDTH//2, 200, True)
            txt("Живёшь на фрилансе!", font_med, WHITE, WIDTH//2, 300, True)
        else:
            txt("Поражение", font_big, RED, WIDTH//2, 200, True)
            txt(f"Осталось {player.money} тг", font_med, WHITE, WIDTH//2, 300, True)
            txt("Но теперь есть портфолио ;)", font_small, YELLOW, WIDTH//2, 400, True)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()