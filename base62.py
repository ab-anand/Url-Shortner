import string



def toBase62(num, base = 62):
    '''input: any base10 integer
    returns: base62 string of the input
    '''
    if base <= 0 or base > 62:
        return 0

    values = string.digits + string.ascii_lowercase + string.ascii_uppercase

    r = num % base
    res = values[r];
    q = num // base

    while q:
        r = q % base
        q = q // base
        res = values[int(r)] + res

    return res


def toBase10(num, b = 62):
    '''input: base62 string
    returns:  base10 integer value of the input
    '''
    base = string.digits + string.ascii_lowercase + string.ascii_uppercase

    limit = len(num)
    res = 0

    for i in range(limit):
        res = b * res + base.find(num[i])

    return res

# print(toBase62(1000000))
# print(toBase10('1'))