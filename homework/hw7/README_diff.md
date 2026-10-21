# 文字比對演算法專題：動態規劃（LCS）v.s. 非動態規劃（Myers 差異演算法）

本專案針對文字與檔案差異比對（`diff`）問題，分別實作經典的**動態規劃（LCS DP）**與工業界標準**非動態規劃（Myers Diff 演算法）**，並進行演算法複雜度分析與效能實測對決。

---

## 目錄結構

```text
.
├── diff_dp.py          # 解法 1：動態規劃（LCS DP）實作
├── diff_myers.py       # 解法 2：非動態規劃（Myers 貪婪編輯圖搜尋）實作
├── benchmark_diff.py   # 效能基準對決測試腳本
└── README_diff.md      # 專題分析與實測報告（本文件）
