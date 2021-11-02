import os
import pygame

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, 'data')


def load_image(filename):
    path = os.path.join(data_dir, filename)
    try:
        image = pygame.image.load(path)
    except pygame.error:
        print('Cannot load image:', path)
        raise SystemExit(str(pygame.get_error()))
    return image.convert_alpha()


def load_game_images():
    return [
        load_image('background.jpg')
    ]


def load_bubble_images():
    return {
        'blue': load_image('bubble_blue.png'),
        'green': load_image('bubble_green.png'),
        'grey': load_image('bubble_grey.png'),
        'orange': load_image('bubble_orange.png'),
        'pink': load_image('bubble_pink.png'),
        'red': load_image('bubble_red.png'),
        'yellow': load_image('bubble_yellow.png')
    }


def load_player_images():
    image = load_image('arrow.png')
    return [image]


def load_sound(filename):
    path = os.path.join(data_dir, filename)
    try:
        sound = pygame.mixer.Sound(path)
    except pygame.error:
        print('Cannot load sound: %s' % path)
        raise SystemExit(str(pygame.get_error()))
    return sound


def load_game_sounds():
    return {
        'bubble': load_sound('bubble.wav'),
        'dead': load_sound('dead.wav')
    }


def load_music(filename):
    path = os.path.join(data_dir, filename)
    try:
        music = pygame.mixer.music.load(path)
    except pygame.error:
        print('Cannot load music: %s' % path)
        raise SystemExit(str(pygame.get_error()))
    return music


def load_game_fonts():
    return [
        pygame.font.SysFont(None, 36),
        pygame.font.SysFont(None, 48),
        pygame.font.SysFont(None, 72)
    ]
