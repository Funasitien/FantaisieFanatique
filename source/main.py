import pyxel
import numpy as np
from math import radians, cos, sin
from random import randint

from graphics import *
from bricks import *
from ball import *

class State:
    """
        Enumeration représentant l'état du jeu
    """
    menu = 0
    shooting = 1
    boucing = 2

def generate_map():
    """
        Renvoie la map faite de briques
    """
    map_tab = []
    for y in range(10, 16, 2):
        for x in range(10):
            for z in range(0, 10, 2):
                map_tab.append(Brick(x, y, z, randint(1, 7)))

    return map_tab

class App:
    def __init__(self):
        self.camera = np.array([3.0, 1.0, 0.0])
        self.at = np.array([-1.0, 1.0, 0.0])

        self.yaw = 180
        self.pitch = 0

        self.current_state = State.shooting

        self.map = generate_map()

        self.ball = None

        pyxel.init(256, 256)
        pyxel.run(self.update, self.draw)

    def update(self):
        speed = .1
        rad_yaw = radians(self.yaw)
        rad_pitch = radians(self.pitch)
            
        if pyxel.btn(pyxel.KEY_I):  # Move forward
            self.camera[0] += cos(rad_yaw) * speed
            self.camera[2] += sin(rad_yaw) * speed
        if pyxel.btn(pyxel.KEY_K):  # Move backward
            self.camera[0] -= cos(rad_yaw) * speed
            self.camera[2] -= sin(rad_yaw) * speed
        if pyxel.btn(pyxel.KEY_J):  # Strafe left
            self.camera[0] -= sin(rad_yaw) * speed
            self.camera[2] += cos(rad_yaw) * speed
        if pyxel.btn(pyxel.KEY_L):  # Strafe right
            self.camera[0] += sin(rad_yaw) * speed
            self.camera[2] -= cos(rad_yaw) * speed
        if pyxel.btn(pyxel.KEY_SPACE):
            self.camera[1] += speed
        if pyxel.btn(pyxel.KEY_SHIFT):
            self.camera[1] -= speed

        # Launch a ball
        # For debug purpose ofcrs
        if pyxel.btnp(pyxel.KEY_F5):
            vec_vel = self.at - self.camera
            print(vec_vel)
            self.ball = Ball(self.at - self.camera)
        
        if pyxel.btn(pyxel.KEY_D):
            self.yaw -= 1
        if pyxel.btn(pyxel.KEY_Q):
            self.yaw += 1
        if pyxel.btn(pyxel.KEY_Z):
            self.pitch += 1
        if pyxel.btn(pyxel.KEY_S):
            self.pitch -= 1

        self.at = np.array([cos(rad_yaw) * cos(rad_pitch), sin(rad_pitch), sin(rad_yaw) * cos(rad_pitch)]) + self.camera

    def draw(self):
        pyxel.cls(0)
        tri_list = bricks_to_triangles(self.map)
        render_3D_objects(self.camera, self.at, tri_list)
        pyxel.text(0, 0, str(self.at), 7)


        if self.ball is not None:
            t = np.array([self.ball.x, self.ball.y, self.ball.z, 1])
            # NOT OPTIMALLLLL
            WorldToView = WorldToViewMatrice(self.camera, self.at)
            ViewToClip = ViewToClipMatrice(60, 1)
            ViewToScreen = ClipToScreenMatrice(256, 256)
            TransformMatrix = ViewToClip @ WorldToView

            p = TransformMatrix @ t
            p = p / p[3]

            p = ViewToScreen @ p

            pyxel.circ(p[0], p[1], 10, 10)



App()
