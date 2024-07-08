import xml.etree.ElementTree as ET
import random
import asyncio
import sys

xmlstring = """<?xml version="1.0" encoding="UTF-8"?>
<tileset>
    <length value="5"/>
    <tile id="sea">
        <color r="0" g="0" b="255"/>
        <neighbors>
            <neighbor type="sea"/>
            <neighbor type="coast"/>
        </neighbors>
        <restrictions>
        </restrictions>
    </tile>
    <tile id="deepsea">
        <color r="11" g="47" b="125"/>
        <neighbors>
            <neighbor type="sea"/>
            <neighbor type="deepsea"/>
        </neighbors>
    </tile>
    <tile id="coast">
        <color r="255" g="255" b="0"/>
        <neighbors>
            <neighbor type="sea"/>
            <neighbor type="coast"/>
            <neighbor type="land"/>
        </neighbors>
        <restrictions>
            <adjacent generateAnyway="true" chance="0.97" diagonals="true"/>
        </restrictions>
    </tile>
    <tile id="land">
        <color r="0" g="255" b="0"/>
        <neighbors>
            <neighbor type="coast"/>
            <neighbor type="land"/>
        </neighbors>
    </tile>
    <tile id="trail">
        <color r="139" g="69" b="19"/>
        <neighbors>
            <neighbor type="land"/>
            <neighbor type="trail"/>
        </neighbors>
        <restrictions>
            <adjacent generateAnyway="true" chance="0.80" diagonals="false"/>
            <thickness/>
        </restrictions>
    </tile>
</tileset>
"""

finalGrid = []
coordinates_set = set()

# Utility Functions
def delay(ms):
    return asyncio.sleep(ms / 1000)

def set_pixel(x, y, r, g, b, overwrite=False):
    coordinate = (x, y)
    
    if coordinate in coordinates_set:
        if overwrite:
            for pixel in finalGrid:
                if pixel['x'] == x and pixel['y'] == y:
                    pixel['color'] = [r, g, b]
                    break
    else:
        finalGrid.append({'x': x, 'y': y, 'color': [r, g, b]})
        coordinates_set.add(coordinate)

def size_dict(d):
    return len(d)

def get_value_at_index(dict, index):
    keys = list(dict.keys())
    return dict[keys[index]] if 0 <= index < len(keys) else None

# Classes
class Tile:
    def __init__(self, color, neighbors, restrictions, id):
        self.color = color
        self.neighbors = neighbors
        self.restrictions = restrictions
        self.id = id

class Cell:
    def __init__(self, x, y, tile):
        self.x = x
        self.y = y
        self.tile_options = tile[:]
        self.collapsed = False
        self.total_done = False

    def entropy(self):
        return len(self.tile_options)

    def update(self, cell, neighbors, coast):
        options_changed = False
        to_delete = []
        backup = self

        for i in range(len(self.tile_options) - 1, -1, -1):
            opt = self.tile_options[i]
            is_valid_neighbor = cell.tile_options[0].neighbors.__contains__(opt.id)

            if opt.restrictions:
                adjacent_restriction = next(
                    (restriction for restriction in opt.restrictions if restriction['type'] == 'adjacent'), None)
                if adjacent_restriction:
                    is_valid_neighbor = is_valid_neighbor and check_adjacent(
                        neighbors, cell, opt, adjacent_restriction['generateAnyway'],
                        float(adjacent_restriction['chance']),
                        adjacent_restriction['diagonals'] == 'true',
                        len(self.tile_options) == 1
                    )

            if not is_valid_neighbor:
                to_delete.append(opt.id)
                options_changed = True

        while to_delete:
            removable = to_delete.pop()
            index_to_remove = next((index for (index, d) in enumerate(self.tile_options) if d.id == removable), None)
            if index_to_remove is not None:
                del self.tile_options[index_to_remove]

        self.collapsed = len(self.tile_options) == 1

        if not self.tile_options:
            self.tile_options.append(coast)
            print("No options for some reason")

        return options_changed

    def collapse(self):
        if self.collapsed:
            return
        random_index = random.randint(0, size_dict(self.tile_options) - 1)
        self.tile_options = [self.tile_options[random_index]]
        self.collapsed = True

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
                set_pixel(cell.x, cell.y, tile.color['r'], tile.color['g'], tile.color['b'])

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
                            set_pixel(x, y, sea.color['r'], sea.color['g'], sea.color['b'], True)
                        elif has_land:
                            land = next(tile for tile in self.tileset if tile.id == 'land')
                            self.update_cell(x, y, [land], True)
                            set_pixel(x, y, land.color['r'], land.color['g'], land.color['b'], True)
        self.render()

