"""
Lambda Calculus 解譯器（有名稱版本 Named Lambda Calculus）
功能特色：
1. 完整 AST 結構（變數 Var、抽象 Abs、應用 App）
2. 支援語法字串解析（Parser，支援 '\' 或 'λ'，多變數簡寫如 \x y. x）
3. 避免變數捕捉（Capture-avoiding substitution）與自動 α-轉換（α-conversion）
4. 採用正規序化簡（Normal Order Reduction，最左外側優先），可求得正規形式（Normal Form）
5. 完整顯示每一步化簡與代換過程（Step-by-step β-reduction trace）
6. 內建布林運算、邱奇數、柯里化等經典測試程式
"""

import re

# ==========================================
# 1. AST 節點定義
# ==========================================

class Expr:
    pass

class Var(Expr):
    """變數 (Variable)"""
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return self.name

    def __eq__(self, other):
        return isinstance(other, Var) and self.name == other.name


class Abs(Expr):
    """抽象函數 (Abstraction: λparam. body)"""
    def __init__(self, param, body):
        self.param = param
        self.body = body

    def __repr__(self):
        return f"(λ{self.param}. {self.body})"

    def __eq__(self, other):
        return isinstance(other, Abs) and self.param == other.param and self.body == other.body


class App(Expr):
    """函數應用 (Application: (func arg))"""
    def __init__(self, func, arg):
        self.func = func
        self.arg = arg

    def __repr__(self):
        f_str = str(self.func)
        a_str = str(self.arg)
        if isinstance(self.arg, App):
            a_str = f"({a_str})"
        return f"({f_str} {a_str})"

    def __eq__(self, other):
        return isinstance(other, App) and self.func == other.func and self.arg == other.arg


# ==========================================
# 2. 自由變數與避免變數捕捉的代換運算
# ==========================================

def free_vars(expr):
    """求出表示式中的所有自由變數 (Free Variables)"""
    if isinstance(expr, Var):
        return {expr.name}
    elif isinstance(expr, Abs):
        return free_vars(expr.body) - {expr.param}
    elif isinstance(expr, App):
        return free_vars(expr.func) | free_vars(expr.arg)
    return set()


_fresh_counter = 0

def fresh_var(base, forbidden):
    """生成不在 forbidden 集合內的新變數名稱（用於 α-conversion）"""
    global _fresh_counter
    candidate = base
    while candidate in forbidden:
        _fresh_counter += 1
        candidate = f"{base}{_fresh_counter}"
    return candidate


def substitute(expr, var, replacement):
    """
    避免變數捕捉代換: expr[var := replacement]
    若發生變數捕捉衝突，自動執行 α-conversion 重新命名被綁定變數
    """
    if isinstance(expr, Var):
        return replacement if expr.name == var else expr

    elif isinstance(expr, App):
        return App(
            substitute(expr.func, var, replacement),
            substitute(expr.arg, var, replacement)
        )

    elif isinstance(expr, Abs):
        if expr.param == var:
            return expr
        
        repl_fv = free_vars(replacement)
        if expr.param in repl_fv:
            # 發生變數捕捉衝突，進行 α-轉換
            forbidden = repl_fv | free_vars(expr.body) | {var}
            new_param = fresh_var(expr.param[0], forbidden)
            new_body = substitute(expr.body, expr.param, Var(new_param))
            return Abs(new_param, substitute(new_body, var, replacement))
        else:
            return Abs(expr.param, substitute(expr.body, var, replacement))

    return expr


# ==========================================
# 3. 詞法分析與語法解析器 (Lexer & Parser)
# ==========================================

def tokenize(s):
    token_spec = r'(λ|\\|\.|\(|\)|[a-zA-Z0-9_]+)'
    return [t for t in re.findall(token_spec, s) if t.strip()]


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self, expected=None):
        tok = self.peek()
        if expected and tok != expected:
            raise SyntaxError(f"預期符號 '{expected}', 但取得 '{tok}'")
        self.pos += 1
        return tok

    def parse_expr(self):
        expr = self.parse_atom()
        while self.peek() and self.peek() not in [')', None]:
            arg = self.parse_atom()
            expr = App(expr, arg)
        return expr

    def parse_atom(self):
        tok = self.peek()
        if tok in ['\\', 'λ']:
            self.consume()
            params = []
            while self.peek() and self.peek() != '.':
                params.append(self.consume())
            self.consume('.')
            body = self.parse_expr()
            for p in reversed(params):
                body = Abs(p, body)
            return body
        elif tok == '(':
            self.consume('(')
            expr = self.parse_expr()
            self.consume(')')
            return expr
        elif tok and tok.isidentifier():
            return Var(self.consume())
        else:
            raise SyntaxError(f"無效 Token: '{tok}'")


