#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : zhyemqww
# @Time     : 2024/4/22 15:10
# @File     : decode_venn_data
# @Project  : MALDI_Decipher
# @Desc     :
import itertools
from typing import Iterable


def decode_venn_data(data: dict) -> dict[tuple: set]:
    """
    Decode the venn data
    :param data: A dictionary where the keys are identifiers and the values are sets
    :return: A dictionary with keys as combinations of identifiers and values as the intersection sets
    """
    # change the data to set
    data = {k: set(v) if not isinstance(v, set) else v for k, v in data.items()}

    # calculate the level of the data
    intersections = {}
    for level in range(len(data), 0, -1):
        data, intersection = cal_intersection(data.keys(), data, level)
        intersections.update(intersection)

    return intersections


def cal_intersection(elements: Iterable, data: dict, level: int) -> tuple[dict, dict[tuple, set]]:
    """
    Calculate the intersection of the combination
    :param elements: List of elements (keys from the data dict)
    :param data: Current dictionary of sets
    :param level: Current level of combination
    :return: Updated data and the intersections for the current level
    """
    # calculate the intersection of the combination
    intersection_data = {}
    combinations = itertools.combinations(elements, level)
    for combination in combinations:
        intersection = set.intersection(*[data[ele] for ele in combination])
        intersection_data[combination] = intersection

    # update the data
    for key, value in data.items():
        incl = [v for k, v in intersection_data.items() if key in k]
        if incl:
            data[key] = value - set.union(*incl)

    return data, intersection_data


if __name__ == '__main__':
    # da = {
    #     "a": set([randint(1, 500) for _ in range(100)]),
    #     "b": set([randint(1, 500) for _ in range(100)]),
    #     "c": set([randint(1, 500) for _ in range(100)]),
    #     "d": set([randint(1, 500) for _ in range(100)]),
    # }
    # print(da['a'])
    # print(da['b'])
    # print(da['c'])
    # print(da['d'])
    # # data = {'a': {1, 2, 3, 4, 5}, 'b': {8, 9, 4, 5}, 'c': {10, 11, 12}}
    # data = {'a': {1, 2, 3}, 'b': {8, 9}, 'c': {10, 11, 12}}
    # da = cal_intersection(data.keys(), data, 2)
    #
    # print(da)
    #
    # for i in range(4, 1, -1):
    #     print(i)
    da = {

        "a" : {3, 10, 11, 24, 25, 31, 43, 45, 54, 56, 60, 63, 74, 75, 77, 82, 85, 93, 98, 104, 105, 107, 116, 118, 120, 126,
         135, 153, 162, 163, 169, 178, 183, 185, 200, 206, 221, 230, 232, 233, 234, 236, 240, 251, 253, 254, 262, 266,
         268, 274, 277, 280, 283, 286, 289, 294, 295, 297, 309, 314, 324, 325, 327, 333, 337, 339, 348, 355, 366, 372,
         381, 384, 400, 407, 411, 414, 417, 421, 437, 438, 444, 447, 450, 456, 461, 464, 465, 467, 470, 490, 495, 496,
         497, 499},
    "b" :{4, 5, 21, 22, 23, 28, 31, 37, 39, 47, 61, 79, 85, 87, 90, 100, 107, 110, 118, 120, 124, 127, 131, 133, 162, 181,
     185, 204, 205, 209, 212, 218, 220, 229, 232, 237, 247, 248, 257, 262, 263, 267, 268, 270, 280, 281, 289, 290, 292,
     299, 304, 306, 313, 315, 322, 343, 344, 350, 351, 374, 376, 383, 384, 390, 397, 398, 411, 418, 423, 425, 427, 428,
     434, 438, 443, 447, 448, 451, 452, 459, 461, 466, 468, 481, 488, 489, 491, 500},
    "c" : {2, 9, 18, 22, 35, 53, 57, 61, 64, 74, 76, 78, 99, 110, 111, 113, 114, 124, 128, 137, 140, 141, 143, 146, 150, 152,
     161, 163, 167, 169, 182, 183, 187, 195, 197, 198, 202, 207, 210, 216, 217, 218, 221, 228, 231, 232, 239, 240, 241,
     242, 243, 244, 249, 251, 259, 268, 270, 278, 286, 297, 304, 308, 311, 312, 314, 316, 324, 333, 341, 351, 353, 359,
     365, 372, 379, 383, 397, 404, 407, 415, 416, 424, 429, 430, 432, 433, 436, 438, 441, 445, 457, 467, 468, 471, 488,
     497, 499},
    "d":{4, 8, 12, 16, 19, 24, 26, 32, 33, 36, 37, 40, 45, 50, 53, 56, 57, 65, 81, 85, 91, 128, 144, 146, 147, 150, 164,
     165, 167, 169, 170, 173, 176, 180, 181, 200, 201, 205, 207, 212, 218, 221, 223, 230, 244, 246, 247, 250, 251, 252,
     259, 264, 265, 271, 272, 275, 278, 280, 281, 282, 287, 300, 305, 313, 318, 323, 325, 328, 333, 336, 341, 343, 345,
     356, 366, 368, 371, 372, 395, 412, 422, 424, 428, 432, 452, 465, 466, 467, 472, 480, 487, 493, 498, 500}

    }

    result = decode_venn_data(da)
    for k, v in result.items():
        print(k, len(v))
