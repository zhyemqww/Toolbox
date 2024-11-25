#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : zhyemqww
# @Time     : 2024/4/24 14:38
# @File     : venn_utils
# @Project  : MALDI_Decipher
# @Desc     :

import math


def cal_distance(s1: float, s2: float, a: float, tol: float = 1e-6, max_iteration: int = 10000,
                 normalization: bool = True) -> tuple[float, float, float]:
    """
    Calculate the distance between two circles
    :param normalization:
    :param s1:
    :param s2:
    :param a:
    :param tol:
    :param max_iteration:
    :return: r1, r2, distance
    """
    # check the input
    s1 = s1 + a
    s2 = s2 + a

    if s1 < 0 or s2 < 0 or a < 0:
        raise Exception("The area must be positive")

    # calculate the radius of the two circles and normalization
    if normalization:
        R1 = math.sqrt(s1 / math.pi)
        R2 = math.sqrt(s2 / math.pi)

        r1 = R1 / max(R1, R2)
        r2 = R2 / max(R1, R2)
        a = a / max(R1, R2) ** 2
    else:
        r1 = math.sqrt(s1 / math.pi)
        r2 = math.sqrt(s2 / math.pi)

    # if a is zero, return the sum of the radius
    if a == 0:
        return r1, r2, r1 + r2
    if a > min(s1, s2):
        raise Exception("The intersection area is larger than the smallest circle")
    if a == min(s1, s2):
        if s1 >= s2:
            return r1, r2, r1 - r2
        else:
            return r1, r2, r2 - r1
    else:
        # calculate the area of the intersection
        """
        lens area formula
        S1 = π * r1^2
        S2 = π * r2^2
        The distance between the centers of the circles is d
        A = r1^2 * arccos((d^2 + r1^2 - r2^2) / (2 * d * r1)) + 
            r2^2 * arccos((d^2 + r2^2 - r1^2) / (2 * d * r2)) - 
            1/2 * sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2))

        """

        def area(d: float) -> float:
            return (r1 ** 2 * math.acos((d ** 2 + r1 ** 2 - r2 ** 2) / (2 * d * r1)) +
                    r2 ** 2 * math.acos((d ** 2 + r2 ** 2 - r1 ** 2) / (2 * d * r2)) -
                    1 / 2 * math.sqrt((-d + r1 + r2) * (d + r1 - r2) * (d - r1 + r2) * (d + r1 + r2)))

        iteration = 0
        distance = max(r1, r2)  # initial distance
        while True:
            iteration += 1
            if iteration > max_iteration:
                break
            if abs(area(distance) - a) < tol:
                break
            if area(distance) > a:
                distance = distance * 1.01
            else:
                distance = distance * 0.99

        return r1, r2, distance


