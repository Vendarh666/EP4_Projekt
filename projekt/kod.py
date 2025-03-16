import pygame
import time
import random

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

# Seznam pro nejlepší skóre
best_scores = [0, 0, 0]

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
    global best_scores
    best_scores.append(score)
    best_scores = sorted(best_scores, reverse=True)[:3]  # Udržujeme pouze tři nejlepší skóre

def game_over_screen(score):
    update_best_scores(score)  # Aktualizace nejlepšího skóre

    font = pygame.font.SysFont('comicsansms', 30)
    while True:
        game_window.fill(dark_gray)
        draw_text("Game Over!", font, red, window_x // 2, window_y // 6)
        draw_text(f"Score: {score}", font, yellow, window_x // 2, window_y // 4)
        
        # Zobrazení tří nejlepších skóre
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
                    return  # Restartuje hru
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def game_loop():
    while True:
        snake_position = [100, 50]
        snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
        direction = 'RIGHT'
        change_to = direction
        
        fruit_position = [random.randrange(3, (window_x//10) - 3) * 10, 
                          random.randrange(3, (window_y//10) - 3) * 10]
        fruit_spawn = True
        score = 0
        
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
            
            # Přidání nové hlavy hada
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
                fruit_position = [random.randrange(3, (window_x//10) - 3) * 10, 
                                  random.randrange(3, (window_y//10) - 3) * 10]
            fruit_spawn = True
            
            game_window.fill(black)
            draw_background()
            draw_frame()
            draw_snake(snake_body)
            pygame.draw.rect(game_window, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
            
            if snake_position[0] < 20 or snake_position[0] >= window_x - 20 or \
               snake_position[1] < 20 or snake_position[1] >= window_y - 20 or \
               snake_position in snake_body[1:]:
                game_over_screen(score)
                break  
            
            font = pygame.font.SysFont('comicsansms', 20)
            draw_text(f"Score: {score}", font, yellow, 60, 20)
            
            pygame.display.update()
            fps.tick(snake_speed)

main_menu()
while True:
    game_loop()
