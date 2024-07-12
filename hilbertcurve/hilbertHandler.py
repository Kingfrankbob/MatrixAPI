import random
from .hilbertCurve import HilbertCurve
from .coloring import generate_rainbow_colors

class HilbertHandler:
    def __init__(self, typee, solidorrandom):
        """
        Types 4 is corners, 5 is full
        """
        self.type = typee
        self.solid_or_random = solidorrandom
        if solidorrandom == 0:
            self.rand_color = [random.randint(10, 255), random.randint(10, 255), random.randint(10, 255)]
        self.hilbert = HilbertCurve(iterations=typee, extras=typee == 4)
        self.points = []
        self.all_together = random.randint(0, 2) # 1 is all together and 0 is individually
        self.in_order = random.randint(0, 1) # 1 is in order and 0 is random
        self.colors = generate_rainbow_colors(random.randint(0, 1023))
        self.counter = random.randint(0, 256)
        self.four_counter = 0

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
            return [random.randint(10, 255), random.randint(10, 255), random.randint(10, 255)]
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