from random import choice, randint
import pygame

# Инициализация PyGame:
pygame.init()

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Initializes the GameObject for other Objects"""

    position = (0, 0)

    def __init__(self) -> None:
        self.position_y = (SCREEN_HEIGHT) // 2
        self.position_x = (SCREEN_WIDTH) // 2
        GameObject.position = (self.position_x, self.position_y)

    def draw(self):
        """Draws the game map"""
        pass


class Apple(GameObject):
    """This class describes the apple actions"""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()
        Apple.position = (self.position_x, self.position_y)

    def randomize_position(self):
        """Gets the initial position x and y for the class"""
        self.position_y = randint(0, SCREEN_HEIGHT - 20)
        self.position_x = randint(0, SCREEN_WIDTH - 20)

    def draw(self, surface):
        """Draws the apple"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """This class controls the movement, rendering, and user actions."""

    length = 1

    def __init__(self) -> None:
        super().__init__()
        self.body_color = SNAKE_COLOR
        Snake.position = (self.position_x, self.position_y)
        self.positions = [Snake.position]
        self.direction = RIGHT

    def update_direction(self):
        """Updates the direction of snake"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Updates the position of snake"""
        """Add new head and remove last element if length has not increased"""
        self.get_head_position()


    def draw(self, surface):
        """Draws the snake"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

            # Отрисовка головы змейки
            head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, head_rect)
            pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

            # Затирание последнего сегмента
            if self.last:
                last_rect = pygame.Rect(
                    (self.last[0], self.last[1]),
                    (GRID_SIZE, GRID_SIZE)
                )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Returns the position of snakes head"""
        return self.positions[0]

    def reset(self):
        """Resets the snake to its initial state after collision"""
        pass

    @staticmethod
    def handle_keys(game_object):
        """Processes the change direction"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and game_object.direction != DOWN:
                    game_object.next_direction = UP
                elif event.key == pygame.K_DOWN and game_object.direction != UP:
                    game_object.next_direction = DOWN
                elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                    game_object.next_direction = LEFT
                elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                    game_object.next_direction = RIGHT


def main():
    """Initializes the game"""
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        apple.draw(screen)
        snake.handle_keys(snake)

        # snake.draw(screen)
        pygame.display.update()


if __name__ == '__main__':
    main()


# Метод draw класса Apple
# def draw(self, surface):
#     rect = pygame.Rect(
#         (self.position[0], self.position[1]),
#         (GRID_SIZE, GRID_SIZE)
#     )
#     pygame.draw.rect(surface, self.body_color, rect)
#     pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

# # Метод draw класса Snake
# def draw(self, surface):
#     for position in self.positions[:-1]:
#         rect = (
#             pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
#         )
#         pygame.draw.rect(surface, self.body_color, rect)
#         pygame.draw.rect(surface, BORDER_COLOR, rect, 1)

#     # Отрисовка головы змейки
#     head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
#     pygame.draw.rect(surface, self.body_color, head_rect)
#     pygame.draw.rect(surface, BORDER_COLOR, head_rect, 1)

#     # Затирание последнего сегмента
#     if self.last:
#         last_rect = pygame.Rect(
#             (self.last[0], self.last[1]),
#             (GRID_SIZE, GRID_SIZE)
#         )
#         pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

# Функция обработки действий пользователя
# def handle_keys(game_object):
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             pygame.quit()
#             raise SystemExit
#         elif event.type == pygame.KEYDOWN:
#             if event.key == pygame.K_UP and game_object.direction != DOWN:
#                 game_object.next_direction = UP
#             elif event.key == pygame.K_DOWN and game_object.direction != UP:
#                 game_object.next_direction = DOWN
#             elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
#                 game_object.next_direction = LEFT
#             elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
#                 game_object.next_direction = RIGHT

# Метод обновления направления после нажатия на кнопку
# def update_direction(self):
#     if self.next_direction:
#         self.direction = self.next_direction
#         self.next_direction = None
