import pygame
import random
import sys

pygame.init()

# Setup display
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer - Practice 11")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GOLD = (255, 215, 0)
SILVER = (192, 192, 192)
BRONZE = (205, 127, 50)

# Global Variables
SPEED = 5 # Initial enemy speed
COIN_SCORE = 0
SPEED_THRESHOLD = 10 # Increase speed every 10 coin points

# Player Class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 50)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.move_ip(-7, 0)
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.move_ip(7, 0)

# Enemy Class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), 0)

    def move(self):
        global SPEED
        self.rect.move_ip(0, SPEED) # Speed increases dynamically
        if self.rect.bottom > HEIGHT + 60:
            self.rect.center = (random.randint(40, WIDTH - 40), 0)

# Coin Class (Requirement: Random weights)
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Randomly generate coin weight and corresponding color/size
        self.weight = random.choice([1, 3, 5])
        
        if self.weight == 1:
            color = BRONZE
            size = 15
        elif self.weight == 3:
            color = SILVER
            size = 20
        else:
            color = GOLD
            size = 25
            
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (size//2, size//2), size//2)
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, WIDTH - 40), -50)

    def move(self):
        self.rect.move_ip(0, 4) # Coins move down the road
        if self.rect.top > HEIGHT:
            self.respawn()

    def respawn(self):
        self.__init__() # Re-roll weight and position

# Setup Sprites
P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group()
enemies.add(E1)
coins = pygame.sprite.Group()
coins.add(C1)
all_sprites = pygame.sprite.Group()
all_sprites.add(P1, E1, C1)

# Game Loop
font = pygame.font.SysFont("Verdana", 20)
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill(WHITE)
    
    # Render Scores
    score_text = font.render(f"Coins: {COIN_SCORE} | Speed: {SPEED}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Move and Draw Sprites
    for entity in all_sprites:
        screen.blit(entity.image, entity.rect)
        entity.move()

    # Collision Logic: Coins
    if pygame.sprite.spritecollideany(P1, coins):
        COIN_SCORE += C1.weight
        # Requirement: Increase speed when player earns N coins
        # Check if we crossed a multiple of SPEED_THRESHOLD
        if COIN_SCORE // SPEED_THRESHOLD > (COIN_SCORE - C1.weight) // SPEED_THRESHOLD:
            SPEED += 1
        C1.respawn()

    # Collision Logic: Enemies
    if pygame.sprite.spritecollideany(P1, enemies):
        pygame.time.wait(1000)
        running = False

    pygame.display.update()
    clock.tick(60)

pygame.quit()