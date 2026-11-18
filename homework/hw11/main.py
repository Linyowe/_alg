"""數值微積分與蒙地卡羅法作業

AI 使用聲明：本程式由 ChatGPT（生成式 AI）協助撰寫與整理，
包含程式架構、函式實作、測試案例及註解。使用者應自行閱讀、理解，
並依課堂要求確認及修改後再繳交。

執行方式：python main.py
僅使用 Python 標準函式庫，不需安裝第三方套件。
"""

from __future__ import annotations

import itertools
import math
import random
from typing import Callable, Sequence


# 函式型別：單變數函式，以及接收 n 維座標陣列的函式
Function1D = Callable[[float], float]
FunctionND = Callable[[Sequence[float]], float]

# 第 5 題：限制黎曼法最多計算的格子數，避免高維度執行時間失控。
MAX_RIEMANN_CELLS = 100_000


def _check_sample_count(n: int) -> None:
    """檢查取樣數量是否為正整數。"""
    if not isinstance(n, int) or n <= 0:
        raise ValueError("取樣數 n 必須是正整數")


def _check_bounds(low: Sequence[float], high: Sequence[float]) -> None:
    """檢查 n 維積分上下界。"""
    if len(low) == 0:
        raise ValueError("積分維度至少必須為 1")
    if len(low) != len(high):
        raise ValueError("low 和 high 的長度必須相同")
    for i, (a, b) in enumerate(zip(low, high)):
        if b < a:
            raise ValueError(f"第 {i + 1} 維的 high 不可小於 low")


# ----------------------------------------------------------------------
# 第 1 題：單變數數值微分與數值積分
# ----------------------------------------------------------------------

def diff(f: Function1D, x: float, h: float = 1e-5) -> float:
    """使用中央差分近似單變數函式在 x 的一階導數。

    f'(x) ≈ [f(x+h) - f(x-h)] / (2h)
    """
    if h <= 0:
        raise ValueError("h 必須大於 0")
    return (f(x + h) - f(x - h)) / (2.0 * h)


def integral_midpoint(
    f: Function1D, low: float, high: float, n: int = 10_000
) -> float:
    """使用中點黎曼和近似單變數定積分。"""
    _check_sample_count(n)
    step = (high - low) / n
    total = 0.0
    for i in range(n):
        x_mid = low + (i + 0.5) * step
        total += f(x_mid)
    return total * step


def integral_simpson(
    f: Function1D, low: float, high: float, n: int = 1_000
) -> float:
    """使用複合辛普森法近似單變數定積分；區間數會調整為偶數。"""
    _check_sample_count(n)
    if n % 2 == 1:
        n += 1

    step = (high - low) / n
    total = f(low) + f(high)
    for i in range(1, n):
        x = low + i * step
        total += (4 if i % 2 == 1 else 2) * f(x)
    return total * step / 3.0


# ----------------------------------------------------------------------
# 第 2 題：蒙地卡羅法計算單變數積分
# ----------------------------------------------------------------------

def mc_integral_1d(
    f: Function1D,
    low: float,
    high: float,
    n_samples: int = 100_000,
    seed: int | None = 42,
) -> float:
    """使用均勻隨機取樣近似單變數定積分。

    integral ≈ (high-low) * average(f(random point))
    seed 設為固定整數時，每次執行可得到相同結果，方便測試。
    """
    _check_sample_count(n_samples)
    rng = random.Random(seed)
    total = 0.0
    for _ in range(n_samples):
        x = rng.uniform(low, high)
        total += f(x)
    return (high - low) * total / n_samples


# ----------------------------------------------------------------------
# 第 3 題：n 變數數值微分（梯度）與數值積分（超體積）
# ----------------------------------------------------------------------

def gradient(
    f: FunctionND, x: Sequence[float], h: float = 1e-6
) -> list[float]:
    """使用中央差分計算 n 變數函式在 x 點的梯度。"""
    if len(x) == 0:
        raise ValueError("x 至少需要一個維度")
    if h <= 0:
        raise ValueError("h 必須大於 0")

    result: list[float] = []
    for i in range(len(x)):
        x_plus = list(x)
        x_minus = list(x)
        x_plus[i] += h
        x_minus[i] -= h
        partial = (f(x_plus) - f(x_minus)) / (2.0 * h)
        result.append(partial)
    return result


