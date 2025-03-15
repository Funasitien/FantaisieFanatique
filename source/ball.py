class Ball:
    """
        La balle !
    """
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.vec_velocity = [0, 0, 0]

    def apply_vec(self):
        """
            Bouge la balle !
        """

    def update_vec(self):
        """
            Vérifie les collisions et fait rebondir la balle en fonction
        """

    def check_col_brick(self, id) -> bool:
        """
            Renvoie True si il y a une collision entre la balle et la brick d'id=id, False sinon
        """

        return False
