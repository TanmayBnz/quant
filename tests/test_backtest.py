import pandas as pd
import pytest

from quant_core.backtest import BacktestConfig, run_backtest, run_batch_backtest


class AlwaysLong:
    name = "always long"

    def generate_targets(self, prices: pd.DataFrame) -> pd.Series:
        return pd.Series(1.0, index=prices.index, name="target")


class FlipOnce:
    name = "flip once"

    def generate_targets(self, prices: pd.DataFrame) -> pd.Series:
        return pd.Series([0.0, 1.0, -1.0, -1.0], index=prices.index, name="target")


@pytest.fixture
def rising_prices() -> pd.DataFrame:
    index = pd.bdate_range("2024-01-02", periods=4)
    return pd.DataFrame({"close": [100.0, 110.0, 121.0, 133.1]}, index=index)


def test_signal_is_shifted_before_it_earns_returns(rising_prices: pd.DataFrame) -> None:
    result = run_backtest(
        rising_prices,
        AlwaysLong(),
        BacktestConfig(initial_capital=100.0, commission_bps=0, slippage_bps=0),
    )

    assert result.history["position"].tolist() == [0.0, 1.0, 1.0, 1.0]
    assert result.history["strategy_return"].tolist() == pytest.approx([0.0, 0.1, 0.1, 0.1])
    assert result.history["equity"].iloc[-1] == pytest.approx(133.1)


def test_cost_is_charged_on_turnover(rising_prices: pd.DataFrame) -> None:
    result = run_backtest(
        rising_prices,
        FlipOnce(),
        BacktestConfig(initial_capital=100.0, commission_bps=10, slippage_bps=0),
    )

    assert result.history["position"].tolist() == [0.0, 0.0, 1.0, -1.0]
    assert result.history["turnover"].tolist() == [0.0, 0.0, 1.0, 2.0]
    assert result.history["trading_cost"].tolist() == pytest.approx([0.0, 0.0, 0.001, 0.002])


def test_rejects_target_outside_supported_leverage(rising_prices: pd.DataFrame) -> None:
    class Leveraged:
        name = "leveraged"

        def generate_targets(self, prices: pd.DataFrame) -> pd.Series:
            return pd.Series(2.0, index=prices.index)

    with pytest.raises(ValueError, match="between -1 and 1"):
        run_backtest(rising_prices, Leveraged())


def test_rejects_insolvent_short_strategy() -> None:
    index = pd.bdate_range("2024-01-02", periods=3)
    prices = pd.DataFrame({"close": [100.0, 100.0, 250.0]}, index=index)

    class AlwaysShort:
        name = "always short"

        def generate_targets(self, prices: pd.DataFrame) -> pd.Series:
            return pd.Series(-1.0, index=prices.index)

    with pytest.raises(ValueError, match="became insolvent"):
        run_backtest(
            prices,
            AlwaysShort(),
            BacktestConfig(commission_bps=0, slippage_bps=0),
        )


def test_batch_backtest_compares_tickers_and_preserves_partial_failures(
    rising_prices: pd.DataFrame,
) -> None:
    invalid = rising_prices.copy()
    invalid.iloc[1, 0] = -1
    batch = run_batch_backtest(
        {"GOOD": rising_prices, "BAD": invalid},
        AlwaysLong(),
        BacktestConfig(commission_bps=0, slippage_bps=0),
    )

    assert list(batch.results) == ["GOOD"]
    assert "BAD" in batch.failures
    comparison = batch.comparison_frame()
    assert comparison.index.tolist() == ["GOOD"]
    assert comparison.loc["GOOD", "observations"] == 4
    assert comparison.loc["GOOD", "benchmark_return"] == pytest.approx(0.331)
