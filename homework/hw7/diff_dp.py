def diff_lcs_dp(a, b):
    """基於動態規劃 (LCS) 的文字差異比對演算法"""
    n, m = len(a), len(b)
    # 建立二維 DP 表格
    dp = [[0] * (m + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if a[i - 1] == b[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # 從右下角回溯路徑
    i, j = n, m
    diff = []
    while i > 0 or j > 0:
        if i > 0 and j > 0 and a[i - 1] == b[j - 1]:
            diff.append((' ', a[i - 1]))
            i -= 1
            j -= 1
        elif j > 0 and (i == 0 or dp[i][j - 1] >= dp[i - 1][j]):
            diff.append(('+', b[j - 1]))
            j -= 1
        elif i > 0 and (j == 0 or dp[i][j - 1] < dp[i - 1][j]):
            diff.append(('-', a[i - 1]))
            i -= 1

    diff.reverse()
    return diff


if __name__ == '__main__':
    doc_a = ["import math", "x = 10", "print(x)"]
    doc_b = ["import math", "x = 20", "y = 30", "print(x)"]
    for op, line in diff_lcs_dp(doc_a, doc_b):
        print(f"{op} {line}")
