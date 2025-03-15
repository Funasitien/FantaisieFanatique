from graphics import *

class Brick:
    """
        Classe représentant les briques cassables
    """
    used_ids = set()
    def __init__(self,
                 x : int, 
                 y : int, 
                 z : int, 
                 col : int
                 ):
        
        self.id = None
        biggest_id = max(Brick.used_ids, default=0)

        for id in range(biggest_id):
            if id not in Brick.used_ids:
                Brick.used_ids.add(id)
                self.id = id

        if self.id is None:
            Brick.used_ids.add(biggest_id + 1)
            self.id = biggest_id + 1

        self.triangles = [
            # Front Face
            Triangle((x, x, x+1), (y, y+1, y), (z, z, z), col),
            Triangle((x, x+1, x+1), (y+1, y+1, y), (z, z, z), col),
            # Back face
            Triangle((x, x, x+1), (y, y+1, y), (z+2, z+2, z+2), col),
            Triangle((x, x+1, x+1), (y+1, y+1, y), (z+2, z+2, z+2), col),
            # Left face
            Triangle((x, x, x), (y, y+1, y), (z, z, z+2), col),
            Triangle((x, x, x), (y+1, y+1, y), (z, z+2, z+2), col),
            # Right face
            Triangle((x+1, x+1, x+1), (y, y+1, y), (z, z, z+2), col),
            Triangle((x+1, x+1, x+1), (y+1, y+1, y), (z, z+2, z+2), col),
            # Top face
            Triangle((x, x, x+1), (y+1, y+1, y+1), (z, z+2, z), col),
            Triangle((x+1, x+1, x), (y+1, y+1, y+1), (z, z+2, z+2), col),
            # Bottom face
            Triangle((x, x, x+1), (y, y, y), (z, z+2, z), col),
            Triangle((x+1, x+1, x), (y, y, y), (z, z+2, z+2), col)
        ]

def destroy_brick(map, id):
    """
        Supprime la brick d'id=id de la map
    """
    for i, b in enumerate(map):
        if b.id == id:
            map.pop(i)
            return

def bricks_to_triangles(brick_list):
    """
        Transforme les briques en triangles à render
    """
    tri_list = []
    for b in brick_list:
        for t in b.triangles:
            tri_list.append(t)

    return tri_list
