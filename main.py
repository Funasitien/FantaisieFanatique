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
    game_over = 3

def generate_map():
    """
        Renvoie la map faite de briques
    """
    map_tab = []
    for y in range(10, 16, 2):
        for x in range(10):
            for z in range(0, 10, 2):
                map_tab.append(Brick(x, y, z, randint(1, 6)))

    return map_tab

class App:
    def __init__(self):
        self.camera = np.array([5.0, 1.0, 5.0])
        self.at = np.array([-1.0, 1.0, 0.0])

        self.yaw = 180
        self.pitch = 0

        self.current_state = State.menu

        self.bricks_start_round = 0
        self.score = 0
        self.high_score = 10000

        self.bricks = generate_map()
        self.bricks_left = 150

        pyxel.init(256, 256)
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def update(self):
        match self.current_state:
            case State.menu: 
                self.update_menu()
                return
            case State.shooting:
                self.update_shooting()
                return
            case State.boucing:
                self.update_bouncing()
                return

    def update_menu(self):
        # Clique sur le bouton
        if pyxel.btnp(pyxel.KEY_SPACE) or pyxel.btnp(pyxel.GAMEPAD1_BUTTON_A):
            self.current_state = State.shooting

    def update_shooting(self):

        if pyxel.btn(pyxel.KEY_D):
            self.yaw -= 1
        if pyxel.btn(pyxel.KEY_Q):
            self.yaw += 1
        if pyxel.btn(pyxel.KEY_Z):
            self.pitch += 1
        if pyxel.btn(pyxel.KEY_S):
            self.pitch -= 1

        if pyxel.btnp(pyxel.KEY_SPACE):
            vec_vel = self.at - self.camera
            self.ball = Ball(self.camera, vec_vel)

            self.current_state = State.boucing

        rad_yaw = radians(self.yaw)
        rad_pitch = radians(self.pitch)
        """
        speed = .1
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
        """
        self.at = np.array([cos(rad_yaw) * cos(rad_pitch), sin(rad_pitch), sin(rad_yaw) * cos(rad_pitch)]) + self.camera

    def update_bouncing(self):

        if pyxel.btn(pyxel.KEY_D):
            self.yaw -= 1
        if pyxel.btn(pyxel.KEY_Q):
            self.yaw += 1
        if pyxel.btn(pyxel.KEY_Z):
            self.pitch += 1
        if pyxel.btn(pyxel.KEY_S):
            self.pitch -= 1

        rad_yaw = radians(self.yaw)
        rad_pitch = radians(self.pitch)
        self.at = np.array([cos(rad_yaw) * cos(rad_pitch), sin(rad_pitch), sin(rad_yaw) * cos(rad_pitch)]) + self.camera

        for brick in self.bricks:
            self.ball.check_col_brick(self.bricks, brick)
        went_oob = self.ball.update_vec()
        self.ball.apply_vec()

        self.bricks_left = len(self.bricks)
        if self.bricks_left == 0:
            self.current_state = State.game_over

        if went_oob:
            self.current_state = State.shooting
            bricks_broken = self.bricks_left - self.bricks_start_round
            self.score += 5 * bricks_broken * (bricks_broken + 1) - 10
            self.bricks_start_round = self.bricks_left

    def draw(self):
        pyxel.cls(0)

        match self.current_state:
            case State.menu: 
                self.draw_menu()
                return
            case State.shooting: 
                self.draw_shooting()
                return
            case State.boucing:
                self.draw_bouncing()
                return

    def draw_menu(self):
        pyxel.text(150, 100, "PRESS SPACE TO CONTINUE", 7)
        pyxel.rect(0, 0, 100, 100, 2)

    def draw_shooting(self):
        tri_list = bricks_to_triangles(self.bricks)
        render_3D_objects(self.camera, self.at, tri_list)
        pyxel.text(84, 2, "Press space to shoot...", 7)
        self.draw_hud()
        # Crosshair
        pyxel.line(124, 127, 130, 127, 7)
        pyxel.line(127, 124, 127, 130, 7)

    def draw_bouncing(self):
        tri_list = bricks_to_triangles(self.bricks)
        render_3D_objects(self.camera, self.at, tri_list, self.ball)
        self.draw_hud()

    def draw_game_over(self):
        tri_list = bricks_to_triangles(self.bricks)
        render_3D_objects(self.camera, self.at, tri_list, self.ball)
        pyxel.text(1, 2, "GAME OVER", 7)
        pyxel.text(110, 12, f"Score: {self.score}", 7)
        pyxel.text(104, 22, f"High Score: {self.high_score}", 7)

    def draw_hud(self):
        pyxel.text(1, 2, f"[{self.bricks_left}/150] briques", 7)
        pyxel.text(1, 12, f"Score: {self.score}", 7)
        pyxel.text(1, 22, f"High Score: {self.high_score}", 7)

App()