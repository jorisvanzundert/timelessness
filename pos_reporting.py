import pickle
import utils
import os
# import spikes.temp

def howards_end_as_pos_text():
    with open( os.path.join( utils.POS_PATH, "POP_1910_Howards End.pickle" ), "rb" ) as file:
        pos_text = ""
        doc = pickle.load( file )
        n = 0
        for token in doc:
            if not token.is_space:
                if ( len( token.lemma_ ) > 1 ) or ( token.lemma_.isalnum() ):
                    pos_text += "{} ({} {}) ".format( token.text, token.lemma_, token.tag_ )
                    n += 1
                    if n == 10:
                        pos_text += '\n'
                        n = 0

    with open( os.path.join( utils.CWD, "project-documentation/POP_1910_Howards End_POStext.txt" ), "w" ) as pos_report_file:
        pos_report_file.write( pos_text )

def create_texts_without_nnps():
    file_names = utils.get_file_names_by_extension( utils.POS_PATH, "pickle" )
    # file_names = spikes.temp.get_remaining()
    for file_name in file_names:
        with open( os.path.join( utils.POS_PATH, file_name ), "rb" ) as file:
            nnpless_text = ""
            doc = pickle.load( file )
            n = 0
            for token in doc:
                if ( not token.is_space ) and ( not token.tag_ == "NNP" ):
                    if ( len( token.lemma_ ) > 1 ) or ( token.lemma_.isalnum() ):
                        nnpless_text += "{} ".format( token.text )
                        n += 1
                        if n == 10:
                            nnpless_text += '\n'
                            n = 0
        txt_file_name = "{}.txt".format( os.path.splitext( file_name )[0] )
        with open( os.path.join( utils.TXTS_AS_DATA, "texts_minus_NNP", txt_file_name ), "w" ) as nnpless_file:
            nnpless_file.write( nnpless_text )

# Main
create_texts_without_nnps()
