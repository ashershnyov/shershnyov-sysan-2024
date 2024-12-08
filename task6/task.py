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

REGULATOR_RULES = """
{
    "холодно":"интенсивно",
    "комфортно":"умеренно",
    "жарко":"слабо"
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


def fuzz(rule: str, val: float, funcs: tp.Dict[str, tp.List[GraphCoefs]]) -> float:
    for func in funcs[rule]:
        if func.l_border <= val <= func.r_border:
            y = func.k * val + func.b
            return max(0.0, y)
    return 0.0


def activate(rule: str, val: float, funcs: tp.Dict[str, tp.List[GraphCoefs]]) -> float:
    for func in funcs[rule]:
        if func.k == 0:
            continue
        v = (val - func.b) / func.k
        if func.l_border <= v <= func.r_border:
            return v
    return 0.0


def main(val_to_phase: float) -> float:
    students = json.loads(INPUT)
    stud_to_func = input_to_funcs(students)

    regulator = json.loads(REGULATOR)
    reg_to_func = input_to_funcs(regulator)

    reg_rules = json.loads(REGULATOR_RULES)
    rules_if = {}
    rules_then = {}
    rules_total = []
    for rule_if, rule_then in reg_rules.items():
        # Фаззификация на 1 множество (множество температур)
        fuzzed = fuzz(rule_if, val_to_phase, stud_to_func)
        rules_if[rule_if] = fuzzed
        # Агрегирование на 2 множестве
        activated = activate(rule_then, fuzzed, reg_to_func)
        rules_then[rule_then] = activated
        # Активация методом min-активации на втром множестве
        rules_total.append(min(fuzzed, activated))

    print(rules_if)
    print(rules_then)
    print(rules_total)

    r_i = rules_total.index(max(rules_total))
    rule_to_use = list(rules_then.keys())[r_i]

    # Возвращаем ближайший максимум
    for r in regulator[rule_to_use]:
        if r[1] == 1 and r[0] > rules_then[rule_to_use]:
            return r[0]
    return 0.0

if __name__ == "__main__":
    res = main(17)
    print(res)
