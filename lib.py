def remove_repetitions(array): # removes repeting element of array
    res = []
    for i in array:
        if not i in res:
            res.append(i)
    return res
