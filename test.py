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

s.plot_system()