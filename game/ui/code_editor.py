import pygame
from game.utils.lexer import SimpleJavaLexer


class CodeEditor:
    def __init__(self, rect, font, initial_text=""):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.text = initial_text
        self.cursor_pos = len(self.text)  # По умолчанию в конец
        self.cursor_visible = True
        self.cursor_timer = 0
        self.lexer = SimpleJavaLexer()
        self.line_height = font.get_linesize()

        self.key_map = {
            pygame.K_SEMICOLON: ';',
            pygame.K_LEFTBRACKET: '[',
            pygame.K_RIGHTBRACKET: ']',
            pygame.K_COMMA: ',',
            pygame.K_PERIOD: '.',
            pygame.K_QUOTE: '"',
            pygame.K_SPACE: ' ',
            pygame.K_RETURN: '\n',
            pygame.K_TAB: '    '
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                if self.cursor_pos > 0:
                    self.text = self.text[:self.cursor_pos - 1] + self.text[self.cursor_pos:]
                    self.cursor_pos -= 1
                return False

            if event.key == pygame.K_v and (event.mod & pygame.KMOD_CTRL):
                clipboard_text = pygame.scrap.get(pygame.SCRAP_TEXT)
                if clipboard_text:
                    try:
                        clean_text = clipboard_text.decode('utf-8').replace('\r', '').replace('\x00', '')
                        self.text = self.text[:self.cursor_pos] + clean_text + self.text[self.cursor_pos:]
                        self.cursor_pos += len(clean_text)
                    except:
                        pass
                return False

            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                return False

            char = ""
            if event.key in self.key_map:
                char = self.key_map[event.key]
            elif event.unicode and event.unicode.isprintable():
                char = event.unicode

            if char:
                self.text = self.text[:self.cursor_pos] + char + self.text[self.cursor_pos:]
                self.cursor_pos += len(char)
                return False

        return False

    def update(self, dt):
        self.cursor_timer += dt
        if self.cursor_timer >= 0.5:
            self.cursor_visible = not self.cursor_visible
            self.cursor_timer = 0

    def draw(self, surface):
        pygame.draw.rect(surface, (30, 30, 30), self.rect)
        pygame.draw.rect(surface, (100, 100, 100), self.rect, 2)

        tokens_per_line = self.lexer.tokenize(self.text)
        y = self.rect.y + 10
        cursor_x, cursor_y = self.rect.x + 10, self.rect.y + 10

        current_line_idx = self.text[:self.cursor_pos].count('\n')
        current_col_idx = self.cursor_pos - self.text[:self.cursor_pos].rfind('\n') - 1

        for line_idx, line_tokens in enumerate(tokens_per_line):
            x = self.rect.x + 10
            for token_text, token_type, start_pos in line_tokens:
                color = self.lexer.colors.get(token_type, self.lexer.colors['DEFAULT'])
                text_surf = self.font.render(token_text, True, color)
                surface.blit(text_surf, (x, y))
                x += self.font.size(token_text)[0]

            if line_idx == current_line_idx:
                prefix_text = self.text[self.text[:self.cursor_pos].rfind('\n') + 1:self.cursor_pos]
                cursor_x = self.rect.x + 10 + self.font.size(prefix_text)[0]
                cursor_y = y

            y += self.line_height

        if self.cursor_visible:
            pygame.draw.line(surface, (255, 255, 255), (cursor_x, cursor_y),
                             (cursor_x, cursor_y + self.line_height - 4), 2)

    def get_code(self) -> str:
        return self.text