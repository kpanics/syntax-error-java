import pygame


class DraggableItem:
    def __init__(self, name, label, pos, font, size=(64, 64)):
        self.name = name
        self.label = label
        self.original_pos = pos
        self.rect = pygame.Rect(pos[0], pos[1], size[0], size[1])
        self.is_dragging = False
        self.is_locked = False

        self.image = pygame.Surface(size, pygame.SRCALPHA)
        self.image.fill((70, 70, 70))
        pygame.draw.rect(self.image, (200, 200, 200), (0, 0, size[0], size[1]), 2)

        words = label.split()
        y_offset = 10
        for word in words:
            text = font.render(word, True, (255, 255, 255))
            text_rect = text.get_rect(center=(size[0] // 2, y_offset))
            self.image.blit(text, text_rect)
            y_offset += 15

    def handle_event(self, event):
        if self.is_locked:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.is_dragging = True
                self.offset_x = self.rect.x - event.pos[0]
                self.offset_y = self.rect.y - event.pos[1]
                return True
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if self.is_dragging:
                self.is_dragging = False
                return True
        elif event.type == pygame.MOUSEMOTION and self.is_dragging:
            self.rect.x = event.pos[0] + self.offset_x
            self.rect.y = event.pos[1] + self.offset_y
        return False

    def reset_position(self):
        self.is_dragging = False
        self.rect.topleft = self.original_pos

    def draw(self, surface):
        surface.blit(self.image, self.rect)