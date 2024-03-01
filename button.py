class Button:


    def __init__(self, row):
        self.clicked = False
        self.locked = False
        self.row = row
        self.image = None
        self.clicked_image = None

    def toggleClicked(self):
        if self.locked is not True:
            self.clicked = not self.clicked

    def lockButton(self):
        self.locked = True