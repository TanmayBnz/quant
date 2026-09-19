"""Performance and risk metrics with explicit edge-case behavior."""

from __future__ import annotations

import math

import numpy as np
import pandas as pd


def max_drawdown(equity: pd.Series) -> float:
    if equity.empty:
        return 0.0
    drawdown = equity / equity.cummax() - 1
    return float(drawdown.min())


def performance_summary(
    returns: pd.Series,
    equity: pd.Series,
    *,
    positions: pd.Series | None = None,
    turnover: pd.Series | None = None,
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> dict[str, float]:
    """Calculate a concise research tear sheet from periodic returns."""

    if len(returns) != len(equity):
        raise ValueError("returns and equity must have the same length")
    if returns.empty:
        raise ValueError("returns must not be empty")

    total_return = float(equity.iloc[-1] / equity.iloc[0] - 1)
    elapsed_periods = max(len(returns) - 1, 1)
    annualized_return = float((1 + total_return) ** (periods_per_year / elapsed_periods) - 1)
    annualized_volatility = float(returns.std(ddof=1) * math.sqrt(periods_per_year))

    daily_risk_free = risk_free_rate / periods_per_year
    excess = returns - daily_risk_free
    excess_std = excess.std(ddof=1)
    sharpe = (
        0.0
        if not np.isfinite(excess_std) or excess_std == 0
        else float(excess.mean() / excess_std * math.sqrt(periods_per_year))
    )

    downside = excess.clip(upper=0)
    downside_deviation = float(np.sqrt((downside**2).mean()) * math.sqrt(periods_per_year))
    sortino = (
        0.0
        if downside_deviation == 0
        else float((excess.mean() * periods_per_year) / downside_deviation)
    )

    summary = {
        "total_return": total_return,
        "annualized_return": annualized_return,
        "annualized_volatility": annualized_volatility,
        "sharpe_ratio": sharpe,
        "sortino_ratio": sortino,
        "max_drawdown": max_drawdown(equity),
    }
    if positions is not None:
        summary["average_abs_exposure"] = float(positions.abs().mean())
    if turnover is not None:
        summary["total_turnover"] = float(turnover.sum())
    return summary
