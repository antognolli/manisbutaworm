import pyglet
from pyglet.gl import *
from pyglet.window import key
import Box2D as box2d
import math

from cocos import draw
from cocos.director import director
from cocos.layer import Layer
from cocos.sprite import Sprite
from cocos.rect import Rect

from constants import WIDTH, HEIGHT


class RectBlock(draw.Canvas):
    p1 = (-10.0, -10.0)
    p2 = (10.0, -10.0)
    p3 = (10.0, 10.0)
    p4 = (-10.0, 10.0)
    zoom = 1
    color = (0, 255, 0, 255)
    stroke_width = 1

    def __init__(self, points=None, zoom=None, color=None):
        super(RectBlock, self).__init__()

        self.points = [self.p1, self.p2, self.p3, self.p4]

        if zoom:
            self.zoom = zoom

        if not points:
            return

        if color:
            self.color = color

        for i, p in enumerate(points):
            self.points[i] = (p[0] * self.zoom, p[1] * self.zoom)

    def _point_xy(self, point):
        # This function is here to be used if later we need some kind of
        # conversion.
        return (point[0], point[1])

    def render(self):
        self.set_color(self.color)
        self.set_stroke_width(3)
        self.set_join(draw.MITER_JOIN)
        self.move_to(self._point_xy(self.points[0]))
        self.line_to(self._point_xy(self.points[1]))
        self.line_to(self._point_xy(self.points[2]))
        self.line_to(self._point_xy(self.points[3]))
        self.line_to(self._point_xy(self.points[0]))

class GameCtrl(Layer):
    is_event_handler = True
    debug = None

    def __init__(self, model):
        super(GameCtrl,self).__init__()

        self.model = model
        self.image = pyglet.resource.image('hero.png')
        self.debug = self.model.settings.debugLevel

    def on_key_press(self, k, m):
        if k == key.RETURN:
            self.model.act()
        elif k == key.RIGHT:
            self.model.move(1)
        elif k == key.LEFT:
            self.model.move(-1)
        elif k == key.UP:
            self.model.jump()
        else:
            print "unhandled key press:", k, m

    def step(self, dt):
        self.elapsed += dt
        self.model.world.Step(dt, self.model.settings.velocityIterations,
            self.model.settings.positionIterations)

    def draw( self ):
        super(GameCtrl, self).draw()

        glLoadIdentity()

        bodies = self.model.world.GetBodyList()
        i = 0
        for b in bodies:
            props = b.GetUserData()
            if not props:
                continue
            sprite, dsprite = props.get_sprite()
            if not sprite:
                if props.isCharacter:
                    shape = b.GetShapeList()[0]
                    vertices = shape.getVertices_b2Vec2()
                    if self.debug:
                        dsprite = RectBlock(vertices, zoom=self.model.zoom, color=(255,0,0,255))
                    sprite = Sprite(self.image)
                elif props.isBlock:
                    shape = b.GetShapeList()[0]
                    vertices = shape.getVertices_b2Vec2()
                    sprite = RectBlock(vertices, zoom=self.model.zoom)
                    dsprite = None
                else:
                    continue

                props.set_sprite(sprite, dsprite)
                self.add(sprite)
                if dsprite:
                    self.add(dsprite)
            sprite.position = (b.position.x * self.model.zoom), \
                (b.position.y * self.model.zoom)
            degrees = -(b.GetAngle() * 180) / math.pi
            sprite.rotation = degrees

            if dsprite:
                dsprite.position = (b.position.x * self.model.zoom), \
                    (b.position.y * self.model.zoom)
                degrees = -(b.GetAngle() * 180) / math.pi
                dsprite.rotation = degrees

        # center the image
        glTranslatef(-400, -300, -800.0)

    def on_enter(self):
        super(GameCtrl, self).on_enter()

        director.push_handlers(self.on_resize)
        self.elapsed = 0
        self.schedule(self.step)

    def on_resize( self, width, height ):
        # change the 2D projection to 3D
        glViewport(0, 0, width, height)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(90, 1.0*width/height, 0.1, 400.0)
        glMatrixMode(GL_MODELVIEW)
