import os

import pygame

from engine.game_ui.constants.text_constants import font, RED, GRAY
from engine.game_ui.constants.window_constants import SCREEN_WIDTH, SCREEN_HEIGHT


class RendererBase:
    screen: pygame.Surface
    resource_path: str

    def __init__(self, screen: pygame.Surface, resource_path: str = 'resources'):
        self.screen = screen
        self.resource_path = resource_path

    def render(self, *args, **kwargs):
        raise NotImplementedError

    def _scalling_factor(self, image: pygame.Surface) -> float:
        return min(SCREEN_WIDTH / image.get_width(), SCREEN_HEIGHT / image.get_height())

    @property
    def _hud_height(self) -> float:
        return SCREEN_HEIGHT // 3


class ForegroundRenderer(RendererBase):

    def render(self, character_image: str, *args, **kwargs):
        image = pygame.image.load(os.path.join(self.resource_path, character_image)).convert_alpha()

        image = pygame.transform.scale(
            image,
            (
                int(image.get_width() * self._scalling_factor(image)),
                int(image.get_height() * self._scalling_factor(image))
            )
        )
        foreground_x = (SCREEN_WIDTH - image.get_width()) // 2
        foreground_y = (SCREEN_HEIGHT - image.get_height()) // 2
        self.screen.blit(image, (foreground_x, foreground_y))


class BackgroundRenderer(RendererBase):
    def render(self, background: str, *args, **kwargs):
        image = pygame.image.load(os.path.join(self.resource_path, background)).convert()
        image = pygame.transform.scale(
            image,
            (
                int(image.get_width() * self._scalling_factor(image)),
                int(image.get_height() * self._scalling_factor(image))
            )
        )
        self.screen.blit(image, (0, 0))


class HUDRenderer(RendererBase):

    def __init__(self, screen: pygame.Surface, resource_path: str = 'resources'):
        super().__init__(screen, resource_path)
        self.font = pygame.font.Font(*font)

    def _draw_hud(self):
        hud_rect = pygame.Rect(0, SCREEN_HEIGHT - self._hud_height, SCREEN_WIDTH, self._hud_height)
        pygame.draw.rect(self.screen, (0, 0, 0), hud_rect)

    def _draw_text(self, character_name: str, text: str, *args, **kwargs):
        name_surface = self.font.render(f"{character_name}:", True, (255, 255, 255))
        name_rect = name_surface.get_rect(left=20, bottom=SCREEN_HEIGHT - (self._hud_height // 2))
        self.screen.blit(name_surface, name_rect)
        text_surface = self.font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(left=20, bottom=SCREEN_HEIGHT - (self._hud_height // 4))
        self.screen.blit(text_surface, text_rect)

    def _render_menu_items(self, menu_items: list[tuple[str, str]], selected_item: int):
        for i, item in enumerate(menu_items):
            color = GRAY if i == selected_item else RED
            text_surface = self.font.render(item[1], True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 25))
            self.screen.blit(text_surface, text_rect)

    def render(
            self,
            character_name: str,
            text: str,
            choices: list[tuple[str, str]] = None,
            selected_item: int = 0,
            *args, **kwargs
    ):
        self._draw_hud()
        self._draw_text(character_name, text, *args, **kwargs)
        if choices:
            self._render_menu_items(menu_items=choices, selected_item=selected_item)


class MenuRenderer(RendererBase):
    def __init__(self, screen: pygame.Surface, resource_path: str = 'resources'):
        super().__init__(screen, resource_path)
        self.font = pygame.font.Font(*font)

    def _render_menu_items(self, menu_items: list[str], selected_item: int):
        for i, item in enumerate(menu_items):
            color = GRAY if i == selected_item else RED
            text_surface = self.font.render(item, True, color)
            text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 200 + i * 35))
            self.screen.blit(text_surface, text_rect)

    def render(self, selected_item: int, menu_items: list[str], *args, **kwargs):
        self.screen.fill((0, 0, 0))
        self._render_menu_items(menu_items, selected_item)


class GameSceneRenderer:
    background_renderer: RendererBase
    foreground_renderer: RendererBase
    hud_renderer: RendererBase

    def __init__(
            self,
            background_renderer: RendererBase,
            foreground_renderer: RendererBase,
            hud_renderer: RendererBase
    ):
        self.background_renderer = background_renderer
        self.foreground_renderer = foreground_renderer
        self.hud_renderer = hud_renderer

    def render(
            self,
            background: str,
            character_name: str,
            character_image: str,
            text: str,
            choices: dict = None,
            *args, **kwargs
    ):
        self.background_renderer.render(background)
        self.foreground_renderer.render(character_image)
        self.hud_renderer.render(character_name, text, choices, *args, **kwargs)
