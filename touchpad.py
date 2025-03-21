import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Key Press Detection")
        self.pressed_key = None
        self.key_map = {getattr(pyxel, name): name for name in dir(pyxel) if name.startswith("KEY_") or name.startswith("GAMEPAD1_")}
        pyxel.run(self.update, self.draw)

    def update(self):
        for key, name in self.key_map.items():
            if pyxel.btnp(key):
                self.pressed_key = name  # Store the key name

    def draw(self):
        pyxel.cls(0)
        pyxel.text(50, 50, "Press any key...", pyxel.frame_count % 16)
        if self.pressed_key:
            pyxel.text(50, 70, f"Key: {self.pressed_key}", 7)  # Display key name

App()