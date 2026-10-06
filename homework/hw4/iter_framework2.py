class IterativeFramework:
    def __init__(self, max_iter=1000, tol=1e-6):
        self.max_iter = max_iter
        self.tol = tol
        self.history = []

    def initialize(self, *args, **kwargs):
        """初始化狀態"""
        raise NotImplementedError("子類別必須實作 initialize 方法")

    def step(self):
        """執行單步迭代更新"""
        raise NotImplementedError("子類別必須實作 step 方法")

    def get_state(self):
        """取得目前狀態"""
        raise NotImplementedError("子類別必須實作 get_state 方法")

    def is_converged(self, prev_state, current_state):
        """檢查是否達到收斂條件"""
        raise NotImplementedError("子類別必須實作 is_converged 方法")

    def run(self, *args, **kwargs):
        """執行完整迭代迴圈"""
        self.initialize(*args, **kwargs)
        for i in range(self.max_iter):
            prev_state = self.get_state()
            self.step()
            current_state = self.get_state()
            self.history.append(current_state)
            
            if self.is_converged(prev_state, current_state):
                print(f"-> 迭代在第 {i+1} 次成功收斂！")
                return current_state
                
        print("-> 已達到最大迭代次數，結束迭代。")
        return self.get_state()


# 範例：使用此框架實作求平方根 (Newton's Method)
class SqrtSolver(IterativeFramework):
    def initialize(self, target):
        self.target = target
        self.x = target / 2.0  # 初始猜測值

    def step(self):
        # 牛頓迭代公式: x_{n+1} = 0.5 * (x + target / x)
        self.x = 0.5 * (self.x + self.target / self.x)

    def get_state(self):
        return self.x

    def is_converged(self, prev_state, current_state):
        return abs(current_state - prev_state) < self.tol


if __name__ == "__main__":
    solver = SqrtSolver(max_iter=100, tol=1e-7)
    result = solver.run(target=5.0)
    print(f"計算結果 sqrt(5.0) = {result:.7f}")
