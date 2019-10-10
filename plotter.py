import utils
import os
import pickle
import matplotlib.pyplot as plt
from matplotlib import patches
import numpy
import umap
import overlap_popularbestselling
import gradient_grid
import math

def gradient_patch( plt, mean, stdev, color, steps ):
    steps_x = steps
    steps_y = math.ceil( ( stdev[1] / stdev[0] ) * steps_x )
    patch_x = numpy.linspace( mean[0] - 0.5 * stdev[0], mean[0] + 0.5 * stdev[0], steps_x )
    patch_y = numpy.linspace( mean[1] - 0.5 * stdev[1], mean[1] + 0.5 * stdev[1], steps_y )
    xv, yv = numpy.meshgrid( patch_x, patch_y )
    colors = gradient_grid.alpha_gradient_grid( steps_x, steps_y, color=color )
    plt.scatter( xv, yv, c=colors, marker="." )

def plot_chart( file_name=None ):
    if file_name:
        figure = plt.figure( dpi=300, figsize=[6.4,4.8] )
    else:
        figure = plt.figure()

    subplot_axes = figure.add_subplot( 1, 1, 1 )
    # subplot_axes.add_patch( patches.Ellipse( bestsellers_mean, bestsellers_stddev[0], bestsellers_stddev[1], facecolor='moccasin', edgecolor='orange', linewidth=1, alpha=0.5 ) )
    # subplot_axes.add_patch( patches.Ellipse( evergreens_mean, evergreens_stddev[0], evergreens_stddev[1], facecolor='lightgreen', edgecolor='green', linewidth=1, alpha=0.3 ) )
    plt.scatter( bestsellers[:,0], bestsellers[:,1], c='orange', label="bestselling", alpha=0.5 )
    plt.scatter( evergreens[:,0], evergreens[:,1], c='green', label='evergreens', alpha=0.5 )
    plt.scatter( both[:,0], both[:,1], c='purple', label="both", alpha=1 )
    plt.axvline( x=bestsellers_mean[0], c='orange', linewidth=1, dashes=[2,2] )
    plt.axhline( y=bestsellers_mean[1], c='orange', linewidth=1, dashes=[2,2] )
    plt.axvline( x=evergreens_mean[0], c='green', linewidth=1, dashes=[2,2] )
    plt.axhline( y=evergreens_mean[1], c='green', linewidth=1, dashes=[2,2] )
    plt.legend()

    steps = 100
    gradient_patch( plt, bestsellers_mean, bestsellers_stdev, "#fff278", steps )
    gradient_patch( plt, evergreens_mean, evergreens_stdev, "#7fff78", steps )

    if file_name:
        plt.savefig( file_name )
    else:
        plt.show()

# MAIN
overlap = overlap_popularbestselling.texts_in_both_sets()
file_names = utils.get_file_names_by_extension( utils.POS_PATH, "pickle" )
def in_both( file_name ):
    for overlapping in overlap:
        if overlapping in file_name:
            return True
    return False
intersected = numpy.array( list( map( in_both, file_names ) ) )

with open( os.path.join( utils.TFIDF_PATH, "20190919_2357/umap_20191001_1903.pickle" ), "rb" ) as file:
    umap_data = pickle.load( file )
both = umap_data[intersected]
bestsellers = umap_data[0:133,:]
evergreens = umap_data[133:,:]

bestsellers_mean = numpy.mean( bestsellers, axis=0 )
evergreens_mean = numpy.mean( evergreens, axis=0 )
bestsellers_stdev = numpy.std( bestsellers, axis=0 )
evergreens_stdev = numpy.std( evergreens, axis=0 )

print( bestsellers_mean )
print( bestsellers_stdev )
print( evergreens_mean )
print( evergreens_stdev )

# plot_chart( "project-reporting/fig_umap_20191001_1905.png" )
plot_chart()
