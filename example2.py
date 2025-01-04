import numpy as np
from scipy.optimize import minimize
from systems import Frame2D
from section import *

# --------------------创建系统--------------------
s = Frame2D()

# 创建材料
steel = Material(E=210e9, rho=8000)

# 创建截面，给一个初始的圆截面
section_1 = Section(material=steel, shape=Circle(0.05))

# 添加节点
s.add_node(-4., 0.)  # node1
s.add_node(0., 0.)  # node2
s.add_node(2., 0.)  # node3
s.add_node(0., 2.)  # node4
s.add_node(0., 4.)  # node5

# 添加钢架并指定截面
s.add_element(1, 5, section_1)  # e1
s.add_element(2, 4, section_1)  # e2
s.add_element(4, 5, section_1)  # e3
s.add_element(4, 3, section_1)  # e4

# 添加边界条件
s.add_fixed_sup(1, 2, 3)

# 添加力
s.add_single_force(5, Fx=200000, Fy=-50000)
s.add_single_moment(5, M=5000)


# -----------------------------------------------

# --------------------优化函数--------------------
def structure_weight(R: np.ndarray):
    G = 0
    for i, e in enumerate(s.elements):
        e.update_shape_params(R=R[i])
        rho = e.section.material.rho
        A = e.section.shape.A
        L = e.L
        G += rho * A * L

    return G


def F(R: np.ndarray):
    for i, e in enumerate(s.elements):
        e.update_shape_params(R=R[i])
    max_stress = s.get_max_stress()
    return max_stress


tol = 100e6


def func(r): return structure_weight(r)


cons = ({'type': 'ineq', 'fun': lambda r: tol - F(r)})

r0 = np.array([0.01,
               0.01,
               0.01,
               0.01])

# 定义截面半径的边界
bounds = [(0.001, 0.05),
          (0.001, 0.05),
          (0.001, 0.05),
          (0.001, 0.05)]

res = minimize(func, r0, method='SLSQP', constraints=cons, bounds=bounds)
print("最小值:", res.fun)
print("最优解:", res.x)
print("迭代终止是否成功", res.success)
print("迭代终止原因", res.message)

print(F(res.x))
