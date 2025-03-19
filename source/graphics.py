import pyxel
import numpy as np
from math import radians, sqrt, cos, sin, tan

class Triangle:
    """
        Classe contenant les triangles à dessiner
    """
    def __init__(self, 
                 x : tuple[3], 
                 y : tuple[3], 
                 z : tuple [3], 
                 col : int
                ):
        x1, x2, x3 = x
        y1, y2, y3 = y
        z1, z2, z3 = z
        self.coords = [[x1, y1, z1, 1], [x2, y2, z2, 1], [x3, y3, z3, 1]]
        self.color = col

def WorldToViewMatrice(camera, at):
    NormalizeVector = lambda v : v / np.linalg.norm(v)

    up = np.array([0, 1, 0])

    w = NormalizeVector(camera - at)
    u = NormalizeVector(np.cross(w, up))
    v = np.cross(w, u)

    return np.array([
        [u[0], u[1], u[2], -np.dot(camera, u)],
        [v[0], v[1], v[2], -np.dot(camera, v)],
        [w[0], w[1], w[2], -np.dot(camera, w)],
        [0, 0, 0, 1]
    ])

def ViewToClipMatrice(fov, aspect):
    far = 100
    near = 0.1

    f = 1 / tan(radians(fov) / 2)
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2*far*near) / (near - far)],
        [0, 0, -1, 0]
    ])

def ClipToScreenMatrice(w, h):
    return np.array([
        [w / 2, 0, 0, (w - 1) / 2],
        [0, h / 2, 0, (h - 1) / 2],
        [0, 0, 1, 0],
        [0, 0, 0, 1]
    ])

def render_3D_objects(
                      camera : tuple[3], 
                      at : tuple[3], 
                      triangles : list[Triangle],
                      ball = None
                      ):
    """
        Fait une projection / impression des triangles sur l'écran
    """
    WorldToView = WorldToViewMatrice(camera, at)
    ViewToClip = ViewToClipMatrice(60, 1)
    ViewToScreen = ClipToScreenMatrice(256, 256)
    TransformMatrix = ViewToClip @ WorldToView

    trianglesToShow = []
    for tri in triangles:
        c, t = tri.color, tri.coords
        p1, p2, p3 = TransformMatrix @ t[0], TransformMatrix @ t[1], TransformMatrix @ t[2]
        p1, p2, p3 = p1 / p1[3], p2 / p2[3], p3 / p3[3]
        
        if not ((1 >= p1[0] >= -1 and
                1 >= p1[1] >= -1 and
                1 >= p1[2] >= -1) or
                (1 >= p2[0] >= -1 and
                1 >= p2[1] >= -1 and
                1 >= p2[2] >= -1) or
                (1 >= p3[0] >= -1 and
                1 >= p3[1] >= -1 and
                1 >= p3[2] >= -1 )):
            continue

        p1, p2, p3 = ViewToScreen @ p1, ViewToScreen @ p2, ViewToScreen @ p3

        trianglesToShow.append((p1, p2, p3, c))

    trianglesToShow.sort(key=lambda pl : max(pl[0][2], pl[1][2], pl[2][2]), reverse=True)

    ball_index = -1 
    if ball is not None:
        t = np.array([ball.x, ball.y, ball.z, 1])
        pball = TransformMatrix @ t
        pball = pball / pball[3]
        pball = ViewToScreen @ pball
        ball_radius = min(100, 100 / np.linalg.norm(np.array([ball.x, ball.y, ball.z]) - camera))
        ball_index = 0
        for i, e in enumerate(trianglesToShow):
            if max(e[0][2], e[1][2], e[2][2]) >= pball[2]:
                ball_index = i
                break

    for p1, p2, p3, c in trianglesToShow:
        if ball_index == 0:
            pyxel.circ(pball[0], pball[1], ball_radius, 10)
        pyxel.tri(p1[0], p1[1], p2[0], p2[1], p3[0], p3[1], c)
        ball_index -= 1

    if ball is not None:
        pyxel.circb(pball[0], pball[1], ball_radius, 7)
