import pickle
import spacy
import os
import utils
from tqdm import tqdm

nlp = spacy.load("en_core_web_md")
nlp.max_length = 2000000
path_to_popular = os.path.join( utils.TXTS_AS_DATA, os.path.basename( utils.POPULAR_FULLTEXT ) )
path_to_bestselling = os.path.join( utils.TXTS_AS_DATA, os.path.basename( utils.BEST_SELLING_FULLTEXT ) )
paths = [ path_to_bestselling, path_to_popular ]
for path in paths:
    file_names = utils.get_file_names_by_extension( path, "txt" )
    for file_name in tqdm( file_names ):
        with open( os.path.join( path, file_name ), "r" ) as txt:
            text_lines = []
            line = txt.readline()
            while line:
                if line[0:3] == "[+]":
                    # insert a method to remove [->] marked here
                    text_lines.append( line[3:] )
                line = txt.readline()
        text = ''.join( text_lines )
        doc = nlp( text )
        file_name = os.path.splitext( file_name )[0]
        with open( os.path.join( utils.POS_PATH, file_name + ".pickle" ), "wb" ) as file:
            pickle.dump( doc, file )
