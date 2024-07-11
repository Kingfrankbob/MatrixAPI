import asyncio
import sys
from grid import Grid
from staticXMLHandler import load_tileset


def delay(ms):
    return asyncio.sleep(ms / 1000)

class WFCRender:
    def __init__(self):
        self.finalGrid = []

    def get_elements(self, index):
        return self.finalGrid[index * 64:(index + 1) * 64]

    
    def start_wfc(self):
        while True:

            tileset = load_tileset()
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

            # print(len(finalGrid))

            if len(grid.finalGrid) >= 4096:
                break

        self.finalGrid = grid.finalGrid

if __name__ == "__main__":
    rend = WFCRender()
    rend.start_wfc()
    mapp = rend.finalGrid

    # print(mapp)
    print("Final length", len(mapp))
    print("System Size", sys.getsizeof(mapp))