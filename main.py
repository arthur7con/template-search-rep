"""Script de demonstração — útil para depurar manualmente."""

from puzzle.state import State
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.a_star import AStar


def print_result(name: str, result):
    print(f"\n{'='*40}")
    print(f"Algoritmo : {name}")
    if result.found:
        print(f"Solução   : {' → '.join(result.actions)}")
        print(f"Custo     : {result.path_cost}")
        print(f"Profund.  : {result.depth}")
    else:
        print("Solução   : NÃO ENCONTRADA")
    print(f"Expandidos: {result.nodes_expanded}")
    print(f"Gerados   : {result.nodes_generated}")
    print(f"Fronteira : {result.max_frontier_size} (máx)")


if __name__ == "__main__":
    exemplos = [
        State((2, 8, 3, 1, 6, 4, 7, 0, 5)),   # exemplo original (sem solução: paridade ímpar)
        State((8, 6, 7, 2, 5, 4, 3, 0, 1)),   # 31 movimentos (um dos mais difíceis)
    ]

    for initial in exemplos:
        print(f"\n{'#'*40}\nEstado inicial:")
        print(initial)
        if not initial.is_solvable():
            print("(este estado não tem solução — número ímpar de inversões)")

        print_result("BFS",  BFS().search(initial))
        print_result("DFS",  DFS().search(initial))
        print_result("A*",   AStar().search(initial))
