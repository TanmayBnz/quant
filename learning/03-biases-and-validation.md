---
type: skill
category: practice
level: working
tracks: [quant, data, ml]
evidence: ["[[Strategy Backtesting Engine]]"]
keywords: [look-ahead bias, survivorship bias, data snooping, overfitting, walk-forward validation]
---
# Biases and validation

## Look-ahead bias

Using information before it was available. The engine prevents the most immediate form
by shifting targets one row before applying returns. That does not automatically make an
entire dataset point-in-time correct.

## Survivorship bias

Testing today's constituents over the past excludes firms that failed, merged, or left
an index. Multi-ticker input does not solve this. A factor project needs dated universe
membership or an explicit survivorship-biased limitation.

## Selection and multiple-testing bias

Trying many tickers and parameters, then reporting only the best, turns noise into an
apparently strong strategy. Cross-ticker comparison is a robustness diagnostic only when
the universe and decision rule were chosen before inspecting results.

## Overfitting

Parameter tuning spends statistical information. A robust workflow separates:

1. Hypothesis formation
2. Training or exploration interval
3. Validation interval
4. Final untouched test interval

Walk-forward testing repeatedly trains on the past and evaluates on the next unseen
window, better matching how a strategy would have been updated through time.

## Other biases to name

- **Data snooping:** repeated reuse of the same test period.
- **Publication bias:** failed strategies disappear from the record.
- **Corporate-action errors:** unadjusted splits or distributions create fake returns.
- **Timestamp leakage:** daily values may be published after the close or revised later.
- **Universe leakage:** requiring future liquidity or history to enter the sample.

## Implemented now versus planned

The one-row execution delay is implemented and tested. Walk-forward evaluation,
point-in-time universes, and multiple-testing corrections are planned; do not claim them
as current features.
