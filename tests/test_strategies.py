import pandas as pd
import pytest

from quant_core.strategies import strategy_parameters
from strategies.moving_average import MovingAverageCrossover
from strategies.rsi_mean_reversion import RsiMeanReversion


def test_moving_average_strategy_has_warmup_period() -> None:
    index = pd.bdate_range("2024-01-02", periods=5)
    prices = pd.DataFrame({"close": [1.0, 2.0, 3.0, 4.0, 5.0]}, index=index)
    strategy = MovingAverageCrossover(fast_window=2, slow_window=3)
    assert strategy.generate_targets(prices).tolist() == [0.0, 0.0, 1.0, 1.0, 1.0]


def test_moving_average_windows_must_be_ordered() -> None:
    with pytest.raises(ValueError, match="greater"):
        MovingAverageCrossover(fast_window=20, slow_window=20)


def test_strategy_parameters_expose_ui_metadata() -> None:
    parameters = strategy_parameters(MovingAverageCrossover)
    assert [parameter.name for parameter in parameters] == ["fast_window", "slow_window"]
    assert parameters[0].label == "Fast window"
    assert parameters[0].min_value == 2


def test_rsi_handles_a_run_with_no_losses() -> None:
    index = pd.bdate_range("2024-01-02", periods=5)
    prices = pd.DataFrame({"close": [1.0, 2.0, 3.0, 4.0, 5.0]}, index=index)
    strategy = RsiMeanReversion(lookback=2, lower_threshold=30, upper_threshold=70)

    assert strategy.generate_targets(prices).tolist() == [0.0, 0.0, -1.0, -1.0, -1.0]
