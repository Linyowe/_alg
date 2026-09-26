import time

# ==================== 方法定義 ====================

# 方法 1：直接使用運算子
def power2n_1(n):
    return 2**n

# 方法 2a：用遞迴 (指數級別的呼叫樹 O(2^n))
def power2n_2a(n):
    if n == 0:
        return 1
    return power2n_2a(n - 1) + power2n_2a(n - 1)

# 方法 2b：用遞迴 (線性遞迴 O(n))
def power2n_2b(n):
    if n == 0:
        return 1
    return 2 * power2n_2b(n - 1)

# 方法 3：用遞迴 + 查表 (Memoization / 記憶化搜尋)
memo = {0: 1}
def power2n_3(n):
    # 1. 檢查是否已經查過表
    if n in memo:
        return memo[n]
    
    # 2. 若不在表中，利用遞迴計算並存入查表字典
    memo[n] = power2n_3(n - 1) + power2n_3(n - 1)
    
    # 3. 回傳結果
    return memo[n]


# ==================== 主程式測試 ====================
if __name__ == "__main__":
    n = 100
    print(f"========================================")
    print(f" 開始執行 $n = {n}$ 的效能測試")
    print(f"========================================\n")
    
    # ---------------- 測試方法 1 ----------------
    start = time.perf_counter()
    res1 = power2n_1(n)
    end = time.perf_counter()
    print(f"[方法 1] 內建運算子 (2**n):")
    print(f"  - 結果 = {res1}")
    print(f"  - 耗時 = {end - start:.8f} 秒\n")

    # ---------------- 測試方法 2a ----------------
    print(f"[方法 2a] 二元遞迴 (power2n(n-1) + power2n(n-1)):")
    print(f"  - 狀態：【略過執行】")
    print(f"  - 原因：當 n = 100 時，其時間複雜度為 O(2^100)，")
    print(f"           呼叫次數呈天文數字成長，會導致電腦 CPU 滿載並無限卡死。\n")
    # 若你想親自體驗卡死，可以取消下方註解：
    # start = time.perf_counter()
    # res2a = power2n_2a(n)
    # end = time.perf_counter()
    # print(f"  - 耗時 = {end - start:.8f} 秒\n")

    # ---------------- 測試方法 2b ----------------
    start = time.perf_counter()
    res2b = power2n_2b(n)
    end = time.perf_counter()
    print(f"[方法 2b] 線性遞迴 (2 * power2n(n-1)):")
    print(f"  - 結果 = {res2b}")
    print(f"  - 耗時 = {end - start:.8f} 秒\n")

    # ---------------- 測試方法 3 ----------------
    start = time.perf_counter()
    res3 = power2n_3(n)
    end = time.perf_counter()
    print(f"[方法 3] 遞迴 + 查表 (Memoization):")
    print(f"  - 結果 = {res3}")
    print(f"  - 耗時 = {end - start:.8f} 秒\n")

    print(f"========================================")
    print(f" 測試完畢！")
    print(f"========================================")
