#!/usr/bin/python
# -*- coding: utf-8 -*-

import numpy as np

def dual_intersections(points):
    totalpoints = len(points)
    for index, point in enumerate(points):
        a1, b1 = point
        for second_point in points[index+1:]: #from index + 1 to the end of the list
            a2, b2 = second_point
            x = (b2-b1)/(a1-a2)
            y = a1*x + b1
            yield (x, y)

def points_to_pos_and_angle(points):
    support_points =  [ (0.0, point[1]) for point in points] # list of points where the lines run through
    line_angles = np.arctan(points[:, 0]) * 180.0 / np.pi # WHYEVER pyqtgraph expects angles in DEGREE
    for idx, p in enumerate(support_points):
        angle = line_angles[idx]
    return support_points, line_angles

def median_line(points):
    """
    for a given set of points, find the line segments of the median line
    """
    ## first step: left limes median line (left of first intersection)
    # We observe that for x << (leftest intersection), the slope of the line defines its order.
    # so we take the lazy route and sort our lines by slope, which is the x_1 coordinate of each point
    lefthand_lines_sorted = sorted(points)
    median = len(points) / 2 # is floor(#points/2), so alright for odd numbers
    ##
