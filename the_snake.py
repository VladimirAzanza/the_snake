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
    """
    Represents a game object for other game entities.

    Attributes
    ----------
    position : tuple
        initial position of the game object
    body_color : tuple
        initial body color of the game object

    Methods
    -------
    draw():
        Draws the game map.
    draw_cell(surface, position, color=None):
        Renders a single cell.

    """

    def __init__(self) -> None:
        """
        Sets all required attributes for the game object.
        Parameters
        ----------
        position : tuple
            initial position of the game object
        body_color : tuple
            initial body color of the game object
        """
        self.position = ((SCREEN_WIDTH) // 2, (SCREEN_HEIGHT) // 2)
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw(self):
        """
        Renders the game object and by default is pass.
        This method should be overriden in child classes.
        """
        pass

    def draw_cell(self, surface, position, color=None):
        """
        Method to render a single cell and will be useful for Apple and Snake.
        Parameters
        ----------
        surface : pygame.Surface
            Screen will be the surface to draw the cell on
        position : tuple
            Position of the cell to draw
        color : str, optional
            The color of the cell is set by default to the body color of game
            object
        """
        color = color or self.body_color
        rect = (
            pg.Rect((position[0], position[1]),
                    (GRID_SIZE, GRID_SIZE))
        )
        pg.draw.rect(surface, color, rect)


class Apple(GameObject):
    """
    Represents the apple in the game.

    Attributes
    ----------
    body_color : tuple
        For the color of the apple's body RGB is used (red color)
    position : tuple
        The position of the apple on the game board

    Methods
    -------
    randomize_position()
        Gives the position attribute for the apple a value.
    draw(surface)
        Renders the apple.
    """

    def __init__(self) -> None:
        """
        Sets all required attributes for the apple object.
        Parameters
        ----------
        position : tuple
            initial position of the game object taken from
            randomize position class
        body_color : tuple
            initial body color of the game object
        """
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """
        Returns the position for the Apple class.
        Returns
        -------
        tuple
            X position, Y position
        """
        return (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        )

    def draw(self, surface):
        """
        Renders the apple on screen.
        Parameters
        ----------
        surface : pygame.Surface
            Screen will be the surface to draw the cell on
        """
        self.draw_cell(surface, self.position, self.body_color)


class Snake(GameObject):
    """
    This class controls the movement, rendering, and user actions of the snake.

    Attributes
    ----------
    body_color : tuple
        For the color of the snake's body RGB is used (green)
    positions : list
        The position of the snake on the game board
    direction : tuple
        The initial direction of the snake
        By default the snake moves to the right
    next_direction : tuple, optional
        The next direction will be applied after the user keypress
        By default is None
    last : tuple, optional
        Position of last segment of the snake's body

    Class attributes
    ----------------
    length : int
        The initial length of the snake's body

    Methods
    -------
    update_direction()
        Updates the direction of the snake based on user input.
    move()
        Updates the position of the snake.
    draw(surface)
        Renders the snake on screen.
    get_head_position()
        Returns the position of the snake's head.
    reset()
        Resets the snake to its initial state after colliding with itself.
    """

    length = 1

    def __init__(self) -> None:
        """
        Sets all required attributes for the snake object.
        Parameters
        ----------
        body_color : tuple
            For the color of the snake's body RGB is used (green)
        positions : list
            A list of tuples with the position of the snake on the game board
        direction : tuple
            The initial direction of the snake
            By default the snake moves to the right
        next_direction : tuple, optional
            The next direction will be applied after the user keypress
            By default is None
        last : tuple, optional
            Position of last segment of the snake's body
        """
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def update_direction(self):
        """The next direction will be applied after the user keypress."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """
        Updates the position of snake.
        Add new head and remove last element if length has not increased.
        Keeps the snake on the margins of the game.
        """
        self.update_direction()
        head_x, head_y = self.get_head_position()

        new_head_x = head_x + self.direction[0] * GRID_SIZE
        new_head_y = head_y + self.direction[1] * GRID_SIZE
        self.positions.insert(0, (new_head_x, new_head_y))

        if len(self.positions) > self.length:
            self.last = self.positions[-1]
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
        """Renders the snake's body, head and tail on screen."""
        for position in self.positions[:-1]:
            self.draw_cell(surface, position, self.body_color)

        self.draw_cell(surface, self.positions[0], self.body_color)

        if self.last:
            self.draw_cell(surface, self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Returns the position of snakes head."""
        return self.positions[0]

    def reset(self):
        """Resets the snake to its initial state after collision"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])


def handle_keys(game_object):
    """
    Processes the change direction based on user keyboard inputs.

    Parameters
    ----------
    game_object : class
        The game object for which the direction will be updated
    """
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
