---
type: skill
category: data
level: thin
tracks: [quant, data]
evidence: ["[[Factor Research Platform]]"]
keywords: [factor research, cross-sectional ranking, information coefficient, quantile returns, portfolio construction]
---
# Factor research and portfolio construction

> Planned project; these are requirements, not current resume claims.

## Cross-sectional versus time-series signals

A time-series signal asks whether one asset is strong relative to its own history. A
cross-sectional factor ranks assets against one another on the same date.

Examples:

- Momentum: past return, usually skipping the most recent month for a classic 12–1 form.
- Low volatility: trailing realized volatility, ranked ascending.
- Trend strength: price relative to a moving average, normalized by volatility.

## Research sequence

1. Define a point-in-time universe.
2. Calculate the raw factor using only available data.
3. Winsorize or otherwise control extreme values.
4. Rank or standardize cross-sectionally.
5. Measure information coefficient and quantile returns.
6. Convert scores into weights subject to exposure constraints.
7. Rebalance, charge costs, and compare with a benchmark.
8. Validate out of sample and across market regimes.

## Portfolio concerns

Factor returns can be disguised sector, size, beta, or liquidity exposure. Neutralization
and exposure reporting matter as much as the raw signal. Weight caps and volatility
scaling prevent a few assets from dominating.

## Metrics

Information coefficient, rank IC, quantile spread, turnover, capacity proxies, beta,
tracking error, information ratio, drawdown, and benchmark-relative attribution.
