---
type: skill
category: practice
level: working
tracks: [quant, data]
evidence: ["[[Strategy Backtesting Engine]]"]
keywords: [simple returns, compounding, portfolio accounting, long short, turnover, adjusted close]
---
# Returns and portfolio accounting

## Simple returns

For close price `P_t`:

```text
r_t = P_t / P_(t-1) - 1
```

Returns chain multiplicatively, not additively:

```text
equity_t = initial_capital × product(1 + strategy_return_i)
```

A 50% loss followed by a 50% gain leaves `0.5 × 1.5 = 0.75`, a 25% loss—not zero.

## Long and short exposure

The normalized gross return is `position × asset return`. A short position profits from a
negative asset return but has asymmetric risk: the asset can rise by more than 100%, so a
fully short strategy can lose more than its capital. The engine detects a periodic return
of `-100%` or worse and reports insolvency instead of compounding nonsensical equity.

## Turnover

```text
turnover_t = abs(position_t - position_(t-1))
```

Moving cash → long is `1×`; long → short is `2×`. This is why a direct flip receives two
sides of cost in the current model.

## Adjusted prices

The Yahoo Finance adapter requests auto-adjusted closes. Adjusted data reduces artificial
jumps from splits and incorporates distributions into the historical series. The exact
provider methodology and licensing still need to be stated in any published research.

## Interview check

**Why not add daily returns?** Because capital after each period becomes the base for the
next period; compounding is multiplicative.

**Why is the batch tester not a portfolio backtest?** Each ticker has an independent
capital account. No weights, shared cash, rebalance, or cross-asset covariance is used.
