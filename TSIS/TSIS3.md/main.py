import pygame
from racer import RacerGame, WIDTH, HEIGHT
from ui import Button
from persistence import load_settings, save_settings, load_leaderboard, add_score


pygame.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS3 Racer Game")

font = pygame.font.SysFont("arial", 24)
big_font = pygame.font.SysFont("arial", 42)
clock = pygame.time.Clock()

settings = load_settings()

state = "menu"
username = ""
game = None
score_saved = False


play_btn = Button(160, 220, 180, 50, "Play")
leader_btn = Button(160, 290, 180, 50, "Leaderboard")
settings_btn = Button(160, 360, 180, 50, "Settings")
quit_btn = Button(160, 430, 180, 50, "Quit")

retry_btn = Button(80, 480, 150, 50, "Retry")
menu_btn = Button(270, 480, 150, 50, "Main Menu")
back_btn = Button(160, 600, 180, 45, "Back")


def draw_title(text):
    label = big_font.render(text, True, (255, 255, 255))
    screen.blit(label, label.get_rect(center=(WIDTH // 2, 100)))


def draw_menu():
    screen.fill((20, 20, 20))
    draw_title("RACER GAME")

    play_btn.draw(screen, font)
    leader_btn.draw(screen, font)
    settings_btn.draw(screen, font)
    quit_btn.draw(screen, font)


def draw_username_screen():
    screen.fill((20, 20, 20))
    draw_title("ENTER NAME")

    text = font.render("Username: " + username, True, (255, 255, 255))
    screen.blit(text, (80, 260))

    hint = font.render("Press Enter to start", True, (150, 150, 150))
    screen.blit(hint, (80, 310))


def draw_leaderboard():
    screen.fill((20, 20, 20))
    draw_title("LEADERBOARD")

    data = load_leaderboard()

    y = 170
    if not data:
        text = font.render("No scores yet.", True, (255, 255, 255))
        screen.blit(text, (150, y))
    else:
        for i, item in enumerate(data, start=1):
            line = f"{i}. {item['name']} | Score: {item['score']} | Distance: {item['distance']}m"
            text = font.render(line, True, (255, 255, 255))
            screen.blit(text, (40, y))
            y += 35

    back_btn.draw(screen, font)


def draw_settings():
    screen.fill((20, 20, 20))
    draw_title("SETTINGS")

    sound = "ON" if settings["sound"] else "OFF"

    lines = [
        f"1. Sound: {sound}",
        f"2. Car color: {settings['car_color']}",
        f"3. Difficulty: {settings['difficulty']}",
        "",
        "Press 1 to toggle sound",
        "Press 2 to change color",
        "Press 3 to change difficulty"
    ]

    y = 200
    for line in lines:
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (70, y))
        y += 35

    back_btn.draw(screen, font)


def draw_game_over():
    screen.fill((20, 20, 20))

    if game.finished:
        title = "FINISHED!"
    else:
        title = "GAME OVER"

    draw_title(title)

    lines = [
        f"Player: {game.username}",
        f"Score: {game.score}",
        f"Distance: {game.distance}m",
        f"Coins: {game.coins_collected}"
    ]

    y = 210
    for line in lines:
        text = font.render(line, True, (255, 255, 255))
        screen.blit(text, (120, y))
        y += 40

    retry_btn.draw(screen, font)
    menu_btn.draw(screen, font)


def cycle_color():
    colors = ["blue", "red", "green", "yellow"]
    current = settings["car_color"]
    index = colors.index(current)
    settings["car_color"] = colors[(index + 1) % len(colors)]
    save_settings(settings)


def cycle_difficulty():
    diffs = ["easy", "normal", "hard"]
    current = settings["difficulty"]
    index = diffs.index(current)
    settings["difficulty"] = diffs[(index + 1) % len(diffs)]
    save_settings(settings)


running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if state == "menu":
            if play_btn.clicked(event):
                username = ""
                state = "username"

            elif leader_btn.clicked(event):
                state = "leaderboard"

            elif settings_btn.clicked(event):
                state = "settings"

            elif quit_btn.clicked(event):
                running = False

        elif state == "username":
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if username.strip():
                        game = RacerGame(username, settings)
                        score_saved = False
                        state = "game"

                elif event.key == pygame.K_BACKSPACE:
                    username = username[:-1]

                else:
                    username += event.unicode

        elif state == "leaderboard":
            if back_btn.clicked(event):
                state = "menu"

        elif state == "settings":
            if back_btn.clicked(event):
                state = "menu"

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    settings["sound"] = not settings["sound"]
                    save_settings(settings)

                elif event.key == pygame.K_2:
                    cycle_color()

                elif event.key == pygame.K_3:
                    cycle_difficulty()

        elif state == "game_over":
            if retry_btn.clicked(event):
                game = RacerGame(username, settings)
                score_saved = False
                state = "game"

            elif menu_btn.clicked(event):
                state = "menu"

    if state == "menu":
        draw_menu()

    elif state == "username":
        draw_username_screen()

    elif state == "leaderboard":
        draw_leaderboard()

    elif state == "settings":
        draw_settings()

    elif state == "game":
        game.update()
        game.draw(screen, font)

        if game.game_over:
            if not score_saved:
                add_score(game.username, game.score, game.distance)
                score_saved = True

            state = "game_over"

    elif state == "game_over":
        draw_game_over()

    pygame.display.update()

pygame.quit()