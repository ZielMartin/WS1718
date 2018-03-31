import numpy

training_data = [
    (numpy.array([0, 0]), 0),
    (numpy.array([0, 1]), 1),
    (numpy.array([1, 0]), 1),
    (numpy.array([1, 1]), 1)
    ]

eta = .5

w = numpy.array([0.0, 0.0, 0.0])

iterations = 20

table = []

def pretty_print(content):
    header = ["w1", "w2", "-theta", "x1", "x2", "k", "sum", "vorhersage", "änderung"]
    row_format ="{:>20}" * (len(header) )
    print(row_format.format(*header))
    for row in content:
        print(row_format.format(*row))

def myDot(inp):
    x = numpy.append([1], inp)

    print("<",x,",",w,"> = ", numpy.dot(x,w))

    return numpy.dot(x, w)

def sign(_sign):
    if _sign < 0: return 0
    return 1

def aenderung(u):
    if u > 0.0: return "+"
    elif u < 0.0: return "-"
    else: return "="

repeat = True
while(repeat):
    repeat = False
    table.append(["_____"] * 9)
    for inp, k in training_data:
        dot = myDot(inp)
        predicted = sign(dot)
        update = eta * (k - predicted)
        if update != 0.0:
            repeat = True
        w[1:] += update * inp
        w[0] += update

        table.append([w[1], w[2], w[0], inp[0], inp[1], k, dot, predicted, aenderung(update)])

pretty_print(table)
