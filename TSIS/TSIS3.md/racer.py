import pygame
import random
import time


WIDTH, HEIGHT = 500, 700
ROAD_X = 80
ROAD_W = 340
LANES = [125, 205, 285, 365]
PLAYER_Y = 580


CAR_COLORS = {
    "blue": (0, 100, 255),
    "red": (255, 0, 0),
    "green": (0, 180, 0),
    "yellow": (255, 220, 0)
}


class RacerGame:
    def __init__(self, username, settings):
        self.username = username
        self.settings = settings

        self.player = pygame.Rect(LANES[1], PLAYER_Y, 45, 75)
        self.car_color = CAR_COLORS.get(settings["car_color"], (0, 100, 255))

        self.traffic = []
        self.obstacles = []
        self.coins = []
        self.powerups = []

        self.coins_collected = 0
        self.score = 0
        self.distance = 0
        self.finish_distance = 3000

        self.game_over = False
        self.finished = False

        self.road_scroll = 0

        self.active_powerup = None
        self.powerup_end_time = 0
        self.shield = False

        self.spawn_timer = 0
        self.coin_timer = 0
        self.powerup_timer = 0

        self.set_difficulty(settings["difficulty"])

    def set_difficulty(self, difficulty):
        if difficulty == "easy":
            self.base_speed = 4
            self.spawn_rate = 80
        elif difficulty == "hard":
            self.base_speed = 7
            self.spawn_rate = 45
        else:
            self.base_speed = 5
            self.spawn_rate = 60

    def current_speed(self):
        speed = self.base_speed + self.distance // 700

        if self.active_powerup == "nitro":
            speed += 4

        return speed

    def move_player(self, keys):
        if keys[pygame.K_LEFT] and self.player.left > ROAD_X:
            self.player.x -= 6

        if keys[pygame.K_RIGHT] and self.player.right < ROAD_X + ROAD_W:
            self.player.x += 6

        if keys[pygame.K_UP] and self.player.top > 90:
            self.player.y -= 5

        if keys[pygame.K_DOWN] and self.player.bottom < HEIGHT - 20:
            self.player.y += 5

    def safe_lane(self):
        available = []

        for lane in LANES:
            test_rect = pygame.Rect(lane, 0, 45, 75)

            if abs(lane - self.player.x) > 50:
                available.append(lane)

        if not available:
            return random.choice(LANES)

        return random.choice(available)

    def spawn_traffic(self):
        lane = self.safe_lane()
        car = pygame.Rect(lane, -90, 45, 75)
        self.traffic.append(car)

    def spawn_obstacle(self):
        lane = self.safe_lane()
        kind = random.choice(["barrier", "oil", "pothole", "speed_bump"])
        rect = pygame.Rect(lane, -50, 50, 35)

        self.obstacles.append({
            "rect": rect,
            "type": kind
        })

    def spawn_coin(self):
        lane = random.choice(LANES)
        value = random.choice([1, 2, 5])
        rect = pygame.Rect(lane + 10, -30, 25, 25)

        self.coins.append({
            "rect": rect,
            "value": value
        })

    def spawn_powerup(self):
        lane = random.choice(LANES)
        kind = random.choice(["nitro", "shield", "repair"])

        rect = pygame.Rect(lane + 5, -35, 35, 35)

        self.powerups.append({
            "rect": rect,
            "type": kind,
            "created": time.time()
        })

    def activate_powerup(self, kind):
        if kind == "repair":
            if self.obstacles:
                self.obstacles.pop(0)
            self.score += 20
            return

        self.active_powerup = kind

        if kind == "nitro":
            self.powerup_end_time = time.time() + 4

        elif kind == "shield":
            self.shield = True
            self.powerup_end_time = 0

    def update_powerup(self):
        if self.active_powerup == "nitro":
            remaining = self.powerup_end_time - time.time()

            if remaining <= 0:
                self.active_powerup = None
                self.powerup_end_time = 0

    def check_collision(self):
        for car in self.traffic:
            if self.player.colliderect(car):
                if self.shield:
                    self.shield = False
                    self.active_powerup = None
                    self.traffic.remove(car)
                else:
                    self.game_over = True

        for obstacle in self.obstacles:
            if self.player.colliderect(obstacle["rect"]):
                if self.shield:
                    self.shield = False
                    self.active_powerup = None
                    self.obstacles.remove(obstacle)
                else:
                    if obstacle["type"] == "oil":
                        self.player.x += random.choice([-40, 40])
                    elif obstacle["type"] == "speed_bump":
                        self.distance = max(0, self.distance - 30)
                    else:
                        self.game_over = True

    def collect_items(self):
        for coin in self.coins[:]:
            if self.player.colliderect(coin["rect"]):
                self.coins_collected += coin["value"]
                self.score += coin["value"] * 10
                self.coins.remove(coin)

        for powerup in self.powerups[:]:
            if self.player.colliderect(powerup["rect"]):
                if self.active_powerup is None or powerup["type"] == "repair":
                    self.activate_powerup(powerup["type"])
                    self.powerups.remove(powerup)

    def remove_old_powerups(self):
        now = time.time()

        for p in self.powerups[:]:
            if now - p["created"] > 6:
                self.powerups.remove(p)

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        self.move_player(keys)

        speed = self.current_speed()
        self.distance += speed // 2
        self.score += speed // 4

        self.road_scroll += speed
        if self.road_scroll >= 40:
            self.road_scroll = 0

        self.spawn_timer += 1
        self.coin_timer += 1
        self.powerup_timer += 1

        difficulty_bonus = self.distance // 500
        actual_spawn_rate = max(20, self.spawn_rate - difficulty_bonus * 5)

        if self.spawn_timer >= actual_spawn_rate:
            if random.random() < 0.65:
                self.spawn_traffic()
            else:
                self.spawn_obstacle()
            self.spawn_timer = 0

        if self.coin_timer >= 55:
            self.spawn_coin()
            self.coin_timer = 0

        if self.powerup_timer >= 300:
            self.spawn_powerup()
            self.powerup_timer = 0

        for car in self.traffic[:]:
            car.y += speed
            if car.top > HEIGHT:
                self.traffic.remove(car)

        for obstacle in self.obstacles[:]:
            obstacle["rect"].y += speed
            if obstacle["rect"].top > HEIGHT:
                self.obstacles.remove(obstacle)

        for coin in self.coins[:]:
            coin["rect"].y += speed
            if coin["rect"].top > HEIGHT:
                self.coins.remove(coin)

        for powerup in self.powerups[:]:
            powerup["rect"].y += speed
            if powerup["rect"].top > HEIGHT:
                self.powerups.remove(powerup)

        self.collect_items()
        self.check_collision()
        self.update_powerup()
        self.remove_old_powerups()

        if self.distance >= self.finish_distance:
            self.finished = True
            self.game_over = True

    def draw_road(self, screen):
        screen.fill((30, 140, 30))

        pygame.draw.rect(screen, (50, 50, 50), (ROAD_X, 0, ROAD_W, HEIGHT))

        for x in [170, 250, 330]:
            for y in range(-40, HEIGHT, 80):
                pygame.draw.rect(
                    screen,
                    (255, 255, 255),
                    (x, y + self.road_scroll, 6, 40)
                )

    def draw(self, screen, font):
        self.draw_road(screen)

        pygame.draw.rect(screen, self.car_color, self.player, border_radius=8)

        for car in self.traffic:
            pygame.draw.rect(screen, (180, 0, 0), car, border_radius=8)

        for obstacle in self.obstacles:
            rect = obstacle["rect"]
            kind = obstacle["type"]

            if kind == "barrier":
                color = (255, 120, 0)
            elif kind == "oil":
                color = (10, 10, 10)
            elif kind == "pothole":
                color = (80, 50, 30)
            else:
                color = (180, 180, 180)

            pygame.draw.rect(screen, color, rect, border_radius=6)

        for coin in self.coins:
            pygame.draw.circle(screen, (255, 220, 0), coin["rect"].center, 13)
            value_text = font.render(str(coin["value"]), True, (0, 0, 0))
            screen.blit(value_text, value_text.get_rect(center=coin["rect"].center))

        for powerup in self.powerups:
            rect = powerup["rect"]
            kind = powerup["type"]

            if kind == "nitro":
                color = (0, 200, 255)
                letter = "N"
            elif kind == "shield":
                color = (120, 0, 255)
                letter = "S"
            else:
                color = (0, 255, 100)
                letter = "R"

            pygame.draw.rect(screen, color, rect, border_radius=8)
            text = font.render(letter, True, (0, 0, 0))
            screen.blit(text, text.get_rect(center=rect.center))

        self.draw_hud(screen, font)

    def draw_hud(self, screen, font):
        remaining = max(0, self.finish_distance - self.distance)

        texts = [
            f"Player: {self.username}",
            f"Score: {self.score}",
            f"Coins: {self.coins_collected}",
            f"Distance: {self.distance}m",
            f"Remaining: {remaining}m"
        ]

        y = 10
        for t in texts:
            label = font.render(t, True, (255, 255, 255))
            screen.blit(label, (10, y))
            y += 25

        if self.active_powerup:
            if self.active_powerup == "nitro":
                rem = max(0, int(self.powerup_end_time - time.time()))
                text = f"Power: NITRO {rem}s"
            elif self.active_powerup == "shield":
                text = "Power: SHIELD"
            else:
                text = "Power: NONE"

            label = font.render(text, True, (0, 255, 255))
            screen.blit(label, (330, 10))