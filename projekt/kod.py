import pygame
import time
import random
import sqlite3

# Inicializace Pygame
pygame.init()

# Nastavení okna
window_x = 450
window_y = 400
game_window = pygame.display.set_mode((window_x, window_y))
pygame.display.set_caption('Snake Game')

# Definice barev
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
dark_gray = (50, 50, 50)

# Nastavení FPS a rychlosti hada
fps = pygame.time.Clock()
snake_speed = 10

# Připojení k databázi SQLite3
conn = sqlite3.connect('snake_game_scores.db')
cursor = conn.cursor()

# Vytvoření tabulky pro skóre, pokud neexistuje
cursor.execute('''
CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    score INTEGER NOT NULL
)
''')
conn.commit()

# Funkce pro uložení skóre do databáze
def save_score_to_db(score):
    """Uloží skóre do databáze."""
    cursor.execute('INSERT INTO scores (score) VALUES (?)', (score,))
    conn.commit()

# Funkce pro načtení nejlepších skóre
def get_top_scores(limit=3):
    """Načte nejlepší skóre z databáze."""
    cursor.execute('SELECT score FROM scores ORDER BY score DESC LIMIT ?', (limit,))
    return [row[0] for row in cursor.fetchall()]

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    game_window.blit(text_surface, text_rect)

def draw_background():
    for x in range(0, window_x, 20):
        pygame.draw.line(game_window, dark_gray, (x, 0), (x, window_y), 1)
    for y in range(0, window_y, 20):
        pygame.draw.line(game_window, dark_gray, (0, y), (window_x, y), 1)

def draw_frame():
    pygame.draw.rect(game_window, dark_gray, pygame.Rect(0, 0, window_x, window_y), 18)

def draw_snake(snake_body):
    for i, pos in enumerate(snake_body):
        if i == 0:  # Hlava hada
            pygame.draw.circle(game_window, green, (pos[0] + 5, pos[1] + 5), 7)
            pygame.draw.circle(game_window, white, (pos[0] + 2, pos[1] + 2), 2)
            pygame.draw.circle(game_window, white, (pos[0] + 8, pos[1] + 2), 2)
        else:
            pygame.draw.circle(game_window, (0, 200, 0), (pos[0] + 5, pos[1] + 5), 5)

