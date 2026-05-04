import pygame
import random

pygame.init()

# Settings
WIDTH, HEIGHT = 600, 400
BLOCK_SIZE = 20
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake - Practice 11")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Verdana", 20)

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Food Class
class Food:
    def __init__(self):
        self.respawn()

    def respawn(self):
        # Position
        self.x = round(random.randrange(0, WIDTH - BLOCK_SIZE) / 20.0) * 20.0
        self.y = round(random.randrange(0, HEIGHT - BLOCK_SIZE) / 20.0) * 20.0
        
        # Requirement: Randomly generate food with different weights
        self.weight = random.choice([1, 2, 5])
        if self.weight == 1: self.color = (200, 0, 0)   # Red (Normal)
        elif self.weight == 2: self.color = (0, 0, 255) # Blue (Double)
        else: self.color = (255, 215, 0)                # Gold (Jackpot)
        
        # Requirement: Foods which are disappearing after some time
        self.spawn_time = pygame.time.get_ticks()
        self.lifespan = 5000 # 5 seconds (5000 milliseconds)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, [self.x, self.y, BLOCK_SIZE, BLOCK_SIZE])

    def check_timer(self):
        current_time = pygame.time.get_ticks()
        # If the food has existed longer than its lifespan, respawn it
        if current_time - self.spawn_time > self.lifespan:
            self.respawn()

# Game Loop function
def gameLoop():
    game_over = False
    
    # Snake initial state
    x1, y1 = WIDTH / 2, HEIGHT / 2
    x1_change, y1_change = 0, 0
    snake_List = []
    Length_of_snake = 1
    score = 0
    
    food = Food()

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and x1_change == 0:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT and x1_change == 0:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP and y1_change == 0:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN and y1_change == 0:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        # Movement and collision with walls
        x1 += x1_change
        y1 += y1_change
        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_over = True

        screen.fill(BLACK)
        
        # Update and draw food
        food.check_timer() # Check if food needs to disappear
        food.draw(screen)

        # Update Snake body
        snake_Head = [x1, y1]
        snake_List.append(snake_Head)
        if len(snake_List) > Length_of_snake:
            del snake_List[0]

        # Self collision
        for x in snake_List[:-1]:
            if x == snake_Head:
                game_over = True

        # Draw Snake
        for x in snake_List:
            pygame.draw.rect(screen, GREEN, [x[0], x[1], BLOCK_SIZE, BLOCK_SIZE])

        # Eating Food
        if x1 == food.x and y1 == food.y:
            score += food.weight     # Add weighted score
            Length_of_snake += 1
            food.respawn()

        # Display UI
        time_left = max(0, (food.lifespan - (pygame.time.get_ticks() - food.spawn_time)) // 1000)
        score_text = font.render(f"Score: {score} | Food despawns in: {time_left}s", True, WHITE)
        screen.blit(score_text, [10, 10])

        pygame.display.update()
        clock.tick(15)

gameLoop()
pygame.quit()