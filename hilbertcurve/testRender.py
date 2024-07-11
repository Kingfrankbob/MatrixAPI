from coordinateDrawer import CoordinateDrawer
from hilbertCurve import HilbertCurve

drawer = CoordinateDrawer()
hilbert = HilbertCurve(drawer=drawer)

hilbert.draw_curve()
drawer.show()