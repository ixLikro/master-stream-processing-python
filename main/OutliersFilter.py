

def negativeFilter(x):
    if x[1] < 0:
        x[1] = None
    return x

def rangeFilter(value):
    if(value[1] is None):
        value[1] = None
        return value
    if value[1] > value[4]:
        value[1] = None
        return value
    if value[1] < value[3]:
        value[1] = None
    return value