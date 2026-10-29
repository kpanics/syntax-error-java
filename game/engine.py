import pygame
from game.scenes.pause_overlay import PauseOverlay

class Engine:
    def __init__(self, screen, clock):
        self.screen = screen
        self.clock = clock
        self.scenes = {}
        self.current_scene = None
        self.current_scene_key = None
        self.pause_overlay = None

    def register_scene(self, key: str, scene_instance):
        self.scenes[key] = scene_instance

    def change_scene(self, key: str):
        if self.current_scene:
            self.current_scene.on_exit()
        self.current_scene_key = key
        self.current_scene = self.scenes.get(key)
        if self.current_scene:
            self.current_scene.on_enter()
        self.pause_overlay = None

    def handle_event(self, event):
        # 1. Перехват ESC для паузы (ДО сцены)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            if self.pause_overlay:
                self.pause_overlay = None
            elif self.current_scene_key != "main_menu":
                self.pause_overlay = PauseOverlay(self)
            return

        # 2. Если пауза активна, события идут только в оверлей
        if self.pause_overlay:
            action = self.pause_overlay.handle_event(event)
            if action == "resume":
                self.pause_overlay = None
            elif action == "restart":
                self.change_scene(self.current_scene_key)
            elif action == "chapter_select":
                self.change_scene("chapter_select")
            elif action == "main_menu":
                self.change_scene("main_menu")
            return

        # 3. Иначе события идут в сцену
        if not self.current_scene:
            return
        next_scene_key = self.current_scene.handle_event(event)
        if next_scene_key:
            self.change_scene(next_scene_key)

    def update(self, dt):
        # Сцена не обновляется, если открыта пауза
        if self.current_scene and not self.pause_overlay:
            self.current_scene.update(dt)

    def draw(self):
        if self.current_scene:
            self.current_scene.draw(self.screen)
        if self.pause_overlay:
            self.pause_overlay.draw(self.screen)