def newton_sqrt(target, tol=1e-7, max_iter=100):
    """
    使用牛頓迭代法求 sqrt(target)
    迭代公式: x_{n+1} = 0.5 * (x_n + target / x_n)
    """
    x = target / 2.0  # 初始猜測值
    print(f"=== 開始計算 sqrt({target}) 的牛頓迭代 ===")
    
    for i in range(max_iter):
        x_next = 0.5 * (x + target / x)
        print(f"第 {i+1} 次迭代: x = {x_next:.7f}")
        
        # 檢查是否達到收斂條件
        if abs(x_next - x) < tol:
            print(f"-> 在第 {i+1} 次迭代成功收斂！")
            return x_next
            
        x = x_next
        
    print("達到最大迭代次數，可能未完全收斂。")
    return x

if __name__ == "__main__":
    val = 5.0
    ans = newton_sqrt(val)
    print(f"最終計算結果: sqrt({val}) ≈ {ans:.7f}")
