from tsp_common import N, DIST_MATRIX, tour_length, format_tour

def solve_tsp_greedy(start_city=0):
    unvisited = set(range(N))
    current = start_city
    tour = [current]
    unvisited.remove(current)

    while unvisited:
        next_city = min(unvisited, key=lambda c: DIST_MATRIX[current][c])
        tour.append(next_city)
        unvisited.remove(next_city)
        current = next_city

    return tour, tour_length(tour)

if __name__ == '__main__':
    print("--- 5. 貪婪演算法 (Nearest Neighbor) ---")
    best_tour, best_len = solve_tsp_greedy(start_city=0)
    print(f"路徑總長度: {best_len:.4f}")
    print(f"路徑: {format_tour(best_tour)}")
