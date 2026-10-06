import numpy as np

class HopfieldNetwork:
    def __init__(self, n_neurons):
        self.n_neurons = n_neurons
        self.weights = np.zeros((n_neurons, n_neurons))

    def train(self, patterns):
        """使用Hebbian學習規則訓練記憶圖樣 (patterns: 列表，包含 -1 與 1)"""
        n_patterns = len(patterns)
        for p in patterns:
            p = np.array(p)
            self.weights += np.outer(p, p)
        # 對角線設為 0，避免自我回饋
        np.fill_diagonal(self.weights, 0)
        self.weights /= n_patterns
        print(f"成功儲存 {n_patterns} 個記憶圖樣。")

    def recall(self, noisy_pattern, max_iter=10):
        """透過非同步迭代更新，讓受損記憶收斂回正確圖樣"""
        state = np.array(noisy_pattern)
        print("開始迭代記憶恢復過程...")
        
        for i in range(max_iter):
            prev_state = state.copy()
            # 依序對每個神經元進行非同步迭代更新
            for j in range(self.n_neurons):
                activation = np.dot(self.weights[j], state)
                state[j] = 1 if activation >= 0 else -1
                
            print(f"第 {i+1} 次迭代狀態: {state}")
            
            # 若狀態不再改變（達到能量極小值/收斂），則提早結束
            if np.array_equal(state, prev_state):
                print(f"-> 在第 {i+1} 次迭代達到能量穩定（收斂）！")
                break
                
        return state

if __name__ == "__main__":
    # 定義 2 個簡單的 4 位元記憶圖樣 (例如字母或標記)
    pattern1 = [1, 1, -1, -1]
    pattern2 = [-1, -1, 1, 1]
    
    # 1. 建立並訓練 Hopfield 網路
    hopfield = HopfieldNetwork(n_neurons=4)
    hopfield.train([pattern1, pattern2])
    
    # 2. 測試容錯能力：給入一個帶有噪聲的輸入 (例如 pattern1 受到干擾變成 [1, -1, -1, -1])
    noisy_input = [1, -1, -1, -1]
    print(f"\n原始受損輸入: {noisy_input}")
    
    # 3. 透過迭代恢復記憶
    recovered = hopfield.recall(noisy_input)
    print(f"最終恢復結果: {recovered.tolist()}")
    print(f"是否成功匹配 Pattern 1? {list(recovered) == pattern1}")
