import pytest

from puzzle.state import State, GOAL_STATE
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.a_star import AStar


def apply(tiles, actions):
    """Aplica as ações ao estado e retorna as peças finais."""
    state = State(tiles)
    for action in actions:
        state = next(s for s in state.neighbors() if s.action == action)
    return state.tiles


CASES = [
    ((1, 2, 3, 4, 5, 6, 7, 8, 0), 0),
    ((1, 2, 3, 4, 5, 6, 7, 0, 8), 1),
    ((1, 2, 3, 4, 0, 6, 7, 5, 8), 2),
    ((4, 1, 3, 7, 2, 6, 0, 5, 8), None),
    ((8, 6, 7, 2, 5, 4, 3, 0, 1), 31),   # um dos estados mais difíceis
]


def test_neighbors_corner():
    children = State((0, 1, 2, 3, 4, 5, 6, 7, 8)).neighbors()
    assert {c.action for c in children} == {"DOWN", "RIGHT"}
    assert all(c.cost == 1 for c in children)


def test_neighbors_center():
    assert len(State((1, 2, 3, 4, 0, 5, 6, 7, 8)).neighbors()) == 4


def test_path_and_actions():
    s0 = State((1, 2, 3, 4, 5, 6, 7, 0, 8))
    s1 = next(s for s in s0.neighbors() if s.action == "RIGHT")
    assert s1.is_goal
    assert s1.path() == [s0, s1]
    assert s1.actions() == ["RIGHT"]
    assert s0.actions() == []


@pytest.mark.parametrize("tiles,_", CASES)
def test_heuristic_admissible_zero_at_goal(tiles, _):
    assert AStar().heuristic(State(GOAL_STATE)) == 0
    assert AStar().heuristic(State(tiles)) >= 0


@pytest.mark.parametrize("tiles,optimal", CASES)
def test_bfs_and_astar_optimal(tiles, optimal):
    bfs = BFS().search(State(tiles))
    ast = AStar().search(State(tiles))
    assert bfs.found and ast.found
    assert bfs.path_cost == ast.path_cost
    if optimal is not None:
        assert ast.path_cost == optimal
    for r in (bfs, ast):
        assert apply(tiles, r.actions) == GOAL_STATE
        assert r.depth == len(r.actions) == r.path_cost
    assert ast.nodes_expanded <= bfs.nodes_expanded


@pytest.mark.parametrize("tiles,_", CASES[:4])
def test_dfs_finds_valid_solution(tiles, _):
    r = DFS().search(State(tiles))
    assert r.found
    assert apply(tiles, r.actions) == GOAL_STATE
    assert r.depth <= 50


def test_dfs_respects_depth_limit():
    r = DFS(depth_limit=1).search(State((1, 2, 3, 4, 0, 6, 7, 5, 8)))
    assert not r.found


@pytest.mark.parametrize("tiles", [
    (1, 2, 3, 4, 5, 6, 8, 7, 0),
    (2, 8, 3, 1, 6, 4, 7, 0, 5),   # exemplo do main.py: paridade ímpar
])
def test_unsolvable(tiles):
    assert not State(tiles).is_solvable()
    for algo in (BFS(), DFS(), AStar()):
        r = algo.search(State(tiles))
        assert not r.found and r.actions == [] and r.path_cost == -1
