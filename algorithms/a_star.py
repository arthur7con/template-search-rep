import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

# posição (linha, coluna) de cada peça no estado objetivo
_GOAL_POSITIONS = {tile: divmod(i, 3) for i, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):
    """Busca A*: expande o nó com menor f(n) = g(n) + h(n).

    Com a heurística da Distância de Manhattan (admissível e consistente),
    o A* encontra a solução ótima expandindo bem menos nós que a BFS.
    """

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan: soma das distâncias de cada peça até sua
        posição no objetivo (o espaço vazio não é contado)."""
        distance = 0
        for i, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            row, col = divmod(i, 3)
            goal_row, goal_col = _GOAL_POSITIONS[tile]
            distance += abs(row - goal_row) + abs(col - goal_col)
        return distance

    def search(self, initial: State) -> SearchResult:
        nodes_expanded = 0
        nodes_generated = 1          # o estado inicial
        max_frontier = 1

        if not initial.is_solvable():
            return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)

        tie = count()                # desempate estável entre nós com mesmo f
        h0 = self.heuristic(initial)
        frontier = [(initial.cost + h0, h0, next(tie), initial)]
        best_g = {initial.tiles: initial.cost}
        explored = set()

        while frontier:
            _, _, _, state = heapq.heappop(frontier)

            if state.tiles in explored:
                continue             # entrada antiga com custo pior

            # teste de objetivo na remoção da fronteira (garante otimalidade)
            if state.is_goal:
                return SearchResult(state, nodes_expanded, nodes_generated, max_frontier, state.cost)

            explored.add(state.tiles)
            nodes_expanded += 1

            for child in state.neighbors():
                nodes_generated += 1
                if child.tiles in explored:
                    continue
                if child.cost < best_g.get(child.tiles, float("inf")):
                    best_g[child.tiles] = child.cost
                    h = self.heuristic(child)
                    heapq.heappush(frontier, (child.cost + h, h, next(tie), child))

            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, nodes_expanded, nodes_generated, max_frontier, 0)