def cal_intersection_points_cc(a1: float, b1: float, r1: float, a2: float, b2: float, r2: float) -> tuple[
    tuple[float, float], tuple[float, float]]:
    """
    Calculate the intersection points of two circles
    :param a1: x of the center of the first circle
    :param b1: y of the center of the first circle
    :param r1: radius of the first circle
    :param a2: x of the center of the second circle
    :param b2: y of the center of the second circle
    :param r2: radius of the second circle
    :return: intersection points
    """
    # calculate the distance between the two centers
    d = math.sqrt((a1 - a2) ** 2 + (b1 - b2) ** 2)
    if d > r1 + r2:
        raise Exception("The two circles do not intersect")
    if d < abs(r1 - r2):
        raise Exception("One circle is within the other")
    if d == 0 and r1 == r2:
        raise Exception("The two circles are coincident")

    # calculate the intersection points
    theta = math.asin(abs(b1 - b2) / d)
    beta = math.acos((r1 ** 2 + d ** 2 - r2 ** 2) / (2 * r1 * d))

    # according center decide the quadrant
    if a1 <= a2:
        if b1 <= b2:
            # Quadrant 1
            x1 = a1 + r1 * math.cos(theta + beta)
            y1 = b1 + r1 * math.sin(theta + beta)

            x2 = a1 + r1 * math.cos(theta - beta)
            y2 = b1 + r1 * math.sin(theta - beta)
        else:
            # Quadrant 4
            x1 = a1 + r1 * math.cos(theta + beta)
            y1 = b1 - r1 * math.sin(theta + beta)

            x2 = a1 + r1 * math.cos(theta - beta)
            y2 = b1 - r1 * math.sin(theta - beta)
    else:
        if b1 <= b2:
            # Quadrant 2
            x1 = a1 - r1 * math.cos(theta + beta)
            y1 = b1 + r1 * math.sin(theta + beta)

            x2 = a1 - r1 * math.cos(theta - beta)
            y2 = b1 + r1 * math.sin(theta - beta)
        else:
            # Quadrant 3
            x1 = a1 - r1 * math.cos(theta + beta)
            y1 = b1 - r1 * math.sin(theta + beta)

            x2 = a1 - r1 * math.cos(theta - beta)
            y2 = b1 - r1 * math.sin(theta - beta)
    #
    #
    # # Quadrant 1
    # x1 = a1 + r1 * math.cos(theta + beta)
    # y1 = b1 + r1 * math.sin(theta + beta)
    #
    # x2 = a1 + r1 * math.cos(theta - beta)
    # y2 = b1 + r1 * math.sin(theta - beta)
    #
    # # Quadrant 2
    # x1 = a1 - r1 * math.cos(theta + beta)
    # y1 = b1 + r1 * math.sin(theta + beta)
    #
    # x2 = a1 - r1 * math.cos(theta - beta)
    # y2 = b1 + r1 * math.sin(theta - beta)
    #
    # # Quadrant 3
    # x1 = a1 - r1 * math.cos(theta + beta)
    # y1 = b1 - r1 * math.sin(theta + beta)
    #
    # x2 = a1 - r1 * math.cos(theta - beta)
    # y2 = b1 - r1 * math.sin(theta - beta)
    #
    # # Quadrant 4
    # x1 = a1 + r1 * math.cos(theta + beta)
    # y1 = b1 - r1 * math.sin(theta + beta)
    #
    # x2 = a1 + r1 * math.cos(theta - beta)
    # y2 = b1 - r1 * math.sin(theta - beta)

    return (x1, y1), (x2, y2)


def cal_intersection_points_cl(x0: float, y0: float, r: float, x1: float, y1: float, x2: float, y2: float) -> tuple[
    tuple[float, float], tuple[float, float]]:
    """
    Calculate the intersection points of a circle and a line

    :param x0: The x-coordinate of the center of the circle
    :param y0: The y-coordinate of the center of the circle
    :param r: The radius of the circle
    :param x1: The x-coordinate of the first point of the line
    :param y1: The y-coordinate of the first point of the line
    :param x2: The x-coordinate of the second point of the line
    :param y2: The y-coordinate of the second point of the line
    :return: A tuple containing two tuples, each representing the coordinates of an intersection point
    """
    if x1 == x2:
        return (x1, y0 + math.sqrt(r ** 2 - (x1 - x0) ** 2)), (x1, y0 - math.sqrt(r ** 2 - (x1 - x0) ** 2))

    # slope of the line
    k = (y2 - y1) / (x2 - x1)
    z = k * x1 - y1 + y0
    a = 1 + k ** 2
    b = -2 * (x0 + k * z)
    c = x0 ** 2 + z ** 2 - r ** 2

    xa = (-b + math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)
    xb = (-b - math.sqrt(b ** 2 - 4 * a * c)) / (2 * a)

    ya = k * xa - k * x1 + y1
    yb = k * xb - k * x1 + y1

    return (xa, ya), (xb, yb)


