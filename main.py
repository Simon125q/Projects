"""
This is a simple Snake game in Python using Pygame library
"""
import random
import sys

import pygame
from pygame.math import Vector2


class Snake:
    """
    This class represents the snake in the game, it keeps track
    of the snake's body parts as a list of Vector2 objects
    """

    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]

    def draw_snake(self):
        """
        Function to draw the snake
        """
        for part in self.body:
            x = part.x * cell_size
            y = part.y * cell_size
            part_rect = pygame.Rect(x, y, cell_size, cell_size)
            pygame.draw.rect(screen, blue, part_rect)

    def move_snake(self):
        """
        Function to move the snake
        """
        if eating():
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + Vector2(direction[0], direction[1]))
            self.body = body_copy[:]
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + Vector2(direction[0], direction[1]))
            self.body = body_copy[:]


class Apple:
    """
    This class represents the apples that the snake will eat
    """

    def __init__(self):
        self.randomize()

    def draw_apple(self):
        """
        Function to draw apples on the screen
        """
        apple_rect = pygame.Rect(self.pos.x * cell_size, self.pos.y * cell_size, cell_size, cell_size)
        if point % 5 == 0 and point != 0:
            screen.blit(apple_gold, apple_rect)
        else:
            screen.blit(apple_red, apple_rect)

    def randomize(self):
        """
        Function to randomize the position of the apples
        """
        self.x = random.randint(0, cell_column - 1)
        self.y = random.randint(0, cell_row - 1)
        self.pos = Vector2(self.x, self.y)


def eating():
    """
    This function checks if the snake's head is at the same position
    as the apple. If so, it updates the score, randomizes
    a new position for the apple and returns True.
    """
    global point
    if apple.pos == snake.body[0]:
        apple.randomize()
        while apple.pos in snake.body:
            apple.randomize()
        if point % 5 == 0 and point != 0:
            point = point + 2
        else:
            point = point + 1
        return True
    else:
        return False


def check_collision():
    """
    This function checks for collisions between the snake and either the walls
    or its own body. If a collision is detected, it calls the loosing function.
    """
    for part in snake.body[1:]:
        if snake.body[0] == part:
            loosing(1)
    if snake.body[0][0] < 0 or snake.body[0][1] < 0 or \
            snake.body[0][0] > cell_column - 1 or snake.body[0][1] > cell_row - 1:
        loosing(0)


def loosing(hit):
    """
    This function is called when the snake loses the game.
    It displays a message on the screen and waits for the player to press the "Ok" button
    """
    global click
    while True:

        screen.fill(green)
        draw_grass()
        myfont = pygame.font.Font('fonts/junegull.ttf', 70)
        if hit == 1:
            msg = myfont.render("OW! You bite yourself!", True, (255, 255, 255))
            msg_score = myfont.render(f"You scored {point * diff} points", True, (255, 255, 255))
            msg_box1 = msg.get_rect()
            msg_box1.center = (cell_column * cell_size / 2, 200)
            msg_box2 = msg_score.get_rect()
            msg_box2.center = (cell_column * cell_size / 2, 360)

        else:
            msg = myfont.render("UPS! You hit the wall!", True, (255, 255, 255))
            msg_score = myfont.render(f"You scored {point * diff} points", True, (255, 255, 255))
            msg_box1 = msg.get_rect()
            msg_box1.center = (cell_column * cell_size / 2, 200)
            msg_box2 = msg_score.get_rect()
            msg_box2.center = (cell_column * cell_size / 2, 360)

        screen.blit(msg, msg_box1)
        screen.blit(msg_score, msg_box2)

        mx, my = pygame.mouse.get_pos()

        back_button = pygame.Rect(cell_size * cell_column / 2 - 160, 800, 320, 70)
        color4 = (105, 190, 40)

        menu_font = pygame.font.Font('fonts/junegull.ttf', 60)
        leave = menu_font.render("Ok", True, (255, 255, 255))
        leave_box = leave.get_rect()
        leave_box.center = (cell_size * cell_column / 2, 800 + 35)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if back_button.collidepoint((mx, my)):
            color4 = (135, 190, 40)
            if click:
                main_menu()

        pygame.draw.rect(screen, color4, back_button)
        screen.blit(leave, leave_box)

        pygame.display.update()
        clock.tick(framerate)


def display_points():
    """
    This function displays the actual number of points in the top-right corner
    """
    myfont = pygame.font.Font('fonts/junegull.ttf', 38)
    msg = myfont.render(f"Points {point * diff}", True, (255, 255, 255))
    msg_box = msg.get_rect()
    msg_box.topright = (cell_column * cell_size - 10, 10)
    screen.blit(msg, msg_box)


def draw_grass():
    """
    This function draws the green grass background for the game screen.
    """
    y = 0
    while y < cell_row:
        if y % 2 == 0:
            x = 1
        else:
            x = 0
        while x < cell_column:
            pygame.draw.rect(screen, dark_green, (x * cell_size, y * cell_size, cell_size, cell_size))
            x = x + 2
        y = y + 1


