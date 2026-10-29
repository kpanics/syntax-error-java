import math
import pygame
from game.ui.button import Button
from game.entities.draggable import DraggableItem
from game.entities.duke import Duke

VACANCY_TEXT = [
    "> INITIALIZING RETROGRADE SYSTEMS ARCHIVE...",
    "> SEARCHING FOR: CODE ARCHIVIST",
    "> STATUS: CRITICAL LEGACY DEBT DETECTED",
    "> ERROR: NoSuchMethodError: ThePast",
    "> REQUIREMENTS: JVM evolution, XML patience, semicolon appreciation.",
]

PROLOGUE_02_RULES = {
    "containers": ["JVM", "JRE", "JDK"],
    "items": {
        "engine": {"label": "Engine", "target": "JVM",
                   "error_msg": "Compilation error: The Engine is the core of the JVM."},
        "libraries": {"label": "Libraries", "target": "JRE",
                      "error_msg": "Compilation error: Libraries are part of the Runtime Environment (JRE)."},
        "javac": {"label": "javac", "target": "JDK",
                  "error_msg": "Compilation error: javac is a development tool. It belongs to the JDK."},
        "debugger": {"label": "Debugger", "target": "JDK",
                     "error_msg": "Compilation error: Debuggers are for developers. JRE is for running apps only."},
        "javadoc": {"label": "javadoc", "target": "JDK",
                    "error_msg": "Compilation error: javadoc is a development tool. It belongs to the JDK."}
    }
}


class PrologueScene01:
    def __init__(self, engine):
        self.engine = engine
        self.font_crt = pygame.font.SysFont("couriernew", 20, bold=True)
        self.font_btn = pygame.font.SysFont("couriernew", 16, bold=True)
        self.duke = Duke(era="1995", pos=(820, 480))
        self.btn_accept = Button((362, 600, 300, 50), "[ CLICK TO ACCEPT_VACANCY ]", self.font_btn, (10, 30, 10),
                                 (20, 80, 20), (0, 255, 0))
        self.time_passed = 0.0

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def update(self, dt):
        self.time_passed += dt

    def handle_event(self, event):
        if self.btn_accept.handle_event(event):
            return "prologue_02"
        return None

    def draw(self, screen):
        screen.fill((10, 10, 10))
        crt_rect = pygame.Rect(100, 80, 700, 450)
        pygame.draw.rect(screen, (15, 30, 15), crt_rect)
        pygame.draw.rect(screen, (50, 100, 50), crt_rect, 4)

        for y in range(crt_rect.top, crt_rect.bottom, 4):
            pygame.draw.line(screen, (0, 0, 0), (crt_rect.left, y), (crt_rect.right, y), 1)

        y_pos = crt_rect.top + 50
        for line in VACANCY_TEXT:
            color = (0, 255, 0) if math.sin(self.time_passed * 5) > -0.8 else (0, 100, 0)
            text_surf = self.font_crt.render(line, True, color)
            screen.blit(text_surf, (crt_rect.left + 40, y_pos))
            y_pos += 40

        if math.sin(self.time_passed * 6) > -0.5:
            self.btn_accept.draw(screen)

        self.duke.draw(screen)


class PrologueScene02:
    def __init__(self, engine):
        self.engine = engine
        self.font = pygame.font.SysFont("couriernew", 18, bold=True)
        self.font_ui = pygame.font.SysFont("couriernew", 14)
        self.duke = Duke(era="1995", pos=(80, 300))

        self.containers = {
            "JDK": pygame.Rect(300, 200, 140, 140),
            "JRE": pygame.Rect(320, 220, 100, 100),
            "JVM": pygame.Rect(340, 240, 60, 60)
        }

        self.items = [
            DraggableItem("engine", "Engine", (650, 200), self.font_ui),
            DraggableItem("libraries", "Libraries", (650, 350), self.font_ui),
            DraggableItem("javac", "javac", (650, 500), self.font_ui),
            DraggableItem("debugger", "Debugger", (800, 200), self.font_ui),
            DraggableItem("javadoc", "javadoc", (800, 350), self.font_ui),
        ]

        self.error_msg = ""
        self.error_timer = 0.0
        self.success = False

    def on_enter(self):
        pass

    def on_exit(self):
        pass

    def update(self, dt):
        if self.error_timer > 0:
            self.error_timer -= dt
            if self.error_timer <= 0:
                self.error_msg = ""

    def handle_event(self, event):
        for item in self.items:
            dragged = item.handle_event(event)
            if dragged and event.type == pygame.MOUSEBUTTONUP:
                self.check_drop(item)
                return None

    def check_drop(self, item):
        if getattr(item, 'is_locked', False):
            return

        target_container = None
        if self.containers["JVM"].collidepoint(item.rect.center):
            target_container = "JVM"
        elif self.containers["JRE"].collidepoint(item.rect.center):
            target_container = "JRE"
        elif self.containers["JDK"].collidepoint(item.rect.center):
            target_container = "JDK"

        if target_container:
            expected_target = PROLOGUE_02_RULES["items"][item.name]["target"]
            if target_container == expected_target:
                item.rect.center = self.containers[target_container].center
                item.is_locked = True
                self.duke.set_state("nod")
                self.error_msg = ""
            else:
                self.error_msg = PROLOGUE_02_RULES["items"][item.name]["error_msg"]
                self.error_timer = 2.5
                item.reset_position()
                self.duke.set_state("drop_cards")
        else:
            item.reset_position()

        self.check_win()

    def check_win(self):
        placed_count = sum(1 for item in self.items if getattr(item, 'is_locked', False))
        if placed_count == 5 and not self.success:
            self.success = True
            self.error_msg = "Pipeline ready: source -> javac -> bytecode -> JVM"
            self.error_timer = 3.0
            self.duke.set_state("point")
            pygame.time.set_timer(pygame.USEREVENT, 3000)

    def draw(self, screen):
        screen.fill((30, 30, 40))
        title = self.font.render("ASSEMBLE THE ENVIRONMENT", True, (255, 255, 255))
        screen.blit(title, (100, 50))

        for i in range(0, 1024, 64):
            pygame.draw.line(screen, (40, 40, 50), (i, 0), (i, 768))
        for j in range(0, 768, 64):
            pygame.draw.line(screen, (40, 40, 50), (0, j), (1024, j))

        for name, rect in self.containers.items():
            pygame.draw.rect(screen, (40, 40, 40), rect)
            pygame.draw.rect(screen, (100, 100, 100), rect, 2)
            lbl = self.font_ui.render(name, True, (100, 100, 100))
            screen.blit(lbl, (rect.x + 5, rect.y + 5))

        for item in self.items:
            item.draw(screen)
        self.duke.draw(screen)

        if self.error_msg:
            is_success = self.success
            color = (0, 255, 0) if is_success else (255, 50, 50)
            bg_color = (0, 50, 0) if is_success else (50, 0, 0)

            msg_surf = self.font.render(self.error_msg, True, color)
            msg_rect = msg_surf.get_rect(center=(512, 650))
            bg_rect = msg_rect.inflate(20, 10)

            pygame.draw.rect(screen, bg_color, bg_rect, border_radius=5)
            pygame.draw.rect(screen, color, bg_rect, 2, border_radius=5)
            screen.blit(msg_surf, msg_rect)