from sokoban.map import Map
from search_methods.lrta_star import lrtastar
from search_methods.beam_search import beam_search
from search_methods.heuristics import (
    manhattan_heuristic,
    hungarian_player_and_boxes_heuristic,
    bfs_static_heuristic,
    greedy_matching_heuristic,
    bfs_heuristic,
    advanced_heuristic,
    bfs_hungarian_heuristic,
    build_target_distance_map,
    box_to_goal_heuristic,
    misplaced_boxes_heuristic
)

class Solver:

    def __init__(self, map: Map) -> None:
        self.map = map

    def solve(self,algorithm):
        print(f"Incep rezolvarea pentru mapa {self.map.test_name}")
        #print(self.map)
        if algorithm == "lrta":
            path, learned = lrtastar(self.map, manhattan_heuristic, max_steps=1000000)
            #print(f"{learned} stări {len(path)} pași.")
            #print(f"{self.map.undo_moves}")
            final_state = path[-1]
            print(f"Număr pull-uri: {final_state.undo_moves}")
        else:
            path, num_States = beam_search(self.map, K=30, heuristic=manhattan_heuristic)
            #print(f"{len(path)} pași.")
            #print(f"{num_States} stari.")
            final_state = path[-1]
            #print(f"Număr pull-uri: {final_state.undo_moves}")
        self.map = path[-1].copy()
        return path
