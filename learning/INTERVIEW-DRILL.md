---
tags: [meta, spoken, quant]
---
# Quant portfolio interview drill

Answer each aloud in under 90 seconds, then point to the relevant code or test.

1. What exact information is available when a target is produced?
2. Why is the target shifted, and what bug appears without the shift?
3. Why is long-to-short turnover `2×`?
4. What does the cost model capture, and what does it omit?
5. Why can a fully short position become insolvent?
6. Why is testing three tickers independently not a portfolio backtest?
7. What does adjusted close change?
8. How would survivorship bias enter a multi-ticker experiment?
9. Why are Sharpe and max drawdown complementary?
10. How can choosing the best ticker or parameter after looking at results overfit?
11. How would you design a train/validation/test or walk-forward experiment?
12. Why are strategies plug-ins but accounting centralized?
13. What are the security consequences of dynamically importing strategy files?
14. How would you turn normalized targets into orders and positions?
15. What must be persisted to make a scheduled paper trader idempotent?

## Project summary

“I built a bias-aware research backtester that discovers typed strategy plug-ins, runs
the same assumptions independently across several symbols, models turnover costs, and
compares strategy and benchmark risk metrics. I kept synthetic data as the reproducible
default and added an optional real-data adapter. The current limitation is deliberate:
it is a close-to-close research engine, not yet a multi-asset portfolio or execution
simulator.”
