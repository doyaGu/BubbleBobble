import pygame
import utils

from Player import *
from Bubble import *
from Level import Level


class GameState(Enum):
    PLAY = 1
    END = 2


class Game(object):
    name = 'Bubble Bobble'
    fonts = []
    images = []
    sounds = {}

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_rect = pygame.Rect((0, 0), self.screen.get_size())

        self.clock = pygame.time.Clock()

        self.state = GameState.PLAY
        self.level = Level(1)
        self.running = True

        '''
        BUTTON_NULL = 0
        BUTTON_LEFT = 1
        BUTTON_MIDDLE = 2
        BUTTON_RIGHT = 3
        '''
        self.mouse = {
            'pos': pygame.mouse.get_pos(),  # [x, y]
            "button": 0
        }
        self.keys = {
            'left': False,
            'right': False,
            'space': False,
        }

        self.intervals = self.level.intervals
        self.time = {
            'level': 0,
            'shot': 0,
            'descend': 0
        }
        self.flag = {
            'level': True,  # bonus if the player finishes a level quickly
            'shot': False,
            'descend': False
        }

        # Create and show the background
        self.background = pygame.Surface(self.screen_rect.size)
        self.background.blit(self.images[0], (0, 0))
        self.screen.blit(self.background, (0, 0))
        pygame.display.flip()

        self.bubbles = pygame.sprite.Group()
        self.targets = pygame.sprite.RenderUpdates()

        # assign default groups to each sprite
        Message.containers = self.targets
        Player.containers = self.targets
        Bubble.containers = self.targets

        self.player = Player(self)
        create_bubbles(self, self.bubbles, self.level.rows, self.level.cols)

    def __event_handler(self, event):
        if event.type == pygame.QUIT:
            self.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                self.keys['left'] = True
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                self.keys['right'] = True
            if event.key == pygame.K_SPACE:
                self.keys['space'] = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                self.quit()
            if event.key == pygame.K_LEFT or event.key == ord('a'):
                self.keys['left'] = False
            if event.key == pygame.K_RIGHT or event.key == ord('d'):
                self.keys['right'] = False
            if event.key == pygame.K_SPACE:
                self.keys['space'] = False
        if event.type == pygame.MOUSEMOTION:
            self.mouse['pos'] = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.mouse['button'] = event.button
        if event.type == pygame.MOUSEBUTTONUP:
            self.mouse['button'] = 0

    def __time_handler(self, time):
        if self.state == GameState.PLAY:
            self.time['level'] += time
            self.time['shot'] += time
            self.time['descend'] += time

            if self.time['level'] >= self.intervals['level']:
                self.flag['level'] = False
                self.time['level'] = 0
            if self.time['shot'] >= self.intervals['shot']:
                self.flag['shot'] = True
                self.time['shot'] = 0
            if self.time['descend'] >= self.intervals['descend']:
                self.flag['descend'] = True
                self.time['descend'] = 0
        elif self.state == GameState.END:
            pass

    def __clear(self):
        self.bubbles.empty()
        self.targets.empty()

    def should_shot(self):
        if self.flag['shot']:
            self.flag['shot'] = False
            return True
        return False

    def should_descend(self):
        if self.flag['descend']:
            self.flag['descend'] = False
            return True
        return False

    def is_running(self):
        return self.running

    def quit(self):
        self.running = False

    def restart(self):
        self.__clear()
        self.player.reinit()
        create_bubbles(self, self.bubbles, self.level.rows, self.level.cols)
        self.time['level'] = 0
        self.time['shot'] = 0
        self.time['descend'] = 0
        self.top_bubble_y = 0

    def end(self, text):
        self.__clear()

        msg = Message(text, (0, 0), self.fonts[2], pygame.Color('white'))
        msg.rect.center = self.screen_rect.center

        self.state = GameState.END

    def update(self, fps):
        for event in pygame.event.get():
            self.__event_handler(event)

        if self.state == GameState.PLAY:
            if self.should_descend():
                descend_bubbles(self, 2)

            if self.player.is_dead():
                if self.player.life > 0:
                    self.restart()
                else:
                    self.end('Game Over.')

            if not self.bubbles.sprites():
                if self.level.number == self.level.total:
                    self.end('You Win!')
                score = self.player.score
                if self.flag['level']:
                    score += 1000
                self.level.next()
                self.restart()
                self.player.score = score
        elif self.state == GameState.END:
            if self.keys['space'] or self.mouse['button'] == 1:
                self.level = Level(1)
                self.restart()
                self.state = GameState.PLAY

        self.targets.update()
        self.__time_handler(self.clock.tick(fps))

    def draw(self):
        self.targets.clear(self.screen, self.background)

        # draw the scene
        rects = self.targets.draw(self.screen)
        pygame.display.update(rects)