from asyncio.windows_utils import pipe
import random
import sys
from turtle import window_height, window_width
import pygame
from pygame.locals import *

window_width = 600
window_height = 499

window = pygame.display.set_mode((window_width,window_height))

elevation = window_height *0.8
game_images = {}
framepersecond = 32

pipeimage = 'images/pipe.png'
background_image = 'images/background.png'
birdplayer_image = 'images/bird.png'
sealevel_image = 'images/base.jfif'

def flappygame():
    your_score = 0
    horizontal = int(window_width/5)
    vertical = int(window_width/2)
    ground = 0
    mytempheight = 100

    first_pipe = createPipe()
    second_pipe = createPipe()

    down_pipes = [
        {'x': window_width+300 - mytempheight,
        'y' : first_pipe[1]['y']},
        {'x': window_width+300-mytempheight+(window_width/2),
        'y': second_pipe[1]['y']},
    ]

    up_pipes = [
        {'x': window_width+300 - mytempheight,
        'y' : first_pipe[0]['y']},
        {'x': window_width+200-mytempheight+(window_width/2),
        'y': second_pipe[0]['y']},
    ]

    pipeVelX = -4
    bird_velocity_y = -9
    bird_Max_Vel_Y = 10
    bird_Min_Vel_Y = -8
    birdAccY = 1

    bird_flap_velocity = -8
    bird_flapped = False
    while True:

        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()

            if event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                if vertical>0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True
        game_over = isGameOver(horizontal, vertical, up_pipes, down_pipes)
        if game_over:
            return     

        playerMidPos = horizontal + game_images['flappybird'].get_width()/2
        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width()/2
            if pipeMidPos <= playerMidPos < pipeMidPos + 4:
                your_score += 1
                print(f'score is {your_score}')
        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY

        if bird_flapped:
            bird_flapped = False
        playerHeight = game_images['flappybird'].get_height()
        vertical = vertical + min(bird_velocity_y, elevation-vertical-playerHeight)
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])

        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0],
                        (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1],
                        (lowerPipe['x'], lowerPipe['y']))
        window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['flappybird'], (horizontal, vertical))

        numbers = [int(x) for x in list(str(your_score))]
        width = 0

        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width)/1.1

        for num in numbers:
            window.blit(game_images['scoreimages'][num], (Xoffset, window_width*0.02))
            Xoffset += game_images['scoreimages'][num].get_width()
        
        pygame.display.update()
        framepersecond_clock.tick(framepersecond)

def createPipe():
    offset = window_height/3
    pipeHeight = game_images['pipeimage'][0].get_height()

    y2 = offset + random.randrange(0, int(window_height - game_images['sea_level'].get_height()- 1.2 * offset))
    pipeX = window_width + 10;
    y1 = pipeHeight - y2 + offset
    pipe = [{'x': pipeX, 'y': -y1},{'x': pipeX, 'y': y2}]
    return pipe

def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    if vertical > elevation - 25 or vertical <0:
        return True
    for pipe in up_pipes:
        pipeHeight = game_images['pipeimage'][0].get_height()
        if(vertical< pipeHeight+pipe['y'] and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            
            return True
    for pipe in down_pipes:
            
        if ((vertical + game_images['flappybird'].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            return True
        return False


if __name__ == "__main__":
    pygame.init()
    framepersecond_clock = pygame.time.Clock()
    game_images['scoreimages'] = (
        pygame.image.load('images/0.png').convert_alpha(),
        pygame.image.load('images/1.png').convert_alpha(),
        pygame.image.load('images/2.png').convert_alpha(),
        pygame.image.load('images/3.png').convert_alpha(),
        pygame.image.load('images/4.png').convert_alpha(),
        pygame.image.load('images/5.png').convert_alpha(),
        pygame.image.load('images/6.png').convert_alpha(),
        pygame.image.load('images/7.png').convert_alpha(),
        pygame.image.load('images/8.png').convert_alpha(),
        pygame.image.load('images/9.png').convert_alpha()
        
    )

    game_images['flappybird'] = pygame.image.load(birdplayer_image).convert_alpha()
    game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()
    game_images['background'] = pygame.image.load(background_image).convert_alpha()
    game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(),180),pygame.image.load(pipeimage).convert_alpha())
    print('Welcome to flappy bird')
    print('press space or enter to start')

    while True:

        horizontal = int(window_width/5)
        vertical = int((window_height - game_images['flappybird'].get_height())/2)

        ground = 0
        while True:
            for event in pygame.event.get():
  
                # if user clicks on cross button, close the game
                if event.type == QUIT or (event.type == KEYDOWN and \
                                          event.key == K_ESCAPE):
                    pygame.quit()
                    sys.exit()
  
                # If the user presses space or
                # up key, start the game for them
                elif event.type == KEYDOWN and (event.key == K_SPACE or\
                                                event.key == K_UP):
                    flappygame()
  
                # if user doesn't press anykey Nothing happen
                else:
                    window.blit(game_images['background'], (0, 0))
                    window.blit(game_images['flappybird'],
                                (horizontal, vertical))
                    window.blit(game_images['sea_level'], (ground, elevation))
                    pygame.display.update()
                    framepersecond_clock.tick(framepersecond)

