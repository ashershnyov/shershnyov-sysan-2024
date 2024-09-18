import json
import typing as tp

TEST_STRING = """
    {
        "1": {
            "2": {
                "3": {
                    "5": {},
                    "6": {}
                },
                "4": {
                    "7": {},
                    "8": {}
                }
            }
        }
    }
"""


def get_object_from_json_string(object_string: str) -> tp.Dict[str, tp.Any]:
    """Разбор json-строки в словарь"""
    return json.loads(object_string)


def recursive_graph_parse(
    graph: tp.Dict[str, tp.Dict],  # Ветка от текущей вершины графа
    graph_repr: tp.Dict[str, tp.Dict],  # Общий словарь репрезентации графа
    parent: tp.Optional[str]=None  # Родитель текущей вершины
) -> None:
    """Рекурсивное разложение графа на импровизированную матрицу смежности - для каждой вершины набор детей и родитель"""
    # Проход по всем детям текущей вершины
    for key, val in graph.items():
        children = []
        if isinstance(val, dict) and val != dict():
            # Если у ребенка есть свои дети, парсим граф от него
            recursive_graph_parse(val, graph_repr, key)
            # Записываем детей текущего ребенка
            children = list(val.keys())
        # Текущего ребенка в итоговую репрезентацию графа
        graph_repr[key] = [children, parent]


def main() -> None:
    source_graph = get_object_from_json_string(TEST_STRING)
    graph_repr ={}
    recursive_graph_parse(source_graph, graph_repr)
    # Сортировка полученной репрезенации по возрастанию номеров вершин
    sorted_repr = {key: val for key, val in sorted(graph_repr.items(), key=lambda x: x[0])}
    print(sorted_repr)


if __name__ == "__main__":
    main()
