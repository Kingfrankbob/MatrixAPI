import math
from datetime import datetime
from .font import FONT

class LEDMatrix:

    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.matrix = [[[0, 0, 0] for _ in range(width)] for _ in range(height)]

    def print_text(self, text, x, y, color):
        """
        Pritns text based off of the matrixes found in the FONT dict
        """
        for char in text:
            if char in FONT:
                self._draw_char(char, x, y, color)
                x += 6 
            if x >= self.width:
                break

    def _draw_char(self, char, x, y, color):
        """
        Draw a char from the font matrix
        """
        char_bitmap = FONT[char]
        for row in range(7):
            for col in range(5):
                if char_bitmap[row][col] == 1:
                    if 0 <= y + row < self.height and 0 <= x + col < self.width:
                        self.set_pixel(x + col, y + row, color)

    def clear(self):
        """
        Sets all elements in the canvas to [0, 0, 0]
        """
        self.matrix = [[[0, 0, 0] for _ in range(self.width)] for _ in range(self.height)]

    def print(self):
        """
        Prints the 'canvas' to the matrix
        """
        for row in range(self.height):
            for col in range(self.width):
                if self.matrix[row][col] != [0, 0, 0]:
                    print('.', end='')
                else:
                    print('#', end='')
            print("END")

    def display_icon(self, icon_name, x, y):
        """
        Draw a premade icon on the canvas, some icons are:
        sun_icon, cloud_icon, rain_icon, and snow_icon
        """
        if icon_name == "sun_icon":
            self.draw_circle(x + 5, y + 5, 5, [255, 255, 0], True) 
            self.draw_circle(x+5,y+5, 2, [255, 136, 0], True)
            self.draw_line(x + 5, y + 5, x + 5, y + 15, [255, 255, 0])  
            self.draw_line(x + 5, y + 5, x + 15, y + 5, [255, 255, 0])
            self.draw_line(x + 5, y + 5, x - 5, y + 5, [255, 255, 0])
            self.draw_line(x + 5, y + 5, x + 5, y - 5, [255, 255, 0])
            self.draw_line(x - 4, y - 4, x + 14, y + 14, [255, 255, 0])
            self.draw_line(x + 14, y - 4, x - 4, y + 14, [255, 255, 0])

        elif icon_name == "cloud_icon":
            self.draw_circle(x + 17, y, 5, [230, 230, 230], True)
            self.draw_circle(x + 12, y, 5, [230, 230, 230], True)
            self.draw_circle(x+7, y, 5, [230, 230, 230], True)

            self.draw_circle(x + 10, y + 5, 5, [192, 192, 192], True)
            self.draw_circle(x + 5, y + 5, 5, [192, 192, 192], True)
            self.draw_circle(x, y + 5, 5, [192, 192, 192], True)

            self.draw_circle(x + 40, y + 3, 5, [192, 192, 192], True)
            self.draw_circle(x + 35, y + 3, 5, [192, 192, 192], True)
            self.draw_circle(x + 30, y + 3, 5, [192, 192, 192], True)

            self.draw_circle(x + 52, y, 5, [255,255,255], True)
            self.draw_circle(x + 45, y, 5, [255,255,255], True)
            self.draw_circle(x + 38, y, 5, [255,255,255], True)

        elif icon_name == "rain_icon":

            self.draw_circle(x + 13, y-2, 3, [192, 192, 192], True)
            self.draw_circle(x + 8, y-2, 3, [192, 192, 192], True)
            self.draw_circle(x + 3, y-2, 3, [192, 192, 192], True)
            self.draw_circle(x + 19, y-2, 3, [192, 192, 192], True)
            self.draw_circle(x + 24, y-2, 3, [192, 192, 192], True)
            self.draw_circle(x + 29, y-2, 3, [192, 192, 192], True)
            self.draw_circle(x + 39, y-2, 3, [192, 192, 192], True)
            self.draw_circle(x + 44, y-2, 3, [192, 192, 192], True)
            self.draw_circle(x + 49, y-2, 3, [192, 192, 192], True)


            self.draw_line(x, y, x+63, y, [0, 0, 0])
            self.draw_line(x, y+1, x+63, y+1, [0, 0, 0])


            self.draw_line(x+1, y, x + 4, y + 5, [0, 0, 255])  
            self.draw_line(x + 4, y, x + 7, y + 5, [0, 0, 255])
            self.draw_line(x + 7, y, x + 10, y + 5, [0, 0, 255])
            self.draw_line(x + 10, y, x + 13, y + 5, [0, 0, 255])
            self.draw_line(x + 13, y, x + 16, y + 5, [0, 0, 255])
            self.draw_line(x + 18, y, x + 21, y + 5, [0, 0, 255])
            self.draw_line(x + 21, y, x + 24, y + 5, [0, 0, 255])
            self.draw_line(x + 24, y, x + 27, y + 5, [0, 0, 255])
            self.draw_line(x + 27, y, x + 30, y + 5, [0, 0, 255])
            self.draw_line(x + 30, y, x + 33, y + 5, [0, 0, 255])
            self.draw_line(x + 38, y, x + 41, y + 5, [0, 0, 255])
            self.draw_line(x + 41, y, x + 44, y + 5, [0, 0, 255])
            self.draw_line(x + 44, y, x + 47, y + 5, [0, 0, 255])
            self.draw_line(x + 47, y, x + 50, y + 5, [0, 0, 255])
            self.draw_line(x + 50, y, x + 53, y + 5, [0, 0, 255])


        elif icon_name == "snow_icon":
            self.draw_circle(x + 4, y + 5, 3, [255, 255, 255], True) 
            self.draw_circle(x + 9, y + 10, 3, [255, 255, 255])
            self.draw_circle(x-1, y + 10, 3, [255, 255, 255])
            self.draw_circle(x + 14, y + 5, 3, [255, 255, 255], True)
            self.draw_circle(x + 19, y+10, 3, [255, 255, 255], True) 
            self.draw_circle(x + 24, y + 5, 3, [255, 255, 255])
            self.draw_circle(x + 29, y + 10, 3, [255, 255, 255], True)
            self.draw_circle(x + 34, y + 5, 3, [255, 255, 255], True)
            self.draw_circle(x + 39, y+10, 3, [255, 255, 255])
            self.draw_circle(x + 44, y + 5, 3, [255, 255, 255])
            self.draw_circle(x + 49, y + 10, 3, [255, 255, 255])
            self.draw_circle(x + 54, y + 5, 3, [255, 255, 255], True)

    def draw_wind_dir(self, x, y, angle):
        """
        Draws a diameter 8LED compass with a needle pointing the correct direction
        """

        self.draw_circle(x+16, y+17, 8, [255, 255, 255], True)

        print(angle)

        length = 7
        end_x = x + 16 + length * math.cos(math.radians(angle))
        end_y = y + 17 - length * math.sin(math.radians(angle))
        
        self.draw_line(x + 16, y + 17, round(end_x), round(end_y), [255, 0, 0])


    def draw_line(self, x1, y1, x2, y2, color):
        """
        Draw a line of color from x1, y1 to x2, y2
        """
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy
        
        while True:
            self.set_pixel(x1, y1, color)
            
            if x1 == x2 and y1 == y2:
                break
            
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy

    def draw_circle(self, x0, y0, radius, color, fill=False):
        """
        Set what you want the origin of the circle
        to be at the X and Y coordinates
        """
        x = radius
        y = 0
        err = 0
        
        while x >= y:
            if fill:
                for i in range(x0 - x, x0 + x + 1):
                    self.set_pixel(i, y0 + y, color)
                    self.set_pixel(i, y0 - y, color)
                for i in range(x0 - y, x0 + y + 1):
                    self.set_pixel(i, y0 + x, color)
                    self.set_pixel(i, y0 - x, color)
            else:
                self.set_pixel(x0 + x, y0 + y, color)
                self.set_pixel(x0 + y, y0 + x, color)
                self.set_pixel(x0 - y, y0 + x, color)
                self.set_pixel(x0 - x, y0 + y, color)
                self.set_pixel(x0 - x, y0 - y, color)
                self.set_pixel(x0 - y, y0 - x, color)
                self.set_pixel(x0 + y, y0 - x, color)
                self.set_pixel(x0 + x, y0 - y, color)
            
            y += 1
            err += 1 + 2 * y
            if 2 * (err - x) + 1 > 0:
                x -= 1
                err += 1 - 2 * x

    def set_pixel(self, x, y, color):
        self.matrix[y][x] = color
    
    def draw_clock(self):
        """
        Here we are assuimg the whole screen needs to be drawn to do so
        """
        now = datetime.now()
        hour = now.hour % 12 
        minute = now.minute
        
        self.draw_circle(29, 29, 27, [255, 255, 255], fill=True)
        self.draw_circle(29, 29, 27, [0, 0, 0])
        
        hour_angle = 360 * (hour / 12.0) + (360 / 12.0) * (minute / 60.0)
        hour_hand_length = 27 // 2
        hour_hand_end_x = 29 + hour_hand_length * math.cos(math.radians(90 - hour_angle))
        hour_hand_end_y = 29 - hour_hand_length * math.sin(math.radians(90 - hour_angle))
        self.draw_line(29, 29, round(hour_hand_end_x), round(hour_hand_end_y), [0, 0, 0])
        
        minute_angle = 360 * (minute / 60.0)
        minute_hand_length = 27 - 3
        minute_hand_end_x = 29 + minute_hand_length * math.cos(math.radians(90 - minute_angle))
        minute_hand_end_y = 29 - minute_hand_length * math.sin(math.radians(90 - minute_angle))
        self.draw_line(29, 29, round(minute_hand_end_x), round(minute_hand_end_y), [0, 0, 0])
        
        digital_time = now.strftime("%I:%M %p")
        self.print_text(digital_time, 9, 57, [255, 255, 255])

    def draw_color_array(self, x, y, array):
        """
        Draw an array of colors
        """
        for row in range(len(array)):
            for col in range (len(array[row])):
                self.set_pixel(x + col, y + row, array[row][col])
