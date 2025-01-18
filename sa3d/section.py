from sa3d.shape import *


class Material:
    def __init__(self,
                 E: float,
                 niu: float = None,
                 rho: float = None):
        self.E = E
        self.niu = niu
        self.rho = rho
        self.G = E / (2 * (1 + niu)) if niu is not None else None


class Section:
    def __init__(self, material: Material, shape: Shape):
        self.material = material
        self.shape = shape

    def update_shape_params(self, **kwargs):
        self.shape.update(**kwargs)
