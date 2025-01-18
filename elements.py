import numpy as np
from section import Section
from matrices import K_beam_local, transfer_matrix, M_beam


class Node:
    def __init__(self,
                 x: float,
                 y: float):
        self.x = x
        self.y = y


class Beam:
    def __init__(self,
                 node1: Node,
                 node2: Node,
                 section: Section):
        """
        二维钢架单元初始化

        Args:
            node1: 节点1
            node2: 节点2
            section: 截面

        """
        self.node1 = node1
        self.node2 = node2
        self.section = section

        # 计算单元长度
        self.L = np.sqrt((node2.x - node1.x) ** 2 +
                         (node2.y - node1.y) ** 2)

        # 偏转角（相对于整体x坐标的正方向）
        self.Phi = np.arctan2((node2.y - node1.y), (node2.x - node1.x))

        self.K_local = None
        self.K_global = None
        self.M_e = None

        self.update()

    def update(self):
        E = self.section.material.E
        rho = self.section.material.rho
        A = self.section.shape.A
        I = self.section.shape.I
        self.K_local = K_beam_local(E, A, I, self.L)
        self.K_global = transfer_matrix(self.Phi).T @ self.K_local @ transfer_matrix(self.Phi)
        self.M_e = M_beam(rho, A, self.L)

    def update_shape_params(self, **kwargs):
        self.section.update_shape_params(**kwargs)
        self.update()
