#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
File that sets up the Window containing visualization
"""

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

import geometry

class VisualizationWindow(object):
    def __init__(self):
        self.mw = QtGui.QMainWindow()
        self.mw.resize(800,800)
        self.view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
        self.mw.setCentralWidget(self.view)
        self.mw.show()
        self.mw.setWindowTitle('Visualization')

        self.point_domain_subwindow = self.view.addPlot() # this will be the points subgraph
        self.line_domain_subwindow = self.view.addPlot() # this will be the lines subgraph

    def add_points(self, position_set, color):
        """
        Adds points to the scatter point subgraph
        """

        scatter_plot_item = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(color))
        # First, let's put the points to the scatter display
        spots = [ # this is a list of dictionaries,
        { 'pos' : point, # each dictionary with a key pos with value of the point coordinates,
          'data': 1 # and a single data value
        } for point in position_set] # for every point in the set

        scatter_plot_item.addPoints(spots)
        self.point_domain_subwindow.addItem(scatter_plot_item)

    def add_lines(self, points, line_angles, color):
        """
        Adds lines that are dual to the points specified in position_set to the line subgraph
        """

        support_points =  [ pg.QtCore.QPointF(*point) for point in points ] # list of points where the lines run through

        for index, point in enumerate(support_points):
             line = pg.InfiniteLine(pos = point, 
                                    angle = line_angles[index],
                                    pen = color)
             self.line_domain_subwindow.addItem(line)

    def add_intersections(self, position_set, color):
        """
        Adds points from position_set to the line graph
        """
        scatter_plot_item = pg.ScatterPlotItem(size=4, pen=pg.mkPen(None), brush=pg.mkBrush(color))
        spots = [ # this is a list of dictionaries,
        { 'pos' : point, # each dictionary with a key pos with value of the point coordinates,
          'data': 1 # and a single data value
        } for point in position_set] # for every point in the set
        scatter_plot_item.addPoints(spots)
        self.line_domain_subwindow.addItem(scatter_plot_item)



if __name__ == '__main__':
    import sys
    app = QtGui.QApplication([])
    my_window = VisualizationWindow()
    n_points = (11,11) # red points, blue points

    colors = ( (255,0,0,200), #Color is RGB, opacity in [0,255]
               (0,0,255,200) )
    point_coordinates = [ np.random.normal(size = (n,2)) for n in n_points ]
    #point_coordinates = [ np.array([ [1, 2] , [2, 3] , [5,7] ]),np.array( [ [-1,2], [2, 5], [3, 3] ] )]
    #point_coordinates  = np.array( [ [ (1,1), ], [(2,3),]] )
    for index, coordinates in enumerate(point_coordinates):
        my_window.add_points(coordinates, colors[index])
        # now, let's find the dual lines for each plot
        points , line_angles = geometry.points_to_pos_and_angle(coordinates)
        my_window.add_lines(points, line_angles, colors[index])
        intersections = geometry.dual_intersections(coordinates)
        my_window.add_intersections(intersections, colors[index])
    
    ### Now run the whole thing
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
