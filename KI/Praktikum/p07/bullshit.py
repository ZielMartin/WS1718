import numpy

training_data = [
    (numpy.array([0, 0]), 0),
    (numpy.array([0, 1]), 1),
    (numpy.array([1, 0]), 1),
    (numpy.array([1, 1]), 1)
    ]

eta = .5

w = [0, 0, 0]

iterations = 2

table = []

def pretty_print(content):
    header = ["w1", "w2", "theta", "x1", "x2", "k", "sum", "vorhersage", "änderung"]
    row_format ="{:>20}" * (len(header) )
    print(row_format.format(*header))
    for row in content:
        print(row_format.format(*row))

def sumFunc(inputs):
    s = 0
    for i in range(len(inputs)):
        s += inputs[i] * w[i]
    s -= w[len(inputs)]
    return s

myDot = lambda inp: numpy.dot(inp, w[1:]) * w[0]

def sign(_sign):
    if _sign <= 0: return False
    return True

def aenderung(u):
    if u > 0.0:
        return "+"
    elif u < 0.0:
        return "-"
    else:
        return "="



for iteration in range(iterations):
    table.append(["_____"] * 9)
    for inp, k in training_data:
        activation = myDot(inp)
        predicted = sign(activation)
        update = eta * (k - predicted)
        w[1:] += update * inp
        w[0] += update
        table.append([w[0], w[1], w[2], inp[0], inp[1], k, sumFunc(inp), predicted, aenderung(update)])

pretty_print(table)
