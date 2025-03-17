class Ball:
    """
        La balle !
    """
    def __init__(self, vector):
        self.x = 0
        self.y = 0
        self.z = 0
        self.speed = 0.1
        self.vec_velocity = vector

    def apply_vec(self):
        """
            Bouge la balle !
        """
        self.x += self.vec_velocity[0] * self.speed
        self.y += self.vec_velocity[1] * self.speed
        self.z += self.vec_velocity[2] * self.speed

    def update_vec(self):
        """
            Vérifie les collisions et fait rebondir la balle en fonction
        """

    def check_col_brick(self, id) -> bool:
        """
            Renvoie True si il y a une collision entre la balle et la brick d'id=id, False sinon
        """

        return False
