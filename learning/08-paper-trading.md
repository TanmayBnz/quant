---
type: skill
category: systems
level: thin
tracks: [quant, systems, swe]
evidence: ["[[Paper Trading Risk Monitor]]"]
keywords: [paper trading, idempotency, orders, fills, reconciliation, risk monitoring]
---
# Paper trading and production risk

> Planned project; no broker or live portfolio is connected yet.

## Why paper trading

Paper trading tests the operational chain prospectively: data arrival, signal generation,
order creation, state transitions, reconciliation, and monitoring. It does not reproduce
real queue position, impact, borrow constraints, or the psychology of risking capital.

## Minimum state model

- Job run: logical date, status, input version, and error
- Signal: strategy version, ticker, target, and timestamp
- Order: stable idempotency key, requested quantity, and state
- Fill: simulated price, quantity, cost, and timestamp
- Position: quantity, cost basis, marked value, and realized/unrealized P&L

## Idempotency

Scheduled jobs retry. The same logical rebalance must not create duplicate orders. A
stable key derived from strategy, portfolio, logical date, ticker, and action makes a
rerun return the existing operation rather than placing another.

## Monitoring

Track data freshness, job latency, missing symbols, reconciliation differences, gross
and net exposure, concentration, volatility, drawdown, and P&L attribution. Alert on
actionable state changes, not every successful heartbeat.

## Backtest versus paper

Store the expected signal and assumed backtest fill beside the paper fill. Differences
can then be attributed to data revisions, timing, costs, or implementation defects rather
than vaguely labeled “model drift.”
