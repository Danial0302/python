import pygame
from datetime import datetime
import os

def mickclock():
    pygame.init()
    

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    images_dir = os.path.join(BASE_DIR, "image")
    
    screen = pygame.display.set_mode((500, 500))
    pygame.display.set_caption("Mickey's Clock")
    clock = pygame.time.Clock()

    try:
        bg = pygame.image.load(os.path.join(images_dir, "sagat_sureti.jpg"))
        lh = pygame.image.load(os.path.join(images_dir, "min.png"))  
        rh = pygame.image.load(os.path.join(images_dir, "time.png"))  
    except FileNotFoundError as e:
        print("Қате: Сурет табылмады!", e)
        print("images папкасы clock.py файлымен бір деңгейде болуы керек.")
        pygame.quit()
        return
    
    center = (250, 250)
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        now = datetime.now()
        sec = now.second
        minute = now.minute
        hour = now.hour % 12

        sec_angle = -sec * 6
        min_angle = -(minute * 6 + sec * 0.1)
        hour_angle = -(hour * 30 + minute * 0.5)
        
        screen.blit(bg, (0, 0))

        hour_rot = pygame.transform.rotate(lh, hour_angle)
        hour_rect = hour_rot.get_rect(center=center)
        screen.blit(hour_rot, hour_rect)

        min_rot = pygame.transform.rotate(rh, min_angle)
        min_rect = min_rot.get_rect(center=center)
        screen.blit(min_rot, min_rect)

        
        pygame.display.update()
        clock.tick(60)
    
    pygame.quit()


if __name__ == "__main__":
    mickclock()