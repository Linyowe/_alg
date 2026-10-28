from tsp_common import N, DIST_MATRIX, tour_length, format_tour, get_random_tour

def solve_tsp_improvement(init_tour):
    tour = list(init_tour)
    improved = True
    iterations = 0

    while improved:
        improved = False
        iterations += 1
        for i in range(N):
            for j in range(i + 2, N if i > 0 else N - 1):
                a, b = tour[i], tour[(i + 1) % N]
                c, d = tour[j], tour[(j + 1) % N]
                delta = (DIST_MATRIX[a][c] + DIST_MATRIX[b][d]) - (DIST_MATRIX[a][b] + DIST_MATRIX[c][d])
                if delta < -1e-9:
                    tour[i + 1 : j + 1] = reversed(tour[i + 1 : j + 1])
                    improved = True
                    break
            if improved:
                break
    return tour, tour_length(tour), iterations

if __name__ == '__main__':
    initial = get_random_tour(seed=42)
    print("--- 1. 改良法 (2-Opt Improvement) ---")
    print(f"初始長度: {tour_length(initial):.4f}")
    best_tour, best_len, iters = solve_tsp_improvement(initial)
    print(f"優化後長度: {best_len:.4f} (歷經 {iters} 輪掃描)")
    print(f"路徑: {format_tour(best_tour)}")
