import math
import random
from tsp_common import N, tour_length, format_tour, get_random_tour

def solve_tsp_simulated_annealing(init_tour, t_start=100.0, t_end=0.001, alpha=0.995, seed=42):
    rnd = random.Random(seed)
    tour = list(init_tour)
    cur_len = tour_length(tour)
    best_tour = list(tour)
    best_len = cur_len
    T = t_start

    while T > t_end:
        i, j = sorted(rnd.sample(range(N), 2))
        neighbor = list(tour)
        neighbor[i : j + 1] = reversed(neighbor[i : j + 1])
        new_len = tour_length(neighbor)
        delta = new_len - cur_len

        # Metropolis 準則
        if delta < 0 or rnd.random() < math.exp(-delta / T):
            tour = neighbor
            cur_len = new_len
            if cur_len < best_len:
                best_tour = list(tour)
                best_len = cur_len

        T *= alpha

    return best_tour, best_len

if __name__ == '__main__':
    initial = get_random_tour(seed=42)
    print("--- 3. 模擬退火法 (Simulated Annealing) ---")
    print(f"初始長度: {tour_length(initial):.4f}")
    best_tour, best_len = solve_tsp_simulated_annealing(initial)
    print(f"優化後長度: {best_len:.4f}")
    print(f"路徑: {format_tour(best_tour)}")
