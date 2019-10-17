import spacy
import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
import utils
import psutil
import os
from tqdm import tqdm

def qualifying_token( token ):
    qualify = False
    if ( len( token.lemma_ ) > 1 ) or ( token.lemma_.isalnum() ):
        qualify = True
        # We don't want person names, they cause big variance between texts
        # while not being tremendously revealing of readers' interest.
        # if token.tag_ == "NNP":
        #      qualify = False
    return qualify

file_names = utils.get_file_names_by_extension( utils.POS_PATH, "pickle" )
docs = []
with tqdm( total=len(file_names) ) as pbar:
    for file_name in file_names:
        with open( os.path.join( utils.POS_PATH, file_name ), "rb" ) as file:
            doc = pickle.load( file )
            # How hacky is this?
            # token_lemma : we umap on lemmas
            # token_lemma + token_tag : we umap on lemmaPOS
            # docs.append( " ".join( [token.lemma_ for token in doc if qualifying_token( token ) ] ) )
            docs.append( " ".join( ["{}{}".format( token.lemma_, token.tag_ ) for token in doc if qualifying_token( token ) ] ) )
            process = psutil.Process( os.getpid() )
            pbar.set_postfix( {"mem": (process.memory_info().rss/1000000) }, refresh=False ) # in bytes
            pbar.update( 1 )
vectorizer = TfidfVectorizer()
tfidf = vectorizer.fit_transform( docs )
print( tfidf.shape )
with open( os.path.join( utils.TFIDF_PATH, "20190919_2357/tfidf_20191001_1624.pickle" ), "wb" ) as file:
    pickle.dump( tfidf, file )
with open( os.path.join( utils.TFIDF_PATH, "20190919_2357/vect_20191001_1624.pickle" ), "wb" ) as file:
    pickle.dump( vectorizer, file )
