from abc import ABC, abstractmethod
from numpy import pi


class Shape(ABC):
    def __init__(self):
        self.A: float = 0.0  # 面积
        self.I: list = [0.0, 0.0, 0.0]  # 惯性矩([I1, I2, J])
        self.parameters: dict = {}  # 存储形状参数

    @abstractmethod
    def update(self, **kwargs):
        """
        更新截面形状参数，采用关键字参数
        """
        pass  # 每个子类需要实现自己的更新方法

    @abstractmethod
    def recalculate(self):
        """
        根据当前参数重新计算面积、惯性矩和其他属性
        """
        pass

    @classmethod
    def get_parameters(cls) -> dict[str, str]:
        """
        返回每个形状类的参数名称和说明，方便用户了解哪些参数是可更新的。
        """
        raise NotImplementedError("子类需要实现 get_parameters 方法")


class Circle(Shape):
    def __init__(self, R: float):
        super().__init__()
        self.parameters['R'] = R
        self.update(R=R)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            # 更新参数
            self.parameters[key] = value

        # 更新截面积，惯性矩和y_max
        self.recalculate()

    def recalculate(self):
        R = self.parameters['R']
        self.A = pi * R ** 2
        I1 = pi * R ** 4 / 4
        I2 = I1  # pi * R ** 4 / 4
        J = pi * R ** 4 / 2
        self.I = [I1, I2, J]
        # self.y_max = R

    @classmethod
    def get_parameters(cls) -> dict[str, str]:
        return {
            'R': '圆的半径'
        }


class Rectangle(Shape):
    def __init__(self, b: float, h: float):
        super().__init__()
        self.parameters['b'] = b
        self.parameters['h'] = h
        self.update(b=b, h=h)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            # 更新参数
            self.parameters[key] = value
        # 更新面积、惯性矩和最大y值
        self.recalculate()

    def recalculate(self):
        b = self.parameters['b']
        h = self.parameters['h']
        self.A = b * h
        I1 = b * h ** 3 / 12
        I2 = h * b ** 3 / 12
        J = (h * b ** 3 + b * h ** 3) / 12
        self.I = [I1, I2, J]

    @classmethod
    def get_parameters(cls) -> dict[str, str]:
        return {
            'b': '矩形的宽度',
            'h': '矩形的高度'
        }
