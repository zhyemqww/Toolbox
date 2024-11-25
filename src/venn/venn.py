#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : zhyemqww
# @Time     : 2024/4/25 16:53
# @File     : venn
# @Project  : MALDI_Decipher
# @Desc     :
from matplotlib import pyplot as plt
from matplotlib.patches import Circle

from src.venn.decode_venn_data import decode_venn_data
from src.venn.venn_utils import cal_intersection_ll, cal_distance, cal_intersection_points_cc, split_arc, cal_centroid


class Venn:
    def __init__(self):
        pass

    def plot(self, *args, **kwargs):
        area = kwargs.get("area", False)
        if not area:
            self.draw(*args, **kwargs)
        else:
            self.draw_area(*args, **kwargs)

    @staticmethod
    def draw(data: dict, alpha: float = 0.5, annotation_color: str = "black", area=False, distance: float = 1.25,
             edgecolor: str = "black", face_colors: list = None, font: str = "Arial", fontsize_annotation: int = 10,
             fontsize_label: int = 12, label_color: str = "black", linewidth: float = 1.0, max_iteration: int = 10000,
             radius: float = 1.0, tol: float = 1e-6, up: bool = True):
        """
        Draw the venn area
        :return:
        """
        length = len(data)
        labels = list(data.keys())

        if length != 2 and length != 3:
            raise Exception("The length of the data must be 2 or 3")

        data = decode_venn_data(data)

        fig, ax = plt.subplots()
        ax.axis('off')
        ax.set_aspect('equal')

        if length == 2:
            if face_colors is None or len(face_colors) != 2:
                face_colors_1 = "#2B9DE3"
                face_colors_2 = "#D3096A"
            else:
                face_colors_1 = face_colors[0]
                face_colors_2 = face_colors[1]

            S1 = len(data[(labels[0],)])
            S2 = len(data[(labels[1],)])
            A12 = len(data[(labels[0], labels[1])])

            # Calculate the distance between two circles
            r1, r2, = radius, radius
            """
            Draw the two circles
            Circle((x, y), radius, color)
            first circle center is (0, 0)
            """

            ax.add_patch(
                Circle((0, 0), r1, facecolor=face_colors_1, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))
            ax.add_patch(
                Circle((distance, 0), r2, facecolor=face_colors_2, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))

            # annotation
            # set the labels
            y = max(r1, r2) * 1.1
            ax.annotate(labels[0], xy=(0, 0), xytext=(-r1, -y), va='center', ha='center', fontsize=fontsize_label,
                        color=label_color)
            ax.annotate(labels[1], xy=(0, 0), xytext=(r2 + distance, -y), va='center', ha='center', fontsize=fontsize_label,
                        color=label_color)

            # set the text
            ax.annotate(f"{S1}", xy=(0, 0), xytext=((-r1 - r2 + distance) / 2, 0), va='center', ha='center',
                        fontsize=fontsize_annotation, color=annotation_color)
            ax.annotate(f"{S2}", xy=(0, 0), xytext=((r1 + r2 + distance) / 2, 0), va='center', ha='center',
                        fontsize=fontsize_annotation, color=annotation_color)
            ax.annotate(f"{A12}", xy=(0, 0), xytext=((r1 - r2 + distance) / 2, 0), va='center', ha='center',
                        fontsize=fontsize_annotation, color=annotation_color)

            for text in ax.texts:
                text.set_fontname(font)

            ax.set_xlim(-1.1 * radius, (distance + r2) * 1.1)
            ax.set_ylim(-1.1 * radius, 1.1 * radius)
            plt.show()

        elif length == 3:
            if face_colors is None or len(face_colors) != 3:
                face_colors_1 = "#2B9DE3"
                face_colors_2 = "#D3096A"
                face_colors_3 = "#FFD700"
            else:
                face_colors_1 = face_colors[0]
                face_colors_2 = face_colors[1]
                face_colors_3 = face_colors[2]

            S1 = len(data[(labels[0],)])
            S2 = len(data[(labels[1],)])
            S3 = len(data[(labels[2],)])
            A12 = len(data[(labels[0], labels[1])])
            A13 = len(data[(labels[0], labels[2])])
            A23 = len(data[(labels[1], labels[2])])
            A123 = len(data[(labels[0], labels[1], labels[2])])

            r1 = radius
            r2 = radius
            r3 = radius

            # calculate the center of the third circle
            x = distance / 2

            if up:
                y = 3 ** 0.5 / 2 * distance
                ax.add_patch(
                    Circle((0, 0), r1, facecolor=face_colors_1, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))
                ax.add_patch(
                    Circle((distance, 0), r2, facecolor=face_colors_2, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))
                ax.add_patch(
                    Circle((x, y), r3, facecolor=face_colors_3, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))

                # set the labels
                bias = r1 * 1.15
                ax.annotate(labels[0], xy=(0, 0), xytext=(-r1, -bias), va='center', ha='center', fontsize=fontsize_label,
                            color=label_color)
                ax.annotate(labels[1], xy=(0, 0), xytext=(r2 + distance, -bias), va='center', ha='center', fontsize=fontsize_label,
                            color=label_color)
                ax.annotate(labels[2], xy=(0, 0), xytext=(x, (y + r3) * 1.15), va='center', ha='center', fontsize=fontsize_label,
                            color=label_color)

                p12 = cal_intersection_ll(-r1 / 2, -0.5 * r1 / 3 ** 0.5, distance + r2 / 2, -0.5 * r1 / 3 ** 0.5, x, y + r3 / 3 ** 0.5, x, y / 3)
                p13 = cal_intersection_ll(-r1 / 2, -0.5 * r1 / 3 ** 0.5, x, y + r3 / 3 ** 0.5, distance + r2 / 2, -0.5 * r1 / 3 ** 0.5, x, y / 3)
                p23 = cal_intersection_ll(x, y + r3 / 3 ** 0.5, distance + r2 / 2, -0.5 * r1 / 3 ** 0.5, -r1 / 2, -0.5 * r1 / 3 ** 0.5, x, y / 3)

                # calculate the text position
                ax.annotate(f"{S1}", xy=(0, 0), xytext=(-r1 / 2, -0.5 * r1 / 3 ** 0.5), va='center', ha='center',
                            fontsize=fontsize_annotation, color=annotation_color)
                ax.annotate(f"{S2}", xy=(0, 0), xytext=(distance + r2 / 2, -0.5 * r1 / 3 ** 0.5), va='center', ha='center',
                            fontsize=fontsize_annotation, color=annotation_color)
                ax.annotate(f"{S3}", xy=(0, 0), xytext=(x, y + r3 / 3 ** 0.5), va='center', ha='center',
                            fontsize=fontsize_annotation, color=annotation_color)
                ax.annotate(f"{A12}", xy=(0, 0), xytext=p12, va='center', ha='center',
                            fontsize=fontsize_annotation, color=annotation_color)
                ax.annotate(f"{A13}", xy=(0, 0), xytext=p13, va='center', ha='center',
                            fontsize=fontsize_annotation, color=annotation_color)
                ax.annotate(f"{A23}", xy=(0, 0), xytext=p23, va='center', ha='center',
                            fontsize=fontsize_annotation, color=annotation_color)
                ax.annotate(f"{A123}", xy=(0, 0), xytext=(x, y / 3), va='center', ha='center',
                            fontsize=fontsize_annotation, color=annotation_color)

                ax.set_xlim(-1.1 * r1, (distance + r2) * 1.1)
                ax.set_ylim(-bias, (y + r3) * 1.2)

            else:
                y = - 3 ** 0.5 / 2 * distance
                ax.add_patch(
                    Circle((0, 0), r1, facecolor=face_colors_1, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))
                ax.add_patch(
                    Circle((distance, 0), r2, facecolor=face_colors_2, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))
                ax.add_patch(
                    Circle((x, y), r3, facecolor=face_colors_3, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))

                # set the labels
                bias = r1 * 1.15
                ax.annotate(labels[0], xy=(0, 0), xytext=(-r1, bias), va='center', ha='center', fontsize=fontsize_label,
                            color=label_color)
                ax.annotate(labels[1], xy=(0, 0), xytext=(r2 + distance, bias), va='center', ha='center', fontsize=fontsize_label,
                            color=label_color)
                ax.annotate(labels[2], xy=(0, 0), xytext=(x, (y - r3) * 1.15), va='center', ha='center', fontsize=fontsize_label,
                            color=label_color)

                p12 = cal_intersection_ll(-r1 / 2, 0.5 * r1 / 3 ** 0.5, distance + r2 / 2, 0.5 * r1 / 3 ** 0.5, x, y - r3 / 3 ** 0.5, x, y / 3)
                p13 = cal_intersection_ll(-r1 / 2, 0.5 * r1 / 3 ** 0.5, x, y - r3 / 3 ** 0.5, distance + r2 / 2, 0.5 * r1 / 3 ** 0.5, x, y / 3)
                p23 = cal_intersection_ll(x, y - r3 / 3 ** 0.5, distance + r2 / 2, 0.5 * r1 / 3 ** 0.5, -r1 / 2, 0.5 * r1 / 3 ** 0.5, x, y / 3)

                # calculate the text position
                ax.annotate(f"{S1}", xy=(0, 0), xytext=(-r1 / 2, 0.5 * r1 / 3 ** 0.5), va='center', ha='center',
                            fontsize=fontsize_annotation, color=annotation_color)
                ax.annotate(f"{S2}", xy=(0, 0), xytext=(distance + r2 / 2, 0.5 * r1 / 3 ** 0.5), va='center', ha='center',
                            fontsize=fontsize_annotation, color=annotation_color)
                ax.annotate(f"{S3}", xy=(0, 0), xytext=(x, y - r3 / 3 ** 0.5), va='center', ha='center',
                            fontsize=fontsize_annotation, color=annotation_color)
                ax.annotate(f"{A12}", xy=(0, 0), xytext=p12, va='center', ha='center',
                            fontsize=fontsize_annotation, color=annotation_color)
                ax.annotate(f"{A13}", xy=(0, 0), xytext=p13, va='center', ha='center',
                            fontsize=fontsize_annotation, color=annotation_color)
                ax.annotate(f"{A23}", xy=(0, 0), xytext=p23, va='center', ha='center',
                            fontsize=fontsize_annotation, color=annotation_color)
                ax.annotate(f"{A123}", xy=(0, 0), xytext=(x, y / 3), va='center', ha='center',
                            fontsize=fontsize_annotation, color=annotation_color)

                ax.set_xlim(-1.1 * r1, (distance + r2) * 1.1)
                ax.set_ylim((y - r3) * 1.2, bias)


            plt.tight_layout()
            plt.show()

    @staticmethod
    def draw_area(data, alpha: float = 0.5, annotation_color: str = "black", area= True, edgecolor: str = "black", face_colors: list = None,
             font: str = "Arial", fontsize_annotation: int = 10, fontsize_label: int = 12, label_color: str = "black",
             linewidth: float = 1.0, max_iteration: int = 10000, radius: float = 1.0, tol: float = 1e-6, up: bool = True):
        """
        Draw the venn area
        :return:
        """
        length = len(data)
        labels = list(data.keys())

        if length != 2 and length != 3:
            raise Exception("The length of the data must be 2 or 3")

        data = decode_venn_data(data)

        fig, ax = plt.subplots()
        ax.axis('off')
        ax.set_aspect('equal')

        if length == 2:
            if face_colors is None or len(face_colors) != 2:
                face_colors_1 = "#2B9DE3"
                face_colors_2 = "#D3096A"
            else:
                face_colors_1 = face_colors[0]
                face_colors_2 = face_colors[1]

            S1 = len(data[(labels[0],)])
            S2 = len(data[(labels[1],)])
            A12 = len(data[(labels[0], labels[1])])

            # Calculate the distance between two circles
            r1, r2, distance = cal_distance(S1, S2, A12, tol=tol, max_iteration=max_iteration, normalization=True)

            """
            Draw the two circles
            Circle((x, y), radius, color)
            first circle center is (0, 0)
            """
            rr1 = r1 * radius
            rr2 = r2 * radius
            dr = distance * radius

            ax.add_patch(
                Circle((0, 0), rr1, facecolor=face_colors_1, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))
            ax.add_patch(
                Circle((dr, 0), rr2, facecolor=face_colors_2, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))

            # annotation
            # set the labels
            y = max(rr1, rr2) * 1.1
            ax.annotate(labels[0], xy=(0, 0), xytext=(-rr1, -y), va='center', ha='center', fontsize=fontsize_label,
                        color=label_color)
            ax.annotate(labels[1], xy=(0, 0), xytext=(rr2 + dr, -y), va='center', ha='center', fontsize=fontsize_label,
                        color=label_color)

            # set the text
            ax.annotate(f"{S1}", xy=(0, 0), xytext=((-rr1 - rr2 + dr) / 2, 0), va='center', ha='center',
                        fontsize=fontsize_annotation, color=annotation_color)
            ax.annotate(f"{S2}", xy=(0, 0), xytext=((rr1 + rr2 + dr) / 2, 0), va='center', ha='center',
                        fontsize=fontsize_annotation, color=annotation_color)
            ax.annotate(f"{A12}", xy=(0, 0), xytext=((rr1 - rr2 + dr) / 2, 0), va='center', ha='center',
                        fontsize=fontsize_annotation, color=annotation_color)

            for text in ax.texts:
                text.set_fontname(font)

            ax.set_xlim(-1.1 * radius, (dr + rr2) * 1.1)
            ax.set_ylim(-1.1 * radius, 1.1 * radius)
            plt.show()

        elif length == 3:
            if face_colors is None or len(face_colors) != 3:
                face_colors_1 = "#2B9DE3"
                face_colors_2 = "#D3096A"
                face_colors_3 = "#FFD700"
            else:
                face_colors_1 = face_colors[0]
                face_colors_2 = face_colors[1]
                face_colors_3 = face_colors[2]

            S1 = len(data[(labels[0],)])
            S2 = len(data[(labels[1],)])
            S3 = len(data[(labels[2],)])
            A12 = len(data[(labels[0], labels[1])])
            A13 = len(data[(labels[0], labels[2])])
            A23 = len(data[(labels[1], labels[2])])
            A123 = len(data[(labels[0], labels[1], labels[2])])

            # Calculate the distance between two circles
            # C1 - C2
            R11, R21, distance1_2 = cal_distance(S1 + A13, S2 + A23, A12 + A123, tol=tol, max_iteration=max_iteration,
                                                 normalization=False)
            # C1 - C3
            R12, R32, distance1_3 = cal_distance(S1 + A12, S3 + A23, A13 + A123, tol=tol, max_iteration=max_iteration,
                                                 normalization=False)
            # C2 - C3
            R23, R33, distance2_3 = cal_distance(S2 + A12, S3 + A13, A23 + A123, tol=tol, max_iteration=max_iteration,
                                                 normalization=False)

            if R11 == R12 and R21 == R23 and R32 == R33:
                R1 = R11
                R2 = R21
                R3 = R32
            else:
                raise Exception("The circles are not intersected")

            # normalize the radius
            st = max(R1, R2, R3)
            rr1 = radius * R1 / st
            rr2 = radius * R2 / st
            rr3 = radius * R3 / st
            dr1_2 = radius * distance1_2 / st
            dr1_3 = radius * distance1_3 / st
            dr2_3 = radius * distance2_3 / st

            # calculate the center of the third circle
            x = (dr1_3 ** 2 - dr2_3 ** 2 + dr1_2 ** 2) / (2 * dr1_2)

            if up:
                y = (dr1_3 ** 2 - x ** 2) ** 0.5
                ax.add_patch(
                    Circle((0, 0), rr1, facecolor=face_colors_1, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))
                ax.add_patch(
                    Circle((dr1_2, 0), rr2, facecolor=face_colors_2, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))
                ax.add_patch(
                    Circle((x, y), rr3, facecolor=face_colors_3, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))

                # set the labels
                bias = max(rr1, rr2) * 1.15
                ax.annotate(labels[0], xy=(0, 0), xytext=(-rr1, -bias), va='center', ha='center', fontsize=fontsize_label,
                            color=label_color)
                ax.annotate(labels[1], xy=(0, 0), xytext=(rr2 + dr1_2, -bias), va='center', ha='center', fontsize=fontsize_label,
                            color=label_color)
                ax.annotate(labels[2], xy=(0, 0), xytext=(x, (y + rr3) * 1.15), va='center', ha='center', fontsize=fontsize_label,
                            color=label_color)

                # calculate the text position
                pE, pC = cal_intersection_points_cc(0, 0, rr1, dr1_2, 0, rr2)
                pB, pD = cal_intersection_points_cc(dr1_2, 0, rr2, x, y, rr3)
                pA, pF = cal_intersection_points_cc(0, 0, rr1, x, y, rr3)

                c1 = split_arc(0, 0, rr1, pA, pC) + split_arc(dr1_2, 0, rr2, pD, pC) + split_arc(x, y, rr3, pA, pD)
                c2 = split_arc(x, y, rr3, pF, pB) + split_arc(0, 0, rr1, pC, pF) + split_arc(dr1_2, 0, rr2, pC, pB)
                c3 = split_arc(0, 0, rr1, pE, pA) + split_arc(dr1_2, 0, rr2, pB, pE) + split_arc(x, y, rr3, pB, pA)

                c12 = split_arc(0, 0, rr1, pC, pF) + split_arc(x, y, rr3, pD, pF) + split_arc(dr1_2, 0, rr2, pD, pC)
                c13 = split_arc(0, 0, rr1, pE, pA) + split_arc(x, y, rr3, pA, pD) + split_arc(dr1_2, 0, rr2, pE, pD)
                c23 = split_arc(0, 0, rr1, pF, pE) + split_arc(x, y, rr3, pF, pB) + split_arc(dr1_2, 0, rr2, pB, pE)

                c123 = split_arc(0, 0, rr1, pF, pE) + split_arc(dr1_2, 0, rr2, pE, pD) + split_arc(x, y, rr3, pD, pF)

                ax.set_xlim(-1.1 * rr1, (dr1_2 + rr2) * 1.1)
                ax.set_ylim(-bias, (y + rr3) * 1.2)

            else:
                y = - (dr1_3 ** 2 - x ** 2) ** 0.5
                ax.add_patch(
                    Circle((0, 0), rr1, facecolor=face_colors_1, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))
                ax.add_patch(
                    Circle((dr1_2, 0), rr2, facecolor=face_colors_2, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))
                ax.add_patch(
                    Circle((x, y), rr3, facecolor=face_colors_3, alpha=alpha, edgecolor=edgecolor, linewidth=linewidth))

                # set the labels
                bias = max(rr1, rr2) * 1.15
                ax.annotate(labels[0], xy=(0, 0), xytext=(-rr1, bias), va='center', ha='center', fontsize=fontsize_label,
                            color=label_color)
                ax.annotate(labels[1], xy=(0, 0), xytext=(rr2 + dr1_2, bias), va='center', ha='center',
                            fontsize=fontsize_label,
                            color=label_color)
                ax.annotate(labels[2], xy=(0, 0), xytext=(x, (y - rr3) * 1.15), va='center', ha='center', fontsize=fontsize_label,
                            color=label_color)

                # calculate the text position
                pA, pF = cal_intersection_points_cc(0, 0, rr1, dr1_2, 0, rr2)
                pB, pD = cal_intersection_points_cc(dr1_2, 0, rr2, x, y, rr3)
                pC, pE = cal_intersection_points_cc(0, 0, rr1, x, y, rr3)

                c1 = split_arc(0, 0, rr1, pA, pC) + split_arc(dr1_2, 0, rr2, pA, pD) + split_arc(x, y, rr3, pD, pC)
                c2 = split_arc(x, y, rr3, pB, pE) + split_arc(0, 0, rr1, pE, pA) + split_arc(dr1_2, 0, rr2, pB, pA)
                c3 = split_arc(0, 0, rr1, pC, pF) + split_arc(dr1_2, 0, rr2, pF, pB) + split_arc(x, y, rr3, pC, pB)

                c12 = split_arc(0, 0, rr1, pE, pA) + split_arc(x, y, rr3, pE, pD) + split_arc(dr1_2, 0, rr2, pA, pD)
                c13 = split_arc(0, 0, rr1, pC, pF) + split_arc(x, y, rr3, pD, pC) + split_arc(dr1_2, 0, rr2, pD, pF)
                c23 = split_arc(0, 0, rr1, pF, pE) + split_arc(x, y, rr3, pB, pE) + split_arc(dr1_2, 0, rr2, pF, pB)

                c123 = split_arc(0, 0, rr1, pF, pE) + split_arc(dr1_2, 0, rr2, pD, pF) + split_arc(x, y, rr3, pE, pD)

                ax.set_xlim(-1.1 * rr1, (dr1_2 + rr2) * 1.1)
                ax.set_ylim((y - rr3) * 1.2, bias)

            ax.annotate(f"{S1}", xy=(0, 0), xytext=(cal_centroid(c1)[1]), va='center', ha='center',
                        fontsize=fontsize_annotation, color=annotation_color)
            ax.annotate(f"{S2}", xy=(0, 0), xytext=(cal_centroid(c2)[1]), va='center', ha='center',
                        fontsize=fontsize_annotation, color=annotation_color)
            ax.annotate(f"{S3}", xy=(0, 0), xytext=(cal_centroid(c3)[1]), va='center', ha='center',
                        fontsize=fontsize_annotation, color=annotation_color)
            ax.annotate(f"{A12}", xy=(0, 0), xytext=(cal_centroid(c12)[1]), va='center', ha='center',
                        fontsize=fontsize_annotation, color=annotation_color)
            ax.annotate(f"{A13}", xy=(0, 0), xytext=(cal_centroid(c13)[1]), va='center', ha='center',
                        fontsize=fontsize_annotation, color=annotation_color)
            ax.annotate(f"{A23}", xy=(0, 0), xytext=(cal_centroid(c23)[1]), va='center', ha='center',
                        fontsize=fontsize_annotation, color=annotation_color)
            ax.annotate(f"{A123}", xy=(0, 0), xytext=(cal_centroid(c123)[1]), va='center', ha='center',
                        fontsize=fontsize_annotation, color=annotation_color)

            plt.tight_layout()
            plt.show()



