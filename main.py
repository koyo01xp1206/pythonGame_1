import pygame
import random

# helps us find the path to files
import os

pygame.font.init()
pygame.mixer.init()  # sound system of pygame
# The coordinates in pygame: top left corner is 0,0.

WIDTH, HEIGHT = 900, 500

# determining the width and height of the window display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

#  BGM random selection
number = random.randrange(1, 4)
B1 = False
B2 = False
B3 = False
if number == 1:
    B1 = True
if number == 2:
    B2 = True
if number == 3:
    B3 = True

# sound systems:
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))
WINNER_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'WINNING_SOUND+.mp3'))
POWER_UP_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'power_up_sound.mp3'))
BGM1 = pygame.mixer.Sound(os.path.join('Assets', 'SPACESHIP_BGM1+.mp3'))
BGM2 = pygame.mixer.Sound(os.path.join('Assets', 'SPACESHIP_BGM2+.mp3'))
BGM3 = pygame.mixer.Sound(os.path.join('Assets', 'SPACESHIP_BGM3+.mp3'))

# Font display
HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)
CHANCE_FONT = pygame.font.SysFont('comicsans', 100)

# setting a caption on a window
pygame.display.set_caption("First game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# determining the speed of the game. most of the games run with 60
FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
VEL = 5  # setting the velocity of the object moving
BULLET_VEL = 7  # speed of the bullet
FAST_BULLET_VEL = BULLET_VEL * 2
MAX_BULLETS = 5

BULLET_SPECIAL_VEL = 15

# ITEM_VEL = 1
# POWER_UP_WIDTH, POWER_UP_HEIGHT = 50, 50

#  images
YELLOW_SPACE_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale
                                           (YELLOW_SPACE_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACE_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACE_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
                                        270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("Assets", "space.png")), (WIDTH, HEIGHT))

YELLOW_LIFE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale
                                                (YELLOW_SPACE_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_LIFE_SPACESHIP = pygame.transform.rotate(
    pygame.transform.scale(RED_SPACE_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
    270)

BOOM_IMG = pygame.image.load(os.path.join("Assets", "boomIMG.png"))
BOOM_IMAGE = pygame.transform.scale(BOOM_IMG, (SPACESHIP_WIDTH + 20, SPACESHIP_HEIGHT + 20))

# POWER_UP_IMAGE = pygame.image.load(os.path.join("Assets", "POWER_UP.png"))
# POWER_UP = pygame.transform.scale(POWER_UP_IMAGE, (POWER_UP_WIDTH, POWER_UP_HEIGHT))

# Hitting situation
YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2
POWER_UP_YELLOW_HIT = pygame.USEREVENT + 3
POWER_UP_RED_HIT = pygame.USEREVENT + 4


def draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)  # rectangle in the middle
    red_health_text = HEALTH_FONT.render("    * " + str(red_health), 1, WHITE)
    yellow_health_text = HEALTH_FONT.render("   * " + str(yellow_health), 1, WHITE)

    WIN.blit(red_health_text, (WIDTH - red_health_text.get_width() - 10, 10))
    WIN.blit(yellow_health_text, (10, 10))

    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  # setting the yellow spaceship image at x300 y100
    WIN.blit(RED_SPACESHIP, (red.x, red.y))

    WIN.blit(YELLOW_LIFE_SPACESHIP, (0, 10))
    WIN.blit(RED_LIFE_SPACESHIP, (WIDTH - red_health_text.get_width() - 10, 10))

    # WIN.blit(POWER_UP, (power_yellow.x, power_yellow.y))
    # WIN.blit(POWER_UP, (power_red.x, power_red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    # for item in power_yellow_list:
    # pygame.draw.rect(WIN, power_yellow, item)

    # for item in power_red_list:
    # pygame.draw.rect(WIN, power_red, item)

    pygame.display.update()  # we need to update the display to show the change


def yellow_handle_movement(keys_pressed, yellow, yellow_health):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # a means left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # d means right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # w means up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT - 15:  # s means down
        yellow.y += VEL


def red_handle_movement(keys_pressed, red, red_health):
    # if red_health < 3:
    #     VEL = 15
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT - 15:
        red.y += VEL


def handle_bullets(yellow_bullets, red_bullets, yellow, red, yellow_health, red_health):
    for bullet in yellow_bullets:
        if yellow_health < 4:
            bullet.x += FAST_BULLET_VEL
        if yellow_health >= 4:
            bullet.x += BULLET_VEL

        if red.colliderect(bullet):  # this colliderect only works when both red and bullet are objects
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        if red_health < 4:
            bullet.x -= FAST_BULLET_VEL
        if red_health >= 4:
            bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):  # this colliderect only works when both red and bullet are objects
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2 - draw_text.get_height() / 2))
    pygame.display.update()


