import pickle
import os
import sys
sys.path.append( os.getcwd() + '/src' )
import utils
import numpy
import matplotlib.pyplot as pyplot
from collections import OrderedDict
import scipy.stats

with open( os.path.join( utils.TXTS_AS_DATA, "texts_lengths.pickle" ), "rb" ) as file:
    texts_sentences_lengths = pickle.load( file )
texts_sentences_lengths = OrderedDict( texts_sentences_lengths )

def is_bestseller( text_name ):
    return text_name.startswith( "BS" )

def is_evergreen( text_name ):
    return text_name.startswith( "POP" )

def get_sentences_lengths( selector ):
    all_sentences_lengths = [ sentences_lengths for ( text_name, sentences_lengths ) in texts_sentences_lengths.items() if selector( text_name ) ]
    # Lose sentences with low word length
    # (Tried > 1, 2, 3 or 4; impact on result is surprisingly marginal.)
    selected_sentences_lengths = [ [ sentence_length_tuple for sentence_length_tuple in sentences_lengths if sentence_length_tuple[1] > 4 ] for sentences_lengths in all_sentences_lengths ]
    # Turn to numpy.array
    sentences_lengths = [ numpy.array( sentences_lengths ) for sentences_lengths in selected_sentences_lengths ]
    return sentences_lengths

bestsellers_sentences_lengths = get_sentences_lengths( selector = is_bestseller )
evergreens_sentences_lengths = get_sentences_lengths( selector = is_evergreen )

print( "number of bestsellers: {}".format( len( bestsellers_sentences_lengths ) ) )
print( "number of evergreens: {}\n\n".format( len( evergreens_sentences_lengths ) ) )

def report( set_label, sentences_lengths ):
    means = numpy.array( [ lengths.mean( axis = 0 ) for lengths in sentences_lengths ] )
    mean = means.mean( axis = 0 )
    std = means.std( axis = 0 )
    print( set_label )
    print( "mean overall token length of sentences: {:.2f} (stdev: {:.2f})".format( mean[1], std[1] ) )
    print( "mean overall char. length of sentences: {:.2f} (stdev: {:.2f})".format( mean[0], std[0] ) )

def confidence_interval( uni_dimensional_np_array, confidence=0.95 ):
    # a = 1.0 * numpy.array( np_array_data[0:,1] )
    a = uni_dimensional_np_array
    n = len( a )
    se = scipy.stats.sem( a )
    confidence = se * scipy.stats.t.ppf( ( 1 + confidence ) / 2., n-1 )
    return confidence

def histo( numpy_array_bestsellers, numpy_array_evergreens, file_name=None ):
    figure = pyplot.figure( dpi=300, figsize=[6.4,4.8] )
    ax_bestsellers_chars = pyplot.subplot( 2, 2, 1 )
    ax_bestsellers_chars.set_title( "Characters" )
    ax_bestsellers_chars.set_ylabel( "Bestsellers", size="large" )
    pyplot.hist( numpy_array_bestsellers[0:,0], 25 )
    ax_bestsellers_tokens = pyplot.subplot( 2, 2, 2 )
    ax_bestsellers_tokens.set_title( "Tokens" )
    pyplot.hist( numpy_array_bestsellers[0:,1], 25 )
    ax_evergreens_chars = pyplot.subplot( 2, 2, 3, sharex=ax_bestsellers_chars, sharey=ax_bestsellers_chars )
    ax_evergreens_chars.set_ylabel( "Evergreens", size="large" )
    pyplot.hist( numpy_array_evergreens[0:,0], 25 )
    pyplot.subplot( 2, 2, 4, sharex=ax_bestsellers_tokens, sharey=ax_bestsellers_tokens )
    pyplot.hist( numpy_array_evergreens[0:,1], 25 )
    if file_name:
        pyplot.savefig( file_name )
    else:
        pyplot.show()

def histo_overlay( numpy_array_bestsellers, numpy_array_evergreens, file_name=None ):
    if file_name:
        figure = pyplot.figure( dpi=300, figsize=[6.4,3.4] )
    else:
        figure = pyplot.figure()
    ax_bestsellers_chars = pyplot.subplot( 1, 2, 1 )
    ax_bestsellers_chars.set_title( "Characters" )
    pyplot.hist( numpy_array_evergreens[0:,0], 25, alpha=0.7, label="evergreens" )
    pyplot.hist( numpy_array_bestsellers[0:,0], 25, alpha=0.8, label="Bestsellers" )
    pyplot.legend()
    ax_bestsellers_tokens = pyplot.subplot( 1, 2, 2, sharey=ax_bestsellers_chars )
    ax_bestsellers_tokens.set_title( "Tokens" )
    pyplot.hist( numpy_array_evergreens[0:,1], 25, alpha=0.7 )
    pyplot.hist( numpy_array_bestsellers[0:,1], 25, alpha=0.8 )
    if file_name:
        pyplot.savefig( file_name )
    else:
        pyplot.show()

def report_std( set_label, sentences_lengths ):
    means = numpy.array( [ lengths.mean( axis = 0 ) for lengths in sentences_lengths ] )
    stds = numpy.array( [ lengths.std( axis = 0 ) for lengths in sentences_lengths ] )
    mean = means.mean( axis = 0 )
    std = means.std( axis = 0 )
    conf_chars = confidence_interval( means[0:,0] )
    conf_tokens = confidence_interval( means[0:,1] )
    mean_stds = stds.mean( axis = 0 )
    std_stds = stds.std( axis = 0 )
    conf_stds_chars = confidence_interval( stds[0:,0] )
    conf_stds_tokens = confidence_interval( stds[0:,1] )
    print( "# {}\n".format( set_label ) )
    print( "overall mean of sentence length\nchars: {:.2f} ±{:.2f}, tokens: {:.2f} ±{:.2f}\n".format( mean[0], conf_chars, mean[1], conf_tokens ) )
    print( "standard deviation of overal mean\nchars: {:.2f}, tokens: {:.2f}\n".format( std[0], std[1] ) )
    print( "mean of standard deviation per text\nchars: {:.2f} ±{:.2f}, tokens: {:.2f} ±{:.2f}\n".format( mean_stds[0], conf_stds_chars, mean_stds[1], conf_stds_tokens ) )
    print( "stdev of standard deviation per text\nchars: {:.2f}, tokens: {:.2f}\n".format( std_stds[0], std_stds[1] ) )
    return means, std_stds[1]

means_best, r1 = report_std( "bestsellers", bestsellers_sentences_lengths )
print( "" )
means_ever, r2 = report_std( "evergreens", evergreens_sentences_lengths )

print( "\nstdev-of-stdev ratio (evergreens/bestsellers): {:.2f}".format( r2/r1 ) )

# histo( means_best, means_ever, "project-reporting/sentence_length_analysis.png" )
histo_overlay( means_best, means_ever, "project-reporting/fig_002_20191004_1503.png" )

# Wat opvalt is dat niet zozeer de gemiddelde zinslengte afwijkt,
# maar vooral de *variantie*. Bij evergreens is de variantie
# (welke low count cut off je ook kiest) altijd ongeveer dubbel zo groot.
#
# Mogelijke andere metingen:
#   * leave out highest and lowest values