if __name__ == '__main__':
    d = {
        "ASFSetgrrrrrrrrrrrrrrrre": {1, 2, 45, 67, 3, 4, 5, 6, 7},
        "Bsgfrrrrrrrrrrrrrrsgse": {6, 7, 8, 9, 10},
        "Csgfrrrrrrrrrrrrrrsgse": {6, 7, 10, 11, 12}
        }

    da = {

        "a": {3, 10, 11, 24, 25, 31, 43, 45, 54, 56, 60, 63, 74, 75, 77, 82, 85, 93, 98, 104, 105, 107, 116, 118, 120,
              126,
              135, 153, 162, 163, 169, 178, 183, 185, 200, 206, 221, 230, 232, 233, 234, 236, 240, 251, 253, 254, 262,
              266,
              497, 499},
        "b": {4, 5, 21, 22, 23, 28, 31, 37, 39, 47, 61, 79, 85, 87, 90, 100, 107, 110, 118, 120, 124, 127, 131, 133,
              162, 181,
              185, 204, 205, 209, 212, 218, 220, 229, 232, 237, 247, 248, 257, 262, 263, 267, 268, 270, 280, 281, 289,
              290, 292,
              434, 438, 443, 447, 448, 451, 452, 459, 461, 466, 468, 481, 488, 489, 491, 500},
        "c": {2, 9, 18, 22, 35, 53, 57, 61, 64, 74, 76, 78, 99, 110, 111, 113, 114, 124, 128, 137, 140, 141, 143, 146,
              150, 152,
              161, 163, 167, 169, 182, 183, 187, 195, 197, 198, 202, 207, 210, 216, 217, 218, 221, 228, 231, 232, 239,
              240, 241,
              365, 372, 379, 383, 397, 404, 407, 415, 416, 424, 429, 430, 432, 433, 436, 438, 441, 445, 457, 467, 468,
              471, 488,
              497, 499},

    }

    venn = Venn()
    venn.plot(da, linewidth=0, annotation_color="black", up=True, radius=3, area=True)
