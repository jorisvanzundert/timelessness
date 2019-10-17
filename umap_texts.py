import utils
import os
import pickle
from sklearn.cluster import KMeans
from sklearn.feature_selection import VarianceThreshold
import matplotlib.pyplot as plt
import numpy
import umap


with open( os.path.join( utils.TFIDF_PATH, "20190919_2357/tfidf_20191001_1624.pickle" ), "rb" ) as file:
    tfidf = pickle.load( file )
with open( os.path.join( utils.TFIDF_PATH, "20190919_2357/vect_20191001_1624.pickle" ), "rb" ) as file:
    vectorizer = pickle.load( file )

# Lesson learned: features that are names show the highest variance

selector = VarianceThreshold( threshold=0.0000001 )
print( len(vectorizer.vocabulary_))
X = selector.fit_transform( tfidf )
features_selected = selector.get_support(indices=True)
feature_names = vectorizer.get_feature_names()
variances = { "{} ({},{},{})".format( feature_names[feature], feature, idx, numpy.count_nonzero( X[:,idx].toarray() ) ):( selector.variances_[feature], numpy.count_nonzero( X[:,idx].toarray() ) ) for idx,feature in enumerate( features_selected ) }
sorted_variances = sorted( variances.items(), key=lambda kv: kv[1][1] )
for variance in reversed( sorted_variances ):
    print( variance[0], "{:.8f}".format( variance[1][0]) )
print( X.shape )
print( X[:,100] )
print( X[:,100].shape )
print( numpy.count_nonzero( X[:,100].toarray() ) )
# print( X.toarray().std(axis=0) )
print( min( selector.variances_ ) )
print( max( selector.variances_ ) )
print( len( selector.variances_ ) )

fit = umap.UMAP()
u = fit.fit_transform(X)
with open( os.path.join( utils.TFIDF_PATH, "20190919_2357/umap_20191001_1903.pickle" ), "wb" ) as file:
    pickle.dump( u, file )
