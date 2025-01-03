def remove_repetitions(array): # removes repeting element of array
    res = []
    for i in array:
        if not i in res:
            res.append(i)
    return res

def zeroer(value, subtractor):
    if subtractor > abs(value):
        return 0
    elif value > 0:
        return float(value) - subtractor
    else:
        return float(value) + subtractor