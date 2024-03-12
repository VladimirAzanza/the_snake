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

    def __init__(self, body_color=BOARD_BACKGROUND_COLOR) -> None:
        """
        Initializes the game object with a board background color.

        Parameters
        ----------
        position : tuple
            initial position of the game object
        body_color : tuple
            initial body color of the game object
        """
        self.position = ((SCREEN_WIDTH) // 2, (SCREEN_HEIGHT) // 2)
        self.body_color = body_color

    def draw(self):
        """Renders the game object and by default is pass."""
        pass

    def draw_cell(self, position, color=None, border_color=None):
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
            pg.Rect((position),
                    (GRID_SIZE, GRID_SIZE))
        )
        pg.draw.rect(screen, color, rect)
        if border_color:
            pg.draw.rect(screen, border_color, rect, 1)


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
    draw()
        Renders the apple.
    """

    def __init__(self, snake_positions=[]) -> None:
        """
        Initializes the Apple object with a random position.

        Parameters
        ----------
        position : tuple
            initial position of the game object taken from
            randomize position class
        body_color : tuple
            initial body color of the game object
        """
        super().__init__(body_color=APPLE_COLOR)
        self.position = self.randomize_position(snake_positions)

    def randomize_position(self, snake_positions):
        """
        Returns the position for the Apple class.

        Parameters
        ----------
        snake_positions : list
            List of snake's body and head positions
        Returns
        -------
        new_position : tuple
        """
        while True:
            new_position = (
                randint(0, GRID_WIDTH - 1) * GRID_SIZE,
                randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            )
            if new_position not in snake_positions:
                return new_position

    def draw(self):
        """Renders the apple on screen."""
        self.draw_cell(self.position, self.body_color, BORDER_COLOR)


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
    length : int
        The initial length of the snake's body

    Methods
    -------
    update_direction()
        Updates the direction of the snake based on user input.
    move()
        Updates the position of the snake.
    draw()
        Renders the snake on screen.
    get_head_position()
        Returns the position of the snake's head.
    reset()
        Resets the snake to its initial state after colliding with itself.
    """

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
        length : int
            The initial length of the snake's body
        """
        super().__init__(body_color=SNAKE_COLOR)
        self.direction = RIGHT
        self.reset()

    # Здесь в update_direction(self) не понял что надо делать
    def update_direction(self, next_direction):
        """The next direction will be applied after the user keypress."""
        self.direction = next_direction

    def move(self):
        """
        Updates the position of snake.
        Add new head and remove last element if length has not increased.
        """
        head_x, head_y = self.get_head_position()

        self.positions.insert(
            0,
            (
                (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
                (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT
            )
        )

        if len(self.positions) > self.length:
            self.last = self.positions.pop()

    def draw(self):
        """Renders the snake's body and tail on screen."""
        self.draw_cell(self.get_head_position(), self.body_color, BORDER_COLOR)

        if self.last:
            self.draw_cell(self.last, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Returns the position of snakes head."""
        return self.positions[0]

    def reset(self):
        """Resets the snake to its initial state after collision."""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice([UP, DOWN, RIGHT, LEFT])
        self.last = None


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
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.update_direction(UP)
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.update_direction(DOWN)
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.update_direction(LEFT)
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.update_direction(RIGHT)


def main():
    """Initializes the game."""
    apple = Apple()
    snake = Snake()

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.move()

        if (head_position := snake.get_head_position()) == apple.position:
            apple = Apple(snake.positions)
            snake.length += 1

        if head_position in snake.positions[2:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()

        apple.draw()
        snake.draw()

        pg.display.update()


if __name__ == '__main__':
    main()
