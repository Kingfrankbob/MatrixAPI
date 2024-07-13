import matplotlib.pyplot as plt

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