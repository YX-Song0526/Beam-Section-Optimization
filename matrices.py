import numpy as np
from numpy import cos, sin


def big_mat(E, A, I, L):
    """
    二维钢架单元的局部单元刚度矩阵

    Args:
        E: 杨氏模量
        A: 截面积
        I: 惯性矩
        L: 单元长度

    Returns:
        6×6 单元刚度矩阵

    """
    return np.array([[E * A / L, 0, 0, -E * A / L, 0, 0],
                     [0, 12 * E * I / L ** 3, 6 * E * I / L ** 2, 0, -12 * E * I / L ** 3, 6 * E * I / L ** 2],
                     [0, 6 * E * I / L ** 2, 4 * E * I / L, 0, -6 * E * I / L ** 2, 2 * E * I / L],
                     [-E * A / L, 0, 0, E * A / L, 0, 0],
                     [0, -12 * E * I / L ** 3, -6 * E * I / L ** 2, 0, 12 * E * I / L ** 3, -6 * E * I / L ** 2],
                     [0, 6 * E * I / L ** 2, 2 * E * I / L, 0, -6 * E * I / L ** 2, 4 * E * I / L]])


def transfer_matrix(phi):
    """
    二维钢架单元坐标转换矩阵

    Args:
        phi: 单元相对于全局x坐标正方向的偏转角（单位为弧度）

    Returns:
        6×6 的坐标转换矩阵

    """
    return np.array([[cos(phi), sin(phi), 0, 0, 0, 0],
                     [-sin(phi), cos(phi), 0, 0, 0, 0],
                     [0, 0, 1, 0, 0, 0],
                     [0, 0, 0, cos(phi), sin(phi), 0],
                     [0, 0, 0, -sin(phi), cos(phi), 0],
                     [0, 0, 0, 0, 0, 1]])
