import sys
import random
import os

import pygame
import pygame.gfxdraw
import pygame_widgets
from pygame_widgets.button import Button

sys.path.insert(0, os.path.dirname("."))

from game_objects import Snake, Fruit
from services import LargeFontService, SmallFontService, GameSoundService
from utils import Position


class Game:
    def __init__(self):
        self.window_fill_color = pygame.Color("black")
        self.window_top_margin = 30
        self.window_width = 500
        self.window_height = 500
        self.window_dimensions = (self.window_width, self.window_height)
        self.window_caption = "Snake Game By Kirabo Ibrahim <3"
        self.window = pygame.display.set_mode(self.window_dimensions)
        self.window.fill(self.window_fill_color)
        pygame.display.set_icon(pygame.image.load("./images/icon.png"))
        pygame.display.set_caption(self.window_caption)

        self.snake = None
        self.starting_snake_position = Position(100, 50)
        self.snake_crawl_unit_size = 10
        self.snake_displacement = (self.snake_crawl_unit_size, 0)
        self.snake_direction = "R"
        self.snake_size = self.snake_crawl_unit_size
        self.fruit = None
        self.eaten_fruit_reward = 10
        self.player_score = 0

        self.font_small = SmallFontService()
        self.font_large = LargeFontService()
        self.game_sound_service = GameSoundService()

        self.frame_rate = 10
        self.clock = pygame.time.Clock()

    def start(self):
        self.game_sound_service.play_background_music()
        self.spawn_snake()
        self.spawn_fruit()

        quit_game, game_over = False, False
        while not quit_game and not game_over:
            self.clear_screen()
            self.draw_score_board()
            self.draw_game_panel_separator()

            events = pygame.event.get()
            for event in events:
                if self.is_quit_event(event):
                    quit_game = True

                self.snake_displacement = self.get_displacement(event)

            self.snake_direction = self.get_snake_direction()
            self.snake.move(self.snake_displacement[0], self.snake_displacement[1])
            self.snake.draw(self.window)

            if self.is_game_over():
                game_over = True
            else:
                if self.has_snake_eaten_fruit():
                    self.update_player_score()
                    self.snake.grow()
                    self.game_sound_service.play_fruit_eaten_sound()
                    self.spawn_fruit()
                else:
                    # Fruit has not been eaten by the snake, re draw it at the same position
                    self.re_draw_fruit()

            pygame.display.update()
            self.clock.tick(self.frame_rate)
        if game_over:
            self.draw_game_over_screen()
        self.quit()

    def update_player_score(self) -> None:
        self.player_score += self.eaten_fruit_reward

    def draw_score_board(self) -> None:
        player_score_position = Position(10, 5)
        self.font_small.draw_text("Score: {}".format(self.player_score), self.window, player_score_position,
                                  pygame.Color("white"))

    def draw_game_panel_separator(self) -> None:
        pygame.gfxdraw.hline(self.window, 0, self.window_width, self.window_top_margin,
                             pygame.Color("white"))

    def spawn_fruit(self) -> None:
        fruit_position = self.generate_fruit_position()
        self.fruit = Fruit(fruit_position)
        self.fruit.draw(self.window)

    def generate_fruit_position(self) -> Position:
        """
        Movement of the snake is increments of snake_crawl_unit_size, so the position of the fruit should
        be a multiple of crawl size in order to avoid misalignment btn the snake body and the fruit
        """
        position_x = random.randint(1, self.window_width // self.snake_crawl_unit_size - self.snake_size) * \
                     self.snake_crawl_unit_size
        position_y = random.randint(self.window_top_margin // self.snake_crawl_unit_size,
                                    self.window_height // self.snake_crawl_unit_size - self.snake_size) * \
                     self.snake_crawl_unit_size
        return Position(position_x, position_y)

    def re_draw_fruit(self) -> None:
        self.fruit.draw(self.window)

    def spawn_snake(self) -> None:
        self.snake = Snake(self.starting_snake_position, self.snake_size)
        self.snake.draw(self.window)

    def has_snake_eaten_fruit(self) -> bool:
        fruit_position = self.fruit.get_position()
        snake_position = self.snake.get_position()
        if fruit_position.x == snake_position.x and fruit_position.y == snake_position.y:
            return True
        return False

    def is_game_over(self) -> bool:
        if self.has_snake_collided_with_walls() or self.snake.has_eaten_itself():
            return True
        return False

    def has_snake_collided_with_walls(self) -> bool:
        snake_position = self.snake.get_position()
        if snake_position.x < 0 or snake_position.x > self.window_width - self.snake_size:
            return True
        if snake_position.y < self.window_top_margin or \
                snake_position.y > self.window_height - self.snake_size:
            return True
        return False

    def draw_game_over_screen(self) -> None:
        self.clear_screen()
        self.game_sound_service.play_game_over_sound()
        self.draw_score_board()
        self.draw_game_panel_separator()
        self.font_large.draw_text_at_center("Game Over :(", self.window, pygame.Color("red"))
        self.font_small.draw_text("Press [SPACE] to restart game", self.window,
                                  Position(110, 300), pygame.Color("white"))

        quit_game, restart_game = False, False
        while not quit_game and not restart_game:
            events = pygame.event.get()
            for event in events:
                if self.is_quit_event(event):
                    quit_game = True
                if self.is_space_bar_key_event(event):
                    restart_game = True
            pygame.display.update()

        if restart_game:
            self.restart()
        self.quit()

    @staticmethod
    def is_space_bar_key_event(event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                return True
        return False

    def clear_screen(self) -> None:
        self.window.fill(self.window_fill_color)

    def get_snake_direction(self) -> str:
        """ Get the snake's current direction of movement,
        The snake is either moving left, right, up or down
        """
        displacement_x = self.snake_displacement[0]
        displacement_y = self.snake_displacement[1]
        if displacement_x > 0:
            return "R"
        elif displacement_x < 0:
            return "L"
        if displacement_y > 0:
            return "D"
        elif displacement_y < 0:
            return "U"

    def get_displacement(self, event: pygame.event.Event) -> tuple[int, int]:
        if self.is_arrow_key_pressed_event(event):
            if event.key == pygame.K_LEFT and self.snake_direction != "R":
                return -1 * self.snake_crawl_unit_size, 0
            elif event.key == pygame.K_RIGHT and self.snake_direction != "L":
                return self.snake_crawl_unit_size, 0
            elif event.key == pygame.K_UP and self.snake_direction != "D":
                return 0, -1 * self.snake_crawl_unit_size
            elif event.key == pygame.K_DOWN and self.snake_direction != "U":
                return 0, self.snake_crawl_unit_size
        return self.snake_displacement

    def restart(self) -> None:
        self.reset_game()
        self.start()

    def reset_game(self) -> None:
        self.player_score = 0
        self.snake_displacement = (self.snake_crawl_unit_size, 0)
        self.snake_direction = "R"

    @staticmethod
    def is_arrow_key_pressed_event(event: pygame.event.Event) -> bool:
        if event.type == pygame.KEYDOWN:
            return (event.key == pygame.K_LEFT) or (event.key == pygame.K_UP) or (event.key == pygame.K_DOWN) or \
                   (event.key == pygame.K_RIGHT)
        return False

    @staticmethod
    def quit() -> None:
        pygame.quit()
        sys.exit()

    @staticmethod
    def is_quit_event(event: pygame.event.Event) -> bool:
        return event.type == pygame.QUIT

    def draw_startup_screen(self):
        startup_image = pygame.image.load("./images/background.png")
        self.window.blit(startup_image, startup_image.get_rect())
        self.draw_start_button()
        self.draw_exit_button()
        self.game_sound_service.play_snake_hissing_sound()

        quit_game = False
        while not quit_game:
            events = pygame.event.get()
            for event in events:
                if self.is_quit_event(event):
                    quit_game = True

            pygame_widgets.update(events)
            pygame.display.update()
        self.quit()

    def draw_start_button(self) -> None:
        start_button_width, start_button_height = 200, 100
        start_button_position_x, start_button_position_y = self.window_width // 2 - 100, self.window_height // 2 - 100
        start_button = Button(self.window, start_button_position_x, start_button_position_y, start_button_width,
                              start_button_height, text="START", font=self.font_large.get_font(),
                              textColour=(255, 255, 255), inactiveColour=(97, 118, 75), radius=20, onClick=self.start
                              )

    def draw_exit_button(self) -> None:
        exit_button_width, exit_button_height = 200, 100
        exit_button_position_x, exit_button_position_y = self.window_width // 2 - 100, self.window_height // 2 + 90
        exit_button = Button(self.window, exit_button_position_x, exit_button_position_y, exit_button_width,
                             exit_button_height, text="EXIT", font=self.font_large.get_font(),
                             textColour=(255, 255, 255), inactiveColour=(97, 118, 75), radius=20, onClick=self.quit
                             )

    def draw_restart_button(self) -> None:
        restart_button_width, restart_button_height = 200, 100
        restart_button_position_x, restart_button_position_y = self.window_width // 2 - 100, self.window_height // 2 + 90
        restart_button = Button(self.window, restart_button_position_x, restart_button_position_y, restart_button_width,
                                restart_button_height, text="RESTART", font=self.font_large.get_font(),
                                textColour=(255, 255, 255), inactiveColour=(97, 118, 75), radius=20, onClick=self.start
                                )


if __name__ == "__main__":
    pygame.init()
    try:
        game = Game()
        game.draw_startup_screen()
    except KeyboardInterrupt:
        pygame.quit()
        sys.exit()