def parse(s):
    tokens = tokenize(s)
    parser = Parser(tokens)
    res = parser.parse_expr()
    if parser.pos != len(tokens):
        raise SyntaxError(f"未解析完畢的多餘字符: {tokens[parser.pos:]}")
    return res


# ==========================================
# 4. 正規序逐步化簡 (Normal Order Reduction)
# ==========================================

def step_normal_order(expr):
    """
    執行單一步驟的最左外側化簡（Normal Order β-reduction）。
    回傳值：(化簡後的新表示式, 步驟說明)；若已無法化簡則回傳 (None, None)。
    """
    if isinstance(expr, Var):
        return None, None

    if isinstance(expr, Abs):
        new_body, desc = step_normal_order(expr.body)
        if new_body is not None:
            return Abs(expr.param, new_body), desc
        return None, None

    if isinstance(expr, App):
        # 1. 最左外側 Redex: 若 func 為抽象，立即執行 β-reduction
        if isinstance(expr.func, Abs):
            reduced = substitute(expr.func.body, expr.func.param, expr.arg)
            desc = f"β-規約: (λ{expr.func.param}. ...) 作用於引數 {expr.arg}  ==>  代換 [{expr.func.param} ↦ {expr.arg}]"
            return reduced, desc

        # 2. 嘗試化簡左側 func
        new_func, desc = step_normal_order(expr.func)
        if new_func is not None:
            return App(new_func, expr.arg), desc

        # 3. 嘗試化簡右側 arg
        new_arg, desc = step_normal_order(expr.arg)
        if new_arg is not None:
            return App(expr.func, new_arg), desc

    return None, None


def evaluate(expr_or_str, max_steps=50):
    """
    對表示式進行完整的逐步求值，並列印每一步驟的計算過程
    """
    expr = parse(expr_or_str) if isinstance(expr_or_str, str) else expr_or_str
    print(f"\n[開始計算] 初始表示式: {expr}")
    
    cur = expr
    step = 0
    while step < max_steps:
        next_expr, desc = step_normal_order(cur)
        if next_expr is None:
            print(f"步驟 {step}: {cur}  ✓ [已達到正規形式 (Normal Form)]")
            return cur
        print(f"步驟 {step}: {cur}")
        print(f"  └── {desc}")
        cur = next_expr
        step += 1

    print(f"達到最大步數限制 ({max_steps})，可能為發散循環 (如 Ω 組合子)。")
    return cur


# ==========================================
# 5. 測試程式與運算展示
# ==========================================

if __name__ == '__main__':
    print("=" * 60)
    print("Lambda Calculus 解譯器 - 完整計算過程展示")
    print("=" * 60)

    # 範例 1：基本柯里化取首項: (λx. λy. x) a b
    print("\n【範例 1】基本應用: (λx. λy. x) a b")
    evaluate("(\\x. \\y. x) a b")

    # 範例 2：布林邏輯運算 AND TRUE FALSE
    # 定義: TRUE = \x.\y.x, FALSE = \x.\y.y, AND = \p.\q.p q p
    print("\n【範例 2】布林運算: AND TRUE FALSE")
    evaluate("(\\p. \\q. p q p) (\\x. \\y. x) (\\x. \\y. y)")

    # 範例 3：邱奇數後繼數計算: SUCC ZERO -> ONE
    # 定義: ZERO = \f.\x.x, SUCC = \n.\f.\x.f (n f x)
    print("\n【範例 3】邱奇數運算: SUCC ZERO -> ONE")
    evaluate("(\\n. \\f. \\x. f (n f x)) (\\f. \\x. x)")

    # 範例 4：避免變數捕捉測試 (α-conversion)
    print("\n【範例 4】變數衝突與 α-轉換: (λx. λy. x y) y")
    evaluate("(\\x. \\y. x y) y")
