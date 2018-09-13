def SubArraysOf(Array,Array_=None):
    if Array_ == None :
        Array_ = Array[:-1]
    if Array == []:
        if Array_ == []:
            return([])
        return( SubArraysOf(Array_,Array_[:-1]) )
    return([Array]+SubArraysOf(Array[1:],Array_))
