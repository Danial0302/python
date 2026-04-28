import pygame


class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text

    def draw(self, screen, font):
        mouse = pygame.mouse.get_pos()

        if self.rect.collidepoint(mouse):
            color = (170, 170, 170)
        else:
            color = (120, 120, 120)

        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 2, border_radius=8)

        label = font.render(self.text, True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=self.rect.center))

    def clicked(self, event):
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)