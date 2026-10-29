import pygame


class Button:
    def __init__(self, rect, text, font, color_normal, color_hover, text_color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.color_normal = color_normal
        self.color_hover = color_hover
        self.text_color = text_color
        self.is_hovered = False

    def draw(self, surface):
        color = self.color_hover if self.is_hovered else self.color_normal
        pygame.draw.rect(surface, color, self.rect, border_radius=4)
        pygame.draw.rect(surface, self.text_color, self.rect, 2, border_radius=4)

        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False