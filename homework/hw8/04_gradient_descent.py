from tsp_common import N, DIST_MATRIX, tour_length, format_tour, get_random_tour

def solve_tsp_gradient_descent(init_tour, max_steps=100):
    tour = list(init_tour)
    cur_len = tour_length(tour)

    for _ in range(max_steps):
        steepest_delta = 0
        best_move = None

        # 遍歷完整鄰域方向，尋找負梯度最大的最速下降步
        for i in range(N):
            for j in range(i + 2, N if i > 0 else N - 1):
                a, b = tour[i], tour[(i + 1) % N]
                c, d = tour[j], tour[(j + 1) % N]
                delta = (DIST_MATRIX[a][c] + DIST_MATRIX[b][d]) - (DIST_MATRIX[a][b] + DIST_MATRIX[c][d])
                if delta < steepest_delta:
                    steepest_delta = delta
                    best_move = (i, j)

        if best_move is None or steepest_delta >= -1e-9:
            break

        i, j = best_move
        tour[i + 1 : j + 1] = reversed(tour[i + 1 : j + 1])
        cur_len += steepest_delta

    return tour, cur_len

if __name__ == '__main__':
    initial = get_random_tour(seed=42)
    print("--- 4. 梯度下降法 (Steepest Descent) ---")
    print(f"初始長度: {tour_length(initial):.4f}")
    best_tour, best_len = solve_tsp_gradient_descent(initial)
    print(f"優化後長度: {best_len:.4f}")
    print(f"路徑: {format_tour(best_tour)}")
