import pygame
import random

CELL = 20
WIDTH, HEIGHT = 600, 600

class SnakeGame:
    def __init__(self):
        self.snake = [(100,100)]
        self.direction = (CELL, 0)
        self.next_direction = (CELL, 0)

        self.food = self.spawn_food()
        self.poison = self.spawn_poison()

        self.score = 0
        self.level = 1

        self.speed = 10
        self.move_counter = 0

        self.powerup = None
        self.powerup_time = 0

        self.obstacles = []

        self.game_over = False

    def set_direction(self, new_dir):
        """Set next direction (prevents 180-degree turns)"""
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.next_direction = new_dir

    # ---------------- FOOD ----------------
    def spawn_food(self):
        return (random.randint(0,29)*CELL, random.randint(0,29)*CELL)

    def spawn_poison(self):
        return (random.randint(0,29)*CELL, random.randint(0,29)*CELL)

    # ---------------- UPDATE ----------------
    def update(self):
        if self.game_over:
            return

        # Update move counter
        self.move_counter += 1
        frames_per_move = max(2, 15 - self.speed)  # Faster as speed increases

        if self.move_counter < frames_per_move:
            return

        self.move_counter = 0
        self.direction = self.next_direction

        head_x, head_y = self.snake[0]
        dx, dy = self.direction

        new_head = (head_x + dx, head_y + dy)

        # collision walls
        if new_head in self.obstacles:
            self.game_over = True

        if new_head[0] < 0 or new_head[1] < 0 or new_head[0] >= WIDTH or new_head[1] >= HEIGHT:
            self.game_over = True

        if new_head in self.snake:
            self.game_over = True

        self.snake.insert(0, new_head)

        # FOOD
        if new_head == self.food:
            self.score += 10
            self.food = self.spawn_food()
            self.level_up()
        else:
            self.snake.pop()

        # POISON
        if new_head == self.poison:
            self.snake = self.snake[:-2]
            if len(self.snake) <= 1:
                self.game_over = True
            self.poison = self.spawn_poison()

    # ---------------- LEVEL ----------------
    def level_up(self):
        if self.score % 50 == 0:
            self.level += 1
            self.speed += 1

            if self.level >= 3:
                self.spawn_obstacles()

    # ---------------- OBSTACLES ----------------
    def spawn_obstacles(self):
        self.obstacles = []
        for _ in range(self.level * 3):
            self.obstacles.append(
                (random.randint(0,29)*CELL, random.randint(0,29)*CELL)
            )