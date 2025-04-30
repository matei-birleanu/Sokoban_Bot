from typing import List
from sokoban import Map

def beam_search(
    initial_state,
    K,
    heuristic
):

    beam: List[tuple[Map, List[Map], int]] = [(initial_state, [initial_state], 0)]
    # Set pentru a retine starile vizitate
    visited = {str(initial_state)}

    while beam:
        candidates: List[tuple[Map, List[Map], int, float]] = []
        
        # Extind fiecare stare din beam
        for state, path_states, g in beam:
            for move in state.filter_possible_moves():
                child = state.copy()
                child.apply_move(move)
                key = str(child)
                if key in visited:
                    continue
                visited.add(key)
                # Euristica negativa pentru sortare descrescatoare
                h = -heuristic(child)
                candidates.append((child, path_states + [child], g + 1, h))

        # Daca nu exista candidati nu mai putem extinde
        if not candidates:
            return []

        # Sortez candidatii dupa scor si retin primii K
        candidates.sort(key=lambda x: x[3], reverse=True)
        beam = [(s, p_states, g) for s, p_states, g, _ in candidates[:K]]

        # Verific daca in noul beam exista solutia
        for state, path_states, _ in beam:
            if state.is_solved():
                return path_states, len(visited)

    return []