def integral_grid(
    f: FunctionND,
    low: Sequence[float],
    high: Sequence[float],
    k: int = 20,
    max_cells: int = 1_000_000,
) -> float:
    """使用 n 維中點黎曼和計算超體積。

    每個維度切成 k 段，總格子數為 k ** n。
    此方法適合低維度；維度增加時，格子數會快速成長。
    """
    _check_bounds(low, high)
    _check_sample_count(k)
    _check_sample_count(max_cells)

    dimensions = len(low)
    cell_count = k ** dimensions
    if cell_count > max_cells:
        raise ValueError(
            f"格子數 k^n={cell_count:,} 超過上限 {max_cells:,}；"
            "請降低 k 或改用蒙地卡羅法。"
        )

    widths = [high[i] - low[i] for i in range(dimensions)]
    cell_volume = math.prod(width / k for width in widths)

    total = 0.0
    for cell in itertools.product(range(k), repeat=dimensions):
        point = [
            low[i] + (cell[i] + 0.5) * widths[i] / k
            for i in range(dimensions)
        ]
        total += f(point)

    return total * cell_volume


# ----------------------------------------------------------------------
# 第 4 題：蒙地卡羅法計算 n 變數積分（超體積）
# ----------------------------------------------------------------------

def mc_integral_n(
    f: FunctionND,
    low: Sequence[float],
    high: Sequence[float],
    n_samples: int = 100_000,
    seed: int | None = 42,
) -> float:
    """使用 n 維超方體內的均勻隨機點估算積分。"""
    _check_bounds(low, high)
    _check_sample_count(n_samples)

    rng = random.Random(seed)
    dimensions = len(low)
    volume = math.prod(high[i] - low[i] for i in range(dimensions))

    total = 0.0
    for _ in range(n_samples):
        point = [rng.uniform(low[i], high[i]) for i in range(dimensions)]
        total += f(point)

    return volume * total / n_samples


# ----------------------------------------------------------------------
# 第 5 題：黎曼積分法 integral(f, low, high)，維度由陣列長度決定
# ----------------------------------------------------------------------

def riemann_subdivisions(dimensions: int) -> int:
    """依照格子數上限，計算每個維度可切分的段數 k。"""
    if dimensions <= 0:
        raise ValueError("dimensions 必須大於 0")
    return max(1, int(MAX_RIEMANN_CELLS ** (1.0 / dimensions)))


def integral(
    f: FunctionND, low: Sequence[float], high: Sequence[float]
) -> float:
    """以 n 維中點黎曼和計算積分，n = len(low) = len(high)。

    為控制運算量，所有維度的格子總數不超過 MAX_RIEMANN_CELLS。
    因此每維切分數 k = floor(MAX_RIEMANN_CELLS ** (1/n))。
    例如 100 維時 k=1，只能用整個超立方體的中心點估算，
    這是非常粗略的黎曼和；程式不會把它假稱為蒙地卡羅法。
    """
    _check_bounds(low, high)
    k = riemann_subdivisions(len(low))

    widths = [high[i] - low[i] for i in range(len(low))]
    cell_volume = math.prod(width / k for width in widths)

    total = 0.0
    for cell in itertools.product(range(k), repeat=len(low)):
        point = [
            low[i] + (cell[i] + 0.5) * widths[i] / k
            for i in range(len(low))
        ]
        total += f(point)

    return total * cell_volume


# ----------------------------------------------------------------------
# 第 6 題：改用蒙地卡羅法，使用相同的 n 維積分題目
# ----------------------------------------------------------------------

def integral_mc(
    f: FunctionND,
    low: Sequence[float],
    high: Sequence[float],
    n_samples: int = 200_000,
    seed: int | None = 42,
) -> float:
    """蒙地卡羅法版本的通用 n 維積分函式。"""
    return mc_integral_n(f, low, high, n_samples=n_samples, seed=seed)


# ----------------------------------------------------------------------
# 測試範例：執行 python main.py 即會依序執行全部測試
# ----------------------------------------------------------------------

def test_q1() -> None:
    print("\n========== 第 1 題：單變數數值微分與積分 ==========")
    f = lambda x: x ** 2

    derivative = diff(f, 2.0)
    midpoint = integral_midpoint(f, 0.0, 1.0)
    simpson = integral_simpson(f, 0.0, 1.0)
    sin_integral = integral_simpson(math.sin, 0.0, math.pi)

    print(f"f(x)=x^2，f'(2) 中央差分 = {derivative:.10f}（正解 4）")
    print(f"積分 x^2，區間 [0,1] 中點法 = {midpoint:.10f}（正解 1/3）")
    print(f"積分 x^2，區間 [0,1] 辛普森法 = {simpson:.10f}（正解 1/3）")
    print(f"積分 sin(x)，區間 [0,pi] 辛普森法 = {sin_integral:.10f}（正解 2）")

    assert abs(derivative - 4.0) < 1e-7
    assert abs(midpoint - 1.0 / 3.0) < 1e-8
    assert abs(simpson - 1.0 / 3.0) < 1e-10
    assert abs(sin_integral - 2.0) < 1e-10
    print("第 1 題測試通過。")


