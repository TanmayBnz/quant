---
type: skill
category: practice
level: working
tracks: [quant, data]
evidence: ["[[Strategy Backtesting Engine]]"]
keywords: [CAGR, volatility, Sharpe ratio, Sortino ratio, max drawdown, exposure, turnover]
---
# Risk and performance metrics

## Total return and CAGR

Total return measures endpoint growth. CAGR converts it to an annualized compound rate:

```text
CAGR = (ending / beginning)^(periods_per_year / elapsed_periods) - 1
```

CAGR hides the path. Two strategies can have the same CAGR and radically different
drawdowns.

## Volatility and Sharpe ratio

Annualized volatility is daily return standard deviation times `sqrt(252)`. Sharpe is
annualized average excess return divided by volatility. It assumes volatility is a useful
proxy for risk and is sensitive to non-normal returns, autocorrelation, and the sampling
interval.

## Sortino ratio

Sortino replaces total volatility with downside deviation. It avoids penalizing upside
variation, but still inherits estimation error and threshold choices.

## Drawdown

```text
running_peak_t = max(equity_0 ... equity_t)
drawdown_t = equity_t / running_peak_t - 1
max_drawdown = min(drawdown_t)
```

Drawdown answers a path-dependent question that Sharpe cannot: how far below a prior
peak the strategy fell. Recovery time is another useful but not yet implemented measure.

## Exposure and turnover

Average absolute exposure distinguishes a low-risk strategy from one that is simply out
of the market. Turnover indicates how much trading was required to produce returns and
connects the signal directly to implementation costs.

## Interview check

Never present a metric alone. Pair return with a benchmark, Sharpe with drawdown, and
gross performance with costs and turnover.
