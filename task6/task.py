import json
import typing as tp

INPUT = """{
    "холодно": [
        [0, 1],
        [16, 1],
        [20, 0],
        [50, 0]
    ],
    "комфортно": [
        [16, 0],
        [20, 1],
        [22, 1],
        [26, 0]
    ],
    "жарко": [
        [0,0],
        [22,0],
        [26,1],
        [50,1]
    ]
}"""

REGULATOR = """
{
    "слабо":[[0,1],[6,1],[10,0],[20,0]],
    "умеренно":[[6,0],[10,1],[12,1],[16,0]],
    "интенсивно":[[0,0],[12,0],[16,1],[20,1]]
}
"""

REGULATOR_SWITCH = """
{
    'холодно':"интенсивно",
    'комфортно':"умеренно",
    'жарко':"слабо"
}
"""

class GraphCoefs:
    """Набор коэффициентов линейной функции"""
    def __init__(self, k: float, b: float, l: float, r: float) -> None:
        self.b = b
        """Коэф. перед x"""
        self.k = k
        """Свободный член"""
        self.l_border = l
        """Левая граница куска функции"""
        self.r_border = r
        """Правая граница куска функции"""

    def __str__(self):
        if self.k == 0:
            return f"y = {self.b}; x in [{self.l_border}; {self.r_border}]"
        return f"y = {self.k}*x + {self.b}; x in [{self.l_border}; {self.r_border}]"

    def __repr__(self):
        return self.__str__()


def get_linear_func(p_1: tp.Tuple[float, float], p_2: tp.Tuple[float, float]) -> tp.Tuple[float, float]:
    if p_2[1] == p_1[1]:
        return 0, p_2[1]
    k = (p_2[1] - p_1[1]) / (p_2[0] - p_1[0])
    b = p_2[1] - k * p_2[0]
    return k, b

def funcs_for_state(states: tp.List[tp.List[float]]) -> tp.List[GraphCoefs]:
    graphs = []
    for i, s in enumerate(states):
        if i == 0:
            continue
        gc = get_linear_func(s, states[i - 1]) # type: ignore
        graphs.append(GraphCoefs(gc[0], gc[1], states[i - 1][0], s[0]))
    return graphs


def input_to_funcs(input: tp.Dict[str, tp.List[tp.List[float]]]) -> tp.Dict[str, tp.List[GraphCoefs]]:
    res = {}
    for k, v in input.items():
        res[k] = funcs_for_state(v)
    return res


def fuzz(val: float, funcs: tp.Dict[str, tp.List[GraphCoefs]]) -> tp.List[float]:
    vals = []
    for f in funcs.values():
        for func in f:
            if func.l_border <= val <= func.r_border:
                y = func.k * val + func.b
                if y != 0:
                    vals.append(y)
    return vals


def defuzz(vals: tp.List[float], funcs: tp.Dict[str, tp.List[GraphCoefs]]) -> float | None:
    for val in vals:
        for f in funcs.values():
            for func in f:
                if func.k == 0:
                    continue
                v = (val - func.b) / func.k
                if func.l_border <= v <= func.r_border and func.k > 0:
                    return func.r_border
    return None


def main(val_to_phase: float) -> None:
    students = json.loads(INPUT)
    stud_to_func = input_to_funcs(students)
    regulator = json.loads(REGULATOR)
    reg_to_func = input_to_funcs(regulator)
    fuzzed = fuzz(val_to_phase, stud_to_func)
    print(fuzzed)
    defuzzed = defuzz(fuzzed, reg_to_func)
    print(defuzzed)

if __name__ == "__main__":
    main(17)