def draw_chance_yellow(text):
    draw_text = CHANCE_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text,(WIDTH / 4 - draw_text.get_width() / 2, HEIGHT / 4 - draw_text.get_height() / 2))
    pygame.display.update()


def draw_chance_red(text):
    draw_text = CHANCE_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text,(WIDTH * 0.75 - draw_text.get_width() / 2, HEIGHT / 4 - draw_text.get_height() / 2))
    pygame.display.update()

# def handle_power_up(power_yellow, power_red, yellow, red, power_yellow_list, power_red_list):
#     for item in power_red_list:
#         item.y += ITEM_VEL
#         if red.colliderect(power_red):
#             pygame.event.post(pygame.event.Event(POWER_UP_RED_HIT))
#             power_red.remove(item)
#
#     for item in power_yellow_list:
#         item.y += ITEM_VEL
#         if yellow.colliderect(power_yellow):
#             pygame.event.post(pygame.event.Event(POWER_UP_YELLOW_HIT))
#             power_yellow.remove(item)
def boom_red(red):
    WIN.blit(BOOM_IMAGE, (red.x-10, red.y))
    pygame.display.update()
    pygame.time.delay(400)


def boom_yellow(yellow):
    WIN.blit(BOOM_IMAGE, (yellow.x-10, yellow.y))
    pygame.display.update()
    pygame.time.delay(400)


def power_up(power):
    MAX_BULLETS = 100

    pygame.display.update()


def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    # power_red = pygame.Rect(700, 100, POWER_UP_WIDTH, POWER_UP_HEIGHT)
    # power_yellow = pygame.Rect(100, 100, POWER_UP_WIDTH, POWER_UP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    red_health = 10
    yellow_health = 10

    power_red_list = []
    power_yellow_list = []

    clock = pygame.time.Clock()
    if B1 == True:
        BGM1.play()
    if B2 == True:
        BGM2.play()
    if B3 == True:
        BGM3.play()

    chance_bool_red = True
    chance_bool_yellow = True


    run = True
    # as long as run is true, the game will keep going.
    while run:
        # this makes sure that this while loop runs 60 times in 1 second.
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
                boom_red(red)

            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()
                boom_yellow(yellow)

            if event.type == POWER_UP_YELLOW_HIT:
                POWER_UP_SOUND.play()

            if event.type == POWER_UP_RED_HIT:
                POWER_UP_SOUND.play()

        winner_text = ""

        if red_health <= 0:
            winner_text = "Yellow wins!"

        if yellow_health <= 0:
            winner_text = "Red wins!"

        if winner_text != "":
            draw_winner(winner_text)  # someone has won!
            WINNER_SOUND.play()
            pygame.time.delay(4000)  # 5 seconds of pause in the game
            break  # quit the game
        if red_health == 3 and chance_bool_red == True:
            draw_chance_red("CHANCE!")
            pygame.time.delay(300)
            chance_bool_red = False

        if yellow_health == 3 and chance_bool_yellow == True:
            draw_chance_yellow("CHANCE!")
            pygame.time.delay(300)
            chance_bool_yellow = False

        keys_pressed = pygame.key.get_pressed()

        yellow_handle_movement(keys_pressed, yellow, yellow_health)
        red_handle_movement(keys_pressed, red, red_health)

        handle_bullets(yellow_bullets, red_bullets, yellow, red, yellow_health, red_health)
        # handle_power_up(power_yellow, power_red, yellow, red)

        draw_window(red, yellow, red_bullets, yellow_bullets, red_health, yellow_health)

    # main()
    pygame.quit()


if __name__ == "__main__":
    main()
