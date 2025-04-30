from collections import deque
from math import inf
from functools import lru_cache
from sokoban.map import Map, OBSTACLE_SYMBOL
from typing import Callable
from scipy.optimize import linear_sum_assignment
from collections import deque
from sokoban.moves import LEFT, RIGHT, UP, DOWN
import math


def manhattan_heuristic(state):
    """
    Heuristica este suma distantelor Manhattan de la fiecare cutie
    pana la cea mai apropiata tinta
    """

    total = 0.0
    for box in state.boxes.values():
        # Distanta Manhattan pana la fiecare tinta
        dists = [
            abs(box.x - tx) + abs(box.y - ty)
            for (tx, ty) in state.targets
        ]
       # Aleg minimul
        total += min(dists)
    return total


def box_to_goal_heuristic(state, metric= "manhattan"):
    """
    Pentru fiecare cutie calculeaza distanta minima pana la oricare target din state targets
    si insumeaza toate aceste distante
    """
    total = 0.0

    for box in state.boxes.values():
        bx, by = box.x, box.y
        best = math.inf

        for gx, gy in state.targets:
            if metric == "manhattan":
                d = abs(bx - gx) + abs(by - gy)
            elif metric == "euclidean":
                d = math.hypot(bx - gx, by - gy)
            if d < best:
                best = d

        total += best

    return total

def misplaced_boxes_heuristic(state):
    # Numar de cutii care nu sunt inca pe un target
    box_positions   = set(state.positions_of_boxes.keys())
    target_positions = set(state.targets)
    num_misplaced = len(box_positions - target_positions)
    return float(num_misplaced)




def hungarian_player_and_boxes_heuristic(state: Map) -> float:
    boxes = list(state.boxes.values())
    targets = state.targets
    n = len(boxes)

    # Construiesc matricea costurilor cutie tinta
    cost_matrix = [
        [abs(b.x - tx) + abs(b.y - ty) for (tx, ty) in targets]
        for b in boxes
    ]

    # Gaseste matching de cost minim
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    cost_pushes = sum(cost_matrix[i][j] for i, j in zip(row_ind, col_ind))

    # Distanta jucator cea mai apropiata cutie
    walk_to_box = min(
        abs(state.player.x - b.x) + abs(state.player.y - b.y)
        for b in boxes
    ) if boxes else 0

    return cost_pushes + walk_to_box



initial_map = Map.from_yaml("tests/super_hard_map1.yaml")
def build_target_distance_map(m: Map):
    """
    Pentru fiecare tinta creeaza o harta distante x y egal
    numarul minim de pasi fara cutii de la x y la tinta
    """

    dist_map = {}
    for tx, ty in m.targets:
        dist = [[inf]*m.width for _ in range(m.length)]
        q = deque([(tx, ty)])
        dist[tx][ty] = 0

        while q:
            x, y = q.popleft()
            for move in (LEFT, RIGHT, UP, DOWN):
                nx, ny = {
                    LEFT:  (x, y-1),
                    RIGHT: (x, y+1),
                    UP:    (x+1, y),
                    DOWN:  (x-1, y),
                }[move]
                if (0 <= nx < m.length and 0 <= ny < m.width 
                   and m.map[nx][ny] != OBSTACLE_SYMBOL 
                   and dist[nx][ny] == inf):
                    dist[nx][ny] = dist[x][y] + 1
                    q.append((nx, ny))

        dist_map[(tx, ty)] = dist
    return dist_map
# Fac un bfs pentru a avea disttnele deja calculate
static_dist = build_target_distance_map(initial_map)

def bfs_static_heuristic(state: Map) -> float:

    total = 0.0

    for box in state.boxes.values():
        best = inf
        for tgt, dist_grid in static_dist.items():
            d = dist_grid[box.x][box.y]
            if d < best:
                best = d
        total += best

    if state.boxes:
        walk = min(
            abs(state.player.x - b.x) + abs(state.player.y - b.y)
            for b in state.boxes.values()
        )
    else:
        walk = 0

    return total + walk



def greedy_matching_heuristic(state: Map) -> float:
    """
    H state este suma greedy a distantelor Manhattan cutie tinta
    plus distanta Manhattan jucator cea mai apropiata cutie
    """

    boxes = list(state.boxes.values())
    targets = state.targets.copy()

    cost_pushes = 0
    unmatched_boxes = boxes.copy()
    unmatched_targets = targets.copy()

    while unmatched_boxes and unmatched_targets:
        # perechea (cutie tinta) cu distanta minima
        best_dist = float('inf')
        best_pair = None
        for b in unmatched_boxes:
            for t in unmatched_targets:
                d = abs(b.x - t[0]) + abs(b.y - t[1])
                if d < best_dist:
                    best_dist = d
                    best_pair = (b, t)
        cost_pushes += best_dist
        unmatched_boxes.remove(best_pair[0])
        unmatched_targets.remove(best_pair[1])

    # distanta jucator cea mai apropiata cutie 
    if boxes:
        walk_to_box = min(
            abs(state.player.x - b.x) + abs(state.player.y - b.y)
            for b in boxes
        )
    else:
        walk_to_box = 0

    return cost_pushes + walk_to_box


