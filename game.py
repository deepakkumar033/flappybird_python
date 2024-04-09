import random
import sys
import pygame
from pygame.locals import *


pygame.mixer.init()
pygame.mixer.music.load('./point-101soundboards.mp3')
crash_sound = pygame.mixer.Sound("./hit-101soundboards.mp3")
music_played = False

# All the Game Variables
window_width = 600
window_height = 499

# set height and width of window
window = pygame.display.set_mode((window_width, window_height), pygame.FULLSCREEN)


elevation = window_height * 0.8
game_images = {}
framepersecond = 32
pipeimage = './pipe.png'
background_image = './background.jpg'
birdplayer_image = './bird.png'
sealevel_image = './base.jpg'


def flappygame():
    global music_played
    your_score = 0
    horizontal = int(window_width / 5)
    vertical = int(window_width / 2)
    ground = 0
    mytempheight = 100

    playerHeight = game_images['flappybird'].get_height()  # Add this line

    # Generating two pipes for blitting on window
    first_pipe = createPipe()
    second_pipe = createPipe()

    # List containing lower pipes
    down_pipes = [
        {'x': window_width + 300 - mytempheight,
         'y': first_pipe[1]['y']},
        {'x': window_width + 300 - mytempheight + (window_width / 2),
         'y': second_pipe[1]['y']},
    ]

    # List Containing upper pipes
    up_pipes = [
        {'x': window_width + 300 - mytempheight,
         'y': first_pipe[0]['y']},
        {'x': window_width + 200 - mytempheight + (window_width / 2),
         'y': second_pipe[0]['y']},
    ]

    # pipe velocity along x
    pipeVelX = -4

    # bird velocity
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
                if vertical > 0:
                    bird_velocity_y = bird_flap_velocity
                    bird_flapped = True

        # This function will return true
        # if the flappybird is crashed
        game_over = isGameOver(horizontal, vertical, up_pipes, down_pipes)
        if game_over:
            displayGameOver(your_score)  
            return

        playerMidPos = horizontal + game_images['flappybird'].get_width() / 2

        for pipe in up_pipes:
            pipeMidPos = pipe['x'] + game_images['pipeimage'][0].get_width() / 2
            if pipeMidPos - 5 < playerMidPos < pipeMidPos + 5:
                your_score += 1
                print(f"Your Score is {your_score}")
                pygame.mixer.music.play()
                music_played = True
            if playerMidPos > pipeMidPos + 5:
                 music_played = False

        if bird_flapped:
            bird_flapped = False
        if bird_velocity_y < bird_Max_Vel_Y and not bird_flapped:
            bird_velocity_y += birdAccY

        if not bird_flapped:
            vertical = min(vertical + bird_velocity_y, window_height - playerHeight)


        # move pipes to the left
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            upperPipe['x'] += pipeVelX
            lowerPipe['x'] += pipeVelX

        # Add a new pipe when the first is
        # about to cross the leftmost part of the screen
        if 0 < up_pipes[0]['x'] < 5:
            newpipe = createPipe()
            up_pipes.append(newpipe[0])
            down_pipes.append(newpipe[1])

        # if the pipe is out of the screen, remove it
        if up_pipes[0]['x'] < -game_images['pipeimage'][0].get_width():
            up_pipes.pop(0)
            down_pipes.pop(0)

        # Lets blit our game images now
        window.blit(game_images['background'], (0, 0))
        for upperPipe, lowerPipe in zip(up_pipes, down_pipes):
            window.blit(game_images['pipeimage'][0],
                        (upperPipe['x'], upperPipe['y']))
            window.blit(game_images['pipeimage'][1],
                        (lowerPipe['x'], lowerPipe['y']))

        window.blit(game_images['sea_level'], (ground, elevation))
        window.blit(game_images['flappybird'], (horizontal, vertical))

        # Fetching the digits of score.
        numbers = [int(x) for x in list(str(your_score))]
        width = 0

        # finding the width of score images from numbers.
        for num in numbers:
            width += game_images['scoreimages'][num].get_width()
        Xoffset = (window_width - width) / 1.1

        # Blitting the images on the window.
        for num in numbers:
            window.blit(game_images['scoreimages'][num],
                        (Xoffset, window_width * 0.02))
            Xoffset += game_images['scoreimages'][num].get_width()

        # Refreshing the game window and displaying the score.
        pygame.display.update()
        framepersecond_clock.tick(framepersecond)

