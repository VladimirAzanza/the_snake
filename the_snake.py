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

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH) // 2, (SCREEN_HEIGHT) // 2)
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw(self):
        """Draws the game map"""
        pass


class Apple(GameObject):
    """This class describes the apple actions"""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Gets the initial position x and y for the class"""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

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
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """Updates the direction of snake"""
        if self.next_direction:
            # Actualiza la direccion segun la tecla apretada
            self.direction = self.next_direction
            # Actualiza la direccion a none para que mantenga su curso
            self.next_direction = None

    def move(self):
        """Updates the position of snake"""
        """Add new head and remove last element if length has not increased"""
        self.update_direction()
        head_x, head_y = self.get_head_position()

        new_head_x = head_x + self.direction[0] * GRID_SIZE
        new_head_y = head_y + self.direction[1] * GRID_SIZE
        self.positions.insert(0, (new_head_x, new_head_y))

        if len(self.positions) > self.length:
            self.last = (head_x, head_y)
            self.positions.pop(-1)

        if new_head_x < 0:
            self.positions[0] = (SCREEN_WIDTH - GRID_SIZE, head_y)
        elif new_head_x >= SCREEN_WIDTH:
            self.positions[0] = (0, head_y)
        elif new_head_y < 0:
            self.positions[0] = (head_x, SCREEN_HEIGHT - GRID_SIZE)
        elif new_head_y >= SCREEN_HEIGHT:
            self.positions[0] = (head_x, 0)

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
        handle_keys(snake)
        snake.move()
        snake.draw(screen)
        apple.draw(screen)

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        pygame.display.update()


if __name__ == '__main__':
    main()
