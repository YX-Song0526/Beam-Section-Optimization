import numpy as np
from sa3d.section import Section


class Node:
    def __init__(self,
                 x: float,
                 y: float,
                 z: float):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Node(x={self.x}, y={self.y}, z={self.z})"


class Beam:
    def __init__(self,
                 node1: Node,
                 node2: Node,
                 n1: np.ndarray,
                 section: Section):
        """
        初始化三维梁单元类

        Args:
            node1: 节点 1
            node2: 节点 2
            n1: 用于确定梁的摆放姿态
            section: 截面
        """
        self.node1 = node1
        self.node2 = node2
        self.n1 = n1
        self.section = section

        self.t = np.array([node2.x - node1.x,
                           node2.y - node1.y,
                           node2.z - node1.z])

        # 计算单元长度
        self.L = np.linalg.norm(self.t)

        self.K_local = None
        self.K_global = None

    def cal_K_local(self):
        # 杨氏模量和剪切模量
        E, G = self.section.material.E, self.section.material.G

        # 惯性矩
        I1, I2, J = self.section.shape.I

        # 截面积
        A = self.section.shape.A

        # 单元长度
        L = self.L

        # 杆行为
        K_bar = (E * A / L) * np.array([[1, -1],
                                        [-1, 1]])

        # 扭转行为
        K_G = (G * J / L) * np.array([[1, -1],
                                      [-1, 1]])

        # n1 方向的弯曲
        K_B1 = (E * I1 / L ** 3) * np.array([[12, 6 * L, -12, 6 * L],
                                             [6 * L, 4 * L ** 2, -6 * L, 2 * L ** 2],
                                             [-12, -6 * L, 12, -6 * L],
                                             [6 * L, 2 * L ** 2, -6 * L, 4 * L ** 2]])

        # n2 方向的弯曲
        K_B2 = (E * I2 / L ** 3) * np.array([[12, 6 * L, -12, 6 * L],
                                             [6 * L, 4 * L ** 2, -6 * L, 2 * L ** 2],
                                             [-12, -6 * L, 12, -6 * L],
                                             [6 * L, 2 * L ** 2, -6 * L, 4 * L ** 2]])

        K_local = np.zeros((12, 12))

        for i in range(2):
            for j in range(2):
                K_local[6 * i, 6 * j] += K_bar[i, j]
                K_local[6 * i + 3, 6 * j + 3] += K_G[i, j]

        for i in range(4):
            for j in range(4):
                dof = [1, 5, 7, 11]
                K_local[dof[i], dof[j]] += K_B1[i, j]
                dof = [2, 4, 8, 10]
                K_local[dof[i], dof[j]] += K_B2[i, j]

        self.K_local = K_local

    def cal_transfer_matrix(self):
        t = self.t
        t /= np.linalg.norm(t)

        n1 = self.n1
        n1 /= np.linalg.norm(n1)

        n2 = np.cross(t, n1)
        n2 /= np.linalg.norm(n2)

        R = np.array([t,
                      n1,
                      n2])

        T = np.zeros((12, 12))
        for i in range(4):
            T[i * 3:(i + 1) * 3, i * 3:(i + 1) * 3] = R

        return T

    def cal_K_global(self):
        T = self.cal_transfer_matrix()
        K_local = self.K_local
        K_global = T.T @ K_local @ T
        self.K_global = K_global




if __name__ == '__main__':
    node = Node(1.0, 2.0, 3.0)
    print(node)
