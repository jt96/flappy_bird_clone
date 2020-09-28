# Flappy Bird Clone in Python 3
# By Jackie Trenh

import pygame
import random

# setting up the game
pygame.init()
win = pygame.display.set_mode((800, 600))
background = pygame.image.load('background.jpg')
pygame.display.set_caption('Flappy Bird Clone')
icon = pygame.image.load('macaw.png')
pygame.display.set_icon(icon)

# flappy bird
bird_img = pygame.image.load('flying_macaw.png')
bird_x = 125
bird_y = 250
bird_y_change = 0.82
bird_width = 64

# pipes
# separate lists for top and bottom pipes
bot_pipes_img = []
top_pipes_img = []
pipes_x_start = [400, 710, 1020]
pipes_x = pipes_x_start[:]
bot_pipes_y = []
top_pipes_y = []
pipes_x_dist = 310
pipes_y_dist = 705
pipe_width = 124
pipe_height = 480
num_of_pipes = 3

for i in range(num_of_pipes):
    bot_pipes_img.append(pygame.image.load('pipe.png').convert_alpha())
    top_pipes_img.append(pygame.image.load('down_pipe.png').convert_alpha())
    bot_pipes_y.append(random.randint(275, 540))
    top_pipes_y.append(bot_pipes_y[i] - pipes_y_dist)


# score
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)
text_x = 10
text_y = 10

# paused
paused_font = pygame.font.Font('freesansbold.ttf', 64)

# game over
game_over_font = pygame.font.Font('freesansbold.ttf', 64)


def bird(x, y):
    win.blit(bird_img, (x, y))


def bot_pipe(x, y, i):
    win.blit(bot_pipes_img[i], (x, y))


def top_pipe(x, y, i):
    win.blit(top_pipes_img[i], (x, y))


# check for bird collision with pipes
def is_collision(bird_x, bird_y, pipes_x, bot_pipes_y, top_pipes_y, i):
    return ((bot_pipes_y[i] <= bird_y + bird_width or bird_y <= top_pipes_y[i] +
             pipe_height) and bird_x >= pipes_x[i] and bird_x <= pipes_x[i] + pipe_width)


# check if scored
def is_scored(pipes_x):
    global bird_width
    return pipes_x + bird_width == bird_x


def show_score(x, y):
    score = font.render('Score: ' + str(score_value), True, (255, 255, 255))
    win.blit(score, (x, y))


def pause_game():
    pause = paused_font.render('PAUSED', True, (255, 255, 255))
    win.blit(pause, (250, 250))


def game_over_text():
    over = game_over_font.render('GAME OVER', True, (255, 255, 255))
    win.blit(over, (200, 250))
    restart = game_over_font.render(
        'Press R to restart', True, (255, 255, 255))
    win.blit(restart, (125, 325))
    quit = game_over_font.render('Press Q to quit', True, (255, 255, 255))
    win.blit(quit, (140, 400))


running = True
paused = False
game_over = False
while running:
    win.blit(background, (0, 0))
    if bird_y > 600 or bird_y + bird_width < 0:
        game_over = True
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_SPACE and not paused and not game_over:
                bird_y -= 95
            if event.key == pygame.K_p:
                if paused:
                    paused = False
                else:
                    paused = True
            if event.key == pygame.K_r:
                game_over = False
                paused = False
                score_value = 0
                pipes_x = pipes_x_start[:]
                bot_pipes_y = [random.randint(275, 540), random.randint(
                               275, 540), random.randint(275, 540)]
                top_pipes_y = [bot_pipes_y[0] - pipes_y_dist,
                               bot_pipes_y[1] - pipes_y_dist, bot_pipes_y[2] - pipes_y_dist]
                bird_y = 250

    bird(bird_x, bird_y)
    for i in range(num_of_pipes):
        if pipes_x[i] <= -pipe_width:
            bot_pipes_y[i] = random.randint(275, 540)
            top_pipes_y[i] = bot_pipes_y[i] - pipes_y_dist
            if i == 0:
                pipes_x[i] = pipes_x[2] + pipes_x_dist
            elif i == 1:
                pipes_x[i] = pipes_x[0] + pipes_x_dist
            else:
                pipes_x[i] = pipes_x[1] + pipes_x_dist
        bot_pipe(pipes_x[i], bot_pipes_y[i], i)
        top_pipe(pipes_x[i], top_pipes_y[i], i)
        scored = is_scored(pipes_x[i])
        if scored:
            score_value += 1
        collision = is_collision(
            bird_x, bird_y, pipes_x, bot_pipes_y, top_pipes_y, i)
        if collision:
            game_over = True

    if game_over:
        game_over_text()
    elif paused:
        pause_game()
    else:
        for i in range(num_of_pipes):
            pipes_x[i] -= 0.5
        bird_y += bird_y_change

    show_score(text_x, text_y)
    pygame.display.update()
