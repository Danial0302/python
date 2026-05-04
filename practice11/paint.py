import pygame
import math

pygame.init()

# Setup
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Paint - Practice 11")
screen.fill((255, 255, 255)) # White background

# Variables
drawing = False
start_pos = (0, 0)
end_pos = (0, 0)
color = (0, 0, 0) # Black brush
mode = 'square' # Default mode

font = pygame.font.SysFont("Verdana", 16)

# Main Loop
running = True
screen_copy = screen.copy() # Used to display preview while dragging

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Keyboard controls to switch modes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1: mode = 'square'
            if event.key == pygame.K_2: mode = 'right_triangle'
            if event.key == pygame.K_3: mode = 'eq_triangle'
            if event.key == pygame.K_4: mode = 'rhombus'

        # Mouse Events
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # Left click
                drawing = True
                start_pos = event.pos
                screen_copy = screen.copy() # Save the canvas before drawing the new shape
                
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                drawing = False
                
        if event.type == pygame.MOUSEMOTION:
            if drawing:
                end_pos = event.pos

    # Drawing Logic (Preview mode while dragging)
    if drawing:
        screen.blit(screen_copy, (0, 0)) # Reset to clean canvas copy to avoid smearing
        x1, y1 = start_pos
        x2, y2 = end_pos
        
        # 1. Draw Square (Forces width and height to be equal)
        if mode == 'square':
            side = min(abs(x2 - x1), abs(y2 - y1))
            # Determine direction of drag to draw correctly in all quadrants
            dir_x = 1 if x2 > x1 else -1
            dir_y = 1 if y2 > y1 else -1
            rect = pygame.Rect(x1, y1, side * dir_x, side * dir_y)
            pygame.draw.rect(screen, color, rect, 2)
            
        # 2. Draw Right Triangle (Bottom-left corner is 90 degrees)
        elif mode == 'right_triangle':
            points = [(x1, y1), (x1, y2), (x2, y2)]
            pygame.draw.polygon(screen, color, points, 2)
            
        # 3. Draw Equilateral Triangle (Approximation within bounding box)
        elif mode == 'eq_triangle':
            mid_x = (x1 + x2) / 2
            # Calculate height using Pythagoras: h = side * sqrt(3) / 2
            width = abs(x2 - x1)
            height = width * (math.sqrt(3) / 2)
            dir_y = 1 if y2 > y1 else -1
            # Top point is center, bottom points are edges
            points = [(mid_x, y1), (x1, y1 + height * dir_y), (x2, y1 + height * dir_y)]
            pygame.draw.polygon(screen, color, points, 2)
            
        # 4. Draw Rhombus (Diamond shape connecting midpoints of bounding box)
        elif mode == 'rhombus':
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            points = [(mid_x, y1), (x2, mid_y), (mid_x, y2), (x1, mid_y)]
            pygame.draw.polygon(screen, color, points, 2)

    # UI Instructions overlay
    ui_rect = pygame.Rect(0, 0, WIDTH, 30)
    pygame.draw.rect(screen, (200, 200, 200), ui_rect)
    instruction = font.render(f"Current Mode: {mode.upper()} | Keys: 1=Square 2=Right Tri 3=Eq Tri 4=Rhombus", True, (0, 0, 0))
    screen.blit(instruction, (10, 5))

    pygame.display.flip()

pygame.quit()