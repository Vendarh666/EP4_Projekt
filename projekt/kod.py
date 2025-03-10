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

# Barvy
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
yellow = (255, 255, 0)
dark_gray = (50, 50, 50)

# FPS
fps = pygame.time.Clock()
snake_speed = 10

def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(x, y))
    game_window.blit(text_surface, text_rect)

def draw_background():
    for x in range(0, window_x, 20):
        pygame.draw.line(game_window, dark_gray, (x, 0), (x, window_y), 1)
    for y in range(0, window_y, 20):
        pygame.draw.line(game_window, dark_gray, (0, y), (window_x, y), 1)

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

def game_over_screen(score):
    font = pygame.font.SysFont('comicsansms', 30)
    while True:
        game_window.fill(dark_gray)
        draw_text("Game Over!", font, red, window_x // 2, window_y // 4)
        draw_text(f"Score: {score}", font, yellow, window_x // 2, window_y // 3)
        draw_text("R = restart | Q = quit", font, white, window_x // 2, window_y // 2)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True  # Indikace restartu
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()

def game_loop():
    while True:
        snake_position = [100, 50]
        snake_body = [[100, 50], [90, 50], [80, 50], [70, 50]]
        direction = 'RIGHT'
        change_to = direction
        
        fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                          random.randrange(1, (window_y//10)) * 10]
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
            
            snake_body.insert(0, list(snake_position))
            if snake_position == fruit_position:
                score += 1
                fruit_spawn = False
            else:
                snake_body.pop()
            
            if not fruit_spawn:
                fruit_position = [random.randrange(1, (window_x//10)) * 10, 
                                  random.randrange(1, (window_y//10)) * 10]
            fruit_spawn = True
            
            game_window.fill(black)
            draw_background()
            for pos in snake_body:
                pygame.draw.rect(game_window, green, pygame.Rect(pos[0], pos[1], 10, 10))
            pygame.draw.rect(game_window, red, pygame.Rect(fruit_position[0], fruit_position[1], 10, 10))
            
            if snake_position[0] < 0 or snake_position[0] >= window_x or \
               snake_position[1] < 0 or snake_position[1] >= window_y:
                if game_over_screen(score):
                    break  # Restart celé hry
            
            for block in snake_body[1:]:
                if snake_position == block:
                    if game_over_screen(score):
                        break  # Restart celé hry
            
            font = pygame.font.SysFont('comicsansms', 20)
            draw_text(f"Score: {score}", font, yellow, 60, 20)
            
            pygame.display.update()
            fps.tick(snake_speed)

main_menu()
while True:
    game_loop()
