import numpy as np
from numpy import cos, sin


def K_beam_local(E, A, I, L):
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


def M_beam(rho, A, L):
    """
    二维钢架单元质量矩阵

    Args:
        rho: 质量密度
        A: 截面积
        L: 单元长度

    Returns:
        6×6 单元质量矩阵

    """
    M_e = rho * A * L * np.array(
        [[1 / 3, 0, 0, 1 / 6, 0, 0],
         [0, 13 / 35, 11 * L / 210, 0, 9 / 70, -13 * L / 420],
         [0, 11 * L / 210, L ** 2 / 105, 0, 13 * L / 420, -L ** 2 / 140],
         [1 / 6, 0, 0, 1 / 3, 0, 0],
         [0, 9 / 70, 13 * L / 420, 0, 13 / 35, -11 * L / 210],
         [0, -13 * L / 420, -L ** 2 / 140, 0, -11 * L / 210, L ** 2 / 105]]
    )

    return M_e


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
