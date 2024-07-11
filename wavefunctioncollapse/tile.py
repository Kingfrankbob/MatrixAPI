class Tile:
    def __init__(self, color, neighbors, restrictions, id):
        self.color = color
        self.neighbors = neighbors
        self.restrictions = restrictions
        self.id = id