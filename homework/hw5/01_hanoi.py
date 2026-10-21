"""
題目 1：河內塔問題（分別用遞迴與禁止遞迴兩種方式實作）
"""

def hanoi_recursive(n, source='A', target='C', auxiliary='B'):
    """遞迴解法：將 n 個盤子從 source 移到 target"""
    if n == 1:
        return [(source, target)]
    moves = []
    # 1. 將前 n-1 個盤子移到輔助柱
    moves.extend(hanoi_recursive(n - 1, source, auxiliary, target))
    # 2. 將最大盤移到目標柱
    moves.append((source, target))
    # 3. 將前 n-1 個盤子從輔助柱移到目標柱
    moves.extend(hanoi_recursive(n - 1, auxiliary, target, source))
    return moves


def hanoi_iterative(n, source='A', target='C', auxiliary='B'):
    """禁止遞迴解法：利用週期性合法移動規律（總步數 2^n - 1）"""
    total_moves = (1 << n) - 1
    # 依盤數奇偶性決定柱子輪轉順序
    pegs = [source, target, auxiliary] if n % 2 != 0 else [source, auxiliary, target]
    state = {source: list(range(n, 0, -1)), auxiliary: [], target: []}
    pairs = [(source, pegs[1]), (source, pegs[2]), (pegs[1], pegs[2])]
    moves = []

    for i in range(1, total_moves + 1):
        p1, p2 = pairs[(i - 1) % 3]
        top1 = state[p1][-1] if state[p1] else float('inf')
        top2 = state[p2][-1] if state[p2] else float('inf')
        
        # 在兩根柱子之間進行唯一合法的移動
        if top1 < top2:
            disk = state[p1].pop()
            state[p2].append(disk)
            moves.append((p1, p2))
        else:
            disk = state[p2].pop()
            state[p1].append(disk)
            moves.append((p2, p1))
    return moves


if __name__ == '__main__':
    n = 3
    rec_moves = hanoi_recursive(n)
    itr_moves = hanoi_iterative(n)
    print(f"--- 河內塔 (n={n}) ---")
    print(f"遞迴解法步數: {len(rec_moves)}")
    print(f"非遞迴解法步數: {len(itr_moves)}")
    print("兩者路徑一致性:", rec_moves == itr_moves)
    for idx, (src, dst) in enumerate(rec_moves, 1):
        print(f"步驟 {idx}: {src} -> {dst}")
