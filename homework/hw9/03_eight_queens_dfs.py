"""
題目 3：八皇后問題（深度優先搜尋與回溯法 DFS & Backtracking）
原理：
- 在 8x8 的西洋棋盤上放置 8 個皇后，使其互不攻擊。
  任意兩個皇后不可處於同一行、同一列或同一對角線上。
- 狀態剪枝與回溯（DFS）：
  1. 由於每一行恰好只能放置一個皇后，以長度為 8 的陣列 board[row] = col 表示位置。
  2. 依序逐行 (row = 0 到 7) 遞迴向下嘗試放置皇后於某一列 (col = 0 到 7)。
  3. 放置前進行安全性剪枝檢驗：
     - 同列衝突：board[r] == col
     - 對角線衝突：abs(r - row) == abs(board[r] - col)
  4. 若當前列合法，則深入下一行 dfs(row + 1)；若無處可放則觸發回溯撤銷當前皇后。
  5. 當 row == 8 時，即找到一組合法解。八皇后共有 92 組標準解。
"""

def solve_n_queens(n=8):
    solutions = []
    board = [-1] * n  # board[row] 存放該行皇后的欄位 index

    def is_valid(row, col):
        """檢查在 (row, col) 放置皇后是否會與上方既有皇后衝突"""
        for r in range(row):
            c = board[r]
            # 同行 (由資料結構自然避免)、同列或同對角線檢查
            if c == col or abs(r - row) == abs(c - col):
                return False
        return True

    def dfs(row):
        # 8 行皆安全擺放完畢，記錄解答
        if row == n:
            solutions.append(list(board))
            return

        for col in range(n):
            if is_valid(row, col):
                board[row] = col      # 放置皇后
                dfs(row + 1)          # 遞迴深入下一行
                board[row] = -1       # 回溯復原

    dfs(0)
    return solutions


def print_board(solution):
    """格式化輸出西洋棋盤擺放結果 (Q: 皇后, .: 空格)"""
    n = len(solution)
    print("棋盤盤面展示：")
    header = "   " + " ".join(f"C{c}" for c in range(n))
    print(header)
    print("  +" + "--" * n + "-+")
    for r in range(n):
        row_str = [" Q" if c == solution[r] else " ." for c in range(n)]
        print(f"R{r}|" + "".join(row_str) + " |")
    print("  +" + "--" * n + "-+")


if __name__ == '__main__':
    print("--- 3. 八皇后問題 (DFS 回溯法求解) ---")
    solutions = solve_n_queens(8)
    print(f"搜尋完成！8 皇后問題共有 {len(solutions)} 組相異合法解。\n")

    # 展示第一組解
    print(f"【展示解法 #1 座標】(每列欄位 index): {solutions[0]}")
    print_board(solutions[0])
