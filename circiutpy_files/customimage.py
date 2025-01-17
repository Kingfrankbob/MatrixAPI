import displayio
import gc

class CustomImage:
    def __init__(self, width, height, total_colors):
        self.width = width
        self.height = height
        self.total_colors = total_colors
        self.bitmap = displayio.Bitmap(width, height, total_colors)
        self.palette = displayio.Palette(total_colors)
        self.palette[0] = (0, 0, 0)
        self.index_set = 2 
    
    def set_pixel(self, x, y, color):
        if 0 <= x < self.width and 0 <= y < self.height:
            self.bitmap[x, y] = self.set_color_and_get(color)
            # print("Set pixel", x, y, color, self.bitmap[x, y])


    def set_color_and_get(self, color):
        color_hex = (color[0], color[1], color[2])

        for i in range(len(self.palette)):
            if self.palette[i] == self.rgb2hex(color[0], color[1], color[2]):
                return i
        self.palette[self.index_set] = color_hex
        index = self.index_set
        self.index_set += 1
        del color_hex
        gc.collect()
        return index


    def rgb2hex(self, r, g, b):
        return (r << 16) + (g << 8) + b
    
    def set_pixels(self, pixel_data):
        for y in range(min(self.height, len(pixel_data))):
            for x in range(min(self.width, len(pixel_data[y]))):
                self.set_pixel(x, y, pixel_data[y][x])

    def set_row(self, row, pixel_data):
        for x in range(min(self.width, len(pixel_data))):
            self.set_pixel(x, row, pixel_data[x])

    def get_group(self):
        tile_grid = displayio.TileGrid(self.bitmap, pixel_shader=self.palette)
        group = displayio.Group()
        group.scale = 1
        group.x = 0
        group.y = 0
        group.append(tile_grid)
        del tile_grid
        gc.collect()
        return group
    
    def clear(self):
        self.bitmap = displayio.Bitmap(self.width, self.height, self.total_colors)
        self.palette = displayio.Palette(self.total_colors)
        self.palette[0] = (0, 0, 0)
        self.index_set = 2
        gc.collect()
    
    def set_color_amount(self, amount):
        self.palette = displayio.Palette(amount)
        self.palette[0] = (0, 0, 0)
        self.index_set = 2

    def draw_line(self, x1, y1, x2, y2, color):
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            self.set_pixel(x1, y1, color)
            if x1 == x2 and y1 == y2:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy