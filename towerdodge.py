class TowerDodge:
    def __init__(self):
        self.lives = 2
        self.directions = ['left', 'right', 'up', 'down']
        self.round = 0

    def move(self, move):
        return move in self.directions

    def hit(self):
        self.lives -= 1
        return self.lives <= 0

    def next_round(self):
        self.round += 1