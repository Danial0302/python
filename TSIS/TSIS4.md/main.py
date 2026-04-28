import pygame
from game import SnakeGame
from db import get_or_create_player, save_game

pygame.init()

screen = pygame.display.set_mode((600, 600))
font = pygame.font.SysFont("arial", 24)
clock = pygame.time.Clock()
FPS = 60

state = "menu"
username = ""
player_id = None

game = SnakeGame()

while True:
    clock.tick(FPS)
    screen.fill((0, 0, 0))

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            pygame.quit()
            exit()

        # -------- MENU INPUT --------
        if state == "menu":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    if username.strip():
                        player_id = get_or_create_player(username)
                        game = SnakeGame()
                        state = "game"
                elif e.key == pygame.K_BACKSPACE:
                    username = username[:-1]
                else:
                    username += e.unicode

        # -------- GAME INPUT --------
        elif state == "game":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_UP:
                    game.set_direction((0, -20))
                elif e.key == pygame.K_DOWN:
                    game.set_direction((0, 20))
                elif e.key == pygame.K_LEFT:
                    game.set_direction((-20, 0))
                elif e.key == pygame.K_RIGHT:
                    game.set_direction((20, 0))

        # -------- GAME OVER INPUT --------
        elif state == "game_over":
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RETURN:
                    state = "menu"
                    username = ""
                    player_id = None

    # -------- MENU --------
    if state == "menu":
        text = font.render("Enter username: " + username, True, (255, 255, 255))
        screen.blit(text, (50, 300))

        hint = font.render("Press ENTER to play", True, (120, 120, 120))
        screen.blit(hint, (50, 340))

    # -------- GAME --------
    elif state == "game":
        game.update()

        # SAVE once when game ends
        if game.game_over:
            save_game(player_id, game.score, game.level)
            state = "game_over"

        # Draw snake
        for segment in game.snake:
            pygame.draw.rect(screen, (0, 255, 0), (*segment, 20, 20))

        # Draw food
        pygame.draw.rect(screen, (255, 0, 0), (*game.food, 20, 20))

        # Draw poison
        pygame.draw.rect(screen, (255, 255, 0), (*game.poison, 20, 20))

        # Draw obstacles
        for ob in game.obstacles:
            pygame.draw.rect(screen, (128, 128, 128), (*ob, 20, 20))

        text = font.render(f"Score: {game.score}  Level: {game.level}", True, (255, 255, 255))
        screen.blit(text, (20, 20))

    # -------- GAME OVER SCREEN --------
    elif state == "game_over":
        over = font.render("GAME OVER", True, (255, 0, 0))
        screen.blit(over, (220, 260))

        score_text = font.render(f"Score: {game.score}  Level: {game.level}", True, (255, 255, 255))
        screen.blit(score_text, (190, 300))

        restart = font.render("Press ENTER to return to menu", True, (150, 150, 150))
        screen.blit(restart, (130, 340))

    pygame.display.update()