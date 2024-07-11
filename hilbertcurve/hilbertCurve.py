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
