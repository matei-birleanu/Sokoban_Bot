from math import inf
from typing import List

from sokoban.map import Map


def lrtastar(
    initial_map,
    heuristic,
    max_steps
):

    H = {}

    current = initial_map
    start_key = str(current)
    H[start_key] = heuristic(current)

    path = [current.copy()]

    for step in range(max_steps):
        if current.is_solved():
            print(f"Is solved: {current.is_solved()}")
            break

        # Generez succesorii
        successors = []
        for move in current.filter_possible_moves():
            neighbor = current.copy()
            neighbor.apply_move(move)
            successors.append((move, neighbor))

        if not successors:
            break

        # Aleg succesorul cu cost minim
        best_cost = inf
        best_neighbor = None  

        for move, neighbor in successors:
            key = str(neighbor)
            # Daca nu am mai vazut starea initializez H cu valoarea euristica
            if key not in H:
                H[key] = heuristic(neighbor)

            f_cost = 1 + H[key]
            if f_cost < best_cost:
                best_cost = f_cost
                best_neighbor = neighbor

        # Updatez estimarea euristica
        H[str(current)] = best_cost

        # Trec la succesorul ales
        current = best_neighbor
        path.append(current.copy())

    num_learned_states = len(H)
    return path, num_learned_states
