import random

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
        random_index = random.randint(0, len(self.tile_options) - 1)
        self.tile_options = [self.tile_options[random_index]]
        self.collapsed = True

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

