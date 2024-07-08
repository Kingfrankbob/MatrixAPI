import matplotlib.pyplot as plt

class CoordinateDrawer:
    def __init__(self):
        self.fig, self.ax = plt.subplots()
        self.points = []

    def draw_point(self, x, y):
        self.points.append((x, y))
        self.ax.plot(x, y, 'bo')  # Draw point

    def draw_line(self, point1, point2):
        x_values = [point1[0], point2[0]]
        y_values = [point1[1], point2[1]]
        self.ax.plot(x_values, y_values, 'r-')  # Draw line

    def continue_line(self, new_point):
        if self.points:
            last_point = self.points[-1]
            self.draw_line(last_point, new_point)
            self.points.append(new_point)
        else:
            self.draw_point(new_point[0], new_point[1])

    def show(self):
        plt.xlabel('X axis')
        plt.ylabel('Y axis')
        plt.title('Coordinate Drawer')
        plt.grid(True)
        plt.show()

class Hilbert_Curve:

    U = 1
    R = 2
    D = 3
    L = 4

    def __init__(self, iterations=4, height=3, drawer=None):
        # self.size = size
        self.drawer = drawer
        self.x = 0
        self.y = 0
        self.height = height
        self.iterations = iterations

    def move(self, j):
        if j == 1:
            self.y -= self.height
        elif j == 2:
            self.x += self.height
        elif j == 3:
            self.y += self.height
        elif j == 4:
            self.x -= self.height

        # print("x: ", self.x, "y: ", self.y)

        self.drawer.continue_line((self.x, self.y))
        # self.drawer.show()

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
        self.drawer.show()

if __name__ == "__main__":
    drawer = CoordinateDrawer()
    hilbert_curve = Hilbert_Curve(iterations=4, drawer=drawer)
    hilbert_curve.draw_curve()
    # drawer.show()


