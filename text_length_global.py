import utils
import os
import numpy

class Path:
    def __init__( self, screen_name, file_path ):
        self.screen_name = screen_name
        self.path = file_path

path_to_popular = os.path.join( utils.TXTS_AS_DATA, os.path.basename( utils.POPULAR_FULLTEXT ) )
path_to_bestselling = os.path.join( utils.TXTS_AS_DATA, os.path.basename( utils.BEST_SELLING_FULLTEXT ) )
paths = [ Path( "Bestsellers", path_to_bestselling ), Path( "Evergreens", path_to_popular ) ]
means_stdevs = []
for path in paths:
    print( "#", path.screen_name, "\n" )
    file_names = utils.get_file_names_by_extension( path.path, "txt" )
    texts_lengths = []
    for file_name in file_names:
        with open( os.path.join( path.path, file_name ), "r" ) as txt:
            text_lines = []
            line = txt.readline()
            while line:
                if line[0:3] == "[+]":
                    # insert a method to remove [->] marked here
                    text_lines.append( line[3:] )
                line = txt.readline()
        text = ''.join( text_lines )
        texts_lengths.append( len( text ) )
    texts_lengths = numpy.array( texts_lengths )
    means_stdevs.append( ( texts_lengths.mean(), texts_lengths.std() ) )
    print( "Mean text lengths: {:,.2f} (st. dev.: {:,.2f})\n\n".format(  means_stdevs[-1][0], means_stdevs[-1][1] ) )
print( 100 - ( 100 * means_stdevs[1][0]/means_stdevs[0][0] ) ) 
