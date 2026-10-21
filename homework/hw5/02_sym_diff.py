"""
題目 2：符號數學式微分（遞迴解決 sym_diff）
"""

def sym_diff(expr, var='x'):
    """
    遞迴求解表示式 expr 對變數 var 的微分。
    表達式格式 (S-expression):
      - 常數: int, float (如 5)
      - 變數: str (如 'x', 'y')
      - 二元運算: (op, u, v)，op 支援 '+', '-', '*', '/', '^'
      - 一元函數: (fn, u)，fn 支援 'sin', 'cos', 'ln'
    """
    # 1. 常數法則: d/dx(c) = 0
    if isinstance(expr, (int, float)):
        return 0

    # 2. 變數法則: d/dx(x) = 1, d/dx(y) = 0
    if isinstance(expr, str):
        return 1 if expr == var else 0

    if isinstance(expr, (tuple, list)):
        # 一元函數
        if len(expr) == 2:
            fn, u = expr
            du = sym_diff(u, var)
            if fn == 'sin': return simplify(('*', ('cos', u), du))
            if fn == 'cos': return simplify(('*', ('-', 0, ('sin', u)), du))
            if fn == 'ln':  return simplify(('/', du, u))

        # 二元運算
        if len(expr) == 3:
            op, u, v = expr
            du = sym_diff(u, var)
            dv = sym_diff(v, var)

            # 和差法則: (u ± v)' = u' ± v'
            if op == '+': return simplify(('+', du, dv))
            if op == '-': return simplify(('-', du, dv))

            # 乘法法則 (Product Rule): (u * v)' = u'v + uv'
            if op == '*':
                return simplify(('+', ('*', du, v), ('*', u, dv)))

            # 商法則 (Quotient Rule): (u / v)' = (u'v - uv') / v^2
            if op == '/':
                return simplify(('/', ('-', ('*', du, v), ('*', u, dv)), ('^', v, 2)))

            # 冪法則 (Power Rule): (u ^ c)' = c * u^(c-1) * u'
            if op == '^':
                if isinstance(v, (int, float)):
                    return simplify(('*', ('*', v, ('^', u, v - 1)), du))

    raise ValueError(f"不支援的表示式格式: {expr}")


def simplify(expr):
    """簡化符號表示式（常數折疊、消除 0 與 1 乘加）"""
    if not isinstance(expr, (tuple, list)):
        return expr
    if len(expr) == 2:
        return (expr[0], simplify(expr[1]))

    op, u, v = expr[0], simplify(expr[1]), simplify(expr[2])

    # 兩運算元皆為數字則常數折疊
    if isinstance(u, (int, float)) and isinstance(v, (int, float)):
        if op == '+': return u + v
        if op == '-': return u - v
        if op == '*': return u * v
        if op == '^': return u ** v

    if op == '+':
        if u == 0: return v
        if v == 0: return u
    elif op == '-':
        if v == 0: return u
        if u == v: return 0
    elif op == '*':
        if u == 0 or v == 0: return 0
        if u == 1: return v
        if v == 1: return u
    elif op == '^':
        if v == 0: return 1
        if v == 1: return u

    return (op, u, v)


def expr_to_str(expr):
    """格式化輸出為易讀的算式字串"""
    if not isinstance(expr, (tuple, list)):
        return str(expr)
    if len(expr) == 2:
        return f"{expr[0]}({expr_to_str(expr[1])})"
    op, u, v = expr
    return f"({expr_to_str(u)} {op} {expr_to_str(v)})"


if __name__ == '__main__':
    print("--- 符號微積分測試 ---")
    test_cases = [
        ('^', 'x', 3),                                            # x^3
        ('-', ('+', ('*', 3, ('^', 'x', 2)), ('*', 5, 'x')), 7),  # 3x^2 + 5x - 7
        ('*', ('sin', 'x'), ('^', 'x', 2)),                      # sin(x) * x^2
    ]
    for expr in test_cases:
        d = sym_diff(expr)
        print(f"d/dx {expr_to_str(expr)} = {expr_to_str(d)}")
