# Lambda Calculus 解譯器（有名稱版本）

本專案實作一個具備完整逐步計算追蹤能力的 **Lambda Calculus（λ-演算）解譯器**。能解析抽象語法樹（AST）、自動處理變數衝突（α-轉換），並透過正規序（Normal Order）進行逐步 β-規約，完整顯示每一次代換的計算軌跡。

---

## 目錄結構

```text
.
├── lambda_interpreter.py   # Lambda Calculus 解譯器核心（含 Lexer, Parser, AST, Evaluator）
├── test_programs.py        # 經典 Lambda Calculus 測試程式集（布林、邱奇數、組合子）
└── README_lambda.md        # 專案說明與計算過程文件（本文件）
