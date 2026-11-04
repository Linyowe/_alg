"""
題目 1：老鼠走迷宮問題（深度優先搜尋 DFS）
原理：
- 將迷宮建模為 2D 網格，0 代表通路，1 代表障礙物（牆壁）。
- 使用深度優先搜尋（DFS）與遞迴回溯（Backtracking）。
- 從起點 (start) 出發，優先沿著一個方向（上、下、左、右）探尋到底，
  若遭遇死胡同或障礙物則回溯（Backtrack），直到抵達終點 (end)。
- 紀錄已造訪格子避免無限循環，並在找到終點時輸出完整走訪路徑。
"""

def solve_maze_dfs(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    visited = [[False] * cols for _ in range(rows)]
    path = []

    def dfs(r, c):
        # 抵達終點
        if (r, c) == end:
            path.append((r, c))
            return True

        visited[r][c] = True
        path.append((r, c))

        # 探索相鄰四個方向：上、下、左、右
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if maze[nr][nc] == 0 and not visited[nr][nc]:
                    if dfs(nr, nc):
                        return True

        # 四方皆不通，回溯
        path.pop()
        return False

    if dfs(start[0], start[1]):
        return path
    return None


def print_maze_with_path(maze, path, start, end):
    """可視化印出迷宮與老鼠走過的路徑"""
    rows, cols = len(maze), len(maze[0])
    path_set = set(path) if path else set()

    print("迷宮可視化 (S: 起點, E: 終點, *: 走訪路徑, #: 牆壁, .: 通路)：")
    for r in range(rows):
        line = []
        for c in range(cols):
            if (r, c) == start:
                line.append(" S ")
            elif (r, c) == end:
                line.append(" E ")
            elif (r, c) in path_set:
                line.append(" * ")
            elif maze[r][c] == 1:
                line.append(" # ")
            else:
                line.append(" . ")
        print("".join(line))


if __name__ == '__main__':
    # 0: 可通行, 1: 障礙物牆壁
    maze = [
        [0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0],
        [0, 0, 0, 1, 0, 0],
        [1, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 0, 0]
    ]
    start = (0, 0)
    end = (4, 5)

    print("--- 1. 老鼠走迷宮 (DFS) ---")
    path = solve_maze_dfs(maze, start, end)

    if path:
        print(f"成功尋得路徑！步數共 {len(path) - 1} 步")
        print("走訪座標序列:", " -> ".join(str(p) for p in path))
        print()
        print_maze_with_path(maze, path, start, end)
    else:
        print("此迷宮無解，老鼠無法抵達終點！")
