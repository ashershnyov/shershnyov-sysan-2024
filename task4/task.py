# Мне стыдно за этот код, но работает же
import math

_TEST_DATA = [
    [20, 15, 10, 5],
    [30, 20, 15, 10],
    [25, 25, 20, 15],
    [20, 20, 25, 20],
    [15, 15, 30, 25],
]

def calc_enthropy(p: list[list[float]|float]) -> float:
    """Расчет энтропии для матрицы/списка вероятностей"""
    h = 0
    if isinstance(p[0], list):
        for row in p:
            h += calc_enthropy(row)
    else:
        for val in p:
            h -= val * math.log2(val)
    return h

def main(m: list[list[float]]) -> tuple[float]:
    s = 0
    sum_y = [0.0] * len(m)
    sum_x = [0.0] * len(m[0])

    for row in m:
        s += sum(row)

    for i, row in enumerate(m):
        for j in range(len(row)):
            row[j] /= s
            sum_x[j] += row[j]
        sum_y[i] = sum(row)

    h_xy = calc_enthropy(m)
    h_y = calc_enthropy(sum_y)
    h_x = calc_enthropy(sum_x)

    for i, row in enumerate(m):
        for j in range(len(row)):
            row[j] /= sum_y[i]

    h_cond = 0.0
    for i, row in enumerate(m):
        tmp_cond_h = calc_enthropy(row)
        h_cond += sum_y[i] * tmp_cond_h

    i_xy = h_x - h_cond

    return tuple(map(lambda x: round(x, 2), (h_xy, h_y, h_x, h_cond, i_xy)))

if __name__ == "__main__":
    res = main(_TEST_DATA)
    print(res)
