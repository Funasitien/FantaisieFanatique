import pyxel

class App:
    def __init__(self):
        pyxel.init(160, 120, title="Key Press Detection")  # Initialize window
        self.pressed_key = None  # Store last pressed key
        pyxel.run(self.update, self.draw)  # Run Pyxel app

    def update(self):
        for key in range(1024):  # Check all possible key codes
            if pyxel.btnp(key):  # If key is pressed
                self.pressed_key = key  # Store key code

    def draw(self):
        pyxel.cls(0)  # Clear screen
        pyxel.text(50, 50, "Press any key...", pyxel.frame_count % 16)  # Blinking text
        if self.pressed_key is not None:
            pyxel.text(50, 70, f"Key Code: {self.pressed_key}", 7)  # Display key code

App()