def cal_centroid(points: list[tuple[float, float]], bias: float = 0.0) -> tuple:
    """
    Calculate the centroid of a polygon.

    :param points: A list of (x, y) tuples representing the points of the polygon.
    :param bias:
    :return: A tuple containing area and the x and y coordinates of the centroid.
    """
    n = len(points)
    area = 0
    cx = 0
    cy = 0
    for i in range(n):
        x1, y1 = points[i]
        x2, y2 = points[(i + 1) % n]
        area += x1 * y2 - x2 * y1
        cx += (x1 + x2) * (x1 * y2 - x2 * y1)
        cy += (y1 + y2) * (x1 * y2 - x2 * y1)

    area /= 2
    cx /= 6 * area
    cy /= 6 * area
    return area, (cx * (1 + bias), cy * (1 + bias))


def cal_radian(x0: float, y0: float, x1: float, y1: float) -> float:
    """
    Calculate the radian between two points
    :param x0: x of the circle center
    :param y0: y of the circle center
    :param x1: x of the second point
    :param y1: y of the second point
    :return: radian
    """
    if x1 == x0:
        if y1 > y0:
            return math.pi / 2
        else:
            return -math.pi / 2
    if y1 == y0:
        if x1 > x0:
            return 0
        else:
            return math.pi
    if x1 > x0 and y1 > y0:
        return math.atan((y1 - y0) / (x1 - x0))
    if x1 < x0 and y1 > y0:
        return math.atan((y1 - y0) / (x1 - x0)) + math.pi
    if x1 < x0 and y1 < y0:
        return math.atan((y1 - y0) / (x1 - x0)) + math.pi
    if x1 > x0 and y1 < y0:
        return math.atan((y1 - y0) / (x1 - x0)) + 2 * math.pi
    return 0


def split_arc(x0: float, y0: float, r: float, start: tuple[float, float], end: tuple[float, float],
              n: int = 100) -> list[tuple[float, float]]:
    """
    Split an arc into n segments.

    :param x0: The x-coordinate of the center of the circle.
    :param y0: The y-coordinate of the center of the circle.
    :param r: The radius of the circle.
    :param start: The starting point of the arc.
    :param end: The ending point of the arc.
    :param n: The number of segments to split the arc into.
    """
    start_radian = cal_radian(x0, y0, start[0], start[1])
    end_radian = cal_radian(x0, y0, end[0], end[1])

    points = []
    for i in range(n + 1):
        if start_radian < end_radian:
            theta = start_radian + (end_radian - start_radian) * i / n
        else:
            theta = start_radian + (2 * math.pi - start_radian + end_radian) * i / n
        x = x0 + r * math.cos(theta)
        y = y0 + r * math.sin(theta)
        points.append((x, y))

    return points


def cal_intersection_ll(x1, y1, x2, y2, x3, y3, x4, y4):
    """
    # 计算两条直线的交点
    :param x1: 第一条直线的第一个点的x坐标
    :param y1: 第一条直线的第一个点的y坐标
    :param x2: 第一条直线的第二个点的x坐标
    :param y2: 第一条直线的第二个点的y坐标
    :param x3: 第二条直线的第一个点的x坐标
    :param y3: 第二条直线的第一个点的y坐标
    :param x4: 第二条直线的第二个点的x坐标
    :param y4: 第二条直线的第二个点的y坐标
    :return: 交点的坐标
    """
    # 计算两条直线的斜率
    if x2 - x1 != 0 and x4 - x3 != 0:
        k1 = (y2 - y1) / (x2 - x1)
        k2 = (y4 - y3) / (x4 - x3)
        # 计算两条直线的截距
        b1 = y1 - k1 * x1
        b2 = y3 - k2 * x3
        # 计算交点的坐标
        x = (b2 - b1) / (k1 - k2)
        y = k1 * x + b1
    else:
        if x2 - x1 == 0:
            k2 = (y4 - y3) / (x4 - x3)
            b2 = y3 - k2 * x3
            x = x1
            y = k2 * x + b2
        else:
            k1 = (y2 - y1) / (x2 - x1)
            b1 = y1 - k1 * x1
            x = x3
            y = k1 * x + b1
    return x, y

# if __name__ == '__main__':
#     print(split_arc(0, 0, 2, (-2 ** 0.5, 2 ** 0.5), (-2 ** 0.5, -2 ** 0.5)))
