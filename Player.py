import random
import pygame

from Message import Message
from Bubble import Bubble, BubbleState


class Player(pygame.sprite.Sprite):
    containers = ()
    images = []

    def __init__(self, game, life=3):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.game = game

        self.image = self.images[0]
        self.rect = self.image.get_rect(midbottom=self.game.screen_rect.midbottom)

        self.dead = False

        self.angle = 0
        self.last_angle = 0
        self.control_by_mouse = True

        self.life = Message('Life', (10, self.game.screen_rect.height - 36 * 1),
                            self.game.fonts[0], pygame.Color('white'), life)
        self.score = Message('Score', (10, self.game.screen_rect.height - 36 * 2),
                             self.game.fonts[0], pygame.Color('white'), 0)
        self.level = Message('Level', (10, self.game.screen_rect.height - 36 * 3),
                             self.game.fonts[0], pygame.Color('white'), self.game.level.number)

        self.shot_pos = (self.rect.centerx - Bubble.width // 2, self.rect.centery - Bubble.height // 2)
        self.wait_pos = (self.shot_pos[0] + Bubble.width * 2, self.shot_pos[1])

        self.shot_bubble = self.__new_bubble(self.shot_pos)
        self.wait_bubble = self.__new_bubble(self.wait_pos)

        self.shot_bubble.ready()
        self.fly_bubble = None

    def __new_bubble(self, pos):
        bubble = Bubble(self.game, Bubble.colors[self.game.level.rand_gen()], BubbleState.WAIT)
        bubble.move_to(pos)
        return bubble

    def __calc_angle_from_point(self, pos):
        x1, y1 = pos
        x2, y2 = self.rect.center
        v = pygame.Vector2()
        v.xy = x1 - x2, y2 - y1
        vx = pygame.Vector2()
        vx.xy = 1, 0
        return vx.angle_to(v)

    def __rotate(self, angle):
        self.image = pygame.transform.rotate(self.images[0], angle - 90)
        center = self.rect.center
        self.rect = self.image.get_rect(center=center)

    def reinit(self):
        self.game.targets.add(self)
        self.life = Message('Life', (10, self.game.screen_rect.height - 36 * 1),
                            self.game.fonts[0], pygame.Color('white'), self.life.value)
        self.score = Message('Score', (10, self.game.screen_rect.height - 36 * 2),
                             self.game.fonts[0], pygame.Color('white'), 0)
        self.level = Message('Level', (10, self.game.screen_rect.height - 36 * 3),
                             self.game.fonts[0], pygame.Color('white'), self.game.level.number)
        self.dead = False

        self.angle = 0
        self.last_angle = 0
        self.control_by_mouse = True

        self.shot_bubble = self.__new_bubble(self.shot_pos)
        self.wait_bubble = self.__new_bubble(self.wait_pos)
        self.shot_bubble.ready()
        self.fly_bubble = None

    def is_dead(self):
        return self.dead

    def die(self):
        self.game.sounds['dead'].play()
        self.life -= 1
        self.dead = True

    def update(self):
        angle = self.__calc_angle_from_point(self.game.mouse['pos'])
        if self.control_by_mouse:
            self.last_angle = self.angle
            self.angle = angle
        self.control_by_mouse = False
        if self.last_angle != angle:
            self.control_by_mouse = True
        if self.angle < 170 and self.game.keys['left']:
            self.angle += 5
        elif self.angle > 10 and self.game.keys['right']:
            self.angle -= 5
        self.__rotate(self.angle)

        ready_shot = self.game.keys['space'] or self.game.mouse['button'] == 1 or self.game.should_shot()
        if ready_shot and not self.fly_bubble:
            self.game.time['shot'] = 0
            self.game.sounds['bubble'].play()
            self.shot_bubble.fly()
            self.fly_bubble = self.shot_bubble

            self.wait_bubble.move_to(self.shot_pos)
            self.shot_bubble = self.wait_bubble
            self.shot_bubble.ready()
            self.wait_bubble = self.__new_bubble(self.wait_pos)

        if self.fly_bubble and not self.fly_bubble.is_flying():
            self.fly_bubble = None
