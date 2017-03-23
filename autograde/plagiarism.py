from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import pairwise_distances
import numpy
import difflib

def ngram(files):
    text = [ open(file).read() for file in files]
    vec = TfidfVectorizer(analyzer='char', ngram_range=(5,12), lowercase=False)
    X = vec.fit_transform(text)
    D = pairwise_distances(X)
    ix = D.argsort(axis=None)
    J = numpy.array([numpy.unravel_index(i, D.shape) for i in ix])
    K = numpy.array([Ji for Ji in J if Ji[0]<Ji[1]])
    return K

def ed(files):
    text = [ open(file).read() for file in files]
    result = []
    for i in range(len(text)):
        for j in range(len(text)):
            if i < j:
                result.append((i,j,difflib.SequenceMatcher(a=text[i], b=text[j], autojunk=False).ratio()))
                               
    return sorted(result, key=lambda x: x[2], reverse=True)
                               