def main_menu():
    font = pygame.font.SysFont('comicsansms', 35)
    while True:
        game_window.fill(dark_gray)
        draw_text("SNAKE GAME", font, yellow, window_x // 2, window_y // 4)
        draw_text("Press SPACE to Play", font, white, window_x // 2, window_y // 2)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return

def update_best_scores(score):
    save_score_to_db(score)  # Uloží skóre do databáze
    return get_top_scores()  # Načte nejlepší skóre z databáze

def game_over_screen(score):
    best_scores = update_best_scores(score)  # Aktualizace skóre v databázi

    font = pygame.font.SysFont('comicsansms', 30)
    while True:
        game_window.fill(dark_gray)
        draw_text("Game Over!", font, red, window_x // 2, window_y // 6)
        draw_text(f"Score: {score}", font, yellow, window_x // 2, window_y // 4)
        
        # Zobrazení nejlepších skóre
        draw_text("Best Scores:", font, white, window_x // 2, window_y // 3)
        for i, best_score in enumerate(best_scores):
            draw_text(f"{i+1}. {best_score}", font, yellow, window_x // 2, window_y // 3 + (i+1) * 30)
        
        draw_text("R = restart | Q = quit", font, white, window_x // 2, window_y // 1.5)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def spawn_fruit(snake_body):
    """Generuje pozici jablka tak, aby nebylo v těle hada."""
    while True:
        position = [random.randrange(3, (window_x // 10) - 3) * 10, 
                    random.randrange(3, (window_y // 10) - 3) * 10]
        if position not in snake_body:
            return position

def game_loop():
    global snake_speed
    while True:
        snake_position = [100, 50]
        snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
        direction = 'RIGHT'
        change_to = direction
        
        fruit_position = spawn_fruit(snake_body)
        fruit_spawn = True
        score = 0
        
        # Zlaté jablko
        golden_fruit_position = None
        golden_fruit_spawn = False
        golden_fruit_timer = 0
        original_snake_speed = snake_speed
        golden_fruit_lifetime = 0
        golden_fruit_spawn_time = 0
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        change_to = 'UP'
                    if event.key == pygame.K_DOWN:
                        change_to = 'DOWN'
                    if event.key == pygame.K_LEFT:
                        change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT:
                        change_to = 'RIGHT'
            
            if change_to == 'UP' and direction != 'DOWN':
                direction = 'UP'
            if change_to == 'DOWN' and direction != 'UP':
                direction = 'DOWN'
            if change_to == 'LEFT' and direction != 'RIGHT':
                direction = 'LEFT'
            if change_to == 'RIGHT' and direction != 'LEFT':
                direction = 'RIGHT'
            
            if direction == 'UP':
                snake_position[1] -= 10
            if direction == 'DOWN':
                snake_position[1] += 10
            if direction == 'LEFT':
                snake_position[0] -= 10
            if direction == 'RIGHT':
                snake_position[0] += 10
            
            snake_body.insert(0, list(snake_position))
            if snake_position == fruit_position:
                if score >= 30:
                    score += 10
                else:
                    score += 1
                fruit_spawn = False
            else:
                snake_body.pop()
            
            if not fruit_spawn:
                fruit_position = spawn_fruit(snake_body)
                fruit_spawn = True

            # Zlaté jablko - generování
            if not golden_fruit_spawn and random.randint(1, 1000) <= 10:  # 1% šance
                golden_fruit_position = spawn_fruit(snake_body)
                golden_fruit_spawn = True
                golden_fruit_spawn_time = time.time()
                golden_fruit_lifetime = random.randint(5, 15)
            
            # Vypršení zlatého jablka
            if golden_fruit_spawn and time.time() - golden_fruit_spawn_time > golden_fruit_lifetime:
                golden_fruit_spawn = False
            
            # Had snědl zlaté jablko
            if golden_fruit_spawn and snake_position == golden_fruit_position:
                snake_speed += 10
                golden_fruit_spawn = False
                golden_fruit_timer = time.time()

            # Reset rychlosti po vypršení efektu zlatého jablka
            if golden_fruit_timer and time.time() - golden_fruit_timer > 10:
                snake_speed = original_snake_speed
                golden_fruit_timer = 0

            # Vykreslení herního prostředí
            game_window.fill(black)
            draw_background()
            draw_frame()
            draw_snake(snake_body)
            
            # Normální jablko
            pygame.draw.circle(game_window, red, (fruit_position[0] + 5, fruit_position[1] + 5), 5)
            pygame.draw.line(game_window, (139, 69, 19), 
                             (fruit_position[0] + 5, fruit_position[1]), 
                             (fruit_position[0] + 5, fruit_position[1] - 4), 2)

            # Zlaté jablko
            if golden_fruit_spawn:
                pygame.draw.circle(game_window, yellow, (golden_fruit_position[0] + 5, golden_fruit_position[1] + 5), 5)
                pygame.draw.line(game_window, (139, 69, 19), 
                                 (golden_fruit_position[0] + 5, golden_fruit_position[1]), 
                                 (golden_fruit_position[0] + 5, golden_fruit_position[1] - 4), 2)

            if snake_position[0] < 20 or snake_position[0] >= window_x - 20 or \
               snake_position[1] < 20 or snake_position[1] >= window_y - 20 or \
               snake_position in snake_body[1:]:
                snake_speed = original_snake_speed
                game_over_screen(score)
                break  
            
            font = pygame.font.SysFont('comicsansms', 20)
            draw_text(f"Score: {score}", font, yellow, 60, 20)
            
            pygame.display.update()
            fps.tick(snake_speed)


main_menu()
while True:
    game_loop()

# Uzavření připojení k databázi při ukončení programu
conn.close()
