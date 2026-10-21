"""
Lambda Calculus 經典程式測試集 (test_programs.py)
展示多種 Lambda Calculus 經典演算法的完整計算過程：
1. 布林邏輯運算：TRUE, FALSE, NOT, AND, OR, IF-THEN-ELSE
2. 邱奇數（Church Numerals）運算：ZERO, ONE, TWO, THREE, SUCC, ADD, MULT
3. 組合子（Combinators）：I, K, S 與 (S K K x ==> x) 恆等驗證
"""

from lambda_interpreter import evaluate

# 常用 Lambda 巨集定義表（字串形式）
MACROS = {
    # 組合子
    "I": r"\x. x",
    "K": r"\x. \y. x",
    "S": r"\x. \y. \z. x z (y z)",
    
    # 邱奇布林值 (Church Booleans)
    "TRUE": r"\x. \y. x",
    "FALSE": r"\x. \y. y",
    "NOT": r"\b. b (\x. \y. y) (\x. \y. x)",
    "AND": r"\p. \q. p q p",
    "OR": r"\p. \q. p p q",
    "IF": r"\cond. \then_expr. \else_expr. cond then_expr else_expr",
    
    # 邱奇數 (Church Numerals)
    "ZERO": r"\f. \x. x",
    "ONE": r"\f. \x. f x",
    "TWO": r"\f. \x. f (f x)",
    "THREE": r"\f. \x. f (f (f x))",
    "SUCC": r"\n. \f. \x. f (n f x)",
    "ADD": r"\m. \n. \f. \x. m f (n f x)",
    "MULT": r"\m. \n. \f. m (n f)"
}


def run_tests():
    print("=" * 65)
    print("【測試群組 1】布林邏輯條件式 IF-THEN-ELSE 與 NOT")
    print("=" * 65)

    # 1. IF TRUE apple banana  ==>  apple
    expr_if = f"({MACROS['IF']}) ({MACROS['TRUE']}) apple banana"
    print("\n測試算式: IF TRUE apple banana (預期輸出: apple)")
    evaluate(expr_if)

    # 2. NOT TRUE  ==>  FALSE (\x. \y. y)
    expr_not = f"({MACROS['NOT']}) ({MACROS['TRUE']})"
    print("\n測試算式: NOT TRUE (預期輸出: FALSE)")
    evaluate(expr_not)

    print("\n" + "=" * 65)
    print("【測試群組 2】邱奇數加法運算 (ADD ONE TWO)")
    print("=" * 65)

    # 3. ADD ONE TWO  ==>  THREE (\f. \x. f (f (f x)))
    expr_add = f"({MACROS['ADD']}) ({MACROS['ONE']}) ({MACROS['TWO']})"
    print("\n測試算式: ADD ONE TWO (預期輸出: 3 的邱奇數)")
    evaluate(expr_add)

    print("\n" + "=" * 65)
    print("【測試群組 3】組合子運算 (S K K x 等價於 I x)")
    print("=" * 65)

    # 4. S K K x  ==>  x
    expr_skk = f"({MACROS['S']}) ({MACROS['K']}) ({MACROS['K']}) result_symbol"
    print("\n測試算式: S K K result_symbol (預期輸出: result_symbol)")
    evaluate(expr_skk)


if __name__ == '__main__':
    run_tests()