def displayGameOver(score):
    font = pygame.font.SysFont(None, 55)
    text = font.render(f"Game Over. Your Score: {score}", True, (255, 255, 255))
    window.blit(text, (window_width / 5, window_height / 2))
    pygame.display.update()
    pygame.time.wait(2000)  # Display for 2 seconds before quitting
    pygame.quit()
    sys.exit()

def isGameOver(horizontal, vertical, up_pipes, down_pipes):
    global crash_sound 
    if vertical > elevation - 25 or vertical < 0:
        crash_sound.play()
        return True

    for pipe in up_pipes:
        pipeHeight = game_images['pipeimage'][0].get_height()
        if(vertical < pipeHeight + pipe['y'] and
           abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width()):
            crash_sound.play()
            return True

    for pipe in down_pipes:
        if (vertical + game_images['flappybird'].get_height() > pipe['y']) and abs(horizontal - pipe['x']) < game_images['pipeimage'][0].get_width():
            crash_sound.play()
            return True
    return False


def createPipe():
    offset = window_height / 3
    pipeHeight = game_images['pipeimage'][0].get_height()
    y2 = offset + random.randrange(
        0, int(window_height - game_images['sea_level'].get_height() - 1.2 * offset))
    pipeX = window_width + 10
    y1 = pipeHeight - y2 + offset
    upper_pipe = {'x': pipeX, 'y': -y1}
    lower_pipe = {'x': pipeX, 'y': y2}
    return upper_pipe, lower_pipe

def start_game():
    horizontal = int(window_width / 5)
    vertical = int((window_height - game_images['flappybird'].get_height()) / 2)
    ground = 0
    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                flappygame()
                return  # Exit the start_game loop after flappygame is done

        window.blit(game_images['background'], (0, 0))
        window.blit(game_images['flappybird'], (horizontal, vertical))
        window.blit(game_images['sea_level'], (ground, elevation))
        pygame.display.update()
        framepersecond_clock.tick(framepersecond)


# program where the game starts
if __name__ == "__main__":
    pygame.init()
    framepersecond_clock = pygame.time.Clock()
    pygame.display.set_caption('Flappy Bird Game')

    # Load images...
    game_images['scoreimages'] = (
        pygame.image.load('./0.png').convert_alpha(),
        pygame.image.load('./1.png').convert_alpha(),
        pygame.image.load('./2.png').convert_alpha(),
        pygame.image.load('./3.png').convert_alpha(),
        pygame.image.load('./4.png').convert_alpha(),
        pygame.image.load('./5.png').convert_alpha(),
        pygame.image.load('./6.png').convert_alpha(),
        pygame.image.load('./7.png').convert_alpha(),
        pygame.image.load('./8.png').convert_alpha(),
        pygame.image.load('./9.png').convert_alpha()
    )
    bird_image = pygame.image.load(birdplayer_image).convert_alpha()
    bird_image = pygame.transform.scale(bird_image, (50, 35))  # Adjust the size as needed
    game_images['flappybird'] = bird_image
    game_images['sea_level'] = pygame.image.load(sealevel_image).convert_alpha()
    game_images['background'] = pygame.image.load(background_image).convert_alpha()
    game_images['pipeimage'] = (pygame.transform.rotate(pygame.image.load(pipeimage).convert_alpha(), 180),
                                pygame.image.load(pipeimage).convert_alpha())

    print("WELCOME TO THE FLAPPY BIRD GAME")
    print("Press space or enter to start the game")

    while True:
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP):
                start_game()

        window.blit(game_images['background'], (0, 0))
        pygame.display.update()
        framepersecond_clock.tick(framepersecond)
