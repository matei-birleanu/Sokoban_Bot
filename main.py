from sokoban import (
	Box,
	DOWN,
	Map,
	Player
)
import os, time
import glob
from search_methods.solver import Solver
from sokoban.gif import *
import argparse
all_tests = [
    'tests/easy_map1.yaml', 'tests/easy_map2.yaml', 'tests/medium_map1.yaml', 'tests/medium_map2.yaml',
    'tests/hard_map1.yaml', 'tests/hard_map2.yaml', 'tests/large_map1.yaml', 'tests/large_map2.yaml',
    'tests/super_hard_map1.yaml'
]
def run_all_tests(all_tests, algorithm='beam'):
    for map_path in all_tests:
        #print(f"Running test for map: {map_path}")
        start_time = time.time()  # Începem măsurarea timpului

        try:
            map_obj = Map.from_yaml(map_path)
            solver = Solver(map_obj)
            path = solver.solve(algorithm=algorithm)
            end_time = time.time()  # Terminăm măsurarea timpului
            elapsed_time = end_time - start_time

            # Verificăm dacă harta a fost rezolvată
            final_map = solver.map
            is_solved = final_map.is_solved()

            #print(f"TIMP pentru {map_path}: {elapsed_time:.2f} secunde")
            #print(f"Succes: {'Da' if is_solved else 'Nu'}")
        except Exception as e:
            print(f"Eroare la rularea testului pentru {map_path}: {e}")
        #print("-" * 40)
def clear_old_images(folder: str):
	for file in glob.glob(os.path.join(folder, "*.png")):
		os.remove(file)

if __name__ == '__main__':
    #run_all_tests(all_tests)
    
    parser = argparse.ArgumentParser()
    parser.add_argument(
        'maps',
        nargs='+',
    )
    parser.add_argument(
        '-a', '--algorithm',
        choices=['lrta', 'beam'],
        default='beam',
    )
    args = parser.parse_args()

    for map_path in args.maps:
        start_time = time.time()
        map_obj = Map.from_yaml(map_path)
        solver = Solver(map_obj)
        path = solver.solve(algorithm=args.algorithm)
        map_name = map_path[6:]
        states = []
        states.append(map_obj.copy())
        for move in path:
            states.append(move)
        output_dir = f"images/steps/{map_name}_{args.algorithm}_steps"
        #clear_old_images(output_dir)

        save_images(states, output_dir)
        gif_name = f"{map_name}_{args.algorithm}.gif"
        create_gif(output_dir, gif_name,output_dir)

        final_map = solver.map
        end_time = time.time()
        elapsed_time = end_time - start_time
        #print(f"TIMP {elapsed_time}")
        #print(final_map.undo_moves)
        #print(final_map)
        print(f"Is solved: {final_map.is_solved()}")
        print("Neighbours of final state:")
        for neighbour in final_map.get_neighbours():
           print(neighbour)
