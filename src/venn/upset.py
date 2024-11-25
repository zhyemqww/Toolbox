#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : zhyemqww
# @Time     : 2024/11/19 16:57
# @File     : upset
# @Project  : Toolbox
# @Desc     :
from typing import Iterable

import numpy as np
from matplotlib import pyplot as plt, gridspec

from src.venn.decode_venn_data import decode_venn_data


class Upset:
    def __init__(self):
        self.set_size_sorted = None
        self.set_size_sorted_index = None
        self.intersections = None
        self.intersection_count = None
        self.intersection_order = None
        self.intersection_matrix = None

    def decode_data(self, data: dict[str: set],
                    intersection_sort: bool = True,
                    intersection_sort_reverse: bool = True,
                    set_sort: bool = True,
                    set_sort_reverse: bool = True,
                    ignore_empty_set: bool = True) -> None:
        """
        decode data to generate venn data
        Args:
            data (dict): the data to generate venn data
            intersection_sort (bool):
            intersection_sort_reverse ():
            set_sort ():
            set_sort_reverse ():
            ignore_empty_set (bool):

        Returns:

        """
        # convert the data to the intersection set
        data = {k: set(v) for k, v in data.items()}

        # sort the data set
        if set_sort:
            self.set_size_sorted = sorted(data, key=lambda x: len(data[x]), reverse=set_sort_reverse)
        else:
            self.set_size_sorted = list(data.keys())

        self.set_size_sorted_index = {s: len(self.set_size_sorted) - i for i, s in enumerate(self.set_size_sorted)}

        # sort the intersection set
        self.intersections = decode_venn_data(data)

        if ignore_empty_set:
            self.intersections = {k: v for k, v in self.intersections.items() if v}
        self.intersection_count = len(self.intersections)

        # sort the intersection set
        if intersection_sort:
            self.intersection_order = sorted(self.intersections, key=lambda x: len(self.intersections[x]),
                                             reverse=intersection_sort_reverse)
        else:
            self.intersection_order = list(self.intersections.keys())

        # create the intersection matrix
        self.intersection_matrix = np.zeros((len(self.set_size_sorted), self.intersection_count))
        for i, s in enumerate(self.set_size_sorted):
            for j, inter in enumerate(self.intersection_order):
                if s in inter:
                    self.intersection_matrix[i, j] = self.set_size_sorted_index[s]

    def plot(self, data: dict[str: set],
             figure_size: tuple[float, float] = (10, 6),
             intersection_sort: bool = True,
             intersection_sort_reverse: bool = True,
             set_sort: bool = True,
             set_sort_reverse: bool = True,
             height_ratios: tuple[int, int] = (10, 5),
             width_ratios: tuple[int, int] = (5, 20),
             size_bar_color: str | Iterable = "black",
             intersection_bar_color: str | Iterable= "black",
             intersection_color: str = "black",
             no_intersections_color: str = "lightgray",
             ignore_empty_set: bool = True) -> None:

        self.decode_data(data, intersection_sort, intersection_sort_reverse, set_sort, set_sort_reverse, ignore_empty_set)

        w_space = max([len(s) for s in self.set_size_sorted]) * 0.025 + 0.05

        # plot the upset plot-------------------------------------------------------------------------------------------
        spec = gridspec.GridSpec(2, 2,
                                 height_ratios=height_ratios,
                                 width_ratios=width_ratios,
                                 wspace=w_space,
                                 hspace=0.1)
        fig = plt.figure(figsize=figure_size)

        # 1. plot the set size bar chart ===============================================================================
        ax_set_size_bar = fig.add_subplot(spec[1, 0])
        set_size_sorted_count = [len(data[k]) for k in self.set_size_sorted]
        bars_h = ax_set_size_bar.barh(self.set_size_sorted[::-1], set_size_sorted_count[::-1],
                                      color=size_bar_color,
                                      height=0.7, alpha=1, align='edge')

        # Adjust the starting point of the bar chart to align it from the right
        for bar, value in zip(ax_set_size_bar.patches, set_size_sorted_count[::-1]):
            bar.set_x(value - bar.get_width())

        for bar in bars_h:
            width = bar.get_width()  # gets the width of the column
            ax_set_size_bar.text(width * 1.02,  # x coordinates (slightly to the right of the column)
                                 bar.get_y() + bar.get_height() / 2,  # y coordinates (slightly higher than the column)
                                 f'{width:.0f}',  # displays text formatted as integers
                                 ha='right', va='center')  # text alignment

        ax_set_size_bar.spines["top"].set_visible(False)
        ax_set_size_bar.spines["right"].set_visible(False)
        ax_set_size_bar.spines["bottom"].set_visible(True)
        ax_set_size_bar.spines["left"].set_visible(False)

        # reverse the horizontal axis
        ax_set_size_bar.invert_xaxis()
        ax_set_size_bar.set_yticks([])

        ax_set_size_bar.set_xlabel("Set Size",
                                   fontdict={"fontsize": 14,
                                             "family": "Arial",
                                             "weight": "normal", })

        # 2. plot the intersection bar chart ===========================================================================
        ax_intersection_bar = fig.add_subplot(spec[0, 1])
        bars = ax_intersection_bar.bar(range(self.intersection_count),
                                       [len(self.intersections[inter]) for inter in self.intersection_order],
                                       color=intersection_bar_color,
                                       width=0.7, alpha=1)

        for bar in bars:
            height = bar.get_height()  # gets the height of the post
            ax_intersection_bar.text(bar.get_x() + bar.get_width() / 2,  # x coordinate
                                     height + 0.5,  # Y-coordinate (slightly higher than the column)
                                     f'{height:.0f}',  # displays text formatted as integers
                                     ha='center', va='bottom')  # text alignment

        ax_intersection_bar.spines["top"].set_visible(False)
        ax_intersection_bar.spines["right"].set_visible(False)
        ax_intersection_bar.spines["bottom"].set_visible(True)
        ax_intersection_bar.spines["left"].set_visible(True)

        ax_intersection_bar.set_xticks([])
        ax_intersection_bar.set_xlim(-1, self.intersection_count)

        ax_intersection_bar.set_ylabel("Intersection Size",
                                       fontdict={"fontsize": 14,
                                                 "family": "Arial",
                                                 "weight": "normal", })

        # 3. plot the intersection matrix ==============================================================================
        ax_intersection = fig.add_subplot(spec[1, 1])

        for i in range(len(self.set_size_sorted)):
            color = [intersection_color if i != 0 else no_intersections_color for i in self.intersection_matrix[i]]
            ax_intersection.scatter(range(self.intersection_count),
                                    [len(self.set_size_sorted) - i for _ in range(self.intersection_count)],
                                    color=color, s=80)

        for i in range(self.intersection_matrix.shape[1]):
            inter_sec = [i for i in self.intersection_matrix.T[i] if i != 0]
            if len(inter_sec) != 1:
                max_index = np.max(inter_sec)
                min_index = np.min(inter_sec)
                ax_intersection.plot([i, i], [min_index, max_index], color=intersection_color)

        ax_intersection.set_yticks(range(1, len(self.set_size_sorted) + 1))
        ax_intersection.set_yticklabels(self.set_size_sorted[::-1])
        ax_intersection.set_xticks([])

        ax_intersection.spines["top"].set_visible(False)
        ax_intersection.spines["right"].set_visible(False)
        ax_intersection.spines["bottom"].set_visible(False)
        ax_intersection.spines["left"].set_visible(False)

        alternate_colors = np.zeros((len(self.set_size_sorted), self.intersection_count))
        for i in range(len(self.set_size_sorted)):
            alternate_colors[i, :] = 1 if i % 2 == 0 else 0

        ax_intersection.imshow(alternate_colors, cmap='binary', aspect='auto',
                               extent=(-1, self.intersection_count, 0.5, len(self.set_size_sorted) + 0.5), alpha=0.05,
                               zorder=0)

        ax_intersection.tick_params(length=0, pad=5)

        ax_intersection.set_xlim(-1, self.intersection_count)

        plt.show()


