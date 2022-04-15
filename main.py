import pygame

# helps us find the path to files
import os

# The coordinates in pygame: top left corner is 0,0.

WIDTH, HEIGHT = 900, 500

# determining the width and height of the window display
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

BORDER = pygame.Rect(WIDTH//2-5,0,10,HEIGHT)

# setting a caption on a window
pygame.display.set_caption("First game")

WHITE = (255, 255, 255)
BLACK = (0,0,0)
RED = (255,0,0)
YELLOW = (255,255,0)

# determining the speed of the game. most of the games run with 60
FPS = 60
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
VEL = 5  # setting the velocity of the object moving
BULLET_VEL = 7  #  speed of the bullet
MAX_BULLETS = 3

YELLOW_SPACE_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_yellow.png"))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale
                                           (YELLOW_SPACE_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACE_IMAGE = pygame.image.load(os.path.join("Assets", "spaceship_red.png"))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACE_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)),
                                        270)

YELLOW_HIT = pygame.USEREVENT+1
RED_HIT = pygame.USEREVENT+2


def draw_window(red, yellow,red_bullets,yellow_bullets):
    WIN.fill(WHITE)  # background color setting
    pygame.draw.rect(WIN, BLACK, BORDER) # rectangle in the middle
    WIN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))  # setting the yellow spaceship image at x300 y100
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN,RED,bullet)

    for bullet in yellow_bullets:
        pygame.draw.rect(WIN,YELLOW,bullet)

    pygame.display.update()  # we need to update the display to show the change


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # a means left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # d means right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # w means up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT-15:  # s means down
        yellow.y += VEL


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT-15:
        red.y += VEL


def handle_bullets(yellow_bullets,red_bullets,yellow,red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): #  this colliderect only works when both red and bullet are objects
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet): #  this colliderect only works when both red and bullet are objects
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)

def main():
    red = pygame.Rect(700, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    yellow = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    clock = pygame.time.Clock()
    run = True
    # as long as run is true, the game will keep going.
    while run:
        # this makes sure that this while loop runs 60 times in 1 second.
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x+yellow.width,yellow.y+yellow.height//2 - 2,10,5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets,red_bullets,yellow,red)


        draw_window(red, yellow,red_bullets,yellow_bullets)

    pygame.quit()


if __name__ == "__main__":
    main()
