#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : zhyemqww
# @Time     : 2024/11/19 15:58
# @File     : __init__.py
# @Project  : Toolbox
# @Desc     :
import matplotlib.pyplot as plt
import numpy as np

# 示例数据
categories = ['A', 'B', 'C', 'D']
values = [5, 7, 3, 6]

# 绘制水平条形图
fig, ax = plt.subplots()

# 设置条形图右对齐
ax.barh(categories, values, align='edge', height=0.6)

# 调整条形图起点，使其从右对齐
for bar, value in zip(ax.patches, values):
    bar.set_x(value - bar.get_width())

# 反转横坐标轴
ax.invert_xaxis()

# 添加标签和标题
ax.set_xlabel('Values')
ax.set_title('Horizontal Bar Chart (Right-Aligned)')

# 显示图形
plt.show()
