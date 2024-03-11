from random import choice, randint

import pygame as pg

pg.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (137, 133, 133)

BORDER_COLOR = (93, 216, 228)

APPLE_COLOR = (255, 0, 0)

SNAKE_COLOR = (0, 255, 0)

SPEED = 20

screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)

pg.display.set_caption('Змейка')

clock = pg.time.Clock()


class GameObject:
    """Initializes the GameObject for other Objects"""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH) // 2, (SCREEN_HEIGHT) // 2)
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw(self):
        """Draws the game map"""
        pass

    def draw_cell(self, surface, position, color=None):
        """sada"""
        color = color or self.body_color
        rect = (
            pg.Rect((position[0], position[1]),
                    (GRID_SIZE, GRID_SIZE))
        )
        pg.draw.rect(surface, color, rect)
        pg.draw.rect(surface, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """This class describes the apple actions"""

    def __init__(self) -> None:
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Returns the position for the Apple class"""
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """Draws the apple on screen"""
        self.draw_cell(surface, self.position, self.body_color)


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
            self.direction = self.next_direction
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
            self.last = self.positions[-1]
            self.positions.pop(-1)

        # Keeps the snake on the margins of the game
        if new_head_x < 0:
            self.positions[0] = (SCREEN_WIDTH - GRID_SIZE, head_y)
        elif new_head_x >= SCREEN_WIDTH:
            self.positions[0] = (0, head_y)
        elif new_head_y < 0:
            self.positions[0] = (head_x, SCREEN_HEIGHT - GRID_SIZE)
        elif new_head_y >= SCREEN_HEIGHT:
            self.positions[0] = (head_x, 0)

    def draw(self, surface):
        """Draws the snake on screen"""
        for position in self.positions[:-1]:
            self.draw_cell(surface, position, self.body_color)

        # Drawing the snake's head
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, head_rect)
        pg.draw.rect(surface, BORDER_COLOR, head_rect, 1)

        # Erase the last segment
        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]),
                (GRID_SIZE, GRID_SIZE)
            )
        pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Returns the position of snakes head"""
        return self.positions[0]

    def reset(self):
        """Resets the snake to its initial state after collision"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])


def handle_keys(game_object):
    """Processes the change direction"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Initializes the game"""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if snake.get_head_position() == apple.position:
            apple = Apple()
            snake.length += 1

        if snake.get_head_position() in snake.positions[2:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()

        apple.draw(screen)
        snake.draw(screen)

        pg.display.update()


if __name__ == '__main__':
    main()
