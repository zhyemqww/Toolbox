#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : zhyemqww
# @Time     : 2024/11/22 19:43
# @File     : volcano
# @Project  : Toolbox
# @Desc     :
from typing import Iterable, Optional

from matplotlib import pyplot as plt
from pandas import DataFrame

class Volcano:
    def __init__(self):
        pass

    @staticmethod
    def plot(data: DataFrame, title: str, x_label: str, y_label: str, fig_size: tuple = (10, 6),
             axes_spine_visibility: Iterable = ("right", 'top'), axes_spine_line_width: float = 1.0,
             y_threshold: Optional[float] = None, x_max_threshold: Optional[float] = None,
             x_min_threshold: Optional[float] = None) -> None:
        """
        Plot a volcano plot.
                x min threshold     x max threshold
                |                   |
            down|                   | up
                |                   |
                |                   |
        --------| ------------------|--------y threshold
                |                   |
                |                   |
                |                   |
        ------------------------------------> x
        Args:
            data (DataFrame): The data.
            title (str): The title.
            x_label (str): The label of x-axis.
            y_label (str): The label of y-axis.
        """
        up = DataFrame()
        down = DataFrame()
        normal = DataFrame()

        if y_threshold is not None:
            if x_max_threshold is not None and x_min_threshold is not None:
                up = data[(data["x"] > x_max_threshold) & (data["y"] > y_threshold)]
                down = data[(data["x"] < x_min_threshold) & (data["y"] > y_threshold)]
            elif x_max_threshold is not None:
                up = data[(data["x"] > x_max_threshold) & (data["y"] > y_threshold)]
            elif x_min_threshold is not None:
                down = data[(data["x"] < x_min_threshold) & (data["y"] > y_threshold)]
            else:
                up = data[data["y"] > y_threshold]
        else:
            if x_max_threshold is not None and x_min_threshold is not None:
                up = data[data["x"] > x_max_threshold]
                down = data[data["x"] < x_min_threshold]
            elif x_max_threshold is not None:
                up = data[data["x"] > x_max_threshold]
            elif x_min_threshold is not None:
                down = data[data["x"] < x_min_threshold]

        normal = data[~data.index.isin(up.index.union(down.index))]

        print(up.columns)
        print(down.columns)
        print(normal.columns)

        print(up)
        print(down)
        print(normal)

        fig, ax = plt.subplots(figsize=fig_size)

        spine_names = ['right', 'top']
        for i, spine_name in enumerate(spine_names):
            ax.spines[spine_name].set_visible(i in axes_spine_visibility)
            ax.spines[spine_name].set_linewidth(axes_spine_line_width)

        ax.set_title(title, fontdict={'size': 16})
        ax.set_xlabel(x_label, fontdict={'size': 12})
        ax.set_ylabel(y_label, fontdict={'size': 12})

        if not normal.empty:
            ax.scatter(normal["x"], normal["y"], s=10, color="#fbb929", picker=True, pickradius=5)
        if not up.empty:
            ax.scatter(up["x"], up["y"], s=10, color="#d42517", picker=True, pickradius=5)
        if not down.empty:
            ax.scatter(down["x"], down["y"], s=10, color="#17d425", picker=True, pickradius=5)

        if y_threshold is not None:
            ax.axhline(y=y_threshold, color='black', label="Y Threshold")

        if x_max_threshold is not None:
            ax.axvline(x=x_max_threshold, color='black', label="X Max Threshold")

        if x_min_threshold is not None:
            ax.axvline(x=x_min_threshold, color='black', label="X Min Threshold")

        plt.show()


if __name__ == '__main__':
    import numpy as np
    import pandas as pd

    data = pd.DataFrame({
        "x": np.random.randn(100),
        "y": np.random.randn(100)
    })

    Volcano.plot(data, "Volcano Plot", "X", "Y", y_threshold=1, x_max_threshold=1, x_min_threshold=-1)








