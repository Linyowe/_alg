def diff_myers(a, b):
    """基於 Myers 演算法 (貪婪編輯圖 BFS) 的差異比對演算法"""
    n, m = len(a), len(b)
    max_d = n + m
    # v[k] 儲存對角線 k 上可抵達的最遠 x 座標
    v = {1: 0}
    trace = []

    for d in range(max_d + 1):
        trace.append(dict(v))
        for k in range(-d, d + 1, 2):
            # 判斷是從上方向下走 (新增)，還是從左方向右走 (刪除)
            if k == -d or (k != d and v.get(k - 1, -1) < v.get(k + 1, -1)):
                x = v.get(k + 1, -1)
            else:
                x = v.get(k - 1, -1) + 1
            y = x - k

            # 沿對角線免費貪婪滑行 (Snake)
            while x < n and y < m and a[x] == b[y]:
                x += 1
                y += 1
            v[k] = x

            # 抵達終點，提早結束並回溯
            if x >= n and y >= m:
                return _backtrack(trace, a, b, d, n, m)
    return []


def _backtrack(trace, a, b, d, n, m):
    x, y = n, m
    diff = []
    for d_step in range(d, 0, -1):
        v = trace[d_step]
        k = x - y
        if k == -d_step or (k != d_step and v.get(k - 1, -1) < v.get(k + 1, -1)):
            prev_k = k + 1
        else:
            prev_k = k - 1
        prev_x = v[prev_k]
        prev_y = prev_x - prev_k

        # 回溯對角線相同字元
        while x > prev_x and y > prev_y:
            diff.append((' ', a[x - 1]))
            x -= 1
            y -= 1

        # 回溯編輯動作
        if x == prev_x:
            diff.append(('+', b[y - 1]))
            y -= 1
        elif y == prev_y:
            diff.append(('-', a[x - 1]))
            x -= 1

    while x > 0 and y > 0:
        diff.append((' ', a[x - 1]))
        x -= 1
        y -= 1
    while x > 0:
        diff.append(('-', a[x - 1]))
        x -= 1
    while y > 0:
        diff.append(('+', b[y - 1]))
        y -= 1

    diff.reverse()
    return diff


if __name__ == '__main__':
    doc_a = ["import math", "x = 10", "print(x)"]
    doc_b = ["import math", "x = 20", "y = 30", "print(x)"]
    for op, line in diff_myers(doc_a, doc_b):
        print(f"{op} {line}")
