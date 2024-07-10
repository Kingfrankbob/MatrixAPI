import matplotlib.pyplot as plt
import random
from coloring import generate_rainbow_colors

class CoordinateDrawer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.points = []
        self.mirrored_points = []
        self.upmirrored_points = []
        self.uppoints = []

    def draw_point(self, x, y, color='bo'):
        self.points.append((x, y))
        self.ax.plot(x, y, color)

    def draw_line(self, point1, point2, color='r-'):
        x_values = [point1[0], point2[0]]
        y_values = [point1[1], point2[1]]
        self.ax.plot(x_values, y_values, color)

    def continue_line(self, new_point, color='r-'):
        if self.points:
            last_point = self.points[-1]
            self.draw_line(last_point, new_point, color)
            self.points.append(new_point)
        else:
            self.draw_point(new_point[0], new_point[1])

    def show(self):
        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        plt.title('Coordinate Drawer')
        plt.grid(True)
        plt.show()

    def plot_all(self, points_list, color):
        for points in points_list:
            self.ax.plot(*zip(*points), color)

class HilbertCurve:

    U = 1
    R = 2
    D = 3
    L = 4

    def __init__(self, iterations=5, height=2, drawer=None, x=0, y=0, extras=False):
        """
        5 Iterations to fill the whole screen
        4 Iterations and extras to fill the corners
        """
        self.drawer = drawer
        self.x = x
        self.y = y
        self.height = height
        self.iterations = iterations
        self.points = [(1, 1)]
        self.mirrored_points = [(63, 1)]
        self.upmirrored_points = [(63, 63)]
        self.uppoints = [(1, 63)]
        self.extras = extras

    def move(self, j):
        if j == 1:
            self.y -= self.height
        elif j == 2:
            self.x += self.height
        elif j == 3:
            self.y += self.height
        elif j == 4:
            self.x -= self.height

        if self.extras:
            self.upmirrored_points.append((64 - (self.x + 1), 64 - (self.y + 1)))
            self.uppoints.append((self.x + 1, 64 - (self.y + 1)))
            self.mirrored_points.append((64 - (self.x + 1), self.y + 1))

        # self.drawer.continue_line((self.x, self.y))

        self.points.append((self.x + 1, self.y + 1))

    def hilbert(self, right, down, left, up, n):
        if n > 0:
            n -= 1
            self.hilbert(down, right, up, left, n)
            self.move(right)
            self.hilbert(right, down, left, up, n)
            self.move(down)
            self.hilbert(right, down, left, up, n)
            self.move(left)
            self.hilbert(up, left, down, right, n)

    def draw_curve(self):
        self.hilbert(self.R, self.D, self.L, self.U, self.iterations)
        if self.drawer is not None:
            self.drawer.plot_all([self.points, self.mirrored_points, self.upmirrored_points, self.uppoints], 'r-')
            self.drawer.show()

class HilbertHandler:
    def __init__(self, typee, solidorrandom):
        """
        Types 4 is corners, 5 is full
        """
        self.type = typee
        self.solid_or_random = solidorrandom
        if solidorrandom == 0:
            self.rand_color = [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        self.hilbert = HilbertCurve(iterations=typee, extras=typee == 4)
        self.points = []
        self.all_together = random.randint(0, 2) # 1 is all together and 0 is individually
        self.in_order = random.randint(0, 1) # 1 is in order and 0 is random
        self.colors = generate_rainbow_colors(random.randint(0, 1023))
        self.counter = random.randint(0, 256)
        self.four_counter = 0

        print(self.counter, " Counter and length ", len(self.colors))

    def render(self):
        self.hilbert.draw_curve()
        colored_points = []

        if self.type == 5:
            random_num = random.randint(0, 1)
            if random_num > 0.5:
                if len(self.hilbert.points) > 1:
                    index = random.randint(1, len(self.hilbert.points) - 1)
                    self.points = self.hilbert.points[index:] + self.hilbert.points[:index]

            for i in range(1, len(self.hilbert.points)):
                point = self.hilbert.points[i]
                prevpoint = self.hilbert.points[i - 1]
                color = self.assign_color()
                colored_points.append({'x1': prevpoint[0], 'y1': prevpoint[1], 'x2': point[0], 'y2': point[1], 'color': color})
            



        elif self.type == 4:
            self.colors = generate_rainbow_colors(random.randint(0, 20))
            lists = [self.hilbert.points, self.hilbert.mirrored_points, self.hilbert.upmirrored_points, self.hilbert.uppoints]
            if self.all_together == 0 or self.all_together == 2:
                for i in range(1, len(self.hilbert.points)):
                    for lst in lists:
                        if lst:
                            point = lst[i]
                            prevpoint = lst[i - 1]
                            color = self.assign_color()
                            colored_points.append({'x1': prevpoint[0], 'y1': prevpoint[1], 'x2': point[0], 'y2': point[1], 'color': color})
            elif self.all_together == 1:
                for i in range(1, len(self.hilbert.points)):
                    if self.in_order == 0:
                        random.shuffle(lists)
                    for lst in lists:
                        if lst:
                            point = lst[i]
                            prevpoint = lst[i - 1]
                            color = self.assign_color()
                            colored_points.append({'x1': prevpoint[0], 'y1': prevpoint[1], 'x2': point[0], 'y2': point[1], 'color': color})
        if random.random() < 0.1:
            random.shuffle(colored_points)
        self.points = colored_points

    def assign_color(self):
        if self.solid_or_random == 0:
            return self.rand_color
        elif self.solid_or_random == 1:
            return [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]
        elif self.solid_or_random == 2:
            return self.assign_rainbow_color() if self.type == 5 else self.assign_rainbow_color_4type()
        
    def assign_rainbow_color(self):
        counter = self.counter % len(self.colors)
        r = self.colors[counter][0]
        g = self.colors[counter][1]
        b = self.colors[counter][2]
        self.counter += 1
        return [r, g, b]
    
    def assign_rainbow_color_4type(self):
        counter = self.counter % len(self.colors)
        r = self.colors[counter][0]
        g = self.colors[counter][1]
        b = self.colors[counter][2]
        self.four_counter += 1
        if self.four_counter % 4 == 0:
            self.counter += 1
        return [r, g, b]

    def get_elements(self, index):
        return self.points[index * 32:(index + 1) * 32]


if __name__ == "__main__":
    # drawer = CoordinateDrawer()
    # hilbert_curve = HilbertCurve(iterations=4, drawer=drawer, extras=True) # Always 1024 length
    # hilbert_curve.draw_curve()
    # print("Lengths: ", len(hilbert_curve.points), len(hilbert_curve.mirrored_points), len(hilbert_curve.upmirrored_points), len(hilbert_curve.uppoints))
    # print("Original Points: ", hilbert_curve.points)
    # print("Mirrored Points: ", hilbert_curve.mirrored_points)
    # print("Up Mirrored Points: ", hilbert_curve.upmirrored_points)
    # print("Up Points: ", hilbert_curve.uppoints)

    handler = HilbertHandler(5, 2)
    handler.render()
    # for i in range(32):
    #     print(handler.get_elements(i))
    print(len(handler.points))
