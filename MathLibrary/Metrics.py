from numpy.linalg import matrix_power


def Manhattan(x, y):
    if len(x) is not len(y):
        raise ValueError

    distance = 0
    for i in range(len(x)):
        distance += abs(x[i] - y[i])

    return distance


def Chebyshev(x, y):
    if len(x) is not len(y):
        raise ValueError

    distance = 0
    max = 0
    for i in range(len(x)):
        distance = abs(x[i] - y[i])
        if distance < max:
            distance = max

    return distance


def Euclidian(x, y):
    if len(x) is not len(y):
        raise ValueError

    distance = 0
    for i in range(len(x)):
        distance += pow(y[i] - x[i], 2) ** (1 / 2)

    return distance


def Canberra(x, y):
    if len(x) is not len(y):
        raise ValueError

    distance = 0
    for i in range(len(x)):
        distance += abs(x[i] - y[i]) / (abs(x[i]) + abs(y[i]))

    return distance


def Cosine(x, y):
    if len(x) is not len(y):
        raise ValueError

    numerator = 0
    denominator = 0
    for i in range(len(x)):
        numerator += x[i] * y[i]
        denominator += (x[i] ** 2) * (y[i] ** 2)
    denominator = denominator ** (1 / 2)

    return numerator / denominator


def Hamming(x, y):
    if len(x) is not len(y):
        raise ValueError

    distance = 0
    for i in range(len(x)):
        if x[i] == y[i]:
            distance += 1

    return distance


def Discrete(x, y):
    if len(x) is not len(y):
        raise ValueError

    distance = 0
    if x is not y:
        distance = 1

    return distance


def Metric(distance, x, y, z):
    if IdentityAndIndiscernable(distance, x, y) \
            and Symmetric(distance, x, y) \
            and TriangleInequality(distance, x, y, z):
        return "Possibly"

    return False


def IdentityAndIndiscernable(distance, x, y):
    if distance(x, y) is not 0:
        raise ValueError
    if x is not y:
        raise ValueError
    if (distance(x, y) is 0 and x is not y) or (distance(x, y) is not 0 and x is y):
        return False

    return True


def Symmetric(distance, x, y):
    if distance(x, y) is distance(y, x):
        return True

    return False


def TriangleInequality(distance, x, y, z):
    if distance(x, y) <= distance(x, z) + distance(z, y):
        return True

    return False