def test_q2() -> None:
    print("\n========== 第 2 題：蒙地卡羅法單變數積分 ==========")
    f = lambda x: x ** 2
    estimate_10k = mc_integral_1d(f, 0.0, 1.0, 10_000, seed=2026)
    estimate_100k = mc_integral_1d(f, 0.0, 1.0, 100_000, seed=2026)
    sin_estimate = mc_integral_1d(math.sin, 0.0, math.pi, 100_000, seed=2026)

    print(f"積分 x^2，N=10,000  = {estimate_10k:.8f}（正解 0.33333333）")
    print(f"積分 x^2，N=100,000 = {estimate_100k:.8f}（正解 0.33333333）")
    print(f"積分 sin(x)，N=100,000 = {sin_estimate:.8f}（正解 2）")

    assert abs(estimate_100k - 1.0 / 3.0) < 0.005
    assert abs(sin_estimate - 2.0) < 0.01
    print("第 2 題測試通過。")


def test_q3() -> None:
    print("\n========== 第 3 題：n 變數梯度與數值積分 ==========")
    f = lambda x: sum(value ** 2 for value in x)

    grad = gradient(f, [1.0, 2.0, 3.0])
    print(f"f(x)=x1^2+x2^2+x3^2，在 [1,2,3] 的梯度 = {[round(v, 6) for v in grad]}")
    print("梯度正解 = [2, 4, 6]")
    assert all(abs(a - b) < 1e-5 for a, b in zip(grad, [2.0, 4.0, 6.0]))

    value_2d = integral_grid(f, [0.0, 0.0], [1.0, 1.0], k=200)
    value_3d = integral_grid(f, [0.0] * 3, [1.0] * 3, k=40)
    print(f"2 維中點黎曼積分 = {value_2d:.8f}（正解 2/3）")
    print(f"3 維中點黎曼積分 = {value_3d:.8f}（正解 1）")
    assert abs(value_2d - 2.0 / 3.0) < 1e-4
    assert abs(value_3d - 1.0) < 1e-3
    print("第 3 題測試通過。")


def test_q4() -> None:
    print("\n========== 第 4 題：蒙地卡羅法 n 變數積分 ==========")
    f = lambda x: sum(value ** 2 for value in x)

    for dimensions in (2, 5):
        low = [0.0] * dimensions
        high = [1.0] * dimensions
        estimate = mc_integral_n(
            f, low, high, n_samples=100_000, seed=2026 + dimensions
        )
        exact = dimensions / 3.0
        print(f"{dimensions:2d} 維蒙地卡羅積分 = {estimate:.8f}（正解 {exact:.8f}）")
        assert abs(estimate - exact) < 0.03
    print("第 4 題測試通過。")


def test_q5() -> None:
    print("\n========== 第 5 題：n 維黎曼積分 integral(f, low, high) ==========")
    f = lambda x: sum(value ** 2 for value in x)

    for dimensions in (1, 2, 5, 100):
        low = [0.0] * dimensions
        high = [1.0] * dimensions
        estimate = integral(f, low, high)
        exact = dimensions / 3.0
        k = riemann_subdivisions(dimensions)
        cells = k ** dimensions
        error_percent = abs(estimate - exact) / exact * 100.0
        print(
            f"{dimensions:3d} 維：每維切 k={k}，格子數={cells:,}，"
            f"估算={estimate:.8f}，正解={exact:.8f}，誤差={error_percent:.2f}%"
        )

        if dimensions < 100:
            assert abs(estimate - exact) / exact < 0.01
        else:
            # 100 維時受格子數上限限制，k=1，中心點每個座標皆為 0.5，
            # 因此 f(0.5,...,0.5) = 100 * 0.25 = 25。這是刻意展示的粗略結果。
            assert k == 1
            assert abs(estimate - 25.0) < 1e-10
    print("第 5 題測試通過（100 維結果會明顯受維度災難影響）。")


def test_q6() -> None:
    print("\n========== 第 6 題：n 維蒙地卡羅積分 integral_mc ==========")
    f = lambda x: sum(value ** 2 for value in x)

    for dimensions in (1, 2, 5, 100):
        low = [0.0] * dimensions
        high = [1.0] * dimensions
        estimate = integral_mc(
            f, low, high, n_samples=200_000, seed=2026 + dimensions
        )
        exact = dimensions / 3.0
        error_percent = abs(estimate - exact) / exact * 100.0
        print(
            f"{dimensions:3d} 維：估算={estimate:.8f}，"
            f"正解={exact:.8f}，誤差={error_percent:.3f}%"
        )
        assert abs(estimate - exact) / exact < 0.01
    print("第 6 題測試通過。")


def run_all_tests() -> None:
    """依序執行六題測試。"""
    test_q1()
    test_q2()
    test_q3()
    test_q4()
    test_q5()
    test_q6()
    print("\n========================================")
    print("全部六題測試完成！")
    print("========================================")


if __name__ == "__main__":
    run_all_tests()
