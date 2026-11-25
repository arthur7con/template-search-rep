from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):
    """Busca em Largura: explora os estados nível a nível (fila FIFO).

    Como todos os movimentos custam 1, a BFS encontra a solução ótima.
    """

    def search(self, initial: State) -> SearchResult:
        nodes_expanded = 0
        nodes_generated = 1          # o estado inicial
        max_frontier = 1

        if initial.is_goal:
            return SearchResult(initial, nodes_expanded, nodes_generated, max_frontier, initial.cost)

        if not initial.is_solvable():
            return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)

        frontier = deque([initial])
        reached = {initial.tiles}    # estados já gerados (fronteira + explorados)

        while frontier:
            state = frontier.popleft()
            nodes_expanded += 1

            for child in state.neighbors():
                nodes_generated += 1
                if child.tiles in reached:
                    continue
                # teste de objetivo na geração (early goal test)
                if child.is_goal:
                    return SearchResult(child, nodes_expanded, nodes_generated, max_frontier, child.cost)
                reached.add(child.tiles)
                frontier.append(child)

            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)
