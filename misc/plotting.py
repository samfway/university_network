#!/usr/bin/env python

__author__ = "Sam Way"
__copyright__ = "Copyright 2014, The Clauset Lab"
__license__ = "BSD"
__maintainer__ = "Sam Way"
__email__ = "samfway@gmail.com"
__status__ = "Development"

""" Functions to plot a confusion matrix (heat map) 
"""

from numpy import arange
import matplotlib.pyplot as plt

def plot_confusion_matrix(M, labels, ax, cmap=plt.cm.Blues, rng=None):
    """ Plot a confusion matrix on supplied axes. 
    
        Inputs:
        M - (KxK) array-like confusion/mixing matrix
        labels - K-dim vector of string labels
        ax - matplotlib axes object to be drawn upon
        cmap - (optional) mpl-compatible colormap 

        Returns:
        matplotlib pcolor results

        Notes:
        Add colorbar with...
    
        >>> # M, labels both previous defined... 
        >>> fig, ax = plt.subplots()
        >>> cm = plot_confusion_matrix(M, labels, ax)
        >>> fig.colorbar(cm)
    """ 
    if rng is None:
        min_value = M.min()
        max_value = M.max()
    else:
        min_value, max_value = rng

    #if max_value < 1.0:
    #    max_value = 1.0 # matrix is normalized 

    heatmap = ax.pcolor(M, cmap=cmap)
    ax.set_xticks(arange(M.shape[0])+0.5, minor=False)
    ax.set_yticks(arange(M.shape[1])+0.5, minor=False)
    ax.invert_yaxis()
    ax.xaxis.tick_top()
    ax.set_xticklabels(labels, minor=False) # add rotation=int to rotate labels
    ax.set_yticklabels(labels, minor=False)
    ax.set_aspect('equal', adjustable='box')  
    ax.xaxis.set_label_position('top')
    heatmap.set_clim(vmin=min_value,vmax=max_value)
    print min_value, max_value

    return heatmap
    
