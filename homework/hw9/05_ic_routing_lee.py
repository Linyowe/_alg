"""
題目 5：IC 設計中的電路繞線問題（Lee's Maze Routing 迷宮繞線演算法）
原理與背景：
- 在超大型積體電路（VLSI / IC）物理設計中，繞線（Routing）負責在晶片格點（Routing Grid）上
  將多個接腳（Pins / Terminals）以金屬導線連接，同時避開巨集障礙物（Obstacles）與已佈導線。
- 電路繞線常見方法概述：
  1. Lee 演算法（Lee's Algorithm / Maze Router）：基於廣度優先搜尋（BFS）的波前擴展（Wave Expansion），
     保證若存在連線，必能找到「最短導線長度」，為最經典的繞線基準演算法。
  2. Hadlock 演算法 / Soukup 演算法：結合定向探索與轉彎數最小化（Detour Number）加速展開。
  3. A* 迷宮繞線法：加入至目標 Pin 的曼哈頓啟發函數，大幅縮小波前展開面積。
  4. 拆線重繞（Rip-up and Reroute）：面對高繞線擁擠度（Congestion）與多條 Net 衝突時的順序調整機制。
- 本程式實作核心 Lee 演算法，並支援「多導線循序繞線（Sequential Multi-Net Routing）」，
  自動將已完成繞線的網路標記為後續導線的障礙，避免短路。
"""

from collections import deque

def route_single_net_lee(grid, source, target, net_id):
    """
    使用 Lee 演算法替單一網路 (Net) 尋找最短導線路徑
    grid 狀態: 0 代表空白可通行軌道, -1 代表既有障礙物, >0 代表已被佔用的 Net 導線
    """
    rows, cols = len(grid), len(grid[0])
    # 波前標記陣列：記錄從 Source 擴展至各格點的步數代價
    wave = [[-1] * cols for _ in range(rows)]
    queue = deque([source])
    wave[source[0]][source[1]] = 0

    # 階段 1：波前擴展 (Wave Expansion / BFS)
    found = False
    while queue:
        r, c = queue.popleft()
        if (r, c) == target:
            found = True
            break

        # 上、下、左、右四個鄰接繞線軌道
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                # 只有空軌道或目標 Pin 本身允許通過
                if (grid[nr][nc] == 0 or (nr, nc) == target) and wave[nr][nc] == -1:
                    wave[nr][nc] = wave[r][c] + 1
                    queue.append((nr, nc))

    if not found:
        return None  # 該 Net 被阻擋，無法連通

    # 階段 2：回溯路徑 (Backtracking)
    path = [target]
    curr = target
    while curr != source:
        r, c = curr
        dist = wave[r][c]
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and wave[nr][nc] == dist - 1:
                curr = (nr, nc)
                path.append(curr)
                break
    path.reverse()

    # 階段 3：佈線佔用 (Clearance / Mark Wire)
    # 將已鋪設的金屬線路標記為該 Net ID，後續導線不可穿越（防止電氣短路）
    for r, c in path:
        grid[r][c] = net_id

    return path


def print_chip_layout(grid, nets_info):
    """晶片繞線佈局可視化輸出"""
    rows, cols = len(grid), len(grid[0])
    print("晶片格點繞線分佈展示（#: 障礙物, .: 可用軌道, 數字: 對應 Net 導線）：")
    for r in range(rows):
        line = []
        for c in range(cols):
            val = grid[r][c]
            if val == -1:
                line.append(" # ")
            elif val == 0:
                line.append(" . ")
            else:
                line.append(f" {val} ")
        print("".join(line))


if __name__ == '__main__':
    # 0: 空導線軌道, -1: IC 晶片障礙物/巨集模組
    chip_grid = [
        [0,  0,  0,  0,  0,  0,  0,  0],
        [0, -1, -1, -1,  0, -1, -1,  0],
        [0, -1,  0,  0,  0,  0, -1,  0],
        [0, -1,  0, -1, -1,  0, -1,  0],
        [0,  0,  0,  0,  0,  0,  0,  0]
    ]

    # 定義待連接的引腳對 (名稱, Source Pin, Target Pin, Net ID)
    nets_to_route = [
        ("Net 1 (電源線)", (0, 0), (4, 7), 1),
        ("Net 2 (信號線)", (2, 2), (2, 5), 2)
    ]

    print("--- 5. IC 設計電路繞線問題 (Lee's Maze Routing) ---")
    for name, src, dst, nid in nets_to_route:
        wire_path = route_single_net_lee(chip_grid, src, dst, nid)
        if wire_path:
            print(f"[{name}] 繞線成功！導線長度: {len(wire_path)} 單位格")
            print(f"       佈線座標: {' -> '.join(str(p) for p in wire_path)}")
        else:
            print(f"[{name}] 繞線失敗：所有軌道均被阻擋！")

    print()
    print_chip_layout(chip_grid, nets_to_route)
