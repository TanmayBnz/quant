import pandas as pd
import pytest

from quant_core.metrics import max_drawdown, performance_summary


def test_max_drawdown() -> None:
    equity = pd.Series([100.0, 120.0, 90.0, 108.0])
    assert max_drawdown(equity) == pytest.approx(-0.25)


def test_flat_returns_have_zero_sharpe_and_sortino() -> None:
    returns = pd.Series([0.0, 0.0, 0.0])
    equity = pd.Series([100.0, 100.0, 100.0])
    summary = performance_summary(returns, equity)
    assert summary["sharpe_ratio"] == 0.0
    assert summary["sortino_ratio"] == 0.0
