import pandas as pd
import matplotlib.pyplot as plt

maps = [
    'easy_map1', 'easy_map2', 'hard_map1', 'hard_map2',
    'large_map1', 'large_map2', 'medium_map1', 'medium_map2',
    'super_hard_map1'
]

data = {
    'manhattan': [92, 18, 2093, 611, 2802, 9300, 198, 4681, 568],
    'misplaced_boxes_heuristic': [1048, 578, 10632, 1420, 109649, 1000001, 18793, 24097, 652765],
    'box_to_goal_heuristic': [1016, 550, 803, 1783, 16530, 67152, 2359, 3716, 1604],
    'hungarian_player_and_boxes_heuristic': [340, 18, 679, 786, 1225, 99009, 206, 5564, 369],
    'bfs_static_heuristic': [214, 18, 308, 417, 921, 75685, 45, 8053, 1668],
    'greedy_matching_heuristic': [340, 18, 679, 1146, 1225, 93513, 206, 9037, 316],
    'bfs_heuristic': [210, 18, 308, 529, 887, 27427, 37, 10059, 1636],
    'advanced_heuristic': [210, 18, 308, 529, 887, 145831, 45, 5997, 2478],
    'bfs_hungarian_heuristic': [150, 18, 64, 1039, 1209, 143675, 45, 5997, 2478]
}

df = pd.DataFrame(data, index=maps)

plt.figure(figsize=(12, 6))
for alg in df.columns:
    plt.plot(df.index, df[alg], marker='o', label=alg)

plt.xlabel('Harta')
plt.ylabel('Numar de pasi')
plt.title('Compararea euristicilor dupa numarul de pasi')
plt.xticks(rotation=45, ha='right')
plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
plt.tight_layout()
plt.show()
