import pygame

from utils import Position


class FontService:
    def __init__(self, filename: str, font_size: int):
        self.__font = pygame.font.Font(filename, font_size)
        self.__font_size = font_size

    def draw_text(self, text: str, surface: pygame.Surface, position: Position, color: pygame.Color) -> None:
        text_surface = self.__font.render(text, True, color)
        surface.blit(text_surface, (position.x, position.y))

    def draw_text_at_center(self, text: str, surface: pygame.Surface, color: pygame.Color) -> None:
        surface_width, surface_height = surface.get_size()
        text_surface = self.__font.render(text, True, color)
        text_surface_height = text_surface.get_size()[1]
        text_rect = text_surface.get_rect()
        text_rect.midtop = (surface_width // 2, surface_height // 2 - text_surface_height)
        surface.blit(text_surface, text_rect)

    def draw_text_at_bottom_center(self, text: str, surface: pygame.Surface, color: pygame.Color) -> None:
        surface_width, surface_height = surface.get_size()
        text_surface = self.__font.render(text, True, color)
        text_surface_height = text_surface.get_size()[1]
        text_rect = text_surface.get_rect()
        text_rect.midtop = (surface_width // 2, surface_height - text_surface_height)
        surface.blit(text_surface, text_rect)

    def get_font(self):
        return self.__font


class SmallFontService(FontService):
    def __init__(self, filename: str = "./fonts/KidpixiesRegular.ttf"):
        super().__init__(filename, font_size=18)


class LargeFontService(FontService):
    def __init__(self, filename: str = "./fonts/KidpixiesRegular.ttf"):
        super().__init__(filename, font_size=44)


class GameSoundService:
    def __init__(self) -> None:
        self.fruit_eaten_sound_channel = pygame.mixer.Channel(0)
        self.fruit_eaten_sound_channel.set_volume(0.9)
        self.main_channel = pygame.mixer.Channel(1)
        self.main_channel.set_volume(0.6)

        self.background_music_sound = pygame.mixer.Sound("./sounds/background.ogg")
        self.fruit_eaten_sound = pygame.mixer.Sound("./sounds/fruit_eaten.wav")
        self.game_over_sound = pygame.mixer.Sound("./sounds/game_over.wav")
        self.snake_hissing_sound = pygame.mixer.Sound("./sounds/snake-hissing-sound.mp3")

    def play_background_music(self) -> None:
        self.main_channel.play(self.background_music_sound, loops=-1)

    def play_fruit_eaten_sound(self) -> None:
        self.fruit_eaten_sound_channel.play(self.fruit_eaten_sound)

    def play_game_over_sound(self) -> None:
        self.main_channel.play(self.game_over_sound)

    def play_snake_hissing_sound(self) -> None:
        self.main_channel.play(self.snake_hissing_sound, loops=-1)
