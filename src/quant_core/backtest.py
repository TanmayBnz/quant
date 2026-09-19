"""A compact close-to-close backtesting engine."""

from __future__ import annotations

from dataclasses import dataclass

import pandas as pd

from quant_core.data import validate_prices
from quant_core.metrics import performance_summary
from quant_core.strategies import Strategy


@dataclass(frozen=True)
class BacktestConfig:
    initial_capital: float = 100_000.0
    commission_bps: float = 1.0
    slippage_bps: float = 2.0
    periods_per_year: int = 252

    def __post_init__(self) -> None:
        if self.initial_capital <= 0:
            raise ValueError("initial_capital must be positive")
        if self.commission_bps < 0 or self.slippage_bps < 0:
            raise ValueError("trading costs must be non-negative")
        if self.periods_per_year <= 0:
            raise ValueError("periods_per_year must be positive")


@dataclass(frozen=True)
class BacktestResult:
    strategy_name: str
    history: pd.DataFrame
    metrics: dict[str, float]


@dataclass(frozen=True)
class BatchBacktestResult:
    results: dict[str, BacktestResult]
    failures: dict[str, str]

    def comparison_frame(self) -> pd.DataFrame:
        """Return one row of comparable metrics per successful ticker."""

        rows: list[dict[str, float | int | str]] = []
        for ticker, result in self.results.items():
            history = result.history
            benchmark_return = float(
                history["benchmark_equity"].iloc[-1] / history["benchmark_equity"].iloc[0] - 1
            )
            rows.append(
                {
                    "ticker": ticker,
                    **result.metrics,
                    "benchmark_return": benchmark_return,
                    "excess_return": result.metrics["total_return"] - benchmark_return,
                    "observations": len(history),
                }
            )
        if not rows:
            return pd.DataFrame()
        return pd.DataFrame(rows).set_index("ticker").sort_index()


def run_backtest(
    prices: pd.DataFrame,
    strategy: Strategy,
    config: BacktestConfig | None = None,
) -> BacktestResult:
    """Run a single-asset backtest without same-bar look-ahead.

    Targets generated using close ``t`` are shifted before they are multiplied by
    returns, so they first earn the return ending at ``t + 1``.
    """

    config = config or BacktestConfig()
    clean_prices = validate_prices(prices)
    raw_target = strategy.generate_targets(clean_prices).reindex(clean_prices.index)
    if raw_target.isna().any():
        raise ValueError("strategy targets must be defined for every price row")
    if ((raw_target < -1) | (raw_target > 1)).any():
        raise ValueError("strategy targets must be between -1 and 1")

    history = clean_prices.copy()
    history["asset_return"] = history["close"].pct_change().fillna(0.0)
    history["target"] = raw_target.astype(float)
    history["position"] = history["target"].shift(1).fillna(0.0)
    history["turnover"] = history["position"].diff().abs().fillna(history["position"].abs())

    cost_rate = (config.commission_bps + config.slippage_bps) / 10_000
    history["trading_cost"] = history["turnover"] * cost_rate
    history["gross_return"] = history["position"] * history["asset_return"]
    history["strategy_return"] = history["gross_return"] - history["trading_cost"]
    if (history["strategy_return"] <= -1).any():
        insolvency_date = history.index[history["strategy_return"] <= -1][0]
        raise ValueError(f"strategy became insolvent on {insolvency_date.date()}")
    history["equity"] = config.initial_capital * (1 + history["strategy_return"]).cumprod()
    history["benchmark_equity"] = config.initial_capital * (1 + history["asset_return"]).cumprod()
    history["drawdown"] = history["equity"] / history["equity"].cummax() - 1

    metrics = performance_summary(
        history["strategy_return"],
        history["equity"],
        positions=history["position"],
        turnover=history["turnover"],
        periods_per_year=config.periods_per_year,
    )
    return BacktestResult(strategy_name=strategy.name, history=history, metrics=metrics)


def run_batch_backtest(
    prices_by_ticker: dict[str, pd.DataFrame],
    strategy: Strategy,
    config: BacktestConfig | None = None,
) -> BatchBacktestResult:
    """Apply one strategy/configuration independently across several tickers."""

    if not prices_by_ticker:
        raise ValueError("prices_by_ticker must not be empty")

    results: dict[str, BacktestResult] = {}
    failures: dict[str, str] = {}
    for ticker, prices in prices_by_ticker.items():
        try:
            results[ticker] = run_backtest(prices, strategy, config)
        except (TypeError, ValueError) as exc:
            failures[ticker] = str(exc)
    return BatchBacktestResult(results=results, failures=failures)
