# -*- coding: utf-8 -*-
"""
File that sets up the Window containing visualization
"""

from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import numpy as np

class VisualizationWindow(object):
    def __init__(self):
        self.app = QtGui.QApplication([])
        self.mw = QtGui.QMainWindow()
        self.mw.resize(800,800)
        self.view = pg.GraphicsLayoutWidget()  ## GraphicsView with GraphicsLayout inserted by default
        self.mw.setCentralWidget(self.view)
        self.mw.show()
        self.mw.setWindowTitle('Visualization')

        self.point_domain_subwindow = self.view.addPlot() # this will be the points subgraph
        self.line_domain_subwindow = self.view.addPlot() # this will be the lines subgraph
    def add_points(self, position_set, color):
        scatter_plot_item = pg.ScatterPlotItem(size=10, pen=pg.mkPen(None), brush=pg.mkBrush(color))
        # First, let's put the points to the scatter display
        spots = [ # this is a list of dictionaries,
        { 'pos' : point, # each dictionary with a key pos with value of the point coordinates,
          'data': 1 # and a single data value
        } for point in position_set] # for every point in the set

        scatter_plot_item.addPoints(spots)
        self.point_domain_subwindow.addItem(scatter_plot_item)

        # now, let's find the dual lines for each plot
        support_points =  [ pg.QtCore.QPointF(0.0, point[1]) for point in position_set ] # list of points where the lines run through
        line_angles = np.arctan(position_set[:, 1]/position_set[:, 0] * 180.0 / np.pi) # WHYEVER pyqtgraph expects angles in DEGREE
        for index, point in enumerate(support_points):
             line = pg.InfiniteLine(pos = point, 
                                    angle = line_angles[index],
                                    pen = color)
             self.line_domain_subwindow.addItem(line)

if __name__ == '__main__':
    import sys
    my_window = VisualizationWindow()
    n_points = (30,30) # red points, blue points

    colors = ( (255,0,0,200), #Color is RGB, opacity in [0,255]
               (0,0,255,200) )
    point_coordinates = [ np.random.normal(size = (n,2)) for n in n_points ]
    for index, coordinates in enumerate(point_coordinates):
        my_window.add_points(coordinates, colors[index])
    
    ### Now run the whole thing
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
