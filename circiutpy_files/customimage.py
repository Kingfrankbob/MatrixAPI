import displayio

class CustomImage:
    def __init__(self, width, height, total_colors):
        self.width = width
        self.height = height
        self.bitmap = displayio.Bitmap(width, height, total_colors)
        self.palette = displayio.Palette(total_colors)
        self.palette[0] = (0, 0, 0)  # Set default background color
        self.index_set = 2  # Initial index for new colors
    
    def set_pixel(self, x, y, color):
        try:
            if 0 <= x < self.width and 0 <= y < self.height:
                self.bitmap[x, y] = self.set_color_and_get(color)
        except Exception as e:
            # pass
            print("Index out of range In Method Pixel", e)

    def set_color_and_get(self, color):
        try:
            color_hex = (color[0], color[1], color[2])
            # print(color_hex)

            if color_hex in self.palette:
                print("COLRO ALREAYD EXIST")

            for i in range(len(self.palette)):
                # print(i, self.palette[i])
                if self.palette[i] == self.rgb2hex(color[0], color[1], color[2]):
                    # print("COLRO ALREAYD EXIST")
                    return i
            self.palette[self.index_set] = color_hex
            index = self.index_set
            self.index_set += 1
            return index
        except Exception as e:
            # pass
            print("Index out of range In Method Color", e, self.index_set, len(self.palette))

    def rgb2hex(self, r, g, b):
        return (r << 16) + (g << 8) + b
    
    def set_pixels(self, pixel_data):
        for y in range(min(self.height, len(pixel_data))):
            for x in range(min(self.width, len(pixel_data[y]))):
                self.set_pixel(x, y, pixel_data[y][x])

    def set_row(self, row, pixel_data):
        index = 0
        try:
            for x in range(min(self.width, len(pixel_data))):
                index = x
                self.set_pixel(x, row, pixel_data[x])
        except Exception as e:
            print(index, "Index out of range In Method", e)

    def get_group(self):
        tile_grid = displayio.TileGrid(self.bitmap, pixel_shader=self.palette)
        group = displayio.Group()
        group.scale = 1
        group.x = 0
        group.y = 0
        group.append(tile_grid)
        return group
    
