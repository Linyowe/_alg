"""
題目 4：NPC 搜尋玩家問題（A* 啟發式搜尋演算法）
原理：
- 在遊戲開發（Game AI）中，非玩家角色（NPC）必須能繞過地圖障礙物，智慧追蹤玩家（Player）。
- 採用 A* 演算法（A-star Algorithm），結合 Dijkstra 的最短路徑保證與貪婪最佳優先搜尋的高效導引。
- 評估函數：f(n) = g(n) + h(n)
  1. g(n)：從 NPC 起點移動到目前格子 n 的實際步數成本。
  2. h(n)：從格子 n 到玩家目標位置的啟發式預估成本，網格四方向移動採用「曼哈頓距離」：
     h(n) = |r_n - r_player| + |c_n - c_player|
     因曼哈頓距離具備可容許性（Admissible，永不高估真實距離），保證能找到最佳最短路徑。
- 使用 Min-Heap（優先佇列 heapq）每次優先展開 f(n) 最小的節點，大幅減少盲目探索。
"""

import heapq

def solve_npc_astar(grid, start, goal):
    """
    A* 演算法求解 NPC 追蹤玩家的最短路徑
    grid: 0 代表平地通路，1 代表建築/障礙物
    start: NPC 當前座標 (r, c)
    goal: 玩家目標座標 (r, c)
    """
    rows, cols = len(grid), len(grid[0])

    def heuristic(a, b):
        # 曼哈頓距離
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    # 優先佇列項目: (f_score, g_score, (r, c))
    open_heap = []
    heapq.heappush(open_heap, (heuristic(start, goal), 0, start))

    g_score = {start: 0}
    came_from = {}
    expanded_nodes = 0

    while open_heap:
        current_f, current_g, current = heapq.heappop(open_heap)
        expanded_nodes += 1

        # 抵達玩家位置
        if current == goal:
            path = []
            curr = goal
            while curr in came_from:
                path.append(curr)
                curr = came_from[curr]
            path.append(start)
            path.reverse()
            return path, current_g, expanded_nodes

        r, c = current
        # 上、下、左、右四方向探索
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            neighbor = (nr, nc)

            # 確認在邊界內且非障礙物
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 0:
                tentative_g = current_g + 1
                if tentative_g < g_score.get(neighbor, float('inf')):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    heapq.heappush(open_heap, (f, tentative_g, neighbor))

    return None, float('inf'), expanded_nodes


def print_game_map(grid, path, start, goal):
    """遊戲地圖視覺化輸出 (N: NPC, P: 玩家, *: 追蹤路徑, #: 障礙物, .: 平地)"""
    rows, cols = len(grid), len(grid[0])
    path_set = set(path) if path else set()

    print("遊戲地圖路徑可視化：")
    for r in range(rows):
        line = []
        for c in range(cols):
            if (r, c) == start:
                line.append(" N ")
            elif (r, c) == goal:
                line.append(" P ")
            elif (r, c) in path_set:
                line.append(" * ")
            elif grid[r][c] == 1:
                line.append(" # ")
            else:
                line.append(" . ")
        print("".join(line))


if __name__ == '__main__':
    # 0: 可行走平地, 1: 建築物/障礙物
    game_map = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 1, 1, 1, 1, 0, 1, 0],
        [0, 0, 0, 0, 1, 0, 1, 0],
        [0, 1, 1, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0, 0, 0]
    ]
    npc_start = (0, 0)      # NPC 位於左上角
    player_target = (5, 7)  # 玩家位於右下角

    print("--- 4. NPC 搜尋玩家問題 (A* 演算法) ---")
    path, cost, exp_count = solve_npc_astar(game_map, npc_start, player_target)

    if path:
        print(f"成功規劃出追蹤路徑！最少移動代價: {cost} 步 (共展開 {exp_count} 個節點)")
        print("路徑節點:", " -> ".join(str(p) for p in path))
        print()
        print_game_map(game_map, path, npc_start, player_target)
    else:
        print("路徑被障礙物完全阻擋，無法抵達玩家身邊！")
