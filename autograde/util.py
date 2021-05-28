from __future__ import division
import pandas as pd

import numpy
def uvt_round(grade):
    if grade < 6.0 and grade > 5.0:
        return numpy.round(grade)
    else:
        return numpy.round(grade*2)/2
    
uvt_round = numpy.vectorize(uvt_round)

def theavg(data):
    "Compute averages for thesis grades: input should be a 2x6 array."
    assert data.shape == (2,6)
    a = numpy.ceil(data.mean(axis=0) * 2) / 2
    components = ['rq','li','me', 're', 'di', 'pr']
    result = pd.DataFrame(data=dict(supervisor=data[0],
                                     secondreader=data[1],
                                     joint=a),
                           index=components)
    final = uvt_round(result['joint'].mean())
    return result, final

                           
