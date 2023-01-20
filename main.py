import random
import sys
import pygame
from pygame.locals import *


def rand_pipe():
    pipe_height = pipe[0].get_height()
    between = height / 4.5
    lower_y = between + random.randrange(0, int(height - base.get_height() - 1.2 * between))
    upper_y = pipe_height - lower_y + between
    pipe_x = width + 10
    return [{'x': pipe_x, 'y': -upper_y},
            {'x': pipe_x, 'y': lower_y}]


# окно выбора сложности
def start_windows():
    standart_button = pygame.Rect(5, 165, 90, 40)
    fast_button = pygame.Rect(170, 165, 90, 40)
    font = pygame.font.SysFont(None, 30)
    lvl1 = 0
    lvl2 = 1
    screen.blit(background, (0, 0))
    screen.blit(difficult, (0, 0))
    standart = font.render('Standart speed', True, pygame.Color('white'))
    screen.blit(standart, (5, 150))
    speed = font.render('Fast speed', True, pygame.Color('white'))
    screen.blit(speed, (170, 150))
    pygame.display.update()
    FPSCLOCK.tick(FPS)
    while True:
        for event in pygame.event.get():
            if event.type == 'QUIT' or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(event.pos)
                if standart_button[0] < pygame.mouse.get_pos()[0] < (standart_button[0] + standart_button[2]):
                    if standart_button[1] > pygame.mouse.get_pos()[1] > (standart_button[1] - standart_button[3]):
                        start_game(lvl1)
                if fast_button[0] < pygame.mouse.get_pos()[0] < (fast_button[0] + fast_button[2]):
                    if fast_button[1] > pygame.mouse.get_pos()[1] > (fast_button[1] - fast_button[3]):
                        start_game(lvl2)


def start_game(lvl):
    base_x = 0

    # координаты play_button
    play_button = pygame.Rect(79, 363, 128, 135)

    font = pygame.font.SysFont(None, 50)

    while True:
        for event in pygame.event.get():
            if event.type == 'QUIT' or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            elif event.type == KEYDOWN and event.key == K_SPACE:
                return

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button[0] < pygame.mouse.get_pos()[0] < (play_button[0] + play_button[2]):
                    if play_button[1] > pygame.mouse.get_pos()[1] > (play_button[1] - play_button[3]):
                        if lvl == 0:
                            game()
                        if lvl == 1:
                            game2()

        # 23 строка - ставит курсор
        # остальные - проверка где находится и ставят курсор руки
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        if play_button[0] < pygame.mouse.get_pos()[0] < (play_button[0] + play_button[2]):
            if play_button[1] > pygame.mouse.get_pos()[1] > (play_button[1] - play_button[3]):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)

        screen.blit(background, (0, 0))
        screen.blit(start_window, (0, 0))
        screen.blit(base, (base_x, ground))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def collision(bird_x, bird_y, upper_pipes, lower_pipes):
    if bird_y > ground or bird_y < 0:
        hit.play()

        game_over()

    for p in upper_pipes:
        pipe_height = pipe[0].get_height()
        if bird_y < pipe_height + p['y'] and abs(bird_x - p['x']) < pipe[0].get_width() - 20:
            hit.play()

            game_over()

    for p in lower_pipes:
        if (bird_y + bird.get_height() > p['y']) and abs(bird_x - p['x']) < pipe[0].get_width() - 20:
            hit.play()

            game_over()

    return False


def game_over():
    global record

    if int(record[0]) < score:
        with open('record.txt', 'w') as file:
            file.write(f'{score} {record[1]}')
        record = [score, record[1]]

    pygame.display.set_caption('Flappy Bird')
    over = pygame.image.load('data/sprites/game_over.png').convert_alpha()
    retry = pygame.image.load('data/sprites/retry.png').convert_alpha()
    home = pygame.image.load('data/sprites/home.png').convert_alpha()
    screen.blit(background, (0, 0))
    screen.blit(base, (0, ground))
    screen.blit(over, (0, 0))
    screen.blit(retry, (30, 220))
    screen.blit(home, (30, 280))
    font = pygame.font.SysFont(None, 25)
    last_rec = font.render(f'Your last record: {record[0]}', True, pygame.Color('black'))
    screen.blit(last_rec, (5, 10))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_SPACE:

                game()

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if 30 < pygame.mouse.get_pos()[0] < 30 + retry.get_width():
                if 220 < pygame.mouse.get_pos()[1] < 220 + retry.get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        game()
            if 30 < pygame.mouse.get_pos()[0] < 30 + home.get_width():
                if 280 < pygame.mouse.get_pos()[1] < 280 + home.get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        start_windows()