def main_menu():
    """
    Function to display the main menu of the game
    """
    global click
    while True:

        screen.fill(green)
        draw_grass()
        myfont = pygame.font.Font('fonts/Bombing.ttf', 190)
        msg = myfont.render("Snake!", True, (255, 255, 255))
        msg_box = msg.get_rect()
        msg_box.center = (cell_size * cell_column / 2, 100)
        screen.blit(msg, msg_box)

        mx, my = pygame.mouse.get_pos()

        height = 70
        play_button = pygame.Rect(cell_size * cell_column / 2 - 160, 260, 320, height)
        leaderboard_button = pygame.Rect(cell_size * cell_column / 2 - 160, 340, 320, height)
        about_button = pygame.Rect(cell_size * cell_column / 2 - 160, 420, 320, height)
        quit_button = pygame.Rect(cell_size * cell_column / 2 - 160, 500, 320, height)
        color1 = (105, 190, 40)
        color2 = (105, 190, 40)
        color3 = (105, 190, 40)
        color4 = (105, 190, 40)

        menu_font = pygame.font.Font('fonts/junegull.ttf', 60)
        playb = menu_font.render("Play", True, (255, 255, 255))
        playb_box = playb.get_rect()
        playb_box.center = (cell_size * cell_column / 2, 260 + height / 2)
        autorb = menu_font.render("Autor", True, (255, 255, 255))
        autorb_box = autorb.get_rect()
        autorb_box.center = (cell_size * cell_column / 2, 340 + height / 2)
        aboutb = menu_font.render("About", True, (255, 255, 255))
        aboutb_box = aboutb.get_rect()
        aboutb_box.center = (cell_size * cell_column / 2, 420 + height / 2)
        back = menu_font.render("Quit", True, (255, 255, 255))
        back_box = back.get_rect()
        back_box.center = (cell_size * cell_column / 2, 500 + height / 2)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if play_button.collidepoint((mx, my)):
            color1 = (135, 190, 40)
            if click:
                play()
        if leaderboard_button.collidepoint((mx, my)):
            color2 = (135, 190, 40)
            if click:
                autor()
        if about_button.collidepoint((mx, my)):
            color3 = (135, 190, 40)
            if click:
                about()
        if quit_button.collidepoint((mx, my)):
            color4 = (135, 190, 40)
            if click:
                pygame.quit()
                sys.exit()

        pygame.draw.rect(screen, color1, play_button)
        pygame.draw.rect(screen, color2, leaderboard_button)
        pygame.draw.rect(screen, color3, about_button)
        pygame.draw.rect(screen, color4, quit_button)
        screen.blit(playb, playb_box)
        screen.blit(autorb, autorb_box)
        screen.blit(aboutb, aboutb_box)
        screen.blit(back, back_box)

        pygame.display.update()
        clock.tick(framerate)


def play():
    """
    Function to display window with option of choosing game difficulty
    """
    global click
    global diff
    global speed
    while True:

        screen.fill(green)
        draw_grass()
        myfont = pygame.font.Font('fonts/junegull.ttf', 100)
        msg = myfont.render("Choose Difficulty", True, (255, 255, 255))
        msg_box = msg.get_rect()
        msg_box.center = (cell_size * cell_column / 2, 100)
        screen.blit(msg, msg_box)

        mx, my = pygame.mouse.get_pos()

        height = 70
        easy_button = pygame.Rect(cell_size * cell_column / 2 - 160, 260, 320, height)
        medium_button = pygame.Rect(cell_size * cell_column / 2 - 160, 340, 320, height)
        hard_button = pygame.Rect(cell_size * cell_column / 2 - 160, 420, 320, height)
        back_button = pygame.Rect(cell_size * cell_column / 2 - 160, 500, 320, height)
        color1 = (105, 190, 40)
        color2 = (105, 190, 40)
        color3 = (105, 190, 40)
        color4 = (105, 190, 40)

        menu_font = pygame.font.Font('fonts/junegull.ttf', 60)
        easy = menu_font.render("Easy", True, (255, 255, 255))
        easy_box = easy.get_rect()
        easy_box.center = (cell_size * cell_column / 2, 260 + height / 2)
        medium = menu_font.render("Medium", True, (255, 255, 255))
        medium_box = medium.get_rect()
        medium_box.center = (cell_size * cell_column / 2, 340 + height / 2)
        hard = menu_font.render("Hard", True, (255, 255, 255))
        hard_box = hard.get_rect()
        hard_box.center = (cell_size * cell_column / 2, 420 + height / 2)
        leave = menu_font.render("Back", True, (255, 255, 255))
        leave_box = leave.get_rect()
        leave_box.center = (cell_size * cell_column / 2, 500 + height / 2)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if easy_button.collidepoint((mx, my)):
            color1 = (135, 190, 40)
            if click:
                speed = 170
                diff = 1
                game()
        if medium_button.collidepoint((mx, my)):
            color2 = (135, 190, 40)
            if click:
                speed = 110
                diff = 2
                game()
        if hard_button.collidepoint((mx, my)):
            color3 = (135, 190, 40)
            if click:
                speed = 60
                diff = 5
                game()
        if back_button.collidepoint((mx, my)):
            color4 = (135, 190, 40)
            if click:
                main_menu()

        pygame.draw.rect(screen, color1, easy_button)
        pygame.draw.rect(screen, color2, medium_button)
        pygame.draw.rect(screen, color3, hard_button)
        pygame.draw.rect(screen, color4, back_button)
        screen.blit(easy, easy_box)
        screen.blit(medium, medium_box)
        screen.blit(hard, hard_box)
        screen.blit(leave, leave_box)

        pygame.display.update()
        clock.tick(framerate)


