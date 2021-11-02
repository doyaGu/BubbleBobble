import random
import pygame
from enum import Enum


class BubbleState(Enum):
    IDLE = 1
    WAIT = 2
    READY = 3
    CHECK = 4
    FALL = 5
    FLY = 6


class Bubble(pygame.sprite.Sprite):
    containers = ()
    images = {}
    colors = [
        'blue',
        'green',
        'grey',
        'orange',
        'pink',
        'red',
        'yellow'
    ]
    width, height = 60, 60
    speed = 40
    rows, cols = 11, 10

    def __init__(self, game, color, state, x=14, y=14):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.game = game
        self.color = color
        self.x, self.y = x, y
        self.state = state
        self.image = self.images[self.color]
        self.rect = self.image.get_rect(topleft=self.__convert_pos())
        self.angle = 0
        self.vector = pygame.Vector2()
        self.fixed = False

    def __convert_pos(self):
        if self.y % 2 == 0:
            pixel_x = Bubble.width * self.x
        else:
            pixel_x = Bubble.width // 2 + Bubble.width * self.x
        pixel_y = (Bubble.height - 10) * self.y
        return pixel_x, pixel_y

    def update(self):
        if self.state == BubbleState.IDLE:
            if self.y >= self.rows and not self.game.player.is_dead():
                self.game.player.die()
        if self.state == BubbleState.WAIT:
            pass
        elif self.state == BubbleState.READY:
            self.angle = self.game.player.angle
            self.vector.from_polar((self.speed, self.angle))
            self.vector.y *= -1
        elif self.state == BubbleState.CHECK:
            same_list = self.find_same_bubble()
            self.game.bubbles.add(self)
            length = len(same_list)
            if length > 2:
                self.game.bubbles.remove(same_list)
                self.game.targets.remove(same_list)
                self.game.player.score += length * 10
                same_list.clear()
                drop_bubbles(self.game)
            else:
                self.state = BubbleState.IDLE
        elif self.state == BubbleState.FALL:
            self.rect.y += self.speed
            if self.rect.y > self.height * self.rows:
                self.game.bubbles.remove(self)
                self.game.targets.remove(self)
        elif self.state == BubbleState.FLY:
            new_rect = self.rect.move(*self.vector.xy)
            self.rect = new_rect
            if not self.game.screen_rect.contains(new_rect):
                tl = not self.game.screen_rect.collidepoint(new_rect.topleft)
                tr = not self.game.screen_rect.collidepoint(new_rect.topright)
                bl = not self.game.screen_rect.collidepoint(new_rect.bottomleft)
                br = not self.game.screen_rect.collidepoint(new_rect.bottomright)
                if tl and bl:
                    self.vector.x *= -1
                if tr and br:
                    self.vector.x *= -1
                if tr and tl or (br and bl):
                    if tr and tl:
                        self.y = 0
                        self.x = self.rect.x // self.width
                        self.move_to(self.__convert_pos())
                    self.game.bubbles.add(self)
                    self.state = BubbleState.IDLE
                    return
            for bubble in self.game.bubbles.sprites():
                if self.collide_with_bubble(bubble):
                    self.adjust_position(bubble)
                    self.state = BubbleState.CHECK
                    break

    def move_to(self, pos):
        self.rect.x, self.rect.y = pos

    def ready(self):
        self.state = BubbleState.READY

    def fly(self):
        self.state = BubbleState.FLY

    def is_flying(self):
        return self.state == BubbleState.FLY

    def collide_with_bubble(self, other):
        return pygame.sprite.collide_circle(self, other)

    def find_same_bubble(self):
        same_list = [self]
        for bubble in same_list:
            for cur in bubble.get_around_bubbles(bubble.game.bubbles):
                if cur.color == bubble.color:
                    if cur not in same_list:
                        same_list.append(cur)
        return same_list

    def get_around_bubbles(self, group):
        nearby_list = pygame.sprite.spritecollide(self, group, False, pygame.sprite.collide_rect_ratio(1.2))
        return nearby_list

    def adjust_position(self, bubble):
        vec1 = pygame.Vector2()
        vec1.x = self.rect.centerx - bubble.rect.centerx
        vec1.y = self.rect.centery - bubble.rect.centery
        vec2 = pygame.Vector2()
        vec2.xy = (0, 0)
        angle = vec1.angle_to(vec2)

        if -30 <= angle <= 30:
            self.x = bubble.x + 1
            self.y = bubble.y
        elif 150 <= abs(angle) <= 180:
            self.x = bubble.x - 1
            self.y = bubble.y
        elif 30 <= angle <= 90:
            if bubble.y % 2 == 0:
                self.x = bubble.x
            else:
                self.x = bubble.x + 1
            self.y = bubble.y - 1
        elif 90 <= angle <= 150:
            if bubble.y % 2 == 0:
                self.x = bubble.x - 1
            else:
                self.x = bubble.x
            self.y = bubble.y - 1
        elif -90 <= angle <= -30:
            if bubble.y % 2 == 0:
                self.x = bubble.x
            else:
                self.x = bubble.x + 1
            self.y = bubble.y + 1
        elif -150 <= angle <= -90:
            if bubble.y % 2 == 0:
                self.x = bubble.x - 1
            else:
                self.x = bubble.x
            self.y = bubble.y + 1

        self.move_to(self.__convert_pos())

    def descend(self, offset):
        self.y += offset
        self.move_to(self.__convert_pos())


def create_bubbles(game, group, rows, cols):
    for y in range(0, rows):
        tmp = cols
        if y % 2 == 1:
            tmp = cols - 1
        for x in range(0, tmp):
            color = game.level.board[y][x]
            bubble = Bubble(game, color, BubbleState.IDLE, x, y)
            group.add(bubble)


def descend_bubbles(game, offset):
    for bubble in game.bubbles:
        bubble.descend(offset)
    bubbles = pygame.sprite.Group()
    create_bubbles(game, bubbles, 2, Bubble.cols)
    bubbles.add(game.bubbles)
    game.bubbles = bubbles


def drop_bubbles(game):
    fixed_list = []
    for bubble in game.bubbles:
        if bubble.y == 0:
            bubble.fixed = True
            fixed_list.append(bubble)

    for bubble in fixed_list:
        for cur in bubble.get_around_bubbles(game.bubbles):
            if not cur.fixed:
                cur.fixed = True
                fixed_list.append(cur)

    n = 0
    for bubble in game.bubbles:
        if not bubble.fixed:
            bubble.state = BubbleState.FALL
            n += 1
    game.player.score += 10 * 2 ** n

    for bubble in game.bubbles:
        bubble.fixed = False
