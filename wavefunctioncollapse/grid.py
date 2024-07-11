import random
from cell import Cell

class Grid:
    def __init__(self, size, tileset):
        self.coast = next(tile for tile in tileset if tile.id == 'coast')
        self.size = size
        self.tileset = tileset
        self.cells = []
        for y in range(size):
            row = []
            for x in range(size):
                cell = Cell(x, y, tileset)
                row.append(cell)
            self.cells.append(row)

        self.finalGrid = []
        self.coordinates_set = set()

    def find_lowest_entropy(self):
        min_entropy = float('inf')
        min_cell = []

        for row in self.cells:
            for cell in row:
                if not cell.collapsed and cell.entropy() < min_entropy:
                    min_cell = []
                    min_entropy = cell.entropy()
                    min_cell.append(cell)
                elif not cell.collapsed and cell.entropy() == min_entropy:
                    min_cell.append(cell)

        return random.choice(min_cell) if min_cell else None

    def update_cell(self, x, y, tile_opts, collapse=False):
        cell = Cell(x, y, tile_opts)
        cell.collapsed = collapse
        self.cells[y][x] = cell

    def get_neighbors(self, x, y, diagonal=False):
        neighbors = []
        if x > 0: neighbors.append(self.cells[y][x - 1])
        if x < self.size - 1: neighbors.append(self.cells[y][x + 1])
        if y > 0: neighbors.append(self.cells[y - 1][x])
        if y < self.size - 1: neighbors.append(self.cells[y + 1][x])

        if diagonal:
            if x > 0 and y > 0: neighbors.append(self.cells[y - 1][x - 1])
            if x > 0 and y < self.size - 1: neighbors.append(self.cells[y + 1][x - 1])
            if x < self.size - 1 and y > 0: neighbors.append(self.cells[y - 1][x + 1])
            if x < self.size - 1 and y < self.size - 1: neighbors.append(self.cells[y + 1][x + 1])

        return neighbors

    def get_if_collapse(self, x, y):
        if x > 0 and not self.cells[y][x - 1].collapsed: return False
        if x < self.size - 1 and not self.cells[y][x + 1].collapsed: return False
        if y > 0 and not self.cells[y - 1][x].collapsed: return False
        if y < self.size - 1 and not self.cells[y + 1][x].collapsed: return False
        return True

    def propogate(self):
        stack = []

        for row in self.cells:
            for cell in row:
                if cell.collapsed and not cell.total_done:
                    stack.append(cell)

        while stack:
            cell = stack.pop()
            cell.total_done = self.get_if_collapse(cell.x, cell.y)
            for neighbor in self.get_neighbors(cell.x, cell.y):
                if neighbor.collapsed:
                    continue
                other_neighbors = self.get_neighbors(neighbor.x, neighbor.y, True)
                neighbor.update(cell, other_neighbors, self.coast)
                if neighbor.collapsed and not neighbor.total_done:
                    stack.append(neighbor)

    def render(self):
        for row in self.cells:
            for cell in row:
                if not cell.collapsed:
                    continue
                tile = cell.tile_options[0]
                self.set_pixel(cell.x, cell.y, tile.color['r'], tile.color['g'], tile.color['b'])

    def clean_coasts(self):
        for y in range(self.size):
            for x in range(self.size):
                cell = self.cells[y][x]
                if cell.collapsed and cell.tile_options[0].id == 'coast':
                    neighbors = self.get_neighbors(x, y, True)
                    has_coast = any(n.collapsed and n.tile_options[0].id == 'coast' for n in neighbors)
                    has_sea = any(n.collapsed and n.tile_options[0].id == 'sea' for n in neighbors)
                    has_land = any(n.collapsed and n.tile_options[0].id == 'land' for n in neighbors)

                    if not has_coast:
                        if has_sea:
                            sea = next(tile for tile in self.tileset if tile.id == 'sea')
                            self.update_cell(x, y, [sea], True)
                            self.set_pixel(x, y, sea.color['r'], sea.color['g'], sea.color['b'], True)
                        elif has_land:
                            land = next(tile for tile in self.tileset if tile.id == 'land')
                            self.update_cell(x, y, [land], True)
                            self.set_pixel(x, y, land.color['r'], land.color['g'], land.color['b'], True)
        self.render()

    def set_pixel(self, x, y, r, g, b, overwrite=False):
        coordinate = (x, y)
        
        if coordinate in self.coordinates_set:
            if overwrite:
                for pixel in self.finalGrid:
                    if pixel['x'] == x and pixel['y'] == y:
                        pixel['color'] = [r, g, b]
                        break
        else:
            self.finalGrid.append({'x': x, 'y': y, 'color': [r, g, b]})
            self.coordinates_set.add(coordinate)
