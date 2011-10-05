import pyglet
import weakref

import Box2D as box2d
from settings import fwSettings

class BodyProperties(object):
    isCharacter = False
    isBlock = True
    _sprite = None
    _dsprite = None

    def __init__(self, isBlock=True, isCharacter=False):
        super(BodyProperties,self).__init__()
        if isCharacter:
            self.isBlock = False
            self.isCharacter = True

    def get_sprite(self):
        return self._sprite, self._dsprite

    def set_sprite(self, sprite, dsprite=None):
        self._sprite = sprite
        self._dsprite = dsprite

class GameModel(pyglet.event.EventDispatcher):
    def __init__(self):
        super(GameModel,self).__init__()
        self.acting = False

        self.character = None
        self.ground = None

        # Box2D Initialization
        self.zoom = 50.0
        self.worldAABB=box2d.b2AABB()
        self.worldAABB.lowerBound = (-200.0, -100.0)
        self.worldAABB.upperBound = ( 200.0, 200.0)
        gravity = (0.0, -10.0)
        doSleep = True

        self.world = box2d.b2World(self.worldAABB, gravity, doSleep)

        settings = fwSettings
        self.settings = settings
        self.flag_info = [ ('draw_shapes', settings.drawShapes,
                            box2d.b2DebugDraw.e_shapeBit),
                           ('draw_joints', settings.drawJoints,
                            box2d.b2DebugDraw.e_jointBit),
                           ('draw_controlers', settings.drawControllers,
                            box2d.b2DebugDraw.e_controllerBit),
                           ('draw_core_shapes', settings.drawCoreShapes,
                            box2d.b2DebugDraw.e_coreShapeBit),
                           ('draw_aabbs', settings.drawAABBs,
                            box2d.b2DebugDraw.e_aabbBit),
                           ('draw_obbs', settings.drawOBBs,
                            box2d.b2DebugDraw.e_obbBit),
                           ('draw_pairs', settings.drawPairs,
                            box2d.b2DebugDraw.e_pairBit),
                           ('draw_center_of_masses', settings.drawCOMs,
                            box2d.b2DebugDraw.e_centerOfMassBit),]

        # Create hero
        self.character = self.create_character(200, 800, 50, 100)
        self.character.SetMassFromShapes()
        self.character.linearVelocity = (1, 0)
        if self.settings.debugLevel:
            print self.character

        # Create ground
        self.ground = self.create_ground(500, 0, 1000, 20)
        self.wall = self.create_ground(400, 20, 100, 20)
        self.wall2 = self.create_ground(600, 100, 100, 20)


    def create_character(self, x, y, w, h):
        props = BodyProperties(isCharacter=True)
        sd = box2d.b2PolygonDef()
        rx = x / self.zoom
        ry = y / self.zoom
        rw = (w / 2) / self.zoom
        rh = (h / 2) / self.zoom
        sd.SetAsBox(rw, rh)
        sd.density = 1.0

        bd = box2d.b2BodyDef()
        bd.position = (rx, ry)
        body = self.world.CreateBody(bd)
        body.CreateShape(sd)
        body.SetUserData(props)
        body.SetFixedRotation(True)
        return body

    def create_ground(self, x, y, w, h):
        rx = x / self.zoom
        ry = y / self.zoom
        rw = (w / 2) / self.zoom
        rh = (h / 2) / self.zoom
        props = BodyProperties()
        sd = box2d.b2PolygonDef()
        sd.SetAsBox(rw, rh)
        bd = box2d.b2BodyDef()
        bd.position = (rx, ry)
        body = self.world.CreateBody(bd)
        body.CreateShape(sd)
        body.SetUserData(props)
        return body

    def set_controller( self, ctrl ):
        self.ctrl = weakref.ref( ctrl )

    def act(self):
        if self.acting:
            return

        self.acting = True
        self.dispatch_event("on_move")

    def jump(self):
        vel = self.character.linearVelocity
        vel = (vel[0], 5)
        self.character.linearVelocity = vel
        self.character.WakeUp()

    def move(self, direction):
        speed = direction * 3
        vel = self.character.linearVelocity
        vel = (speed, vel[1])
        self.character.linearVelocity = vel
        self.character.WakeUp()


GameModel.register_event_type('on_move')
GameModel.register_event_type('on_colision')
GameModel.register_event_type('on_win')
GameModel.register_event_type('on_gameover')
