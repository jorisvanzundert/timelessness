import glob
import nltk

def texts_in_both_sets( verbose=False ):
    paths_best = glob.glob( "data/Best Selling_Fulltext/*.txt" )
    names_best = [ path.split( '/' )[-1][8:-4] for path in paths_best ]
    set_best = set( names_best )
    if( verbose ):
        print( "Number of all bestsellers - number of unique bestsellers: {}".format( len( paths_best ) - len( set_best ) ) )
        duplicates = set( [ text for text in names_best if names_best.count( text ) > 1 ] )
        if( len( duplicates ) > 0 ):
            print( "Duplicates bestsellers: {}".format( duplicates ) )
    paths_popular = glob.glob( "data/Popular_Fulltext/*.txt" )
    names_popular = [ path.split( '/' )[-1][9:-4] for path in paths_popular ]
    set_popular = set( names_popular )
    if( verbose ):
        print( "Number of all evergreens - number of unique evergreens: {}".format( len( paths_popular ) - len( set_popular ) ) )
        duplicates = set( [ text for text in names_popular if names_popular.count( text ) > 1 ] )
        if( len( duplicates ) > 0 ):
            print( "Duplicate evergreens: {}".format( duplicates ) )
    if( verbose ):
        print( "Overlap: {}".format( set_best & set_popular ) )
    return ( set_best & set_popular )
    # overlapping = []
    # for popular_text in set_popular:
    #     for bestselling_text in set_best:
    #         if nltk.edit_distance( popular_text, bestselling_text ) < 4:
    #             overlapping.append( ( popular_text, bestselling_text) )
    # print( overlapping )

# Main
texts_in_both_sets( True )
