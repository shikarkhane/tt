def split_by_first_occurance(s, find_s):
    '''
    desc: split a string into 2 parts based on the position of find_s parameter in s
    returns: a list with 2 elements
    '''
    p = s.find(find_s)
    return [s[0:p], s[p+1:]]

