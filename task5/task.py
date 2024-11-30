import json
import typing as tp

RANGING_A = "[1, [2, 3], 4, [5, 6, 7], 8, 9, 10]"
RANGING_B = "[[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]"

Matrix = list[list[int]]
Range = list[tp.Union[list[int], int]]

def make_range_matrix(r: Range) -> Matrix:
    ranks = {}
    for i, val in enumerate(r):
        if isinstance(val, list):
            for v in val:
                ranks[v] = i
        else:
            ranks[val] = i
    m = []
    for _, v_1 in sorted(ranks.items(), key=lambda k: k[0]):
        row = []
        for _, v_2 in sorted(ranks.items(), key=lambda k: k[0]):
            if v_2 <= v_1:
                row.append(1)
            else:
                row.append(0)
        m.append(row)
    return m

def matrix_logical_and(r1: Matrix, r2: Matrix) -> Matrix:
    m = []
    for i in range(len(r1)):
        row = [r1[i][j] & r2[i][j] for j in range(len(r1[i]))]
        m.append(row)
    return m


def main(r1: str, r2: str) -> str:
    range_1 = json.loads(r1)
    range_2 = json.loads(r2)
    matrix_1 = make_range_matrix(range_1)
    matrix_2 = make_range_matrix(range_2)
    res_matrix = matrix_logical_and(matrix_1, matrix_2)
    res = []
    for i in range(len(res_matrix)):
        for j in range(i, len(res_matrix[i])):
            if res_matrix[i][j] == res_matrix[j][i] and i != j:
                res.append([i + 1, j + 1])
    return json.dumps(res)

if __name__ == "__main__":
    res = main(RANGING_A, RANGING_B)
    print(res)
