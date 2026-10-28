# 演算法作業：第八週習題（旅行推銷員問題 TSP 五種最佳化解法）

本專案收錄金門大學演算法課程第七週作業題目實作，針對經典 NP-hard 組合最佳化問題——**旅行推銷員問題（Traveling Salesperson Problem, TSP）**，分別實作五種經典與啟發式最佳化演算法，探討其演算法機制、收斂特性與解品質差異。

---

## 專案目錄結構

建議於 GitHub 儲存庫建立如下之檔案結構：

```text
.
├── README.md                 # 專案說明文件（本文件）
├── tsp_common.py             # 城市座標資料、距離矩陣計算與共用輔助函式
├── 01_improvement.py         # 方法 1：改良法 (Iterative 2-Opt Improvement)
├── 02_hill_climbing.py       # 方法 2：爬山演算法 (Stochastic Hill Climbing)
├── 03_simulated_annealing.py # 方法 3：模擬退火法 (Simulated Annealing)
├── 04_gradient_descent.py    # 方法 4：梯度下降法 (離散最速下降 Steepest Descent)
└── 05_greedy.py              # 方法 5：貪婪演算法 (Nearest Neighbor 最近鄰居法)
