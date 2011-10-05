import pyglet
from pyglet.window import key

from cocos.director import director
from cocos.scene import Scene
from cocos.layer import Layer
from cocos.text import Label
from cocos.scenes.transitions import FadeTransition

from constants import WIDTH, HEIGHT, FONT
from gameview import GameView
from gamemodel import GameModel
from gamectrl import GameCtrl
from background import BackgroundLayer

import sound

class LogoLayer(Layer):

    is_event_handler = True

    def __init__(self):
        super(LogoLayer, self).__init__()

        # self.img = pyglet.resource.image('jungle.png')
        # self.img.anchor_x = self.img.width / 2
        # self.img.anchor_y = self.img.height / 2

        name = Label('Man Is But A Worm',
            font_name = FONT, font_size = 40,
            anchor_x = 'center', anchor_y = 'center')
        name.position = WIDTH / 2, HEIGHT * 3 / 4
        self.add(name)

        info = Label('Press space to act',
            font_name = FONT, font_size = 18,
            anchor_x = 'center', anchor_y = 'center')
        info.position = WIDTH / 2, HEIGHT / 5
        self.add(info)

        sound.start_music()

    def draw(self):
        # self.img.blit(WIDTH / 2, HEIGHT / 2)
        pass

    def on_key_press(self, k, m):
        if k in [key.SPACE, key.RETURN]:
            scene = new_game()
            director.replace(FadeTransition(scene, 2))
            return True
        # FIXME remove after tests
        elif k in [key.Z]:
            sound.inc_music()
            return True
        # FIXME remove after tests
        elif k in [key.X]:
            sound.dec_music()
            return True
        return False


def new_game():
    scene = Scene()
    model = GameModel()
    ctrl = GameCtrl(model)
    view = GameView(model)

    model.set_controller( ctrl )

    scene.add( BackgroundLayer(), z=0, name="background" )
    scene.add( ctrl, z=1, name="controller" )
    scene.add( view, z=2, name="view" )

    return scene


if __name__ == "__main__":
    pyglet.resource.path.append('data')
    pyglet.resource.reindex()
    pyglet.font.add_directory('data')

    director.init(resizable = True, width = WIDTH, height = HEIGHT)
    director.set_depth_test()
    scene = Scene()
    scene.add(LogoLayer())
    director.run(scene)
