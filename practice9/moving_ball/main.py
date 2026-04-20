import os
import pygame

pygame.init()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

screen = pygame.display.set_mode((700, 600))
pygame.display.set_caption("Ball")

bg = pygame.image.load(os.path.join(BASE_DIR, "bg_ball.png"))

circle_x = 325
circle_y = 275
color_red = (255,0,0)

radius = 20
speed = 25

clock = pygame.time.Clock()
FPS = 30

runnig = True
while runnig:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runnig = False
    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        circle_y -= speed
    if keys[pygame.K_DOWN]:
        circle_y += speed
    if keys[pygame.K_RIGHT]:
        circle_x += speed
    if keys[pygame.K_LEFT]:
        circle_x -= speed

    if circle_x - radius <0:
        circle_x = radius
    if circle_x + radius > 700:
        circle_x = 700 - radius
    if circle_y - radius <0:
        circle_y = radius
    if circle_y + radius > 600:
        circle_y = 600 - radius


    
    screen.blit(bg,(0,0))
    pygame.draw.circle(screen,color_red,(circle_x,circle_y),radius)
    clock.tick(FPS)
    pygame.display.flip()
pygame.quit()