def about():
    """
    Function displaying game rules
    """
    global click
    while True:

        screen.fill(green)
        draw_grass()
        myfont = pygame.font.Font('fonts/junegull.ttf', 100)
        msg = myfont.render("Game Rules", True, (255, 255, 255))
        msg_box = msg.get_rect()
        msg_box.center = (cell_size * cell_column / 2, 100)
        screen.blit(msg, msg_box)

        text = pygame.image.load('graphics/rules.png').convert_alpha()
        text = pygame.transform.scale(text, (900, 450))
        text_rect = text.get_rect()
        text_rect.center = (cell_size * cell_column / 2 + 40, 400)
        screen.blit(text, text_rect)

        mx, my = pygame.mouse.get_pos()

        back_button = pygame.Rect(cell_size * cell_column / 2 - 160, 800, 320, 70)
        color4 = (105, 190, 40)

        menu_font = pygame.font.Font('fonts/junegull.ttf', 60)
        leave = menu_font.render("Back", True, (255, 255, 255))
        leave_box = leave.get_rect()
        leave_box.center = (cell_size * cell_column / 2, 800 + 35)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if back_button.collidepoint((mx, my)):
            color4 = (135, 190, 40)
            if click:
                main_menu()

        pygame.draw.rect(screen, color4, back_button)
        screen.blit(leave, leave_box)

        pygame.display.update()
        clock.tick(framerate)


def autor():
    """
    Function displaying information about the autor
    """
    global click
    while True:

        screen.fill(green)
        draw_grass()
        myfont = pygame.font.Font('fonts/junegull.ttf', 100)
        msg = myfont.render("About Autor", True, (255, 255, 255))
        msg_box = msg.get_rect()
        msg_box.center = (cell_size * cell_column / 2, 100)
        screen.blit(msg, msg_box)
        text = pygame.image.load('graphics/autor.png').convert_alpha()
        text = pygame.transform.scale(text, (700, 700))
        text_rect = text.get_rect()
        text_rect.center = (cell_size * cell_column / 2, 400)
        screen.blit(text, text_rect)

        mx, my = pygame.mouse.get_pos()

        back_button = pygame.Rect(cell_size * cell_column / 2 - 160, 800, 320, 70)
        color4 = (105, 190, 40)

        menu_font = pygame.font.Font('fonts/junegull.ttf', 60)
        leave = menu_font.render("Back", True, (255, 255, 255))
        leave_box = leave.get_rect()
        leave_box.center = (cell_size * cell_column / 2, 800 + 35)

        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if back_button.collidepoint((mx, my)):
            color4 = (135, 190, 40)
            if click:
                main_menu()

        pygame.draw.rect(screen, color4, back_button)
        screen.blit(leave, leave_box)

        pygame.display.update()
        clock.tick(framerate)


def game():
    """
    Function containing main logic of the game
    """
    global direction
    global point
    global snake
    snake = Snake()
    point = 0
    direction = [1, 0]
    pygame.time.set_timer(SCREEN_UPDATE, speed)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SCREEN_UPDATE:
                snake.move_snake()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if direction[0] != -1:
                        direction = [1, 0]
                if event.key == pygame.K_LEFT:
                    if direction[0] != 1:
                        direction = [-1, 0]
                if event.key == pygame.K_UP:
                    if direction[1] != 1:
                        direction = [0, -1]
                if event.key == pygame.K_DOWN:
                    if direction[1] != -1:
                        direction = [0, 1]

        screen.fill(green)
        draw_grass()
        apple.draw_apple()
        snake.draw_snake()
        display_points()
        check_collision()
        pygame.display.update()
        clock.tick(framerate)


if __name__ == "__main__":
    point = 0
    diff = 1
    direction = [1, 0]
    speed = 170
    cell_size = 40
    cell_row = 23
    cell_column = 20
    framerate = 60
    window_size = (cell_size * cell_column, cell_size * cell_row)
    click = False

    green = (175, 215, 70)
    dark_green = (185, 225, 80)
    red = (255, 0, 0)
    blue = (10, 10, 200)

    pygame.init()
    screen = pygame.display.set_mode(window_size)
    clock = pygame.time.Clock()

    apple_red = pygame.image.load('graphics/apple_red.png').convert_alpha()
    apple_red = pygame.transform.scale(apple_red, (cell_size, cell_size))
    apple_gold = pygame.image.load('graphics/apple_goldv2.png').convert_alpha()
    apple_gold = pygame.transform.scale(apple_gold, (cell_size, cell_size))

    apple = Apple()
    snake = Snake()

    SCREEN_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SCREEN_UPDATE, speed)

    main_menu()
