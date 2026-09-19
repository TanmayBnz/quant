---
type: skill
category: practice
level: working
tracks: [quant, data]
evidence: ["[[Strategy Backtesting Engine]]"]
keywords: [backtesting, signal timing, benchmark, target exposure, look-ahead bias]
---
# Backtesting fundamentals

## The question

A backtest asks: “Under an explicit information set, trading rule, execution model, and
cost model, what path would capital have followed?” It does not prove that the same path
will occur out of sample.

## Bar timing in this engine

At close `t`, a strategy can use prices through `t` to produce `target[t]`. The engine
uses:

```text
position[t] = target[t - 1]
strategy_return[t] = position[t] × asset_return[t] - trading_cost[t]
```

The shift matters. Without it, a moving average calculated with today's close could earn
the return that ended at the same close—information that was not known before the return
occurred.

## Target versus order

A target is desired exposure, not an order. In the current normalized model:

- `1` means fully long.
- `0` means cash.
- `-1` means fully short.
- Turnover is the absolute change between consecutive positions.

A production simulator would translate targets into quantities, orders, fills, cash,
fees, and positions. This engine deliberately has not made that claim yet.

## Benchmark

Every run includes buy-and-hold over the same prices. An absolute positive return is not
enough: a strategy returning 10% while the asset returns 30% has negative benchmark
relative performance.

## Implemented now

- Daily adjusted-close data
- One-period signal delay
- Long, cash, short, and fractional exposure in `[-1, 1]`
- Linear turnover costs
- Buy-and-hold benchmark
- Independent tests over several ticker histories

## Not implemented

Orders, partial fills, bid/ask quotes, volume constraints, financing, borrow availability,
dividends as cash flows, taxes, and a combined multi-asset account.
