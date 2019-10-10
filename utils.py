import os
import glob

CWD = os.getcwd()
DATA = os.path.join( CWD, "data" )
POPULAR_FULLTEXT = os.path.join( DATA, "Popular_Fulltext" )
BEST_SELLING_FULLTEXT = os.path.join( DATA, "Best Selling_Fulltext" )
TXTS_AS_DATA = os.path.join( DATA, "Texts-as-Data" )
POS_PATH = os.path.join( TXTS_AS_DATA, "POS" )
TFIDF_PATH = os.path.join( TXTS_AS_DATA, "TfIdf" )

DROP_EXTENSION = True

def get_file_names_by_extension( path, extension, drop_extension=False ):
    file_names = glob.glob( "{}/*.{}".format( path, extension ) )
    file_names = [ os.path.basename( file_name ) for file_name in file_names ]
    if drop_extension == True:
        file_names = [ os.path.splitext( pdf_file_name )[0] for pdf_file_name in file_names ]
    file_names.sort()
    return file_names

def cp1252_to_utf8( path, file_name ):
    in_file = open( os.path.join( path, file_name ), encoding="cp1252" )
    text = in_file.read()
    in_file.close()
    out_file = open( os.path.join( path, file_name ), "w" )
    out_file.write( text )
    out_file.close()

def correct_wrong_encodings( path ):
    txts = get_file_names_by_extension( path, "txt" )
    txt_starts = {}
    for txt in txts:
        with open( os.path.join( path, txt ), "r" ) as txt_file:
            try:
                text = txt_file.read()
            except UnicodeDecodeError:
                print( txt )
                # txt_file.close()
                # cp1252_to_utf8( path, txt )
