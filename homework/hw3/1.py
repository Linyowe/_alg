import itertools

def solve_sat(variables, clauses):
    """
    使用真值表列舉法求解 SAT 問題
    :param variables: 變數名稱列表，例如 ['A', 'B', 'C']
    :param clauses: 子句函數列表，每個函數接受一個字典並回傳布林值
    """
    n = len(variables)
    # 產生 2^n 種 True/False 組合
    for values in itertools.product([False, True], repeat=n):
        assignment = dict(zip(variables, values))
        
        # 檢查是否所有子句皆為 True（即 AND 關係）
        if all(clause(assignment) for clause in clauses):
            return True, assignment
            
    return False, None

# 範例：求解 (A OR B) AND (NOT A OR C)
variables = ['A', 'B', 'C']
clauses = [
    lambda assign: assign['A'] or assign['B'],
    lambda assign: (not assign['A']) or assign['C']
]

satisfiable, solution = solve_sat(variables, clauses)
if satisfiable:
    print(f"找到可滿足解 (SAT)：{solution}")
else:
    print("不可滿足 (UNSAT)")
