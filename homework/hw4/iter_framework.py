class IterativeSolver:
    def __init__(self, max_iter=1000, tol=1e-6):
        self.max_iter = max_iter
        self.tol = tol
        self.history = []

    def initialize(self, *args, **kwargs):
        raise NotImplementedError

    def step(self):
        raise NotImplementedError

    def is_converged(self):
        raise NotImplementedError

    def run(self, *args, **kwargs):
        self.initialize(*args, **kwargs)
        for i in range(self.max_iter):
            prev_state = self.get_state()
            self.step()
            current_state = self.get_state()
            self.history.append(current_state)
            
            if self.is_converged():
                print(f"Converged at iteration {i+1}")
                break
        return self.get_state()
