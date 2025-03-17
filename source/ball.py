from bricks import Brick, destroy_brick
import numpy as np

class Ball:
    """
        La balle !
    """
    def __init__(self, vector):
        self.x = 0
        self.y = 0
        self.z = 0
        self.speed = 1
        self.vec_velocity = vector
    
    def update_vec(self):
        """
            Vérifie les collisions et fait rebondir la balle en fonction
        """
        if not 0 <= self.x <= 10:
            self.vec_velocity[0] = -self.vec_velocity[0]
        if self.y <= 20:
            self.vec_velocity[1] = -self.vec_velocity[1] 
        if not 0 <= self.z <= 10:
            self.vec_velocity[2] = -self.vec_velocity[2]
        if self.y < 0:
            self.vec_velocity = np.array([0.0, 0.0, 0.0])



    def check_col_brick(self, map_list: list, brick: Brick) -> bool:
        """
            Renvoie True si il y a une collision entre la balle et la brick d'id=id, False sinon
        """
        if (brick.x < self.x < brick.x + 1) and (brick.y < self.y < brick.y + 1) and (brick.z < self.z < brick.z + 2):
            self.vec_velocity[1] = -self.vec_velocity[1]
            destroy_brick(map_list, brick.id)
            return True
        return False

    def apply_vec(self):
        """
            Bouge la balle !
        """
        self.x += self.vec_velocity[0] * self.speed
        self.y += self.vec_velocity[1] * self.speed
        self.z += self.vec_velocity[2] * self.speed


