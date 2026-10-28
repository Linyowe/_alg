"""
TSP 基礎資料與距離矩陣共用模組 (tsp_common.py)
"""
import math
import random

# 12 個代表性城市座標 (名稱, 經度, 緯度)
CITIES = [
    ("Taipei", 121.5654, 25.0330),
    ("Taoyuan", 121.3010, 24.9936),
    ("Hsinchu", 120.9688, 24.8138),
    ("Taichung", 120.6736, 24.1477),
    ("Chiayi", 120.4491, 23.4800),
    ("Tainan", 120.2033, 22.9997),
    ("Kaohsiung", 120.3014, 22.6273),
    ("Pingtung", 120.4884, 22.6761),
    ("Taitung", 121.1444, 22.7583),
    ("Hualien", 121.6068, 23.9872),
    ("Yilan", 121.7533, 24.7570),
    ("Keelung", 121.7462, 25.1276)
]

N = len(CITIES)

def calc_dist(c1, c2):
    """計算兩城市間歐式直線距離"""
    return math.sqrt((c1[1] - c2[1])**2 + (c1[2] - c2[2])**2)

# 預先計算並快取距離矩陣
DIST_MATRIX = [[calc_dist(CITIES[i], CITIES[j]) for j in range(N)] for i in range(N)]

def tour_length(tour):
    """計算完整閉合巡迴路徑總長度"""
    length = sum(DIST_MATRIX[tour[i]][tour[i + 1]] for i in range(len(tour) - 1))
    length += DIST_MATRIX[tour[-1]][tour[0]]
    return length

def format_tour(tour):
    """輸出城市走訪路徑字串"""
    return " -> ".join(CITIES[i][0] for i in tour) + " -> " + CITIES[tour[0]][0]

def get_random_tour(seed=42):
    """生成隨機初始巡迴路徑"""
    rnd = random.Random(seed)
    tour = list(range(N))
    rnd.shuffle(tour)
    return tour