def load_tileset(xml):
    root = ET.fromstring(xml)
    tiles = root.findall('tile')

    tileset = []

    for tile in tiles:
        id = tile.get('id')
        color_element = tile.find('color')
        color = {
            'r': int(color_element.get('r')),
            'g': int(color_element.get('g')),
            'b': int(color_element.get('b'))
        }

        neighbors = [neighbor.get('type') for neighbor in tile.findall('neighbors/neighbor')]

        restrictions = []
        restriction_elements = tile.find('restrictions')
        if restriction_elements is not None:
            for restriction_element in restriction_elements:
                restriction = {key: restriction_element.get(key) for key in restriction_element.keys()}
                restriction['type'] = restriction_element.tag
                restrictions.append(restriction)

        if id == 'coast':
            coast = Tile(color, neighbors, restriction, id)

        tileset.append(Tile(color, neighbors, restrictions, id))

    return tileset

def check_adjacent(neighbors, current_cell, tile_type, generate_anyway, chance, check_diagonals, no_options):
    count = 0
    adjacent_offsets = [
        {'x': -1, 'y': 0},  # left
        {'x': 1, 'y': 0},   # right
        {'x': 0, 'y': -1},  # top
        {'x': 0, 'y': 1}    # bottom
    ]

    diagonal_offsets = [
        {'x': -1, 'y': -1},  # top-left
        {'x': 1, 'y': -1},   # top-right
        {'x': -1, 'y': 1},   # bottom-left
        {'x': 1, 'y': 1}     # bottom-right
    ]

    for offset in adjacent_offsets:
        neighbor = next((n for n in neighbors if n.x == current_cell.x + offset['x'] and n.y == current_cell.y + offset['y']), None)
        if neighbor:
            try:
                if neighbor.collapsed and neighbor.tile_options[0].id == tile_type.id:
                    count += 1
            except Exception as e:
                print("Neighbor", neighbor)

    if check_diagonals and no_options:
        for offset in diagonal_offsets:
            neighbor = next((n for n in neighbors if n.x == current_cell.x + offset['x'] and n.y == current_cell.y + offset['y']), None)
            if neighbor:
                try:
                    if neighbor.collapsed and neighbor.tile_options[0].id == tile_type.id:
                        count += 1
                except Exception as e:
                    print("Neighbor", neighbor)

    if count > 0:
        return True

    has_land = any(n.collapsed and n.tile_options[0].id == "land" for n in neighbors)
    has_sea = any(n.collapsed and n.tile_options[0].id == "sea" for n in neighbors)

    if has_land and has_sea and tile_type.id == "coast":
        return True

    if generate_anyway:
        if random.random() < chance:
            return True

    return False


# class WFCRender:
#     def __init__(self):
#         self.finalGrid = []

#     def get_elements(self):
#         element_list = []
#         for i in range(64):
#             element = self.finalGrid.pop(0)
#             element_list.append(element)

#         print(len(element_list))
#         return element_list
    
#     def start_wfc(self):
#         while True:
#             tileset = load_tileset(xmlstring)
#             grid = Grid(64, tileset)

#             grid.update_cell(24, 24, [tileset[0]], True)

#             while True:
#                 lowest = grid.find_lowest_entropy()
#                 if lowest:
#                     lowest.collapse()
#                 grid.propogate()
#                 grid.render()

#                 if all(cell.collapsed for row in grid.cells for cell in row):
#                     break

#             grid.clean_coasts()

#             print(len(finalGrid))

#             if len(finalGrid) >= 4096:
#                 break

#         self.finalGrid = finalGrid

class WFCRender:
    def __init__(self):
        self.finalGrid = []

    def get_elements(self, index):
        element_list = []
        for i in range(64):
            element = self.finalGrid[(index * 64) + i]
            element_list.append(element)
        # print(len(element_list))
        return element_list
    
    def start_wfc(self):
        global finalGrid, coordinates_set
        
        while True:
            finalGrid = []
            coordinates_set = set()

            tileset = load_tileset(xmlstring)
            grid = Grid(64, tileset)

            grid.update_cell(24, 24, [tileset[0]], True)

            while True:
                lowest = grid.find_lowest_entropy()
                if lowest:
                    lowest.collapse()
                grid.propogate()
                grid.render()

                if all(cell.collapsed for row in grid.cells for cell in row):
                    break

            grid.clean_coasts()

            print(len(finalGrid))

            if len(finalGrid) >= 4096:
                break

        self.finalGrid = finalGrid

if __name__ == "__main__":
    rend = WFCRender()
    print("rendering")
    rend.start_wfc()
    print("Mapping")
    mapp = rend.finalGrid

    print(mapp)
    print(len(mapp))
    print(sys.getsizeof(mapp))