def game():
    global score
    score = 0
    bird_x = width // 5
    bird_y = height // 2
    base_x = 0

    pipe1, pipe2 = rand_pipe(), rand_pipe()
    upper_pipes = [{'x': width + 200, 'y': pipe1[0]['y']}, {'x': width + 200 + width / 2, 'y': pipe2[0]['y']}]
    lower_pipes = [{'x': width + 200, 'y': pipe1[1]['y']}, {'x': width + 200 + width / 2, 'y': pipe2[1]['y']}]

    pipe_vel_x = -4
    bird_vel_y = -9
    bird_max_vel_y = 10
    bird_min_vel_y = -8
    bird_acc_y = 1

    bird_flap = -8
    bird_flapped = False
    
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if bird_y > 0:
                    bird_vel_y = bird_flap
                    bird_flapped = True
                    wing.play()

        crash_test = collision(bird_x, bird_y, upper_pipes, lower_pipes)
        if crash_test:
            return

            # очки
        bird_mid_pos = bird_x + bird.get_height() / 2
        for n_pipe in upper_pipes:
            pipe_mid_pos = n_pipe['x'] + bird.get_height() / 2
            if pipe_mid_pos <= bird_mid_pos < pipe_mid_pos + 4:
                score += 1
                point.play()

        if bird_vel_y < bird_max_vel_y and not bird_flapped:
            bird_vel_y += bird_acc_y

        if bird_flapped:
            bird_flapped = False
        bird_height = bird.get_height()
        bird_y = bird_y + min(ground - bird_y - bird_height, bird_vel_y)

        # перемещение влево
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            upper_pipe['x'] += pipe_vel_x
            lower_pipe['x'] += pipe_vel_x

        # добавляем новые
        if 0 < upper_pipes[0]['x'] < 5:
            new_pipe = rand_pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])

        # удаление труб с экрана
        if upper_pipes[0]['x'] < -pipe[0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        screen.blit(background, (0, 0))
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            screen.blit(pipe[0], (upper_pipe['x'], upper_pipe['y']))
            screen.blit(pipe[1], (lower_pipe['x'], lower_pipe['y']))

        screen.blit(base, (base_x, ground))
        screen.blit(bird, (bird_x, bird_y))

        digits = [int(x) for x in list(str(score))]
        width_digit = 0

        for digit in digits:
            width_digit += numbers[digit].get_width()
        between_x = (width - width_digit) / 2

        for digit in digits:
            screen.blit(numbers[digit], (between_x, height * 0.12))
            between_x += numbers[digit].get_width()
        font = pygame.font.SysFont(None, 25)
        last_rec = font.render(f'Your last record: {record[0]}', True, pygame.Color('black'))
        screen.blit(last_rec, (5, 10))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def collision2(bird_x, bird_y, upper_pipes, lower_pipes):
    if bird_y > ground or bird_y < 0:
        hit.play()

        game_over2()

    for p in upper_pipes:
        pipe_height = pipe[0].get_height()
        if bird_y < pipe_height + p['y'] and abs(bird_x - p['x']) < pipe[0].get_width() - 20:
            hit.play()

            game_over2()

    for p in lower_pipes:
        if (bird_y + bird.get_height() > p['y']) and abs(bird_x - p['x']) < pipe[0].get_width() - 20:
            hit.play()

            game_over2()

    return False


def game_over2():
    global record

    if int(record[1]) < score_2:
        with open('record.txt', 'w') as file:
            file.write(f'{record[0]} {score_2}')
        record = [record[0], score_2]

    over_screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Flappy Bird')
    over = pygame.image.load('data/sprites/game_over.png').convert_alpha()
    retry = pygame.image.load('data/sprites/retry.png').convert_alpha()
    home = pygame.image.load('data/sprites/home.png').convert_alpha()
    screen.blit(background, (0, 0))
    screen.blit(base, (0, ground))
    screen.blit(over, (0, 0))
    screen.blit(retry, (30, 220))
    screen.blit(home, (30, 280))
    font = pygame.font.SysFont(None, 25)
    last_rec = font.render(f'Your last record: {record[1]}', True, pygame.Color('black'))
    screen.blit(last_rec, (5, 10))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and event.key == K_SPACE:

                game2()

            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if 30 < pygame.mouse.get_pos()[0] < 30 + retry.get_width():
                if 220 < pygame.mouse.get_pos()[1] < 220 + retry.get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        game2()
            if 30 < pygame.mouse.get_pos()[0] < 30 + home.get_width():
                if 280 < pygame.mouse.get_pos()[1] < 280 + home.get_height():
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                        start_windows()


# 2 уровень сложности
def game2():
    global score_2
    score_2 = 0
    bird_x = width // 5
    bird_y = height // 2
    base_x = 0

    pipe1, pipe2 = rand_pipe(), rand_pipe()
    upper_pipes = [{'x': width + 200, 'y': pipe1[0]['y']}, {'x': width + 200 + width / 2, 'y': pipe2[0]['y']}]
    lower_pipes = [{'x': width + 200, 'y': pipe1[1]['y']}, {'x': width + 200 + width / 2, 'y': pipe2[1]['y']}]

    pipe_vel_x = -7
    bird_vel_y = -9
    bird_max_vel_y = 10
    bird_min_vel_y = -8
    bird_acc_y = 1

    bird_flap = -8
    bird_flapped = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == MOUSEBUTTONDOWN:
                if bird_y > 0:
                    bird_vel_y = bird_flap
                    bird_flapped = True
                    wing.play()

        crash_test = collision2(bird_x, bird_y, upper_pipes, lower_pipes)
        if crash_test:
            return

            # очки
        bird_mid_pos = bird_x + bird.get_height() / 2
        for n_pipe in upper_pipes:
            pipe_mid_pos = n_pipe['x'] + bird.get_height() / 2
            if pipe_mid_pos <= bird_mid_pos < pipe_mid_pos + 4:
                score_2 += 1
                point.play()

        if bird_vel_y < bird_max_vel_y and not bird_flapped:
            bird_vel_y += bird_acc_y

        if bird_flapped:
            bird_flapped = False
        bird_height = bird.get_height()
        bird_y = bird_y + min(ground - bird_y - bird_height, bird_vel_y)

        # перемещение влево
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            upper_pipe['x'] += pipe_vel_x
            lower_pipe['x'] += pipe_vel_x

        # добавляем новые
        if 0 < upper_pipes[0]['x'] < 7:
            new_pipe = rand_pipe()
            upper_pipes.append(new_pipe[0])
            lower_pipes.append(new_pipe[1])

        # удаление труб с экрана
        if upper_pipes[0]['x'] < -pipe[0].get_width():
            upper_pipes.pop(0)
            lower_pipes.pop(0)

        screen.blit(background, (0, 0))
        for upper_pipe, lower_pipe in zip(upper_pipes, lower_pipes):
            screen.blit(pipe[0], (upper_pipe['x'], upper_pipe['y']))
            screen.blit(pipe[1], (lower_pipe['x'], lower_pipe['y']))

        screen.blit(base, (base_x, ground))
        screen.blit(bird, (bird_x, bird_y))

        digits = [int(x) for x in list(str(score_2))]
        width_digit = 0

        for digit in digits:
            width_digit += numbers[digit].get_width()
        between_x = (width - width_digit) / 2

        for digit in digits:
            screen.blit(numbers[digit], (between_x, height * 0.12))
            between_x += numbers[digit].get_width()
        font = pygame.font.SysFont(None, 25)
        last_rec = font.render(f'Your last record: {record[1]}', True, pygame.Color('black'))
        screen.blit(last_rec, (5, 10))
        pygame.display.update()
        FPSCLOCK.tick(FPS)


FPS = 30
width, height = 289, 511
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Flappy Bird')
ground = height * 0.8
FPSCLOCK = pygame.time.Clock()

pygame.init()
numbers = (pygame.image.load('data/sprites/0.png').convert_alpha(),
           pygame.image.load('data/sprites/1.png').convert_alpha(),
           pygame.image.load('data/sprites/2.png').convert_alpha(),
           pygame.image.load('data/sprites/3.png').convert_alpha(),
           pygame.image.load('data/sprites/4.png').convert_alpha(),
           pygame.image.load('data/sprites/5.png').convert_alpha(),
           pygame.image.load('data/sprites/6.png').convert_alpha(),
           pygame.image.load('data/sprites/7.png').convert_alpha(),
           pygame.image.load('data/sprites/8.png').convert_alpha(),
           pygame.image.load('data/sprites/9.png').convert_alpha()
           )

background = pygame.image.load('data/sprites/background.png').convert_alpha()
start_window = pygame.image.load('data/sprites/startwindow.png').convert_alpha()
bird = pygame.image.load('data/sprites/bird.png').convert_alpha()
pipe = (pygame.transform.rotate(pygame.image.load('data/sprites/pipe.png').convert_alpha(), 180),
        pygame.image.load('data/sprites/pipe.png').convert_alpha())
base = pygame.image.load('data/sprites/base.png').convert_alpha()
difficult = pygame.image.load('data/sprites/difficult.png').convert_alpha()

die = pygame.mixer.Sound('data/audio/sfx_die.ogg')
hit = pygame.mixer.Sound('data/audio/sfx_hit.ogg')
swoosh = pygame.mixer.Sound('data/audio/sfx_swooshing.ogg')
point = pygame.mixer.Sound('data/audio/sfx_point.ogg')
wing = pygame.mixer.Sound('data/audio/sfx_wing.ogg')

score_2 = 0
score = 0

with open('record.txt', 'r') as my_file:
    record = my_file.read().split()

while True:
    start_windows()
    start_game()
    game()
    game2()
