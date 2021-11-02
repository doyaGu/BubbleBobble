import pygame


class Message(pygame.sprite.Sprite):
    containers = ()

    def __init__(self, msg, pos, font, color, value=None):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.msg = msg
        self.font = font
        self.color = color
        self.value = value
        if value is not None:
            self.last_value = -1
            msg = self.msg + ': {}'.format(self.value)

        self.image = self.font.render(msg, 0, self.color)
        self.rect = self.image.get_rect().move(pos)

    def __lt__(self, other):
        if self.value is not None:
            return self.value < other

    def __le__(self, other):
        if self.value is not None:
            return self.value <= other

    def __gt__(self, other):
        if self.value is not None:
            return self.value > other

    def __ge__(self, other):
        if self.value is not None:
            return self.value >= other

    def __add__(self, other):
        if self.value is not None:
            self.value += other
        return self

    def __sub__(self, other):
        if self.value is not None:
            self.value -= other
        return self

    def update(self):
        if self.value is not None and self.value != self.last_value:
            self.last_value = self.value
            msg = self.msg + ': {}'.format(self.value)
            self.image = self.font.render(msg, 0, self.color)

