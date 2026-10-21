"""
題目 3：自製 map, filter, reduce 函數，禁止迴圈解決泡沫排序
"""

# --- 1. 自製純遞迴高階函數（嚴格禁止使用 for / while）---

def my_map(fn, lst):
    """自製純遞迴 map"""
    if not lst:
        return []
    return [fn(lst[0])] + my_map(fn, lst[1:])


def my_filter(pred, lst):
    """自製純遞迴 filter"""
    if not lst:
        return []
    head, tail = lst[0], lst[1:]
    rest = my_filter(pred, tail)
    return [head] + rest if pred(head) else rest


def my_reduce(fn, lst, initial=None):
    """自製純遞迴 reduce"""
    if initial is None:
        if not lst:
            raise TypeError("my_reduce() 序列不可為空且無初始值")
        return my_reduce(fn, lst[1:], lst[0])
    if not lst:
        return initial
    return my_reduce(fn, lst[1:], fn(initial, lst[0]))


# --- 2. 純函數式泡沫排序（全過程禁止迴圈）---

def bubble_pass(lst):
    """單趟冒泡：純遞迴比較相鄰兩元素，將較大者後移"""
    if len(lst) <= 1:
        return lst
    head1, head2 = lst[0], lst[1]
    tail = lst[2:]
    if head1 > head2:
        return [head2] + bubble_pass([head1] + tail)
    else:
        return [head1] + bubble_pass([head2] + tail)


def make_list(n):
    """純遞迴生成長度為 n 的計數清單，取代內建 range() 迴圈物件"""
    if n <= 0:
        return []
    return make_list(n - 1) + [n - 1]


def bubble_sort(lst):
    """利用自製 my_reduce 串聯 n 趟冒泡，達成零迴圈排序"""
    passes = make_list(len(lst))
    return my_reduce(lambda cur_arr, _: bubble_pass(cur_arr), passes, lst)


if __name__ == '__main__':
    data = [64, 34, 25, 12, 22, 11, 90]
    print("--- 自製高階函數與無迴圈泡沫排序測試 ---")
    print("原始資料:", data)
    print("my_map (x * 2):", my_map(lambda x: x * 2, data))
    print("my_filter (偶數):", my_filter(lambda x: x % 2 == 0, data))
    print("my_reduce (總和):", my_reduce(lambda a, b: a + b, data, 0))
    sorted_data = bubble_sort(data)
    print("泡沫排序結果:", sorted_data)
    assert sorted_data == sorted(data), "排序結果錯誤！"
    print("測試全部通過！")
