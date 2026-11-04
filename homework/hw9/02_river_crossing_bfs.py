"""
題目 2：狼羊甘藍菜過河問題（廣度優先搜尋 BFS）
原理：
- 狀態表示：四元組 (農夫, 狼, 羊, 甘藍菜)，0 代表在左岸，1 代表在右岸。
- 安全規則限制：
  1. 農夫不在場時，狼與羊不能同岸（狼會吃羊）。
  2. 農夫不在場時，羊與甘藍菜不能同岸（羊會吃甘藍菜）。
- 動作空間：農夫每次必須搭船，可選擇「獨自一人」或「攜帶同岸的一件物品」過河。
- 演算法採用廣度優先搜尋（BFS）：
  使用 FIFO 佇列（Queue）由淺入深層序展開狀態圖，
  最先抵達目標狀態 (1, 1, 1, 1) 時，保證為「最少過河次數（最短路徑）」。
"""

from collections import deque

def is_safe(state):
    """檢查當前狀態是否安全（無動物或菜被吃）"""
    f, w, g, c = state
    # 農夫不在場時，狼吃羊
    if f != w and w == g:
        return False
    # 農夫不在場時，羊吃甘藍菜
    if f != g and g == c:
        return False
    return True


def state_to_str(state):
    """格式化印出左岸與右岸成員清單"""
    names = ["農夫", "狼", "羊", "甘藍菜"]
    left = [names[i] for i, pos in enumerate(state) if pos == 0]
    right = [names[i] for i, pos in enumerate(state) if pos == 1]
    return f"左岸: {left} | 右岸: {right}"


def solve_river_crossing_bfs():
    start = (0, 0, 0, 0)  # 全員在左岸
    goal = (1, 1, 1, 1)   # 全員抵達右岸

    # Queue 元素結構: (當前狀態, 走過狀態路徑, 動作名稱記錄)
    queue = deque([(start, [start], ["初始狀態：全員在左岸"])])
    visited = {start}

    while queue:
        current, path, actions = queue.popleft()
        if current == goal:
            return path, actions

        f, w, g, c = current
        next_f = 1 - f

        # 農夫的可能動作
        candidates = [
            ((next_f, w, g, c), "農夫【獨自】過河"),
        ]
        if w == f:
            candidates.append(((next_f, next_f, g, c), "農夫帶【狼】過河"))
        if g == f:
            candidates.append(((next_f, w, next_f, c), "農夫帶【羊】過河"))
        if c == f:
            candidates.append(((next_f, w, g, next_f), "農夫帶【甘藍菜】過河"))

        for next_state, act_name in candidates:
            if is_safe(next_state) and next_state not in visited:
                visited.add(next_state)
                queue.append((next_state, path + [next_state], actions + [act_name]))

    return None, None


if __name__ == '__main__':
    print("--- 2. 狼羊甘藍菜過河問題 (BFS 最短路徑求解) ---")
    path, actions = solve_river_crossing_bfs()

    if path:
        print(f"成功找到最佳解！最少過河次數共 {len(actions) - 1} 步：\n")
        for step_idx in range(len(actions)):
            print(f"步驟 {step_idx}: {actions[step_idx]}")
            print(f"        當前格局 => {state_to_str(path[step_idx])}")
    else:
        print("未找到安全過河路徑！")
