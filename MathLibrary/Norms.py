# =================================== Vector Norms ================================================


def euclidean_norm(v):
    return p_norm(v, 2)


def manhattan_norm(v):
    return p_norm(v, 1)


def p_norm(v, p):
    if p < 1:
        raise ValueError
    valSum = 0
    for x in v:
        valSum += pow(abs(x), p)
    return pow(valSum, 1 / p)


def supremum(p, s):
    if len(s) > len(p):
        raise IndexError
    sup = 0
    for i in s:
        if p[i] > sup:
            sup = p[i]
    return sup


def infimum(p, s):
    inf = p[s[0]]
    for i in s:
        if p[i] < inf:
            inf = p[i]


# =================================== Matrix Norms ================================================


def one_norm(m):
    if not is_matrix(m):
        raise ValueError

    columnSums = []
    for c in range(len(m[0])):
        columnSums.append(manhattan_norm(column(m, c)))
    return max(columnSums)


def infinity_norm(m):
    if not is_matrix(m):
        raise ValueError

    rowSums = []
    for r in range(len(m)):
        rowSums.append(manhattan_norm(m[r]))
    return max(rowSums)


def frobenius_norm(m):
    if not is_matrix(m):
        raise ValueError

    valSum = 0
    for r in range(len(m)):
        for c in range(len(m[r])):
            valSum += pow(abs(m[r][c]), 2)
    return pow(valSum, 1 / 2)


def max_norm(m):
    if not is_matrix(m):
        raise ValueError

    vals = []
    for r in range(len(m)):
        for c in range(len(m[0])):
            vals.append(abs(m[r][c]))
    return max(vals)


def is_matrix(m):
    r = len(m)
    c = len(m[0])
    for x in range(r):
        if len(m[x]) != c:
            return False
    return True


def column(m, i):
    if not is_matrix(m):
        raise ValueError
    c = []
    for row in m:
        c.append(row[i])
    return c
