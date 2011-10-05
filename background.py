import pyglet

from cocos.layer import Layer

from constants import WIDTH, HEIGHT, FONT

class BackgroundLayer(Layer):
    def __init__(self):
        super(BackgroundLayer, self).__init__()

        self.img = pyglet.resource.image('jungle.png')
        self.img.anchor_x = self.img.width / 2
        self.img.anchor_y = self.img.height / 2

    def draw(self):
        # self.img.blit(WIDTH / 2, HEIGHT / 2)
        pass
