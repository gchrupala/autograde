from __future__ import division

import numpy
def uvt_round(grade):
    if grade < 6.0 and grade > 5.0:
        return numpy.round(grade)
    else:
        return numpy.round(grade*2)/2
    
uvt_round = numpy.vectorize(uvt_round)