def bfs_heuristic(state: Map) -> float:
    """
    H state este suma distantelor reale boxa cea mai apropiata tinta
    plus distanta reala jucator cea mai apropiata cutie
    Toate distantele sunt calculate cu BFS ignorand doar obstacolele map obstacles
    """
    L, W = state.length, state.width


    dist = [[inf]*W for _ in range(L)]
    q = deque()
    for tx, ty in state.targets:
        dist[tx][ty] = 0
        q.append((tx, ty))

    while q:
        x, y = q.popleft()
        for dx, dy in ((0,1),(0,-1),(1,0),(-1,0)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < L and 0 <= ny < W \
               and state.map[nx][ny] != OBSTACLE_SYMBOL \
               and dist[nx][ny] == inf:
                dist[nx][ny] = dist[x][y] + 1
                q.append((nx, ny))

    total = 0.0
    for box in state.boxes.values():
        total += dist[box.x][box.y]

    visited = [[False]*W for _ in range(L)]
    qp = deque([(state.player.x, state.player.y, 0)])
    visited[state.player.x][state.player.y] = True
    walk = 0
    found = False
    while qp and not found:
        x, y, d = qp.popleft()
        if (x, y) in state.positions_of_boxes:
            walk = d
            break
        for dx, dy in ((0,1),(0,-1),(1,0),(-1,0)):
            nx, ny = x+dx, y+dy
            if 0 <= nx < L and 0 <= ny < W \
               and not visited[nx][ny] \
               and state.map[nx][ny] != OBSTACLE_SYMBOL:
                visited[nx][ny] = True
                qp.append((nx, ny, d+1))

    return total + walk


def advanced_heuristic(state: Map) -> float:
    """
    1) Detecteaza deadlock-uri: cutie (nu pe tinta) blocata de 2 obstacole - cost = inf.
    2) BFS multi-tinta (cached) pentru distanta minima celula-tinta.
    3) H = suma(distante box-tinta) + min_Manhattan(player-cutie).
    """

    L, W = state.length, state.width

    def is_wall(x, y):
        return not (0 <= x < L and 0 <= y < W) or state.map[x][y] == OBSTACLE_SYMBOL

    for box in state.boxes.values():
        if (box.x, box.y) in state.targets:
            continue
        x, y = box.x, box.y
        if (is_wall(x-1, y) and is_wall(x, y-1)) or \
           (is_wall(x-1, y) and is_wall(x, y+1)) or \
           (is_wall(x+1, y) and is_wall(x, y-1)) or \
           (is_wall(x+1, y) and is_wall(x, y+1)):
            return inf

    @lru_cache(maxsize=1)
    def build_distances():
        dist = [[inf]*W for _ in range(L)]
        q = deque()
        for tx, ty in state.targets:
            dist[tx][ty] = 0
            q.append((tx, ty))
        while q:
            x, y = q.popleft()
            for dx, dy in ((0,1),(0,-1),(1,0),(-1,0)):
                nx, ny = x+dx, y+dy
                if 0 <= nx < L and 0 <= ny < W and \
                   state.map[nx][ny] != OBSTACLE_SYMBOL and \
                   dist[nx][ny] == inf:
                    dist[nx][ny] = dist[x][y] + 1
                    q.append((nx, ny))
        return dist

    dist_map = build_distances()

    total = 0.0
    for box in state.boxes.values():
        d = dist_map[box.x][box.y]
        total += (d if d < inf else 1e6)

    if state.boxes:
        walk = min(
            abs(state.player.x - b.x) + abs(state.player.y - b.y)
            for b in state.boxes.values()
        )
    else:
        walk = 0

    return total + walk


def bfs_hungarian_heuristic(state: Map) -> float:

    L, W = state.length, state.width

    def is_wall(x, y):
        return not (0 <= x < L and 0 <= y < W) or state.map[x][y] == OBSTACLE_SYMBOL

    for box in state.boxes.values():
        if (box.x, box.y) in state.targets:
            continue
        x, y = box.x, box.y
        if (is_wall(x-1,y) and is_wall(x,y-1)) or \
           (is_wall(x-1,y) and is_wall(x,y+1)) or \
           (is_wall(x+1,y) and is_wall(x,y-1)) or \
           (is_wall(x+1,y) and is_wall(x,y+1)):
            return inf

    @lru_cache(maxsize=1)
    def build_target_distances():
        dist = [[inf]*W for _ in range(L)]
        q = deque()
        for tx, ty in state.targets:
            dist[tx][ty] = 0
            q.append((tx, ty))
        while q:
            x, y = q.popleft()
            for dx, dy in ((0,1),(0,-1),(1,0),(-1,0)):
                nx, ny = x+dx, y+dy
                if 0 <= nx < L and 0 <= ny < W \
                   and state.map[nx][ny] != OBSTACLE_SYMBOL \
                   and dist[nx][ny] == inf:
                    dist[nx][ny] = dist[x][y] + 1
                    q.append((nx, ny))
        return dist

    dist = build_target_distances()

    boxes = list(state.boxes.values())
