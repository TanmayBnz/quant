---
type: skill
category: practice
level: working
tracks: [quant, systems]
evidence: ["[[Strategy Backtesting Engine]]"]
keywords: [commissions, slippage, basis points, turnover, spread, market impact, execution]
---
# Costs and execution

## Current cost model

The engine combines commission and slippage in basis points:

```text
cost_rate = (commission_bps + slippage_bps) / 10,000
trading_cost_t = turnover_t × cost_rate
```

One basis point is `0.01%`. Costs are deducted from the periodic portfolio return when
exposure changes.

## Why turnover matters

A small predictive edge can disappear when the strategy trades frequently. Reporting a
cost-free backtest without turnover says little about implementability.

## What linear cost misses

- Bid/ask spread varying by ticker and time
- Market impact increasing nonlinearly with order size
- Volume participation and partial fills
- Short borrow fees and availability
- Financing and cash yield
- Limit versus market order behavior
- Latency and intraday price movement

## Sensitivity analysis

A credible report reruns the same frozen strategy under several cost assumptions. If the
conclusion reverses after a small cost increase, the edge is fragile.

## Honest interview answer

“The current engine uses a transparent linear turnover model. It is appropriate for
comparing low-frequency ideas, not for claiming execution realism. The next upgrade would
separate commission, half-spread, market impact, and borrow costs.”