if __name__ == '__main__':
    da = {

        "a": {3, 10, 11, 24, 25, 31, 43, 45, 54, 56, 60, 63, 74, 75, 77, 82, 85, 93, 98, 104, 105, 107, 116, 118, 120,
              126,
              135, 153, 162, 163, 169, 178, 183, 185, 200, 206, 221, 230, 232, 233, 234, 236, 240, 251, 253, 254, 262,
              266,
              268, 274, 277, 280, 283, 286, 289, 294, 295, 297, 309, 314, 324, 325, 327, 333, 337, 339, 348, 355, 366,
              372,
              381, 384, 400, 407, 411, 414, 417, 421, 437, 438, 444, 447, 450, 456, 461, 464, 465, 467, 470, 490, 495,
              496, 3453, 435, 35, 345,
              497, 499},
        "b": {4, 5, 21, 22, 23, 28, 31, 37, 39, 47, 61, 79, 85, 87, 90, 100, 107, 110, 118, 120, 124, 127, 131, 133,
              162, 181,
              185, 204, 205, 209, 212, 218, 220, 229, 232, 237, 247, 248, 257, 262, 263, 267, 268, 270, 280, 281, 289,
              290, 292,
              299, 304, 306, 313, 315, 322, 343, 344, 350, 351, 374, 376, 383, 384, 390, 397, 398, 411, 418, 423, 425,
              427, 428,
              434, 438, 443, 447, 448, 451, 452, 459, 461, 466, 468, 481, 488, 489, 491, 500},
        "c": {2, 9, 18, 22, 35, 53, 57, 61, 64, 74, 76, 78, 99, 110, 111, 113, 114, 124, 128, 137, 140, 141, 143, 146,
              150, 152,
              161, 163, 167, 169, 182, 183, 187, 195, 197, 198, 202, 207, 210, 216, 217, 218, 221, 228, 231, 232, 239,
              240, 241,
              242, 243, 244, 249, 251, 259, 268, 270, 278, 286, 297, 304, 308, 311, 312, 314, 316, 324, 333, 341, 351,
              353, 359,
              365, 372, 379, 383, 397, 404, 407, 415, 416, 424, 429, 430, 432, 433, 436, 438, 441, 445, 457, 467, 468,
              471, 488,
              497, 499},
        "d": {4, 8, 12, 16, 19, 24, 26, 32, 33, 36, 37, 40, 45, 50, "435", 56, 57, 65, 81, 85, 91, 128, 144, 146, 147, 150,
              164,
              165, 167, 169, 170, 173, 176, 180, 181, 200, 201, 205, 207, 212, 218, 221, 223, 230, 244, 246, 247, 250,
              251, 252,
              259, 264, 265, 271, 272, 275, 278, 280, 281, 282, 287, 300, 305, 313, 318, 323, 325, 328, 333, 336, 341,
              343, 345, 23432, 54646, 356, 366, 368, 371, 372, 395, 412, 422, 424, 428, 432, 452, 465, 466, 467, 472,
              356, 366, 368, 371, 372, 395, 412, 422, 424, 428, 432, 452, 465, 466, 467, 472, 480, 487, 493, 498, 500}

    }

    import random


    def generate_random_groups(num_groups=6, num_range=(0, 1000), group_size_range=(1, 20)):
        """
        随机生成指定数量的数字组合。

        :param num_groups: 要生成的数字组合的组数，默认为6
        :param num_range: 每组数字的范围，默认为 (0, 10000)
        :param group_size_range: 每组数字数量的范围，默认为 (1, 20)
        :return: 包含生成结果的列表
        """
        groups = []
        for _ in range(num_groups):
            group_size = 980 # 随机确定当前组的大小
            group = random.sample(range(*num_range), group_size)  # 随机生成一组数字
            groups.append(group)
        return groups


    # 调用函数生成
    data = {}
    random_groups = generate_random_groups()
    for i, group in enumerate(random_groups, 1):
        data[f"zu_{i}"] = group
    print(data)


    us = Upset()
    us.plot(da, set_sort=True, intersection_sort=True, ignore_empty_set=True,
            size_bar_color=["#442255", "#CC6677"],
            intersection_bar_color=["#332288", "#88CCEE"],
            intersection_color="#ff8888",
            no_intersections_color="#8888ff"
            # intersection_bar_color="cyan", size_bar_color='red', intersection_color="blue"
            )
    print(us.intersections)
