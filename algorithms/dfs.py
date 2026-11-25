from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):
    """Busca em Profundidade com limite de profundidade (pilha LIFO).

    O limite evita que a busca desça indefinidamente. Um estado já visitado
    só é reexplorado se for alcançado com profundidade menor do que antes,
    o que evita ciclos sem perder soluções dentro do limite.
    A DFS não garante a solução ótima.
    """

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        nodes_expanded = 0
        nodes_generated = 1          # o estado inicial
        max_frontier = 1

        if initial.is_goal:
            return SearchResult(initial, nodes_expanded, nodes_generated, max_frontier, initial.cost)

        if not initial.is_solvable():
            return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)

        stack = [initial]
        best_depth = {initial.tiles: 0}   # menor profundidade em que cada estado foi visto

        while stack:
            state = stack.pop()

            # entrada desatualizada: o estado foi reencontrado mais raso depois
            if best_depth.get(state.tiles, float("inf")) < state.cost:
                continue

            if state.is_goal:
                return SearchResult(state, nodes_expanded, nodes_generated, max_frontier, state.cost)

            if state.cost >= self.depth_limit:
                continue

            nodes_expanded += 1
            # empilha em ordem reversa para expandir na ordem UP, DOWN, LEFT, RIGHT
            for child in reversed(state.neighbors()):
                nodes_generated += 1
                if child.cost < best_depth.get(child.tiles, float("inf")):
                    best_depth[child.tiles] = child.cost
                    stack.append(child)

            max_frontier = max(max_frontier, len(stack))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)
