import random
from tsp_common import N, tour_length, format_tour, get_random_tour

def solve_tsp_hill_climbing(init_tour, max_iter=5000, seed=42):
    rnd = random.Random(seed)
    tour = list(init_tour)
    cur_len = tour_length(tour)

    for _ in range(max_iter):
        i, j = sorted(rnd.sample(range(N), 2))
        neighbor = list(tour)
        neighbor[i : j + 1] = reversed(neighbor[i : j + 1])
        new_len = tour_length(neighbor)
        if new_len < cur_len:
            tour = neighbor
            cur_len = new_len

    return tour, cur_len

if __name__ == '__main__':
    initial = get_random_tour(seed=42)
    print("--- 2. 爬山演算法 (Hill Climbing) ---")
    print(f"初始長度: {tour_length(initial):.4f}")
    best_tour, best_len = solve_tsp_hill_climbing(initial, max_iter=5000)
    print(f"優化後長度: {best_len:.4f}")
    print(f"路徑: {format_tour(best_tour)}")
